# pip install azure-identity azure-mgmt-resource azure-mgmt-compute azure-mgmt-storage azure-mgmt-network
import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient


# Initialize Azure credentials and subscription ID
credential = DefaultAzureCredential()
subscription_id = "7ceee2ac-3bca-4342-8d4e-725195bd5865"

# Initialize Azure management clients
resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)
storage_client = StorageManagementClient(credential, subscription_id)
network_client = NetworkManagementClient(credential, subscription_id)

# Basic level of resource pulling implemented here.
# Can be expanded later to include more detailed configuration information per resource type.
def fetch_azure_resources():
    resources = []

    # fetch resource groups as list
    resource_groups = resource_client.resource_groups.list()
    for resource_group in resource_groups:
        resources.append({
            "type": "Resource Group",
            "name": resource_group.name,
            "location": resource_group.location
        })

    # fetch virtual machines (tags + public IP check)
    virtual_machines = compute_client.virtual_machines.list_all()
    for vm in virtual_machines:
        vm_rg = vm.id.split('/')[4]
        tags = vm.tags if vm.tags else {}
        public_ips = []

        # check NICs attached to VM for public IPs
        for nic_ref in vm.network_profile.network_interfaces:
            nic_id = nic_ref.id
            nic_name = nic_id.split('/')[-1]
            nic_rg = nic_id.split('/')[4]
            try:
                nic = network_client.network_interfaces.get(nic_rg, nic_name)
                for ip_cfg in nic.ip_configurations:
                    if ip_cfg.public_ip_address:
                        # public_ip_address is a resource reference; try to read actual IP
                        pip_id = ip_cfg.public_ip_address.id
                        pip_name = pip_id.split('/')[-1]
                        pip_rg = pip_id.split('/')[4]
                        try:
                            pip = network_client.public_ip_addresses.get(pip_rg, pip_name)
                            public_ips.append(pip.ip_address)
                        except Exception:
                            # If we can't resolve the public IP resource, store the resource id
                            public_ips.append({"public_ip_id": pip_id})
            except Exception:
                pass

        resources.append({
            "type": "Virtual Machine",
            "name": vm.name,
            "location": vm.location,
            "resource_group": vm_rg,
            "tags": tags,
            "public_ips": public_ips
        })

    # fetch storage accounts (encryption + secure transfer)
    storage_accounts = storage_client.storage_accounts.list()
    for account in storage_accounts:
        sa_rg = account.id.split('/')[4]
        try:
            account_props = storage_client.storage_accounts.get_properties(sa_rg, account.name)
        except Exception:
            account_props = None

        # extract encryption and secure transfer fields
        encryption_enabled = None
        secure_transfer_required = None
        if account_props:
            try:
                # account_props.encryption.services.blob may exist
                encryption_enabled = bool(account_props.encryption.services.blob.enabled)
            except Exception:
                encryption_enabled = None
            try:
                secure_transfer_required = bool(account_props.enable_https_traffic_only)
            except Exception:
                secure_transfer_required = None

        resources.append({
            "type": "Storage Account",
            "name": account.name,
            "location": account.location,
            "resource_group": sa_rg,
            "encryption_enabled": encryption_enabled,
            "secure_transfer_required": secure_transfer_required
        })

    # fetch Network Security Groups (capture inbound rules)
    network_sgs = network_client.network_security_groups.list_all()
    for nsg in network_sgs:
        nsg_rg = nsg.id.split('/')[4]
        # call get to ensure full details of security_rules
        try:
            nsg_detail = network_client.network_security_groups.get(nsg_rg, nsg.name)
            rules_source = nsg_detail.security_rules or []
        except Exception:
            rules_source = nsg.security_rules or []

        inbound_rules = []
        for rule in rules_source:
            # Some rule fields may be None; extract safely
            inbound_rules.append({
                "name": getattr(rule, "name", None),
                "access": getattr(rule, "access", None),
                "direction": getattr(rule, "direction", None),
                "protocol": getattr(rule, "protocol", None),
                "source_address_prefix": getattr(rule, "source_address_prefix", None),
                "destination_port_range": getattr(rule, "destination_port_range", None)
            })

        resources.append({
            "type": "Network Security Group",
            "name": nsg.name,
            "location": nsg.location,
            "resource_group": nsg_rg,
            "inbound_rules": inbound_rules
        })

    # fetch VM network interfaces (detailed ip configs)
    network_interfaces = network_client.network_interfaces.list_all()
    for nic in network_interfaces:
        ip_configs = []
        has_public_ip = False
        for ip_cfg in nic.ip_configurations:
            ip_data = {
                "private_ip": getattr(ip_cfg, "private_ip_address", None)
            }
            if getattr(ip_cfg, "public_ip_address", None):
                has_public_ip = True
                pip_id = ip_cfg.public_ip_address.id
                pip_name = pip_id.split('/')[-1]
                pip_rg = pip_id.split('/')[4]
                try:
                    pip = network_client.public_ip_addresses.get(pip_rg, pip_name)
                    ip_data["public_ip"] = pip.ip_address
                except Exception:
                    ip_data["public_ip_id"] = pip_id
            ip_configs.append(ip_data)

        resources.append({
            "type": "Network Interface",
            "name": nic.name,
            "location": nic.location,
            "resource_group": nic.id.split('/')[4],
            "ip_configurations": ip_configs,
            "has_public_ip": has_public_ip
        })

    return resources


if __name__ == "__main__":
    resources = fetch_azure_resources()
    with open("azure_resources.json", "w") as file:
        json.dump(resources, file, indent=4)
    print("Resource data saved to azure_resources.json")

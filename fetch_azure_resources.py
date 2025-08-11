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

# Fetch Azure resources and their configuration
# Can be expanded later to include more detailed configuration information per resource types.
# Additional Compliance rules/checks might need more detailed information to be fetched/pulled
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

    # fetch virtual machines details and configuration
    # Include type (vm), name, location, resource group, tags, and public IPs
    # Note: Public IPs are fetched from the NICs attached to the VM then append to the VM resource
    #       This is because VMs do not directly expose public IPs in their properties.
    # Note: NICs are fetched separately to get detailed IP configurations
    virtual_machines = compute_client.virtual_machines.list_all()
    for vm in virtual_machines:
        vm_resource_group = vm.id.split('/')[4]
        public_ips = []     
        if vm.tags:
            tags = vm.tags
        else:
            tags = []

        # check NICs attached to VM for public IPs
        for nic_reference in vm.network_profile.network_interfaces:
            nic_id = nic_reference.id
            nic_name = nic_id.split('/')[-1] # extract NIC name from resource ID
            nic_resource_group = nic_id.split('/')[4] # extract resource group from resource ID
            try:
                # retrieve NIC details using NIC resource group and name
                nic = network_client.network_interfaces.get(nic_resource_group, nic_name)

                # check each IP configuration on the NIC for a public IP address
                # Note: public_ip_address is a resource reference, so we need to resolve it
                for ip_config in nic.ip_configurations:
                    if ip_config.public_ip_address:
                        # public_ip_address is a resource reference; try to read actual IP
                        public_ip_id = ip_config.public_ip_address.id

                        public_ip_name = public_ip_id.split('/')[-1] # extract public IP name from resource ID
                        public_ip_resource_group = public_ip_id.split('/')[4] # extract resource group from public IP resource ID

                        try:
                            # retrieve the actual public IP resource to get the IP address string
                            public_ip = network_client.public_ip_addresses.get(public_ip_resource_group, public_ip_name)
                            public_ips.append(public_ip.ip_address)
                        except Exception:
                            # If we can't resolve the public IP resource, store the resource id
                            public_ips.append({"public_ip_id": public_ip_id})
            except Exception:
                pass

        # append the collected VM information into the resources list        
        resources.append({
            "type": "Virtual Machine",
            "name": vm.name,
            "location": vm.location,
            "resource_group": vm_resource_group,
            "tags": tags,
            "public_ips": public_ips
        })

    # fetch storage accounts
    # Include type (storage account), name, location, resource group, encryption status, and secure transfer requirement
    # Note: encryption_enabled and secure_transfer_required are extracted from the storage account properties
    storage_accounts = storage_client.storage_accounts.list()
    for account in storage_accounts:
        storage_account_resource_group = account.id.split('/')[4] # extract resoource group associated with the storage account
        try:
            # retrieve detailed storage account properties
            account_properties = storage_client.storage_accounts.get_properties(storage_account_resource_group, account.name)
        except Exception:
            account_properties = None

        # initialize encryption and secure transfer status for compliance checks
        # These may not always be available, so we handle exceptions
        encryption_enabled = None
        secure_transfer_required = None

        if account_properties:

            # check if encryption for Blob service is enabled
            try:
                encryption_enabled = bool(account_properties.encryption.services.blob.enabled)
            except Exception:
                encryption_enabled = None

            # check if secure transfer is required (HTTPS only)
            try:
                secure_transfer_required = bool(account_properties.enable_https_traffic_only)
            except Exception:
                secure_transfer_required = None

        # append the collected storage account information into the resources list
        resources.append({
            "type": "Storage Account",
            "name": account.name,
            "location": account.location,
            "resource_group": storage_account_resource_group,
            "encryption_enabled": encryption_enabled,
            "secure_transfer_required": secure_transfer_required
        })

    # fetch Network Security Groups
    # include type (NSG), name, location, resource group, and inbound rules
    # Note: inbound rules are extracted from the security_rules property of the NSG
    network_security_groups = network_client.network_security_groups.list_all()
    for nsg in network_security_groups:
        network_security_group_resource_group = nsg.id.split('/')[4] # extract resource group associated with the NSG


        # try to get detailed NSG properties to ensure all security rules are included
        # use the detailed security rules if available, otherwise use the basic security rules
        # This is to ensure we have the most accurate and complete set of rules
        try:
            network_security_group_detail = network_client.network_security_groups.get(network_security_group_resource_group, nsg.name)
            rules_source = network_security_group_detail.security_rules or []
        except Exception:
            rules_source = nsg.security_rules or []

        # extract inbound rules from the NSG
        # extract relevant properties from each security rule
        # Note: getattr is used to safely access properties that may not exist (which default to None)
        # Note: This ensures that if a property is missing, it won't raise an AttributeError
        inbound_rules = []
        for rule in rules_source:
            inbound_rules.append({
                "name": getattr(rule, "name", None),
                "access": getattr(rule, "access", None),
                "direction": getattr(rule, "direction", None),
                "protocol": getattr(rule, "protocol", None),
                "source_address_prefix": getattr(rule, "source_address_prefix", None),
                "destination_port_range": getattr(rule, "destination_port_range", None)
            })

        # append the collected NSG information into the resources list
        resources.append({
            "type": "Network Security Group",
            "name": nsg.name,
            "location": nsg.location,
            "resource_group": network_security_group_resource_group,
            "inbound_rules": inbound_rules
        })

    # fetch VM network interfaces to get IP configurations details
    # include type (NIC), name, location, resource group, IP configurations (public and private IP), and public IP presence
    network_interfaces = network_client.network_interfaces.list_all()
    for nic in network_interfaces:
        ip_configs = []
        has_public_ip = False # flag to check if NIC has a public IP assigned
        for ip_config in nic.ip_configurations:

            # initialize dictionary to hold IP information for each IP configuration
            # Note: private_ip_address is always available, public_ip_address may not be set
            ip_data = {
                "private_ip": getattr(ip_config, "private_ip_address", None) # get private IP address
            }

            # check if public IP address is assigned
            if getattr(ip_config, "public_ip_address", None):
                has_public_ip = True
                public_ip_id = ip_config.public_ip_address.id # get public IP resource ID
                public_ip_name = public_ip_id.split('/')[-1] # extract public IP resource name from resource ID
                public_ip_resource_group = public_ip_id.split('/')[4] # extract resource group of the public IP

                # try to fetch the actual public IP address from the public IP resource
                # If the public IP resource is not found, we store the resource ID instead
                try:
                    public_ip = network_client.public_ip_addresses.get(public_ip_resource_group, public_ip_name)
                    ip_data["public_ip"] = public_ip.ip_address
                except Exception:
                    ip_data["public_ip_id"] = public_ip_id

            # append this IP configuration data to the list of IP configs for the NIC
            # this allows us to capture all IP configurations associated with the NIC       
            ip_configs.append(ip_data)

        # append the collected NIC information into the resources list including IP configurations and public IP flag
        resources.append({
            "type": "Network Interface",
            "name": nic.name,
            "location": nic.location,
            "resource_group": nic.id.split('/')[4],
            "ip_configurations": ip_configs,
            "has_public_ip": has_public_ip
        })

    # return the complete list of Azure resources with detailed configurations
    return resources

# execute the fetch_azure_resources function and save them to a JSON file
if __name__ == "__main__":
    resources = fetch_azure_resources()
    with open("azure_resources.json", "w") as file:
        json.dump(resources, file, indent=4)
    print("Resource data saved to azure_resources.json")

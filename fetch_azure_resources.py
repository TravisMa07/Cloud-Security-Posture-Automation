# pip install azure-identity azure-mgmt-resource azure-mgmt-compute azure-mgmt-storage azure-mgmt-network azure-mgmt-authorization
import json
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient



# Initialize Azure credentials and subscription ID
credential = DefaultAzureCredential()
subscription_id = "7ceee2ac-3bca-4342-8d4e-725195bd5865"

# Initalize Azure management clients
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

    # fetch virtual machines
    virtual_machines = compute_client.virtual_machines.list_all()
    for vm in virtual_machines:
        resources.append({
            "type": "Virtual Machine",
            "name": vm.name,
            "location": vm.location,
            "resource_group": vm.id.split('/')[4]
        })

    # fetch storage accounts
    storage_accounts = storage_client.storage_accounts.list()
    for account in storage_accounts:
        resources.append({
            "type": "Storage Account",
            "name": account.name,
            "location": account.location,
            "resource_group": account.id.split('/')[4]
        })

    # fetch Network Security Groups
    network_sgs = network_client.network_security_groups.list_all()
    for nsg in network_sgs:
        resources.append({
            "type": "Network Security Group",
            "name": nsg.name,
            "location": nsg.location,
            "resource_group": nsg.id.split('/')[4]
        })
    
    # fetch VM network interfaces
    network_interfaces = network_client.network_interfaces.list_all()
    for nic in network_interfaces:
        resources.append({
            "type": "network interface",
            "name": nic.name,
            "location": nic.location,
            "resource_group": nic.id.split('/')[4],
            "ip_configurations": [ip_config.private_ip_address for ip_config in nic.ip_configurations]
        })

    return resources



if __name__ == "__main__":
    resources = fetch_azure_resources()
    with open("azure_resources.json", "w") as file:
        json.dump(resources, file, indent=4)
    print("Resource data saved to azure_resources.json")

        


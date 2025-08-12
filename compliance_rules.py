# Compliance Rules
# This module defines compliance rules for various operations in Azure including:
# Storage Accounts: Checks encryption and secure transfer configurations
# Virtual Machines: Checks tags, public IPs presence, and whether NSGs block inbound traffic for RDP/SSH
# Network Security Groups (NSGs): Find overly permissive inbound rules on critical ports
# ^^^ Compliance rules are defined here and can be extended as needed ^^^

import json

def open_json_file(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

# compliance checks for storage accounts
# checks if encryption and secure transfer are enabled
def check_storage_account_compliance(storage_account):
    
    return {
        "encryption_enabled": storage_account.get("encryption_enabled") is True,
        "secure_transfer_required": storage_account.get("secure_transfer_required") is True
    }

# compliance checks for virtual machines
def check_virtual_machine_compliance(vm, nsgs):
    tags = vm.get("tags", {})
    public_ips = len(vm.get("public_ips", [])) > 0

    # check if any NSG are atttached to the VM's resource group
    # list comprehension to filter all NSGs to get those attached to the VM's resource group
    vm_rg = vm.get("resource_group")
    nsgs_attached = [nsg for nsg in nsgs if nsg.get("resource_group") == vm_rg]


    # Checks if a specific port is blocked (denied) in the given Network Security Group (NSG).
    # Return true if the port is blocked, otherwise false.
    def is_port_blocked(nsg, port):
        for rule in nsg.get("inbound_rules", []):
            if (rule.get("destination_port_range") == port and
                rule.get("access") == "Deny" and
                rule.get("direction") == "Inbound"): 
                return True
        return False
    
    # Check if RDP (port 3389) and SSH (port 22) are blocked in any of the NSGs attached to the VM's resource group
    # For each NSG attached, it call is_port_blocked to check if the port is blocked and returns True if any NSG blocks the port otherwise False
    block_rdp = any(is_port_blocked(nsg, "3389") for nsg in nsgs_attached)
    block_ssh = any(is_port_blocked(nsg, "22") for nsg in nsgs_attached)

    # return environment tags, owner tag, public IP presence, and RDP/SSH block status
    return {
        "environment_tags": "environment" in tags,
        "owner_tag": "owner" in tags,
        "has_public_ips": public_ips,
        "block_rdp": block_rdp,
        "block_ssh": block_ssh,
        
    }

# compliance checks for network security groups
# checks for overly permissive inbound rules on critical ports (22, 3389, 80, 443) which include:
# - source_address_prefix is "*"
# - access is "Allow"
# - direction is "Inbound"
# returns count of permissive rules and details of each rule
def check_network_security_group_compliance(nsg):
    
    permissive_rules = []
    check_ports = ["22", "3389", "80", "443"]

    for rule in nsg.get("inbound_rules", []):
        if (rule.get("source_address_prefix") == "*" 
            and rule.get("access") == "Allow" 
            and rule.get("direction") == "Inbound" 
            and rule.get("destination_port_range") in check_ports):

            # append relevant details of rules that been found to be overly permissive
            # append dictionary with key pair values for name, source_address, and destination_port to permissive_rules list
            permissive_rules.append({"name": rule.get("name"), 
                                    "source_address": rule.get("source_address_prefix"), 
                                    "destination_port": rule.get("destination_port_range")})
            
    return {
        "permissive_rules_count": len(permissive_rules),
        "permissive rules details": permissive_rules
    }
    


# Evaluate compliance for all resources
# take dictionary of Azure resources (from JSON file) and evaluate compliance for each resource type
# returns name and compliance status for each resource type
# iterate through all resources type and check compliance using the defined functions above
def evaluate_compliance(resources):
    compliance_report = { "storage_accounts": [], "virtual_machines": [], "network_security_groups": []}

    # filter each resource type using list comprehensions
    # the input 'resources' is a flat list of dictionaries, where each dictionary represents a resource and includes a 'type' key
    # Since the data is a mixed flat list (not grouped/nested by resource type), we cannot access resources by type directly.
    # so directly accessing keys like 'resource.get("type")' won't work on a list, therefore we filter the list to separate resources by their 'type'
    storage_accounts = [r for r in resources if r.get("type") == "Storage Account"]
    virtual_machines = [r for r in resources if r.get("type") == "Virtual Machine"]
    network_security_groups = [r for r in resources if r.get("type") == "Network Security Group"]
    

    for storage_account in storage_accounts:
        compliance_report["storage_accounts"].append({
            "name": storage_account.get("name"),
            "compliance": check_storage_account_compliance(storage_account)
        })
    for virtual_machine in virtual_machines:
        nsgs = network_security_groups
        compliance_report["virtual_machines"].append({
            "name": virtual_machine.get("name"),
            "compliance": check_virtual_machine_compliance(virtual_machine, nsgs)
        })
    for nsg in network_security_groups:
        compliance_report["network_security_groups"].append({
            "name": nsg.get("name"),
            "compliance": check_network_security_group_compliance(nsg)
        })

    return compliance_report




if __name__ == "__main__":
    resources = open_json_file('azure_resources.json')
    compliance_report = evaluate_compliance(resources)
    with open('compliance_report.json', 'w') as report_file:
        json.dump(compliance_report, report_file, indent=4)
 



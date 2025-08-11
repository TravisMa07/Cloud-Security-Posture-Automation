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
def check_virtual_machine_compliance(vm, nsg):
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

# LATER IMPLEMENTATION: compliance checks for Network Security Groups
# LATER IMPLEMENTATION: evaluate compliance for all resources
# LATER IMPLEMENTATION: Main function
'''
def check_network_security_group_compliance(nsg):

def evaluate_compliance(resources):


if __name__ == "__main__":
    resources = open_json_file('azure_resources.json')
    compliance_report = evaluate_compliance(resources)
    print(json.dumps(compliance_report, indent=4))
        
'''

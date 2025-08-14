import os
import subprocess

terraform_directory = "../terraform/root"
log_directory = "../terraform/runs"
os.makedirs(log_directory, exist_ok=True)
log_file_path = os.path.join(log_directory, "terraform_remediation.log")


tfvars = {
    "resource_group_name": "CSPA-Project-RG",
    "vm_name": "CSPA-VM1",
    "nsg_name": "CSPA-VM1NSG",
    "allowed_cidrs": '["100.34.227.34/32"]',
    "environment_tag": "production",
    "owner_tag": "Travis Ma"
}

def terraform_command(command, cwd=terraform_directory):
    pass


def main():
    pass
    terraform_command("terraform", "init")
    terraform_command("terraform", "plan")
    terraform_command("terraform", "apply")


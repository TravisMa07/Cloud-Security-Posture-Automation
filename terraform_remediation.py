import subprocess

# This script is used to run Terraform commands from Python and pass variables to the configuration.
# It initializes the Terraform directory, plans the infrastructure changes, and applies them through the script instead of manually running Terraform commands.

# Path to the Terraform directory where commands will be executed
terraform_directory = "../terraform/root"

# Terraform variables to be passed to the configuration
# tfvars dictionary contains the variables and their values which prevent manual input during Terraform execution
tfvars = {
    "resource_group_name": "CSPA-Project-RG",
    "vm_name": "CSPA-VM1",
    "nsg_name": "CSPA-VM1NSG",
    "allowed_cidrs": '["100.34.227.34/32"]',
    "environment_tag": "production",
    "owner_tag": "Travis Ma"
}

# Convert a tfvars dictionary of Terraform variables and value into a list of CLI arguments
#           Terraform CLI expects variable in the format: -var="key=value"
# The function takes a dictionary and returns a list of string in where each string is a CLI argument (-var="key=value") for Terraform commands
def tfvars_to_vars(tfvars):
    cli_args = []
    for key, value in tfvars.items():\
    #   value
        pass


tfvars_terraform_cli_args = tfvars_to_vars(tfvars)


subprocess.run(["terraform", "init"], cwd=terraform_directory)
subprocess.run(["terraform", "plan"] #value)
subprocess.run(["terraform", "apply"] #value)
               
print("Terraform commands executed successfully.")
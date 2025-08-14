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

    # Iterate through the tfvars dictionary (both keys and values) and format them for Terraform CLI
    for key, value in tfvars.items():

        # insert dictionary's key and value into the Terraform CLI -var format
                # EXAMPLE: if key="vm_name" and value="CSPA-VM1", it will produce -var=vm_name="CSPA-VM1"
        cli_args.append(f'-var={key}="{value}"')

    return cli_args


tfvars_terraform_cli_args = tfvars_to_vars(tfvars)


# Initialize the Terraform directory, plan the changes, and apply them using subprocess to call Terraform commands
subprocess.run(["terraform", "init"], cwd=terraform_directory)

# "+ tfvars_terraform_cli_args" inject your Python tfvars values into the Terraform "plan" command
    # Example: output will be: terraform plan -var=vm_name="CSPA-VM1" -var=resource_group_name="CSPA-Project-RG" ...
subprocess.run(["terraform", "plan"] + tfvars_terraform_cli_args, cwd=terraform_directory)

# "-auto-approve" flag is used to skip the interactive approval/confirmation prompt when applying changes
subprocess.run(["terraform", "apply", "-auto-approve"] + tfvars_terraform_cli_args, cwd=terraform_directory)
               
print("Terraform commands executed successfully.")
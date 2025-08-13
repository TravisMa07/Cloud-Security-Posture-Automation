# Cloud-Security-Posture-Automation

Cloud Security Posture Automation (CSPA) is a Python-based and Terraform-powered framework designed to automatically assess, remediate, and monitor cloud environment configurations for security best practices. This project focuses on identifying misconfigurations, enforcing compliance with CIS Benchmarks & NIST CSF, and streamlining security governance across Azure.

## Features
- **Automated Security Audits:** Scans cloud resources for misconfigurations (e.g., storage account encryption and secure transfer settings, VM public exposure, overly permissive network security group rules)
- **Compliance Enforcement:** Validates configurations against CIS Benchmarks and NIST CSF (Cybersecurity Framework).
- **Automated Remediation:** Uses Terraform scripts and cloud-native CLI tools to remediate security findings.
- **Continuous Monitoring:** Scheduled scans to detect new risks in real time.
- **Reporting:** Generates JSON reports from compliance evaluation scripts.

## Technology Stack
- **Cloud Providers:** Azure
- **Languages:** Python, Terraform, Powershell, Azure CLI
- **Security Tools:** Azure CLI, Azure Web Interface
- **Compliance Frameworks:** CIS Benchmarks, NIST CSF

## Architecture
1. **Azure Config** collects and evaluates resource configurations.
2. **Python Script** pulls compliance data via Azure SDK libraries(e.g.,`azure-mgmt`).
3. **Rule Engine** evaluates the collected data against best practices and compliance frameworks.
4. **Reporting Module** generates detailed security posture reports.


# Detailed Workflow
**1. Authenticate to Azure:**
Use Azure CLI (``az login``) or a service principal to securely authenticate and grant your scripts permissions to access Azure resources.

**2. Scan Cloud Resources:**
Query Azure resources (e.g., Storage Accounts, Network Security Groups, Virtual Machines) using Azure SDK scripts to collect their current configuration details.

**3. Evaluate Compliance:**
Evaluate the collected configurations against CIS Benchmarks and NIST Cybersecurity Framework controls using Python functions

**4. Generate Reports:**
Produce detailed JSON reports for automated processing and human-readable HTML reports for security teams, highlighting misconfigurations, risk severity, and remediation advice.

**5. Automate Remediation:**
For critical findings like public blob containers or overly permissive network security group rules, leverage Terraform modules or Azure CLI commands to automatically remediate issues and improve security posture.

**6. Continuous Monitoring:**
Schedule periodic scans via Azure Automation Runbooks to detect and remediate new risks in real-time, maintaining an up-to-date security posture.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following installed and configured:

- **Azure Account:**  
  Create a free Azure account at [https://azure.microsoft.com/free/](https://azure.microsoft.com/free/) to access cloud resources.  

- **Python 3.8+ and Virtual Environment:**  
  Install Python 3.8 or later from [python.org](https://www.python.org/downloads/).  
  It is recommended to use a virtual environment to manage dependencies.

- **Azure CLI:**  
  Install the Azure Command-Line Interface (CLI) from [https://learn.microsoft.com/en-us/cli/azure/install-azure-cli](https://learn.microsoft.com/en-us/cli/azure/install-azure-cli) and configure it by running:  
  ```bash
  az login
  ```
  This authenticates your session with Azure
  
- **Terraform:**
  Download and install Terraform from ``https://learn.hashicorp.com/tutorials/terraform/install-cli``.
  Terraform is used to automate remediation by applying configuration changes to your Azure environment.

- **Open Policy Agent (OPA):**
  Install the OPA CLI from ``https://www.openpolicyagent.org/docs/latest/#running-opa``.
  OPA is used to implement policy-as-code for compliance validation of your cloud resources.

# Optional: Open Policy Agent (OPA) Integration
### What is OPA?
Open Policy Agent (OPA) is a lightweight, general-purpose policy engine that enables a unified platform for policy enforcement across cloud-native stack. It allows you to define compliance rules as code using a declarative language called Rego.

## Why OPA is not used in this project
While OPA provides a powerful and flexible way to enforce policies across cloud environments, for the scope of this project and to maintain simplicity and clarity, compliance rules are implemented directly in Python. This approach allows for easier customization, debugging, and integration within the Python-based tooling already in use

The walkthrough and examples focus on using Python scripts leveraging the Azure SDK to collect resource data and evaluate compliance based on CIS benchmarks and NIST CSF control. Future expansion may consider adding OPA policies for enhanced policy-as-code capabilities.

That said, the project walkthrough does include instructions on how to install OPA, complete with screenshots, to familiarize user with the tool. Additionally, the prerequistites section above briefly shows how to install OPA for those interested in exploring policy-as-code outside the current project scope.

# Cloud Security Posture Automation Walkthrough

## Step 1: Setup Development Environment and Azure Access
- Install Python, create virtual env
  
  ![csap1.1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap1.1.png)
- Install Azure CLI and authenticate

  ![csap1.2 1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%201.2%201.png)
  
  - In order to ``az login``, a Azure Account is needed. Create a free Azure Account at ``https://azure.microsoft.com/en-us/pricing/purchase-options/azure-account?icid=azurefreeaccount`` Require Credit Card Information
  
  ![csap 1.2 2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%201.2%202.png)
  
- Install Terraform
  - Install terraform at ``https://developer.hashicorp.com/terraform/install``. Install version for your machine and extract the .zip in its own dedicated folder on your drive.
    
  ![csap 1.3.1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%201.3%201.png)
  - Under User Variables, click on Path then edit. Add new to your dedicated folder for terraform (``C:\terraform``)
    
  ![csap 1.3.2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%201.3%202.png)
- Install Open Policy Agent (OPA)
  - Install OPA at ``https://www.openpolicyagent.org/docs?current-os=windows#1-download-opa``. Install version for your machine and move the .exe file into its own dedicate folder on your drive.
    
  ![csap 1.4.1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%201.4%201.png)
    - Under User Variables, click on path then edit. Add new to your dedicated folder for OPA (``C:\Tools\OPA``)
      
  ![csap 1.4.2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%201.4%202.png)

## Step 2: Azure Resource Inventory and Data Collection
- Create necessary Resources for Project Demostration
  - Creating necessary resources includes: Resource Group, Storage Account, Virtual Machine, Network Security Group (NSG), Associate NSG with VM's Network Interfaces Card (NIC)
    - Can either be done through Azure Web Interface and/or Azure CLI (demo will be through Azure CLI)
  - Resource Group Creation: name it anything
    
    ![csap 2.1 setup 1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%202.1%20setup%201.png)
    
  - Storage Account Creation: name it anything, select Resource Group just created, Stock-Keeping Unit (SKU) select Standard-LRS (Locally Redundant Storage, Support Account Kinds: Storage, BlobStorage, StorageV2)
    
    ![csap 2.1 setup 2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%202.1%20setup%202.png)
    
  - Virtual Machine Creation: Choose any supported Ubuntu image (e.g., Ubuntu2204). If you encounter errors during VM creation, try selecting a different VM --size .
 
    ![csap 2.1 setup 3](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%202.1%20setup%203.png)
  - Network Security Group (NSG) Creation
    ![csap 2.1 setup 4](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%202.1%20setup%204.png)
    
  - Assign NSG to VM's Network Interface
    ![csap 2.1 setup 5](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%202.1%20setup%205.png)
    
  - Create Role Assignment (IAM) -- Assign the "Reader" role to yourself
    ![csap 2.1 setup 6](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%202.1%20setup%206.png)

- Use the Python SDK script (`fetch_azure_resources.py`) to collect detailed Azure resource configurations.
- The script extracts critical security details needed for compliance checks:
  - Storage Accounts: Checked to ensure encryption at rest and secure transfer are enabled, critical for protecting stored data.
  - Virtual Machines: Validated for the presence of essential tags (`environment`, `owner`) to aid resource management and accountability, and to ensure they do not have public IPs or unblocked RDP/SSH ports without proper network security group (NSG) restrictions.
  - Network Security Groups: detect overly permissive inbound rules that allow open access (source `0.0.0.0/0`) on sensitive ports such as SSH (22), RDP (3389), HTTP (80), and HTTPS (443).
- Output is saved in `azure_resources.json` for subsequent compliance evaluation.
- see the `fetch_azure_resources.py` script and the generated `azure_resources.json` file in the repoistory for implementation details
  - The resource gathering script can be expanded to collect additional data if you plan to implement more compliance rules.

## Step 3: Compliance Rule Implementation
- Python functions evaluate compliance of the collected resources against CIS Benchmarks and NIST CSF controls.
- Key rules include:
  - Storage Accounts: Verify encryption and secure transfer are enabled
  - Virtual Machines: Confirm required tags (`environment`, `owner`) and no public exposure via IPs or unblocked RDP/SSH ports
  - Network Security Groups: Detect overly permissive inbound rules open to `0.0.0.0/0` on critical ports (22, 3389, 80, 443)
- The compliance evaluation includes cross-referencing NSG rules with VM resource groups to confirm proper port blocking, helping identify misconfigurations that expose resources to potential threats.
- You can run and test the compliance logic using the `compliance_rules.py` in the repository against the collected data from `azure_resources.json` file. An example output report from the test can be found in the `compliance_report.json` highlighting non-compliant configurations, which will be use in the Automated Remediation Section.


## Step 4: Automated Remediation and Infrastructure as Code
- Automate the correction of detected compliance violations in `compliance_report.json` using Infrasturcture as Code (IaC) practices, specifically Terraform
   - Terraform Files are wrriten in HashiCorp Configuration Language (HCL)
- Develop Terraform modules that address misconfiguration found during compliance checks
- Integrate the Terraform modules with Python scripts to dynamically trigger remediations based on the compliance report outputs
- Verify that compliance issues are automatically resolved and that the infrastructure posture aligns with compliance rules following CIS Benchmarks and NIST CSF

- 4.1: Understanding compliance violations found in JSON and define remediation targets
  - ``environment_tags`` = ``false``, but need to be ``true``
  - ``owner_tag`` = ``false``, but need to be ``true``
  - ``block_rdp`` = ``false``, but need to be ``true`` for only **your current public IP**
  - ``block_ssh`` = ``false``, but need to be ``true`` for only **your current public IP**
  - CSPA-VM1NSG has one Permissive Rule: ``default-allow-ssh``
    - **Remediation:** Update source_address to **your current public IP**
![csap 4.1 1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/CSAP%204.1%201.png)   

- 4.2: Write Terraform Modules to fix each misconfiguration
  - a Terraform module to restrict SSH and RDP to your public IP
  - a Terraform module to add VM tags (environment and owner) by using Azure CLI via Terraform's ``null_resource``
  - a run folder to call the terraform modules with ``terraform init/plan/apply``

- 4.2.1: Create Terraform folder layout
  - head over to your Github Repo Root Directory
    - Create the following Folders
      - Can be done through Github Web Page or CLI (demo will be in CLI)

![csap 4.2.1 1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.1%201.png)

![csap 4.2.1 2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.1%202.png)
        
- 4.2.2 Terraform Module: Restrict SSH/RDP to your public IP (NSG)
  - Create Terraform file via path ``terraform\module\nsg_fix\variables.tf``, ``terraform\module\nsg_fix\main.tf``, ``terraform\module\nsg_fix\outputs.tf``
    - Use ``new-item`` to create terraform files
    - Use ``nano`` to write into files (must install nano via ``winget install GNU.nano``)

- ``variables.tf`` Contents:
  - The ``variables.tf`` file defines input variables/parameters that make the module reusable and customizeable across different environment
    - Store configuration values (``RG name``, ``NSG name``, ``allowed CIDRs/IPs``, and ``rule priorities``)
      - (Note: for rule priorities, lower the number = higher precedence. Range from: ``100-4096``)
  - Instead of having specific values inside the Terraform configuration, declaring variables here and assign their values in ``main.tf`` allow for easy changes
    
![csap 4.2.2 1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.2%201.png)
    
  - ``main.tf`` Contents:
    - The ``main.tf`` file is the main logic that tells Terraform what infrastructure changes to make
      - ``main.tf`` logic:
        - Connect to your Azure NSG
        - Create or update rules to allow SSH (22) and RDP (3389) only from your public IP
        - Block access from everywhere else by default
    - Syntax Explanation:
      - ``provider``
        - In terraform HCL, provider = the cloud platform (Azure, AWS, GCP, etc)
      - ``resource``
        - In terraform HCL, resource = a block of actual piece of infrastructure to create or manage
    - Documentation:
      - https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/network_security_rule
        
![csap 4.2.2 2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.2%202.png)

  - ``outputs.tf`` Contents:
    - The ``outputs.tf`` file defines the output values that Terraform will show after applying the configuration from ``main.tf``
    - Output important information about resources that been created or modified (rule name, etc)
    - Syntax Explanation:
      - ``output``
        - In terraform HCL, output = name that can be reference after applying
      - ``value``
        - In terraform HCL, value = what's actually outputted. The ``.name`` attribute is use to reference the name attribute in the main.tf (NSG rules)
          
![csap 4.2.2 3](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.2%203.png)
  
- 4.2.3 Terraform Module: Tag the Virtual Machine (Environmental and Owner)
  - Create Terraform file via path ``terraform\module\vm_tagging\variables.tf``, ``terraform\module\vm_tagging\main.tf``, ``terraform\module\vm_tagging\outputs.tf``
    - Use ``new-item`` to create terraform files
    - Use ``nano`` to write into files (must install nano via ``winget install GNU.nano``)

- ``variables.tf`` Contents:
  -  The ``variables.tf`` file defines input variables/parameters that make the module reusable and customizeable across different environment
      - Store configuration values (``Resource Group Name``, ``Virtual Machine Name``, ``Environment Tag``, and ``Owner Tag``)
  - ``environment_tag`` = value such as "development", "production", "testing", etc
  - ``owner_tag``       = value such as "your name", "team name", etc
  - Instead of having specific values inside the Terraform configuration, declaring variables here and assign their values in ``main.tf`` allow for easy changes

![csap 4.2.3 1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.3%201.png)

- ``main.tf`` Contents:
  - The ``main.tf`` file is the main logic that tells Terraform what infrastructure changes to make
  - ``main.tf`` logic:
    - Connect to your existing Azure Virtual Machine (VM) using resource group and VM name variables
    - Create or update tags on the VM to set ``environment`` and ``owner`` tags with values provided
    - Ensure the VM complies with tagging requirements defined in the compliance rules
      - can't be = ``false``, neeed to be = ``true``
  - Syntax Explanation
    - ``provider``
      - In terraform HCL, provider = the cloud platform (Azure, AWS, GCP, etc)
    - ``resource``
      - In terraform HCL, resource = a block of actual piece of infrastructure to create or manage
    - ``tags = {...}``
      - In terraform HCL, tag = sets or updates tags for the VM resource
  - Documentation:
    - https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/virtual_machine

![csap 4.2.3 2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.3%202.png)

- ``outputs.tf`` Contents:
  - The ``outputs.tf`` file defines the output values that Terraform will show after applying the configuration from ``main.tf``
  - Output important information about resources that been created or modified (tags applied, VM name, VM resource group)
  - Syntax Explanation:
      - ``output``
        - In terraform HCL, output = name that can be reference after applying
      - ``value``
        - In terraform HCL, value = what's actually outputted. The ``.name``, ``.resource_group_name``, ``.tags`` attribute is use to reference the attributes in the main.tf (Virtual Machine Resource)
        
![csap 4.2.3 3](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.3%203.png)

- 4.2.4 Terraform Root Module: Ties both ``NSG restriction module`` and ``VM tagging module``
  - Create ``root directory`` under ``.../terraform`` and create files: ``variables.tf``, ``main.tf``, ``outputs.tf``
  - Root directory files combines values from both modules into a single file (Ex: combing ``variables.tf`` from both module into one ``variables.tf``)
    - The root directory act as the top-level Terraform configuration that:
      - Calls each individual module with the right inputs (variables)
      - Combines all the pieces together to build the full infrastructure configuration for deployment
    - Why combine both modules into root directory?
      - Modularity and Reusability
        - Each module handle different task/logic (one to restrict NSG rules, other to manage VM tags). By breaking down the infrastructure into smaller modules:
          -  it allow the ability to reuse the same module across different environments without rewriting code.
          -  It allow the ability to maintain and update module independently (Ex: if you change the logic in the tagging module. It won't effect other environment beside the one you are working in), so changes in one module won't unintentionally affect others.
      - Simplified Deployment:
        - When runnig ``terraform apply`` at the root level, Terraform grasp the complete task for the infrastructure, including all the modules and their relationship. This prevent partial or out-of-sync deployments.
  - Why Root Directory Summary:
    - The root module provides a single source of an up-to-date orchestration layer that connects all your modular pieces into one cohesive and manageable infrastructure codebase, ensuring that your deployments are consistent, maintainable, and scalable.

- ``root directory`` and ``variables.tf``, ``main.tf``, ``outputs.tf`` creation:

![csap 4.2.4 1](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.4%201.png)

- ``variables.tf`` content:

![csap 4.2.4 2](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.4%202.png)

- ``main.tf`` content:

![csap 4.2.4 3](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.4%203.png)

- ``outputs.tf`` content:

![csap 4.2.4 4](https://raw.githubusercontent.com/TravisMa07/Cloud-Security-Posture-Automation/refs/heads/main/csap%204.2.4%204.png)


  
4.3: Create Python logic to dynamically trigger terraform remediation
4.4: test end-to-end remediation


## Step 5: Continuous Monitoring, Scheduling and Alerting
- Set up cron jobs or Task Scheduler for periodic scans
- Automate report generation and remediation triggers
- Add alerting or notification (email/Slack) if desired
  

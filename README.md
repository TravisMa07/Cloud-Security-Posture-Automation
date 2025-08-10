# Cloud-Security-Posture-Automation

Cloud Security Posture Automation (CSPA) is a Python-based and Terraform-powered framework designed to automatically assess, remediate, and monitor cloud environment configurations for security best practices. This project focuses on identifying misconfigurations, enforcing compliance with CIS Benchmarks, and streamlining security governance across Azure.

## Features
- **Automated Security Audits:** Scans cloud resources for misconfigurations (e.g., open blob storage container, overly permissive IAM roles, insecure network settings).
- **Compliance Enforcement:** Validates configurations against CIS Benchmarks and other compliance standards.
- **Automated Remediation:** Uses Terraform scripts and cloud-native CLI tools to remediate security findings.
- **Continuous Monitoring:** Scheduled scans to detect new risks in real time.
- **Reporting:** Generates JSON and HTML reports for security teams.

## Technology Stack
- **Cloud Providers:** Azure (mock/test mode available for development)
- **Languages:** Python, Terraform, Bash
- **Security Tools:** Azure CLI, Open Policy Agent (OPA)
- **Compliance Frameworks:** CIS Benchmarks, NIST CSF

## Architecture
1. **Azure Config** collects and evaluates resource configurations.
2. **Python Script** pulls compliance data via Azure SDK libraries(e.g.,`azure-mgmt`).
3. **Rule Engine** checks results against best practices and compliance mappings.
4. **Reporting Module** outputs a detailed posture report.


# Detailed Workflow
**1. Authenticate to Azure:**
Use the Azure CLI (az login) or a service principal to securely connect your scripts with Azure and gain read/write permissions to cloud resources.

**2. Scan Cloud Resources:**
Query Azure resources (e.g., Storage Accounts, Network Security Groups, IAM roles) through the Azure SDK or CLI to gather their current configuration details.

**3. Evaluate Compliance:**
Check the retrieved configurations against CIS Benchmarks and NIST Cybersecurity Framework controls. Compliance rules are implemented as Python functions and Open Policy Agent (OPA) policies, which classify configurations as compliant or non-compliant.

**4. Generate Reports:**
Produce detailed JSON reports for machine processing and human-readable HTML reports for security teams. These reports highlight misconfigurations, risk severity, and remediation suggestions.

**5. Automate Remediation:**
For high-risk findings (e.g., public blob containers, overly permissive IAM roles), execute Terraform modules or Azure CLI commands to automatically correct misconfigurations, improving security posture without manual intervention.

**6. Continuous Monitoring:**
Schedule periodic scans via cron jobs, Windows Task Scheduler, or Azure Automation Runbooks to detect and remediate new risks in real-time, maintaining an up-to-date security posture.

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


# Cloud Security Posture Automation Walkthrough

## Step 1: Setup Development Environment & Azure Access
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

## Step 2: Azure Resource Inventory & Data Collection
- Create necessary Resources for Project Demostration
  - Creating necessary resources includes: Resource Group, Storage Account, Virtual Machine, Network Security Group (NSG), Associate NSG with VM's Network Interfaces
    - Can either be done through Azure Web Interface or Azure CLI (demo will be through Azure CLI)
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
  
- Use Azure SDK/CLI to list resources
- Pull configuration details for key resource types (storage, VMs, network, IAM)
- Store data locally (JSON, database, etc.)

## Step 3: Compliance Rule Development
- Implement CIS benchmark and NIST CSF rules in Python
- Write OPA policies for some rules (optional/parallel)
- Test rule evaluation logic

## Step 4: Reporting Module
- Design JSON report structure
- Implement report generation (JSON + HTML)
- Test report clarity and completeness

## Step 5: Automated Remediation
- Write Terraform modules for fixing common misconfigs
- Integrate remediation trigger in Python
- Test remediation end-to-end on test environment

## Step 6: Continuous Monitoring & Scheduling
- Set up cron jobs or Task Scheduler for periodic scans
- Automate report generation and remediation triggers
- Add alerting or notification (email/Slack) if desired
  
## Step 7: Documentation & Final Touches
- Write detailed guides and update README
- Add screenshots and usage examples
- Clean up code and add tests if possible

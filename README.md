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
2. **Python Script** pulls compliance data via `boto3`.
3. **Rule Engine** checks results against best practices and compliance mappings.
4. **Reporting Module** outputs a detailed posture report.

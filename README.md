# Cloud-Security-Posture-Automation

Automated cloud security posture management (CSPM) tool that scans AWS environments for misconfigurations, compliance violations, and security risks using the free tier of AWS Config and Python-based automation.

## Features
- **Automated Posture Scans** – Programmatically assess AWS resources against security best practices.
- **Compliance Mapping** – Map findings to frameworks like CIS Benchmarks and NIST 800-53.
- **Free-Tier Friendly** – Uses AWS Config’s free tier to avoid unnecessary costs.
- **Custom Rule Integration** – Add custom security rules beyond AWS managed ones.
- **Automated Reports** – Generate JSON and HTML summaries of misconfigurations.
- **Cloud SDK Support** – Built with `boto3` for AWS automation.

## Architecture
1. **AWS Config** collects and evaluates resource configurations.
2. **Python Script** pulls compliance data via `boto3`.
3. **Rule Engine** checks results against best practices and compliance mappings.
4. **Reporting Module** outputs a detailed posture report.

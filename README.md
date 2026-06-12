# ⚡ CloudOps Controller Dashboard

A responsive, full-stack cloud infrastructure automation platform built to provision, monitor, and audit AWS cloud architecture asynchronously. This system bridges the gap between software development and cloud operations, implementing secure AWS SDK integrations, backend API routing, interactive frontend interfaces, and local database state management.

---

## 🔍 Project Capabilities (What It Does)

This platform provides a centralized, local operational panel to manage core AWS resources programmatically without needing to interact with the heavy AWS Management Console:

* **🖥️ Compute Engine Management**: Spin up fresh EC2 virtual machine instances dynamically using specified AMI signatures, stop running instances instantly, or query active instance statuses.
* **🪣 Dynamic S3 Storage**: Deploy globally unique Amazon S3 bucket environments that automatically adapt to your configured AWS regional constraints to bypass location-constraint restrictions.
* **👤 Access Control (IAM)**: Programmatically provision new functional IAM development users with targeted resource administrative scopes.
* **📋 Local Operational Logging**: Tracks an immutable historical record of every creation, deletion, or cloud system failure using an embedded SQLite transaction database.
* **📊 CloudWatch Metrics & Costs**: Hooks into AWS monitoring subsystems to parse computational workloads (CPU %) and monthly account billing forecasts.

---

## 📁 Project File Structure

Organize your workspace root directory exactly as shown below to ensure the Flask engine maps routing schemas, module classes, and tracking assets correctly:

```text
Cloud-Automation/
│
├── app.py                      # Main entry point: runs Flask server, handles API endpoints, writes logs
├── requirements.txt            # Lists Python packages for easy environmental distribution
├── .gitignore                  # Explicit file matrix protecting database binaries and access tokens
│
├── aws/                        # Modular AWS logical infrastructure subsystems
│   ├── __init__.py             # Identifies the directory as an executable package folder
│   ├── ec2_manager.py          # Real-time EC2 API integration wrappers
│   ├── s3_manager.py           # Real-time S3 storage interaction hooks & location adapters
│   ├── iam_manager.py          # Programmatic user access lifecycle management
│   └── cloudwatch_manager.py   # CloudWatch resource metrics analysis engine
│
├── templates/                  # Frontend view templates folder
│   └── dashboard.html          # Utility-first interactive UI using Tailwind CSS v4
│
├── database/                   # Embedded structural transactional datastore[cite: 1]
│   └── cloud.db                # SQLite database file (Automatically generated on boot)[cite: 1]
│
├── reports/                    # Folder for saving exported cost or infrastructure audits[cite: 1]
└── backups/                    # Target folder containing local files ready for S3 synchronization[cite: 1]
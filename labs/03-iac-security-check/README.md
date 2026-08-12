# 🛡️ Lab 03: Custom Composite Action for IaC Security Scanning

## 📌 Overview
This lab demonstrates how to create and consume a **Custom Composite Action** in GitHub Actions. The goal is to enforce static code analysis, linting, and misconfiguration detection on Terraform (`.tf`) files prior to deployment.

---

## 📁 Laboratory Structure

```text
.
├── .github/
│   ├── actions/
│   │   └── iac-security-check/
│   │       └── action.yml           # Reusable Composite Action definition
│   └── workflows/
│       └── 03-workflow-composite-action.yml # Test harness workflow
└── labs/
    └── 03-iac-security-check/
        ├── main.tf                  # Sample vulnerable Terraform file
        ├── .tflint.hcl              # TFLint AWS plugin configuration
        └── README.md                # Lab Documentation
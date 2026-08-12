# 🚀 GitHub Actions Enterprise Mastery (GH-200)

This repository serves as a hands-on technical portfolio and study guide for the **GitHub Actions Certification (GH-200)**. It covers production-ready CI/CD patterns, DevSecOps practices, and workflow architectures.

---

## 📚 Table of Contents & Learning Path

| ID | Topic / Core Domain | Technical Concepts | Paths & Artifacts |
| :--- | :--- | :--- | :--- |
| **01** | **Matrix, Services & Artifacts** *(Domain 1 & 4)* | Parallel Matrices, PostgreSQL Service Containers, `$GITHUB_OUTPUT`, Artifact Retention | [Workflow](.github/workflows/01-matrix-services-artifacts.yml) \| [Code](labs/01-matrix-services/src/app.py) |
| **02** | **Zero-Trust AWS Auth via OIDC** *(Domain 2 & 3)* | OpenID Connect, JWT Claims, IAM Trust Policies, Least Privilege, Passwordless CI/CD | [Workflow](.github/workflows/02-workflow-aws-oidc.yml) \| [Labs](labs/02-aws-oidc/) |
| **03** | **Custom Composite Action (IaC Security & Quality)** *(Domain 1 & 4)* | Composite Actions (`action.yml`), TFLint, Trivy SAST, Centralized `env`/`vars`, Artifact Retention | [Workflow](.github/workflows/03-workflow-composite-action.yml) \| [Labs](labs/03-iac-security-check/) |

---

## 01 - Matrix Strategies, Service Containers & Artifacts

### 🎯 Business Challenge
We need to validate a Python application against multiple runtime versions (`3.10` and `3.11`) across operational environments (`staging` and `production`). The execution requires an active PostgreSQL database instance to verify connectivity and must persist execution logs as audit artifacts without polluting the runner host.

---

## 02 - Zero-Trust AWS Authentication via OpenID Connect (OIDC)

### 🎯 Business Challenge
Storing long-lived static cloud credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) in GitHub Secrets introduces critical security risks, including credential leakage, lack of automated rotation, and overly broad privileges. We need to eliminate static credentials entirely by establishing a passwordless, short-lived authentication mechanism between GitHub Actions and AWS IAM using OpenID Connect (OIDC).

### 🛠️ Architecture & Workflow Overview
Instead of exchanging fixed secrets, the GitHub runner requests a short-lived JSON Web Token (JWT) from GitHub's OIDC Provider. AWS Security Token Service (STS) validates the token against a strict IAM Trust Policy and exchanges it for temporary AWS security credentials.

---

## 03 - Custom Composite Action (IaC Security & Quality Scanner)

### 🎯 Business Challenge
As Infrastructure-as-Code (IaC) adoption scales across multiple development teams, manually maintaining linting, formatting, and static application security testing (SAST) in individual workflows creates maintenance bottlenecks, inconsistent security baselines, and drift. We need an enterprise-grade, reusable **Custom Composite Action** to standardize security and quality scans for Terraform code with zero code duplication.

### 🛠️ Action & Workflow Architecture
The custom action encapsulates `tflint` (for syntax/provider quality) and `trivy` (for misconfiguration scanning) into a single reusable module (`action.yml`). Workflows consume it by passing input parameters like `working-directory` and `fail-on-error`.
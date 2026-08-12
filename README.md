# 🚀 GitHub Actions Enterprise Mastery (GH-200)

This repository serves as a hands-on technical portfolio and study guide for the **GitHub Actions Certification (GH-200)**. It covers production-ready CI/CD patterns, DevSecOps practices, and workflow architectures.

---

## 📚 Table of Contents & Learning Path

| ID | Topic / Core Domain | Technical Concepts | Paths & Artifacts |
| :--- | :--- | :--- | :--- |
| **01** | **Matrix, Services & Artifacts** *(Domain 1 & 4)* | Parallel Matrices, PostgreSQL Service Containers, `$GITHUB_OUTPUT`, Artifact Retention | [Workflow](.github/workflows/01-matrix-services-artifacts.yml) \| [Code](src/app.py) |
| **02** | **Zero-Trust AWS Auth via OIDC** *(Domain 2 & 3)* | OpenID Connect, JWT Claims, IAM Trust Policies, Least Privilege, Passwordless CI/CD | [Workflow](.github/workflows/02-workflow-aws-oidc.yml) \| [Labs](labs/02-aws-oidc/) |

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

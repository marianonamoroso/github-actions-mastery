# 🚀 GitHub Actions Enterprise Mastery (GH-200)

This repository serves as a hands-on technical portfolio and study guide for the **GitHub Actions Certification (GH-200)**. It covers production-ready CI/CD patterns, DevSecOps practices, and workflow architectures.

---

## 📚 Table of Contents & Learning Path

| ID | Topic / Core Domain | Technical Concepts | Paths & Artifacts |
| :--- | :--- | :--- | :--- |
| **01** | **Matrix, Services & Artifacts** *(Domain 1 & 4)* | Parallel Matrices, PostgreSQL Service Containers, `$GITHUB_OUTPUT`, Artifact Retention | [Workflow](.github/workflows/01-matrix-services-artifacts.yml) \| [Code](src/app.py) |

---

## 01 - Matrix Strategies, Service Containers & Artifacts

### 🎯 Business Challenge
We need to validate a Python application against multiple runtime versions (`3.10` and `3.11`) across operational environments (`staging` and `production`). The execution requires an active PostgreSQL database instance to verify connectivity and must persist execution logs as audit artifacts without polluting the runner host.

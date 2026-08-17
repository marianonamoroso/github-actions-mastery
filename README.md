# 🚀 GitHub Actions Enterprise Mastery (GH-200)

This repository serves as a hands-on technical portfolio and study guide for the **GitHub Actions Certification (GH-200)**. It covers production-ready CI/CD patterns, DevSecOps practices, and workflow architectures.

---

## 📚 Table of Contents & Learning Path

| ID | Topic / Core Domain | Technical Concepts | Paths & Artifacts |
| :--- | :--- | :--- | :--- |
| **01** | **Matrix, Services & Artifacts** *(Domain 1 & 4)* | Parallel Matrices, PostgreSQL Service Containers, `$GITHUB_OUTPUT`, Artifact Retention | [Workflow](.github/workflows/01-matrix-services-artifacts.yml) \| [Code](labs/01-matrix-services/src/app.py) |
| **02** | **Zero-Trust AWS Auth via OIDC** *(Domain 2 & 3)* | OpenID Connect, JWT Claims, IAM Trust Policies, Least Privilege, Passwordless CI/CD | [Workflow](.github/workflows/02-workflow-aws-oidc.yml) \| [Labs](labs/02-aws-oidc/) |
| **03** | **Custom Composite Action (IaC Security & Quality)** *(Domain 1 & 4)* | Composite Actions (`action.yml`), TFLint, Trivy SAST, Centralized `env`/`vars`, Artifact Retention | [Workflow](.github/workflows/03-workflow-scan.yml) \| [Labs](labs/03-iac-security-check/) |
| **04** | **Reusable Workflows & CD Environments** *(Domain 1, 2 & 3)* | `workflow_call`, Caller vs Callable, `secrets: inherit`, GitHub Environments & Manual Protection Rules | [Workflow Invocador](.github/workflows/04-workflow-cd-pipeline.yml) \| [Reusable](.github/workflows/04-reusable-cd.yml) \| [Lab](labs/04-reusable-cd/) |
| **05** | **Concurrency Controls, Dynamic Matrix & Self-Hosted** *(Domain 1 & 2)* | Workflow Cancellation (`cancel-in-progress`), Resilient Matrix (`fail-fast: false`), Multi-OS Targets, Self-Hosted Architecture | [Workflow](.github/workflows/05-concurrency-matrix.yml) \| [Lab](labs/05-concurrency-matrix/) |

---

## 01 - Matrix Strategies, Service Containers & Artifacts

### 🎯 Business Challenge  (LAB01)

We need to validate a Python application against multiple runtime versions (`3.10` and `3.11`) across operational environments (`staging` and `production`). The execution requires an active PostgreSQL database instance to verify connectivity and must persist execution logs as audit artifacts without polluting the runner host.

### 🛠️ Workflow Architecture (LAB01)

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     Matrix Execution (4 Jobs)                          │
│                                                                        │
│  [Python 3.10 / Staging] ───┐                                          │
│  [Python 3.10 / Prod]    ───┼──► Local Postgres Container (Port 5432)  │
│  [Python 3.11 / Staging] ───┤           │                              │
│  [Python 3.11 / Prod]    ───┘           ▼                              │
│                                Execute App & Persistence               │
│                                         │                              │
│                                         ▼                              │
│                           Upload Artifacts (Zip Log)                   │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 02 - Zero-Trust AWS Authentication via OpenID Connect (OIDC)

### 🎯 Business Challenge (LAB02)

Storing long-lived static cloud credentials (`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`) in GitHub Secrets introduces critical security risks, including credential leakage, lack of automated rotation, and overly broad privileges. We need to eliminate static credentials entirely by establishing a passwordless, short-lived authentication mechanism between GitHub Actions and AWS IAM using OpenID Connect (OIDC).

### 🛠️ Workflow Overview (LAB02)

Instead of exchanging fixed secrets, the GitHub runner requests a short-lived JSON Web Token (JWT) from GitHub's OIDC Provider. AWS Security Token Service (STS) validates the token against a strict IAM Trust Policy and exchanges it for temporary AWS security credentials.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                         OIDC Authentication Flow                       │
│                                                                        │
│  1. Runner ──► Request OIDC Token ──► GitHub OIDC Provider             │
│  2. GitHub OIDC ──► Issues Signed JWT Token ──► Runner                 │
│  3. Runner ──► Present JWT to AWS STS (AssumeRoleWithWebIdentity)      │
│  4. AWS STS ──► Validates JWT with IAM Trust Policy                    │
│  5. AWS STS ──► Issues Temporary Security Credentials ──► Runner       │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 03 - Custom Composite Action (IaC Security & Quality Scanner)

### 🎯 Business Challenge (LAB03)

As Infrastructure-as-Code (IaC) adoption scales across multiple development teams, manually maintaining linting, formatting, and static application security testing (SAST) in individual workflows creates maintenance bottlenecks, inconsistent security baselines, and drift. We need an enterprise-grade, reusable **Custom Composite Action** to standardize security and quality scans for Terraform code with zero code duplication.

### 🛠️ Workflow Architecture (LAB03)

The custom action encapsulates `tflint` (for syntax/provider quality) and `trivy` (for misconfiguration scanning) into a single reusable module (`action.yml`). Workflows consume it by passing input parameters like `working-directory` and `fail-on-error`.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Workflow Execution                              │
│                                                                        │
│  1. Checkout Code ──► 2. Run Composite Action (./.github/actions)      │
│                              │                                         │
│                              ├─► Step A: Setup & Exec TFLint (JSON)    │
│                              └─► Step B: Exec Trivy Scan (JSON)        │
│                              │                                         │
│                       3. Upload Reports as Artifacts (v4)              │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 04 - Reusable Workflows & CD Environments

### 🎯 Business Challenge (LAB04)

To prevent drift, bypass of approval processes, and duplication across application deployment pipelines, we need a centralized, standard CD template. This pipeline must automatically deploy to `staging` upon passing checks, but require a mandatory manual approval gate before promoting changes to `production`.

### 🛠️ Workflow Architecture (LAB04)

We decouple the orchestration logic (Caller Workflow) from the execution logic (Reusable Workflow).

```text
┌────────────────────────────────────────────────────────────────────────┐
│                            Caller Workflow                             |
|                                                                        │
│                                   │                                    │
│  1. Job: DeployStaging ───────────┼───► 04-reusable-cd.yml             │
│                                   │     (environment: staging)         │
│  2. Job: DeployProduction ────────┼───► 04-reusable-cd.yml             │
│     (needs: DeployStaging)        │     (environment: production)      │
│                                   │                │                   │
│                                   │     [Requires Manual Gate]         │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 05 - Concurrency Controls, Dynamic Matrix & Self-Hosted Architecture

### 🎯 Business Challenge (LAB05)

High-frequency commit pushes or manual triggers often lead to redundant, overlapping pipeline runs that waste compute resources and runner minutes. We need an automated strategy to terminate stale workflow executions, control matrix failures resiliently (`fail-fast: false`), and target multi-OS runner environments efficiently.

### 🛠️ Workflow Architecture (LAB05)


```text
┌────────────────────────────────────────────────────────────────────────┐
│                   Concurrency Group Execution                          │
│                                                                        │
│  Trigger Run #1 ──► [In Progress] ──┐                                  │
│                                     ├──► Trigger Run #2 (New Commit)   │
│                                     │         │                        │
│                                     ▼         ▼                        │
│                           [Run #1 Cancelled] [Run #2 Executes]         │
│                                               │                        │
│                                               ▼                        │
│                          Matrix Execution (Multi-OS)                   │
│                       ┌───────────────────────┬──────────────────────┐ │
│                       │  Ubuntu + Py 3.10     │  Ubuntu + Py 3.11    │ │
│                       ├───────────────────────┼──────────────────────┤ │
│                       │  Windows + Py 3.11    │ [Win + 3.10 Excluded]│ │
│                       └───────────────────────┴──────────────────────┘ │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Local Developer Experience & IDE Setup

To enable native **IntelliSense, syntax validation, and JSON Schema autocompletion** for both Workflows and Composite Actions in VS Code:

### 1. Recommended Extensions

* **GitHub Actions** (`github.vscode-github-actions`) — Official GitHub extension.
* **YAML** (`redhat.vscode-yaml`) — Red Hat schema validation engine.

### 2. VS Code Configuration (`.vscode/settings.json`)

Ensure proper file associations and schema binding to prevent generic YAML fallback:

```json
{
  "files.associations": {
    "**/.github/workflows/*.yml": "github-actions-workflow",
    "**/.github/workflows/*.yaml": "github-actions-workflow",
    "**/.github/actions/**/action.yml": "github-actions-workflow",
    "**/.github/actions/**/action.yaml": "github-actions-workflow"
  },
  "yaml.schemas": {
    "[https://json.schemastore.org/github-workflow.json](https://json.schemastore.org/github-workflow.json)": [
      "**/.github/workflows/*.yml",
      "**/.github/workflows/*.yaml"
    ],
    "[https://json.schemastore.org/github-action.json](https://json.schemastore.org/github-action.json)": [
      "**/action.yml",
      "**/action.yaml"
    ]
  },
  "yaml.validate": true,
  "yaml.completion": true
}
```

### 3. VS Code Configuration (`keybindings.json`)

```json
[
  {
    "key": "alt+space",
    "command": "editor.action.triggerSuggest",
    "when": "editorHasCompletionItemProvider && textInputFocus && !editorReadonly && !suggestWidgetVisible"
  }
]

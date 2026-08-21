# 🚀 GitHub Actions Enterprise Mastery (GH-200)

This repository serves as a hands-on technical portfolio and study guide for the **GitHub Actions Certification (GH-200)**. It covers production-ready CI/CD patterns, DevSecOps practices, and workflow architectures.

> 💡 **Local Developer Tip:** To enable native IntelliSense, syntax validation, and JSON schemas in VS Code, check the [IDE Configuration](#️-local-developer-experience--ide-setup) section.
---

## 📚 Table of Contents & Learning Path

| ID | Topic / Core Domain | Technical Concepts | Paths & Artifacts |
| :--- | :--- | :--- | :--- |
| **01** | **Matrix, Services & Artifacts** *(Domain 1 & 4)* | Parallel Matrices, PostgreSQL Service Containers, `$GITHUB_OUTPUT`, Artifact Retention | [Workflow](.github/workflows/01-matrix-services-artifacts.yml) \| [Lab](labs/01-matrix-services/) |
| **02** | **Zero-Trust AWS Auth via OIDC** *(Domain 2 & 3)* | OpenID Connect, JWT Claims, IAM Trust Policies, Least Privilege, Passwordless CI/CD | [Workflow](.github/workflows/02-workflow-aws-oidc.yml) \| [Lab](labs/02-aws-oidc/) |
| **03** | **Custom Composite Action (IaC Security & Quality)** *(Domain 1 & 4)* | Composite Actions (`action.yml`), TFLint, Trivy SAST, Centralized `env`/`vars`, Artifact Retention | [Workflow](.github/workflows/03-workflow-scan.yml) \| [Action](.github/actions/iac-security-check/action.yml) \| [Lab](labs/03-iac-security-check/) |
| **04** | **Reusable Workflows & CD Environments** *(Domain 1, 2 & 3)* | `workflow_call`, Caller vs Callable, `secrets: inherit`, GitHub Environments & Manual Protection Rules | [Caller Workflow](.github/workflows/04-workflow-cd-pipeline.yml) \| [Reusable Workflow](.github/workflows/04-reusable-cd.yml) \| [Lab](labs/04-reusable-workflow/) |
| **05** | **Concurrency Controls, Dynamic Matrix & Self-Hosted** *(Domain 1 & 2)* | Workflow Cancellation (`cancel-in-progress`), Resilient Matrix (`fail-fast: false`), Multi-OS Targets, Self-Hosted Architecture | [Workflow](.github/workflows/05-concurrency-matrix.yml) \| [Lab](labs/05-concurrency-matrix/) |
| **06** | **SAST & Security Scanning with CodeQL** *(Domain 2 & 4)* | AST & Taint Tracking, Least Privilege (`security-events: write`), SARIF Upload, Advanced Security Dashboard | [Workflow](.github/workflows/06-workflow-codeql.yml) \| [Lab](labs/06-codeql-security/) |
| **07** | **Dynamic Release Management & Auto-tagging** *(Domain 1 & 4)* | SemVer Calculation, `$GITHUB_OUTPUT`, GitHub CLI (`gh`), `contents: write`, Asset Packaging | [Workflow](.github/workflows/07-workflow-release.yml) \| [Lab](labs/07-release-management/) |
| **08** | **Security Hardening & Supply Chain Protection** *(Domain 2 & 4)* | `::add-mask::`, Script Injection Mitigation, Action SHA Pinning, Immutable Supply Chain | [Workflow](.github/workflows/08-workflow-hardening.yml) \| [Lab](labs/08-security-hardening/) |
| **09** | **Runner Governance, ARC & Enterprise Policies** *(Domain 2 & 3)* | Self-Hosted Runners, ARC on K8s, Ephemeral Lifecycles, `runner.*` Context, Runner Groups | [Workflow](.github/workflows/09-workflow-governance.yml) \| [Lab](labs/09-runner-governance/) |

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

## 06 - SAST & Security Scanning with GitHub CodeQL

### 🎯 Business Challenge (LAB06)

Traditional regex-based security linters produce high false-positive rates and fail to understand contextual data flows across application layers. To prevent critical security flaws (such as SQL Injections and Command Injections) from reaching production, we need an automated **Static Application Security Testing (SAST)** engine embedded directly into the CI/CD lifecycle. This pipeline must perform semantic taint tracking, adhere to the Least Privilege model, and ingest structured SARIF reports directly into the GitHub Security dashboard without relying on third-party SaaS platforms.

### 🛠️ Workflow Architecture (LAB06)

The pipeline checks out the codebase with read-only permissions, initializes the CodeQL semantic database using extended security query suites (`security-extended,security-and-quality`), and evaluates execution paths from user-controlled inputs (*sources*) to execution methods (*sinks*). Results are formatted into a standard SARIF payload and pushed to GitHub Advanced Security via `security-events: write`.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        CodeQL SAST Pipeline                            │
│                                                                        │
│  1. Checkout Code (contents: read)                                     │
│            │                                                           │
│            ▼                                                           │
│  2. CodeQL Init (github/codeql-action/init@v3)                         │
│     ├─ Target: Python AST & Data Flow Graph                            │
│     └─ Suites: security-extended, security-and-quality                 │
│            │                                                           │
│            ▼                                                           │
│  3. CodeQL Analyze (github/codeql-action/analyze@v3)                   │
│     ├─ Taint Tracking (Source ──► Sanitizer ──► Sink)                  │
│     └─ Generates SARIF Report (CWE-89 SQLi, CWE-78 RCE)                │
│            │                                                           │
│            ▼                                                           │
│  4. Publish to GitHub Security Tab (security-events: write)            │
│     └─ Updates "Code scanning alerts" Dashboard                        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 07 - Dynamic Release Management & Auto-tagging

### 🎯 Business Challenge (LAB07)

Manual release processes are error-prone, lack consistent changelogs, and detach compiled assets from their source code tags. To streamline continuous delivery, we need an automated pipeline that dynamically calculates Semantic Versioning (SemVer), packages the application into production-ready distribution assets, and publishes a formal GitHub Release with automated notes—ensuring every deployment artifact is strictly tied to an immutable Git milestone.

### 🛠️ Workflow Architecture (LAB07)

The workflow relies on `workflow_dispatch` inputs to determine the version bump. It leverages `$GITHUB_OUTPUT` to pass the computed tag across isolated steps and uses the native GitHub CLI (`gh`) to securely interact with the platform API, requiring elevated `contents: write` permissions.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Release Management Pipeline                     │
│                                                                        │
│  1. Manual Trigger (workflow_dispatch: patch/minor/major)              │
│            │                                                           │
│            ▼                                                           │
│  2. Calculate SemVer (Bash script + git describe)                      │
│     └─► Outputs: $GITHUB_OUTPUT (new_tag=v1.2.0)                       │
│            │                                                           │
│            ▼                                                           │
│  3. Package Asset (tar -czf app-v1.2.0.tar.gz)                         │
│     └─► Consumes: steps.semver.outputs.new_tag                         │
│            │                                                           │
│            ▼                                                           │
│  4. Publish GitHub Release (gh CLI via GITHUB_TOKEN)                   │
│     ├─ Push Tag: v1.2.0 (contents: write)                              │
│     ├─ Generate automated release notes                                │
│     └─ Upload Asset: app-v1.2.0.tar.gz                                 │
└────────────────────────────────────────────────────────────────────────┘
```

---

## 08 - Enterprise Security Hardening & Supply Chain Protection

### 🎯 Business Challenge (LAB08)

Dynamic CI/CD workflows frequently process untrusted input and handle ephemeral credentials generated at runtime. Using mutable action tags exposes pipelines to supply chain hijacking, while direct context interpolation in shell blocks enables Script Injection (RCE). We need to enforce strict enterprise hardening: cryptographic Action Pinning, dynamic runtime secret masking, and safe environment variable binding.

### 🛠️ Workflow Architecture (LAB08)

The workflow demonstrates defense-in-depth: pinning actions by immutable 40-character SHAs, sanitizing the log output buffer using the workflow command `::add-mask::`, and passing untrusted inputs strictly via OS environment variables to prevent command execution.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        Hardened Security Pipeline                      │
│                                                                        │
│  1. Checkout Code ──► Immutable Action Pinning (Commit SHA)            │
│            │                                                           │
│            ▼                                                           │
│  2. Generate Dynamic Secret ──► echo "::add-mask::$TOKEN"              │
│     └─► Runner Redaction Engine captures pattern                       │
│            │                                                           │
│            ▼                                                           │
│  3. Standard Output Log ──► Intercepted & Replaced with "***"          │
│            │                                                           │
│            ▼                                                           │
│  4. Untrusted Payload ($INPUT) ──► Bound to System Env ($RAW_INPUT)    │
│     └─► Bash processes literal data string (No Shell Execution)        │
└────────────────────────────────────────────────────────────────────────┘
```
g
---

## 09 - Runner Governance, Autoscaling (ARC) & Enterprise Policies

### 🎯 Business Challenge (LAB09)

Static self-hosted runner virtual machines suffer from configuration drift, persistent state pollution, high idle cloud costs, and severe security risks if shared across untrusted repositories. To maintain enterprise compliance and security isolation, we need an automated strategy utilizing Kubernetes-native Autoscaling Runner Controller (ARC) for ephemeral runner provisioning, combined with strict organizational runner group boundaries and context-driven audit policies.

### 🛠️ Workflow Architecture (LAB09)

The workflow dynamically evaluates target execution environments, inspects runner host metadata via the `runner.*` context object, and enforces governance boundaries for ephemeral container workloads.

```text
┌────────────────────────────────────────────────────────────────────────┐
│                     Runner Governance Architecture                     │
│                                                                        │
│  1. Dynamic Target Selection (workflow_dispatch / labels)              │
│            │                                                           │
│            ▼                                                           │
│  2. Ephemeral Compute Provisioning (K8s ARC / GitHub-Hosted)           │
│     └─ Single-Job Execution (Zero Persistent State)                    │
│            │                                                           │
│            ▼                                                           │
│  3. Runner Context Inspection (runner.os, runner.arch, runner.name)   │
│     └─ Runtime Verification of Environment Compliance                  │
│            │                                                           │
│            ▼                                                           │
│  4. Job Execution & Auto-Teardown                                      │
│     └─ Immediate destruction of runner compute host                    │
└────────────────────────────────────────────────────────────────────────┘
```

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

---

### 3. VS Code Configuration (`keybindings.json`)

```json
[
  {
    "key": "alt+space",
    "command": "editor.action.triggerSuggest",
    "when": "editorHasCompletionItemProvider && textInputFocus && !editorReadonly && !suggestWidgetVisible"
  }
]

# Lab 06: SAST & Security Scanning with GitHub CodeQL

## Overview

Implementation of an automated **Static Application Security Testing (SAST)** pipeline using GitHub's native semantic analysis engine (**CodeQL**). 

The goal of this lab is to perform deep abstract syntax tree (AST) and taint tracking analysis over application source code, catching vulnerabilities before merging to production.

---

## Architectural & Security Decisions

* **Semantic Taint Analysis:** Unlike regex-based linters, CodeQL traces untrusted user inputs (*sources*) to critical execution methods (*sinks*).
* **Least Privilege Model (`GITHUB_TOKEN`):**
  * `contents: read` — Clone and parse repository source code.
  * `security-events: write` — Upload SARIF (Static Analysis Results Interchange Format) reports to GitHub Security.
  * `actions: read` — Sychronize execution metadata with previous runs.
* **Extended Security Queries:** Configured with `security-extended,security-and-quality` suites to capture critical CVEs, CWE patterns, and code smells.

---

## Vulnerabilities Covered in Mock Application

* **CWE-89 (SQL Injection):** Unsanitized query concatenation mapped in `vulnerable_app.py`.
* **CWE-78 (OS Command Injection):** Direct invocation of `os.system` with external parameters.

---

## How to Trigger & Inspect Findings

1. Trigger the workflow via `git push origin main` or manually using `workflow_dispatch`.
2. Navigate to the repository tab: **Security** -> **Vulnerability alerts** -> **Code scanning**.
3. Inspect the alerts to evaluate the execution path, data flow traces, and remediation guidance.
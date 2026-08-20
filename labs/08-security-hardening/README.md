# Lab 08: Enterprise Security Hardening & Supply Chain Protection

## Overview

Implementation of enterprise-grade security defenses in GitHub Actions workflows to prevent credential leakage, supply chain tampering, and remote code execution via script injection vulnerabilities.

---

## Architectural & Security Decisions

* **Full Commit SHA Pinning:** Third-party actions are pinned to complete 40-character commit SHAs instead of mutable tags (`@v4`), ensuring cryptographic immutability and preventing upstream supply chain attacks.
* **Dynamic Secret Masking (`::add-mask::`):** Run-time generated secrets and dynamic credentials are registered into the runner's redaction engine immediately upon creation to prevent accidental exposure in CI logs.
* **Script Injection Mitigation:** Untrusted input from GitHub contexts (`github.event.inputs.*`) is strictly passed through intermediate environment variables (`env:`) rather than inline expression interpolation (`${{ ... }}`), neutralizing shell metacharacter injection.
* **Strict Least Privilege Token:** Scoped to `contents: read` to prevent lateral movement or unauthorized mutations if the runner environment is compromised.

---

## Execution Flow

1. **Checkout Repository:** Fetches the codebase using an immutable commit SHA (`actions/checkout@692973e...`).
2. **Ephemeral Secret Generation & Masking:** Generates a dynamic token, registers it via `echo "::add-mask::$TOKEN"`, and exports it through `$GITHUB_OUTPUT`.
3. **Log Sanitization Check:** Attempts to output the token to stdout, verifying that the runner engine automatically redacts it as `***`.
4. **Safe Input Processing:** Accepts an untrusted payload containing shell metacharacters (`;`, `$()`) and safely renders it via system environment variable binding without executing commands.

---

## How to Trigger & Inspect Findings

1. Navigate to **Actions** -> **08 - Security Hardening**.
2. Click **Run workflow** (leave the default simulated injection payload).
3. Open the execution logs:
   * Inspect **Verify Secret Masking in Logs** to confirm the generated token is masked as `***`.
   * Inspect **Process Untrusted Input Securely** to confirm the injection string is handled as plain text rather than executing arbitrary commands.
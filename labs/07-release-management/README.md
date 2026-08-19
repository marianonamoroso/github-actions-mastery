# Lab 07: Dynamic Release Management & Auto-tagging

## Overview

Automation of the versioning lifecycle using Semantic Versioning (SemVer) and GitHub Releases. This pipeline eliminates manual tagging and asset packaging, ensuring that every distributed binary is cryptographically linked to a specific, immutable point in the Git history.

---

## Architectural & Security Decisions

* **Native GitHub CLI Integration:** Using `gh release create` instead of third-party Actions reduces supply chain attack surface. 
* **State Management via `$GITHUB_OUTPUT`:** Context passing between steps (tag calculation -> asset packaging -> release publishing) is handled via explicitly scoped outputs rather than polluting the global runner environment.
* **Least Privilege Model (`GITHUB_TOKEN`):** 
  * `contents: write` is strictly required and scoped to allow the workflow to push Git Tags and create GitHub Releases via the API.

---

## Execution Flow

1. **Calculate Next Version:** Evaluates the latest Git tag and increments it based on the user's manual input (patch, minor, major).
2. **Build Asset:** Compresses the application source/binary into a `.tar.gz` distribution file.
3. **Publish Release:** Pushes the new Git tag, generates automated release notes based on merged PRs/commits, and attaches the tarball asset to the GitHub Release.

---

## How to Trigger & Inspect Findings

1. Navigate to **Actions** -> **07 - Release Management**.
2. Click **Run workflow** and select the release bump type (`patch`, `minor`, `major`).
3. Once completed, navigate to the **Releases** section on the repository's main page to verify the published tag, changelog, and attached asset.
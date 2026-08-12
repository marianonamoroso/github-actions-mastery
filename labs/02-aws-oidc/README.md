### 🛠️ Pre-requisite: AWS OIDC Identity Provider Setup

Before assuming roles, AWS IAM must be configured to trust GitHub's OIDC issuer.

1. **AWS Console Navigation:** Go to **IAM** -> **Identity providers** -> **Add provider**.
2. **Configuration Settings:**
   * **Provider Type:** `OpenID Connect`
   * **Provider URL:** `https://token.actions.githubusercontent.com`
   * **Audience:** `sts.amazonaws.com`
3. **Thumbprint Verification:** Click **Get thumbprint** to retrieve and attach GitHub's top-level CA fingerprint.
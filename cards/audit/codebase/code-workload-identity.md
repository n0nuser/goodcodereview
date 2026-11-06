---
id: code-workload-identity
level: codebase
tags: [security, supply-chain, ci, credentials]
severity: should-fix
status: stable
lang: core
applies_when: A CI job or a service authenticates to a cloud provider.
tool_gate: none
note: exchange for a short-lived credential backed by GitHub (no long-lived AWS secrets), Google (federated identities instead of a service account key) and Microsoft Entra (federation without managing secrets); pin the trust policy backed by GitHub (at least one condition, evaluate `sub`), Google (attribute condition) and GitLab (claims as condition keys in trust policies); GitLab's ID token page describes the token and its claims and does not argue against stored secrets
borrowed_from:
  - https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws
  - https://cloud.google.com/iam/docs/workload-identity-federation
  - https://docs.gitlab.com/ci/secrets/id_token_authentication/
  - https://learn.microsoft.com/en-us/entra/workload-id/workload-identity-federation
---

**Rule.** Exchange the platform's OIDC token for a short-lived cloud credential, and pin the trust policy to the workload.

**Why.** A cloud key stored as a CI secret stays valid until someone rotates it, and every job that reads it can use it elsewhere. An OIDC token is minted for one job, expires with it, and names the repository, branch or environment. The cloud side has to check that name. A trust policy with no `sub` condition lets any repository assume the role.

**FAIL**

```yaml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**PASS**

```yaml
on:
  push:
    branches: [main]
permissions:
  id-token: write
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@<40-char-sha>
        with:
          role-to-assume: arn:aws:iam::123456789012:role/deploy
          aws-region: eu-west-1
# trust policy condition:
# token.actions.githubusercontent.com:sub: repo:org/repo:ref:refs/heads/main
# repositories created after 15 July 2026, or opted in, use immutable IDs:
# repo:org@123456/repo@456789:ref:refs/heads/main
```

**Counterpoint.** "Static keys work with every provider and every runner." Some providers and self-hosted setups cannot issue an OIDC token, so a scoped key is the fallback. If a key is unavoidable, scope it to the one deploy action, keep it in the platform's secret store rather than in the repository, rotate it, and keep the deploy job away from pull request code. Where OIDC is available, use it and pin the claim.

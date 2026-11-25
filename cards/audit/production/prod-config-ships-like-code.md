---
id: prod-config-ships-like-code
level: production
tags: [reliability, deploys, config]
severity: should-fix
status: stable
lang: core
applies_when: A service has runtime configuration, feature-flag values or limits that can change in production.
tool_gate: Production config store writable only by the deploy pipeline; the config repository requires review before merge.
note: Google SRE (config changes lack the review and testing code gets; keep config in source control for history, rollback and review), Amazon Builders' Library (runtime config such as rate limits and feature flags ships in a dedicated pipeline with the same safety mechanisms as code) and Microsoft (a configuration or feature-flag update carries deployment risk and every deployment must follow a standard, automated pattern). OpenGitOps describes a method and is not counted
borrowed_from:
  - https://sre.google/workbook/configuration-design/
  - https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/
  - https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments
---

**Rule.** Change configuration and flag values through a reviewed commit and the same staged, automated pipeline as code, not by hand on a host or console.

**Why.** One configuration value can change behaviour as much as a code change, with less testing and review. A hand edit leaves no history, no second reader and no rollback, and it skips the canary that would catch the mistake ([[prod-canary-staged-rollout]]).

**FAIL**

```text
ssh prod-3 "sed -i 's/rate_limit: 100/rate_limit: 1000/' /etc/app/config.yaml"
```

**PASS**

```text
PR "raise rate_limit to 1000" -> reviewed -> merged -> config pipeline: 5% of hosts, health check, then the rest, auto-rollback on failure
```

**Counterpoint.** "In an incident we need to change a value now." An out-of-band change is allowed when the pipeline is too slow, as long as a commit records the same value straight after, so the repository stays the source of truth. A fast config pipeline makes the exception rare.

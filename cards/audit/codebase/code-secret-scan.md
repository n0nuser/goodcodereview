---
id: code-secret-scan
level: codebase
tags: [security, process, secrets, ci]
severity: block
status: draft
lang: core
applies_when: Any repository, including its history, issues and pull requests.
tool_gate: Secret scanning on push (provider or pre-commit hook) with push protection on.
borrowed_from:
  - https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning
  - https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
  - https://www.cisa.gov/resources-tools/resources/product-security-bad-practices
---

**Rule.** Scan for committed credentials, and treat any hit as leaked: revoke and replace it first.

**Why.** A secret in history is readable by everyone with clone access, and forks and caches keep it after a rewrite. Rewriting history is slow and often unnecessary once the secret is dead.

**FAIL**

```text
git log -p | rg 'AKIA'      # a live cloud key in an old commit; "removed it in the next commit"
```

**PASS**

```text
scanner runs on every push and covers history
key revoked and reissued the same day; new value comes from the secret store
```

**Counterpoint.** "Scanners give false positives." Tune with an allowlist of reviewed, non-secret strings. A missed live key costs far more than a triaged alert. [[sys-secrets-and-errors]] covers where secrets live at runtime.

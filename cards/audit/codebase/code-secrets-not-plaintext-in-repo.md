---
id: code-secrets-not-plaintext-in-repo
level: codebase
tags: [security, secrets]
severity: should-fix
status: stable
lang: core
applies_when: Auditing source files, config files and infrastructure code for credentials, keys and tokens.
tool_gate: Secret scanning on push; a lint that rejects literal values for fields named password, token or key.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
  - https://docs.gitlab.com/user/application_security/secret_detection/
  - https://www.cisa.gov/resources-tools/resources/product-security-bad-practices
  - https://laravel.com/docs/12.x/configuration
  - https://symfony.com/doc/current/configuration.html
  - https://nextjs.org/docs/app/guides/environment-variables
  - https://vite.dev/guide/env-and-mode
---

**Rule.** Keep secrets out of source code and config.

**Why.** Anyone with read access to the repository, and every clone and fork, gets a plaintext secret, and removing it later does not recall the copies. Read the secret at run time from a secret store, and it can be rotated without a code change. [[code-env-files-ignored]] covers local `.env` files.

**FAIL**

```python
DB_PASSWORD = "S3cr37-prod"
conn = connect(host="db.internal", user="app", password=DB_PASSWORD)
```

**PASS**

```python
import os
conn = connect(host="db.internal", user="app", password=os.environ["DB_PASSWORD"])
```

**Counterpoint.** "Environment variables are plaintext too, and they leak into process listings and crash dumps." True, so the secret store is the source and the variable is only the hand-off. Mount the value from the store at start, and keep it out of logs. [[code-secret-scan]] covers finding a secret that is already committed.

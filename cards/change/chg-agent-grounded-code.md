---
id: chg-agent-grounded-code
level: change
tags: [agents, ai-generated, reuse]
severity: block
status: draft
lang: core
applies_when: The change was written fully or partly by an AI agent.
tool_gate: Compiler, type checker and dependency-resolution in CI catch non-existent imports and calls.
borrowed_from:
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
---

**Rule.** Check every external call and import exists with that signature, and that the code does not re-implement a helper already in the repo; the author can explain each hunk.

**Why.** Agents invent plausible APIs and rewrite nearby utilities without searching. A green build only proves what the compiler sees.

**FAIL**

```python
import requests_cache_pro                # package does not exist
total = sum_cents(items)                 # new helper; money.sum_cents() already exists
resp = client.fetch_json(url, retries=3) # fetch_json has no retries param
```

**PASS**

```python
from money import sum_cents
resp = client.fetch_json(url)   # signature checked against source
```

**Counterpoint.** "Humans make the same mistakes." True, but agents make them fluently and at volume, and disclosure alone does not catch them. Kubernetes requires disclosure and an author who can explain the change; the specific failure modes here are practitioner observation with no study in the notes.

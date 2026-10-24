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

**Rule.** Verify that every import and external call the agent wrote exists with that signature.

**Why.** Agents invent plausible APIs and rewrite nearby utilities without searching. A green build proves only what the compiler sees. [[chg-reuse-before-write]] covers re-implemented helpers. The author must also be able to explain each hunk; see [[chg-agent-independent-review]].

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

**Counterpoint.** "Humans make the same mistakes." True, but agents make them fluently and at volume, and disclosure alone does not catch them. Kubernetes requires disclosure and an author who can explain the change. A compiler and a dependency check catch the mechanical part, so use this card for calls that resolve but behave differently than assumed.

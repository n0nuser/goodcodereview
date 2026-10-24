---
id: svc-bound-client-controlled-sizes
level: service
tags: [security, dos, api]
severity: should-fix
status: draft
lang: core
applies_when: A request parameter or body sets how many records, bytes, items or operations the server handles.
tool_gate: Gateway request-size limit; schema `maxLength`/`maxItems`; test with a 10 MB body and `limit=1000000`.
borrowed_from:
  - https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
  - https://genai.owasp.org/llmrisk/llm102025-unbounded-consumption/
---

**Rule.** Cap every client-controlled size and count on the server: body bytes, string length, array items, page size and batch size.

**Why.** A request for `limit=10000000` or a batch of 50,000 operations lets one client exhaust memory or the bill for a paid backend. The cap has to sit in the server, since a UI limit is not one. [[svc-rate-limit-quota]] and [[svc-timeouts]] cover rate and time; this card covers size.

**FAIL**

```text
limit = int(request.args["limit"])
rows = db.fetch(limit)                              # no ceiling
items: list[Item]                                    # schema with no maxItems
```

**PASS**

```text
limit = min(int(request.args.get("limit", 50)), 100)
items: list[Item] = Field(max_length=100)            # body capped at 1 MB by the proxy
```

**Counterpoint.** "Legit clients sometimes need big batches." Offer a documented bulk or export endpoint with its own quota. The default path stays capped.

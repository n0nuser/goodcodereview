---
id: svc-api-error-code-stable
level: service
tags: [api, errors]
severity: should-fix
status: draft
note: RFC 9457 and Google AIP-193 describe the mechanism; the rule never to reword a published code is inference from both
lang: core
applies_when: Callers of an HTTP or RPC API branch on the kind of error.
tool_gate: Spec linter that requires an enumerated error `type` or `reason` per operation; a test that pins the codes.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9457.html
  - https://google.aip.dev/193
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
---

**Rule.** Give each error a stable machine-readable code that callers branch on, and never make them parse the message text.

**Why.** Message text gets reworded, translated and fixed. A client that matches on "already exists" breaks on the first edit. A published code is a contract.

**FAIL**

```text
if "already exists" in response.json()["detail"]:   # client
    handle_conflict()
```

**PASS**

```text
if response.json()["type"] == "https://api.example.com/problems/order-exists":   # client
    handle_conflict()
# the server keeps that type value for as long as the API version lives
```

**Counterpoint.** "The HTTP status is enough." It is too coarse: two different 409 conflicts need different handling. Add a code only where callers act differently; do not mint one for every branch.

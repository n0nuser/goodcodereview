---
id: svc-api-conditional-writes
level: service
tags: [api, http, concurrency]
severity: should-fix
status: draft
lang: core
applies_when: Two callers can update the same resource through PUT, PATCH or DELETE.
tool_gate: Integration test that sends a write with a stale `If-Match` and expects 412.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9110.html
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.

**Why.** A read-modify-write over HTTP is a race. The second writer overwrites the first without knowing it, and no error appears anywhere.

**FAIL**

```text
GET /docs/4  -> 200 {title: "A"}
PUT /docs/4  {title: "B"}   -> 200   # overwrites a change made after the GET
```

**PASS**

```text
GET /docs/4  -> 200  ETag: "v7"
PUT /docs/4  If-Match: "v7"  -> 200  ETag: "v8"
PUT /docs/4  If-Match: "v7"  -> 412 Precondition Failed
```

**Counterpoint.** "Last write wins is fine here." For a log or a counter it is; say so in the spec. For a document, a profile or a config that two people edit, it loses work. Zalando makes ETag support a MAY, so the card applies to shared, human-edited resources.

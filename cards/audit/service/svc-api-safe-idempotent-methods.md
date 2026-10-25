---
id: svc-api-safe-idempotent-methods
level: service
tags: [compatibility, api, http]
severity: block
status: draft
lacks: duplicate, the GET half is already in stable svc-csrf-state-changing; PUT and DELETE have IETF only
note: RFC 9110 sections 9.2.1 and 9.2.2; Dropbox backs GET without side effects, which stable svc-csrf-state-changing also requires; PUT and DELETE idempotence has the IETF only
lang: core
applies_when: A service exposes HTTP endpoints, or a handler changes which method it accepts.
tool_gate: API linter, and an integration test that calls each GET twice and each PUT or DELETE twice and compares state.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9110.html
  - https://dropbox.tech/developers/limitations-of-the-get-method-in-http
---

**Rule.** Keep GET, HEAD and OPTIONS free of side effects, and make PUT and DELETE give the same end state when repeated.

**Why.** Clients, caches, prefetchers and crawlers repeat safe methods freely, and clients and proxies retry PUT and DELETE automatically after a connection failure. A GET that deletes or counts, or a PUT that appends, turns a retry into data loss or duplicates.

**FAIL**

```text
GET /reports/7/archive          -> moves report 7 to the archive
PUT /carts/9/items               -> appends the item again on each call
```

**PASS**

```text
POST /reports/7/archive          -> state change under an unsafe method
PUT /carts/9/items/42 {qty: 2}   -> sets the item; repeating it changes nothing
```

**Counterpoint.** "We need a link a user can click to confirm an email." Make the click a GET that shows a page, and have the page submit a POST. Logs or counters written by a GET are fine; the rule covers changes to resource state that a caller can see. Retries of POST fall under [[svc-idempotency-key]].

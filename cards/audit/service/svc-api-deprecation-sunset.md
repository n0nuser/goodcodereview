---
id: svc-api-deprecation-sunset
level: service
tags: [api, deprecation]
severity: should-fix
status: stable
lang: core
applies_when: A service retires an endpoint, field, version or parameter that outside callers use.
tool_gate: Middleware that adds both headers for routes tagged deprecated; a spec linter on `deprecated: true` without a sunset date; a dashboard counting calls that carry the headers.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9745.html
  - https://www.rfc-editor.org/rfc/rfc8594.html
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://spec.openapis.org/oas/v3.1.0.html
---

**Rule.** Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers, with the `Sunset` date no earlier than the `Deprecation` date.

**Why.** Callers cannot read your roadmap. A removal with no signal in the responses is an outage for whoever has not read the changelog. Counting calls that carry the headers also tells you when removal is safe.

**FAIL**

```text
git: delete GET /v1/orders/{id}/summary
responses before removal: no header, spec not marked deprecated
```

**PASS**

```text
GET /v1/orders/9/summary -> 200
  Deprecation: @1767225600
  Sunset: Wed, 01 Jul 2026 00:00:00 GMT
  Link: <https://api.example.com/docs/summary-removal>; rel="deprecation"
spec: deprecated: true
```

**Counterpoint.** "Our only callers are internal." Then the call count with the header gives you the list of owners to ask, and removal is cheap. [[chg-expand-contract]] covers the order of steps; this card covers what the response tells the caller. Both headers describe one resource, so send them on each deprecated route, not only on the API root.

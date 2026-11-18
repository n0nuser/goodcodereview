---
id: svc-api-version-on-every-request
level: service
tags: [compatibility, maintainability, api, versioning]
severity: should-fix
status: draft
lacks: unreviewed, sources listed but no stable pass has checked them against rules 1 to 10
lang: core
applies_when: The code calls an HTTP API that publishes dated or numbered versions, or the service offers one.
context: [server]
tool_gate: A shared HTTP client wrapper or gateway rule that sets the version, and a contract test that a request without one is rejected.
borrowed_from:
  - https://docs.github.com/en/rest/about-the-rest-api/api-versions
  - https://google.aip.dev/185
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
---

**Rule.** Name the API version on every request, in a header or a query parameter.

**Why.** A request with no version gets whatever the server treats as the default, and that default moves. The caller then breaks on the server's schedule, not its own. A request that names its version keeps the behaviour it was tested against until the caller moves it. Choosing the scheme and keeping a version stable are covered by [[svc-api-versioning-policy]].

**FAIL**

```text
GET /orders HTTP/1.1
Host: api.example.com
```

**PASS**

```text
GET /orders?api-version=2026-03-01 HTTP/1.1
Host: api.example.com
```

**Counterpoint.** "Always sending a version is clutter, and the latest is what we want anyway." The latest is only what you want on the day you tested it. Put the version in one client wrapper so call sites stay clean, and bump it as a reviewed change.

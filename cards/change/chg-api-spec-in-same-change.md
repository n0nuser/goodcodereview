---
id: chg-api-spec-in-same-change
level: change
tags: [compatibility, api, contracts]
severity: should-fix
status: draft
lacks: orgs, Kubernetes (spec in the same PR) and Zalando (spec first) back it; OpenAPI defines the format only; needs one more org
lang: core
applies_when: The diff adds, removes or changes an HTTP route, a request or response field, a status code or a header.
context: [server]
tool_gate: Breaking-change diff of the spec in CI, plus a check that fails when route files change and the spec file does not.
note: Kubernetes: update the swagger and OpenAPI spec with make update, as a commit separate from the code but in the same PR; Zalando: define APIs before coding; OpenAPI spec is a format definition, not a practice
borrowed_from:
  - https://spec.openapis.org/oas/v3.1.0.html
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-architecture/api_changes.md
---

**Rule.** Update the API spec in the same change that alters the routes, fields, status codes or headers it describes.

**Why.** A spec updated "later" is usually never updated. The reviewer also loses the one place where the shape of the change is readable at a glance.

**FAIL**

```text
diff: + @app.post("/orders/{id}/cancel")
      (no change to openapi.yaml)
```

**PASS**

```text
diff: + @app.post("/orders/{id}/cancel")
      + openapi.yaml: /orders/{id}/cancel with 204, 404 and 409 responses
```

**Counterpoint.** "The spec is generated, so every change updates it." Then the generated file is committed or checked in CI, and the diff shows it. If it is generated at build time and not committed, mark the card N/A. [[svc-api-spec-matches-impl]] checks the service as a whole.

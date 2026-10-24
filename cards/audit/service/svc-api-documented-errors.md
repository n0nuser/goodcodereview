---
id: svc-api-documented-errors
level: service
tags: [api, contracts, errors]
severity: should-fix
status: draft
note: OpenAPI requires only one response per operation; the stricter rule comes from Zalando rule 151
lang: core
applies_when: A service has an OpenAPI description, or callers depend on its error responses.
tool_gate: Spec linter that requires 4xx and 5xx responses with a schema on every operation, and an example on each.
borrowed_from:
  - https://spec.openapis.org/oas/v3.1.0.html
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Document every error status each operation can return, with a schema and one example.

**Why.** Callers write error handling from the spec. An operation that lists only 200 teaches them nothing about 404, 409, 422 or 429, so they find out in production.

**FAIL**

```text
/orders/{id}:
  get:
    responses:
      "200": {description: ok}
```

**PASS**

```text
/orders/{id}:
  get:
    responses:
      "200": {description: ok}
      "404": {$ref: "#/components/responses/Problem"}   # has an example
      "429": {$ref: "#/components/responses/RateLimited"}
```

**Counterpoint.** "A shared `default` response covers everything." OpenAPI allows `default`, but it hides which codes carry which meaning. List the codes a caller must act on and use `default` for the rest.

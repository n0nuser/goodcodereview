---
id: svc-api-spec-matches-impl
level: service
tags: [api, contracts]
severity: should-fix
status: draft
lang: core
applies_when: A service publishes an OpenAPI (Swagger) description that callers, SDK generators or gateways read.
tool_gate: Contract test or schema validation in CI that runs requests against the service and checks responses against the spec, or a spec generated from the code.
borrowed_from:
  - https://spec.openapis.org/oas/v3.1.0.html
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Keep the OpenAPI document as the source of truth, and generate it from the code or test the running service against it in CI.

**Why.** A hand-edited spec drifts from the handlers. Callers and generated SDKs then code against fields and codes the service does not return.

**FAIL**

```text
openapi.yaml (hand-written, last edited 14 months ago)
POST /orders returns {id, status, total_cents}; spec lists {id, status, total}
no CI step reads openapi.yaml
```

**PASS**

```text
CI: schemathesis run openapi.yaml --url $STAGING   # fails on any response the spec does not describe
or: the framework emits the spec from the handler types and the file is committed
```

**Counterpoint.** "The spec is documentation, a stale one does little harm." Generated SDKs, gateways and mock servers read it as fact, and a wrong spec fails there first. If the team does not publish a spec, mark the card N/A.

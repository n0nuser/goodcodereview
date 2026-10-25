---
id: svc-api-trace-context
level: service
tags: [observability, api, tracing]
severity: should-fix
status: draft
lacks: orgs, W3C is the only backer; needs two more orgs that forward trace headers on every call
lang: core
applies_when: A service calls another service over HTTP while handling a request.
tool_gate: Instrumentation library or HTTP-client middleware that injects `traceparent`; an integration test that checks the outgoing header.
borrowed_from:
  - https://www.w3.org/TR/trace-context/
---

**Rule.** Forward `traceparent` and `tracestate` on every outgoing call, keep the incoming trace id, and set a new parent id for each hop.

**Why.** A hop that drops the header splits one request into two traces. When something is slow or failing, the trace ends at the service that forgot, and the next hop cannot be found.

**FAIL**

```text
resp = http.post(PAYMENTS_URL, json=body)   # no trace headers; a new trace starts in payments
```

**PASS**

```text
headers = {}
propagator.inject(headers)    # traceparent: 00-<trace-id>-<new-span-id>-01
resp = http.post(PAYMENTS_URL, json=body, headers=headers)
```

**Counterpoint.** "A mesh or agent handles it." Then show it propagates through your queue consumers and thread pools too; a sidecar sees only the network edge. Never put personal data in either header, since they travel to third parties. The id in log lines is [[svc-request-id-logging]].

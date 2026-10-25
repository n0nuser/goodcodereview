---
id: svc-request-id-logging
level: service
tags: [observability, logging]
severity: should-fix
status: draft
lacks: evidence, the W3C spec does not mention logs; only Honeycomb backs putting the id on every log line
lang: core
applies_when: A service handles requests and writes logs while doing so.
tool_gate: Logging middleware or formatter that injects the id; test that fails on a log line without it.
note: the trace-context spec does not mention logs; recording the id in log lines is inference, backed by the wide-events page
borrowed_from:
  - https://www.w3.org/TR/trace-context/
  - https://honeycomb.io/blog/structured-events-basis-observability
---

**Rule.** Put the request or trace id on every log line written during a request.

**Why.** Concurrent requests interleave in one log. Without a shared id, you cannot pull one request's lines together or match them with other services' logs and the trace.

**FAIL**

```text
log.info("payment failed")                 # which request?
```

**PASS**

```text
log.info("payment failed", extra={"trace_id": ctx.trace_id})   # id set once by middleware
```

**See also.** [[svc-api-trace-context]] covers the `traceparent` header that carries the id between services.

**Counterpoint.** "Ids are high-cardinality and will blow up our metrics." Keep them out of metric labels ([[prod-wide-events-bounded-labels]]). Logs and events are where per-request ids belong.

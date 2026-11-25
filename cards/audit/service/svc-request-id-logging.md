---
id: svc-request-id-logging
level: service
tags: [observability, logging]
severity: should-fix
status: draft
lacks: evidence, Microsoft, Datadog and Google recommend correlation ids in logs; none says every line; needs a source that does
lang: core
applies_when: A service handles requests and writes logs while doing so.
context: [server]
tool_gate: Logging middleware or formatter that injects the id; test that fails on a log line without it.
note: the trace-context spec does not mention logs; Microsoft (use correlation IDs consistently) and Datadog (trace IDs injected into logs improve correlation) recommend it, Google Cloud documents the LogEntry trace field; logs and traces are sampled independently, so the id belongs on the line even when the trace is dropped
borrowed_from:
  - https://www.w3.org/TR/trace-context/
  - https://honeycomb.io/blog/structured-events-basis-observability
  - https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability
  - https://docs.datadoghq.com/tracing/other_telemetry/connect_logs_and_traces.md
  - https://cloud.google.com/trace/docs/trace-log-integration
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

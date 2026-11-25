---
id: prod-metric-labels-bounded
level: production
tags: [observability, performance, metrics]
severity: should-fix
status: stable
lang: core
applies_when: A service records aggregated metrics (counters, histograms, gauges) with labels or dimensions.
tool_gate: A cardinality limit on the metrics backend; a lint that rejects labels named user_id, request_id or raw path.
note: Prometheus (no user IDs, email addresses or other unbounded sets), Microsoft Azure Monitor (never a constantly changing value; timestamp as the example) and Micrometer (normalize and bound user-supplied tag values; the 404 URI example)
borrowed_from:
  - https://prometheus.io/docs/practices/naming/
  - https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/metrics-custom-overview
  - https://docs.micrometer.io/micrometer/reference/concepts/naming.html
---

**Rule.** Give a metric label only a bounded set of values; never a user id, request id, email, timestamp or raw URL path.

**Why.** Every distinct label value creates a new time series. An unbounded label multiplies storage and query cost until the backend drops data or the bill arrives. User-supplied values are the usual cause, and a request path that includes ids or random 404 URLs is the sneakiest. Put per-request detail in a log line, span or event instead.

**FAIL**

```python
REQUESTS = Counter("app_requests_total", "Requests", ["user_id", "path"])
REQUESTS.labels(user_id=uid, path=request.url.path).inc()
```

**PASS**

```python
REQUESTS = Counter("app_requests_total", "Requests", ["route", "status"])
REQUESTS.labels(route=request.scope["route"].path, status=str(resp.status_code)).inc()   # "/users/{id}"
```

**Counterpoint.** "We need per-user numbers." Aggregated metrics are the wrong store for that. Wide-event and log stores are built for high-cardinality fields, so write the user id there and keep the metric label to the route and status class. A small, known set such as tenant tier or region is fine.

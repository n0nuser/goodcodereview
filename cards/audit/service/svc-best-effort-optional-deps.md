---
id: svc-best-effort-optional-deps
level: service
tags: [reliability, resilience, dependencies, observability]
severity: should-fix
status: draft
lacks: orgs, best-effort calls have Netflix, Uber and Cabify; counting every fallback has Cabify only
note: best-effort calls - Netflix (calls to metrics, logs and other systems are best-effort; a slow dependency degrades the graph and never blocks it), Uber (rate-limit clients fail open when the control plane is down), Cabify (skips non-critical details in a driver offer when it cannot collect them fast enough); a metric and alert on each fallback - Cabify only
lang: core
applies_when: The critical path of a request or a job calls a dependency whose data the product can do without, such as enrichment, recommendations, analytics, or a rate-limit control plane.
tool_gate: none
borrowed_from:
  - https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf
  - https://www.uber.com/es/en/blog/ubers-rate-limiting-system/
  - https://tech.cabify.com/blog/engineering/degraded-experiences
---

**Rule.** Give each call to a non-critical dependency a short budget and a default, so its failure degrades the result instead of failing the critical path, and count every fallback.

**Why.** An order page should not fail because the recommendations service is slow. Netflix makes enrichment best-effort, so a slow dependency can degrade its knowledge graph but never block it. Uber's rate-limit clients let traffic through when the control plane is down, because blocking would cause an outage of its own. Cabify drops non-critical details from a driver offer when it cannot collect them in time. It also puts metrics and alerts on every such fallback, because SLO dashboards built for critical flows miss them.

**FAIL**

```python
def trip_offer(trip_id):
    trip = trips.get(trip_id, timeout=0.5)
    eta = traffic.eta(trip.route, timeout=2.0)   # optional detail, but an error here fails the offer
    return Offer(trip, eta)
```

**PASS**

```python
def trip_offer(trip_id):
    trip = trips.get(trip_id, timeout=0.5)
    try:
        eta = traffic.eta(trip.route, timeout=0.1)
    except (TimeoutError, ConnectionError):
        eta = None                                # the offer goes out without the ETA
        degraded.labels(dep="traffic").inc()      # alert on this rate
    return Offer(trip, eta)
```

**Counterpoint.** "A silent default hides an outage." It does when nobody counts it, so the PASS needs the metric and an alert on it. Call a dependency non-critical only when the product works without its data. Authentication, payment, and authorization checks are critical, and they fail closed. Failing open on a rate limiter gives up protection to keep availability, so write that choice into the design. For the timeout itself, see [[svc-timeouts]]. To check that the fallback really runs, see [[prod-kill-switch-fallback]].

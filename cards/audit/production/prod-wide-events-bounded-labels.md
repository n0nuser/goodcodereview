---
id: prod-wide-events-bounded-labels
level: production
tags: [observability, telemetry]
severity: should-fix
status: draft
lang: core
applies_when: A request handler or job emits telemetry.
tool_gate: Lint for high-cardinality metric labels.
borrowed_from:
  - https://www.honeycomb.io/blog/time-to-version-observability-signs-point-to-yes
---

**Rule.** Emit one structured event per request carrying trace, tenant, build and flag state.

**Why.** Many narrow log lines cannot be joined to answer "who is affected". A metric labeled with user id explodes cost. Without a deploy marker, you cannot compare before and after. Also keep metric labels bounded and record deploys and flag changes as telemetry.

**FAIL**

```text
log("start"); log("db ok"); log("done")
metric requests{user_id="u81234"}
```

**PASS**

```text
event{trace, tenant, build, flag.x, status, duration_ms}
metric requests{route, status}
```

**Counterpoint.** This is a vendor position (one Honeycomb post), and its "metrics are the past" claim is not a review criterion. Only the structural checks above are. Wide events cost storage; sample if needed.

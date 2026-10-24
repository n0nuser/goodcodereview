---
id: prod-profile-on-demand
level: production
tags: [performance, observability]
severity: discuss
status: stable
lang: core
applies_when: A service runs in production where CPU, memory, or latency problems would need a diagnosis.
tool_gate: none
borrowed_from:
  - https://go.dev/doc/diagnostics
  - https://pkg.go.dev/net/http/pprof
  - https://grafana.com/docs/pyroscope/latest/introduction/continuous-profiling/
  - https://docs.cloud.google.com/profiler/docs/about-profiler
  - https://docs.python.org/3/library/profile.html
  - https://www.brendangregg.com/flamegraphs.html
---

**Rule.** Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.

**Why.** Test environments rarely match production load, so the hot path in a test run is often not the hot path in production. When latency spikes, a redeploy to add profiling loses the moment and changes the system you wanted to observe, so the profiler is in place before the incident and the runbook says how to reach it.

**FAIL**

```text
runbook "high CPU": restart the pod
no profiler agent, no /debug/pprof, no sampling profiler in the image
```

**PASS**

```text
continuous profiler agent at ~2% overhead, 14-day retention
or: pprof on 127.0.0.1:6060 only, reached by port-forward; steps in runbook
```

**Counterpoint.** "Profiling costs CPU and opens an endpoint." Sampling profilers stay at a few percent, and you can profile one replica at a time. Bind the endpoint to localhost or an admin port. A profile endpoint on a public listener is a security fail.

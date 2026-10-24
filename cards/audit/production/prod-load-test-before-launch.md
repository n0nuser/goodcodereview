---
id: prod-load-test-before-launch
level: production
tags: [performance, reliability, release, capacity]
severity: should-fix
status: stable
lang: core
applies_when: A new service, a new feature with its own traffic, or a large architecture change is about to launch.
tool_gate: Load-test job with thresholds (k6, Gatling) in the release pipeline.
borrowed_from:
  - https://sre.google/sre-book/reliable-product-launches/
  - https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/performance-test
  - https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_process_culture_load_test.html
  - https://grafana.com/docs/k6/latest/testing-guides/test-types/
  - https://grafana.com/docs/k6/latest/using-k6/thresholds/
---

**Rule.** Load test before launch, past the expected peak, with pass and fail thresholds written down.

**Why.** Overload behaviour is hard to predict from code, and launch traffic often beats the estimate. Test the whole workload on production-like infrastructure: testing one component, on smaller machines, or only up to the expected load misses the queue that fills first.

**FAIL**

```text
launch checklist: "load test: n/a, staging handled 50 rps fine"
expected peak 2,000 rps; no test above 1,000
```

**PASS**

```text
k6 stress run on the prod-sized env: ramp to 3x expected peak (6,000 rps)
thresholds: p99 < 400 ms, errors < 0.1%; result linked in the launch doc
```

**Counterpoint.** "A production-sized test environment costs too much." Size the test to the risk. A scaled-down environment is acceptable for a non-critical workload, and skipping the test is low risk for a small one. For a launch that could take down a shared dependency, the test is cheaper than the outage. Roll out in stages either way ([[prod-canary-staged-rollout]]).

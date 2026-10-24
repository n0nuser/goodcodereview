# production

## prod-canary-staged-rollout

severity: block  
concerns: reliability  
applies_when: A change, config or dependency update is rolled out to production.

**Rule.** Roll out in stages behind a canary, and abort by rule, not by judgment.

**Why.** A 100% push exposes everyone to the bug. A canary must be large and long enough to be representative. Errors of 20% on 5% of traffic are only 1% overall, so tie the canary to your error budget.

**FAIL**

```text
deploy: all hosts at once, no comparison, rollback = "ask someone"
```

**PASS**

```text
# compare the canary to a control on a few chosen metrics
5% canary 30m -> compare error rate, p99 -> auto-rollback if worse -> 25% -> 100%
```


**Counterpoint.** "Hotfixes can't wait." Then keep the canary short, not absent. Fleet tools should also have velocity limits. A hermetic, reproducible build tied to one revision is the precondition for rollback to mean anything.

## prod-latency-slo-percentile

severity: should-fix  
concerns: performance, observability  
applies_when: A latency SLO, dashboard, or alert is defined for a service.

**Rule.** Define latency SLOs and alerts on high percentiles, never on the mean.

**Why.** A mean can look healthy while 1 request in 100 takes seconds, and those are the users who leave. Averaging per-instance quantiles is also wrong: quantiles do not add, so compute the percentile from a histogram, the one form that aggregates correctly across replicas.

**FAIL**

```text
alert: avg(rate(request_seconds_sum[5m]) / rate(request_seconds_count[5m])) > 0.3
avg(http_latency{quantile="0.99"})        # averages summaries across pods
```

**PASS**

```text
histogram_quantile(0.99, sum by (le) (rate(request_seconds_bucket[5m]))) > 0.3
SLO: 99% of requests under 300 ms over 28 days
```

**Counterpoint.** "Percentiles are noisy at low traffic." They are, so set a minimum request count before the alert fires, or alert on the error budget burn rate. Pick bucket edges around the objective, or the percentile will be a guess between two wide buckets.

## prod-load-test-before-launch

severity: should-fix  
concerns: performance, reliability  
applies_when: A new service, a new feature with its own traffic, or a large architecture change is about to launch.

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

## prod-profile-on-demand

severity: discuss  
concerns: performance, observability  
applies_when: A service runs in production where CPU, memory, or latency problems would need a diagnosis.

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

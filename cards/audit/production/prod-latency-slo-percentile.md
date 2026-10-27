---
id: prod-latency-slo-percentile
level: production
tags: [performance, observability, slo]
severity: should-fix
status: stable
lang: core
applies_when: A latency SLO, dashboard, or alert is defined for a service.
tool_gate: Lint alert rules for avg() over latency or over pre-computed quantiles.
note: Never the mean: Google, AWS (a vendor), Microsoft (a vendor). Prometheus warns only against averaging quantiles; OpenTelemetry is a definition page
borrowed_from:
  - https://sre.google/sre-book/service-level-objectives/
  - https://sre.google/sre-book/monitoring-distributed-systems/
  - https://builder.aws.com/content/3EuxPBdIiiUhB5IK47p3O3fxhy7/instrumenting-distributed-systems-for-operational-visibility
  - https://prometheus.io/docs/practices/histograms/
  - https://opentelemetry.io/docs/specs/otel/metrics/api/
  - https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/monitoring
---

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

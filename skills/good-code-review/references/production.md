# production

## prod-a11y-audit-before-launch

severity: should-fix  
concerns: accessibility, usability  
applies_when: A new UI service or a major redesign is about to open to the public.  
context: ui  
tool gate: none; a launch checklist item that links the audit report.  
Backed by: GOV.UK (unjudged), W3C (unjudged), Section508.gov (unjudged), Deque (unjudged), Government of British Columbia (supports), US Department of Veterans Affairs (supports). Backing: mixed.

**Rule.** Before a public launch, run an accessibility audit against WCAG 2.2 AA that includes assistive technology, and link the report in the launch checklist.

**Why.** Quick checks and automated tools are a first pass, not an evaluation. A page can pass both and still block a screen-reader user from finishing the task. Finding that after launch means fixing it under load and in public. The audit is not a one-off: test again, with automated and manual checks, when features change.

**FAIL**

```text
Launch checklist
[x] Load test      [x] Rollback plan      [x] Monitoring
(no accessibility line)
```

**PASS**

```text
Launch checklist
[x] Accessibility audit vs WCAG 2.2 AA, with screen reader, magnifier, and voice input.
    Report: docs/audit-2026-10.pdf. Open issues: 2, both minor, owner and date set.
```

**Counterpoint.** "We have no budget for an external audit." The auditor can be in-house, if they are trained and did not build the service. Cut scope instead of the audit: audit the main task flows first, and say in the report which parts are not covered.

## prod-alert-actionable-context

severity: should-fix  
concerns: observability  
applies_when: A service ships alert rules that page a person.  
tool gate: A lint on alert rules that requires a description and a runbook annotation.  
Backed by: Google (unjudged), Microsoft (unjudged), AWS (unjudged), Datadog (unjudged). Backing: unjudged.

**Rule.** Give every paging alert context a responder can act on: what it means and what to do next.

**Why.** A page that says only "metric X is high" makes the responder start from nothing at 3 a.m. The usual form is a one-line description, the owning team and a link to a runbook for the first checks and the mitigation. Written-down steps shorten recovery time, and an alert with an owner cannot be ignored by default. Alerts that need no immediate action belong in a ticket queue, not a page ([prod-alerts-symptoms-golden-signals](production.md#prod-alerts-symptoms-golden-signals)).

**FAIL**

```yaml
- alert: HighErrorRatio
  expr: job:http_errors:ratio5m > 0.05
  for: 5m
  labels: {severity: page}
```

**PASS**

```yaml
- alert: HighErrorRatio
  expr: job:http_errors:ratio5m > 0.05
  for: 5m
  labels: {severity: page, team: payments}
  annotations:
    summary: "More than 5% of checkout requests fail"
    runbook_url: https://wiki.example.com/runbooks/checkout-errors
```

**Counterpoint.** "Runbooks go stale and nobody reads them." A stale runbook is a fixable defect, and the card asks only that the alert say what it means and where to start. Ticket-only and informational alerts need no runbook, so the rule covers rules that page.

## prod-alerts-symptoms-golden-signals

severity: should-fix  
concerns: observability  
applies_when: A service ships alerts or dashboards.  
Backed by: Google (unjudged), Prometheus (unjudged), Grafana Labs (unjudged), Datadog (unjudged). Backing: unjudged.

**Rule.** Page on user-visible symptoms, such as error rate and latency, not on causes.

**Why.** Cause-based pages (CPU high) wake people without user impact. A mean hides the slow tail, and failed-request latency mixed with successes hides both. Require an error-rate alert to hold for a few minutes, so one blip does not page. Also cover latency, traffic, errors, and saturation, and page on saturation when a limit is about to be reached, not only after it is hit. Track latency as a distribution, and delete alerts that never fire.

**FAIL**

```text
alert: cpu > 80%  -> page
dashboard: avg latency only
```

**PASS**

```text
alert: error ratio > X, for 5m -> page
latency p50/p99 histogram, errors split from successes
```

**Counterpoint.** Cause alerts help diagnosis. Keep them as tickets or dashboard hints, not pages. The Honeycomb wide-event camp argues against pre-set metrics, while the SRE book favors simple metric-based paging, so this card does not ban events, only cause-paging.

## prod-canary-staged-rollout

severity: block  
concerns: reliability  
applies_when: A change, config or dependency update is rolled out to production.  
tool gate: Deploy pipeline with canary stage and automatic abort.  
Backed by: Google (unjudged), AWS (unjudged), OWASP (unjudged), Anthropic (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Roll out in stages behind a canary, and abort by rule, not by judgment.

**Why.** A 100% push exposes everyone to the bug. A canary must be large and long enough to be representative. Errors of 20% on 5% of traffic are only 1% overall, so tie the canary to your error budget. A feature flag does the same job inside one release: switch the change on for a small share of users, watch, then widen.

**FAIL**

```text
deploy: all hosts at once, no comparison, rollback = "ask someone"
```

**PASS**

```text
# compare the canary to a control on a few chosen metrics
5% canary 30m -> compare error rate, p99 -> auto-rollback if worse -> 25% -> 100%
```

**See also.** [inc-rollback-path-tested](incident.md#inc-rollback-path-tested) (drill the rollback).

**Counterpoint.** "Hotfixes can't wait." Then keep the canary short, not absent. Fleet tools should also have velocity limits. A hermetic, reproducible build tied to one revision ([code-build-hermetic](codebase.md#code-build-hermetic)) is the precondition for rollback to mean anything. [prod-config-ships-like-code](production.md#prod-config-ships-like-code) covers config and flag values.

## prod-config-ships-like-code

severity: should-fix  
concerns: reliability  
applies_when: A service has runtime configuration, feature-flag values or limits that can change in production.  
tool gate: Production config store writable only by the deploy pipeline; the config repository requires review before merge.  
Backed by: Google (unjudged), AWS (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Change configuration and flag values through a reviewed commit and the same staged, automated pipeline as code, not by hand on a host or console.

**Why.** One configuration value can change behaviour as much as a code change, with less testing and review. A hand edit leaves no history, no second reader and no rollback, and it skips the canary that would catch the mistake ([prod-canary-staged-rollout](production.md#prod-canary-staged-rollout)).

**FAIL**

```text
ssh prod-3 "sed -i 's/rate_limit: 100/rate_limit: 1000/' /etc/app/config.yaml"
```

**PASS**

```text
PR "raise rate_limit to 1000" -> reviewed -> merged -> config pipeline: 5% of hosts, health check, then the rest, auto-rollback on failure
```

**Counterpoint.** "In an incident we need to change a value now." An out-of-band change is allowed when the pipeline is too slow, as long as a commit records the same value straight after, so the repository stays the source of truth. A fast config pipeline makes the exception rare.

## prod-kill-switch-fallback

severity: should-fix  
concerns: reliability  
applies_when: A new risky feature or a dependency fallback is added.  
Backed by: AWS (unjudged), Cloudflare (unjudged), GitHub (unjudged), Slack (unjudged), Dropbox (unjudged), Shopify (unjudged), FeatBit (unjudged), GrowthBook (unjudged), Harness (unjudged), Anthropic (unjudged). Backing: unjudged.

**Rule.** Make a risky feature switchable off without a deploy, give each kill switch that stays an owner, and exercise every fallback path in test or in production on a schedule.

**Why.** A deploy is the slowest way to stop a feature that is hurting users. An untested fallback fails exactly when you need it: a fail-open path that never ran under load can overload the systems behind it, and a kill switch applied to a case it never met can raise its own error. Run the service with the dependency turned off, such as the cache disabled, and check that the safeguards hold.

**FAIL**

```python
if redis_down:
    return backup_lookup(key)   # never run since it was written
new_checkout(cart)              # no flag; turning it off needs a deploy
```

**PASS**

```python
if flags.enabled("checkout_v2"):   # runtime toggle, default off
    new_checkout(cart)
# chaos job, weekly: block Redis for 10 minutes and assert backup_lookup serves
```

**Counterpoint.** "Flags add branches." True for release flags, so delete each one after the rollout. A kill switch is meant to stay: keep it, and exercise it with the fallbacks, so it still works the day you need it. For runbook steps that a person runs, such as a rollback or a failover, see [inc-rollback-path-tested](incident.md#inc-rollback-path-tested).

## prod-latency-slo-percentile

severity: should-fix  
concerns: performance, observability  
applies_when: A latency SLO, dashboard, or alert is defined for a service.  
tool gate: Lint alert rules for avg() over latency or over pre-computed quantiles.  
Backed by: Google (unjudged), AWS (unjudged), Prometheus (unjudged), OpenTelemetry (unjudged), Microsoft (unjudged). Backing: unjudged.

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
tool gate: Load-test job with thresholds (k6, Gatling) in the release pipeline.  
Backed by: Google (unjudged), Microsoft (unjudged), AWS (unjudged), Grafana Labs (unjudged). Backing: unjudged.

**Rule.** Load test before launch, past the expected peak, with pass and fail thresholds written down.

**Why.** Overload behaviour is hard to predict from code, and launch traffic often beats the estimate. Test the whole workload on production-like infrastructure: testing one component, on smaller machines, or only up to the expected load misses the queue that fills first. Run the test as a pipeline step too, so a later change cannot slip under the thresholds.

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

**Counterpoint.** "A production-sized test environment costs too much." Size the test to the risk. A scaled-down environment is acceptable for a non-critical workload, and skipping the test is low risk for a small one. For a launch that could take down a shared dependency, the test is cheaper than the outage. Roll out in stages either way ([prod-canary-staged-rollout](production.md#prod-canary-staged-rollout)).

## prod-metric-labels-bounded

severity: should-fix  
concerns: observability, performance  
applies_when: A service records aggregated metrics (counters, histograms, gauges) with labels or dimensions.  
tool gate: A cardinality limit on the metrics backend; a lint that rejects labels named user_id, request_id or raw path.  
Backed by: Prometheus (unjudged), Microsoft (unjudged), Micrometer (unjudged). Backing: unjudged.

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

## prod-profile-on-demand

severity: discuss  
concerns: performance, observability  
applies_when: A service runs in production where CPU, memory, or latency problems would need a diagnosis.  
Backed by: Google (unjudged), Grafana Labs (unjudged), Python Software Foundation (unjudged). Backing: unjudged. People cited: Brendan Gregg (unjudged).

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

## prod-shadow-compare-before-cutover

severity: should-fix  
concerns: correctness, reliability  
applies_when: Reads, writes, or a pipeline's traffic move from an old system to a new one, such as a new data store, a database upgrade, or a rewritten service.  
context: data  
Backed by: Netflix (unjudged), Stripe (unjudged), Airbnb (unjudged), GitHub (unjudged), American Express (supports), Microsoft (supports), Shopify (supports). Backing: strong.

**Rule.** Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.

**Why.** Fixtures cover the cases someone thought of, and production holds the rest. Airbnb's replay of real queries against MySQL 5.7 and 8.0 found queries whose row order was never fixed, and an application that sent the same cacheable query over and over. Neither shows up in a test suite. A diff on real traffic finds these while the old system still answers users, so a mismatch costs a log line instead of an incident. Then shift traffic in steps with a way back; see [prod-canary-staged-rollout](production.md#prod-canary-staged-rollout) and [prod-kill-switch-fallback](production.md#prod-kill-switch-fallback).

**FAIL**

```python
def get_order(order_id):
    return new_store.get(order_id)    # cut over in one step; never compared on real reads
```

**PASS**

```python
def get_order(order_id):
    old = old_store.get(order_id)     # users still get the old answer
    try:
        if new_store.get(order_id) != old:
            shadow_mismatch.inc()
            log.info("shadow mismatch", extra={"order_id": order_id})
    except Exception:
        shadow_error.inc()
    return old
# once shadow_mismatch is zero or every mismatch is explained, the cutover flag shifts traffic in steps;
# setting it back to 0% returns every read to the old store
```

**Counterpoint.** "Running both is slow and doubles the load." It is slower than a flag-day switch, and Netflix says that is the reason it trusts the result. Keep the cost down: shadow a sample, call the new system off the request path, and never shadow a call with side effects such as a charge or an email. For writes, compare data snapshots after replication, as Stripe does, instead of sending each write twice. A refactor inside one process needs a characterization test, not production traffic. See [chg-refactor-has-behaviour-pin](change.md#chg-refactor-has-behaviour-pin).

## prod-slo-error-budget

severity: discuss  
concerns: reliability, observability  
applies_when: A service has users or dependents who rely on its availability.  
Backed by: Google (supports), GitLab (supports), Atlassian (supports). Backing: strong.

**Rule.** Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

**Why.** Without a stated target, nobody can say whether reliability work or a freeze is warranted, and every incident is argued from feelings.

**FAIL**

```text
"we aim for high availability" ; no SLI, alerts at arbitrary thresholds
```

**PASS**

```text
SLO: 99.9% of requests succeed in 300ms over 30d ; budget burn alert; freeze at 0
```

**Counterpoint.** "SLOs are bureaucracy for small teams." A one-line target is enough. Skip it for internal tools with no users.

# Clusters: production + incident

Counts: READY 0, NEAR 1, ONE 10 listed. Dropped groups at the end.

## prod-sampling-profiler | orgs: 2 | status: NEAR
Rule: Profile production with a sampling profiler, not an instrumenting or deterministic one.
Concern tags: performance, reliability
Severity guess: discuss
Rows: 1367, 1376
Orgs: psf, grafana
Conflicts/duplicates: none (prod-profile-on-demand says a profile must be obtainable; it does not say which kind)
Notes: PSF frames it as sampling over deterministic; Grafana as minimal overhead. Needs one more org, then fold into prod-profile-on-demand as a clause.

## prod-limit-shadow-mode | orgs: 1 | status: ONE
Rule: Run a new rate limit in shadow mode (measured, not enforced) before turning enforcement on.
Concern tags: reliability, process
Severity guess: should-fix
Rows: 2021, 2470
Orgs: uber
Conflicts/duplicates: none; adjacent to prod-shadow-compare-before-cutover (that card is about a new system, not a limit)
Notes: both rows are the same Uber page set.

## prod-canary-few-metrics-one-at-a-time | orgs: 1 | status: ONE
Rule: Evaluate a canary on a short list of user-problem metrics (about a dozen at most) and run one canary at a time.
Concern tags: reliability, process
Severity guess: discuss
Rows: 196, 197
Orgs: google
Conflicts/duplicates: none (prod-canary-staged-rollout states staging and abort rules only)
Notes: two clauses, each Google only.

## prod-alert-names-threshold-impact | orgs: 1 | status: ONE
Rule: Each alert names the threshold in sustained breach, its impact and the affected components.
Concern tags: observability
Severity guess: discuss
Rows: 1382
Orgs: microsoft
Conflicts/duplicates: none
Notes: single source.

## prod-page-actionable | orgs: 1 | status: ONE
Rule: Every page is actionable; a page that needs only a robotic response is automated, not paged.
Concern tags: observability, process
Severity guess: discuss
Rows: 1396
Orgs: google
Conflicts/duplicates: partial overlap with prod-alerts-symptoms-golden-signals (symptoms, not actionability); keep separate
Notes: single source.

## prod-monitoring-self-alert | orgs: 1 | status: ONE
Rule: Alert when the monitoring stack itself (collector, alert router, pushgateway) is down or not working.
Concern tags: observability, reliability
Severity guess: should-fix
Rows: 1387
Orgs: prometheus
Conflicts/duplicates: none
Notes: Slack row 1132 (alert when a scheduled backup fails or stops) is the same shape for backups; could join as a "silent-failure jobs have a liveness alert" clause with slack, reaching 2 orgs.

## inc-backup-failure-alert | orgs: 1 | status: ONE
Rule: Alert when a scheduled backup fails or stops running.
Concern tags: reliability, observability
Severity guess: should-fix
Rows: 1132
Orgs: slack
Conflicts/duplicates: none
Notes: see prod-monitoring-self-alert; merge candidate for a 2-org liveness clause.

## prod-slo-budget-burn-postmortem | orgs: 1 | status: ONE
Rule: An incident that burns over 20 percent of the quarterly error budget requires a postmortem with a P0 action item.
Concern tags: process, reliability
Severity guess: discuss
Rows: 1404, 1405
Orgs: google
Conflicts/duplicates: none; adjacent to inc-review-asks-which-check and prod-slo-error-budget
Notes: the 20 percent number is Google-specific.

## inc-mitigate-before-root-cause | orgs: 1 | status: ONE
Rule: Mitigate user impact first (divert, shed, disable), and root-cause afterwards.
Concern tags: reliability, process
Severity guess: discuss
Rows: 1136
Orgs: google
Conflicts/duplicates: none
Notes: single source; hard to mark FAIL from a diff, may fail rule 4.

## prod-latency-excludes-fast-failures | orgs: 1 | status: ONE
Rule: Keep fast-failed requests out of the latency metric for successful requests.
Concern tags: observability, correctness
Severity guess: should-fix
Rows: 2064
Orgs: aws
Conflicts/duplicates: refines prod-latency-slo-percentile, no contradiction
Notes: single source.

## prod-failure-domain-whole-facility-test | orgs: 1 | status: ONE
Rule: Test failure domains by taking a whole facility offline, not only individual parts.
Concern tags: reliability, testing
Severity guess: discuss
Rows: 2057
Orgs: cloudflare
Conflicts/duplicates: overlaps inc-rollback-path-tested and prod-kill-switch-fallback (exercise on a schedule); only the "whole facility" clause is new
Notes: Shopify 1150 (game-day scenario written as a hypothesis) is a sibling clause, 1 org.

## CONFLICT candidates (no card proposed)
- Row 1359 (airbnb): "Captured production traffic is never replayed in lower environments." CONFLICT with prod-shadow-compare-before-cutover, which allows running a new system on captured production traffic. Likely resolves if the card says where the replay runs; left for the maintainer.

## Dropped
- Duplicate of a card: 1140 (USE per resource) -> inc-perf-fix-has-profile-evidence; 861, 416 (profile/benchmark evidence) -> same; 1365, 1149 (rollback, failover rerunnable) -> inc-rollback-path-tested; 166, 1422, 2578 (gradual rollout) -> prod-canary-staged-rollout; 1139 (postmortem review) -> weak, one org, no checkable evidence.
- Linter or library API only: 1384 (OpenTelemetry callbacks), 1389, 1390 (PromQL query form), 1361 (stop scheduling replay on failures, tooling-specific).
- Advice or not checkable at level: 1142 (look at short-interval peaks), 1352 (review failure modes), 1416 (dynamic dashboards), 1374 (load shape), 1402 (few SLOs), 1399 (spare capacity), 1412 (log every alert), 1381 (separate prod and nonprod telemetry), 1817, 1820, 1150, 219, 179 (accessibility statement; one org, a process not a code check).

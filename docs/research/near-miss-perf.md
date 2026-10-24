# Near-miss sources, perf lane: third orgs for four performance cards

Fetched 2026-10-24 through WebFetch (a small model summarises the page), so every row is paraphrase. Each row gives the URL, what it says, and the card whose Rule it backs. Pages from one org count once. A source counts only if it backs the Rule line, not just the Why. Cards keep their status, Rules, and severities; the stable pass decides promotion.

## 1. svc-timeouts (deadline half)

1. https://learn.microsoft.com/en-us/aspnet/core/grpc/deadlines-cancellation (Microsoft, ASP.NET Core). Without a deadline a gRPC call has no time limit. A service that calls another service should pass the deadline it received to the child call, so the second hop times out when the original caller's deadline passes. When both a propagated and a local deadline exist, the smaller one wins. A retry loop shares one deadline across all attempts. Backs `svc-timeouts`, both halves, including the "retries inside a 1 s deadline" FAIL line. Strong primary.

Count for the deadline half: 2 before (Google via gRPC and SRE, AWS) -> 3 after (+ Microsoft). Microsoft's Azure retry-pattern page already in `borrowed_from` backs only bounded retries, so this ASP.NET page is the first Microsoft source for propagation.

Near misses, not cited: https://twitter.github.io/finagle/guide/Contexts.html (Finagle names a broadcast Deadline context but does not say timeouts use it) and https://twitter.github.io/finagle/guide/Clients.html (per-module timeouts, no deadline propagation). https://www.envoyproxy.io/docs/envoy/latest/configuration/http/http_filters/router_filter sets `x-envoy-expected-rq-timeout-ms` from the configured route timeout, not from a remaining budget, so it does not back derivation. https://pkg.go.dev/context is Google, already counted.

## 2. chg-new-query-has-plan

2. https://docs.gitlab.com/development/database_review/ (GitLab). A merge request with raw SQL needs the query plan, linked after each snippet, taken from a production-sized clone (Database Lab) or a seeded environment with `EXPLAIN ANALYZE`. A plan must not return zero rows or fewer than the limit. For a changed query, give the plan before and after. The page says clone timings differ from production, so treat a slow plan as a hint. Backs the Rule, both "attach" and "production-sized data". Strong primary.
3. https://aws.amazon.com/blogs/database/how-postgresql-processes-queries-and-how-to-analyze-them/ (AWS). Run `EXPLAIN` before deploying a new query to estimate its cost, and check performance before and after a change, since a plan is an assumption until measured. Backs "get the plan before it ships". Does not say to attach it to the change.
4. https://www.postgresql.org/docs/current/using-explain.html (PostgreSQL, already cited). Re-read for the Counterpoint: a plan on a toy-sized table cannot be assumed to hold for a large one, and a one-page table nearly always gets a sequential scan. This supports the "production-sized" clause of the Rule and the Counterpoint.

Count: 3 orgs back "show the plan" (PostgreSQL, Oracle MySQL, SQLite) and now AWS and GitLab join them. "Attach the plan to the change" has 1 org (GitLab). "On production-sized data" has 2 (GitLab, PostgreSQL). The card's own `note:` says attaching is its own practice; that is still true. Finding: the Rule's attach clause rests on one org, so a strict stable pass should move "attach" to Why or keep the card as a draft.

Near misses, not cited: https://docs.aws.amazon.com/prescriptive-guidance/latest/postgresql-query-tuning/explain-query-plan.html (explains plans; does not say to run one before deploying) and https://docs.gitlab.com/development/database/understanding_explain_plans/ (GitLab again; recommends production-like data, never mentions merge requests).

## 3. inc-perf-fix-has-profile-evidence

5. https://docs.gitlab.com/development/performance/ (GitLab). The workflow is to measure the code in production for at least 24 hours, record graphs and timings in the issue, then fix, then measure again for at least 24 hours after deploy. The page warns against claims from benchmarks alone and names profiling and tracing as the tools for seeing where time goes. Backs both halves of the Rule (evidence before, same measurement after). It says "measure", not "profile" strictly, and puts the numbers in the issue, not the postmortem.
6. https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/optimize-code-infrastructure (Microsoft). Instrument the code, find hot paths with profiling or performance-test tools, and do not hide a code problem by adding capacity. Backs the "name the bottleneck first" half. The only before-and-after measurement advice on the page is about compression, so it does not back the "same measurement after" half.

Count: the "evidence before the fix" half had 2 orgs (Google, Brendan Gregg) and now has 4 (+ GitLab, + Microsoft). The "same measurement after the fix" half has 2 firm orgs (Google's Go blog, GitLab), so it is the weaker half. The `note:` in the card's front matter says it cannot be promoted yet; that is the coordinator's call.

Near misses, not cited: https://docs.python.org/3/library/profile.html (what a profiler shows, never says to profile before optimising), https://nnethercote.github.io/perf-book/profiling.html (says to profile to find hot code; says nothing about measuring the change), https://developer.chrome.com/docs/devtools/performance (a tutorial; Google again).

## 4. inc-perf-regression-guard

None found for a third org on the postmortem-action pairing. The card already lists Google (SRE postmortems, web.dev), Microsoft, AWS, Mozilla, and Cloudflare, so "an automated check or threshold catches performance regressions" has 5 orgs. What has 2 orgs is "make that check a postmortem action": Google SRE (postmortem actions that prevent recurrence) and Cloudflare (post-outage CPU guard and per-rule profiling test). The AWS S3 2017 summary (https://aws.amazon.com/message/41926/) lists capacity guardrails as remediation but is not a performance regression. The Stack Overflow 2016 regex postmortem returned 403 and was not read. The Rust project's perf site (https://perf.rust-lang.org/compare.html) is only a comparison page, and the forge triage page returned 404, so Rust is not cited. Chromium's regression doc (raw GitHub text of docs/speed/addressing_performance_regressions.md) says a regressing change must be fixed or reverted, found by a bisect bot, but Chromium is Google, so it adds no org.

Finding: the Rule reads as one rule, but it is two claims. The CI-guard claim has 5 orgs; the "as a postmortem action" claim has 2. Consider keeping the guard in the Rule and the postmortem placement in Why.

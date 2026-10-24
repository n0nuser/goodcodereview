---
id: code-perf-budget-in-ci
level: codebase
tags: [performance, process, ci]
severity: should-fix
status: stable
lang: core
applies_when: The repo has a performance target (bundle size, page metrics, latency under load, or a benchmark) that matters to users.
tool_gate: Lighthouse CI assert, size-limit, k6 thresholds, Gatling assertions, or a benchstat comparison in CI.
borrowed_from:
  - https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md
  - https://github.com/ai/size-limit
  - https://grafana.com/docs/k6/latest/using-k6/thresholds/
  - https://docs.gatling.io/concepts/assertions/
  - https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/performance-test
  - https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_process_culture_load_test.html
  - https://firefox-source-docs.mozilla.org/testing/perfdocs/perf-sheriffing.html
  - https://pkg.go.dev/golang.org/x/perf/cmd/benchstat
---

**Rule.** Write the performance budget down as a CI check that fails the build when it is exceeded.

**Why.** Performance regresses a few percent at a time, and no reviewer sees a 3% slowdown in a diff. A budget that only warns becomes a log line nobody reads.

**FAIL**

```text
lighthouserc.json: "assertions": { "categories:performance": ["warn", { "minScore": 0.9 }] }
k6 script with no thresholds block
```

**PASS**

```text
size-limit: [{ "path": "dist/app.js", "limit": "180 kB" }]   # npm run size in CI
k6: thresholds: { http_req_duration: ["p(95)<300"] }        # non-zero exit fails the job
```

**Counterpoint.** "Benchmarks in CI are noisy and flake." They are when a gate trusts one run. Gate on a stable budget, compare repeated runs (benchstat wants 10 to 20), and keep the threshold above the noise. On a site with much room to improve, a tight budget only turns every build red, so set it at today's level and lower it later.

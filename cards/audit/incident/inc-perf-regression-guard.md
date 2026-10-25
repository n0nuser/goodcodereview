---
id: inc-perf-regression-guard
level: incident
tags: [performance, testing]
severity: should-fix
status: draft
lacks: duplicate, the guard half is the stable code-perf-budget-in-ci Rule; the postmortem-action half has Google SRE and Cloudflare only
lang: core
applies_when: A postmortem covers a performance regression or a resource-exhaustion incident.
tool_gate: none
note: draft after stable pass 5 - "an automated check catches performance regressions" has 5 orgs but is stable code-perf-budget-in-ci's Rule; "make it a postmortem action" has 2 (Google SRE, Cloudflare); splitting leaves a duplicate plus a 2-org half
borrowed_from:
  - https://sre.google/sre-book/postmortem-culture/
  - https://web.dev/articles/lighthouse-ci
  - https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/performance-test
  - https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_process_culture_load_test.html
  - https://firefox-source-docs.mozilla.org/testing/perfdocs/perf-sheriffing.html
  - https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/
---

**Rule.** Add an automated check that would have caught the regression (a benchmark, a budget, a load-test threshold, or a resource guard) as one of the postmortem's actions.

**Why.** A fix without a guard leaves the next change free to bring the regression back, and performance regressions arrive silently. The guard turns what the incident taught into a check that runs on every change.

**FAIL**

```text
action items: "be careful with regex in WAF rules"; "review perf more closely"
```

**PASS**

```text
action: CI benchmark per WAF rule, fails above 1 ms per request (owner: WAF team, due 2026-11-15)
action: CPU guard aborts a rule over its budget in production
```

**Counterpoint.** "Some regressions can't be reproduced in a test." Then guard the symptom in production: an alert on the resource, or a limit that stops runaway work. A "be careful" action is not a guard. [[inc-postmortem-owned-actions]] asks for an owner on every action, and this card says what a performance action looks like.

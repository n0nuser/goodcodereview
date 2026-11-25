# Leads: process and testing (rollout, on-call, postmortems, test strategy)

Method: each page fetched with `curl -sL --compressed` and tags stripped with `python3 -I`; the sentence found by regex in the stripped text (about 70 fetches, 2026-11-24). Quotes are 10 words or fewer; the rest is paraphrase. Org grouping follows docs/PROMOTION.md (Google covers sre.google, SWE at Google and Google testing; Microsoft covers Learn, Azure WAF and the code-with-engineering playbook; AWS covers Well-Architected). Blogspot pages (Google Testing Blog) return only comments in raw text, so they were not used. Existing-card check: `rg` over `cards/` first. Already covered, so not proposed: canary and abort (`prod-canary-staged-rollout`), rollback drilled (`inc-rollback-path-tested`), rollback stated in PR (`chg-rollback-path`), postmortem actions owned (`inc-postmortem-owned-actions`), flaky quarantine (`code-flaky-test-quarantine`), tests with change (`chg-tests-ship-with-change`), test selection, order independence, fixtures, suite time budget, contract tests, symptom alerts (`prod-alerts-symptoms-golden-signals`), SLO budget, kill switch, flag retirement.

## Ranking

| # | Lead | Orgs | Verdict |
|---|---|---|---|
| 1 | Postmortem is blameless: no individual named as the cause | 4 (Google, PagerDuty, Atlassian, Microsoft) | clears 3, new card |
| 2 | Every paging alert links a runbook or playbook entry | 3 (Google, Prometheus, Grafana) | clears 3, new card |
| 3 | Unit tests do not sleep or touch real I/O | 3 firm (Google, Microsoft, Cypress) + Selenium and GitLab soft | clears 3, new card |
| 4 | Test suite is shaped as a pyramid: most unit, few end-to-end | 3 (Google, GitLab, Microsoft) | clears 3, new card, audit level |
| 5 | A named incident commander runs each major incident | 3 firm (Google, PagerDuty, AWS) + Atlassian soft | clears 3, runbook-checkable only |
| 6 | A bug fix ships a regression test that fails before the fix | 2 (Rust, Django) | short, clause on `chg-tests-ship-with-change` |
| 7 | Mitigate first (rollback, reroute), find the root cause after | 1 (Google); Microsoft partial | short |
| 8 | Postmortem has defined triggers | 1 (Google) | short |
| 9 | Coverage is a signal, not a target | 1 (Google) | short |
| 10 | No production data in test environments | 0 found | short, no usable source fetched |

## 1. Postmortem is blameless

Rule candidate: "A postmortem names causes in the system and the decisions around it, not an individual or team as at fault." A reviewer greps the postmortem document in the repo or wiki for a named person as "root cause" or words like "careless". Nearest card: `inc-postmortem-owned-actions` (actions, not tone). New card, id `inc-postmortem-blameless`.

1. https://sre.google/sre-book/postmortem-culture/ . Google. "without indicting any individual or team for bad or inappropriate behavior". Found: "Blameless postmortems are a tenet of SRE culture".
2. https://postmortems.pagerduty.com/culture/blameless/ . PagerDuty. Blame and punishment make engineers hesitate to speak up; the postmortem should find systemic factors. Found: "Engineers will hesitate to speak up when incidents occur for fear of being blamed."
3. https://www.atlassian.com/incident-management/postmortem/blameless . Atlassian. Everyone is assumed to have acted with good intentions on what they knew. Found: "it's assumed that every team and employee acted with the best intentions".
4. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/incident-response . Microsoft (Azure WAF). Run a blameless postmortem led by an impartial facilitator. Found: "blameless postmortem led by an impartial facilitator".

Scope caveat: applies to written postmortems and review meetings; says nothing about performance management. Counterpoint: blamelessness can dodge accountability; Atlassian answers that it still names who made which change, as part of the timeline, and assigns approval to a senior owner. Card should not forbid names in the timeline, only as the cause.

Google's own workbook example (https://sre.google/workbook/postmortem-culture/) is a labelled bad example that blames a named person; use it as the FAIL.

## 2. Every paging alert links a runbook or playbook entry

Rule candidate: "Each alert rule carries a link to a runbook, dashboard or playbook entry that says what to check and do." Checkable in alert rule files (annotation `runbook_url` or equivalent). Nearest card: `prod-alerts-symptoms-golden-signals` (what to page on, not what the page links); `inc-rollback-path-tested` mentions runbooks but not alert links. New card, id `prod-alert-links-runbook`.

1. https://sre.google/workbook/on-call/ . Google. "Each alert should have a corresponding playbook entry." Found: the paragraph on reviewing new alerts. Also: playbooks explain severity, impact, debugging and mitigation.
2. https://prometheus.io/docs/practices/alerting/ . Prometheus (CNCF). "Alerts should link to relevant consoles". Found: the bullet list under "Alerting".
3. https://grafana.com/docs/grafana/latest/alerting/guides/best-practices/ . Grafana. Use annotations to link to relevant dashboards and runbooks, which are essential for faster resolution. Found: the sentence on annotations. The same page says every alert should be actionable.

Not found: Datadog monitor best-practices page (talks about actionable monitors but no runbook sentence in raw text); AWS OPS07-BP03 describes runbooks as documented procedures but does not tie them to alerts. Counterpoint: stale runbooks are worse than none; Google's own text has a "Maintaining Playbooks" section. Pair the card with a freshness note, or accept that stale links are caught by `inc-rollback-path-tested` drills.

## 3. Unit tests do not sleep or touch real I/O

Rule candidate: "A unit test does not call sleep or wait on a fixed delay, and does not reach the network, a database or the file system." Greppable in the test directory (`sleep(`, `time.Sleep`, `cy.wait(<number>)`). Nearest cards: `code-tests-order-independent`, `code-flaky-test-quarantine` (handle flakes after the fact), `mod-mock-at-boundaries-only` (what to mock, not that unit tests must be I/O-free). New card, id `code-unit-tests-no-sleep-no-io`. The sleep half and the I/O half could be split.

1. https://abseil.io/resources/swe-book/html/ch11.html . Google (SWE at Google). Small tests "aren't allowed to sleep, perform I/O operations" or make other blocking calls. Found: the "small tests" constraints paragraph.
2. https://microsoft.github.io/code-with-engineering-playbook/automated-testing/unit-testing/ . Microsoft. Under "Things to Avoid": a sleep can mean the code calls a dependency it should not; sleeps also slow the suite. Found: "Sleeps - A sleep can be an indicator".
3. https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices . Microsoft (same org as 2). Unit tests "have no dependencies on any outside factors", such as a file system or database. Found: "Isolated".
4. https://docs.cypress.io/app/core-concepts/best-practices . Cypress (vendor, tool docs). "you almost never need to use cy.wait()" with an arbitrary number. Found: the arbitrary-wait anti-pattern; it adds that a lint rule can catch `cy.wait(<number>)`.
5. https://www.selenium.dev/documentation/webdriver/waits/ . Selenium (soft). Says a sleep is the first fix many reach for and "can fail when it doesn't sleep long enough". Descriptive, not a rule; use explicit waits instead.
6. https://docs.gitlab.com/development/testing_guide/testing_levels/ . GitLab (soft, I/O half only). Frontend unit tests assume an unreachable backend, so outgoing requests are mocked. Descriptive.

Count: Google, Microsoft, Cypress firm for the sleep half; Google, Microsoft firm for the I/O half (GitLab soft). Scope caveat: end-to-end and integration tests legitimately use real I/O and may poll; the rule is for tests in the small tier. Counterpoint: a sleep-free test of time-based logic needs an injected clock; `mod-inject-boundary-collaborators` covers that. Not found: Kubernetes flaky-test guide uses `time.Sleep` only as a way to provoke races, not a rule.

## 4. Test suite is shaped as a pyramid

Rule candidate: "Most tests are fast unit tests, fewer are integration, fewest are end-to-end." Audit-level: a reviewer counts tests per tier from the repo layout or CI report. Nearest card: `code-test-suite-time-budget` (time) and `code-test-selection-on-pr`; none states the shape. New card, id `code-test-pyramid-shape`, level codebase, `severity: discuss`.

1. https://abseil.io/resources/swe-book/html/ch11.html . Google. A rough mix of 80% unit, 15% integration, 5% end-to-end, drawn as a pyramid. Found: "around 80% of our tests being narrow-scoped unit tests". A guideline, "very rough".
2. https://docs.gitlab.com/development/testing_guide/testing_levels/ . GitLab. "Most of our tests should be at the unit level". Found: the opening of the testing pyramid section. End-to-end tests are the most expensive to run and maintain.
3. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/testing . Microsoft (Azure WAF). Heading "Use the test pyramid as a guide": unit base, integration middle, slower layers above. Found: that heading.

Not found: Atlassian types-of-testing page says end-to-end tests are expensive and hard to maintain but never draws the pyramid; Thoughtworks and AWS prescriptive pages did not load usable text. Counterpoint: some stacks (UI-heavy apps, thin services over a database) get more value from integration tests; Google's text says the mix is not fixed. Hard to FAIL on a diff; fits only as an audit card with a ratio the reviewer can compute.

## 5. A named incident commander runs each major incident

Rule candidate: "A runbook or incident policy names one incident commander (or manager) role per major incident, with the other roles reporting to it." Checkable only in a process document. Nearest card: `inc-rollback-path-tested` ("naming who may trigger"). New card, id `inc-single-incident-commander`, likely `discuss`.

1. https://sre.google/sre-book/managing-incidents/ . Google. "The incident commander holds the high-level state about the incident." Found: the roles list; the Ops lead is the only group changing the system.
2. https://response.pagerduty.com/before/different_roles/ . PagerDuty. The commander is "the single source of truth" during a major incident, and some roles have only one person per incident. Found: Incident Commander entry.
3. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_event_response_push_notify.html . AWS (OPS10-BP05). "Assign a major incident manager to oversee incident response activities". Found: implementation steps, "Define roles and responsibilities".
4. https://www.atlassian.com/incident-management/handbook/incident-response . Atlassian (soft). An incident manager follows a set sequence from detection to resolution. Descriptive of its own process.

Scope caveat: a team of three does not need a role hierarchy. Counterpoint: the role split adds overhead for small incidents; Google and PagerDuty both scope it to major incidents.

## 6. Bug fix ships a regression test (short, 2 orgs)

Rule candidate: "A bug fix includes a test that fails before the fix." Nearest card: `chg-tests-ship-with-change` already says to ship a test that fails if the behaviour breaks; this narrows it to bug fixes. Clause, not a card.

1. https://rustc-dev-guide.rust-lang.org/tests/adding.html . Rust. "we expect every PR that fixes a bug" to carry a regression test. Found: opening of "Adding new tests".
2. https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/ . Django. A patch checklist asks for a proper regression test that fails before the fix. Found: "Is there a proper regression test".

Tried and did not give a usable sentence in raw text: Python devguide pull-request lifecycle (says bug fixes need an issue first, nothing on tests), Kubernetes PR guide, Mozilla testing policy page (JS shell), Chromium contributing page. A third org is likely findable (Mozilla, Chromium, Go) with a targeted fetch; add both URLs to `chg-tests-ship-with-change` `borrowed_from` meanwhile.

## 7. Mitigate first, find the root cause after (short)

Rule candidate: "An incident runbook puts mitigation (rollback, reroute, flag off) ahead of root-cause debugging." Nearest: `inc-rollback-path-tested`.

1. https://sre.google/workbook/incident-response/ . Google. Generic mitigations alleviate pain "even before the root cause is fully understood"; they "stop the bleeding" while the team looks for the cause. Found: the generic mitigations paragraph.
2. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/incident-response . Microsoft (partial). Procedures cover detection, containment and triage first, then root cause analysis. Found: "detection, containment, and triage".

Not found: PagerDuty incident commander training page and Atlassian incident response page: no sentence that orders mitigation before diagnosis. One org firm, one partial; short.

## 8 to 10. Short leads, nothing to build on

- Postmortem triggers (a defined list of when a postmortem is required): Google only ("common postmortem triggers include", with user-visible downtime above a threshold). No second org's sentence found in raw text.
- Coverage is a signal, not a target: Google only. SWE book says coverage is "often held up as the gold standard" and that this is unfortunate. The Google Testing Blog page is empty in raw text. Atlassian's coverage page is a tutorial with no rule.
- No production data in test environments: no source fetched. OWASP ASVS (v4.0.3 chapter 14 and v5 raw files), NIST SP 800-53 raw markdown, GOV.UK service manual and the NCSC page returned no usable sentence or 404. Azure WAF testing page says tests "often interact with production data", about risk, not a rule. Try PCI DSS 6.5.5 and NIST SA-3(2) from a PDF or OSCAL JSON in a later pass.
- On-call load cap (no more than 25% of time on call): Google only (https://sre.google/sre-book/being-on-call/). Not checkable from a diff.

## Notes for the parent

- Leads 3 and 4 are the most diff- or repo-checkable. Leads 1, 2 and 5 are checkable only if the repo holds postmortems, alert rules or an incident policy, so they sit at `incident` and `production` levels with `discuss` or `should-fix`.
- Feeds for existing cards (add to `borrowed_from`): Google workbook incident-response and Azure incident-response to `inc-rollback-path-tested`; Azure `testing` page to `code-test-suite-time-budget` is weak, skip; Rust and Django to `chg-tests-ship-with-change`.
- Cypress is a vendor's tool docs; the card should lean on Google and Microsoft and cite Cypress as a third.

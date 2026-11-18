# Source pilot: production level

Goal: find code-review rules in five source pages that the card set may not cover.
Method: WebFetch of each URL, up to three checkable rules per page, then `rg` over `cards/`, `packs/` and `docs/COVERAGE.md`, reading the nearest card in each case.

Caveat: WebFetch returns a summary written by a small model. The quoted sentences below are from that summary, not checked against the page text. Verify any quote before citing it in a card.

Marks: **covered** (card id), **partial** (card id and what is missing), **NEW** (nearest ids checked; a lead only, since a new card needs three independent orgs).

Totals: 15 rules. Covered 4, partial 5, NEW 6. Blocked: 0.

---

## 1. Slack Engineering: Slack AI, the path to multi-cloud

URL: https://slack.engineering/slack-ai-the-path-to-multi-cloud/
Fetch status: fetched, content present.

1. **Backup model per feature.** Quote: "we always designate backup models for every feature"
   - Coverage: **NEW**. Nearest: `prod-kill-switch-fallback` (fallback paths are exercised, but no card requires a designated alternate per feature). No card covers model or provider failover.
   - Other source needed: two more independent orgs that describe designated fallback providers or models.

2. **Circuit breaker partial-open recovery.** Quote: "the breaker enters a partial-open state, allowing a small, controlled trickle of requests"
   - Coverage: **partial**, `svc-circuit-breaker-bulkhead`. The card requires a breaker with limited half-open probing (one probe). It does not mention the trip signals on the page (TTFT, 5xx spike, p90 latency threshold).

3. **Normalize provider errors.** Quote: "'Rate Limit Exceeded' from one provider and a 'Throttling Exception' from another were handled identically"
   - Coverage: **NEW**. Nearest: `svc-retry-policy` (retry only transient errors). No card covers mapping vendor-specific error codes to one internal error type.
   - Other source needed: two more independent orgs with a vendor error-normalization writeup.

## 2. AWS Builder Center: Instrumenting distributed systems for operational visibility

URL: https://builder.aws.com/content/3EuxPBdIiiUhB5IK47p3O3fxhy7/instrumenting-distributed-systems-for-operational-visibility
Fetch status: fetched, content present. The page has about 18 rules; these are the three chosen.

1. **One request log entry per unit of work.** Quotes: "Emit one request log entry for every unit of work." and "Emit no more than one request log entry for a given request."
   - Coverage: **partial**, `prod-wide-events-bounded-labels` (status: draft). The card says "Emit one structured event per request". It does not require pipeline stages to share one metrics object, and it is still a draft.

2. **Sanitize input before logging.** Quote: "we make sure to sanitize input (encode, escape, and truncate) before we log it."
   - Coverage: **partial**, `fn-header-value-encoding`. The card rejects or encodes CR and LF in request-derived header values. It does not cover log-write escaping or truncation.

3. **Emit zero counts for availability metrics.** Quote: "Emit zero counts for availability metrics."
   - Coverage: **NEW**. Nearest: `svc-tenant-id-in-telemetry` (verified tenant id on telemetry). No card covers zero-versus-absent metric emission.
   - Other source needed: two more independent orgs on metric emission for availability or error counters.

## 3. Grafana docs: Alerting best practices

URL: https://grafana.com/docs/grafana/latest/alerting/guides/best-practices/
Fetch status: fetched, content present.

1. **Every alert has an owner and a scope.** Quote: "Every alert must have an owner: a team responsible for maintaining the alert and responding when it fires."
   - Coverage: **NEW**. Nearest: `inc-postmortem-owned-actions` (owner on postmortem actions) and `prod-kill-switch-fallback` (owner on kill switches). No card covers an owner label on alert rules. `prod-alerts-symptoms-golden-signals` does not mention owners.
   - Other source needed: two more independent orgs that require alert ownership.

2. **Require the condition to persist before alerting.** Quote: "Require issues to persist before alerting."
   - Coverage: **partial**, `prod-alerts-symptoms-golden-signals`. The card requires an error-rate alert to hold for a few minutes (`for: 5m`). It does not state the general rule for all alerts or the warning against instant-value thresholds (`cpu_usage > 90`).

3. **Avoid a separate alert rule per host, service, or endpoint.** Quote: "In distributed systems, avoid creating separate alert rules for every host, service, or endpoint."
   - Coverage: **NEW**. Nearest: `prod-alerts-symptoms-golden-signals` (page on symptoms, not causes) and `sys-health-liveness-readiness`. Neither covers duplicated per-host rules.
   - Other source needed: two more independent orgs on alert-rule duplication.

## 4. Microsoft Code With Engineering Playbook: Shadow testing

URL: https://microsoft.github.io/code-with-engineering-playbook/automated-testing/shadow-testing/
Fetch status: fetched, content present. The page is an architecture write-up with few code-level rules.

1. **No candidate response reaches users.** Quote: "we don't return any response from V-Next environment to users"
   - Coverage: **covered**, `prod-shadow-compare-before-cutover` (its PASS example keeps returning the old answer to users). This URL is already in the card's `borrowed_from`.

2. **Diff old and new outputs and report regressions.** Quote (Diffy, via the page): "It then compares the responses, and reports any regressions that may surface from those comparisons."
   - Coverage: **covered**, `prod-shadow-compare-before-cutover` (`shadow_mismatch` counter; cutover gated on zero unexplained mismatches).

3. **Candidate scales the same way as current.** Quote: "V-Next should scale with the same way V-Current does."
   - Coverage: **NEW**. Nearest: `prod-shadow-compare-before-cutover` (no scaling check) and `prod-canary-staged-rollout`. Neither covers capacity parity between old and new environments.
   - Other source needed: two more independent orgs that compare capacity between a shadow and a production environment.

## 5. VA Design System: Accessibility

URL: https://design.va.gov/accessibility/
Fetch status: fetched, content present. Mostly a test process; these rules are the checkable ones.

1. **WCAG 2.2 AA conformance.** Quote: "Today our compliance testing sets a minimal standard (WCAG 2.2 AA) that we are striving to raise."
   - Coverage: **partial**, `prod-a11y-audit-before-launch`. The card names WCAG 2.2 AA, but as a launch-gate audit, not a per-change conformance rule. The card already cites this URL.

2. **Automated axe scan of rendered pages.** Quote: "Conduct automated testing with axe DevTools by Deque"
   - Coverage: **covered**, `code-a11y-check-in-ci` (axe on rendered pages in automated tests, fail on violation).

3. **Real heading elements.** Quote (page lists heading levels as a manual check): "Heading levels"
   - Coverage: **covered**, `fn-heading-structure` (real `<h1>` to `<h6>`, not styled `div`, `span`, or `p`).

---

## Notes for the orchestrator

- Four NEW candidates (Slack backup models, Slack provider error normalization, AWS zero-count availability metrics, Grafana alert owner) each need two more independent orgs before any card is written. No card was created or edited.
- The Grafana per-host alert rule and the Microsoft capacity-parity rule are also NEW leads.
- Four of the five pages are already in cards' `borrowed_from` lists: Slack (`prod-kill-switch-fallback`), Microsoft (`prod-shadow-compare-before-cutover`), Grafana (`prod-alerts-symptoms-golden-signals`) and VA (`prod-a11y-audit-before-launch`). Only the AWS Builder Center page is not cited anywhere. Its rules are the source of most partial marks, so the page is worth a closer look.

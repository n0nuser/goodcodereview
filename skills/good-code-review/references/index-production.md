# Production audit index

One line per stable production card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `production.md`: read them with offset `<first>` and limit `<count>`.

- `prod-a11y-audit-before-launch` [should-fix] {accessibility, usability} <ui> L3+30: Before a public launch, run an accessibility audit against WCAG 2.2 AA that includes assistive technology, and link the report in the launch checklist.
- `prod-alerts-symptoms-golden-signals` [should-fix] {observability} L34+26: Page on user-visible symptoms, such as error rate and latency, not on causes.
- `prod-canary-staged-rollout` [block] {reliability} L61+28: Roll out in stages behind a canary, and abort by rule, not by judgment.
- `prod-kill-switch-fallback` [should-fix] {reliability} L90+28: Make a risky feature switchable off without a deploy, and exercise every fallback path in test or in production on a schedule.
- `prod-latency-slo-percentile` [should-fix] {performance, observability} L119+27: Define latency SLOs and alerts on high percentiles, never on the mean.
- `prod-load-test-before-launch` [should-fix] {performance, reliability} L147+27: Load test before launch, past the expected peak, with pass and fail thresholds written down.
- `prod-profile-on-demand` [discuss] {performance, observability} L175+26: Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.
- `prod-shadow-compare-before-cutover` [should-fix] {correctness, reliability} <data> L202+35: Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.
- `prod-slo-error-budget` [discuss] {reliability, observability} L238+24: Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

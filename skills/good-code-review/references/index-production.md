# Production audit index

One line per stable production card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `production.md`: read them with offset `<first>` and limit `<count>`.

- `prod-a11y-audit-before-launch` [should-fix] {accessibility, usability} <ui> L3+30: Before a public launch, run an accessibility audit against WCAG 2.2 AA that includes assistive technology, and link the report in the launch checklist.
- `prod-alert-actionable-context` [should-fix] {observability} L34+34: Give every paging alert context a responder can act on: what it means and what to do next.
- `prod-alerts-symptoms-golden-signals` [should-fix] {observability} L69+26: Page on user-visible symptoms, such as error rate and latency, not on causes.
- `prod-canary-staged-rollout` [block] {reliability} L96+28: Roll out in stages behind a canary, and abort by rule, not by judgment.
- `prod-config-ships-like-code` [should-fix] {reliability} L125+25: Change configuration and flag values through a reviewed commit and the same staged, automated pipeline as code, not by hand on a host or console.
- `prod-kill-switch-fallback` [should-fix] {reliability} L151+28: Make a risky feature switchable off without a deploy, give each kill switch that stays an owner, and exercise every fallback path in test or in production on a schedule.
- `prod-latency-slo-percentile` [should-fix] {performance, observability} L180+27: Define latency SLOs and alerts on high percentiles, never on the mean.
- `prod-load-test-before-launch` [should-fix] {performance, reliability} L208+27: Load test before launch, past the expected peak, with pass and fail thresholds written down.
- `prod-metric-labels-bounded` [should-fix] {observability, performance} L236+27: Give a metric label only a bounded set of values; never a user id, request id, email, timestamp or raw URL path.
- `prod-profile-on-demand` [discuss] {performance, observability} L264+26: Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.
- `prod-shadow-compare-before-cutover` [should-fix] {correctness, reliability} <data> L291+36: Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.
- `prod-slo-error-budget` [discuss] {reliability, observability} L328+24: Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

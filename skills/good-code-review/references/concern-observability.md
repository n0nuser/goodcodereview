# observability cards

Every stable card that lists the `observability` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## function

- `fn-error-message-actionable` [discuss] {usability, observability} function.md:L632+24: Say in an error message what went wrong and what the reader can do about it.
- `fn-log-or-return-not-both` [should-fix] {observability, maintainability} function.md:L1378+30: Handle an error once: return it or log it, not both.

## service

- `svc-best-effort-optional-deps` [should-fix] {reliability, observability} service.md:L566+34: Give each call to a non-critical dependency a short budget and a default, so its failure degrades the result instead of failing the critical path, and count every fallback.
- `svc-logs-structured` [should-fix] {observability} <server> service.md:L1445+34: Log an event as a constant message plus key/value fields; do not build the message by interpolating variable data into it.
- `svc-tenant-id-in-telemetry` [should-fix] {security, observability} <server> service.md:L2039+28: Put the verified tenant id on every tenant-scoped log, metric and audit record.

## production

- `prod-alert-actionable-context` [should-fix] {observability} production.md:L34+34: Give every paging alert context a responder can act on: what it means and what to do next.
- `prod-alerts-symptoms-golden-signals` [should-fix] {observability} production.md:L69+26: Page on user-visible symptoms, such as error rate and latency, not on causes.
- `prod-latency-slo-percentile` [should-fix] {performance, observability} production.md:L180+27: Define latency SLOs and alerts on high percentiles, never on the mean.
- `prod-metric-labels-bounded` [should-fix] {observability, performance} production.md:L236+27: Give a metric label only a bounded set of values; never a user id, request id, email, timestamp or raw URL path.
- `prod-profile-on-demand` [discuss] {performance, observability} production.md:L264+26: Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.
- `prod-slo-error-budget` [discuss] {reliability, observability} production.md:L328+24: Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

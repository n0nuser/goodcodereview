# observability cards

Every stable card that lists the `observability` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## service

- `svc-best-effort-optional-deps` [should-fix] {reliability, observability} service.md:L536+34: Give each call to a non-critical dependency a short budget and a default, so its failure degrades the result instead of failing the critical path, and count every fallback.
- `svc-tenant-id-in-telemetry` [should-fix] {security, observability} <server> service.md:L1745+28: Put the verified tenant id on every tenant-scoped log, metric and audit record.

## production

- `prod-alerts-symptoms-golden-signals` [should-fix] {observability} production.md:L34+26: Page on user-visible symptoms, such as error rate and latency, not on causes.
- `prod-latency-slo-percentile` [should-fix] {performance, observability} production.md:L119+27: Define latency SLOs and alerts on high percentiles, never on the mean.
- `prod-profile-on-demand` [discuss] {performance, observability} production.md:L175+26: Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.
- `prod-slo-error-budget` [discuss] {reliability, observability} production.md:L238+24: Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

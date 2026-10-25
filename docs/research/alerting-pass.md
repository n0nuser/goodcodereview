# Alerting: extra sources

Fetched 2026-10-25 through WebFetch (a small model summarises the page), so every row is paraphrase. Each row gives the URL, the org, what it says, and the card whose Rule it backs.

1. https://prometheus.io/docs/practices/alerting/ (org: Prometheus). Alert on symptoms rather than causes to reduce noise, and keep alerts few and tied to end-user pain. Page on user-visible errors, and alert on latency and error rate as high up in the stack as possible. Its page says it is based on Rob Ewaschuk's observations at Google, so it is not independent of the SRE book. Backs `prod-alerts-symptoms-golden-signals`.
2. https://grafana.com/docs/grafana/latest/alerting/guides/best-practices/ (org: Grafana Labs). Alerts should detect user-facing failures, not internal component behavior. Latency, errors, and availability are better paging signals. Require a high error rate to hold for some minutes before paging. Backs `prod-alerts-symptoms-golden-signals`.
3. https://www.datadoghq.com/blog/monitoring-101-alerting/ (org: Datadog). Build pages around symptoms rather than causes. Page only when the system stops doing useful work, because symptoms surface real, user-facing problems. Backs `prod-alerts-symptoms-golden-signals`.
4. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability (org: Microsoft). Alert on workload health, not arbitrary values, and make alerts actionable. This row is weaker: it never says "symptoms" or "causes", so it does not count toward the Rule.

Count: Google SRE book (already on the card), Grafana Labs, Datadog = 3 independent orgs behind the Rule line. Prometheus derives from the same Google author, so it adds a source but not an org. Datadog (2015) names Ewaschuk as one influence and builds its own framework. Datadog does not name error rate, so "error rate" in the Rule is an example, backed by Prometheus and Grafana.

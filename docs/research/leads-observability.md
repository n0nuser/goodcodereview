# Leads: observability (logging, metrics, tracing, alerting, dashboards)

Method: each page fetched with `curl -sL --compressed` into a scratch dir, tags stripped with `python3 -I`, sentence found with `rg` in the stripped text. Fetch date 2026-11-24. Datadog docs need the `.md` URL variant (HTML is a JS shell). Quotes are 10 words or fewer. Org grouping follows docs/PROMOTION.md (Microsoft covers Learn, Azure and ASP.NET; Google covers SRE, Cloud docs and Go; Python docs are the Python project).

Existing-card check (`rg` over `cards/`): `prod-alerts-symptoms-golden-signals` (stable; symptoms, `for` duration), `prod-wide-events-bounded-labels` (draft; bounded labels only in the Why), `svc-request-id-logging` (draft, lacks orgs), `svc-api-trace-context` (draft), `svc-tenant-id-in-telemetry`, `svc-security-event-logging`, `svc-logs-tamper-resistant`, `sys-secrets-and-errors` (secrets in logs only in the Why), `sys-pii-minimise-retention`, `fn-mask-credentials-in-output` (CLI output, not logs), `fn-log-or-return-not-both`, `sys-health-liveness-readiness`, `prod-slo-error-budget`, `prod-latency-slo-percentile`, `svc-debug-off-in-production`. Pass 6b lead 5 (log variables as fields, not interpolation) is not yet a card; lead 5 below overlaps it.

## Ranking

| # | Rule | Orgs | Verdict |
|---|---|---|---|
| 1 | Metric labels take bounded values (no user id, request id, raw path) | 3 | clears 3, new card (pulls the Why out of `prod-wide-events-bounded-labels`) |
| 2 | Never write secrets or credentials to a log line | 3 (+1 derived) | clears 3, new card |
| 3 | Neutralise newlines and delimiters in external input before logging | 4 | clears 3, new card |
| 4 | An alert carries an owner and the action to take (runbook link) | 4 for "actionable", 2 to 3 soft for "runbook link" | clears 3 on actionable; runbook link soft |
| 5 | Log events as structured key/value records, not formatted strings | 3 (one descriptive) | clears 3; merge with pass 6b lead 5 |
| 6 | Log lines carry the trace or correlation id | 3 (two descriptive) | soft; clause on `svc-request-id-logging` |
| 7 | Span names are low-cardinality; request detail goes in attributes | 2 firm + 1 soft | short |
| 8 | Write the log stream to stdout, not to app-managed files | 1 firm + 4 descriptive | soft |
| 9 | Dashboard answers a stated question; no per-instance copies | 3 general | soft, hard to check on a diff |
| 10 | Metric names follow one scheme, base units | Prometheus vs OTel conflict | short, conflict |

## 1. Metric labels take bounded values

Rule candidate: "Give a metric label or dimension only a bounded set of values; never a user id, request id, email, timestamp or raw URL path." A diff that adds `labels={"user_id": uid}` or `path=request.url.path` to a counter is a FAIL. Nearest card: `prod-wide-events-bounded-labels` (draft; "keep metric labels bounded" is a trailing sentence in the Why, and the Rule is about wide events). New card, scoped to metrics, with `tool_gate` naming a cardinality limit or label lint. The draft keeps the wide-event Rule and can drop its label clause.

1. https://prometheus.io/docs/practices/naming/ . Prometheus. "Do not use labels to store dimensions with high cardinality", such as user IDs, email addresses or unbounded value sets. Found: Labels section. The instrumentation page adds a rule of thumb (cardinality under 10; investigate over 100).
2. https://learn.microsoft.com/en-us/azure/azure-monitor/essentials/metrics-custom-overview . Microsoft (Azure Monitor). "You should never use a constantly changing value in a dimension"; timestamp is the example; aim under 100 values. Found: "High-cardinality metric dimensions". Also: do not put a variable in the metric name.
3. https://docs.micrometer.io/micrometer/reference/concepts/naming.html . Micrometer (Broadcom/VMware project). Tag values from user-supplied sources can blow up cardinality: "carefully normalize and add bounds to user-supplied input". Found: tag-naming section, with a 404-URI example.
4. Soft extra: https://opentelemetry.io/docs/specs/otel/metrics/sdk/ . OpenTelemetry. SDKs SHOULD support a cardinality limit. Found: "Cardinality limits". A tool-side guard, not a rule on authors.

Count: Prometheus, Microsoft, Micrometer = 3 firm. Counterpoint: Honeycomb and wide-event stores want high-cardinality fields (user id, request id); the rule is about aggregated metrics, and the high-cardinality value belongs in a log, span or event instead. Azure says to switch to custom logs when high cardinality is essential. Draft id: `prod-metric-labels-bounded`.

## 2. Never write secrets or credentials to a log line

Rule candidate: "Do not log passwords, tokens, keys or session ids; log an internal id or a masked value instead." A diff that logs a request header map, a whole config object or `token=%s` is a FAIL. Nearest card: `sys-secrets-and-errors` (secrets-in-logs is one clause in its Why; Rule is fail-closed and error bodies) and `fn-mask-credentials-in-output` (CLI display). New card, `context: [server]`, `tool_gate`: secret-scanning of log output in tests plus a redacting formatter.

1. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html . OWASP. Access tokens, passwords, session ids, keys, connection strings, card data "should usually not be recorded directly in the logs". Found: "Data to exclude" list ("removed, masked, sanitized, hashed, or encrypted").
2. https://cwe.mitre.org/data/definitions/532.html . MITRE (CWE-532). "Do not write secrets into the log files." Found: Potential Mitigations.
3. https://docs.gitlab.com/development/secure_coding_guidelines/ . GitLab. "Never log credentials under any circumstances"; log the credential's internal id instead. Found: "What should not be captured in the logs". Also bars personal data other than integer ids, UUIDs and IPs.
4. Soft: https://opentelemetry.io/docs/security/handling-sensitive-data/ . OpenTelemetry. Follow data minimization; you are responsible for sensitive data in telemetry. No log-specific ban.
5. Not independent: https://docs.aws.amazon.com/prescriptive-guidance/latest/logging-monitoring-for-application-owners/logging-best-practices.html . AWS Prescriptive Guidance. Same list as OWASP, near word for word. Do not count it.

Count: OWASP, MITRE, GitLab = 3 firm. Counterpoint: debug logs of full requests are sometimes needed; the usual answer is a redaction layer and a short retention (`sys-pii-minimise-retention`), and GitLab allows IPs and UUIDs. Draft id: `svc-no-secrets-in-logs`.

## 3. Neutralise external input before it is written to a log

Rule candidate: "Strip or escape CR, LF and delimiter characters in user-supplied values before logging them, or log them as structured fields." A diff that logs `f"login failed for {username}"` with a raw header or form value in a plain-text log is a FAIL. Nearest card: none (`svc-logs-tamper-resistant` is about storage, not input). New card.

1. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html . OWASP. "Perform sanitization on all event data to prevent log injection attacks", naming CR, LF and delimiters. Found: event-data handling list.
2. https://cwe.mitre.org/data/definitions/117.html . MITRE (CWE-117). Weakness: a log message built from external input without neutralising special elements. Found: Description.
3. https://docs.gitlab.com/development/secure_coding_guidelines/ . GitLab. External input "should not be directly captured in the logs without any validation". Found: "Protecting log files".
4. https://docs.python.org/3/howto/logging-cookbook.html . Python. Shows a formatter that escapes newlines "if you are concerned about log injection". Found: multi-line records recipe. Descriptive, not a rule.

Count: OWASP, MITRE, GitLab = 3 firm; Python descriptive. Counterpoint: JSON-structured logs escape newlines by construction, so this card should be scoped to plain-text logs (ties into lead 5). Draft id: `svc-log-input-neutralised`.

## 4. An alert carries an owner and the action to take

Rule candidate: "Every alert rule says who owns it and what to do, with a runbook or doc link in an annotation." A diff that adds an alert rule with no `runbook_url`, owner or description is a FAIL. Nearest card: `prod-alerts-symptoms-golden-signals` (stable; what to page on, not what the page carries). New sibling card.

1. https://sre.google/sre-book/monitoring-distributed-systems/ . Google SRE. "Every page should be actionable." Found: alerting-philosophy list. The introduction chapter (https://sre.google/sre-book/introduction/) says a recorded "playbook" gave roughly a 3x MTTR improvement.
2. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability . Microsoft. "Alerts should be actionable and provide context", with a process that "defines owners, actions, and scope"; also "define SLO-driven alerts, dashboards, and runbooks". Found: alerting paragraph and Azure Functions note.
3. https://docs.aws.amazon.com/wellarchitected/latest/operational-excellence-pillar/ops_workload_observability_create_alerts.html . AWS. OPS08-BP04 "Create actionable alerts"; anti-pattern is too many non-critical alerts. Found: page title and "Common anti-patterns". No runbook sentence.
4. https://docs.datadoghq.com/monitors/guide/monitor_best_practices.md . Datadog. Context "clarifies ownership and impact". Found: "Give context".
5. Runbook field only (tool descriptions, soft): https://grafana.com/docs/grafana/latest/alerting/fundamentals/alert-rules/annotation-label/ (`runbook_url`: runbook page "to guide operators"); https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/ (annotations "such as alert descriptions or runbook links"); https://cloud.google.com/monitoring/alerts/doc-variables (playbook URL in alert documentation).

Count: Google, Microsoft, AWS, Datadog = 4 on "actionable with context"; the runbook-link wording is firm only for Google (playbooks) and Microsoft (runbooks), with Grafana, Prometheus and Google Cloud as feature descriptions. Write the Rule at "actionable: owner plus next step", with runbook link as the checkable form. Counterpoint: ticket-queue and informational alerts need no runbook (Google SRE sends them to a queue); scope to paging alerts. Draft id: `prod-alert-has-owner-and-runbook`.

## 5. Log events as structured key/value records

Rule candidate: "Emit log events as a message plus key/value fields, not a formatted string." A diff that adds `log.Printf("order %s failed for %s", id, user)` where the codebase has a structured logger is a FAIL. Nearest card: none. Overlaps pass 6b lead 5 (`fn-log-no-interpolated-message`: pass variables as arguments, not interpolated). Same rule seen from two sides; propose one card, with this lead's orgs added to 6b's.

1. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability . Microsoft. "Prefer structured telemetry so that the data is queryable and searchable." Found: telemetry-collection list. The ASP.NET and logging-library pages add the template rule (6b lead 5).
2. https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-instrumentation/logging.md . Kubernetes. Unstructured klog methods like `Infof` are "no longer recommended"; migrate to structured calls. Found: "How to log".
3. https://go.dev/blog/slog . Google (Go). "Structured logs use key-value pairs" so they can be parsed, filtered, searched. Found: opening section. Descriptive of the benefit, no ban on formatted strings.
4. Soft: https://www.elastic.co/guide/en/ecs-logging/overview/current/intro.html (Elastic; pitches JSON ECS logs to avoid grok parsing, a product pitch); https://cloud.google.com/logging/docs/structured-logging (Google Cloud; how-to for `jsonPayload`).

Count: Microsoft, Kubernetes, Google = 3, the third descriptive. Counterpoint: CLIs and small scripts print human text; scope to services that ship logs to an aggregator. Draft id: `svc-logs-structured`.

## 6. Log lines carry the trace or correlation id

Clause lead for `svc-request-id-logging` (draft, `lacks: evidence`). That card's Rule already says it; what is missing is sources beyond Honeycomb.

1. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability . Microsoft. "Use correlation IDs consistently" across presentation, middle and data tiers. Found: "Correlate data for end-to-end insights".
2. https://docs.datadoghq.com/tracing/other_telemetry/connect_logs_and_traces.md . Datadog. Correlation "is improved by the injection of trace IDs, span IDs" and `env`, `service`, `version` into logs. Found: opening paragraph.
3. https://cloud.google.com/trace/docs/trace-log-integration . Google. Set `trace`, `spanId` and `traceSampled` on a LogEntry to link logs with traces. Found: "Link log entries with traces". Describes the feature.
4. Descriptive only: https://opentelemetry.io/docs/specs/otel/logs/data-model/ (log record has TraceId and SpanId fields); https://www.elastic.co/docs/reference/ecs/ecs-tracing (`trace.id` field).

Count: Microsoft firm, Datadog moderate, Google and OTel and Elastic descriptive. Verdict soft: the sources say "support or recommend", not "every line must". Caveat from the card: logs and traces are sampled independently (Datadog says so), so the id must be on the line even when the trace is dropped. Action: add Microsoft and Datadog and Google to `borrowed_from`, keep status draft unless the maintainer accepts "recommend" as enough.

## 7. Span names are low-cardinality

Rule candidate: "Name a span after the operation class (`GET /users/{id}`), never with ids or raw paths; put the specifics in attributes." Nearest card: none (lead 1 is the metric version). A diff that builds `tracer.start_span(f"get_user/{uid}")` is a FAIL.

1. https://opentelemetry.io/docs/specs/otel/trace/api/ . OpenTelemetry. Span name SHOULD be general; `get_user/314159` is "not a good name due to its high cardinality". Found: "Span" name section.
2. https://docs.sentry.io/platforms/javascript/tracing/instrumentation/custom-instrumentation/ . Sentry. Auto-derived names "are low-cardinality"; raw paths and queries "stay in attributes". Found: span-name note. A description of automatic behaviour. Also https://develop.sentry.dev/sdk/telemetry/traces/span-operations/ says operations are low-cardinality and "as general as possible".
3. https://docs.datadoghq.com/tracing/glossary.md . Datadog. Dynamic endpoints are "grouped by a static span name" such as `web.request`. Found: Resource entry. Descriptive.

Count: OpenTelemetry firm, Sentry and Datadog soft = 2 firm + 1 soft. Short; look for Honeycomb, Jaeger or Elastic text before carding (their docs did not render a matching sentence). Draft id would be `svc-span-name-low-cardinality`.

## 8. Write the log stream to stdout

Rule candidate: "A containerised service writes events to stdout/stderr and leaves routing to the platform; it does not open or rotate log files." Nearest card: none.

1. https://12factor.net/logs . Twelve-Factor (Heroku authors, now a community spec). App "should not attempt to write to or manage logfiles"; each process writes its stream to stdout. Found: opening paragraphs.
2. Descriptive of platform behaviour, not a rule: https://devcenter.heroku.com/articles/logging (logs capture what the app writes to stdout or stderr); https://docs.cloudfoundry.org/devguide/deploy-apps/streaming-logs.html (OUT and ERR channels); https://kubernetes.io/docs/concepts/cluster-administration/logging/ (containers write to stdout and stderr; node agent collects); https://docs.docker.com/engine/logging/ (stdout and stderr drivers).

Count: 1 firm, 4 platforms that work this way. Verdict soft: platform docs describe what they capture, they do not say "do not write files". Counterpoint: VMs, desktop and CLI tools legitimately write files.

## 9. A dashboard answers a stated question

1. https://sre.google/sre-book/monitoring-distributed-systems/ . Google SRE. Dashboards "should answer basic questions about your service". Also: signals neither on a dashboard nor in an alert are "candidates for removal".
2. https://grafana.com/docs/grafana/latest/dashboards/build-dashboards/best-practices/ . Grafana Labs. "A dashboard should tell a story or answer a question"; use template variables instead of a copy per node; keep dashboard JSON in version control.
3. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability . Microsoft. "Ensure that dashboards are meaningful and actionable."

Count: 3 orgs, all general guidance. Verdict soft: the checkable parts (JSON in version control, variables not copies) come from Grafana alone. Do not card unless a second org states the as-code or no-copy part.

## 10. Metric names: one scheme, base units

Prometheus (https://prometheus.io/docs/practices/naming/) asks for a domain prefix, base units (seconds, bytes) and a unit suffix such as `_seconds`, `_total`. OpenTelemetry (https://opentelemetry.io/docs/specs/semconv/general/metrics/) says metrics with unit metadata SHOULD NOT put the unit in the name, and uses UCUM units. Datadog (https://docs.datadoghq.com/developers/guide/what-best-practices-are-recommended-for-naming-metrics-and-tags.md) wants a namespace prefix and consistency across teams, with no unit rule. The only shared points are a namespace prefix and consistency within a codebase. Verdict short and in conflict; skip, or card as "follow the repo's metric naming scheme" only if a Rule that vague earns a place.

## Not carded or not found

- Health checks: already `sys-health-liveness-readiness`.
- Alert `for` duration, SLO burn rate, percentiles: already inside `prod-alerts-symptoms-golden-signals`, `prod-slo-error-budget`, `prod-latency-slo-percentile`.
- Log level semantics (ERROR means someone must act): only definitions (Microsoft, Python, Google Cloud severity), no org states a rule against logging expected conditions at ERROR. Not found.
- Failure metrics: Prometheus asks for a total next to a failure count; no second org found.
- Prometheus, Grafana, Datadog and Microsoft pages already back `prod-alerts-symptoms-golden-signals`; not repeated here.

## Parent notes

- Leads 2 and 3 are security-flavoured; the maintainer may want `severity: should-fix` and `context: [server]`.
- Shared scratch dir had other agents writing `get.sh` and `strip.py` at the same path; two of my first fetches failed on a clobbered script and were redone from a private dir.

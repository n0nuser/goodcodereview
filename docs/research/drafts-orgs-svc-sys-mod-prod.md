# Draft cards lacking orgs (service, system, module, production, incident)

Method: `curl -sL` + `python3 -I` tag strip, sentence matched with a regex on the stripped text. Fetch date 2026-11-24. Quotes are short excerpts. "Firm" = states the practice as advice; "soft" = describes a feature or an example only. Org grouping follows docs/PROMOTION.md. Cards not edited. Pages that returned JS shells or no match (GitLab docs, Sentry develop, JetBrains, protobuf API guide, Rails guides, AWS REL12, Azure incident guide, Finagle, Redis, Datadog) are not counted.

23 draft cards have `lacks: orgs`. Result: 5 reach three firm, 5 reach three with one soft source, 13 stay short.

## Summary

| Card | Orgs before | Orgs after | Verdict |
|---|---|---|---|
| sys-shuffle-shard | AWS, Airbnb | +Grafana Labs = 3 | clears 3 |
| svc-tenant-scope-in-data-layer | Microsoft, OWASP | +AWS = 3 | clears 3 |
| mod-call-parent-setup-teardown | Laravel, PSF | +Django = 3 | clears 3 |
| svc-path-normalise-before-authz | Envoy, PortSwigger | +Istio (firm), +Cloudflare (soft) = 4 | clears 3 |
| svc-server-read-timeouts | Cloudflare, Node.js | +Microsoft, +nginx, +Apache, +Envoy = 6 | clears 3 (all describe settings, Envoy edge page is the only "recommended" one) |
| svc-api-trace-context | W3C | +Google Cloud Trace, +OpenTelemetry (soft) = 3 | clears 3 with soft |
| svc-paginate-by-server-links | GitHub / Google | next link: +Microsoft, +Zalando; token: +Zalando | next-link clears 3; token clause 2 firm |
| sys-cache-hit-rate-watched | AWS, Google | +Microsoft (soft) = 3 | soft 3 |
| svc-logs-tamper-resistant | Google, OWASP | +AWS CloudTrail (soft) = 3 | soft 3 |
| sys-constraint-not-valid | PostgreSQL | +Django (soft), +strong_migrations (soft, one author) = 3 | soft |
| sys-leader-two-leaders | AWS | +Microsoft (firm), +Kubernetes (soft) = 3 | clears 3 with soft |
| svc-debug-off-in-production | OWASP, Microsoft | debug clause +Django, +Flask; Swagger clause no new | debug clause clears; Swagger clause short |
| mod-thin-entry-point | none | Python (PSF), Rust = 2 | short by one |
| inc-postmortem-owned-actions | none | Atlassian, Google SRE workbook (soft) = 2 | short |
| sys-cache-cold-start | AWS | +Microsoft (partial), +Fastly, +Go singleflight (both tool descriptions) | short |
| svc-401-sends-challenge | IETF | +Mozilla = 2 | short |
| prod-wide-events-bounded-labels | Honeycomb | labels: +Prometheus; events: +Stripe (soft) | short |
| mod-no-repeated-switches | Refactoring.Guru, Google | nothing | short (2) |
| sys-hedge-budget | Google, Envoy | nothing | short (2) |
| svc-boolean-no-is-prefix | Google, Microsoft | nothing | short (2) |
| mod-central-config | Uber, Cabify | nothing for "one settings module" | short, drop candidate |
| mod-no-wire-types-in-public-api | cursor/plugins | nothing | short, drop candidate |
| inc-review-asks-which-check | Anthropic via x.com | nothing | short, drop candidate |

## Per card

### sys-shuffle-shard (3)
- Grafana Labs: https://grafana.com/docs/mimir/latest/configure/configure-shuffle-sharding/ . "Shuffle sharding is a technique that isolates different tenant's workloads and gives each tenant a single-tenant experience". Also: "The goal of shuffle sharding is to reduce the blast radius of an outage and better isolate tenants."

### svc-tenant-scope-in-data-layer (3)
- AWS: https://aws.amazon.com/blogs/database/multi-tenant-data-isolation-with-postgresql-row-level-security/ . "By centralizing the enforcement of RDBMS isolation policies at the database level you ease the burden on your software developers." Also "reduce the risk of cross-tenant data access".

### mod-call-parent-setup-teardown (3)
- Django: https://docs.djangoproject.com/en/stable/topics/testing/tools/ . "If you need to override those methods, don't forget to call the super implementation".

### svc-path-normalise-before-authz (4)
- Istio: https://istio.io/latest/docs/ops/best-practices/security/ . "A policy mismatch happens when the Envoy proxy and the backend application interpret the request differently." and "it's also why we need path normalization in the authorization policy". Note Istio builds on Envoy; keep Istio as its own project but flag if the maintainer groups it with Envoy.
- Cloudflare (soft): https://developers.cloudflare.com/rules/normalization/ . "...modify the URLs of incoming requests so that they conform to a consistent formatting standard. This is important because the same resource can be requested using different URL formats". Feature description, no authz sentence in the part matched.
- Envoy edge page https://www.envoyproxy.io/docs/envoy/latest/configuration/best_practices/edge sets `normalize_path: true`, `merge_slashes: true`; same org as the existing Envoy source.

### svc-server-read-timeouts (6)
- Microsoft Kestrel: https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/options . "RequestHeadersTimeout gets or sets the maximum amount of time the server spends receiving request headers". Soft (option description).
- nginx: https://nginx.org/en/docs/http/ngx_http_core_module.html . "If a client does not transmit the entire header within this time, the request is terminated with the 408 (Request Time-out) error." Soft.
- Apache httpd: https://httpd.apache.org/docs/2.4/mod/mod_reqtimeout.html . Example "RequestReadTimeout handshake=5 header=10 body=30". Soft.
- Envoy (firm): https://www.envoyproxy.io/docs/envoy/latest/configuration/best_practices/edge . "Envoy is a production-ready edge proxy, however, the default settings are tailored for the service mesh use case, and some values need to be" changed; the listed settings include `request_timeout` and `stream_idle_timeout`.

### svc-api-trace-context (3)
- Google Cloud Trace: https://cloud.google.com/trace/docs/trace-context . "When your application handles a request and calls downstream services, it passes identifiers such as the trace ID, parent span ID, and sampling status by using request headers or metadata."
- OpenTelemetry (soft): https://opentelemetry.io/docs/concepts/context-propagation/ . "The default propagator uses the headers specified by the W3C TraceContext specification." Describes the SDK, not a rule for service authors.

### svc-paginate-by-server-links
Next-link clause:
- Microsoft: https://raw.githubusercontent.com/microsoft/api-guidelines/vNext/azure/Guidelines.md . "DO return a `nextLink` field with an absolute URL that the client can GET in order to retrieve the next page of the collection." Server-side rule, supports the clause by implication.
- Zalando: https://opensource.zalando.com/restful-api-guidelines/ . Rule heading "SHOULD use pagination links" (heading only matched in the index; body not quoted).
Token clause:
- Zalando: "cursor : an opaque pointer to a page, never to be inspected or constructed by clients." Firm.
- Microsoft's example uses `"nextLink": "{opaqueUrl}"` (soft).
Count: next link 3 (GitHub, Microsoft, Zalando); token 2 firm (Google, Zalando) + 1 soft. Not found: Slack (describes cursors as "pointers", no opacity sentence), Stripe, YouTube (Google), Atlassian (JS shell).

### sys-cache-hit-rate-watched (3, soft)
- Microsoft: https://learn.microsoft.com/en-us/azure/azure-cache-for-redis/cache-how-to-monitor . Lists a "Cache Hits" metric ("Cache Hits is the total number of hits for the entire cache"). Metric exists; no sentence says to alert on it.

### svc-logs-tamper-resistant (3, soft)
- AWS CloudTrail: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-log-file-validation-intro.html . "To determine whether a log file was modified, deleted, or unchanged after CloudTrail delivered it, you can use CloudTrail log file integrity validation." Detects tampering, does not say ship off-host.

### sys-constraint-not-valid (3, soft)
- Django: https://docs.djangoproject.com/en/stable/ref/contrib/postgres/operations/ . "PostgreSQL supports the NOT VALID option with the ADD CONSTRAINT statement to add check constraints without enforcing validation on existing rows." and a `ValidateConstraint` operation for later. Descriptive.
- strong_migrations: https://github.com/ankane/strong_migrations/blob/master/README.md . "add the foreign key without validating existing rows ... Then validate them in a separate migration." A tool by one author, not an org.
Not found: GitLab (docs.gitlab.com is a JS shell; raw path 404), Sentry, Rails guides.

### sys-leader-two-leaders (3)
- Microsoft: https://learn.microsoft.com/en-us/azure/architecture/patterns/leader-election . "Stop leader-specific work when ownership is lost or can't be confirmed. Lease expiration doesn't stop the old process; use resource-side ownership checks to reject stale-leader writes. Make replayed business operations idempotent." Firm, matches all three clauses.
- Kubernetes (soft): https://pkg.go.dev/k8s.io/client-go/tools/leaderelection . "This implementation does not guarantee that only one client is acting as a leader (a.k.a. fencing)." States the limit, not the rule.

### svc-debug-off-in-production
- Django: https://docs.djangoproject.com/en/stable/howto/deployment/checklist/ . "For a production environment, though, this is a really bad idea, because it leaks lots of information about your project".
- Flask (Pallets): https://flask.palletsprojects.com/en/stable/debugging/ . "Do not run the development server, or enable the built-in debugger, in a production environment."
Debug clause: OWASP, Django, Flask = 3. Swagger clause: still Microsoft only. Suggest narrowing the Rule to debug mode, or splitting Swagger out.

### mod-thin-entry-point (2)
- Python: https://docs.python.org/3/library/__main__.html . "those files are kept short and import functions to execute from other modules. Those other modules can then be easily unit-tested and are properly reusable."
- Rust Book: https://doc.rust-lang.org/book/ch12-03-improving-error-handling-and-modularity.html . "Split your program into a main.rs file and a lib.rs file and move your program's logic to lib.rs."
Go module layout page does not say it. Needs one more; both should be added to `borrowed_from` (currently empty).

### inc-postmortem-owned-actions (2)
- Atlassian: https://www.atlassian.com/incident-management/handbook/postmortems . "Who will take the actions and by when?" and "All postmortem actions must be tracked in Jira." Firm; priority actions also carry an SLO.
- Google SRE workbook (soft, example): https://sre.google/workbook/postmortem-culture/ . The sample action-item table has columns "Action Item, Type, Priority, Owner, Tracking Bug". An example, not a stated rule.
PagerDuty response guide names a postmortem owner, not action owners.

### sys-cache-cold-start (short)
- Microsoft (partial): https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching . "An application should be able to continue functioning if the shared cache is unavailable." Covers fallback, not capping the miss path.
- Fastly (soft): https://docs.fastly.com/en/guides/request-collapsing . "Request collapsing is the practice of combining multiple requests for the same object into a single request to origin". CDN feature.
- Go singleflight (soft, Google): "provides a duplicate function call suppression mechanism". Library description; same org as Google if Google is later added.
Facebook memcache paper PDF returned no text match.

### svc-401-sends-challenge (2)
- Mozilla MDN: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/401 . "This status code is sent with an HTTP WWW-Authenticate response header that contains information on the authentication scheme the server expects". MDN restates RFC 9110. OWASP REST cheat sheet lists 401 with no challenge sentence.

### prod-wide-events-bounded-labels (short)
- Prometheus: https://prometheus.io/docs/practices/naming/ . "Do not use labels to store dimensions with high cardinality (many different label values), such as user IDs, email addresses, or other unbounded sets of values." Firm, labels clause only.
- Stripe (soft): https://stripe.com/blog/canonical-log-lines . One canonical log line per request; blog post, not a rule.
- Google Cloud Monitoring defines cardinality but gives no rule.

### No new org found
mod-no-repeated-switches, sys-hedge-budget, svc-boolean-no-is-prefix, mod-central-config (12factor says "Store config in the environment", which is about location, not one module), mod-no-wire-types-in-public-api (Android data-layer page says nothing on point), inc-review-asks-which-check (GitLab handbook and AWS pages gave no matching sentence).

## Drop candidates
- mod-central-config: nobody backs "one settings module"; the knob-out-of-code half is already carried by other cards. Drop or reduce to the backed half.
- inc-review-asks-which-check: one vendor source, an x.com link that is not a primary page; no second org found. Drop.
- mod-no-wire-types-in-public-api: single vendor opinion, nothing found. Drop unless a source surfaces.
- prod-wide-events-bounded-labels: glues two rules. Split "bounded labels" (Prometheus plus two more needed) from "one event per request".
- svc-debug-off-in-production: keep, but narrow to debug mode, or split Swagger.

# Security batch P: third organisations for I1-I8, plus workload identity

Checked 2026-11-06 against `docs/research/sec-classes-I.md`. Every page below was fetched and read; quotes are verbatim, 1-2 per row. Organisation counting follows `docs/PROMOTION.md`: one organisation counts once, a person's blog/book does not count, and a plan or draft does not count as a practice.

The task was to find the organisations missing for one weak clause per class, not to re-research the whole class. Each Verdict therefore says how many organisations the clause had before, which ones are new, and whether the clause now reaches three. About 30 pages were fetched successfully; two URLs failed (an old Redis keyspace path and the TypeORM docs). The one linter page opened this pass is the OpenSSF Scorecard checks page, to confirm the P8 gate.

Two findings up front:

- **P4's cost clause is already the Rule of a draft card.** `svc-rate-limit-by-cost` says "When request costs differ by orders of magnitude, charge each request its estimated cost against the quota instead of counting it as one" and cites Shopify, GitHub and Airbnb. Do not add a second card for that clause; extend or promote that draft. The new work for I4 is the window/reset clause.
- **P9 has no existing card.** `code-secret-scan` removes a leaked key and `code-workflow-supply-chain` limits a workflow's token, but neither says to replace a long-lived cloud key with a federated short-lived credential.

## P1 (I1): filter soft-deleted rows by default in every query path

**Candidate Rule.** Make every read path exclude deleted records: filter tombstones in the model's default scope, and require an explicit opt-in to read them.

**Level.** service. **Tool gate.** none found.

**Existing card.** None. `fn-object-level-authz` authorises one object, not a deleted one; no card mentions soft delete, `deleted_at`, or tombstones.

**FAIL/PASS.** FAIL: `SELECT * FROM doc WHERE id = ?` against a table with `deleted_at`, with no filter, plus a second path that uses raw SQL. PASS: the model uses `SoftDeletes`, `paranoid: true` or `@SoftDelete`, a shared helper adds `deleted_at IS NULL`, and raw SQL is the only audited bypass.

1. https://laravel.com/docs/12.x/eloquent#soft-deleting (org: Laravel). The framework's documented default is exclusion: "When querying a model that uses soft deletes, the soft deleted models will automatically be excluded from all query results." The mechanism is a global scope: "Global scopes allow you to add constraints to all queries for a given model." The page adds that Laravel's own soft delete functionality "utilizes global scopes" to retrieve only non-deleted models. The bypass is one explicit call: "you may force soft deleted models to be included in a query's results by calling the `withTrashed` method". Backs P1.

2. https://sequelize.org/docs/v6/core-concepts/paranoid/ (org: Sequelize). The default is stated for every query, not one helper: "Every query performed by Sequelize will automatically ignore soft-deleted records (except raw queries, of course)." It names the bypass and its cost: "If you really want to let the query see the soft-deleted records, you can pass the `paranoid: false` option to the query method." It also shows that a primary-key lookup returns `null` for a deleted row, "as if that record didn't exist". Backs P1.

3. https://docs.jboss.org/hibernate/orm/6.6/userguide/html_single/Hibernate_User_Guide.html (org: Hibernate / Red Hat, partial; section 3.12). The guide makes the annotation the supported path: "Hibernate offers first-class support for this behavior through its `@SoftDelete` annotation." It also rejects the hand-rolled version: "It was possible to hack together support for soft deletes in previous versions using a combination of filters, `@Where` and custom delete event handling. However, that approach was tedious and did not work in all cases. `@SoftDelete` should be highly preferred." The page does not state in so many words that queries exclude deleted rows by default; it backs "use the built-in soft-delete mapping, not ad-hoc filters", so count it only as partial for this clause. Backs P1 partially.

4. https://edgeguides.rubyonrails.org/active_record_querying.html (org: Rails, partial). Rails documents the same mechanism and its bypass without using the word "delete": "If you want a scope to be applied across all queries to the model, you can use the `default_scope` method within the model itself." And: "If we wish to remove scoping for any reason we can use the `unscoped` method ... This method removes all scoping and will do a normal query on the table." This backs "a default scope really does cover every query, and the bypass is explicit", not "deleted rows". Partial, not counted.

**Verdict.** Before this pass the clause had Microsoft only (EF Core global query filter). New: Laravel and Sequelize, both of which state the default exclusion in so many words. **3 solid organisations (Microsoft, Laravel, Sequelize)**, with Hibernate and Rails as partial support for the mechanism. Confidence high for the clause as written ("ORM global filter / default scope").

## P2 (I2): put the tenant in every cache key and in log/analytics queries

**Candidate Rule.** Carry the tenant and the access filter into every derived store: prefix the cache key with the tenant, and write the tenant into every log, metric and analytics record so the read can be scoped by it.

**Level.** service. **Tool gate.** none found.

**Existing card.** None. `fn-object-level-authz` checks one object; nothing mentions cache keys, key prefixes, log labels or a tenant filter in a derived store.

**FAIL/PASS.** FAIL: `cache.set("user:"+id, row)` and `logger.info("user %s", id)` with no tenant field, in a shared cache and a shared log index. PASS: `cache.set(f"t{tenant}:user:{id}", row)`, every log/metric record carries `tenant_id`, and the analytics query filters on it.

1. https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/cache-redis (org: Microsoft). This is the practice, with the tenant named: "Use a unique and stable tenant prefix, such as `tenantId:`, to identify a tenant's keys." On onboarding: "establish a unique and collision-resistant convention for key prefixes, like a tenant identifier." It also caps the claim, which belongs in the counterpoint: "A key prefix or hash slot isn't an authorization or tenant-isolation boundary." Backs P2 (cache key).

2. https://redis.io/blog/data-isolation-multi-tenant-saas/ (org: Redis). The practice is named for caches: "Tenant-aware key naming (for example, tenant:{tenant-id}:{resource-type}:{resource-id}) reduces the risk of key collisions between tenants and, combined with proper Access Control Lists (ACLs) and tenant-aware application logic, helps avoid cross-tenant data exposure." It says where the leaks come from: "Cache leaks often aren't about collisions—they're frequently caused by missing tenant context on read/write paths (wrong key prefix, wrong token leading to wrong prefix)." It also caps the key: "Redis OSS logical databases are not a security boundary". Backs P2 (cache key).

3. https://developers.cloudflare.com/workers/cache/cache-keys/ (org: Cloudflare). The platform puts the tenant in the key only if the caller does: "If you use `ctx.props` to carry per-caller authorization context — user ID, tenant ID, organization, role — caching is safe by default." And: "Two callers that invoke your Worker with different `ctx.props` get separate cached entries — one caller can never receive another caller's cached response." The failure is documented too: if auth arrives in a header that is not in the key, "that input is not automatically part of the cache key. Two callers authenticated by different header values but otherwise identical requests will share a single cached entry". Backs P2 (cache key).

4. https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/layers-hide-tenant-details.html (org: AWS). Tenant context is injected into observability records by the shared layer: "both services need to inject tenant context into their log messages and metric events". The layer "uses the JWT token to resolve the tenant context and inject it into the log messages and metric events." That is a team describing what it does across every service, which is the log/analytics half of the clause. Backs P2 (logs/analytics).

5. https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-tenant-logging (org: Google). The log store itself is partitioned by tenant: "To create tenant-specific logs, the cluster admin creates a sink to route log entries to each tenant's project." And: "In each tenant project, individual teams can control how the logs are stored and used". The filter is the tenant's namespace: `--log-filter=resource.labels.namespace_name="$TENANT_NAMESPACE"`. This is a config-level practice a reviewer can check. Backs P2 (logs/analytics).

**Verdict.** Before this pass, both clauses had OWASP only. New for the cache-key clause: Microsoft, Redis and Cloudflare, all three naming the tenant and the key. **4 solid (OWASP, Microsoft, Redis, Cloudflare) on the cache key.** New for the log/analytics clause: AWS and Google, both of which name the practice and the mechanism. **3 solid (OWASP, AWS, Google) on logs/analytics.** Overall class: 6 organisations (OWASP, Microsoft, Redis, Cloudflare, AWS, Google). Both halves now reach three.

## P3 (I3): an export returns only what the requesting user may read

**Candidate Rule.** Scope every export, backup and restore to the principal and tenant that may read it, and apply the caller's read filter inside the export query rather than after it.

**Level.** service. **Tool gate.** none found.

**Existing card.** None. `fn-object-level-authz` covers a single object fetch, not a bulk export; no card mentions export formats, download endpoints or restore.

**FAIL/PASS.** FAIL: `GET /export` runs `SELECT * FROM rows` and streams it to any authenticated caller. PASS: the export handler reuses the caller's read filter (`WHERE tenant_id = ? AND ...`), and only formats that apply restrictions are offered.

1. https://confluence.atlassian.com/display/CONF719/Export+Content+to+Word,+PDF,+HTML+and+XML (org: Atlassian). The export carries the exporter's read permission: "HTML – export an HTML file containing only the pages you have permission to view." The same is stated for PDF: "PDF – export a PDF file containing only the pages you have permission to view." And for a single item: "If you've got permission to view the page in Confluence, you'll be able to export it in this way". Backs P3.

2. https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-export-data (org: Microsoft). The export is gated on read permission: "If you have permissions to the data, you can see and export the data that Power BI uses to create a visualization." Row-level security is applied at export time: "Row-level security (RLS) - If RLS is applied, you can only export data you're authorized to see. This condition might result in no data or limited data being exported." Backs P3.

3. https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html (org: OWASP), already cited in `sec-classes-I.md` for this class. It supplies the restore half ("Reapply current access and retention rules") and the export test, but not the export-scope sentence this clause needs beyond OWASP's general tenant rule. Not re-opened this pass.

**Verdict.** Before this pass the export-scope clause had OWASP only. New: Atlassian and Microsoft, both documenting that the export applies the caller's read rights. **3 organisations (OWASP, Atlassian, Microsoft) for the export-scope clause.** Confidence high, with an important caveat below: Atlassian's own XML export is a counter-example, so the Rule must name the format or the query, not just "an export".

**Counterpoint for this clause.** Atlassian shows that not every export obeys the filter: "XML – export a full XML file containing all the pages in the space, including those you don't have permission to view." A reviewer should therefore check which export path is in the diff; a format that deliberately exports the whole space is a different product decision, not a missing `WHERE`.

## P4 (I4): charge the limiter by cost, and name the window and reset

**Candidate Rule.** Charge each request to the authenticated principal at its estimated cost, and publish the window and the reset so a client can back off before it is rejected.

**Level.** service. **Tool gate.** none found.

**Existing card.** `svc-rate-limit-quota` (stable) has a per-tenant quota; its Why adds a per-tenant concurrency cap and 429 vs 503. Missing: a principal or key as the limiter key, cost rather than call count, an explicit window/reset, and charging before the work runs. **`svc-rate-limit-by-cost` (draft) already covers the cost clause as its Rule**, citing Shopify, GitHub and Airbnb; its `lacks:` says "none recommends it". That card is the place to fix the cost half, not a new card.

**FAIL/PASS.** FAIL: `if requests_from_ip > 100: reject` counted after the handler ran, with an undocumented window. PASS: `limiter.consume(principal, estimated_cost)` before the work, and the response or docs state the window and the reset.

1. https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api (org: GitHub). Cost, not calls: "The GraphQL API assigns points to each query and limits the points that you can use within a specific amount of time." The budget names the window: "For users: 5,000 points per hour per user." The query's price is available before it runs: "You can also roughly calculate the point value of a query before you make the query", and after: "You can return the point value of a query by querying the `cost` field on the `rateLimit` object". The reset is explicit: `x-ratelimit-reset` is "The time at which the current rate limit window resets, in UTC epoch seconds." Backs P4 (cost and window/reset).

2. https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits (org: Shopify). The same model with a different unit: "Calls to the GraphQL Admin API are limited based on calculated query cost, which means you should consider the cost of requests over time rather than the number of requests." The window is a restore rate, and the Standard plan's figure is "100 points/second": "your quota refills continuously, so short bursts are fine as long as your average cost stays under the restore rate." A single query has its own ceiling: "A single query may not exceed a cost of 1,000 points". Backs P4 (cost and window/reset).

3. https://www.ietf.org/archive/id/draft-ietf-httpapi-ratelimit-headers-10.html (org: IETF, **draft, not counted**). It defines exactly the window/reset vocabulary: "This document defines the RateLimit-Policy and RateLimit HTTP header fields for servers to advertise their quota policies and the current service limits". The window is `w`: "The 'w' parameter value conveys a time window applicable to the quota". The reset is `t`: "The 't' parameter indicates the number of seconds until additional quota associated with the quota policy is made available." The unit can be bytes: `qu` allows `content-bytes`, and "Quotas are allocated per partition key." It is an Internet-Draft: "It is inappropriate to use Internet-Drafts as reference material or to cite them other than as 'work in progress.'" So it does not count toward the three; it is the shape a resolver should use, not a practice in force.

**Verdict.** Before this pass the cost clause had OWASP and Cloudflare; new: GitHub and Shopify, both documenting cost-based limits. **4 organisations for cost (OWASP, Cloudflare, GitHub, Shopify).** The window/reset clause had Microsoft (sliding `renewal-period`) and AWS (token bucket); new: GitHub (`x-ratelimit-reset`) and Shopify (restore rate), so **4 organisations (Microsoft, AWS, GitHub, Shopify)**, with the IETF draft excluded. Only GitHub names an explicit reset timestamp; Shopify and AWS publish a restore rate and Microsoft a window length, so "reset" is the weakest word in the clause. Confidence high. **Duplicate warning:** the cost clause is already the Rule of `svc-rate-limit-by-cost`; rule 8 says the two cards must merge or one must drop the clause.

## P5 (I5): cap decompressed output size

**Candidate Rule.** Cap the bytes a decoder may produce before it allocates them, and set the cap on the output, not on the compressed input.

**Level.** service. **Tool gate.** no linter rule. Config gates exist: Apache `DeflateInflateLimitRequestBody` plus `DeflateInflateRatioLimit`; ASP.NET Core `MaxRequestBodySize` / `[RequestSizeLimit]`.

**Existing card.** `svc-upload-validate-store` (stable) says "Count the decompressed size of archives" in Why; `svc-bound-client-controlled-sizes` (stable) caps body, string, array and page sizes. Missing: an output ceiling in the Rule, a compression-ratio check, and a query-language cost/depth bound. Neither card caps what a decoder produces.

**FAIL/PASS.** FAIL: `gunzip(body)` then `parse(body)`, with the body cap applied to the compressed bytes only. PASS: `zlib.gunzip(buf, { maxOutputLength: 1 << 20 })`, or `DeflateInflateLimitRequestBody 1048576`, or ASP.NET `MaxRequestBodySize` left on.

1. https://httpd.apache.org/docs/2.4/mod/mod_deflate.html (org: Apache HTTP Server). The directive is exactly this control: "The `DeflateInflateLimitRequestBody` directive specifies the maximum size of an inflated request body." The default is the finding: "None, but `LimitRequestBody` applies after deflation", and "A value of `0` means no limit is applied to the inflated body size". The ratio control is also documented: "The `DeflateInflateRatioLimit` directive specifies the maximum ratio of deflated to inflated size of an inflated request body", default 200, checked "as the body is streamed in". And the page warns why a compressed-size check is not enough: "don't trust the `Content-Length` header! ... not the byte count of the decompressed data stream." Backs P5.

2. https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/request-decompression?view=aspnetcore-10.0 (org: Microsoft). The middleware states the purpose and the mechanism: "In order to protect against zip bombs or decompression bombs: The maximum size of the decompressed request body is limited to the request body size limit enforced by the endpoint or server." The enforcement point is on the output: "If the number of bytes read from the decompressed request body stream exceeds the limit, an `InvalidOperationException` is thrown to prevent additional bytes from being read from the stream." The opt-out is called out: "Disabling the request body size limit poses a security risk in regards to uncontrolled resource consumption". Backs P5.

3. https://nodejs.org/api/zlib.html (org: Node.js), already cited in `sec-classes-I.md`. The convenience methods take `maxOutputLength`: "Limits output size when using convenience methods", default `buffer.kMaxLength`. The zip-file API has a separate `maxSize`: "Reject content declaring more than this many uncompressed bytes, before allocating anything", and `setMaxZipContentSize` calls it "a guard against zip bombs: an archive whose central directory declares a member larger than this is rejected before allocating memory for it." The existing file's quote about "before allocating anything" belongs to `maxSize`, not `maxOutputLength`; both are caps, but on different APIs.

4. https://docs.python.org/3/library/tarfile.html (org: Python Software Foundation), already cited, partial: the extraction filters "will prevent the most dangerous security issues. However, it will not prevent all unintended or insecure behavior." It backs "inspect before extract", not a byte ceiling.

**Verdict.** Before this pass the output-ceiling clause had Node.js and a partial Python source. New: Apache and Microsoft, both with an explicit inflated-size ceiling and a documented default. **3 solid (Node.js, Apache, Microsoft) plus Python partial.** Confidence high for "cap the decompressed output"; medium for "also cap the ratio", which Apache alone states.

## P6 (I6): a poison message must not block the messages behind it

**Candidate Rule.** Bound the retries per message and isolate the failure, so a message that cannot be processed is dead-lettered without stopping the messages behind it.

**Level.** service. **Tool gate.** `svc-dlq` names a Terraform SQS `redrive_policy` with `maxReceiveCount` and a DLQ depth alarm (not re-opened). No linter.

**Existing card.** `svc-dlq` (stable) has the DLQ and replay as its Rule and the retry cap in Why. Missing: head-of-line isolation as a Rule, per-message or per-partition processing, and delayed retry rather than an immediate hot loop.

**FAIL/PASS.** FAIL: one shared queue, a handler that throws on a malformed message, and unbounded redelivery in front of the backlog. PASS: `maxReceiveCount`/`maxDeliveryAttempts` set, a DLQ with an alarm, and per-key, per-session or per-group consumption that moves on after the failure.

1. https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-sessions (org: Microsoft). Sessions are the isolation unit: "When multiple concurrent receivers pull from the queue, the messages belonging to a particular session are dispatched to the specific receiver that currently holds the lock for that session." The poison message leaves the path and the consumer continues: "Once exceeded, the message is moved to the dead-letter queue (DLQ), and the receiver continues receiving subsequent messages from the session." A retry without a bound loops: "Abandoning a message causes the same message to be served again by the next receive operation." Backs P6.

2. https://cloud.google.com/pubsub/docs/ordering (org: Google). It names head-of-line blocking and the remedy: "Unacknowledged messages for a given ordering key can potentially delay delivery of messages for other ordering keys, especially during server restarts or traffic changes." The advice: "If timely acknowledgment is not possible, consider using a dead-letter topic to prevent indefinite message holding." It also warns what a redelivery costs: "Redeliveries of a message trigger redelivery of all subsequent messages for that key, even acknowledged ones." Backs P6.

3. https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html (org: AWS). The blocking is explicit and per group: "No additional messages from the same message group ID are returned until the first message is deleted or becomes visible again." The isolation is the group: "FIFO queues allow parallel processing of messages across different message group IDs." The example repeats it: "Until the consumer deletes these messages or the visibility timeout expires, no additional messages from Group A are received." AWS states the blocking, not the DLQ remedy on this page; the retry cap and DLQ come from `svc-dlq`. Backs P6.

**Verdict.** Before this pass the isolation clause had 0 clear organisations (RabbitMQ's delayed retry was the nearest). New: Microsoft, Google and AWS, each naming the blocking unit and the way around it. **3 organisations (Microsoft, Google, AWS) for head-of-line isolation.** Confidence medium-high: all three describe the failure and the isolation unit, but only Microsoft and Google also tie it to a DLQ in the same sentence. How a failed message stops blocking the rest is not fully answered by AWS's page.

## P7 (I7): reject messages outside a timestamp window

**Candidate Rule.** Reject an inbound webhook or signed message whose creation time is outside a short tolerance, and refuse one whose signature has expired.

**Level.** service. **Tool gate.** none found.

**Existing card.** `svc-idempotency-key` (stable) covers a retryable write with a caller key. Missing: a timestamp tolerance on inbound messages, deduplication by event id, and an ordering or stale-event rule.

**FAIL/PASS.** FAIL: verify the HMAC, then apply the event, with no clock check and no `expires` check. PASS: reject if `abs(now - created) > tolerance`, reject when `now > expires`, and dedupe by the event id or nonce.

1. https://www.rfc-editor.org/rfc/rfc9421.html (org: IETF). The standard names both checks as verifier duties: "Enforcing a maximum signature age from the time of the `created` timestamp." And: "Rejecting signatures past the expiration time in the `expires` timestamp." The parameters are defined: `created` is "Creation time as a UNIX timestamp value of type Integer", `expires` is "Expiration time as a UNIX timestamp value of type Integer", `nonce` is "A random unique value generated for this signature as a String value." Section 7.2.2 explains why a signature alone is not enough: "it is possible for two different HTTP messages to validate against the same signature." Backs P7.

2. https://docs.svix.com/receiving/verifying-payloads/how-manual (org: Svix), already cited: "You should compare this timestamp against your system timestamp and make sure it's within your tolerance in order to prevent timestamp attacks." Not re-opened this pass.

3. https://docs.slack.dev/authentication/verifying-requests-from-slack/ (org: Slack), already cited: "we verify that the timestamp does not differ from local time by more than five minutes", and "It could be a replay attack, so let's ignore it." Not re-opened this pass.

**Verdict.** Before this pass the replay-window clause had Svix and Slack. New: IETF RFC 9421, a Standards Track document that makes the age and expiration checks part of verification. **3 organisations (Svix, Slack, IETF) for the timestamp window.** Confidence high for the clause, medium for any fixed number: RFC 9421 leaves the tolerance to the application, and Svix notes that a tight tolerance has a real false-negative cost for delayed deliveries. GitHub's webhook validation, already in the file, authenticates the sender but checks no clock, so it does not back this clause.

## P8 (I8): do not run untrusted PR code in a privileged CI workflow

**Candidate Rule.** Keep code from an unreviewed change out of any job that holds secrets or can deploy, and pin every action that runs in that job.

**Level.** codebase. **Tool gate.** OpenSSF Scorecard `Dangerous-Workflow` (Risk: Critical) is the matching check; `Pinned-Dependencies` and zizmor `unpinned-uses` cover the pin. The `Dangerous-Workflow` page was opened this pass: it "determines whether the project's GitHub Action workflows has dangerous code patterns", and it names "Untrusted Code Checkout" as `pull_request_target` or `workflow_run` "used in conjunction with an explicit pull request checkout". It adds no organisation for this clause because OpenSSF is already counted in I8. No linter was found that decides whether a branch is "reviewed".

**Existing card.** `code-workflow-supply-chain` (stable) has the SHA pin as its Rule; its Why already has least-privilege tokens, untrusted event data out of `run:`, and `pull_request_target` checkout. `code-dependency-pinning` (stable) covers lockfile hashes. Missing: the untrusted-code boundary as a Rule, and CI config under review as an explicit control.

**FAIL/PASS.** FAIL: `pull_request_target` with `actions/checkout` of the PR head, a write token or a deploy secret, and `run: echo "${{ github.event.pull_request.title }}"`. PASS: `pull_request` with a read-only token and no secrets, deploy isolated to a protected branch or protected runner, every `uses:` pinned to a 40-character SHA.

1. https://docs.gitlab.com/ci/pipelines/ (org: GitLab). The protected-runner rule is the practice: "Runners marked as protected can run jobs only on protected branches, preventing untrusted code from executing on the protected runner and preserving deployment keys and other credentials from being unintentionally accessed." The credential half travels with it: "Variables marked as protected are accessible to jobs that run in pipelines for protected branches." Backs P8.

2. https://docs.github.com/en/actions/reference/security/secure-use (org: GitHub), already cited by `code-workflow-supply-chain`: `pull_request_target` and untrusted checkout warnings, least-privilege `permissions`, and script injection. Not re-opened this pass. Backs P8.

3. https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html (org: OWASP), already cited: "Perform builds in appropriately isolated nodes", integrity checks on downloaded packages, and review of the CI definition before merge. Not re-opened this pass. Backs P8.

4. https://github.com/ossf/scorecard/blob/main/docs/checks.md (org: OpenSSF; **tool gate, not a new organisation for this clause**). Opened this pass to confirm the gate. `Dangerous-Workflow` is described as: "This check determines whether the project's GitHub Action workflows has dangerous code patterns." The first pattern is the clause: "Untrusted Code Checkout: This is the misuse of potentially dangerous triggers. This checks if a `pull_request_target` or `workflow_run` workflow trigger was used in conjunction with an explicit pull request checkout." It also states the limit of the gate: "This check does not detect whether untrusted code checkouts are used safely, for example, only on pull request that have been assigned a label." Backs P8 as a gate only; OpenSSF was already one of I8's organisations.

**Verdict.** Before this pass the defining clause had GitHub and OWASP. New: GitLab, with a documented protected-runner control that a reviewer can check in config. **3 organisations (GitHub, OWASP, GitLab) for "untrusted code must not run in a privileged workflow".** The tool gate is confirmed: Scorecard `Dangerous-Workflow` documents the exact pattern. Confidence medium-high. NIST SP 800-218 and the CISA/NSA CI/CD guidance remain UNFETCHED (PDF/403 as recorded in `sec-classes-I.md`); they would be the fourth and fifth if a text copy becomes reachable.

## P9 (new class): workload identity instead of long-lived cloud keys

**Candidate Rule.** Give CI jobs and services short-lived credentials from a federated identity: exchange the platform's OIDC token for cloud access, scope the trust policy to the workload, and keep no long-lived cloud key in a secret store.

**Level.** codebase (the workflow file and the cloud trust policy are repo config). A service-level variant applies to any workload that calls a cloud API; the same Rule with a service account or pod identity. **Tool gate.** none found for OIDC itself. `code-secret-scan` catches a committed cloud key but not a long-lived key pasted into a CI variable; `code-workflow-supply-chain` checks the `permissions` block and pins, not the credential source. A config check can assert `id-token: write` + `role-to-assume` (GitHub) or an `id_tokens:` block (GitLab) and no static `AWS_SECRET_ACCESS_KEY`.

**Existing card.** None. `code-secret-scan` (stable) revokes a leaked credential; `sys-secrets-and-errors` (stable) says to read secrets from the environment or a secrets manager, which still leaves a long-lived value; `code-workflow-supply-chain` (stable) limits the workflow token. Nothing says the cloud credential itself should be short-lived and federated.

**FAIL/PASS.** FAIL: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` stored as repository or CI secrets and exported into a deploy job. PASS: `permissions: id-token: write` and `role-to-assume` with a trust policy that pins the repo and ref, or a GitLab `id_tokens:` block with an `aud` the cloud verifies; no stored cloud key.

1. https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws (org: GitHub). The purpose is stated as replacing the long-lived secret: "OpenID Connect (OIDC) allows your GitHub Actions workflows to access resources in Amazon Web Services (AWS), without needing to store the AWS credentials as long-lived GitHub secrets." The exchanged credential is short-lived: the OIDC token "is then used to authenticate with external services using a short-lived access token." The trust policy is the control, and it is mandatory: "you must define at least one condition, so that untrusted repositories can't request access tokens for your cloud resources", with `token.actions.githubusercontent.com:sub` pinned to the repo and branch or environment. Backs P9.

2. https://cloud.google.com/iam/docs/workload-identity-federation (org: Google). The alternative is named for its risk: "Using Workload Identity Federation, you can provide on-premises or multicloud workloads with access to Google Cloud resources by using federated identities instead of a service account key." And: "Workload Identity Federation eliminates the maintenance and security burden associated with service account keys." The result is short-lived: "The token exchange flow returns a federated access token", and "a short-lived OAuth 2.0 access token". The trust is narrowed by an attribute condition: "You can use an attribute condition to restrict which identities can authenticate using your workload identity pool." Backs P9.

3. https://docs.gitlab.com/ci/secrets/id_token_authentication/ (org: GitLab). The job gets a platform-minted JWT: "ID tokens are JSON web tokens (JWT) generated by GitLab CI/CD. CI/CD jobs can use ID tokens for OIDC authentication with third-party services". The lifetime is short by default: "The expiry time for the token is set to the job's timeout if specified, or 5 minutes if no timeout is specified." The trust policy is scoped to the workload: "When you write a trust policy, include stable, unique identifiers such as `namespace_id` and `project_id` alongside path-based claims like `sub`". Backs P9.

**Verdict.** **3 organisations (GitHub, Google, GitLab), each documenting the same practice**: no stored cloud key, a platform-issued OIDC token exchanged for a short-lived credential, and a trust policy that pins the workload. Confidence high for the Rule. The card should name the trust-policy condition as part of the PASS, not only the token exchange: all three warn that an unconstrained trust policy lets another repository or project assume the role.

## Counter-evidence and limits

- **A tenant-prefixed key is necessary, not sufficient.** Microsoft says "A key prefix or hash slot isn't an authorization or tenant-isolation boundary"; Redis says "Redis OSS logical databases are not a security boundary"; and Cloudflare shows that the key carries the tenant only if the caller puts it there (`ctx.props`), so a gateway that authenticates with a header not in the key still shares entries. The card's PASS should show the prefix and the authorization check, not the prefix alone.
- **Atlassian's XML export is the counter-example to naive export scoping.** The same page that says HTML and PDF exports contain "only the pages you have permission to view" says XML exports contain "all the pages in the space, including those you don't have permission to view." The Rule must be about the export path the code implements, and the card should list the format in the FAIL.
- **Apache's inflated-body cap is off by default.** `DeflateInflateLimitRequestBody` defaults to "None, but `LimitRequestBody` applies after deflation"; setting it to `0` removes the limit. ASP.NET Core's cap is the server's request-body limit, shared with the compressed body, and `[DisableRequestSizeLimit]` removes it. So the practice is "set and keep the ceiling", not "the platform does it".
- **Microsoft's Power BI page covers the export moment, not the file.** It says a user with RLS "can only export data you're authorized to see", but the page does not claim the exported CSV/XLSX keeps RLS after download; it only says sensitivity labels stay attached to protected files. A card should not claim the file is protected.
- **The IETF ratelimit draft is not a practice.** It says of itself: "It is inappropriate to use Internet-Drafts as reference material or to cite them other than as 'work in progress.'" It is listed for the shape of `w`/`t`/`pk`, excluded from the count.
- **A rate limit is a target, not an invariant.** The existing file already records AWS ("best-effort basis ... targets rather than guaranteed request ceilings") and Microsoft ("rate limiting is never completely accurate"). The P4 Rule should ask for a cost-aware limiter with a published window, not an exact accounting guarantee.
- **RFC 9421 leaves the tolerance to the application.** The standard requires a check, not a number. Svix's own page notes that a tolerance can reject a genuinely delayed delivery, so the card cannot pick a number for the reviewer. Slack's five minutes is one product's choice.
- **GitLab's protected runner is not the whole boundary.** The same docs warn that a project member can run a fork's pipeline in the parent project "where it uses the fork's configuration and the parent's available resources and unprotected variables", and that masking a variable is not a guarantee. The PASS must show the untrusted ref cannot reach the protected runner *and* the protected variables.
- **The P9 trust policy is the weak point in practice.** GitHub's own prerequisite says the condition is mandatory, and GitLab documents that a new project can inherit an old project's trust policy when the `sub` claim is path-based ("GitLab blocks ID token issuance when the configured `sub` claim contains a `project_path` ... previously used by a different project"). A token exchange with `repo:*` or `sub` unset passes a superficial check and fails the Rule.
- **NIST and CISA are still missing for P8.** The SSDF is a PDF and the CISA guidance returned 404/403 in the earlier pass. They are not counted, and the P8 card must not claim them.

## Also read, no rule

- https://www.postgresql.org/docs/current/routine-vacuuming.html (org: PostgreSQL), already cited for I1. It backs "a delete leaves the row version behind", not the ORM default filter.
- https://docs.jboss.org/hibernate/orm/6.5/javadocs/org/hibernate/annotations/SoftDelete.html (org: Hibernate). The annotation reference describes `@SoftDelete`, its column and its strategy, but not the query default; the User Guide row above is the stronger of the two.
- https://redis.io/docs/latest/develop/using-commands/keyspace/ (org: Redis). The generic naming page: "Redis doesn't support namespaces or other categories for keys, so you must take care to avoid name collisions", and it recommends the colon convention. It never says "tenant", so it is superseded by the Redis architecture blog in P2.
- https://www.fastly.com/documentation/guides/full-site-delivery/caching/manipulating-the-cache-key (org: Fastly). The general rule: "If your origin uses special values (e.g., request headers) to select content for users or to otherwise direct requests to appropriate security domains, consider including those values in your cache key or Vary header. Doing so will prevent you from accidentally caching content across security domains and could prevent malicious attackers from poisoning your cache." It says "security domains", not tenant; not counted, but it is the strongest phrasing of why the discriminator belongs in the key.
- https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/understanding-the-cache-key.html (org: AWS). Another general rule: "When a value in the viewer request determines the response that your origin returns, you should include that value in the cache key." Generic edge caching, no tenant; not counted. It also supplies the counterpoint that over-keying duplicates objects and lowers the hit ratio.
- https://typeorm.io/entities (org: TypeORM). Fetch returned no body, so it is excluded; the repository's `@DeleteDateColumn` docs would be a candidate fourth org for P1 if reachable.
- https://www.standardwebhooks.com/ (org: Standard Webhooks project). Not fetched this pass. It is the obvious fourth source for P7's tolerance, but the RFC already fills the third slot.
- https://about.gitlab.com/resources/well-architected/best-practices/principles/isolate-execution-by-trust/ (org: GitLab). Stronger wording than the docs page for P8 ("Run untrusted code on different infrastructure from jobs that hold secrets or can reach deployment systems"), but `about.gitlab.com` is not in `tools/orgs.py`; the `docs.gitlab.com` page is used instead so the card validates.
- https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/api-management (org: Microsoft). Says "ensure that you include the tenant identifier in the cache key", but it is the same organisation as the cache-redis row and adds nothing to the count.
- https://github.com/ossf/scorecard/blob/main/docs/checks.md (org: OpenSSF). The `Dangerous-Workflow` check is the P8 gate and was opened; it is listed in the P8 rows, not here.
- https://www.cisa.gov/resources-tools/resources/defending-cicd-environments (org: CISA). 404 in the earlier pass; the alert page is an announcement. Still not a source.
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf (org: NIST). `application/pdf`; the fetch tool rejects it. Still UNFETCHED for practice text.

## Per-clause organisation count

| Clause | Orgs before (for this clause) | New orgs found | Total | Confidence |
|---|---|---|---|---|
| P1 filter deleted rows by default | 1 (Microsoft) | Laravel, Sequelize | **3 solid** (+ Hibernate, Rails partial) | high |
| P2 tenant in cache key | 1 (OWASP) | Microsoft, Redis, Cloudflare | **4 solid** | high |
| P2 tenant in logs/analytics | 1 (OWASP) | AWS, Google | **3 solid** | high |
| P3 export scoped to the reader | 1 (OWASP) | Atlassian, Microsoft | **3 solid** | high, with a format caveat |
| P4 charge by cost | 2 (OWASP, Cloudflare) | GitHub, Shopify | **4 solid**, but duplicates `svc-rate-limit-by-cost` | high |
| P4 name the window/reset | 2 (Microsoft, AWS) | GitHub, Shopify | **4 solid** (IETF draft excluded) | high |
| P5 cap decompressed output | 2 (Node.js, Python partial) | Apache, Microsoft | **3 solid + Python partial** | high |
| P6 poison message must not block the rest | 0 | Microsoft, Google, AWS | **3 solid** | medium-high |
| P7 reject outside timestamp window | 2 (Svix, Slack) | IETF RFC 9421 | **3 solid** | high |
| P8 untrusted PR code in privileged CI | 2 (GitHub, OWASP) | GitLab | **3 solid** | medium-high |
| P9 workload identity (new) | 0 | GitHub, Google, GitLab | **3 solid** | high |

## What to do next

- **P1:** new `svc-soft-delete-default` is ready on three orgs. FAIL is a read path without the filter; PASS is the framework's built-in soft delete plus an explicit, audited bypass.
- **P2:** both halves are ready. The cache key has OWASP, Microsoft, Redis and Cloudflare; the log store has OWASP, AWS and Google. Keep the caveat from Microsoft, Redis and Cloudflare that a prefix is not an authorization boundary in the Counterpoint.
- **P3:** new `svc-export-scope` is ready on OWASP, Atlassian and Microsoft. Name the export format in the FAIL; the XML counter-example is the reason.
- **P4:** do not add a cost card. Extend `svc-rate-limit-by-cost` with the window/reset clause and the pre-work check, or promote that draft and add the window to `svc-rate-limit-quota`. That draft's `lacks: evidence` note should be re-checked: it says "none recommends it", but Cloudflare recommends budgeting query complexity and OWASP recommends per-operation limits, so the evidence bar may already be met.
- **P5:** add `svc-decompression-cap` for the output ceiling (Node.js, Apache, Microsoft) and keep the query-amplification half (GraphQL, OWASP) in Why until a third org is found.
- **P6:** add `svc-poison-message-isolation` for head-of-line blocking (Microsoft, Google, AWS); keep `svc-dlq` for the retry cap and replay, and cross-link the two.
- **P7:** add `svc-webhook-replay-window` for the timestamp tolerance (Svix, Slack, IETF RFC 9421); `svc-idempotency-key` stays for the caller-supplied write key.
- **P8:** either promote the untrusted-code boundary from the Why of `code-workflow-supply-chain` to a Rule (GitHub, OWASP, GitLab), or add `code-untrusted-ci-step` and keep the pin in the existing card. Cite the GitLab docs page, not `about.gitlab.com`, until the latter is mapped.
- **P9:** add `code-workload-identity` at codebase level. Its PASS needs three parts: the platform token permission, the exchange (`role-to-assume` or `id_tokens`), and a trust policy that pins the workload's `sub`/`aud`. Without the third it is a false PASS.

## `tools/orgs.py` prefixes to add before a card cites these pages

| Prefix | Org | Used by |
|---|---|---|
| `sequelize.org` | Sequelize | P1 |
| `httpd.apache.org` | apache | P5 |
| `docs.jboss.org` | Hibernate / Red Hat | P1 partial (only if the User Guide is cited) |

Everything else is already mapped: `laravel.com`, `redis.io`, `learn.microsoft.com`, `docs.aws.amazon.com`, `docs.cloud.google.com` (via `cloud.google.com`), `confluence.atlassian.com` (via `atlassian.com`), `docs.github.com`, `shopify.dev`, `docs.gitlab.com`, `rfc-editor.org`, `nodejs.org`, `docs.python.org`, `cheatsheetseries.owasp.org`. `about.gitlab.com` is not mapped; use `docs.gitlab.com` instead. `www.ietf.org/archive/id/...` is also not mapped as a prefix (`datatracker.ietf.org` and `rfc-editor.org` are), so cite the draft at `datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/` if it is ever quoted in a card.

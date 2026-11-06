# Security classes I: data lifecycle, messaging, supply chain

Checked 2026-11-05/06 for the eight Cloudflare security-audit classes I1 to I8. Every page below was fetched and read; quotes are verbatim, 1-2 per row. Organisation counting follows `docs/PROMOTION.md`. About 30 pages were fetched, so the pass stops at the brief's cap. No linter rule page was opened in this pass: tool gates already named by an existing card are marked "(not re-opened)".

New URL prefixes this file needs in `tools/orgs.py` before a card can cite them: `docs.svix.com`/`svix.com` (Svix), `graphql.org` (GraphQL Foundation), `rabbitmq.com` (RabbitMQ, Broadcom/Tanzu). Everything else is already mapped (`postgresql.org`, `elastic.co`, `docs.stripe.com`, `docs.slack.dev`, `nodejs.org`, `cloud.google.com`, `learn.microsoft.com`, `docs.aws.amazon.com`, `cheatsheetseries.owasp.org`).

## I1. Soft-delete and tombstone bypass

**Candidate Rule.** Make every read path exclude deleted records: filter tombstones by default, purge them from every derived copy, and expire the version or row that still holds them.

**Level.** service. **Tool gate.** none found.

**Existing card.** None. `fn-object-level-authz` authorises one object, not a deleted one; no card mentions soft delete, delete markers or tombstones.

**FAIL/PASS.** FAIL: `SELECT * FROM doc WHERE id = ?` with no `deleted_at IS NULL`, and a cache/index copy never invalidated. PASS: the shared query helper adds `deleted_at IS NULL`, a purge job clears the index and cache, and noncurrent object versions expire.

1. https://learn.microsoft.com/en-us/ef/core/querying/filters (org: Microsoft). Soft delete is a documented pattern whose default is a global query filter: "Soft deletion allows rows to be undeleted if needed, or to preserve an audit trail where deleted rows are still accessible. Global query filters can be used to filter out soft-deleted rows by default". It also names the bypass: "Filters may be disabled for individual LINQ queries by using the IgnoreQueryFilters operator". The filter must be on every read path, or the bypass is one call away. Backs I1.
2. https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html (org: OWASP). Deletion must cover the copies, not the source row: "Apply a documented retention and deletion policy to every place tenant data lives: active stores, caches, object versions, replicas, exports, backups, and encryption keys." Do's list repeats "Apply and verify the documented retention and deletion policy during offboarding." Backs I1.
3. https://www.postgresql.org/docs/current/routine-vacuuming.html (org: PostgreSQL). A delete leaves the row version behind: "In PostgreSQL, an UPDATE or DELETE of a row does not immediately remove the old version of the row." The stated remedy is routine vacuuming, and autovacuum is "optional but highly recommended"; the page warns "It is unwise to disable the daemon completely". Backs I1.
4. https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html (org: AWS). A delete in a versioned bucket only adds a marker: "Because the object is in a versioning-enabled bucket, the object is not deleted. But the delete marker makes Amazon S3 behave as if the object is deleted." The old bytes stay reachable: "The only way to list delete markers (and other versions of an object) is by using a ListObjectVersions request." The lifecycle page supplies the practice: "Expiration actions – These actions define when objects expire. Amazon S3 deletes expired objects on your behalf" (https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html). Backs I1.

**Verdict.** 4 organisations for the combined rule, but the clauses split: "filter deleted rows by default" has Microsoft only; "purge every derived copy" has OWASP only; "remove the residue physically" has PostgreSQL and AWS. Confidence medium-high on the whole rule, low on any single clause reaching three.

## I2. Derived copies and access-control drift

**Candidate Rule.** Carry the tenant and access filter into every derived store: put the tenant id in the query, in the cache key, and in the role that guards the search index.

**Level.** service. **Tool gate.** none found.

**Existing card.** None. Nothing mentions cache keys, search-index roles or a tenant filter in derived stores.

**FAIL/PASS.** FAIL: `cache.set("user:"+id, row)` and a search index with one shared role. PASS: `cache.set(f"t{tenant}:user:{id}", row)`, the query carries `tenant_id = ?`, and the index role carries a document-level query.

1. https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html (org: OWASP). Cache keys must carry the tenant: "Include the tenant identifier in every cache key whose value or authorization varies by tenant." The sheet also refuses to let the key replace authorisation: "Authorize the request before reading a protected cached value; cache-key separation does not replace authorization." Audit data follows the same rule: "A centralized audit store is acceptable when read access enforces tenant scope." Backs I2.
2. https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data (org: Microsoft). Row-level security only works if the filter travels with the query: "When you use row-level security, you need to ensure that the user's identity and tenant identity are propagated through the application and into the data store with each query." The EF page states the default: the tenant filter "provides strong tenant isolation for your queries by default, removing the need to think of filtering for the tenant in each and every query" (https://learn.microsoft.com/en-us/ef/core/querying/filters). Backs I2.
3. https://www.elastic.co/guide/en/elasticsearch/reference/current/document-level-security.html (org: Elastic). A search index needs its own filter because the source ACL does not reach it: "Document level security restricts the documents that users have read access to." The default is open, and one omission removes the control: "Omitting the query parameter entirely disables document level security for the respective indices permission entry." Multiple roles combined grant the union, so a broad role defeats a narrow one. Backs I2.

**Verdict.** 3 organisations for the whole rule. Per clause: "tenant filter in the query" has Microsoft plus Elastic's index-level query (2, different layers); "tenant in cache keys" has OWASP only; "logs/analytics store" has OWASP only. Confidence medium-high on the rule, not enough for each clause.

## I3. Export, backup and restore scope

**Candidate Rule.** Scope an export, backup or restore to the principal and tenant that may read it, and re-apply current access and retention rules after a restore.

**Level.** service. **Tool gate.** none found.

**Existing card.** None. `fn-object-level-authz` covers a single object fetch, not a bulk export or a restore that brings back other tenants' rows.

**FAIL/PASS.** FAIL: `GET /export` streams the whole table; a shared snapshot is restored over live data to recover one tenant. PASS: the export is filtered by the caller's tenant, and a single-tenant restore lands in a separate resource and re-applies current ACLs.

1. https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html (org: OWASP). A shared backup crosses tenants: "A shared backup can contain data from several tenants. For a single-tenant recovery from a shared database, restore into a separate resource and selectively recover the target tenant's data." Restore must not revive old access: "Reapply current access and retention rules; a backup can contain old memberships or data that should no longer be accessible." It gives a concrete test: "Test a backup with two tenants: recover one tenant, verify the other tenant's records and objects are absent". Backs I3.
2. https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data (org: Microsoft). Same rule from the platform side: "In a shared database, restoring a single tenant might require you to restore the database to a separate resource and selectively recover that tenant's data." It also ties backup and restore to the isolation choice in its key considerations. Backs I3.
3. https://cloud.google.com/architecture/dr-scenarios-planning-guide (org: Google). Recovered data keeps production's controls: "Treat recovered data like production data" and "the same permissions, encryption, and audit requirements should all apply". Restore authority must be known and auditable: "Know where your backups are located and who is authorized to restore data." The plan must be tested: "Test your plan regularly". Backs I3.

**Verdict.** 3 organisations for the whole rule. Per clause: "restore into a separate resource" has OWASP and Microsoft (2); "re-apply current access/retention" has OWASP and Google (2); "export is scoped to the reader" has OWASP only. Confidence medium-high; a fourth org for the export-scope clause is missing.

## I4. Quota and rate-limit accounting gaps

**Candidate Rule.** Charge each request to the authenticated principal at its real cost, and make the window and reset explicit.

**Level.** service. **Tool gate.** none found.

**Existing card.** `svc-rate-limit-quota` (stable). Its Rule is a per-tenant quota, with a per-tenant concurrency cap and 429 vs 503 in Why. Missing: the limiter keyed to the principal or API key rather than the IP, an explicit reset window, charging cost (a GraphQL batch or expensive operation) rather than one call, and charging before the work runs.

**FAIL/PASS.** FAIL: `if requests_from_ip > 100: reject` counted after the handler ran, with an undocumented window. PASS: `limiter.consume(principal, cost)` before the work, window and reset published, 429 with `Retry-After`.

1. https://owasp.org/API-Security/editions/2023/en/0xa4-unrestricted-resource-consumption/ (org: OWASP). "Implement a limit on how often a client can interact with the API within a defined timeframe (rate limiting)." It is per principal and per operation: "Limit/throttle how many times or how often a single API client/user can execute a single operation". It also asks for a spend ceiling on paid backends: "Configure spending limits for all service providers/API integrations." Backs I4.
2. https://learn.microsoft.com/en-us/azure/api-management/rate-limit-policy (org: Microsoft). The limiter is per subscription and names its window: "The rate-limit policy prevents API usage spikes on a per subscription basis by limiting the call rate to a specified number per a specified time period." `renewal-period` is "the length in seconds of the sliding window", with a maximum of 300 seconds. Microsoft admits the count drifts: "rate limiting is never completely accurate". Backs I4.
3. https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html (org: AWS). The client key is explicit: "Per-client throttling limits are applied to clients that use API keys associated with your usage plan as client identifier." The accounting model is a token bucket: "a token counts for a request." Limits are targets, not guarantees: "Both throttles and quotas are applied on a best-effort basis and should be thought of as targets rather than guaranteed request ceilings." Backs I4.
4. https://developers.cloudflare.com/waf/rate-limiting-rules/best-practices/ (org: Cloudflare). The counting characteristic is chosen per principal: a rule can count by "Header (`x-api-key`)" and the guide says to "combine Path with the `x-api-key` header ... to set the maximum number of downloads that a specific client ... can make". It also charges complexity, not calls: "Limit the total amount of query complexity any given user is allowed to request", then "track complexity over time" and "block subsequent requests after reaching a complexity budget or limit". Backs I4.

**Verdict.** 4 organisations. "Key the limiter to the principal/key" has AWS, Cloudflare and Microsoft (subscription) = 3. "Charge cost, not call count" has OWASP and Cloudflare = 2. "Name the window/reset" has Microsoft and AWS = 2. Confidence high on principal keying, medium on the other clauses.

## I5. Decompression and amplification

**Candidate Rule.** Bound the output of every decoder and query expansion by bytes, depth or cost before allocating memory.

**Level.** service. **Tool gate.** none found.

**Existing card.** `svc-upload-validate-store` (stable) says "Count the decompressed size of archives" in Why, and `svc-bound-client-controlled-sizes` (stable) caps body, string, array and page sizes. Missing: a decompression ratio or output ceiling as the Rule, an XML/JSON entity-expansion rule, and a GraphQL/regex cost or depth rule. Neither card bounds work that is multiplied by a query language.

**FAIL/PASS.** FAIL: `gunzip(body)` then parse, with no cap. PASS: `zlib.gunzip(buf, { maxOutputLength: 1 << 20 })`, plus a query-depth and batch limit on the API.

1. https://nodejs.org/api/zlib.html (org: Node.js). A zip-bomb guard is built in and documented as such: `maxSize` will "Reject content declaring more than this many uncompressed bytes, before allocating anything." The setter says: "This is a guard against zip bombs: an archive whose central directory declares a member larger than this is rejected before allocating memory for it." The default ceiling is 268435456 bytes (256 MiB). Backs I5.
2. https://graphql.org/learn/security/ (org: GraphQL Foundation). Amplification is handled before execution: "it's a good idea to limit the maximum depth of fields that a single operation can have", and "there should also be an upper limit on the total number of queries allowed in a single batch." Cost can be a budget: "If the combination of fields included in a request exceeds a maximum allowable cost per request, you may choose to reject the request outright." Backs I5.
3. https://cheatsheetseries.owasp.org/cheatsheets/Denial_of_Service_Cheat_Sheet.html (org: OWASP). "Limit total request size" and "Limit file upload size and extensions" are the generic bounds; "Prevent input based resource allocation" names the class where input multiplies work. It also puts cheap checks first: "Using validation that is cheap in resources first". Backs I5.
4. https://docs.python.org/3/library/tarfile.html (org: Python Software Foundation). The warning is the rule: "Never extract archives from untrusted sources without prior inspection." The default filter helps but is not a proof: since 3.14 the default (`data`) "will prevent the most dangerous security issues. However, it will not prevent all unintended or insecure behavior." Backs I5.

**Verdict.** 4 organisations. "Bound decompressed/output size" has Node.js and Python (Python only partially: filters, no byte ceiling) = 2; "bound query amplification" has GraphQL and OWASP = 2. Confidence medium-high for the rule, medium per clause.

## I6. Poison messages and head-of-line blocking

**Candidate Rule.** Cap retries, dead-letter the failed message, and isolate it so one poison message cannot block the rest of the queue.

**Level.** service. **Tool gate.** The existing card names an SQS `redrive_policy` with `maxReceiveCount` and an alarm on DLQ depth (not re-opened this pass). No linter.

**Existing card.** `svc-dlq` (stable; the brief called it a draft). Its Rule is "Give every consumer queue a dead-letter queue and a way to replay its messages after the fix." The retry cap and alarm are in Why. Missing: a retry cap in the Rule, per-message or per-partition isolation (head-of-line), and delayed retry instead of an immediate hot loop.

**FAIL/PASS.** FAIL: one shared queue with unbounded redelivery. PASS: `maxReceiveCount`/`maxDeliveryAttempts` set, a DLQ with an alarm, and a per-tenant or per-type queue or partition.

1. https://learn.microsoft.com/en-us/azure/service-bus-messaging/service-bus-dead-letter-queues (org: Microsoft). The DLQ exists for the poison case: "The purpose of the dead-letter queue is to hold messages that can't be delivered to any receiver, or messages that couldn't be processed." The retry cap is on by default: "The default value is 10 ... When the delivery count exceeds the limit, the message is moved to the DLQ." Replay is a documented step: "Once you resolve the issue that caused a message to be dead-lettered, you can resubmit it ... to be reprocessed." It also warns the DLQ needs an owner: "There's no automatic cleanup of the DLQ." Backs I6.
2. https://cloud.google.com/pubsub/docs/dead-letter-topics (org: Google). Same shape: "After an approximately configured number of delivery attempts, Pub/Sub can forward the undeliverable message to a dead-letter topic." The bound is explicit: "Maximum number of delivery attempts ... Default value = 5 ... Maximum value = 100". The failed messages leave the hot path: "A separate subscription attached to the dead-letter topic can then receive these forwarded messages for analysis and offline debugging." Backs I6.
3. https://www.rabbitmq.com/docs/dlx (org: RabbitMQ/Broadcom). Dead-lettering is tied to a delivery limit: a message is dead-lettered when "returned more times to a quorum queue than the delivery-limit". It separates the two jobs: "Dead lettering remains the right tool for messages that cannot be processed at all, for example, those that exceed the delivery limit", while "Quorum queues natively support delayed retry ... the recommended approach for this use case." It also warns that a DLX is not a guarantee: dead-lettering can lose messages when the target queue is unavailable. Backs I6.

**Verdict.** 3 new organisations (Microsoft, Google, RabbitMQ), plus AWS, Netflix, Dropbox, Notion and Uber already in `svc-dlq`. The DLQ clause is strong. "Per-message isolation / head-of-line blocking" has 0 clear orgs; RabbitMQ's delayed retry and per-queue delivery limit are the nearest, so a new card on isolation still needs a source that names head-of-line blocking.

## I7. Stale, replayed or out-of-order message acceptance

**Candidate Rule.** Reject a message outside its replay window, deduplicate it by id, and process events in order or reject out-of-order ones.

**Level.** service. **Tool gate.** none found.

**Existing card.** `svc-idempotency-key` (stable) covers a retryable write with a caller key. Missing: a timestamp or nonce window on inbound webhooks, deduplication by event id, ordering (or stale-event) handling, and the rule that the receiver validates before doing work.

**FAIL/PASS.** FAIL: verify the signature only, then apply the event. PASS: reject if `abs(now - timestamp) > 300`, store the event id, and ignore an event older than the stored state.

1. https://docs.svix.com/receiving/verifying-payloads/how-manual (org: Svix). The timestamp is part of the check: "You should compare this timestamp against your system timestamp and make sure it's within your tolerance in order to prevent timestamp attacks." The id survives a resend: the message id "will be the same when the same webhook is being resent (e.g. due to a previous failure)", which makes it the dedupe key. Backs I7.
2. https://docs.slack.dev/authentication/verifying-requests-from-slack/ (org: Slack). A concrete window: "The signature depends on the timestamp to protect against replay attacks. ... we verify that the timestamp does not differ from local time by more than five minutes." The action is explicit: "It could be a replay attack, so let's ignore it." Backs I7.
3. https://docs.stripe.com/webhooks/signature (org: Stripe). Duplicates are expected: "Webhook endpoints might occasionally receive the same event more than once. Guard against duplicated event receipts by logging the event IDs you've processed, and then not processing already-logged events." Retries last three days, and the receiver must stop them: "When your endpoint receives an event you've already processed, skip it and return a 200 response to stop further retries." Ordering is called out when replaying a backlog: "Using `ending_before` with auto-pagination returns events in chronological order, so you process them in the order they were created." Backs I7.
4. https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries (org: GitHub). Authenticity, not replay: "To ensure that your server only processes webhook deliveries that were sent by GitHub and to ensure that the delivery was not tampered with, you should validate the webhook signature before processing the delivery further." It adds constant-time comparison. Backs the authenticity half of I7, not the window.

**Verdict.** 3 organisations for the whole rule (Svix, Slack, Stripe). Per clause: "replay window" has Svix and Slack only = 2, short of three; "deduplicate by id" has Svix and Stripe = 2, plus `svc-idempotency-key` for a caller key. Confidence medium; the class still needs a third org for the timestamp window (Twilio, RFC 9421 or Standard Webhooks were not fetched).

## I8. Untrusted code in a privileged CI workflow and unpinned build inputs

**Candidate Rule.** Keep untrusted code out of privileged workflows and pin every build input by immutable hash.

**Level.** codebase. **Tool gate.** `code-workflow-supply-chain` already names zizmor `unpinned-uses` and OpenSSF Scorecard `Pinned-Dependencies`; neither rule page was re-opened in this pass.

**Existing card.** `code-workflow-supply-chain` (stable) has the SHA pin as its Rule and, in Why, least-privilege tokens, untrusted event data out of `run:` and out of `pull_request_target` checkouts, and provenance. `code-dependency-pinning` (stable) covers lockfiles with hashes. Missing: the new clause is composed of parts already in Why, not a Rule. There is no card for poisoned build artifacts or caches crossing a workflow boundary, or for keeping the CI config itself under review.

**FAIL/PASS.** FAIL: `pull_request_target` with a checkout of the PR head and `run: echo "${{ github.event.pull_request.title }}"`. PASS: `pull_request` with a read-only token and no secrets, `uses: org/action@<40-char-sha>`, no event text in `run:`.

1. https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html (org: OWASP). Pinning includes integrity: "Version pinning should be performed ... and the integrity of any package the system downloads should be validated by comparing its hash or checksum to a known good hash of the pinned package." Builds are isolated: "Perform builds in appropriately isolated nodes". The pipeline definition is guarded: if the CI file is stored with the code, "it is imperative that the file is reviewed before any merge request is approved". Credentials are not shared across pipelines. Backs I8.
2. https://learn.microsoft.com/en-us/azure/devops/organizations/security/security-best-practices?view=azure-devops (org: Microsoft). Least privilege at the pipeline boundary: "Limit access by scoping your Azure Resource Manager service connections to specific resources and groups. Don't grant broad contributor rights across the entire Azure subscription." Environments are separated: "Segment environments: Use separate Azure accounts for different environments". Long-lived tokens are replaced: "Replace your PATs with Microsoft Entra tokens". Backs the privilege half of I8.
3. https://docs.github.com/en/actions/reference/security/secure-use (org: GitHub), already cited by `code-workflow-supply-chain` for SHA pinning, `pull_request_target`, script injection and least privilege. It backs the untrusted-code half of I8; not re-opened in this pass.
4. https://github.com/ossf/scorecard/blob/main/docs/checks.md (org: OpenSSF), already cited by the same card for the `Pinned-Dependencies` check. Backs the pin half; not re-opened in this pass.

**Verdict.** 4 organisations for the combined rule. The specific new clause, "untrusted code must not run in a privileged workflow", has GitHub and OWASP = 2. NIST SP 800-218 and the CISA/NSA CI/CD sheet would be the obvious third and fourth, but both were UNFETCHED (see below), so they are excluded. Confidence medium; do not promote a new card on 2 orgs for its defining clause.

## Counter-evidence and limits

- AWS API Gateway says throttles and quotas are "applied on a best-effort basis and should be thought of as targets rather than guaranteed request ceilings", and Microsoft APIM says "rate limiting is never completely accurate". That weakens any rule that claims an exact accounting invariant; the rule should ask for a principal-keyed, cost-aware limiter and a published window, not for an exact count.
- Elastic's document-level security is off by omission and roles combine as a union, so a narrow role is defeated by a broad one. That supports the drift claim but also warns that a config check can pass while the effective access is wider.
- OWASP says "cache-key separation does not replace authorization", which limits I2: a tenant-scoped key is necessary, not sufficient.
- RabbitMQ says dead-lettering "can fail" and messages can be lost without publisher confirms. A DLQ is not a delivery guarantee; I6's Rule should not claim one.
- Svix's own example "may fail verification due to the timestamp being old": a tolerance is a product decision with a real false-negative cost (retried or delayed deliveries), so a reviewer cannot pick a number blindly.
- ICO right-to-erasure guidance, which the brief names as a regulator source for I1/I3, returned HTTP 403 on three attempts and is excluded. The GDPR-erasure clause therefore rests on OWASP's deletion policy, not on a regulator.

## Also read, no rule

- https://docs.aws.amazon.com/whitepapers/latest/saas-tenant-isolation-strategies/saas-tenant-isolation-strategies.html and https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/tenant-isolation.html (org: AWS). Both redirect to a short introduction that says isolation matters; neither states a checkable practice, so neither backs a Rule.
- https://cheatsheetseries.owasp.org/cheatsheets/User_Privacy_Protection_Cheat_Sheet.html (org: OWASP). Covers cryptography, HSTS, panic modes and sessions; no deletion or soft-delete practice.
- https://learn.microsoft.com/en-us/compliance/assurance/assurance-data-retention-deletion-and-destruction-overview (org: Microsoft). Describes retention periods (30/90/180 days) and that expired data is "rendered commercially unrecoverable"; no code or config practice.
- https://csrc.nist.gov/pubs/sp/800/218/final (org: NIST). Landing page only: the abstract calls the SSDF "a core set of high-level secure software development practices" but states none. UNFETCHED for practice text: the PDF (https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf) is `application/pdf` and the fetch tool rejected it.
- https://www.cisa.gov/resources-tools/resources/defending-cicd-environments (org: CISA). 404. The alert at https://www.cisa.gov/news-events/alerts/2023/06/28/cisa-and-nsa-release-joint-guidance-defending-continuous-integrationcontinuous-delivery-cicd is an announcement, not the guidance. UNFETCHED: the CSI PDF at media.defense.gov returned 403. Search snippets showed the mitigation list (pin/sign configuration, 2PR, least privilege), but snippets are not citable.
- UNFETCHED, 404: https://cloud.google.com/bigquery/docs/row-level-security (Google, would back I2); https://learn.microsoft.com/en-us/dotnet/standard/data/xml/xml-security-considerations (Microsoft, would back I5); https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/caching (Microsoft, would back I2).
- https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ (org: ICO). UNFETCHED, 403 on three attempts. Excluded, including the "put the backup data beyond use" line that search results attributed to it.

## Per-claim organisation count

| Class | Orgs behind the whole rule | Weakest clause (orgs) | Confidence |
|---|---|---|---|
| I1 soft delete | 4 (Microsoft, OWASP, PostgreSQL, AWS) | read-path filter (1); derived copies (1) | medium-high |
| I2 derived copies | 3 (OWASP, Microsoft, Elastic) | cache key (1); logs (1) | medium-high |
| I3 export/backup/restore | 3 (OWASP, Microsoft, Google) | export scope (1); re-apply ACLs (2) | medium-high |
| I4 quota accounting | 4 (OWASP, Microsoft, AWS, Cloudflare) | cost-based charge (2); window (2) | high on keying |
| I5 decompression/amplification | 4 (Node.js, GraphQL Foundation, OWASP, PSF) | output ceiling (2); query bound (2) | medium-high |
| I6 poison messages | 3 new + 5 existing (Microsoft, Google, RabbitMQ; AWS, Netflix, Dropbox, Notion, Uber) | isolation/head-of-line (0-1) | high on DLQ, low on isolation |
| I7 replay/ordering | 3 (Svix, Slack, Stripe) | replay window (2); dedupe (2) | medium |
| I8 privileged CI | 4 (OWASP, Microsoft, GitHub, OpenSSF) | untrusted code in privileged workflow (2) | medium |

## Answer to "what is missing" per class

- I1: no card. A new `svc-soft-delete-scope` would need a third org for "every read path filters tombstones" and a second for "purge every derived copy".
- I2: no card. Closest is `fn-object-level-authz`; a new `svc-derived-store-tenant-scope` needs a second org for cache keys and a second for the audit store.
- I3: no card. A new `svc-export-restore-scope` needs a second org for export scoping.
- I4: `svc-rate-limit-quota` exists; extend its Rule with principal keying, cost, window and a pre-work check, or add `svc-quota-accounting` for the clauses it does not state.
- I5: `svc-upload-validate-store` (zip-bomb line in Why) and `svc-bound-client-controlled-sizes` exist; add `svc-decompression-and-query-amplification` for the output/ratio and depth/complexity bounds.
- I6: `svc-dlq` exists; a new `svc-poison-message-isolation` for head-of-line blocking still has no source that names the practice.
- I7: `svc-idempotency-key` covers the write key; add `svc-webhook-replay-window` for timestamp tolerance and dedupe, but it needs a third org for the window.
- I8: `code-workflow-supply-chain` covers the pin and the untrusted-input warnings in Why; either promote those to the Rule (GitHub + OWASP), or add `code-untrusted-build-step` once NIST or CISA is fetched.

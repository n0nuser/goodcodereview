# Writer U evidence: data, messaging and supply-chain security

Checked 2026-11-06. Every URL below was fetched in this session and the quote was read on the page. Format: `card-id | URL | org | "verbatim quote" | clause it backs`.

## svc-soft-delete-default

svc-soft-delete-default | https://learn.microsoft.com/en-us/ef/core/querying/filters | Microsoft | "Global query filters can be used to filter out soft-deleted rows by default, while still allowing you to access them in specific places by disabling the filter for a specific query." | filter deleted rows by default; explicit opt-in
svc-soft-delete-default | https://learn.microsoft.com/en-us/ef/core/querying/filters | Microsoft | "Filters may be disabled for individual LINQ queries by using the IgnoreQueryFilters operator" | the bypass is an explicit call
svc-soft-delete-default | https://laravel.com/docs/12.x/eloquent | Laravel | "When querying a model that uses soft deletes, the soft deleted models will automatically be excluded from all query results." | filter deleted rows by default
svc-soft-delete-default | https://laravel.com/docs/12.x/eloquent | Laravel | "you may force soft deleted models to be included in a query's results by calling the withTrashed method" | explicit opt-in
svc-soft-delete-default | https://sequelize.org/docs/v6/core-concepts/paranoid/ | Sequelize | "Every query performed by Sequelize will automatically ignore soft-deleted records (except raw queries, of course)." | filter deleted rows by default
svc-soft-delete-default | https://sequelize.org/docs/v6/core-concepts/paranoid/ | Sequelize | "If you really want to let the query see the soft-deleted records, you can pass the paranoid: false option to the query method." | explicit opt-in
svc-soft-delete-default | https://www.postgresql.org/docs/current/routine-vacuuming.html | PostgreSQL | "In PostgreSQL, an UPDATE or DELETE of a row does not immediately remove the old version of the row." | the row survives the delete
svc-soft-delete-default | https://www.postgresql.org/docs/current/routine-vacuuming.html | PostgreSQL | "It is unwise to disable the daemon completely" | vacuum removes the residue
svc-soft-delete-default | https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html | AWS | "Because the object is in a versioning-enabled bucket, the object is not deleted. But the delete marker makes Amazon S3 behave as if the object is deleted." | a delete leaves the old bytes
svc-soft-delete-default | https://docs.aws.amazon.com/AmazonS3/latest/userguide/DeleteMarker.html | AWS | "The only way to list delete markers (and other versions of an object) is by using a ListObjectVersions request." | versions hold the old copy
svc-soft-delete-default | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "Apply a documented retention and deletion policy to every place tenant data lives: active stores, caches, object versions, replicas, exports, backups, and encryption keys." | deletion reaches derived copies

## svc-tenant-id-in-telemetry

svc-tenant-id-in-telemetry | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "Include server-verified tenant context in tenant-scoped security and audit events" | tenant id on every audit record
svc-tenant-id-in-telemetry | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "A centralized audit store is acceptable when read access enforces tenant scope." | the read must be scoped
svc-tenant-id-in-telemetry | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "Authorize the request before reading a protected cached value; cache-key separation does not replace authorization." | a key prefix is not authorization
svc-tenant-id-in-telemetry | https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/layers-hide-tenant-details.html | AWS | "both services need to inject tenant context into their log messages and metric events" | tenant id on every log and metric
svc-tenant-id-in-telemetry | https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/layers-hide-tenant-details.html | AWS | "the code uses the JWT token to resolve the tenant context and inject it into the log messages and metric events" | write from verified context
svc-tenant-id-in-telemetry | https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-tenant-logging | Google | "To create tenant-specific logs, the cluster admin creates a sink to route log entries to each tenant's project." | tenant id on log records
svc-tenant-id-in-telemetry | https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-tenant-logging | Google | "resource.labels.namespace_name=\"$TENANT_NAMESPACE\"" | the tenant field is the read filter
svc-tenant-id-in-telemetry | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data | Microsoft | "If you monitor or meter your tenants, consider how your solution reports metrics and whether it can easily link metrics to the tenant that triggered the request." | metric records carry the tenant

## svc-export-scope

svc-export-scope | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "Provide tenant data export when contract, regulation, or product policy requires it." | export is a tenant-scoped read
svc-export-scope | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "Test a backup with two tenants: recover one tenant, verify the other tenant's records and objects are absent" | test the export with two tenants
svc-export-scope | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "A shared backup can contain data from several tenants. For a single-tenant recovery from a shared database, restore into a separate resource and selectively recover the target tenant's data." | restore into a separate resource
svc-export-scope | https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html | OWASP | "Reapply current access and retention rules; a backup can contain old memberships or data that should no longer be accessible." | re-apply current access after restore
svc-export-scope | https://confluence.atlassian.com/display/CONF719/Export+Content+to+Word,+PDF,+HTML+and+XML | Atlassian | "HTML – export an HTML file containing only the pages you have permission to view." | export is scoped to the reader
svc-export-scope | https://confluence.atlassian.com/display/CONF719/Export+Content+to+Word,+PDF,+HTML+and+XML | Atlassian | "PDF – export a PDF file containing only the pages you have permission to view." | export is scoped to the reader
svc-export-scope | https://confluence.atlassian.com/display/CONF719/Export+Content+to+Word,+PDF,+HTML+and+XML | Atlassian | "XML – export a full XML file containing all the pages in the space, including those you don't have permission to view." | the counter-example: an admin backup
svc-export-scope | https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-export-data | Microsoft | "If you have permissions to the data, you can see and export the data that Power BI uses to create a visualization." | export is gated on read permission
svc-export-scope | https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-export-data | Microsoft | "If RLS is applied, you can only export data you're authorized to see." | the filter applies inside the export
svc-export-scope | https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data | Microsoft | "In a shared database, restoring a single tenant might require you to restore the database to a separate resource and selectively recover that tenant's data." | restore into a separate resource
svc-export-scope | https://cloud.google.com/architecture/dr-scenarios-planning-guide | Google | "Make sure that the security controls that you apply to your production data also apply to your recovered data: the same permissions, encryption, and audit requirements should all apply." | recovered data keeps current controls
svc-export-scope | https://cloud.google.com/architecture/dr-scenarios-planning-guide | Google | "Know where your backups are located and who is authorized to restore data." | restore authority is known

## svc-decompression-cap

svc-decompression-cap | https://nodejs.org/api/zlib.html | Node.js (OpenJS Foundation) | "Limits output size when using convenience methods." | cap the decompressed output
svc-decompression-cap | https://nodejs.org/api/zlib.html | Node.js (OpenJS Foundation) | "Reject content declaring more than this many uncompressed bytes, before allocating anything." | cap before allocation
svc-decompression-cap | https://nodejs.org/api/zlib.html | Node.js (OpenJS Foundation) | "Reject content declaring more than this many uncompressed bytes, before decompressing anything. Default: no limit." | zipEntry.contentIterator has no default maxSize
svc-decompression-cap | https://nodejs.org/api/zlib.html | Node.js (OpenJS Foundation) | "it is not capped by zlib.getMaxZipContentSize() the way zipEntry.content() is" | the iterator needs its own maxSize
svc-decompression-cap | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/request-decompression?view=aspnetcore-10.0 | Microsoft | "The maximum size of the decompressed request body is limited to the request body size limit enforced by the endpoint or server." | cap the decompressed output
svc-decompression-cap | https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/request-decompression?view=aspnetcore-10.0 | Microsoft | "If the number of bytes read from the decompressed request body stream exceeds the limit, an InvalidOperationException is thrown to prevent additional bytes from being read from the stream." | the cap is enforced on the output stream
svc-decompression-cap | https://httpd.apache.org/docs/2.4/mod/mod_deflate.html | Apache | "The DeflateInflateLimitRequestBody directive specifies the maximum size of an inflated request body." | cap the inflated body
svc-decompression-cap | https://httpd.apache.org/docs/2.4/mod/mod_deflate.html | Apache | "None, but LimitRequestBody applies after deflation" | the inflated cap is not set by default
svc-decompression-cap | https://httpd.apache.org/docs/2.4/mod/mod_deflate.html | Apache | "A value of 0 means no limit is applied to the inflated body size" | zero removes the cap
svc-decompression-cap | https://httpd.apache.org/docs/2.4/mod/mod_deflate.html | Apache | "don't trust the Content-Length header!" | the compressed length is the wrong number
svc-decompression-cap | https://httpd.apache.org/docs/2.4/mod/mod_deflate.html | Apache | "The Content-Length header reflects the length of the incoming data from the client and not the byte count of the decompressed data stream." | the compressed length is the wrong number
svc-decompression-cap | https://docs.python.org/3/library/tarfile.html | Python Software Foundation | "Never extract archives from untrusted sources without prior inspection." | inspection is not a byte cap
svc-decompression-cap | https://docs.python.org/3/library/tarfile.html | Python Software Foundation | "will prevent the most dangerous security issues. However, it will not prevent all unintended or insecure behavior." | a filter is not a size bound

## svc-webhook-replay-window

svc-webhook-replay-window | https://docs.svix.com/receiving/verifying-payloads/how-manual | Svix | "You should compare this timestamp against your system timestamp and make sure it's within your tolerance in order to prevent timestamp attacks." | reject outside the tolerance
svc-webhook-replay-window | https://docs.svix.com/receiving/verifying-payloads/how-manual | Svix | "will be the same when the same webhook is being resent (e.g. due to a previous failure)" | dedupe by message id
svc-webhook-replay-window | https://docs.slack.dev/authentication/verifying-requests-from-slack/ | Slack | "The signature depends on the timestamp to protect against replay attacks." | the timestamp is the replay control
svc-webhook-replay-window | https://docs.slack.dev/authentication/verifying-requests-from-slack/ | Slack | "we verify that the timestamp does not differ from local time by more than five minutes" | a short tolerance
svc-webhook-replay-window | https://docs.slack.dev/authentication/verifying-requests-from-slack/ | Slack | "It could be a replay attack, so let's ignore it." | reject the message
svc-webhook-replay-window | https://www.rfc-editor.org/rfc/rfc9421.html | IETF | "Enforcing a maximum signature age from the time of the created timestamp." | reject outside the age window
svc-webhook-replay-window | https://www.rfc-editor.org/rfc/rfc9421.html | IETF | "Rejecting signatures past the expiration time in the expires timestamp." | reject an expired signature
svc-webhook-replay-window | https://www.rfc-editor.org/rfc/rfc9421.html | IETF | "it is possible for two different HTTP messages to validate against the same signature" | a signature alone does not stop replay
svc-webhook-replay-window | https://docs.stripe.com/webhooks/signature | Stripe | "Webhook endpoints might occasionally receive the same event more than once. Guard against duplicated event receipts by logging the event IDs you've processed, and then not processing already-logged events." | dedupe by event id
svc-webhook-replay-window | https://docs.stripe.com/webhooks/signature | Stripe | "When your endpoint receives an event you've already processed, skip it and return a 200 response to stop further retries." | skip a duplicate

## code-workload-identity

code-workload-identity | https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws | GitHub | "OpenID Connect (OIDC) allows your GitHub Actions workflows to access resources in Amazon Web Services (AWS), without needing to store the AWS credentials as long-lived GitHub secrets." | exchange a token instead of a stored key
code-workload-identity | https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws | GitHub | "you must define at least one condition, so that untrusted repositories can't request access tokens for your cloud resources" | pin the trust policy
code-workload-identity | https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws | GitHub | "This token is then used to authenticate with external services using a short-lived access token." | the credential is short-lived
code-workload-identity | https://cloud.google.com/iam/docs/workload-identity-federation | Google | "Using Workload Identity Federation, you can provide on-premises or multicloud workloads with access to Google Cloud resources by using federated identities instead of a service account key." | exchange instead of a key
code-workload-identity | https://cloud.google.com/iam/docs/workload-identity-federation | Google | "Workload Identity Federation eliminates the maintenance and security burden associated with service account keys." | no stored cloud key
code-workload-identity | https://cloud.google.com/iam/docs/workload-identity-federation | Google | "You can use an attribute condition to restrict which identities can authenticate using your workload identity pool." | pin the trust policy
code-workload-identity | https://docs.gitlab.com/ci/secrets/id_token_authentication/ | GitLab | "ID tokens are JSON web tokens (JWT) generated by GitLab CI/CD. CI/CD jobs can use ID tokens for OIDC authentication with third-party services" | the platform mints the token
code-workload-identity | https://docs.gitlab.com/ci/secrets/id_token_authentication/ | GitLab | "The expiry time for the token is set to the job's timeout if specified, or 5 minutes if no timeout is specified." | the credential is short-lived
code-workload-identity | https://docs.gitlab.com/ci/secrets/id_token_authentication/ | GitLab | "When you write a trust policy, include stable, unique identifiers such as namespace_id and project_id alongside path-based claims like sub" | pin the trust policy

## svc-dlq (edit)

svc-dlq | https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-sessions | Microsoft | "Once exceeded, the message is moved to the dead-letter queue (DLQ), and the receiver continues receiving subsequent messages from the session." | a failed message does not block the session
svc-dlq | https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-sessions | Microsoft | "When multiple concurrent receivers pull from the queue, the messages belonging to a particular session are dispatched to the specific receiver that currently holds the lock for that session." | the session is the isolation unit
svc-dlq | https://cloud.google.com/pubsub/docs/ordering | Google | "Unacknowledged messages for a given ordering key can potentially delay delivery of messages for other ordering keys, especially during server restarts or traffic changes." | the head-of-line failure
svc-dlq | https://cloud.google.com/pubsub/docs/ordering | Google | "If timely acknowledgment is not possible, consider using a dead-letter topic to prevent indefinite message holding." | the dead-letter queue releases the block
svc-dlq | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html | AWS | "No additional messages from the same message group ID are returned until the first message is deleted or becomes visible again." | the block is per group
svc-dlq | https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html | AWS | "FIFO queues allow parallel processing of messages across different message group IDs." | a group is the isolation unit

## code-workflow-supply-chain (edit)

code-workflow-supply-chain | https://docs.github.com/en/actions/reference/security/secure-use | GitHub | "The pull_request_target and workflow_run workflow triggers, when used with the checkout of an untrusted pull request, expose the repository to security compromises." | keep untrusted code out of a privileged job
code-workflow-supply-chain | https://docs.github.com/en/actions/reference/security/secure-use | GitHub | "Workflows that use these triggers must not explicitly check out untrusted code, including from pull request forks or from repositories that are not under your control." | the untrusted-code boundary
code-workflow-supply-chain | https://docs.github.com/en/actions/reference/security/secure-use | GitHub | "Pin references to actions to a commit SHA in your workflow files." | pin every action
code-workflow-supply-chain | https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html | OWASP | "Perform builds in appropriately isolated nodes" | isolate the build
code-workflow-supply-chain | https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html | OWASP | "If the file is stored alongside the code, it is imperative that the file is reviewed before any merge request is approved." | review the CI file
code-workflow-supply-chain | https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html | OWASP | "credential sharing across pipelines should be kept to a minimum" | limit the privilege of the job
code-workflow-supply-chain | https://docs.gitlab.com/ci/pipelines/ | GitLab | "Runners marked as protected can run jobs only on protected branches, preventing untrusted code from executing on the protected runner and preserving deployment keys and other credentials from being unintentionally accessed." | keep untrusted code off the deploy runner
code-workflow-supply-chain | https://docs.gitlab.com/ci/pipelines/ | GitLab | "Variables marked as protected are accessible to jobs that run in pipelines for protected branches." | the credential follows the protected job
code-workflow-supply-chain | https://github.com/ossf/scorecard/blob/main/docs/checks.md | OpenSSF | "This check determines whether the project's GitHub Action workflows has dangerous code patterns." | the Dangerous-Workflow gate
code-workflow-supply-chain | https://github.com/ossf/scorecard/blob/main/docs/checks.md | OpenSSF | "This checks if a pull_request_target or workflow_run workflow trigger was used in conjunction with an explicit pull request checkout." | the gate names the pattern

## svc-rate-limit-quota (edit)

svc-rate-limit-quota | https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api | GitHub | "The GraphQL API assigns points to each query and limits the points that you can use within a specific amount of time." | the window is stated
svc-rate-limit-quota | https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api | GitHub | "5,000 points per hour per user" | the count is per principal
svc-rate-limit-quota | https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api | GitHub | "The time at which the current rate limit window resets, in UTC epoch seconds." | when capacity returns
svc-rate-limit-quota | https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits | Shopify | "Calls to the GraphQL Admin API are limited based on calculated query cost, which means you should consider the cost of requests over time rather than the number of requests." | the window is a rate over time
svc-rate-limit-quota | https://shopify.dev/docs/apps/build/apis/graphql-admin/rate-limits | Shopify | "your quota refills continuously, so short bursts are fine as long as your average cost stays under the restore rate." | when capacity returns
svc-rate-limit-quota | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html | AWS | "Per-client throttling limits are applied to clients that use API keys associated with your usage plan as client identifier." | key the count to the principal
svc-rate-limit-quota | https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html | AWS | "a token counts for a request" | the token bucket states the window
svc-rate-limit-quota | https://learn.microsoft.com/en-us/azure/api-management/rate-limit-policy | Microsoft | "The rate-limit policy prevents API usage spikes on a per subscription basis by limiting the call rate to a specified number per a specified time period." | key the count to the principal, state the window
svc-rate-limit-quota | https://learn.microsoft.com/en-us/azure/api-management/rate-limit-policy | Microsoft | "The length in seconds of the sliding window during which the number of allowed requests should not exceed the value specified in calls." | the window is explicit

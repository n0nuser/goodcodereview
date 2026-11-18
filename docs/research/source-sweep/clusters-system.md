# Clusters, level: system (77 rows in, 0 CONFLICT cards proposed, 1 source-level conflict noted)

## sys-cache-hit-rate-watched | orgs: 3 | status: READY (3+ orgs)
Rule: Emit a cache hit-rate or memory-use metric and alert on it, so an undersized cache is noticed before it hurts the origin.
Concern tags: observability, performance, reliability
Severity guess: discuss
Rows: 1425, 2071, 1410
Orgs: aws, google, atlassian
Conflicts/duplicates: none (sys-cache-bounds-invalidation covers size and expiry, not monitoring)
Notes: aws = hit-rate and utilization metrics; google = alert at 80% memory ratio; atlassian = repeated re-downloads signal a too-small cache (an indirect hit-rate signal, the weakest of the three; check before promoting).

## sys-hedge-budget | orgs: 2 | status: NEAR (2 orgs)
Rule: Cap hedged requests with a retry budget or retry limit, and stop hedging when the server asks clients not to retry.
Concern tags: reliability, performance
Severity guess: should-fix
Rows: 2118, 2119, 2400
Orgs: google, envoy
Conflicts/duplicates: none (sys-fanout-leg-deadlines only names hedging as one option)
Notes: google = failure-driven token budget plus honour server pushback; envoy = hedging needs a retry policy that caps retries. Common clause: hedging is bounded.

## sys-ssrf-pin-resolved-ip | orgs: 2 | status: NEAR (2 orgs)
Rule: Connect only to the IP address that passed the destination check, so DNS rebinding cannot swap in a private address.
Concern tags: security
Severity guess: should-fix
Rows: 2067, 2072
Orgs: owasp, github
Conflicts/duplicates: none (sys-ssrf states the allowlist only; sibling or extension)
Notes: Row 2068 (owasp: disable redirect following) has one org; could be a second clause.

## sys-shuffle-shard | orgs: 2 | status: NEAR (2 orgs)
Rule: Assign each tenant a shuffled subset of shared workers, so one tenant's fault reaches only a few other tenants.
Concern tags: reliability
Severity guess: discuss
Rows: 1454, 2044
Orgs: aws, airbnb
Conflicts/duplicates: none (sys-cells-limit-blast-radius is about independent cells; shuffle sharding is a distinct technique, but check for overlap)
Notes: both describe the same technique; failable only where a diff shows tenant-to-node assignment.

## sys-no-single-facility-dependency | orgs: 2 | status: NEAR (2 orgs)
Rule: Do not hard-code a dependency on one facility or stamp; run at least two.
Concern tags: reliability
Severity guess: discuss
Rows: 2058, 2136
Orgs: cloudflare, microsoft
Conflicts/duplicates: none (sys-cells-limit-blast-radius is about splitting, not redundancy)
Notes: cloudflare = no facility dependency for GA services; microsoft = at least two stamps. Cloudflare one is a service-class policy, may not be reviewable in a diff.

## sys-timing-free-lock-safety | orgs: 2 | status: NEAR (2 orgs)
Rule: Do not make a lock's safety depend on timing; measure lock and lease expiry with a monotonic clock, not the wall clock.
Concern tags: correctness, reliability
Severity guess: should-fix
Rows: 2151, 2566, 2150
Orgs: kleppmann, salvatore
Conflicts/duplicates: partial overlap with sys-lock-fencing and sys-leader-two-leaders; narrow the card to the clock clause
Notes: both are individuals (blog/author sources), so promotion needs a real org or the person-standing rule. Row 2150 (state whether the lock is for efficiency or correctness) is kleppmann only. Row 2054 (aws: no lease renewal from a heartbeat thread) is a third, separate clause.

## sys-tx-per-batch-migration | orgs: 2 | status: NEAR (2 orgs)
Rule: Run each batch or each part of a large migration in its own transaction.
Concern tags: reliability, performance
Severity guess: should-fix
Rows: 2082, 2117
Orgs: cockroach, gocardless
Conflicts/duplicates: overlaps sys-migration-expand-contract (batches in a separate migration); likely a clause merge, not a new card
Notes: SOURCE CONFLICT, no card: retool 129 says wrap every migration in a transaction; doctolib 2115 says run migrations outside a transaction. Also conflicts in scope with stable sys-index-concurrently (outside a transaction block for CONCURRENTLY). Do not draft until reconciled (it is per-statement dependent).

## CONFLICT | orgs: 1 | status: ONE
Rule: On corrupt config, log and fall back to a known-good state rather than dropping requests.
Concern tags: reliability
Severity guess: discuss
Rows: 1145
Orgs: cloudflare
Conflicts/duplicates: CONFLICT with sys-secrets-and-errors (fail closed); no card proposed
Notes: fail-open for config vs fail-closed for auth; the two apply to different failure classes but the wording clashes.

## sys-no-secrets-pii-in-logs | orgs: 1 | status: ONE
Rule: Keep secrets and personal data out of logs, and redact per tenant at ingestion.
Concern tags: security, observability
Severity guess: should-fix
Rows: 1836, 207, 1814
Orgs: microsoft
Conflicts/duplicates: none (sys-secrets-and-errors covers error responses; sys-pii-minimise-retention covers retention)
Notes: strong candidate; needs two more orgs (OWASP logging cheat sheet is the obvious one).

## sys-agent-human-approval | orgs: 1 | status: ONE
Rule: Require human approval before an agent runs a high-risk or irreversible action.
Concern tags: security, process
Severity guess: should-fix
Rows: 2146, 2183
Orgs: microsoft
Conflicts/duplicates: none (chg-bot-approval-not-human is about review approvals; sys-agent-tool-least-privilege is about tool scope)
Notes: needs two more orgs.

## sys-ssrf-no-redirects | orgs: 1 | status: ONE
Rule: Disable redirect following in the outbound HTTP client for user-supplied URLs.
Concern tags: security
Severity guess: should-fix
Rows: 2068
Orgs: owasp
Conflicts/duplicates: none
Notes: could join sys-ssrf-pin-resolved-ip.

## sys-lock-order | orgs: 1 | status: ONE
Rule: Acquire locks on the same tables in the same order on every transaction path.
Concern tags: correctness, reliability
Severity guess: should-fix
Rows: 1393
Orgs: shopify
Conflicts/duplicates: none
Notes: row 2156 (postgresai: take all migration locks at transaction start and retry the whole transaction) is related but separate.

## sys-cache-negative-ttl | orgs: 1 | status: ONE
Rule: Cache error responses under a negative TTL distinct from the positive TTL.
Concern tags: reliability, performance
Severity guess: discuss
Rows: 2066
Orgs: aws
Conflicts/duplicates: none (extends sys-cache-bounds-invalidation)
Notes: clause of an existing card, not a new one.

## sys-cache-not-system-of-record | orgs: 1 | status: ONE
Rule: Keep the system of record authoritative; never store critical data only in the cache.
Concern tags: correctness, reliability
Severity guess: should-fix
Rows: 2132
Orgs: microsoft
Conflicts/duplicates: none
Notes: needs two more orgs.

## sys-warehouse-pseudonymise | orgs: 1 | status: ONE
Rule: Pseudonymise personal data before it enters the data warehouse.
Concern tags: security, process
Severity guess: should-fix
Rows: 1311
Orgs: shopify
Conflicts/duplicates: none (sys-pii-minimise-retention is about retention); row 2100 (gdpr-info: collect only what is adequate and limited to purpose) is a neighbouring clause
Notes: needs two more orgs.

## sys-rpc-deadline-in-service-def | orgs: 1 | status: ONE
Rule: Every RPC method sets its deadline in the service definition; opting out is explicit.
Concern tags: reliability
Severity guess: should-fix
Rows: 1202
Orgs: dropbox
Conflicts/duplicates: close to go-http-client-timeout and sys-fanout-leg-deadlines; likely a clause extension
Notes: row 2125 (kubernetes: start deadline per scheduled run) is separate.

## sys-json-column-size-check | orgs: 1 | status: ONE
Rule: Give each new JSON or JSONB column a database-level size limit via a CHECK constraint.
Concern tags: reliability, security
Severity guess: should-fix
Rows: 2395
Orgs: gitlab
Conflicts/duplicates: none (svc-bound-client-controlled-sizes is API-level)
Notes: needs two more orgs.

## sys-notnull-after-deploy | orgs: 1 | status: ONE
Rule: Add a NOT NULL constraint only after the application changes are deployed, in a post-deployment migration.
Concern tags: reliability, compatibility
Severity guess: should-fix
Rows: 228
Orgs: gitlab
Conflicts/duplicates: row 234 (postgresql: NOT NULL scans the table unless NOT VALID) is covered by sys-constraint-not-valid; dropped
Notes: ordering clause not in sys-constraint-not-valid.

## Dropped (no group)
- Duplicates of existing cards: 2171 (mit least privilege, sys-agent-tool-least-privilege), 2100/2153 (retention, sys-pii-minimise-retention), 1427 and 2113 (expiry and size bound, sys-cache-bounds-invalidation), 2158/2084/2085 (retention, sys-append-only-stores-have-retention).
- Tutorial, product behaviour or linter-owned: 2050, 2052, 2204 (icons), 2084, 2085, 2093, 2098, 2120, 2121, 2187, 2189, 2198, 2395-adjacent IETF rows 2401 and 2402, 2398, 2070, 2163 (redis memory settings), 2123, 1127, 1135, 2166, 1241, 1262, 1408, 2063, 2109, 2129, 2190, 2186, 2200, 2201, 2168, 2054, 2055, 2150-alone rows.

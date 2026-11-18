# Service-level clusters (from cluster-in/service.tsv)

## svc-tls-all-traffic | orgs: 3 | status: READY (3+ orgs)
Rule: Serve and call every HTTP-based API over TLS, with no plaintext fallback.
Concern tags: security
Severity guess: should-fix
Rows: 1767, 1925, 1092
Orgs: mozilla, owasp, nist
Conflicts/duplicates: none (svc-tls-modern-only covers the protocol versions a server accepts; fn-tls-verify-on covers certificate checks; neither states "all traffic is encrypted")
Notes: mozilla says all communications; owasp says all client to external-facing HTTP services, no fallback to unencrypted; nist says encrypt all API traffic in transit. Row 1767 also touches HSTS preload (leave out).

## svc-api-version-on-every-request | orgs: 3 | status: READY (3+ orgs)
Rule: Require the caller to name the API version on every request, in a header or query parameter.
Concern tags: compatibility, maintainability
Severity guess: should-fix
Rows: 1642, 1738, 2348
Orgs: github, google, microsoft
Conflicts/duplicates: none (svc-api-versioning-policy is about the scheme and no breaking change inside a version; it does not require the caller to send the version)
Notes: github uses a header and says "should"; google requires header or query param (for APIs under its individual versioning scheme); microsoft requires a query param api-version on every operation. Github's wording is a recommendation to clients, so check the "require" clause.

## svc-client-paces-outgoing-calls | orgs: 3 | status: READY (3+ orgs)
Rule: Pace outgoing calls to a rate-limited API on the client (token bucket or fixed rate) so the client is not throttled.
Concern tags: reliability, performance
Severity guess: should-fix
Rows: 1935, 1695, 1640
Orgs: shopify, stripe, github
Conflicts/duplicates: none (svc-rate-limit-quota, svc-rate-limit-by-cost, svc-retry-policy are server side or retry after failure)
Notes: shopify paces to the leak rate (about 2 req/s); stripe says implement a client token bucket; github says pause at least 1 s between writes. Stripe and github also say serialise writes (rows 1696, 1640): only 2 orgs, so keep that clause out.

## svc-bound-inbound-concurrency | orgs: 4 | status: READY (3+ orgs)
Rule: Cap how many requests a service handles at once with an explicit concurrency limit; a timeout alone does not bound it.
Concern tags: reliability, performance
Severity guess: should-fix
Rows: 1453, 1670, 2562, 2108
Orgs: aws, tokio, uber, netflix
Conflicts/duplicates: partial overlap with svc-circuit-breaker-bulkhead (limit per dependency, outbound) and svc-bounded-background-tasks (background work); this card is the inbound request limit
Notes: aws says timeouts and retries do not prevent concurrency exhaustion; tokio says cap in-flight requests or invite DoS; uber uses in-flight concurrency, not QPS, as the overload signal; netflix gives each request group a share of one shared concurrency limit (weaker, the share clause is separate). Decide with the maintainer whether this is a new card or an extension of the bulkhead card.

## svc-circuit-breaker-fail-fast | orgs: 2 | status: NEAR (2 orgs)
Rule: Wrap a failing dependency in a circuit breaker that opens after recent failures pass a threshold and then fails calls at once.
Concern tags: reliability
Severity guess: should-fix
Rows: 1710, 1818, 1819
Orgs: spotify, microsoft
Conflicts/duplicates: none (svc-circuit-breaker-bulkhead states only the per-dependency concurrency limit)
Notes: microsoft also describes half-open trial requests (1819); spotify says fast-fail for weak dependencies. Half-open clause has one org.

## svc-no-stacked-retries | orgs: 2 | status: NEAR (2 orgs)
Rule: Retry at one layer of a call chain only, so attempts do not multiply down the chain.
Concern tags: reliability, performance
Severity guess: should-fix
Rows: 2036, 1823
Orgs: google, microsoft
Conflicts/duplicates: none stated by svc-retry-policy (attempt caps and backoff only)
Notes: google says avoid retries at multiple levels; microsoft says retry only where the full context of the failing operation is known.

## svc-logs-tamper-resistant | orgs: 2 | status: NEAR (2 orgs)
Rule: Ship logs and audit trails to a store that the logged host cannot alter or delete.
Concern tags: security, observability
Severity guess: should-fix
Rows: 1747, 1748, 1958
Orgs: google, owasp
Conflicts/duplicates: none (svc-security-event-logging is draft and covers failed-auth content)
Notes: google wants immutable, remote, centralised logs; owasp wants integrity controls against tampering or deletion on transaction audit trails. Row 2352 (google, restrict reading logs) is a second clause with one org.

## svc-no-default-credentials | orgs: 2 | status: NEAR (2 orgs)
Rule: Ship no default or hard-coded credential that is the same for every installation.
Concern tags: security
Severity guess: should-fix
Rows: 2528, 2529, 2557
Orgs: mitre, cisa
Conflicts/duplicates: none (svc-fail-closed-defaults is about security controls on and empty allow-lists)
Notes: mitre also says force a change at install (2529); cisa says eliminate default passwords. "Force change at install" is a fallback clause with one org, so keep the narrow ban.

## svc-path-normalise-before-authz | orgs: 2 | status: NEAR (2 orgs)
Rule: Normalise the URL path, or reject escaped slashes and case variants, before matching authorisation or routing rules.
Concern tags: security
Severity guess: should-fix
Rows: 1891, 1972, 1973, 1911
Orgs: portswigger, envoy
Conflicts/duplicates: none
Notes: portswigger says match on a normalised path so case or suffix variants cannot bypass a deny and that origin and cache must resolve paths alike; envoy rejects %2F, %5C and fragments by default. The origin-cache agreement clause is portswigger only.

## svc-reject-get-with-body | orgs: 2 | status: NEAR (2 orgs)
Rule: Reject a GET or HEAD request that carries a body.
Concern tags: security, correctness
Severity guess: should-fix
Rows: 1913, 1982, 1905
Orgs: portswigger, fastly
Conflicts/duplicates: none (svc-request-framing covers Transfer-Encoding plus Content-Length only)
Notes: fastly answers 400 and does not forward; portswigger says do not accept fat GETs and never assume a request has no body (that clause reads differently: parse the body anyway).

## svc-framing-denied-by-csp | orgs: 2 | status: NEAR (2 orgs)
Rule: Forbid framing of pages with CSP frame-ancestors (not only X-Frame-Options), set explicitly.
Concern tags: security
Severity guess: should-fix
Rows: 1469, 1477, 1567, 1568
Orgs: owasp, mozilla
Conflicts/duplicates: svc-security-headers (draft, held) already states this in its Why; do not add a card until it gets a third org or the held card is revisited
Notes: owasp says frame-ancestors replaces X-Frame-Options; mozilla says set it explicitly because default-src does not fall back.

## svc-nosniff | orgs: 2 | status: NEAR (2 orgs)
Rule: Send X-Content-Type-Options: nosniff on every response, with a correct Content-Type.
Concern tags: security
Severity guess: should-fix
Rows: 1569, 1570, 1919
Orgs: mozilla, owasp
Conflicts/duplicates: svc-security-headers (draft, held) already states this in its Why
Notes: mozilla stresses a correct MIME type on every resource; owasp says every HTTP response.

## svc-session-expiry | orgs: 2 | status: NEAR (2 orgs)
Rule: Give every session an overall and an inactivity expiry, and end the session when either runs out.
Concern tags: security
Severity guess: should-fix
Rows: 1883, 1576
Orgs: nist, mozilla
Conflicts/duplicates: none (svc-session-lifecycle covers new ID at login and cookie flags only)
Notes: nist specifies both timeouts; mozilla only says expire as soon as possible.

## svc-tenant-scope-in-data-layer | orgs: 2 | status: NEAR (2 orgs)
Rule: Enforce tenant scope in the data layer by default (query filter or row-level security), not per call site.
Concern tags: security, correctness
Severity guess: should-fix
Rows: 1840, 1841, 1481, 1480
Orgs: microsoft, owasp
Conflicts/duplicates: none (svc-tenant-id-in-telemetry is about telemetry; svc-soft-delete-default is a similar pattern for deleted rows)
Notes: microsoft uses a default global query filter; owasp uses forced RLS on table owners plus a server-verified tenant binding.

## svc-debug-off-in-production | orgs: 2 | status: NEAR (2 orgs)
Rule: Keep debug modes and developer tooling (such as Swagger UI) disabled in production.
Concern tags: security
Severity guess: should-fix
Rows: 1928, 791
Orgs: owasp, microsoft
Conflicts/duplicates: none
Notes: owasp says debug modes off for all components; microsoft says enable Swagger only in development. Narrow to debug and docs endpoints.

## svc-server-read-timeouts | orgs: 2 | status: NEAR (2 orgs)
Rule: Set read and header timeouts on a server that faces untrusted clients.
Concern tags: security, reliability
Severity guess: should-fix
Rows: 546, 2329
Orgs: cloudflare, nodejs
Conflicts/duplicates: none (svc-timeouts is about outgoing remote calls)
Notes: cloudflare says set both read and write timeouts; nodejs says headersTimeout must be non-zero.

## svc-paginate-by-server-links | orgs: 2 | status: NEAR (2 orgs)
Rule: Fetch further pages only through the server's next link or opaque token, never by building page numbers or parsing tokens.
Concern tags: correctness, compatibility
Severity guess: should-fix
Rows: 1652, 1736, 1650
Orgs: github, google
Conflicts/duplicates: none (svc-list-endpoint-paginates is server side)
Notes: github follows link headers and wants stable sort order (one org); google says page tokens must be opaque.

## svc-boolean-no-is-prefix | orgs: 2 | status: NEAR (2 orgs)
Rule: Name boolean fields without an "is" prefix.
Concern tags: maintainability
Severity guess: discuss
Rows: 1733, 1217
Orgs: google, microsoft
Conflicts/duplicates: none (svc-api-naming-consistent covers casing only)
Notes: google says omit "is" on boolean fields; microsoft says "enabled", not "isEnabled". Style rule, low review value.

## svc-update-writes-inactive-copy | orgs: 2 | status: NEAR (2 orgs)
Rule: Write an update only to the inactive slot, and verify it before switching the boot pointer.
Concern tags: reliability
Severity guess: should-fix
Rows: 1946, 1657
Orgs: google, mender
Conflicts/duplicates: partial overlap with svc-update-rollback-on-failure (restore previous version) and svc-update-verify-provenance
Notes: mender verifies the checksum then flips the bootloader flag; google says never update the running slot's partitions. The "verify before switch" clause has one org.

## svc-401-sends-challenge | orgs: 2 | status: NEAR (2 orgs)
Rule: Answer an unauthenticated request with 401 and a WWW-Authenticate challenge.
Concern tags: compatibility, correctness
Severity guess: should-fix
Rows: 1581, 2000
Orgs: siemens, ietf
Conflicts/duplicates: check svc-api-specific-status-codes (401 may already be listed without the header)
Notes: siemens is a vendor API page that restates the RFC; ietf is the primary source, so the count may be effectively 1. Treat as weak.

## svc-encode-log-data | orgs: 1 | status: ONE (1 org)
Rule: Encode untrusted data written to logs so it cannot inject log lines or attack log tooling.
Concern tags: security, observability
Severity guess: should-fix
Rows: 1959, 2161
Orgs: owasp
Conflicts/duplicates: none
Notes: both rows are OWASP (ASVS and a cheat sheet), so one org.

## svc-propagate-remaining-deadline | orgs: 1 | status: ONE (1 org)
Rule: Pass the remaining time budget to downstream calls instead of a new deadline per hop.
Concern tags: reliability
Severity guess: should-fix
Rows: 2037, 1751
Orgs: google
Conflicts/duplicates: none (svc-timeouts says a timeout on every call, not propagation)
Notes: google only; ASK whether 1751 (relative, not absolute, to avoid skew) fits.

## svc-dlq-replay-audited | orgs: 1 | status: ONE (1 org)
Rule: Record who replays dead-letter messages, when and why, and require a stated reason.
Concern tags: process, observability
Severity guess: should-fix
Rows: 1994, 1995
Orgs: notion
Conflicts/duplicates: extends svc-dlq (replay exists, audit not stated)
Notes: notion only.

## svc-regex-untrusted-input | orgs: 1 | status: ONE (1 org)
Rule: Never build a regex from untrusted input, and give regexes that see untrusted input a timeout or a non-backtracking engine.
Concern tags: security, performance
Severity guess: should-fix
Rows: 808, 809
Orgs: microsoft
Conflicts/duplicates: none
Notes: microsoft only.

## svc-refresh-token-rotation | orgs: 1 | status: ONE (1 org)
Rule: Rotate refresh tokens on use, and revoke everything issued since when an invalidated token is replayed.
Concern tags: security
Severity guess: should-fix
Rows: 1450, 1843
Orgs: auth0, microsoft
Conflicts/duplicates: svc-token-revocation (logout and disable revocation, no rotation)
Notes: auth0 states reuse detection; microsoft only says delete the old token after refresh. The reuse-revokes clause has one org (auth0).

## svc-client-access-checks-server-side | orgs: 1 | status: ONE (1 org)
Rule: Enforce every access check on the server; hiding a link or a client-side check is not access control.
Concern tags: security
Severity guess: should-fix
Rows: 1063, 2365
Orgs: owasp, microsoft
Conflicts/duplicates: likely duplicate of svc-authz-central-deny-default; open that card before drafting
Notes: listed as ONE because it is probably already covered.

## svc-api-test-every-endpoint | orgs: 1 | status: ONE (1 org)
Rule: Cover every API endpoint and each of its HTTP methods with a test.
Concern tags: testing
Severity guess: discuss
Rows: 1460
Orgs: cloudflare
Conflicts/duplicates: none; stripe row 1355 (block merge until tests validate API design patterns) is a different clause
Notes: cloudflare only.

## Dropped rows
Dropped as advice, history, vendor-only or linter-owned: OpenAPI structural rules (223-225, 2226), Clipboard iframe attribute (928), CLI and UX rows (1505, 1540, 1541, 1771, 1502, 2546, 2424, 1198, 1536, 1537), skeleton and spinner UX rows (1990-1992, 1435, 1868, 1544), Auth0/Pact/AWS contract-test rows (46, 2409; duplicate of svc-api-contract-tests), idempotency rows (1527, 1528, 1156; duplicate of svc-idempotency-key), canary and gradual rollout rows (1144, 2351; duplicate of prod-canary-staged-rollout), saga and rollback rows (1704, 1871, 2548, 2549; svc-saga-steps), upload rows (1069, 1793, 1632; svc-upload-validate-store, one org each for the extras), HTTP framing rows (2302, 2303, 2378, 2381, 1904; svc-request-framing and one-org leftovers).

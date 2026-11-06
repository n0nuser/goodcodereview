# Judge report: security cards (sonnet)

Scope: 21 cards from `part-sec.txt`. Every `borrowed_from` URL was fetched once (curl, text extracted). UNFETCHED: Netflix tech blog (HTTP 403) and Uber blog (HTTP 406), both cited by `svc-dlq`. Auth0 pages are JS-rendered and returned thin text, so they are weak evidence either way. `tools/validate.py` exits 0 on the working tree. Clauses of edited cards that the diff did not touch were not re-audited.

Method for counts: an organisation is counted only when the fetched page states the clause's practice (PROMOTION rule 3). "weak" means the page mentions the topic but does not recommend the clause.

## code-workflow-supply-chain — PASS
1. consider, check 1. The note says "GitHub, OWASP and GitLab back the untrusted-code boundary". The OWASP CI/CD cheat sheet only says untrusted code can be deployed and that PRs should be reviewed before merge and protected branches used; it never says to keep unreviewed code away from jobs with secrets. The real third org is OpenSSF: the Scorecard `Dangerous-Workflow` check (cited in `tool_gate`) names "untrusted code checkouts". Fix: name OpenSSF in the note, keep OWASP as a reference.
   - GitHub (secure-use): "pull_request_target ... with the checkout of an untrusted pull request, expose the repository"; "must not explicitly check out untrusted code".
   - GitLab (/ci/pipelines): "Runners marked as protected can run jobs only on protected branches, preventing untrusted code from executing on the protected runner and preserving deployment keys".
2. consider, check 3. The PASS ends with a comment ("deployment runs only on a protected branch...") rather than config, so the second Rule clause is not shown as passing. Add a `deploy:` job with `environment: production` or drop the comment.
Counts: pin = GitHub, OpenSSF, StepSecurity (3). Boundary = GitHub, OpenSSF, GitLab (3; OWASP weak).

## svc-api-cache-control — PASS
1. consider, check 6. The new Rule clause ("keep that header authoritative at the edge, where cacheability follows the response `Content-Type`, not the URL extension") joins two ideas in one clause and reads awkwardly. Split: "do not let an edge rule override `Cache-Control`" and "decide cacheability from `Content-Type`, not the extension".
2. consider, check 1. Per-sub-clause support:
   - Edge must not override origin header: PortSwigger ("Configure your CDN settings so that your caching rules don't override the Cache-Control header"), AWS (Expiration page warning: "If your minimum TTL is greater than 0, CloudFront uses the cache policy's minimum TTL, even if ... no-store ... private"), Google (`FORCE_CACHE_ALL` "overriding any cache directives set by the origin"), Microsoft (Front Door honors private/no-store "even if you override the caching behavior by using the Rules Engine"). 4 orgs.
   - Content-Type over extension: Cloudflare Cache Deception Armor ("verify a URL's extension matches the returned Content-Type"), Google (Cloud CDN "inspects the Content-Type HTTP response header"), PortSwigger ("verifies that the response Content-Type matches the request's URL file extension"). 3 orgs. AWS and Microsoft do not back this one.
3. The note correctly keeps path-parsing discrepancy in Why (PortSwigger only).
Counts: edge-override = PortSwigger, AWS, Google, Microsoft (4); Content-Type = Cloudflare, Google, PortSwigger (3).

## svc-dlq — ISSUES
1. act, check 2/3. The note counts Dropbox as one of three orgs for "dead-letter queue and replay". The Dropbox page only proposes it: "One way to reduce this operational overhead ... would be to create dead letter queues ... The ATF framework could impose a maximum number of retries". That is a plan, not a practice (PROMOTION rule 3). Confirmed practice pages: AWS Builders' Library ("We alarm if there are any messages in this queue ... it lets us re-process the messages after the bug is fixed") and Notion ("Re-enqueue is a first-class workflow"; DLQ plus replay). Netflix and Uber are UNFETCHED, so the third org cannot be confirmed. Fix: replace Dropbox with Notion in the note, and have the maintainer confirm Netflix or Uber, otherwise the DLQ+replay clause has 2 confirmed orgs.
2. consider, check 1. New isolation clause ("isolate a poison message so the rest keep moving"). Pages describe mechanics, none recommends "give each independent stream its own group":
   - AWS FIFO: "you can't receive additional messages from the same message group ID ... until the currently received messages are deleted, or they become visible again". Its "Best practice" is one group ID per producer, for ordering.
   - Microsoft sessions: after `MaxDeliveryCount` "the message is moved to the dead-letter queue ... and the receiver continues receiving subsequent messages from the session".
   - Google Pub/Sub: "Unacknowledged messages for a given ordering key can potentially delay delivery of messages for other ordering keys, especially during server restarts or traffic changes ... consider using a dead-letter topic".
   Three orgs describe the head-of-line effect, so the count is 3, but the card states Pub/Sub's hedged sentence flatly ("one unacknowledged ordering key delays the others"). Soften to "can delay". Pub/Sub also warns that with ordering plus a dead-letter topic, order is not preserved; the card is silent on that.
3. consider, check 3. FAIL cannot be marked from the Terraform it shows: "every producer uses the same MessageGroupId" is a comment, not config. Show the producer call (`send_message(..., MessageGroupId="orders")`) in the FAIL.
4. consider, check 6. Why is the longest in the service set. Cut the last sentence (visibility timeout) or move it out; it backs neither Rule clause.
Counts: DLQ+replay = AWS, Notion confirmed (2), Netflix/Uber UNFETCHED, Dropbox does not count; isolation = AWS, Microsoft, Google (3, descriptive).

## svc-rate-limit-quota — PASS
1. No defect. The new Why sentence ("key the count to the identity that owns the quota ... state the window and when capacity returns") is supported: GitHub (limits per user / per installation, with reset), Shopify ("bucket size and restore rate" per app and store), AWS API Gateway (per-client limits via usage plans and API keys), Microsoft APIM (`renewal-period`, `retry-after-header-name`). It stays in Why, correctly, since it is not a Rule clause.
2. consider, check 1. The note says the per-tenant cap "rests on AWS, Google, NIST and Microsoft". NIST SP 800-228 says "rate limiting, quotas" generically and does not say per tenant. AWS (per-customer limits), Google SRE ("per-customer quotas") and Microsoft (noisy neighbor: "prevent a single tenant from overwhelming") are enough for 3. Drop NIST from the note.
Counts: per-tenant quota = AWS, Google, Microsoft (3).

## svc-session-lifecycle — PASS
1. No defect. The added host-scope sentences match MDN ("Use `__Host-` for all cookies needed only on a specific domain (no subdomains) where Path is set to /") and the OWASP Session cheat sheet ("`__Host-` ... must not have a Domain attribute ... Prevents subdomain forgery ... Recommended for session IDs"). Two orgs (Mozilla, OWASP), so it correctly stays in Why. The PASS already used `__Host-sid`.
2. consider, check 3. The Rule does not mention `__Host-` but the PASS shows it, so a reviewer cannot FAIL a cookie without the prefix. Either add it to the Rule (needs a third org; none cited) or mark it in the PASS as optional.
Counts: host-scope = Mozilla, OWASP (2, Why only).

## code-workload-identity — PASS
1. consider, check 3. The PASS comment shows `sub: repo:org/repo:ref:refs/heads/main`. GitHub's page now says repositories created after 15 July 2026 (or opted in) have an immutable-ID `sub` such as `repo:octo-org@123456/octo-repo@456789:ref:refs/heads/octo-branch`. A new repository copying the PASS would write a condition that never matches. Add one line giving the new format.
2. consider, check 6. "A trust policy with no condition, or a wildcard `sub`, lets any repository assume the role, so an exchange without the condition leaves the role open to any repository" repeats itself, and "wildcard sub" is not on the cited page (GitHub: "at least one condition, so that untrusted repositories can't request access tokens"). A wildcard scoped to an org is not "any repository". Say "a missing `sub` condition" and drop the last clause.
3. Sources confirmed: GitHub ("without needing to store the AWS credentials as long-lived GitHub secrets"; `sub` condition), Google (WIF "instead of a service account key"; attribute conditions "restrict which identities can authenticate"), GitLab (ID token `exp` 5 min or job timeout; "Use ID token claims in cloud trust policies"). No duplicate found (code-secret-scan, code-workflow-supply-chain, sys-secrets-and-errors cover other ground).
Counts: exchange = GitHub, Google, GitLab (3); pin trust policy = GitHub, Google, GitLab (3).

## fn-header-value-encoding — PASS
1. consider, check 3. `applies_when` and the card name a download filename, but the Rule and PASS handle only CR/LF. A filename also needs quote and `;` handling or RFC 6266/5987 encoding. Either drop "download filename" from `applies_when` or add a line.
2. Sources confirmed: RFC 9112 §11.1 states both halves ("restricting the output of header fields to APIs that filter for bad octets and not allowing application servers to write directly to the protocol stream"; filtering `%0D`/`%0A` is not enough because of "charset transcoding, XML entity translation, base64 decoding ..."). Node ("Attempting to set a header field name or value that contains invalid characters will result in a TypeError"), Django (`BadHeaderError` on CR or LF), MITRE CWE-113 mitigations. No duplicate card.
Counts: framework API = IETF, OpenJS, Django, MITRE (4); reject/encode CR LF = IETF, MITRE, Django, OpenJS (4).

## svc-account-linking — ISSUES
1. consider, check 1. Auth0's page does not back either clause. Its server-rendered text says only "Suggested account linking: identify accounts with the same email address and prompt the user in your app to link them", and the page body is mostly JS. Drop it from `borrowed_from` or cite it only for the counterpoint.
2. Confirmed: Microsoft MSRC (root cause: "fails to verify that the user actually owns the supplied identifier"; classic-federated merge), OWASP Authentication cheat sheet "Secure Federated Account Linking" (`iss`+`sub` not `sub` alone; "Do not automatically link accounts solely because their email ... match"; "Require an authenticated session with the existing application account"), NIST SP 800-63C (federated identifier = subject plus issuer; RP must never process the subject identifier without the issuer), Google ("Only use the Google ID token's sub field"; ownership of a third-party email "may have since changed"), OpenID Core (`sub` locally unique and never reassigned; RP must not rely on email being unique).
Counts: prove control of both = Microsoft, OWASP, Google (3; NIST implied); key on `iss`+`sub` = OWASP, NIST, OpenID, Google (4).
Substance holds; the Auth0 item is the only finding (consider).

## svc-api-key-scope — ISSUES
1. consider, check 1. "Showing the secret once and keeping only a hash" (Why) has no source. AWS says the secret access key "can be retrieved only at the time you create it", but none of the cited pages says to store a hash. NIST 800-63B's hashing text is about passwords. Add a source (Stripe, GitHub, GitLab do not state it either) or cut the sentence.
2. consider, check 1. "Bounded lifetime" has GitHub ("set an expiration date for the minimum amount of time") and GitLab ("Consider setting a token that expires when your task is complete"). The third org is AWS, which says to use temporary credentials instead of access keys. That is a different control (avoid long-lived keys) from expiring an issued key. Count it as weak. Stripe has rotation but no expiry; Google API keys have none.
3. Confirmed: narrowest scopes = GitHub ("only select the minimum permissions or scopes"), GitLab ("use the most limited scope possible"), Stripe ("Use restricted API keys"), Google ("Add at least one API key restriction") (4); rotate or revoke on schedule and after exposure = Stripe ("Rotate secret API keys periodically", exposure contingency plan), GitHub (rotation steps for compromised credentials), GitLab ("Review all active access tokens ... on a regular basis and revoke"), AWS ("Regularly review, update, and delete access keys") (4).
Counts: scopes 4; lifetime 2 clear plus 1 weak (AWS); rotate/revoke 4.
Recommend stable only if the lifetime clause gains a third direct source, otherwise move "bounded lifetime" to Why.

## svc-cache-key-completeness — ISSUES
1. act, check 1. The note and `borrowed_from` count Microsoft for "key completeness". The Front Door page covers only query-string cache modes and says the `Accept`, `Accept-Language` and `Vary` request headers "don't get forwarded to the origin when caching is enabled". That does not state the practice, and it conflicts with the PASS (`Vary: Accept-Language`) on that platform. Remove Microsoft from the key-completeness count.
   - Remaining orgs: AWS ("When a value in the viewer request determines the response that your origin returns, you should include that value in the cache key"), Fastly ("consider including those values in your cache key or Vary header"), Cloudflare ("Do not rely on values in HTTP headers if they are not part of your cache key"). That is still 3, so the clause survives.
2. consider, check 4. Overlap with `svc-api-cache-control`, whose Rule already says "add `Vary` for any request header that changes the body". Both cards require an input that changes the response to be in the key. The note draws the line (Cache-Control/Vary vs. key and unkeyed inputs), but a reviewer can FAIL the same code under both. Cross-link the two cards or merge the Vary clause into one.
3. consider, check 3. The PASS says "return 400 to a GET with a body". Cloudflare says to treat the GET body as untrusted and "consider bypassing cache or using a POST request"; the 400 is the card's own choice. Fine, but say "or bypass the cache".
4. Confirmed: strip unkeyed inputs = Fastly (exact headers `X-Forwarded-Host`, `X-Rewrite-URL`, `X-Original-URL`), Cloudflare ("Do not include untrusted header values in your response body"; GET body), PortSwigger (poisoning page covers unkeyed inputs and recommends restricting caching to static responses) (3). Static-only default: Cloudflare, PortSwigger, Google (CACHE_ALL_STATIC default), correctly in Why.
Counts: key completeness = AWS, Fastly, Cloudflare (3, Microsoft does not count); strip unkeyed = Fastly, Cloudflare, PortSwigger (3).

## svc-decompression-cap — ISSUES
1. act, check 3. The size claims are wrong for gzip/DEFLATE. Why: "A few kilobytes of gzip can expand to gigabytes". `tool_gate`: "a test that inflates a 1 KB gzip to 1 GB". DEFLATE tops out near 1030:1. Measured here: 200 MiB of zeros gzips to 203,860 bytes (ratio 1029:1), so 1 KB inflates to about 1 MB and 1 GB needs about 1 MB of gzip. The Counterpoint's "A 1 MB gzip can still inflate to 1 GB" is correct. Fix both sentences (for example "a 1 MB gzip can inflate to about 1 GB") and make the test use a 1 MB gzip. Nested archives or other codecs can exceed 1030:1, but the card names gzip.
2. consider, check 6. The Why spends a sentence on `zipEntry.contentIterator()` (Node 26.8 API, "Added in: v26.8.0"; `maxSize` "Default: no limit"). Verified accurate, but it is a niche new API and makes the Why long. Cut or move to a note.
3. consider, check 4. Related to `svc-bound-client-controlled-sizes` (caps request body bytes) and `svc-upload-validate-store` (mentions zip bombs in `tool_gate`). Not duplicates (this card caps decoded output), but add a See also line.
4. Confirmed: Node (`maxOutputLength`, "Default: buffer.kMaxLength"), Apache (`DeflateInflateLimitRequestBody`; "don't trust the Content-Length header ... reflects the length of the incoming data from the client and not the byte count of the decompressed data stream"; "A value of 0 means no limit"), ASP.NET Core ("The maximum size of the decompressed request body is limited to the request body size limit"), Python tarfile ("the pre-defined filters do not prevent denial-of-service attacks").
Counts: cap decompressed output = OpenJS, Apache, Microsoft (3; Python is a reference).

## svc-export-scope — PASS
1. consider, check 6. Roughly a third of the Why is about restore and recovered environments. The sources back it (OWASP "Reapply current access and retention rules; a backup can contain old memberships"; Microsoft "restore the database to a separate resource and selectively recover that tenant's data"; Google DR "Treat recovered data like production data"), but it is a different failure from an unscoped export query. Move to its own card or cut; it also pulls in the Google DR page, which says nothing about exports.
2. consider, check 3. PASS filters only by `tenant_id`. The Rule says "what the requesting principal may read", which also covers role and row ownership. Add an ownership predicate or say "tenant".
3. Confirmed: Atlassian (HTML and PDF: "Only those you can view"; XML: "Yes, they remain restricted"; "full XML file containing all the pages in the space, including those yo[u cannot view]"), Microsoft Power BI ("If you don't have permissions to the data, you can't export or open it"), OWASP (tenant filter on queries; row-level security), Microsoft multitenant storage guide. "Inside the export query" has OWASP and Microsoft storage guide as clear support; Atlassian shows the outcome, not the query. Count 2 clear plus Atlassian for the principal-scope clause. Atlassian page is Confluence 7.19 docs; fine for this behaviour.
Counts: scope to principal = Atlassian, Microsoft, OWASP (3); filter in the query = OWASP, Microsoft (2 clear, Atlassian outcome only). Treat as 3 only if "inside the query" is read loosely.

## svc-host-header-trust — PASS
1. Confirmed per clause:
   - Configured base URL: Fastly ("Avoid using the Host header value and its variants in application code"), Rails (mailer: "set the host value to your application's domain", "unlike controllers, the mailer instance doesn't have any context about the incoming request"), PortSwigger (3).
   - Allowlist: Django (`ALLOWED_HOSTS`, "to prevent HTTP Host header attacks"), Microsoft Kestrel (`AllowedHosts`, "Host headers aren't validated"), Rails (`config.hosts`), Laravel (`trustHosts`), Fastly ("Perform strict validation") (5).
   - Trusted proxy only: Microsoft (`KnownProxies`/`KnownNetworks`, "trust concerns with forwarded headers"), Django (`USE_X_FORWARDED_HOST`), PortSwigger, Fastly (4).
   - Duplicate Host: RFC 9112 "A server MUST respond with a 400 ... to any request message that contains more than one Host header field line". The note says IETF and Fastly only, which is cautious; the IETF text is a MUST.
2. consider, check 3. PASS mixes Django's `ALLOWED_HOSTS` with an invented `TRUSTED_PROXIES`; harmless pseudo-code, but name the setting per framework in a comment.
Counts: base URL 3; allowlist 5; trusted proxy 4.

## svc-mfa-step-up — ISSUES
1. consider, check 3. The Rule's "or a documented recovery path" is ambiguous. It reads as an alternative that satisfies the check for any sensitive action. The sources mean something narrower: a user who lost the factor needs a recovery path (NIST "Account Recovery"; OWASP recovery codes), and that path is itself a control. Reword: "Require fresh authentication with an already-bound factor ...; provide a documented recovery path for a user who has lost it."
2. consider, check 5. Severity `block`. The defect needs an already-stolen session to matter, so it is not directly exploitable on its own; `should-fix` fits the repo's definition better. Keep `block` only if the maintainer counts "persist after password change" as direct takeover.
3. Confirmed: OWASP MFA ("Require reauthentication with an existing enrolled factor before allowing changes. Do not rely solely on the active session, as it may be hijacked"; also lists password, email, disabling MFA), NIST 800-63B events ("When any new authenticator is bound ... requires authentication at either the maximum AAL currently available ... or the maximum AAL at which the new authenticator will be used"; notify on binding) and session ("SHALL NOT be considered at a higher AAL than the authentication event"), Microsoft protected actions (policy enforced "at the time the user attempts to perform the protected action"). Microsoft combined-registration page only covers Conditional Access for the registration page; Auth0 step-up page is JS-only (no text confirmed).
Counts: fresh auth before factor change = OWASP, NIST, Microsoft (3); sensitive actions (password, email) = OWASP, Microsoft protected actions, Auth0 unconfirmed (2 clear, 3 if Auth0's page says it); recovery path = OWASP, NIST (2; Auth0 recovery-codes page not cited).
Recommend stable only after the sensitive-actions and recovery-path clauses get a confirmed third org; otherwise draft (`orgs`).

## svc-oauth-code-flow-binding — ISSUES
1. act, check 3. The PASS is not a valid client flow. `request.args["redirect_uri"]` does not exist on an authorization response (which carries `code`, `state`, `iss`), so the assert would raise `KeyError` on a real callback. The token request in the PASS also omits `redirect_uri`, which RFC 6749 requires when it was sent in the authorization request. The FAIL has the same flaw ("redirect_uri comes from the request"). Show `redirect_uri` as a constant from config, sent in both the authorization request and the token exchange, and drop the assert on a request arg. Also show the `code_challenge`/`S256` on the authorization request, since the Rule leads with it.
2. consider, check 3. The Rule requires PKCE and `state`/`nonce` for every client. RFC 9700 §2.1.1: "Public clients MUST use PKCE ... For confidential clients, the use of PKCE is RECOMMENDED"; confidential OIDC clients "MAY use the nonce ... instead"; and "Clients that have ensured that the authorization server supports PKCE MAY rely on the CSRF protection provided by PKCE". OWASP OAuth2 says the same. The Rule is stricter than the sources. Say "PKCE, or nonce for a confidential OIDC client".
3. consider, check 1. "Send the exact registered `redirect_uri`" is an authorization-server requirement in RFC 9700 §2.1 ("authorization servers MUST utilize exact string matching"). Client-side support: Microsoft ("must exactly match one of the redirect URIs you registered") and OpenID Core. OWASP's OAuth2 sheet says only that servers must not allow `http` except loopback. Orgs: IETF (AS side), Microsoft, OpenID = 3, but the clause is worded for the client.
4. Confirmed: S256 (RFC 9700 "S256 is the only such method"; Microsoft sample uses `code_challenge_method=S256`; OWASP PKCE section), ID-token checks (OpenID Core `aud`, `exp`, `nonce`; Google verify page lists signature, `aud`, `iss`, expiry; OWASP Authentication "Validate ID Tokens ... iss, aud, signature, exp"), loopback port exception (RFC 9700 and RFC 8252).
Counts: PKCE S256 = IETF, OWASP, Microsoft (3); exact redirect = IETF, Microsoft, OpenID (3); state/nonce = IETF, OWASP, OpenID (3); ID-token checks = OpenID, Google, OWASP (3).

## svc-password-reset — ISSUES
1. act, check 1. Two of the six sources do not state the practice:
   - Symfony `reset_password.html` now redirects to `passwords.html#reset-password`, which says only "Using MakerBundle and SymfonyCastsResetPasswordBundle, you can create a secure solution". It says nothing about single use, expiry or hashing. The rest of that page is about hashing the new password.
   - Microsoft SSPR (`concept-sspr-howitworks`) covers authentication methods and registration; no token, session or expiry text.
2. act, check 2. Clauses with fewer than three confirmed orgs:
   - Single-use and short-lived: OWASP ("Single use and expire after an appropriate period"), Auth0 ("valid for one use only"; "URL Lifetime field determines how long the link is valid"). NIST describes the same for recovery codes ("SHALL invalidate that recovery code"), not reset links. 2 clear, 1 analogous.
   - Store only a hash: OWASP says "Stored in a secure manner, as discussed in the Password Storage Cheat Sheet"; NIST hashes recovery codes. No source says to hash the reset token. 0 to 2.
   - Revoke every session on success: Auth0 ("Resetting a user's password makes their session expire"), Microsoft MSRC (Unexpired Session Identifier Attack: "the password reset did not invalidate the attacker's session"), OWASP only says "Ask the user if they want to invalidate all of their existing sessions" in the normal flow and requires it after suspected compromise. 3, but OWASP's baseline is optional.
   - Revoke every other outstanding reset token: OWASP, after suspected compromise ("invalidate existing sessions and outstanding password reset and recovery links"); Auth0 invalidates earlier links when a newer one is sent, which is a different trigger. 1 to 2.
   Fix: either find third sources for hash-at-rest and revoke-others, or move those two clauses to Why and judge the Rule on single-use, short-lived and session revocation. Status should be draft (`orgs`) until then.
3. consider, check 3. OWASP makes session invalidation a user choice in the standard flow, so the Rule's "every session" is stronger than that source. Say so in the Counterpoint.
Counts: single-use + short-lived 2 (+1 analogous); hash 0 to 2; sessions 3 (OWASP optional); other tokens 1 to 2.

## svc-request-framing — PASS
1. Confirmed per clause:
   - Reject or strip one framing field: RFC 9112 ("MAY reject ... or process ... in accordance with the Transfer-Encoding alone. Regardless, the server MUST close the connection"), Cloudflare (400 "Cloudflare follows the RFC"), Envoy (`allow_chunked_length`: "By default such messages are rejected"), PortSwigger, Fastly, Kestrel ("Request smuggling protection ... per RFC 9112 Section 6.3") (6).
   - Strict parsing, no leniency flag: RFC 9112 ("A server MUST reject, with a response status code of 400, any received request message that contains whitespace between a header field name and colon"), Node (`insecureHTTPParser` "Using the insecure parser should be avoided. Default: false"), Envoy, Kestrel (4).
   - HTTP/2 downgrade in Why: PortSwigger and Fastly, as the note says.
2. FAIL byte count checks out (`0\r\n\r\nGET /admin` = 15 bytes). The CL.TE description matches the PortSwigger and Fastly terminology.
Counts: framing field 6; strict parsing 4.

## svc-saml-assertion-binding — PASS
1. Confirmed: OASIS profiles ("Verify that the InResponseTo attribute in the bearer SubjectConfirmationData equals the ID"; "An unsolicited Response MUST NOT contain an InResponseTo attribute"; "The service provider MUST ensure that bearer assertions are not replayed, by maintaining the set of used ID values"), OWASP SAML (ignore `KeyInfo` and take the key from the IdP; never `getElementsByTagName` for security elements; validate `Destination`, `Audience`, `NotBefore`/`NotOnOrAfter`, `Recipient`, `InResponseTo`), NIST 800-63C ("This signature SHALL cover the entire assertion, including its identifier, issuer, audience, subject, and time validity window"; "All RPs SHALL check that the audience of an assertion contains an identifier for their RP"), python3-saml ("Avoiding Replay attacks ... the ID of the current Message/Assertion does not exists in the list of the ones already processed"; wrapping CVE note). Microsoft's page shows the fields in IdP-emitted samples only; it does not instruct an SP. Not counted.
2. consider, check 6. The Rule is one very long sentence of seven checks. It passes the "failable" test, but split the ID/replay check into its own sentence for readability.
Counts: signature over the read element with a pinned key = OWASP, NIST, python3-saml, OASIS (4); audience/recipient = OASIS, OWASP, NIST (3); InResponseTo = OASIS, OWASP (2) plus Microsoft sample (not counted); NotOnOrAfter = OASIS, OWASP (2); replay set = OASIS, python3-saml, OWASP (3).
Note: the InResponseTo and NotOnOrAfter clauses have only two orgs that state them, and OWASP restates OASIS. Under the "every clause needs its own three" bar this card is borderline; NIST 63C names audience and time validity but not InResponseTo. Recommend keeping stable only if the maintainer accepts the five checks as one clause ("validate the SubjectConfirmation and Conditions"), otherwise draft (`orgs`).

## svc-soft-delete-default — ISSUES
1. consider, check 1. Why-only claims are not backed by the cited pages. S3: "keeps a delete marker over the old bytes until a lifecycle rule expires it". The DeleteMarker page says nothing about lifecycle rules; it says delete markers remain listed by `ListObjectVersions`. Also, expiring a delete marker does not remove noncurrent versions, which need `NoncurrentVersionExpiration`. PostgreSQL: vacuum reclaims dead row versions, which concerns hard deletes and updates, not why a soft-deleted row (still a live row) stays readable.
2. consider, check 6. Cut both sentences. They back neither Rule clause and the service page is over its size cap. If kept, say "S3 keeps earlier versions until they are deleted by version ID or expired by a noncurrent-version rule".
3. Confirmed for the Rule: Microsoft EF ("filter out soft-deleted rows by default, while still allowing you to access them in specific places by disabling the filter"), Laravel ("automatically be excluded from all query results"; `withTrashed()`), Sequelize ("findByPk ... will be null as if that record didn't exist ... pass the paranoid: false option"). These are feature docs rather than recommendations, which is a thin reading of PROMOTION rule 3, but the three frameworks each make default-exclude with explicit opt-in the design, so I count them.
Counts: default filter + explicit opt-in = Microsoft, Laravel, Sequelize (3).

## svc-tenant-id-in-telemetry — ISSUES
1. act, check 2. The Rule ("Put the tenant id on every log and audit record") has two confirmed orgs:
   - AWS SaaS Lens: "both services need to inject tenant context into their log messages and metric events".
   - OWASP: "Include server-verified tenant context in tenant-scoped security and audit events".
   - Microsoft storage guide: "consider how your solution reports metrics and whether it can easily link metrics to the tenant that triggered the request". A consideration for metrics, not a rule for logs and audit records. Weak.
   - Google GKE multi-tenant logging routes logs to per-tenant buckets by namespace label. It backs the Counterpoint ("a store per tenant is stronger"), not the Rule.
   Fix: find a third source (for example a logging or SaaS vendor that adds tenant id to every record) or set `status: draft` with `lacks: orgs`.
2. consider, check 6. The last two Why sentences are about cache keys ("Put the same discriminator in a cache key too"). OWASP supports it, but the card is about telemetry; cut or move to a cache card.
3. Verified: the "centralized audit store is acceptable only when read access enforces tenant scope" sentence matches OWASP ("A centralized audit store is acceptable when read access enforces tenant scope").
Counts: tenant id on every log and audit record = AWS, OWASP (2 confirmed, Microsoft weak).

## svc-webhook-replay-window — ISSUES
1. act, check 3. The PASS defeats itself. The HMAC covers only `body`; the timestamp in `X-Timestamp` is a separate header outside the signature. An attacker who captured a request can resend the same body and signature with a fresh timestamp and pass both checks. Slack signs `v0:<timestamp>:<body>`, and Svix and Stripe include the timestamp in the signed payload. Fix the PASS to verify the HMAC over `f"{ts}.{body}"`, then check `ts`. Add "covered by the signature" to the Rule: "Reject an inbound signed message whose signed creation time is outside a short tolerance."
2. act, check 1. The Counterpoint says "RFC 9421 requires the check and leaves the number to the application". RFC 9421 §3.2.1 lists "Enforcing a maximum signature age from the time of the `created` timestamp" among "non-normative examples of additional requirements an application might define" (applications "MAY impose requirements above and beyond"). §7.2.2 says the signer "can provide a timestamp ... limiting the utility of a captured signature value". It is a permitted application check, not a required one. Correct the sentence.
3. act, check 1. The Stripe URL `https://docs.stripe.com/webhooks/signature` now redirects to `/events/manage-webhook-endpoints`, which has no replay or tolerance text. The practice is on `https://docs.stripe.com/webhooks` ("Preventing replay attacks ... Our libraries have a default tolerance of 5 minutes ... Don't use a tolerance value of 0"). Replace the URL.
4. Confirmed: Svix ("compare this timestamp against your system timestamp and make sure it's within your tolerance in order to prevent timestamp attacks"), Slack ("verify that the timestamp does not differ from local time by more than five minutes ... could be a replay attack"), Stripe (at the corrected URL). IETF counts as a weak fourth (permits it).
Counts: tolerance on creation time = Svix, Slack, Stripe (after URL fix) (3), IETF weak. The "five minutes" in the PASS matches Slack and Stripe.

## Summary table

| id | verdict | confirmed orgs per clause | recommended status |
|---|---|---|---|
| code-workflow-supply-chain | PASS | pin 3 (GitHub, OpenSSF, StepSecurity); boundary 3 (GitHub, OpenSSF, GitLab; OWASP weak) | stable |
| svc-api-cache-control | PASS | edge-override 4; Content-Type 3 | stable |
| svc-dlq | ISSUES | DLQ+replay 2 confirmed (AWS, Notion), Netflix/Uber UNFETCHED, Dropbox is a proposal; isolation 3 (descriptive) | stable only if Netflix or Uber is confirmed; otherwise draft (`orgs`) |
| svc-rate-limit-quota | PASS | per-tenant quota 3 (NIST does not count) | stable |
| svc-session-lifecycle | PASS | host-scope 2 (Why only) | stable |
| code-workload-identity | PASS | exchange 3; pin 3 | stable |
| fn-header-value-encoding | PASS | API 4; reject/encode 4 | stable |
| svc-account-linking | ISSUES (consider only) | prove both 3; key on iss+sub 4 | stable |
| svc-api-key-scope | ISSUES | scopes 4; lifetime 2 + 1 weak; rotate/revoke 4 | draft (`orgs`) unless lifetime gets a third source or moves to Why |
| svc-cache-key-completeness | ISSUES | key completeness 3 (Microsoft does not count); strip unkeyed 3 | stable (drop Microsoft; cross-link `svc-api-cache-control`) |
| svc-decompression-cap | ISSUES | cap output 3 | stable after fixing the 1 KB to 1 GB claim |
| svc-export-scope | PASS | principal scope 3; filter in query 2 clear | stable |
| svc-host-header-trust | PASS | base URL 3; allowlist 5; trusted proxy 4 | stable |
| svc-mfa-step-up | ISSUES | fresh auth 3; sensitive actions 2; recovery path 2 | draft (`orgs`) unless a third source is found for the last two |
| svc-oauth-code-flow-binding | ISSUES | PKCE 3; redirect 3; state/nonce 3; ID token 3 | stable after fixing the PASS example |
| svc-password-reset | ISSUES | single-use 2 (+1 analogous); hash 0 to 2; sessions 3; other tokens 1 to 2 | draft (`orgs`) |
| svc-request-framing | PASS | framing field 6; strict parsing 4 | stable |
| svc-saml-assertion-binding | PASS | signature 4; audience 3; InResponseTo 2; NotOnOrAfter 2; replay 3 | stable if the checks count as one clause; otherwise draft (`orgs`) |
| svc-soft-delete-default | ISSUES | default filter 3 | stable after cutting the PG/S3 sentences |
| svc-tenant-id-in-telemetry | ISSUES | tenant id on records 2 (+1 weak) | draft (`orgs`) |
| svc-webhook-replay-window | ISSUES | tolerance 3 after the Stripe URL fix | stable after fixing the PASS, the Counterpoint and the URL |

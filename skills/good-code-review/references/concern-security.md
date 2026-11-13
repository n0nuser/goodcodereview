# security cards

Every stable card that lists the `security` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-name-attack-surface` [should-fix] {security, process} change.md:L316+27: List any new attack surface in the description.

## function

- `fn-bounded-read-fails-at-cap` [should-fix] {correctness, reliability, security} function.md:L60+36: When a size cap is reached, return an error; never hand back the first N bytes as if they were the whole input.
- `fn-confine-file-path` [block] {security} function.md:L182+27: Resolve the final path and check that it stays inside the intended base directory before using it.
- `fn-constant-time-secret-compare` [should-fix] {security} function.md:L210+31: Compare a secret, token or MAC with the platform's constant-time function, never with `==` or `!=`.
- `fn-csprng-for-secrets` [block] {security} function.md:L242+27: Draw every security-relevant random value from the platform CSPRNG.
- `fn-header-value-encoding` [block] {security} <server> function.md:L616+31: Set every response header through the framework's header API, never by writing to the connection, and reject or encode CR and LF in any request-derived value.
- `fn-jwt-verify-pinned` [block] {security} <server> function.md:L768+29: Verify the signature against a fixed list of accepted algorithms, and check `iss` and `aud`, before reading any claim.
- `fn-link-url-scheme-allowlist` [should-fix] {security} <ui> function.md:L904+28: Parse a URL that comes from data and allow only `https:` (and `http:` or `mailto:` where needed) before you set it as a link target.
- `fn-mask-credentials-in-output` [should-fix] {security, usability} <cli> function.md:L933+34: Mask credentials in list, show and debug output (keep only the last four characters), and print a full value only behind an explicit flag.
- `fn-no-eval-untrusted` [block] {security} function.md:L1120+27: Never pass untrusted text to `eval`, `exec`, `new Function`, or a template compiler. Pass it to a fixed template or a parser as data.
- `fn-no-mass-assignment` [block] {security} <server> function.md:L1202+29: Bind request data to a DTO or an explicit field allowlist, never straight onto the model.
- `fn-no-native-deserialise-untrusted` [block] {security} function.md:L1232+27: Parse untrusted input with a data-only format, never with a native object deserialiser.
- `fn-no-prototype-pollution` [block] {security} function.md:L1292+35: Never write an untrusted key into a plain object. Use a `Map`, an object from `Object.create(null)`, or an allowlist of keys.
- `fn-no-raw-html-sink` [block] {security} <ui,server> function.md:L1328+29: Write untrusted text through an encoding sink (`textContent`, auto-escaped template), never through a raw HTML sink.
- `fn-no-shell-with-input` [block] {security} function.md:L1358+27: Start processes with the program and each argument as separate list items, and never through a shell string.
- `fn-object-level-authz` [block] {security} <server> function.md:L1386+29: Check that the caller may act on the specific record before returning or changing it.
- `fn-password-slow-hash` [block] {security} <server> function.md:L1446+28: Hash passwords with Argon2id (or scrypt, bcrypt, PBKDF2) and a per-password salt from the library.
- `fn-redirect-target-allowlist` [should-fix] {security} <server> function.md:L1475+29: Redirect only to a local path or to a host on a server-side allowlist, never to a URL taken from the request as is.
- `fn-response-fields-explicit` [should-fix] {security, compatibility} <server> function.md:L1636+28: Return a response type that lists each field, never the stored model or a generic dump of it.
- `fn-tls-verify-on` [block] {security} function.md:L1821+26: Leave certificate and hostname verification on in every environment that ships.
- `fn-xml-no-external-entities` [block] {security} function.md:L1886+27: Parse untrusted XML with external entity resolution turned off, for example through a hardened parser such as `defusedxml`.

## module

- `mod-vetted-crypto-only` [block] {security} module.md:L633+27: Encrypt with an authenticated mode such as AES-GCM, and never reuse a nonce under one key.

## service

- `svc-account-linking` [block] {security} <server> service.md:L3+33: Link a federated identity to an existing account only after proving control of both, and key the link on the pair `iss` and `sub`, never on an unverified email or another profile claim.
- `svc-api-cache-control` [should-fix] {performance, security} <server> service.md:L37+35: Set an explicit `Cache-Control` on every response a cache may store, use `private` or `no-store` for user-specific data, add `Vary` for any request header that changes the body, keep the origin's `Cache-Control` authoritative at the edge (no minimum TTL or force-cache override), and decide cacheability by the response `Content-Type`, not the URL extension.
- `svc-api-key-scope` [should-fix] {security} <server> service.md:L229+30: Issue each API key with the narrowest scopes and a bounded lifetime, and rotate or revoke it after any exposure.
- `svc-auth-throttle-generic-errors` [block] {security} <server> service.md:L443+29: Limit failed attempts per account, and return the same message and status code whether or not the account exists.
- `svc-authn-by-default` [should-fix] {security} <server> service.md:L473+32: Require authentication on every route by default, and mark each public route by name.
- `svc-authz-central-deny-default` [block] {security} <server> service.md:L506+29: Route every request through one authorization layer that denies when no rule allows it.
- `svc-bound-client-controlled-sizes` [should-fix] {security} <server> service.md:L571+29: Cap every client-controlled size and count on the server: body bytes, string length, array items, page size and batch size.
- `svc-cache-key-completeness` [block] {security} <server> service.md:L638+37: Key every request input that can change the response, and strip any other request value before it reaches a cached body.
- `svc-cors-allowlist` [should-fix] {security} <server> service.md:L831+30: Allow cross-origin access only to a fixed list of named origins, and never echo the request `Origin` header back unchecked.
- `svc-csp-strict-script-src` [should-fix] {security} <server> service.md:L862+27: Send a `Content-Security-Policy` whose `script-src` uses a per-response nonce or script hashes, with `object-src 'none'` and `base-uri 'none'`.
- `svc-csrf-state-changing` [block] {security} <server> service.md:L890+29: Require a CSRF token (or an equivalent header check) on every cookie-authenticated request that changes state, and never change state on GET.
- `svc-decompression-cap` [should-fix] {security, performance} <server> service.md:L920+28: Cap the decompressed output of every decoder, and set the cap on the output rather than the compressed input.
- `svc-export-scope` [block] {security} <data> service.md:L1004+28: Scope an export to what the requesting principal may read.
- `svc-fail-closed-defaults` [should-fix] {security} <server> service.md:L1033+42: Ship every security control switched on, with an empty allow-list denying everything.
- `svc-host-header-trust` [block] {security} <server> service.md:L1076+30: Build absolute URLs from configured values, answer only for a `Host` on an allowlist, and take `X-Forwarded-*` values only from a trusted proxy.
- `svc-mfa-step-up` [should-fix] {security} <server> service.md:L1215+33: Require a fresh authentication with an already-bound factor before sensitive actions and before adding, replacing or removing an MFA factor; an existing session alone is not enough.
- `svc-no-secrets-in-url` [should-fix] {security} <server> service.md:L1279+32: Send tokens, keys, passwords, and personal data in a header or the request body, never in the path or query string.
- `svc-oauth-code-flow-binding` [block] {security} <server> service.md:L1312+36: Finish the authorization-code flow with PKCE and a challenge method that keeps the verifier out of the authorization request (`S256`), send the exact registered `redirect_uri` (a native app on the loopback interface may vary the port), and reject the response unless this transaction's `state` or OIDC `nonce` matches and the ID token's signature, `iss`, `aud` and `exp` check out.
- `svc-password-reset` [block] {security} <server> service.md:L1349+34: Make the reset token single-use and short-lived, and on success revoke every session.
- `svc-rate-limit-quota` [should-fix] {security, reliability} <server> service.md:L1384+27: Enforce a per-tenant quota on shared APIs and queues.
- `svc-request-framing` [block] {security} <server> service.md:L1450+42: Reject a request that carries both `Transfer-Encoding` and `Content-Length`, or remove one field at the first hop, and parse header framing strictly rather than with a leniency flag.
- `svc-saml-assertion-binding` [block] {security} <server> service.md:L1556+38: Verify the XML signature over the assertion you read, with the IdP's configured key rather than a key carried in the response, then require the assertion's `Audience` and its bearer `SubjectConfirmationData` `Recipient` to name this SP, the response `Destination` to be this endpoint, `InResponseTo` to match your request (absent for an IdP-initiated response), `NotOnOrAfter` to be current, and the assertion ID to be unseen. These are one step, verify the assertion, and each check is cited.
- `svc-session-lifecycle` [block] {security} <server> service.md:L1595+28: Issue a new session ID at login, and set `Secure`, `HttpOnly` and `SameSite` on the session cookie.
- `svc-soft-delete-default` [should-fix] {security, correctness} <data> service.md:L1655+30: Filter soft-deleted rows out of every read path by default, and make a read that includes them an explicit call.
- `svc-sqli-authn` [block] {security} <server,data> service.md:L1686+28: Pass untrusted data to queries as bound parameters, never by string concatenation or formatting.
- `svc-tenant-id-in-telemetry` [should-fix] {security, observability} <server> service.md:L1745+28: Put the verified tenant id on every tenant-scoped log, metric and audit record.
- `svc-tls-modern-only` [should-fix] {security} <server> service.md:L1805+28: Accept only TLS 1.2 and TLS 1.3 on servers.
- `svc-token-revocation` [should-fix] {security} <server> service.md:L1834+31: Revoke the user's refresh tokens on the server at logout and when the account is disabled, and make access tokens expire quickly or check them against a revocation record.
- `svc-update-verify-provenance` [should-fix] {security} service.md:L1909+37: Verify a downloaded update against a signature, an attestation or a pinned key, or against a checksum that reached you by another route than the file; a checksum fetched from the same host as the file does not count.
- `svc-upload-validate-store` [block] {security} <server> service.md:L1947+28: Allowlist the file type, cap the size, and store each upload under a generated name where the server will not execute it.
- `svc-webhook-replay-window` [should-fix] {security} <server> service.md:L1976+33: Reject an inbound signed message whose creation time is outside a short tolerance, and sign that time with the body so it cannot be swapped.

## system

- `sys-agent-tool-least-privilege` [block] {security, process} system.md:L3+26: Give the agent only the narrow tools and the minimal credentials its task needs.
- `sys-pii-minimise-retention` [should-fix] {security} system.md:L347+27: Give every store of personal or sensitive data a retention period, and delete or anonymise the data when it ends.
- `sys-prompt-injection` [block] {security} system.md:L375+25: Validate model output deterministically before code acts on it.
- `sys-secrets-and-errors` [block] {security, correctness} system.md:L401+30: Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.
- `sys-ssrf` [block] {security} system.md:L432+27: Fetch a user-supplied URL only when its host matches a server-side allowlist.

## codebase

- `code-dependency-licence-sbom` [should-fix] {security} codebase.md:L173+26: Generate an SBOM, and scan dependencies for known vulnerabilities on every change or on a schedule. Each ask is judged separately: name which one failed on the FAIL line.
- `code-dependency-pinning` [block] {security} codebase.md:L200+42: Commit a lockfile with hashes and install from it in CI.
- `code-secret-scan` [block] {security, process} codebase.md:L470+26: Scan for committed credentials, and treat any hit as leaked: revoke and replace it first. With no scanner present and no secret found, the FAIL is the missing control; evidence is "absent in <paths>". A platform scanner (GitHub secret scanning with push protection, GitLab secret detection) counts when it is enabled on the repo and covers history.
- `code-vuln-remediation-window` [should-fix] {security, process} codebase.md:L580+27: Write down how long a known-vulnerable dependency may stay unfixed and fix or upgrade it inside that window.
- `code-workflow-supply-chain` [block] {security, process} codebase.md:L608+49: Pin every CI action to a full commit SHA, and keep code from an unreviewed change out of any job that holds secrets or can deploy.
- `code-workload-identity` [should-fix] {security} codebase.md:L658+43: Exchange the platform's OIDC token for a short-lived cloud credential, and pin the trust policy to the workload.

# Security gaps O: third organisations for clauses G1/G2/G3/G4/G6 and H2/H3/H5

Checked 2026-11-06 against the clauses named in the task. Every page below was fetched and read; quotes are verbatim, 1-2 short ones per row. "New for this clause" means the organisation was not already listed for **that clause** in `sec-classes-G.md` or `sec-classes-H.md`; an organisation already used for a different clause of the same class (Google in G3, Fastly in G4, Microsoft in G4, IETF in G1/G4) is still new for the clause it is cited under. Organisation counting follows `docs/PROMOTION.md`.

This pass fetched about 36 URLs, of which 9 were 404 or a redirect to a different page; those are listed under "Also read, no rule" and are not counted. It went slightly past the brief's 30-page cap because the first hits for Akamai, Google cookie prefixes and Fastly cache deception were 404 and needed replacements.

**Bottom line.** Five of the eight clauses now reach three organisations: G2's unkeyed-header clause and static-only clause, G3's "CDN must not override origin" and "no extension-only caching" clauses, G4's "configured base URL" clause, G6's host-only/`__Host-` clause (with one of the three being an IETF draft), H3's factor-change re-authentication, H5's hashed reset token (one source is adjacent), and H2's replay cache and `Destination`. Two clauses stay at two organisations and should move to `Why`: G1's "no HTTP/1 downgrade" and G4's "reject duplicate Host". G3's "origin and cache agree on path interpretation" stays at one.

New prefix `tools/orgs.py` needs before a card can cite it: `github.com/SAML-Toolkits/` → a new `saml-toolkits` org (display "python3-saml (SAML-Toolkits)"). `fastly.com`, `laravel.com`, `symfony.com`, `guides.rubyonrails.org`, `envoyproxy.io`, `cloud.google.com`, `docs.aws.amazon.com`, `learn.microsoft.com`, `docs.djangoproject.com`, `datatracker.ietf.org`, `developers.cloudflare.com` and `rfc-editor.org` are already mapped. `httpd.apache.org` is **not** mapped; add it only if a card cites the Apache page listed below.

---

## O1 — G1 request smuggling: normalise at the front end, reject at the back end; no HTTP/1 downgrade

**Candidate Rule.** Normalise an ambiguous request at the first hop and reject it at the next, or close the connection; never downgrade an HTTP/2 request into an unchecked HTTP/1.1 one.

**Level.** service (system when the chain has more than one proxy hop). **Tool gate.** none found; the controls are parser and proxy configuration.

**Existing card.** None. `fn-bounded-read-fails-at-cap` bounds how much a reader takes, not where one message ends. No card mentions `Content-Length`, `Transfer-Encoding`, chunked framing, desync or request smuggling.

**FAIL/PASS.** FAIL: a front end forwards a request carrying both `Content-Length` and an obfuscated `Transfer-Encoding` to a keep-alive backend. PASS: the front end normalises or returns 400, the backend rejects anything still ambiguous and closes the connection, and an HTTP/2 front end validates the rewritten HTTP/1.1 request.

1. https://www.fastly.com/learning/security/what-is-http-request-smuggling (org: Fastly). New for this clause. Both halves, in its own prevention list: "Front-end servers receiving both CL and TE headers should normalize requests to a single mechanism for determining the length of a request, and remove the extraneous headers to prevent origins from receiving ambiguous requests." On the downgrade path: "Front-end servers downgrading to HTTP/1.1 should validate that rewritten requests are not malformed or ambiguous." It also states the vendor default: "Fastly either rejects or normalizes ambiguous requests at the Edge." Backs G1, and is the second organisation (after PortSwigger) for the downgrade clause.

2. https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/http/header_validators/envoy_default/v3/header_validator.proto.html (org: Envoy). New for this clause. The default is rejection, and the opt-out is named as a smuggling risk: "Allows Envoy to process HTTP/1 requests/responses with both Content-Length and Transfer-Encoding headers set. By default such messages are rejected, but if option is enabled - Envoy will remove the Content-Length header and process the message." and "Enabling this option might lead to request smuggling vulnerabilities, especially if traffic is proxied via multiple layers of proxies." The validator's summary lists "Validation of HTTP/1 requests with both Content-Length and Transfer-Encoding headers." Backs G1's reject clause and supplies a named configuration default (`allow_chunked_length`, default false).

3. https://developers.cloudflare.com/support/troubleshooting/http-status-codes/4xx-client-error/error-400/ (org: Cloudflare). New for G1 (Cloudflare was already used for G2/G3). States the edge behaviour: "If the request contains both `Content Length` and `Transfer Encoding` chunked, these two framing methods contradict each other." and "Cloudflare follows the RFC and an `HTTP Error 400` will be returned." Backs G1's reject-at-the-front-end clause.

**Count for O1.** "Normalise at the front end and reject at the back end" now has 5 organisations (PortSwigger, IETF, Fastly, Envoy, Cloudflare). "No HTTP/1 downgrade" still has 2 (PortSwigger, Fastly): Fastly says validate the rewritten request rather than disable downgrading, so the clause should read "validate on downgrade", or move to `Why`. Confidence high on the rule, low on the downgrade wording.

---

## O2 — G2 cache key completeness: no unkeyed input in a cached response; static assets only by default

**Candidate Rule.** Key every request input that can change the response, never let an unkeyed header or GET body reach a cached body, and cache only static content unless the origin says otherwise.

**Level.** service. **Tool gate.** none found; cache-key and cache-mode configuration are the controls.

**Existing card.** `svc-api-cache-control` (stable) covers `Cache-Control` and `Vary`, which is the origin's half. Missing: the cache key itself, unkeyed headers and GET bodies reaching the body, and the CDN's default cache mode.

**FAIL/PASS.** FAIL: the origin echoes `X-Forwarded-Host` or a GET body into the page while the CDN keys only on the URL. PASS: the edge strips the unkeyed header (or puts it in the key), GET bodies do not change the body, and only static MIME types are cached without explicit origin directives.

4. https://www.fastly.com/documentation/guides/full-site-delivery/caching/preventing-cache-poisoning/ (org: Fastly). New for this clause. Names the exact failure and the fix: "If your site's Fastly configuration passes one of these headers to your backend and does not factor the contents of it into the effective edge cache key (for example, explicitly or via the `Vary` HTTP response header), an attacker could potentially cause the edge to store a response with arbitrary content inserted into a victim's cache." The remedy is "strip or normalize the values of X-Forwarded-Host, X-Rewrite-URL, or X-Original-URL in VCL", or "the values could be included in your cache key or Vary header to prevent caching of content across security domains." Backs G2's unkeyed-header clause.

5. https://cloud.google.com/cdn/docs/caching (org: Google). New for this clause (Google was already used for G3). The default cache mode is static-only: "`CACHE_ALL_STATIC` | Automatically caches successful responses with static content that isn't otherwise non-cacheable. Origin responses that set valid caching directives are also cached. This behavior is the default for Cloud CDN-enabled backends created by using the Google Cloud CLI or the REST API." and "Other content types, such as HTML (`text/html`) and JSON (`application/json`), are not cached by default for successful responses." This is a documented vendor default with a number-free but explicit type list. Backs G2's static-only clause and G3's extension clause.

6. https://www.fastly.com/documentation/guides/full-site-delivery/caching/manipulating-the-cache-key/ (org: Fastly, same org as #4). Says to key the value rather than ignore it: "If your origin uses special values (e.g., request headers) to select content for users or to otherwise direct requests to appropriate security domains, consider including those values in your cache key or Vary header." and "Doing so will prevent you from accidentally caching content across security domains and could prevent malicious attackers from poisoning your cache." Backs G2's keying clause (extra support; it does not add a second organisation).

**Count for O2.** "Do not reflect unkeyed headers or GET bodies" now has 3 (Cloudflare, PortSwigger, Fastly). "Cache only static assets by default" now has 3 (Cloudflare, PortSwigger, Google). Confidence high on both; note that Fastly's own cache-control page says "most content is cacheable by default", so the static-only clause is a recommendation, not a vendor-wide default.

---

## O3 — G3 cache deception: the cache rule must not override the origin; no extension-only cacheability

**Candidate Rule.** Keep the origin's `Cache-Control` authoritative at the edge, and decide cacheability from the response `Content-Type`, not from the URL extension.

**Level.** service. **Tool gate.** none found; the controls are the origin header and the CDN cache policy.

**Existing card.** `svc-api-cache-control` (stable) already owns the `private`/`no-store` half as its Rule. Missing: cache deception proper (a dynamic path served as `/foo.css` and cached by extension), the rule that a CDN's cache rule must not override the origin header, and path-interpretation agreement.

**FAIL/PASS.** FAIL: the CDN sets a minimum TTL of an hour over the origin's `private, no-store`, and it caches `/account` when requested as `/account/x.css` because of the extension. PASS: the CDN's minimum TTL is 0 (or the policy honours origin headers), `private`/`no-store` survives, and a response whose `Content-Type` does not match the extension is not stored.

7. https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html (org: AWS). New for this clause. Documents both the pass and the fail as configuration: with a minimum TTL of 0, "CloudFront and browsers respect the headers"; with a minimum TTL above 0, "CloudFront uses the cache policy's minimum TTL, even if the `Cache-Control: no-cache`, `no-store`, and/or `private` directives are present in the origin headers." It also records the unsafe default: "If you opt out of using a cache policy, the default TTL (Time to Live) is 24 hours". Backs G3's "the CDN must not override the origin" clause and names the configuration value to check (`Minimum TTL = 0`).

8. https://cloud.google.com/cdn/docs/caching (org: Google, same page as #5, new for this clause). The extension rule is explicit: "Cloud CDN doesn't use file extensions in the URL path to determine whether a response is cacheable because many valid cacheable responses aren't reflected in URLs." It also names the override mode: "`FORCE_CACHE_ALL` | Unconditionally caches successful responses, overriding any cache directives set by the origin." Backs G3's extension clause.

**Count for O3.** "The CDN must not override the origin's `Cache-Control`" now has 3 (PortSwigger, Microsoft, AWS). "Do not decide cacheability by extension alone" now has 3 (Cloudflare, PortSwigger, Google). "The origin and the cache agree on path interpretation" stays at 1 (PortSwigger) and belongs in `Why`. Confidence high on the private/`no-store` half, medium on the deception half.

---

## O4 — G4 Host trust: absolute URLs from configuration, duplicate Host rejected

**Candidate Rule.** Build absolute URLs (reset links, mailers) from configured values rather than the `Host` header, allowlist the Host values the app will answer, and reject a request with more than one `Host`.

**Level.** service. **Tool gate.** none found; framework host filtering and the mailer/base-URL setting are the controls.

**Existing card.** None for this class. `fn-redirect-target-allowlist` (stable) checks the *target* of a redirect, not how a URL or reset link is built. `sys-ssrf` covers the server following a URL, not the server publishing one.

**FAIL/PASS.** FAIL: `link = "https://" + request.headers["Host"] + "/reset?token=" + token` with no host allowlist. PASS: `link = f"{settings.PUBLIC_BASE_URL}/reset?token={token}"`, a framework host allowlist is configured, and two `Host` headers get 400.

9. https://guides.rubyonrails.org/action_mailer_basics.html (org: Ruby on Rails). New for this clause (Rails was not in G4). The config-based base URL is the documented practice: "In order to add URLs to your mailer, you need to set the host value to your application's domain first. This is because, unlike controllers, the mailer instance doesn't have any context about the incoming request." The setting is `config.action_mailer.default_url_options = { host: "example.com" }`, and the guide adds "Once the host is configured, it is recommended that email views use the `*_url` with the full URL". Backs G4's "build absolute URLs from configuration" clause (for mailer/reset links).

10. https://guides.rubyonrails.org/configuring.html (org: Ruby on Rails, same org as #9). Host allowlisting with an explicit production warning: "`config.hosts` ... An array of strings, regular expressions, or IPAddr used to validate the Host header. Used by the `HostAuthorization` middleware to help prevent DNS rebinding attacks." and "In other environments `Rails.application.config.hosts` is empty and no Host header checks will be done. If you want to guard against header attacks on production, you have to manually permit the allowed hosts". Backs G4's allowlist clause (already at 4) and is the production-default caveat.

11. https://laravel.com/docs/12.x/passwords (org: Laravel). New for G4. States the fail behaviour and ties it to password reset: "By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header. In addition, the `Host` header's value will be used when generating absolute URLs to your application during a web request." The fix is the `trustHosts` middleware: "This is particularly important when your application offers password reset functionality." Backs G4's allowlist clause and the reset-poisoning risk. It does **not** back "build URLs from configuration" (Laravel's default is the opposite).

**Count for O4.** "Build absolute URLs from configuration" now has 3 (PortSwigger, Fastly, Rails). "Allowlist the Host and reject unknown" now has 6 (PortSwigger, Fastly, Django, Microsoft, Rails, Laravel; Apache would make 7 — IETF is not counted here because RFC 9112 rejects a missing or duplicate Host, not an unknown one). "Reject duplicate Host" still has 2 (IETF, Fastly) and should move to `Why`. "Honour forwarded headers only from a trusted proxy" stays at 4. Confidence high on the allowlist and trusted-proxy clauses, medium on the configured-base-URL clause, low on duplicate Host.

---

## O5 — G6 cookie scope: omit `Domain`, use the `__Host-` prefix

**Candidate Rule.** Set session cookies host-only (omit `Domain`), use the `__Host-` prefix, and keep `Secure`, `HttpOnly`, `SameSite` and `Path=/`.

**Level.** service. **Tool gate.** none found; the `Set-Cookie` header is the control. A header assertion in the login test is the practical gate.

**Existing card.** `svc-session-lifecycle` (stable) already has `Secure`, `HttpOnly` and `SameSite` in its Rule and `__Host-sid` in its PASS example, but not host-only scope or the prefix in the Rule. Missing from the Rule: omit `Domain`, use `__Host-`, and the subdomain-injection reason.

**FAIL/PASS.** FAIL: `Set-Cookie: sid=...; Domain=example.com; SameSite=None` on an app that shares the domain with user content. PASS: `Set-Cookie: __Host-sid=...; Secure; HttpOnly; SameSite=Lax; Path=/` with no `Domain`.

12. https://datatracker.ietf.org/doc/html/draft-ietf-httpbis-rfc6265bis (org: IETF; **an active Internet-Draft**, `draft-ietf-httpbis-rfc6265bis-22`, not an RFC). New for this clause. Host-only scope: "If the server omits the Domain attribute, the user agent will return the cookie only to the origin server." The prefix: "If a cookie's name begins with a case-sensitive match for the string `__Host-`, then the cookie will have been set with a `Secure` attribute, a `Path` attribute with a value of `/`, and no `Domain` attribute." and "The lack of a `Domain` attribute ensures that the cookie's host-only-flag is true". Backs G6's missing clause.

**Count for O5.** "Omit `Domain`; use `__Host-`" now has 3 **including a draft** (Mozilla, OWASP, IETF draft); without the draft it is still 2. The draft's own status page says "It is inappropriate to use Internet-Drafts as reference material or to cite them other than as 'work in progress.'" A card that cites it must say so, and the clause is not yet at three stable organisations. I found no Google page (two web.dev/Chrome URLs 404), and the Microsoft, Django and Rails pages I opened do not state host-only scope (see "Also read"). Confidence medium; hold the clause until a third stable source appears.

---

## O6 — H3 MFA: re-authenticate with an existing factor before adding or removing a factor

**Candidate Rule.** Before adding, replacing or removing an MFA factor, require a fresh authentication with a factor already bound to the account; an existing session alone must not be enough.

**Level.** service. **Tool gate.** none found; an integration test (password-only session gets a step-up challenge on the factor-change route) is the gate.

**Existing card.** None. `svc-session-lifecycle` covers login fixation and timeouts. `svc-auth-throttle-generic-errors` covers failed attempts and generic errors. Neither covers MFA enrolment or step-up.

**FAIL/PASS.** FAIL: `@login_required def add_phone(): user.phone = request.form["phone"]` — an old password-only session can replace the second factor. PASS: a step-up check requires an existing factor (or a temporary access pass) before add/remove, and the user is notified.

13. https://learn.microsoft.com/en-us/entra/identity/authentication/howto-registration-mfa-sspr-combined (org: Microsoft). New for this clause (Microsoft was used in G4 and H3 for step-up on protected actions, not for factor change). A Conditional Access policy on the "Register security information" user action: "Users connected on a nontrusted network must either perform MFA or sign in by using a temporary access pass to register for MFA or reset their password by using SSPR." The policy is scoped to "Under **Cloud apps or actions**, select **User actions**. Select the **Register security information** checkbox". Backs H3's factor-change re-authentication, with the caveat that it is an IdP policy, not app code.

**Count for O6.** "Re-authenticate with an existing factor before a factor change" now has 3 (OWASP, NIST, Microsoft). Microsoft's control is at the IdP and uses MFA or a temporary access pass, so the Rule should say "an existing factor or a documented recovery path", not "MFA only". GitHub's 2FA-change page was read and does not back this clause (it requires a code from the **new** method, not an existing factor). Confidence medium-high.

---

## O7 — H5 password reset: store the token only as a hash

**Candidate Rule.** Generate the reset token from a CSPRNG, store only a hash of it, and never keep the raw value after the mail is sent.

**Level.** service. **Tool gate.** none found; a test that reads the reset table and asserts it does not contain the mailed token is the gate.

**Existing card.** `svc-auth-throttle-generic-errors` (stable) covers identical replies and rate limiting on the request endpoint. `svc-session-lifecycle` covers sessions but not revocation on reset. `fn-password-slow-hash` covers the new password's storage. Missing: token lifecycle (single-use, TTL, hashing) and revocation of other tokens.

**FAIL/PASS.** FAIL: `user.reset_token = raw` (or a predictable `f"{user.id}-{int(time())}"`). PASS: `db.store(sha256(raw), expires=now+15m)` and the raw value exists only in the mail.

14. https://symfony.com/doc/current/security/reset_password.html (org: Symfony). New for this clause. A documented use of the password hasher for recovery secrets: "In some cases, you may define a password hasher in your configuration that is not tied to a user class. For example, you might use a separate hasher for password recovery codes or API tokens." The example hashes the raw value before storing: "Note: use `hash()`, not `hashPassword()`, as we are not using a `UserInterface` object" then `$hashedToken = $this->passwordHasher->hash($plaintextToken);`. Backs H5's hashed-storage clause, but only for "recovery codes or API tokens", not the emailed reset link by name.

**Count for O7.** "Store only a hash of the reset token" now has 3 (OWASP, NIST, Symfony). OWASP says "Stored securely" and points at its Password Storage Cheat Sheet; NIST's exact wording is about recovery codes ("hashed form using an approved one-way function"); Symfony's is recovery codes/API tokens. No source in this pass says "the emailed reset link token, stored as SHA-256" verbatim, so the clause is at 3 but medium confidence. Laravel's implementation hashes the token, but its documentation says only that tokens are stored in a table and does not say hashed; not counted.

---

## O8 — H2 SAML: reject a reused assertion ID and check `Destination`

**Candidate Rule.** Run the SP in strict mode, reject an assertion or response ID already seen until its `NotOnOrAfter`, and require `Destination` (and `Recipient`, `Audience`, `InResponseTo`) to match this SP.

**Level.** service (the SP's ACS handler). **Tool gate.** none found; crafted replay and cross-SP responses in the security tests are the gate.

**Existing card.** `fn-xml-no-external-entities` (stable) covers XXE only. Nothing covers SAML signature placement or assertion checks.

**FAIL/PASS.** FAIL: `if response.status == Success: login(find(".//NameID"))` with no signature binding, no ID cache and no `Destination` check. PASS: strict validation, signature over the assertion actually read, `Destination == ACS_URL`, and the assertion ID recorded until `NotOnOrAfter`.

15. https://github.com/SAML-Toolkits/python3-saml (org: python3-saml toolkit, SAML-Toolkits maintainers; formerly OneLogin). New for this clause. The replay cache is stated as the practice: "In order to avoid them, the SP can keep a list of SAML Messages or Assertion IDs already validated and processed." and "Checking that the ID of the current Message/Assertion does not exists in the list of the ones already processed will prevent replay attacks." The retention window is bounded: "Those values only need to be stored the amount of time of the SAML Message life time". `Destination` is covered by its strict-mode setting: "Also it will reject the messages if the SAML standard is not strictly followed. Destination, NameId, Conditions ... are validated too." and "In production, the `strict` parameter MUST be set as `"true"`." Backs H2's replay-cache clause and its `Destination` clause.

**Count for O8.** "Reject a reused assertion ID" now has 3 (OASIS, OWASP, python3-saml). "Check `Destination`" now has 3 (OWASP, Microsoft as a description of the field, python3-saml). NIST SP 800-63C was fetched and its only replay sentence is about audience restriction, not an ID cache: "All RPs SHALL check that the audience of an assertion contains an identifier for their RP to prevent the assertion injection and replay of an assertion generated for one RP at another RP." That is an `Audience` source, not a replay-cache source, so it is not counted for the replay clause. Confidence medium-high; the normative sources remain OASIS and OWASP, with python3-saml a project's own implementation guide.

---

## Counter-evidence and limits

- **G1 does not require rejection.** RFC 9112 says the CL+TE combination "ought to be handled as an error" and then lets an intermediary strip `Content-Length` and forward. Fastly says it "either rejects or normalizes"; Envoy rejects by default but can be configured to strip; Cloudflare returns 400. The Rule should say "normalise at the first hop, and reject or close at the next", not "reject everywhere".
- **G1 downgrade has two organisations, not three.** PortSwigger says "Use HTTP/2 end to end and disable HTTP downgrading if possible"; Fastly says "validate that rewritten requests are not malformed or ambiguous" and that HTTP/2 is protected "when downgrading is disabled". No third source was found. Keep the clause in `Why`, or narrow it to "validate on downgrade" (PortSwigger and Fastly).
- **G2 static-only is advice, not every vendor's default.** Fastly's cache-control page says "most content is cacheable by default" and treats `private` as "Don't store" while ignoring `no-store`. A card must not claim that every CDN caches static content only.
- **G3 override is a configuration duty, not a vendor guarantee.** CloudFront overrides `no-store`/`private` when the minimum TTL is above 0; Cloudflare's Cache Deception Armor docs say "A `Cache-Control` header from the origin, or an Edge Cache TTL Cache Rule may override the protection"; Google's `FORCE_CACHE_ALL` "overriding any cache directives set by the origin". The check is the specific policy value, not the vendor's reputation.
- **G3 extension behaviour differs by vendor.** Cloudflare says "Because the path ends in `.jpg`, Cloudflare caches the response by default"; Google says it "doesn't use file extensions in the URL path to determine whether a response is cacheable". A pass on one CDN is not a pass on another.
- **G4 duplicate `Host` has two organisations.** RFC 9112 requires a 400 for "more than one Host header field", and Fastly's host-header page says "Validate there is only one Host header." nginx's changelog has no duplicate-`Host` entry; Apache's `HttpProtocolOptions Strict` page, as fetched, does not mention it. Move the clause to `Why`.
- **G4 production defaults are open.** Rails: "In other environments `Rails.application.config.hosts` is empty and no Host header checks will be done." Laravel: "By default, Laravel will respond to all requests it receives regardless of the content of the HTTP request's `Host` header." The allowlist is opt-in in both.
- **G6 depends on a draft.** Mozilla and OWASP are stable; the IETF text is an active Internet-Draft. Two web.dev/Chrome URLs for cookie prefixes returned 404, so Google is not a source here. The Microsoft cookie-authentication page, the Django settings page and the Rails guides I opened do not state host-only scope.
- **H3's Microsoft source is a Conditional Access policy**, not application code. It is evidence that requiring MFA (or a temporary access pass) before security-info registration is accepted practice, not a claim that every app can use Conditional Access.
- **H5's hashing clause is adjacent, not exact.** NIST's wording is about recovery codes; Symfony's is about "password recovery codes or API tokens". OWASP says "Stored securely" and points at its Password Storage Cheat Sheet. No source says "the emailed reset link is stored as a SHA-256 hash" in those words.
- **H2 `Destination` is not the same field as `Recipient`.** OASIS's Web Browser SSO profile requires the `Recipient` attribute in `SubjectConfirmationData` to match the ACS URL; OWASP and python3-saml say `Destination` on the `<Response>`. A card should check both, and should not use the OASIS `Recipient` requirement as a `Destination` source.
- **H2 replay must key on the object actually accepted.** Recording the ID of a `<Response>` whose inner assertion is the one used does not stop a wrapped assertion with a different ID. The cache should hold the ID of the signed assertion (or response) that was validated, for its `NotOnOrAfter` window.

## Also read, no rule

- https://www.fastly.com/documentation/guides/full-site-delivery/caching/about-cache-control-headers/ (org: Fastly). Documents that Fastly honours `private` but "All other `Cache-Control` directives are ignored and will **not** influence Fastly's caching ... `Cache-Control: no-cache`, `Cache-Control: no-store`, and `Cache-Control: must-revalidate`." Counter-evidence for G3's "the CDN must not override the origin"; not counted for the clause.
- https://laravel.com/docs/12.x/urls (org: Laravel). "The generated URL will automatically use the scheme (HTTP or HTTPS) and host from the current request being handled by the application." This is the FAIL behaviour for G4, not a configuration practice; not counted.
- https://docs.github.com/en/authentication/securing-your-account-with-two-factor-authentication-2fa/changing-your-two-factor-authentication-method (org: GitHub). "Changes to an existing 2FA method will only take effect after you have provided a valid code from the new method and clicked **Save**", plus a CAPTCHA. It proves the new factor, not an existing one; not counted for H3.
- https://learn.microsoft.com/en-us/aspnet/core/security/authentication/accconfirm (org: Microsoft). Token lifespans ("The built-in Identity user tokens ... have a one day timeout") and Data Protection, but no statement that the reset token is stored hashed; not counted for H5.
- https://docs.djangoproject.com/en/5.2/topics/auth/default/ (org: Django). `PasswordResetView` "generating a one-time use link" and `default_token_generator`, but no storage or hashing statement; not counted for H5.
- https://docs.djangoproject.com/en/5.2/ref/settings/ (org: Django). `SESSION_COOKIE_DOMAIN`: "Set this to a string such as `"example.com"` for cross-domain cookies, or use `None` for a standard domain cookie." Too vague to back "omit `Domain`"; not counted for G6.
- https://learn.microsoft.com/en-us/aspnet/core/security/authentication/cookie (org: Microsoft). Cookie authentication options, but nothing on `Domain` or `__Host-`; not counted for G6.
- https://httpd.apache.org/docs/2.4/mod/core.html (org: Apache Software Foundation). `StrictHostCheck`: "By setting `StrictHostCheck` to `ON`, the server will return an HTTP 400 error if the requested hostname hasn't been explicitly listed by either `ServerName` or `ServerAlias`". Backs G4's allowlist clause, which already has four organisations; not a missing-clause source. `httpd.apache.org` needs a `tools/orgs.py` prefix if a card cites it.
- https://nginx.org/en/CHANGES (org: nginx). 1.21.1: "now nginx always returns an error if both `Content-Length` and `Transfer-Encoding` header lines are present in the request"; 1.21.2: "now nginx rejects HTTP/1.0 requests with the `Transfer-Encoding` header line". A changelog entry with no rationale, not a practice page; not counted for G1.
- https://www.fastly.com/learning/security/what-is-web-cache-deception (404, UNFETCHED). No Fastly cache-deception page found.
- https://techdocs.akamai.com/property-mgr/docs/origin-cache-control (404), https://techdocs.akamai.com/property-mgr/docs/honor-origin-cache-control (404), https://techdocs.akamai.com/property-mgr/docs/cache-control-header (404). No Akamai page was located; Akamai is not a source in this pass.
- https://varnish-cache.org/docs/trunk/users-guide/vcl-built-in-subs.html (404, UNFETCHED). No Varnish source.
- https://web.dev/articles/cookie-prefixes (404) and https://developer.chrome.com/docs/privacy-security/cookie-prefixes (404). No Google cookie-prefix page located; Google is not a source for G6.
- https://owasp.org/www-project-web-security-testing-guide/latest/4-Web_Application_Security_Testing/07-Input_Validation_Testing/16-Testing_for_HTTP_Request_Smuggling (redirected to the WSTG home page at fetch time; UNFETCHED). No smuggling remediation text was available from that URL.
- https://pages.nist.gov/800-63-4/sp800-63c/Federation/ (org: NIST). Fetched for the replay check; its replay sentence is audience-based, not an assertion-ID cache, so it does not back O8's replay clause.

## Per-claim organisation count

| Clause | Orgs behind it now | New in this pass | Status |
|---|---|---|---|
| G1 normalise + reject | 5 (PortSwigger, IETF, Fastly, Envoy, Cloudflare) | Fastly, Envoy, Cloudflare | done |
| G1 no HTTP/1 downgrade | 2 (PortSwigger, Fastly) | Fastly | short; move to Why |
| G2 no unkeyed reflection | 3 (Cloudflare, PortSwigger, Fastly) | Fastly | done |
| G2 static-only default | 3 (Cloudflare, PortSwigger, Google) | Google | done, but vendor-dependent |
| G3 CDN must not override origin | 3 (PortSwigger, Microsoft, AWS) | AWS | done, configuration duty |
| G3 no extension-only caching | 3 (Cloudflare, PortSwigger, Google) | Google | done, vendor-dependent |
| G3 path interpretation agrees | 1 (PortSwigger) | none | short; Why only |
| G4 base URL from config | 3 (PortSwigger, Fastly, Rails) | Rails | done |
| G4 Host allowlist | 6 (PortSwigger, Fastly, Django, Microsoft, Rails, Laravel) | Rails, Laravel | already done |
| G4 duplicate Host rejected | 2 (IETF, Fastly) | none | short; move to Why |
| G4 forwarded only from trusted proxy | 4 (Django, Microsoft, PortSwigger, Fastly) | none | already done |
| G6 omit Domain / `__Host-` | 3 with a draft (Mozilla, OWASP, IETF draft); 2 stable | IETF draft | not yet stable; hold |
| H3 reauth existing factor before factor change | 3 (OWASP, NIST, Microsoft) | Microsoft | done |
| H5 reset token stored as hash | 3 (OWASP, NIST, Symfony) | Symfony | done, medium |
| H2 replay cache | 3 (OASIS, OWASP, python3-saml) | python3-saml | done |
| H2 `Destination` check | 3 (OWASP, Microsoft, python3-saml) | python3-saml | done |

## Answer to "what is missing" per class, after this pass

- **G1:** a new `svc-request-framing` is supported by 5 organisations for normalise+reject. Drop "no HTTP/1 downgrade" from the Rule (2 orgs) or rephrase it as "validate the rewritten HTTP/1.1 request on downgrade", which PortSwigger and Fastly both state.
- **G2:** a new `svc-cache-key-completeness` is supported by 3 organisations for the unkeyed-input clause and 3 for the static-only default. Keep "cache only static assets" as a default, not an absolute.
- **G3:** `svc-api-cache-control` already owns `private`/`no-store`. Add the deception clause (extension vs `Content-Type`, cache rule vs origin) to that card; both clauses now have 3. Leave path interpretation in `Why` (1).
- **G4:** a new `svc-host-header-trust` clears the bar for allowlist (6), configured base URL (3) and trusted proxy (4). Move "reject duplicate Host" to `Why` (2).
- **G6:** `svc-session-lifecycle` still carries the attribute clause. Hold "omit `Domain`; use `__Host-`" until a third stable organisation appears; the IETF draft is the third only if a draft is accepted, and the document itself says not to cite it as anything but work in progress.
- **H3:** the factor-change re-authentication clause now has 3 and can move back into the Rule; keep the NIST recovery-path caveat.
- **H5:** the hashed-storage clause now has 3, but one of them (Symfony) is about recovery codes/API tokens, so keep "as you would a password" in the note and do not overstate the exact hash.
- **H2:** replay cache and `Destination` each have 3 now. State that the cache is keyed on the assertion/response ID that was actually validated and kept until `NotOnOrAfter`; do not present OASIS's `Recipient` rule as a `Destination` source.

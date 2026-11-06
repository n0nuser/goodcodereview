# Security class research H: identity and authentication

Goal: independent ORGANISATION sources behind six draft cards for Cloudflare's identity and authentication attack classes (H1-H6). Each claim is a candidate Rule line. A source counts only when it states a practice; people are listed apart and never count.

Org convention (from `docs/PROMOTION.md` and `tools/orgs.py`): OWASP is one org (Cheat Sheets, ASVS, Top 10). Google counts `cloud.google.com`, `developers.google.com` and the Google Security Blog as one. Microsoft counts `learn.microsoft.com`, MSRC and Microsoft Research as one. Okta and Auth0 are mapped separately (`auth0.com` → `auth0`); where a page is Auth0's, it is counted as Auth0, not Okta. OASIS, IETF, NIST, OpenID Foundation, GitHub, GitLab, Stripe and AWS are each one.

Order: H1 OAuth/OIDC binding, H2 SAML, H3 MFA/step-up, H4 account linking, H5 password reset, H6 API keys.

---

## H1 — OAuth 2.0 / OIDC authorization-code flow binding

**Candidate Rule.** "Complete the authorization-code flow with PKCE (`S256`), compare `redirect_uri` exactly against a registered value, and reject the response unless `state` (or the OIDC `nonce`) matches the transaction and the ID token's signature, `iss`, `aud` and `exp` check out."

**Level.** service (the server-side OAuth client; the authorization-server side is a different card).

**Tool gate.** none. No linter or SAST rule for this; the nearest aid is a maintained OAuth/OIDC SDK, which is not a named rule. Say `tool_gate: none`.

**Existing cards.** `svc-authn-by-default` only decides whether a route needs a session. `fn-redirect-target-allowlist` covers generic `?next=` redirects, not the client's registered `redirect_uri`. `svc-session-lifecycle` covers the session issued after login. None covers the flow binding. **Missing:** PKCE, exact redirect matching, state/nonce binding, ID-token claim checks.

**FAIL / PASS ideas.**
FAIL: `token = exchange(code); login(token.sub)` — `redirect_uri` echoed from the request, no `state`, no `code_verifier`, ID token decoded without signature/`aud` check.
PASS: `assert state == session.pop("oauth_state"); assert redirect_uri in REGISTERED; exchange(code, code_verifier=verifier); claims = verify_jwt(id_token, jwks, iss=ISSUER, aud=CLIENT_ID, nonce=session.pop("nonce"))`.

1. `https://www.rfc-editor.org/rfc/rfc9700.html` (org: IETF). Best Current Practice, January 2025. Exact matching: "When comparing client redirection URIs against pre-registered URIs, authorization servers MUST utilize exact string matching except for port numbers in `localhost` redirection URIs of native apps". PKCE: "Public clients MUST use PKCE [RFC7636] to this end", and "the PKCE challenge or OpenID Connect `nonce` MUST be transaction-specific and securely bound to the client and the user agent in which the transaction was started." Method: "Currently, `S256` is the only such method." CSRF: clients without PKCE/nonce "one-time use CSRF tokens carried in the `state` parameter that are securely bound to the user agent MUST be used for CSRF protection". Backs **H1**.

2. `https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html` (org: OWASP). "Clients **must** use the Authorization Code Grant with PKCE (`response_type=code`) for all client types, including SPAs and native applications." "Clients are preventing injection (replay) of authorization codes into the authorization response by using PKCE flow." It repeats the state rule: "one-time user CSRF tokens carried in the 'state' parameter that are securely bound to the user agent must be used for CSRF protection", and adds that "In OpenID Connect flows, the 'nonce' parameter provides CSRF protection." Backs **H1**. Tool-gate note: the cheat sheet names no linter.

3. `https://openid.net/specs/openid-connect-core-1_0.html` (org: OpenID Foundation). `redirect_uri`: "This URI MUST exactly match one of the Redirection URI values for the Client pre-registered at the OpenID Provider, with the matching performed as described in Section 6.2.1 of [RFC3986] (Simple String Comparison)." `nonce`: "If present in the ID Token, Clients MUST verify that the nonce Claim Value is equal to the value of the nonce parameter sent in the Authentication Request." `aud`: "It MUST contain the OAuth 2.0 client_id of the Relying Party as an audience value." `exp`: "Expiration time on or after which the ID Token MUST NOT be accepted by the RP when performing authentication with the OP." Backs **H1** and is the primary source for the ID-token clause.

4. `https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow` (org: Microsoft). `redirect_uri`: "It must exactly match one of the redirect URIs you registered in the Microsoft Entra admin center". `state`: "The app should verify that the state values in the request and response are identical." `nonce`: "The app can then verify this value to mitigate token replay attacks." PKCE: "This parameter is now recommended for all application types, both public and confidential clients". Backs **H1**.

5. `https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce` (org: Auth0). "a malicious attacker can only intercept the Authorization Code, and they cannot exchange it for a token without the Code Verifier." The code returned is "good for one use". Backs **H1** for the PKCE/code-interception clause.

6. `https://auth0.com/docs/secure/tokens/id-tokens/validate-id-tokens` (org: Auth0). Validation order: "1. Validate the JWT." Then `aud`: "The audience value for the token must match the client ID of the application"; `nonce`: "The nonce value in the token must exactly match the original nonce sent in the request." "If any of these checks fail, the token is considered invalid, and the request must be rejected." Backs **H1** for the claim checks.

7. `https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html` (org: OWASP, same org as #2). "Validate ID Tokens on the relying party: issuer (`iss`), audience (`aud`), signature (per provider JWKs), expiration (`exp`)." Backs **H1** for the ID-token clause. This page is also the H4 source; it adds no second OWASP organisation.

8. `https://developers.google.com/identity/gsi/web/guides/verify-google-id-token` (org: Google). "To verify that the token is valid, ensure that the following criteria are satisfied: The ID token is properly signed by Google. Use Google's public keys ... to verify the token's signature"; "The value of `aud` in the ID token is equal to one of your app's client IDs"; "The value of `iss` in the ID token is equal to `accounts.google.com` or `https://accounts.google.com`"; "The expiry time (`exp`) of the ID token has not passed." It also names the CSRF check for the POST flow (compare the `g_csrf_token` cookie and body value). Backs **H1**.

**Clause counts (H1).** exact `redirect_uri`: IETF, OpenID Foundation, Microsoft = 3. PKCE + `S256`: IETF, OWASP, Microsoft, Auth0 = 4. `state`/`nonce` binding: IETF, OWASP, OpenID Foundation, Microsoft, Auth0 = 5. ID-token signature/`iss`/`aud`/`exp`: OpenID Foundation, OWASP, Google = 3 explicit; Auth0 adds aud + nonce and says "Validate the JWT", Microsoft backs the `nonce` part. **6 distinct organisations, high confidence.**

**Counter-evidence (H1).**
- RFC 9700 keeps a localhost port exception for native apps, so "exact match" is not byte-for-byte for `http://localhost` redirect URIs. A card must state the exception.
- RFC 9700 is a BCP, not a protocol update; OAuth 2.1 (`draft-ietf-oauth-v2-1`) is still a draft and is not counted here. OWASP's cheat sheet calls it an "active IETF Working Group draft".
- Microsoft still documents the hybrid/implicit response for ID tokens in the same page, while recommending code + PKCE for SPAs. So the practice is "code + PKCE", not "no other response type exists".

## H2 — SAML signature and assertion binding

**Candidate Rule.** "Verify the XML signature over the signed content that contains the assertion you actually read, using a key from configured IdP metadata rather than the document's `KeyInfo`, then require `Audience` and `Recipient`/`Destination` to match this SP, `InResponseTo` to match the request, `NotOnOrAfter` to be current, and the assertion ID to be unseen."

**Level.** service (the SP's ACS handler).

**Tool gate.** none. No linter rule. The nearest gate is crafted signature-wrapping responses in the security tests, not a named static rule.

**Existing cards.** `fn-xml-no-external-entities` covers XXE only. Nothing covers SAML signature placement or assertion checks. **Missing:** all of it.

**FAIL / PASS ideas.**
FAIL: `doc = etree.fromstring(b64decode(response)); user = doc.find(".//NameID").text; login(user)` — no signature verification, first matching element trusted.
PASS: `signed = verify_xmlsig(response, idp_metadata_key); assert signed.covers(assertion); assert assertion.audience == SP_ENTITY; assert assertion.recipient == ACS_URL; assert assertion.in_response_to == request_id; assert not used(assertion.id)`.

1. `https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf` (org: OASIS). The Web Browser SSO profile's `<Response>` processing rules ("Regardless of the SAML binding used, the service provider MUST do the following:") list: "Verify any signatures present on the assertion(s) or the response"; "Verify that the Recipient attribute in any bearer <SubjectConfirmationData> matches the assertion consumer service URL to which the <Response> or artifact was delivered"; "Verify that the NotOnOrAfter attribute in any bearer <SubjectConfirmationData> has not passed"; and "Verify that the InResponseTo attribute in the bearer <SubjectConfirmationData> equals the ID of its original <AuthnRequest> message, unless the response is unsolicited ... in which case the attribute MUST NOT be present". The assertion must carry an "`<AudienceRestriction>` including the service provider's unique identifier as an `<Audience>`". POST binding: "If the HTTP POST binding is used to deliver the <Response>, the enclosed assertion(s) MUST be signed." Replay: "The service provider MUST ensure that bearer assertions are not replayed, by maintaining the set of used ID values for the length of time for which the assertion would be considered valid based on the NotOnOrAfter attribute in the <SubjectConfirmationData>." Backs **H2**.

2. `https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html` (org: OWASP). Signature wrapping: "Never use `getElementsByTagName` to select security related elements in an XML document without prior validation." "Always use absolute XPath expressions to select elements, unless a hardened schema is used for validation." Key source: "If you expect only one signing key, use `StaticKeySelector`. Obtain the key directly from the identity provider, store it in a local file and ignore any `KeyInfo` elements in the document." Binding checks: "Validate the `Destination` attribute on `<samlp:Response>` exactly matches the SP's expected Assertion Consumer Service (ACS) URL ... Reject responses that are missing `Destination` or where it does not match — this prevents cross-SP assertion replay." "Validate `<saml:Audience>` matches the SP's EntityID". "Verify that the XML signature's `<ds:Reference URI>` resolves to the signed Assertion or Response, and that the exact assertion used for authentication is protected by that validated signature." Signing: "Sign each individual Assertion or the entire Response element". Also: "Unsolicited Response is inherently less secure by design due to the lack of login CSRF protection". Backs **H2**.

3. `https://pages.nist.gov/800-63-4/sp800-63c/Federation/` (org: NIST). "Assertions **SHALL** be cryptographically signed by the issuer (IdP). The RP **SHALL** validate the digital signature or MAC of each such assertion based on the issuer's verification key. This signature **SHALL** cover the entire assertion, including its identifier, issuer, audience, subject, and time validity window." Backs **H2** for "the signature must cover the assertion you use".

4. `https://learn.microsoft.com/en-us/entra/identity-platform/single-sign-on-saml-protocol` (org: Microsoft). Describes the response it sends and what each field means: "Microsoft Entra ID signs the assertion in response to a successful sign-on. The `Signature` element contains a digital signature that the cloud service can use to authenticate the source to verify the integrity of the assertion." It sets "`Destination`: When sign-on completes successfully, this is set to the `RedirectUri` of the service provider (cloud service)"; "`InResponseTo`: This is set to the `ID` attribute of the `AuthnRequest` element that initiated the response"; and "Like the `Issuer` value, the `Audience` value must exactly match one of the service principal names that represents the cloud service in Microsoft Entra ID." Backs **H2**, descriptive rather than a "must verify" command, so it is supporting evidence only.

5. `https://developer.okta.com/docs/concepts/saml/` (org: Okta). "After receiving the SAML assertion, the SP must validate that the assertion comes from a valid IdP." "The SP needs to obtain the public certificate from the IdP to validate the signature." Backs **H2** thinly (it states the practice, not the full check list).

**Clause counts (H2).** Verify signature before trusting: OASIS, OWASP, NIST = 3. Signature covers the assertion used / no wrapping: OASIS ("Verify any signatures present"), OWASP (Reference URI + XPath), NIST ("cover the entire assertion") = 3. Audience/Recipient/Destination: OASIS, OWASP, Microsoft (descriptive) = 3. `InResponseTo`: OASIS, OWASP, Microsoft = 3. Replay cache: OASIS, OWASP = 2 (OWASP's replay detection is for unsolicited responses; OASIS is general). **5 distinct organisations, medium-high confidence** (Microsoft and Okta are descriptive; the three normative ones are OASIS, OWASP, NIST).

**Counter-evidence (H2).**
- A Response signature is allowed in the browser SSO profile (OASIS errata), so "the assertion itself must be signed" is too strong. OWASP's wording is the safe one: "each Assertion or the entire Response element is signed", and the assertion you read must be inside the signed content. OASIS's POST rule says assertions MUST be signed when the message is unsigned.
- IdP-initiated SSO has no `InResponseTo` by design ("An unsolicited <Response> MUST NOT contain an InResponseTo attribute"), so that clause cannot apply there. OWASP calls unsolicited responses "inherently less secure by design" and tells you to implement replay detection if you keep them.
- A signed response is not enough if the reader picks a different element (`NameID`) than the one covered; that is the wrapping attack. The rule must bind the element read to the verified signature, not just "a signature is present".

## H3 — MFA enrollment, step-up and downgrade

**Candidate Rule.** "Require a fresh authentication with an already-bound factor before sensitive actions and before adding, replacing or removing an MFA factor; never let an existing session alone enroll or change a factor."

**Level.** service.

**Tool gate.** none. Write an integration test: a session that passed password-only login gets 403/step-up on factor-change and other sensitive routes; and a session that just enrolled a factor must not silently replace it on the next request.

**Existing cards.** `svc-session-lifecycle` covers login fixation and timeouts. `svc-auth-throttle-generic-errors` covers failed attempts and generic errors. Neither covers MFA enrollment or step-up. **Missing:** all of it.

**FAIL / PASS ideas.**
FAIL: `@login_required def add_phone(): user.phone = request.form["phone"]` — an old password-only session can replace the second factor.
PASS: `@login_required @recent_auth(max_age=300, factor="existing") def add_phone(): ...; notify(user)`.

1. `https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html` (org: OWASP). "The most important place to require MFA on an application is when the user logs in. However ... it may also be appropriate to require MFA for performing sensitive actions, such as: Changing passwords or security questions. Changing the email address associated with the account. Disabling MFA. Elevating a user session to an administrative session." Factor changes: "Require reauthentication with an existing enrolled factor before allowing changes." "Do not rely solely on the active session, as it may be hijacked." "Notify the user through out-of-band channels ... whenever an MFA factor is changed." Downgrade: "Disable legacy authentication protocols and endpoints that cannot enforce MFA consistently." "Prevent fallback from phishing-resistant authenticators to lower-assurance authentication methods unless required by a documented security policy." Passkeys: "require user verification and validate the returned user-verification flag on the server; a touch confirming user presence alone is not a second factor." Backs **H3**.

2. `https://pages.nist.gov/800-63-4/sp800-63b/events/` (org: NIST). Binding a new authenticator: "When any new authenticator is bound to a subscriber account, the CSP **SHALL** ensure that the process requires authentication at either the maximum AAL currently available in the subscriber account or the maximum AAL at which the new authenticator will be used, whichever is lower." It also requires an out-of-band notification: "the CSP **SHALL** notify the subscriber via a mechanism independent of the transaction binding the new authenticator". Recovery at AAL2 requires two independent methods: "Two recovery codes obtained using different methods from the set (i.e., saved, issued, and recovery contacts)" or one code plus a single-factor authenticator. Backs **H3** for "enrollment needs an authenticated, fresh, strong ceremony", and supplies the numeric recovery rule.

3. `https://pages.nist.gov/800-63-4/sp800-63b/session/` (org: NIST, same org). "The periodic reauthentication of sessions **SHALL** be performed to confirm the subscriber's continued presence at an authenticated session." Sessions inherit the AAL of the authentication event and "**SHALL NOT** be considered at a higher AAL than the authentication event." Backs **H3** for "a session is not a fresh factor"; adds no new org.

4. `https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/protected-actions-overview` (org: Microsoft). "When a user attempts to perform a protected action, they must first satisfy the Conditional Access policies assigned to the required permissions." The example is exactly step-up: "to allow administrators to update Conditional Access policies, you can require that they first satisfy the Phishing-resistant MFA policy." "Because the policy enforcement occurs at the time the user attempts to perform the protected action and not during user sign-in or rule activation, users are prompted only when needed." Backs **H3** for step-up at the action, not at login.

5. `https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication` (org: Auth0). "applications that allow access to different types of resources can require users to authenticate with a stronger authentication mechanism to access sensitive resources." For a web app: "If the claims show that the user already has authenticated with MFA then display the sensitive information. Otherwise, trigger authentication again and, using an Action, prompt the user to authenticate with MFA." Backs **H3** for the step-up mechanism.

**Clause counts (H3).** Require fresh auth before sensitive actions: OWASP, Microsoft, Auth0, NIST (reauthentication) = 4. Reauth with an existing factor before factor changes: OWASP, NIST (binding at max AAL) = 2 strong; Auth0's step-up can be configured for it but the page does not say "factor change". Never rely on the session alone: OWASP, NIST = 2. Refuse downgrade to legacy/weaker factors: OWASP only for the explicit "downgrade" wording; NIST covers restricted authenticators and AAL floors. **4 distinct organisations, medium confidence**: one clause (factor-change reauth) is at two orgs and needs a third, or should move to the Why.

**Counter-evidence (H3).**
- NIST classifies SMS/PSTN as a *restricted* authenticator (OWASP repeats this), so "MFA" in a card must not be satisfied by SMS for high-value accounts. That is a real constraint on the Rule, not a refutation.
- Requiring a fresh factor on every sensitive action is a usability cost; OWASP itself offers risk-based authentication to reduce prompt frequency. The Rule should say "sensitive" and name the actions, as OWASP does.
- Factor-change step-up can lock out a user who lost the only factor. The recovery path has to exist (OWASP: single-use recovery codes, multiple factors); otherwise the control becomes a denial-of-service.

## H4 — Account linking and identity collision

**Candidate Rule.** "Link a federated identity to an existing account only after proving control of both: require an authenticated session for the existing account and key the new identity on `iss` + `sub`, never on an unverified email; if email is the lookup hint, still require proof of control of the existing account."

**Level.** service.

**Tool gate.** none. Integration test: create a local account with an unverified email, then sign in through an IdP asserting that email; the accounts must stay separate (or require the local password), not merge.

**Existing cards.** None. `svc-auth-throttle-generic-errors` mentions registration replies but not linking. **Missing:** all of it.

**FAIL / PASS ideas.**
FAIL: `if user.email == claims.email: link(user, claims.sub)` — merges on an unverified claim.
PASS: `assert session.user; assert claims.email_verified; assert claims.iss and claims.sub; link(session.user, (claims.iss, claims.sub)); notify(session.user)`.

1. `https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks` (org: Microsoft). "Fundamentally, the root cause of account pre-hijacking vulnerabilities is that the service fails to verify that the user actually owns the supplied identifier (e.g. email address or phone number) before allowing use of the account." "All the attacks described above could be mitigated if the service sent a verification email to the user-provided email address and required the verification to be completed before allowing any further actions on the account." "If the service uses an IdP, it should check whether the IdP performs this verification or perform its own additional verification." Merging: "When a service merges an account created via the classic route with one created via the federated route (or vice-versa), the service must ensure that the user currently controls both accounts." Password reset defence: "Sign out all other sessions and invalidate all other authentication tokens for that account", "Cancel all pending email change actions", and notify the user which identities are linked. Backs **H4**.

2. `https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html` (org: OWASP). "Identify the federated identity using the combination of `iss` (issuer) and `sub` (subject), not `sub` alone." "Do not automatically link accounts solely because their `email`, `preferred_username`, or other profile attributes match." "Require an authenticated session with the existing application account before adding or removing linked identities". "Authenticate the identity being added and validate the resulting ID Token before saving the link." "After unlinking, disallow access to the application account through the removed identity." Backs **H4**.

3. `https://pages.nist.gov/800-63-4/sp800-63c/Federation/` (org: NIST). "the RP **SHALL** require an authenticated session with the subscriber account for all linking functions. This authenticated session **SHOULD** require authentication using one existing federated identifier before linking the new federated identifier to the RP subscriber account." Account resolution: "An RP that performs account resolution **SHALL** design the process such that it does not associate an RP subscriber account's information with a federated identifier that does not belong to the subscriber." And: "it is imperative that an RP never process the subject identifier without accounting for the IdP that issued the subject identifier." Backs **H4**.

4. `https://auth0.com/docs/manage-users/user-accounts/user-account-linking` (org: Auth0). "Insecurely linking accounts can allow malicious actors to access legitimate user accounts." "For both manual and automatic account links, your tenant should request authentication for **both** accounts before linking occurs." "In addition, **every** manual account link should prompt the user to enter credentials." Backs **H4**.

5. `https://developers.google.com/identity/gsi/web/guides/verify-google-id-token` (org: Google). For "An existing account that already exists in your site": "You can show a web page that allows the end user to input their password and link the legacy account with their Google credentials. This confirms that the user has access to the existing account." On the identifier: "Only use Google ID token **`sub`** field as identifier for the user as it is unique among all Google Accounts and never reused"; "don't use email address as an identifier because a Google Account can have multiple email addresses at different points in time." Backs **H4**.

6. `https://openid.net/specs/openid-connect-core-1_0.html#ClaimStability` (org: OpenID Foundation, same page as H1 #3). "The `sub` (subject) and `iss` (issuer) Claims from the ID Token, used together, are the only Claims that an RP can rely upon as a stable identifier for the End-User"; "the only guaranteed unique identifier for a given End-User is the combination of the `iss` Claim and the `sub` Claim." And: "other Claims such as `email`, `phone_number`, `preferred_username`, and `name` MUST NOT be used as unique identifiers for the End-User". Backs **H4**.

**Clause counts (H4).** Verify the identifier before use/merge: Microsoft, OWASP, NIST, Google = 4. Do not link on an unverified email/profile match: Microsoft, OWASP, NIST, OpenID Foundation, Google = 5. Authenticate both sides: OWASP, NIST, Auth0, Microsoft, Google = 5. Key on `iss` + `sub`, not `sub` alone: OWASP, NIST, OpenID Foundation, Google = 4. **6 distinct organisations, high confidence.**

**Counter-evidence (H4).**
- Linking on a *verified* email is a normal product decision; the sources prohibit automatic linking on an *unverified* claim, not all email-based linking. State the distinction or the card over-reaches.
- Some IdPs do not assert a verified email at all. Microsoft's MSRC blog says to "check whether the IdP performs this verification or perform its own"; a card that assumes `email_verified` exists will fail on those providers.
- OIDC Core itself warns that `email` is not a stable or unique identifier and "MUST NOT be used as unique identifiers for the End-User". The durable key is `iss` + `sub`; email is only a lookup hint.
- Google's own page adds a second caveat about `email_verified`: it "can also be true as Google initially verified the user when the Google account was created, however ownership of the third party email account may have since changed." A verified-at-issue-time email is not proof of control now, which is why the existing-account password check matters.

## H5 — Password reset and account recovery

**Candidate Rule.** "Issue password-reset tokens that are random, single-use, short-lived and stored hashed; answer the request the same way whether or not the account exists; and on success revoke every session and every other outstanding reset or recovery token."

**Level.** service.

**Tool gate.** none. Integration tests: reuse a token (must fail), use an expired token (must fail), reset and then use an old session cookie (must fail), request for an unknown address (same status/body/timing).

**Existing cards.** `svc-auth-throttle-generic-errors` covers rate limiting and identical replies on reset endpoints (it cites OWASP, NIST, PortSwigger, Microsoft, Auth0, Google). `svc-session-lifecycle` covers sessions but not revocation on reset. `fn-password-slow-hash` covers the new password's storage. **Missing:** token lifecycle (single-use, TTL, hashing), and revocation of other tokens.

**FAIL / PASS ideas.**
FAIL: `token = f"{user.id}-{int(time())}"; user.reset_token = token; send(link(token))` — predictable, stored plaintext, reusable, old sessions survive.
PASS: `raw = secrets.token_urlsafe(32); db.store(sha256(raw), user, expires=now+15m); consume_once(raw); revoke_sessions(user); revoke_pending_resets(user)`.

1. `https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html` (org: OWASP). Request: "Return a consistent message for both existent and non-existent accounts." "Ensure that the time taken for the user response message is uniform." Tokens must be "Randomly generated using a cryptographically safe algorithm", "Sufficiently long to protect against brute-force attacks", "Stored securely", and "Single use and expire after an appropriate period"; "Invalidated after they have been used." Storage: "Stored in a secure manner, as discussed in the [Password Storage Cheat Sheet]." On success: "Ask the user if they want to invalidate all of their existing sessions, or invalidate the sessions automatically." Recovery after compromise: "After successful recovery, invalidate existing sessions and outstanding password reset and recovery links or codes so they cannot restore an attacker's access." Also "Don't rely on the Host header while creating the reset URLs" and "Do not make a change to the account until a valid token is presented". Backs **H5**.

2. `https://pages.nist.gov/800-63-4/sp800-63b/events/` (org: NIST). Issued recovery codes "**SHALL** be valid for at most: ... 10 minutes when sent via text message or voice; 24 hours when sent to an email address". "Following the use of a saved recovery code, the CSP **SHALL** invalidate that recovery code and **SHALL** issue a new saved recovery code to the subscriber." "Saved recovery codes **SHALL** be stored in the subscriber account in hashed form using an approved one-way function." Verification "**SHALL** be subject to the throttling requirements". "Account recovery **SHALL** cause a notification to be sent to the subscriber." Backs **H5** with concrete numbers.

3. `https://auth0.com/docs/authenticate/database-connections/password-change` (org: Auth0). "The reset password link in the email is valid for one use only." "If the user receives multiple password reset emails, only the password link in the most recent email is valid." "The **URL Lifetime** field determines how long the link is valid." "Resetting a user's password makes their session expire." Backs **H5** for single-use, newest-only, TTL and session invalidation.

4. `https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks` (org: Microsoft). "We highly recommend that you choose two or more authentication methods so that your users have more flexibility in case they're unable to access one method when they need it." "If this option is set to **Yes**, users resetting their password receive an email notifying them that their password has been changed." Backs **H5** for the notification and multiple-method clauses; it does not document token storage or single use.

5. `https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks` (org: Microsoft, same org). On a password reset the service must "Sign out all other sessions and invalidate all other authentication tokens for that account" and "Cancel all pending email change actions for that account". Backs **H5** for revocation (and is the same page as H4 #1).

**Clause counts (H5).** Single-use + short expiry: OWASP, NIST, Auth0 = 3. Hashed storage: OWASP ("Stored in a secure manner ... Password Storage"), NIST ("hashed form using an approved one-way function") = 2; Microsoft and Auth0 do not say it. Same reply / no enumeration: OWASP = 1 on this card; that clause already lives in `svc-auth-throttle-generic-errors` with Microsoft, Auth0, Google and PortSwigger, so keep it there and link it. Revoke sessions + other tokens on success: OWASP, Auth0, Microsoft = 3. **4 distinct organisations; medium-high confidence**, with the hashing clause short of three and the enumeration clause better handled by the existing card.

**Counter-evidence (H5).**
- "Short-lived" has no single number: NIST allows 24 hours for email recovery codes, which is long for a reset link. A card should require a stated number and a reason, rather than the word "short-lived".
- Microsoft's own SSPR portal tells a user who is not enabled for SSPR to "contact their administrator", which reveals that the account exists or is not enabled. That is a counter-example to a strict "no enumeration anywhere in the flow" rule, and a reason to scope the rule to the request endpoint.
- OWASP says not to lock the account in response to a forgotten-password request (denial of service); a rate limit, not a lockout, is the control.
- Recovery codes and reset tokens are different lifetimes; do not copy the 24-hour email recovery-code limit onto a reset link without deciding it is acceptable.

## H6 — API key scope and exposure

**Candidate Rule.** "Issue each API key with the narrowest scopes and an expiry, show the secret once and store only a hash, rotate or revoke it on a schedule and on exposure, and never embed a secret key in client-side code or a URL."

**Level.** service (the key issuer) with a codebase check for embedded keys.

**Tool gate.** none for scope or rotation. For exposure the existing `code-secret-scan` gate applies: GitHub secret scanning with push protection, or GitLab secret detection (name the scanner; no single rule id covers "a key with too much scope").

**Existing cards.** `svc-no-secrets-in-url` covers tokens in URLs (and its counterpoint already handles email links). `code-secret-scan` covers committed credentials. `fn-constant-time-secret-compare` covers verifying a presented key. `sys-secrets-and-errors` covers where secrets live at runtime. **Missing:** least-privilege scoping, hashed storage, expiry/rotation, and "never embed a secret key in a distributed app".

**FAIL / PASS ideas.**
FAIL: `const key = "sk_live_..."` in browser JS; one key with full account scope and no expiry, stored plaintext in the DB.
PASS: `issue(scope=["orders:read"], expires_in=90d); db.store(hmac_sha256(key, PEPPER)); return key once; rotate_on_schedule(); revoke_on_exposure()`.

1. `https://cloud.google.com/docs/authentication/api-keys` (org: Google). "Unrestricted API keys are insecure." "API restrictions: Limit an API key to only be used with a specific set of APIs." "Application restrictions: Limit an API key so it can only be used by specific websites, IP addresses, or applications." "We recommend setting both API restrictions and application restrictions." Rotation: "By periodically rotating your API keys, you can limit the impact of any compromised API keys." "When you rotate an API key, you create a new key with the same restrictions as the old key, and update your applications to use the new key. After all of your applications are updated, you delete the old key." Backs **H6**.

2. `https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure` (org: GitHub). "only select the minimum permissions or scopes needed, and set an expiration date for the minimum amount of time you'll need to use the token". "Never hardcode authentication credentials like tokens, keys, or app-related secrets into your code." "Treat authentication credentials the same way you would treat your passwords or other sensitive credentials." On a leak: "Generate a new credential. Replace the old credential with the new one everywhere that you are storing or accessing the credential. Delete the old compromised credential." Backs **H6**.

3. `https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens` (org: GitHub, same org). Fine-grained tokens: "Each token is granted specific, fine-grained permissions, which offer more control than the scopes granted to personal access tokens (classic)." "You should choose the minimal repository access that meets your needs." "You should choose the minimal permissions necessary for your needs." "we highly recommend adding an expiration to your personal access tokens." Backs **H6** for scope granularity and expiry.

4. `https://docs.stripe.com/keys-best-practices` (org: Stripe). "Never put secret API keys in source code". "Follow the principle of least privilege". "Use restricted API keys with limited permissions instead of unrestricted secret API keys." "Rotate secret API keys periodically". "When you create a secret API key in the Stripe Dashboard, you see it one time." "Never embed secret API keys in applications: Unauthorized parties can unpack applications to search for embedded keys. For client-side use cases such as client tools, SDKs, and mobile apps, embed publishable keys instead." Backs **H6** and is the strongest source for the client-side clause.

5. `https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html` (org: AWS). "As a best practice, use temporary security credentials (such as IAM roles) instead of creating long-term credentials like access keys." "The secret access key can be retrieved only at the time you create it. If you lose your secret access key, you must delete the access key and create a new one." "Do NOT put access keys or credential information in your application files." "Regularly review, update, and delete access keys as needed." "You can have a maximum of two access keys per user." Backs **H6** for show-once, rotation and the temporary-credential preference.

6. `https://docs.gitlab.com/security/tokens/` (org: GitLab). "When creating a scoped token, use the most limited scope possible to reduce the impact of an accidentally leaked token." "Consider setting a token that expires when your task is complete." "Pass tokens with headers instead of URLs". "Review all active access tokens of all types on a regular basis and revoke any you don't need." Do not "Store tokens in plaintext in your projects." Backs **H6**.

7. `https://pages.nist.gov/800-63-4/sp800-63b/authenticators/` (org: NIST). Look-up secrets (the model for a bearer key the server must verify): "Verifiers **SHALL** store look-up secrets in a form that is resistant to offline attacks. All look-up secrets **SHALL** be stored in a hashed form using an approved hashing function." "A secret from a look-up secret authenticator **SHALL** be used successfully only once." Backs **H6** for hashed storage and single-use where a key is one-time.

**Clause counts (H6).** Least-privilege scope: Google, GitHub, Stripe, GitLab = 4. Expiry/rotation: Google, GitHub, Stripe, AWS, GitLab = 5. Show once / store a hash, not the secret: NIST, AWS (retrieve only at creation), Stripe (see it one time) = 3. Never in source or client code: Stripe, GitHub, AWS = 3 (plus GitLab forbids plaintext storage). Never in a URL: GitLab, and the existing `svc-no-secrets-in-url` card (OWASP, IETF, MITRE, Mozilla). **6 distinct organisations, high confidence** for scope and rotation; hashed storage is at three but only NIST says "hashed" explicitly.

**Counter-evidence (H6).**
- A standard Google Cloud API key is not an authentication credential: it "doesn't identify a principal" and "can't use Identity and Access Management (IAM) to check whether the caller is authorized". Requiring least-privilege *scopes* on it makes sense as API restrictions, but not as an identity claim; do not mix standard API keys with authorization keys.
- Hashing a 128-bit random key with plain SHA-256 is fine against offline guessing; the NIST password-hashing cost factors are for low-entropy passwords. A card should say "a keyed hash or SHA-256 of a high-entropy key", not "Argon2id", or it will be wrong for this class.
- AWS's first recommendation is to avoid long-lived keys entirely (roles/temporary credentials). Rotation is the fallback for a key that must exist; the card should prefer short-lived credentials where the platform offers them.
- API-key restriction by referrer or IP is spoofable in some clients; Google itself notes that browser referrer policies can drop the path. Treat network/app restrictions as defence in depth, not authentication.

---

## Also read, no rule

- `https://auth0.com/docs/authenticate/protocols/saml` (org: Auth0). Describes SAML support and bindings; no validation practice. Not counted for H2.
- `https://auth0.com/docs/get-started/authentication-and-authorization-flow/authorization-code-flow-with-pkce` is counted for H1, but it is client-side SDK guidance; it does not cover the authorization server's exact-match duty.
- `draft-ietf-oauth-v2-1` (IETF). Deliberately not counted: a draft, and RFC 9700 already carries the practice. OWASP's cheat sheet calls OAuth 2.1 an "active IETF Working Group draft".
- RFC 6749 and RFC 7636. Not fetched separately; RFC 9700 and OIDC Core cite and extend them. Do not cite them without opening them.
- `https://www.ory.com/blog/secure-account-linking-iam-sso-oidc-saml` and `https://workos.com/blog/oauth-auto-link-email-account-takeover` (vendor blogs). Secondary summaries of the Microsoft/OIDC guidance; not counted under rule 3.
- `https://developers.google.com/identity/account-linking` (Google). The overview was not fetched; the Google ID-token verification page is the Google source counted for H1 and H4.
- OWASP Session Management Cheat Sheet and ASVS V6. Relevant, but already the backbone of `svc-session-lifecycle`; not re-read here.
- OASIS SAML Core (`saml-core-2.0-os.pdf`). The PDF does not fetch through the text tool; the Profiles PDF was converted with `pdftotext`. Core signature-inheritance sections (5.3/5.4) are referenced by OWASP but were not read directly, so they are not quoted.
- Microsoft Entra "protected actions" is an admin-plane feature; it is used here as evidence that step-up at the action is an accepted practice, not as a claim that every app must use Conditional Access.

## People cited (never count)

- Avinash Sudhodanan (independent researcher) and Andrew Paverd (MSRC) — authors of the pre-hijacking research on Microsoft's MSRC blog. The organisation counted is Microsoft, because the page is Microsoft's; the person does not add to the count.
- RFC 9700 authors (T. Lodderstedt, J. Bradley, A. Labunets, D. Fett) — the organisation is IETF.
- The OWASP cheat-sheet editors are not named on the pages; the organisation is OWASP.

## Per-claim confidence

- **H1:** 6 organisations (IETF, OWASP, OpenID Foundation, Microsoft, Auth0, Google). High. Every main clause has at least three; the ID-token `iss`/`aud`/`exp`/signature clause has OpenID Foundation, OWASP and Google = 3 explicit, with Auth0 and Microsoft on parts. The card should keep the localhost port exception and should not claim OAuth 2.1 is final.
- **H2:** 5 organisations (OASIS, OWASP, NIST, Microsoft, Okta). Medium-high. The normative three (OASIS, OWASP, NIST) cover signature verification and "signature covers the assertion"; Microsoft and Okta are descriptive. **Gap:** replay-cache has two strong orgs (OASIS, OWASP), and `Destination` has two (OWASP plus Microsoft's description); if a strict per-clause rule is enforced, fold replay into "reject a reused assertion ID" backed by OASIS+OWASP+NIST's time-window requirement, or leave replay in the Why.
- **H3:** 4 organisations (OWASP, NIST, Microsoft, Auth0). Medium. Step-up before sensitive actions has 4; "reauth with an existing factor before a factor change" has OWASP and NIST only (2). Either find a third (Okta/Auth0 factor-management docs were not fetched) or move that clause to the Why and keep the Rule on step-up for sensitive actions.
- **H4:** 6 organisations (Microsoft, OWASP, NIST, Auth0, Google, OpenID Foundation). High. Every clause has at least three, including `iss` + `sub` (OWASP, NIST, OpenID Foundation, Google).
- **H5:** 4 organisations (OWASP, NIST, Auth0, Microsoft). Medium-high. Single-use/expiry and revocation have three; hashed storage has two (NIST, OWASP) and should be softened to "store only a hash, as you would a password" with the two-org note, or a third source found (GitLab/GitHub do not document reset-token storage). No-enumeration belongs to `svc-auth-throttle-generic-errors`, which already has the organisations.
- **H6:** 6 organisations (Google, GitHub, Stripe, AWS, GitLab, NIST). High. Scope has 4, rotation 5, show-once/hash 3, client-side 3. The URL clause is already the separate stable card `svc-no-secrets-in-url`; do not restate it in the new card, link it.

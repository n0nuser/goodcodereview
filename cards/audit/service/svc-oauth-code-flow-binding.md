---
id: svc-oauth-code-flow-binding
level: service
tags: [security, authn, oauth]
severity: block
status: stable
lang: core
applies_when: The service acts as an OAuth 2.0 or OpenID Connect client and exchanges an authorization code for tokens.
context: [server]
tool_gate: none
note: RFC 9700 requires the authorization server to match redirect URIs exactly, which is why the client must send the registered value (RFC 6749 section 4.1.3); the loopback port exception is only for a native app's http://127.0.0.1 redirect; fn-redirect-target-allowlist covers ?next= redirects, not the registered redirect_uri, and svc-session-lifecycle covers the session issued after login
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9700.html
  - https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html
  - https://openid.net/specs/openid-connect-core-1_0.html
  - https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
---

**Rule.** Finish the authorization-code flow with PKCE and a challenge method that keeps the verifier out of the authorization request (`S256`), send the exact registered `redirect_uri` (a native app on the loopback interface may vary the port), and reject the response unless this transaction's `state` or OIDC `nonce` matches and the ID token's signature, `iss`, `aud` and `exp` check out.

**Why.** A code that is not bound to the browser in front of you can be injected into another session, and an ID token minted for a different client or issuer can be replayed at your login. PKCE makes an intercepted code useless without the verifier, and `S256` is the method that does not reveal the verifier in the request. An exact redirect URI stops the code reaching an attacker's host. `state` or `nonce` ties the response to the login the user started. The ID-token checks reject a token that another app, another issuer or an expired clock made.

**FAIL**

```text
code = request.args["code"]
token = exchange(code, redirect_uri=request.args["redirect_uri"])
session["user"] = jwt.decode(token["id_token"], options={"verify_signature": False})["sub"]
# no PKCE, no state check, no ID-token validation, and the redirect_uri is taken from the request
```

**PASS**

```python
# the authorization request carried code_challenge=...&code_challenge_method=S256
if not secrets.compare_digest(request.args["state"], session.pop("oauth_state")):
    raise PermissionDenied
token = exchange(request.args["code"], redirect_uri=REDIRECT_URI,   # constant from config
                 code_verifier=session.pop("code_verifier"))
claims = verify_jwt(token["id_token"], jwks, iss=ISSUER, aud=CLIENT_ID,
                    nonce=session.pop("oauth_nonce"))
```

**Counterpoint.** "The OAuth client library already handles this." It handles the protocol, not your configuration. Some libraries decode the ID token unless you pass the issuer, audience and nonce, and the state or nonce store belongs to your session code. Test with a token minted for another client and a response with no state. The loopback exception is narrow: the port may differ, the host and path may not. The card is stricter than RFC 9700, which recommends PKCE for confidential clients and lets a confidential OIDC client use `nonce` instead; a reviewer may accept that alternative when the authorization server is known to bind the code another way.

**See also.** [[fn-redirect-target-allowlist]] covers redirect targets taken from a request; [[svc-csrf-state-changing]] covers the CSRF check on your own forms.

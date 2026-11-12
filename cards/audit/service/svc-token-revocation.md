---
id: svc-token-revocation
level: service
tags: [security, authn, tokens]
severity: should-fix
status: stable
lang: core
applies_when: The service issues refresh tokens, or self-contained access tokens such as JWTs, that outlive one request.
context: [server]
tool_gate: none
note: refresh revoked at logout - Cognito, ASVS 7.4.1, Entra single sign-out (public clients only); at disable - Cognito, ASVS 7.4.2, Entra CAE; access-token window named or closed - Cognito, RFC 7009, ASVS 7.4.1, Entra CAE. Revoking on a credential change has one firm source (Entra; ASVS only offers it), so it is in Why and svc-password-reset owns the reset case. The practical gate is a test that logs out and disables an account, then replays the old refresh token and the old access token
borrowed_from:
  - https://docs.aws.amazon.com/cognito/latest/developerguide/token-revocation.html
  - https://auth0.com/docs/secure/tokens/refresh-tokens/revoke-refresh-tokens
  - https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens
  - https://developers.google.com/identity/protocols/oauth2/web-server
  - https://www.rfc-editor.org/rfc/rfc7009
  - https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation
  - https://auth0.com/docs/secure/tokens/access-tokens
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x16-V7-Session-Management.md
---

**Rule.** Revoke the user's refresh tokens on the server at logout and when the account is disabled, and make access tokens expire quickly or check them against a revocation record.

**Why.** A refresh token is a long-lived credential. If logout only deletes it from the browser, a stolen copy keeps minting access tokens, and a disabled account whose refresh token still works keeps its access. The same holds after a password change, which [[svc-password-reset]] covers for a reset. A self-contained access token is valid until its `exp` unless the resource server checks something else, so revoking the refresh token alone leaves a window as long as the access lifetime. Close it with a lifetime of minutes, or with a denylist by `jti`, a per-user "not before" cutoff, or a per-user signing key.

**FAIL**

```text
POST /logout        -> delete the cookie, 204
disable account     -> user.active = false; refresh tokens untouched
access token exp = 24h; resource server checks signature and exp only
```

**PASS**

```text
POST /logout        -> mark the refresh token (and its grant) revoked in the store
disable account     -> revoke every refresh token of the user; set user.tokens_valid_after = now
access token exp = 5-15 min; resource server rejects iat < user.tokens_valid_after
```

**Counterpoint.** "Stateless tokens exist to avoid a lookup." Refresh already hits the store, so revoking there is free; only the access-token window needs a decision. A short lifetime accepts that window; a per-user cutoff costs one cached read per request. Name which one you chose, and do not claim revocation is immediate if it is not.

**See also.** [[svc-session-lifecycle]] owns server-side logout for cookie sessions; [[svc-password-reset]] owns revocation on a reset; [[svc-api-key-scope]] owns revocation of API keys.

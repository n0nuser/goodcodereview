---
id: svc-token-revocation
level: service
tags: [security, authn, tokens]
severity: should-fix
status: draft
lacks: unreviewed, sources are listed but no stable pass has checked them against rules 1 to 10
lang: core
applies_when: The service issues refresh tokens, or self-contained access tokens such as JWTs, that outlive one request.
context: [server]
tool_gate: none
note: refresh revoked on logout, credential change or disable - Cognito, Entra, Auth0, Google, ASVS 7.4.2; a revoked grant also kills its access tokens or the expiry gap is named - Cognito, Auth0, RFC 7009, ASVS 7.4.1. The practical gate is a test that logs out, changes the password, and disables the account, then replays the old refresh token and the old access token
borrowed_from:
  - https://docs.aws.amazon.com/cognito/latest/developerguide/token-revocation.html
  - https://auth0.com/docs/secure/tokens/refresh-tokens/revoke-refresh-tokens
  - https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens
  - https://developers.google.com/identity/protocols/oauth2/web-server
  - https://www.rfc-editor.org/rfc/rfc7009
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x16-V7-Session-Management.md
---

**Rule.** Revoke the user's refresh tokens on the server at logout, credential change and account disable, and give access tokens a short lifetime or a revocation check.

**Why.** A refresh token is a long-lived credential. If logout only deletes it from the browser, a stolen copy keeps minting access tokens, and a password change that leaves it alive does not evict the intruder. A self-contained access token is valid until its `exp` unless the resource server checks something else, so revoking the refresh token alone leaves a window as long as the access lifetime. Close it with a lifetime of minutes, or with a denylist by `jti`, a per-user "not before" cutoff, or a per-user signing key.

**FAIL**

```text
POST /logout        -> delete the cookie, 204
POST /password      -> update hash; refresh tokens untouched
access token exp = 24h; resource server checks signature and exp only
```

**PASS**

```text
POST /logout        -> mark the refresh token (and its grant) revoked in the store
POST /password     -> revoke every refresh token of the user; set user.tokens_valid_after = now
disable account     -> same
access token exp = 5-15 min; resource server rejects iat < user.tokens_valid_after
```

**Counterpoint.** "Stateless tokens exist to avoid a lookup." Refresh already hits the store, so revoking there is free; only the access-token window needs a decision. A short lifetime accepts that window; a per-user cutoff costs one cached read per request. Name which one you chose, and do not claim revocation is immediate if it is not.

**See also.** [[svc-session-lifecycle]] owns server-side logout for cookie sessions; [[svc-password-reset]] owns session revocation on reset; [[svc-api-key-scope]] owns revocation of API keys.

# Token revocation pass, 2026-11-12

Sources for the draft card `svc-token-revocation`. Each page was fetched on 2026-11-12.

- AWS Cognito: https://docs.aws.amazon.com/cognito/latest/developerguide/token-revocation.html. Revoking a refresh token invalidates the access tokens it issued. `GlobalSignOut` and `AdminUserGlobalSignOut` revoke all of a user's tokens, and disabling a user revokes refresh and access tokens. Revoked JWTs still pass a library that checks only signature and `exp`.
- Auth0: https://auth0.com/docs/secure/tokens/refresh-tokens/revoke-refresh-tokens. Revocation takes effect at once and invalidates every token issued for the same grant. The page does not say what happens to an issued access token, so the expiry gap is not backed by Auth0 alone.
- Microsoft Entra: https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens. Lists which changes revoke refresh tokens: password change, self-service reset, user or admin revoking all tokens, single sign-out. Not every token class is revoked by every change, so the card says "credential change" without naming a matrix.
- Google: https://developers.google.com/identity/protocols/oauth2/web-server. Revoking an access token that has a refresh token revokes the refresh token too. Revocation may take time to have full effect.
- IETF RFC 7009: https://www.rfc-editor.org/rfc/rfc7009. The server must support revoking refresh tokens, should invalidate access tokens of the same grant if it supports it, and otherwise the deployment must account for the risk.
- OWASP ASVS 5.0 V7: https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x16-V7-Session-Management.md. 7.4.1 (reference tokens invalidated in the backend; self-contained tokens need a revocation list, a per-user cutoff time, or per-user signing key rotation), 7.4.2 (end all sessions when an account is disabled or deleted), 7.4.3 (offer to end other sessions after a factor change).

Not used: the OWASP JWT cheat sheet. The fetch returned 404 on both the site and the raw Markdown path. OWASP counts once, so it would add no organisation.

Organisations: AWS, Auth0 (Okta), Microsoft, Google, IETF, OWASP. The clause "revoke refresh tokens at logout, credential change and disable" has Cognito, Entra, Auth0, Google and ASVS behind it. The clause on the access-token window has Cognito, RFC 7009 and ASVS. Auth0's page is silent on it. A stable pass still has to check rules 1 to 10.

## Stable pass, 2026-11-12

Two more pages, fetched the same day:

- Microsoft Entra continuous access evaluation: https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation. Access tokens last one hour by default. A disabled or deleted user, a password change, and an admin revoking all refresh tokens are critical events the resource provider checks. Microsoft found that only shortening token lifetimes degrades reliability without removing the risk, so it adds a revocation check.
- Auth0 access tokens: https://auth0.com/docs/secure/tokens/access-tokens. Set the validity period from the API's security needs. It does not mention revocation.

Per clause, after the pass:

- Revoke at logout: Cognito (`RevokeToken`, `GlobalSignOut`), ASVS 7.4.1, Entra single sign-out (it revokes only public-client tokens, not confidential ones). Three, with Entra partial.
- Revoke at account disable: Cognito (disabling revokes refresh and access tokens), ASVS 7.4.2, Entra CAE. Three.
- Access-token window: Cognito, RFC 7009, ASVS 7.4.1, Entra CAE. Four.
- Revoke at credential change: Entra only states it as a rule. ASVS 7.4.3 offers it as an option, and Cognito and Auth0 are silent. It moved to Why, and `svc-password-reset` already owns the reset case (rule 8).

Auth0's revocation page backs the mechanism (revoking a refresh token kills its grant) but no single clause above, so it is a reference. Google's page covers app removal, not logout or disable. The card stays at `should-fix`: ASVS puts 7.4.1 at level 1, but no source calls a missing revocation a release blocker.

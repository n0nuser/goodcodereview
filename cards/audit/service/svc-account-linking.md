---
id: svc-account-linking
level: service
tags: [security, authn, accounts]
severity: block
status: stable
lang: core
applies_when: The service links a federated identity to an existing account, or looks up an account by an email or profile claim.
context: [server]
tool_gate: none
note: the practical gate is an integration test: a local account with an unverified email, then an IdP sign-in asserting the same address, must not merge without proof of control of the local account
borrowed_from:
  - https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://pages.nist.gov/800-63-4/sp800-63c/Federation/
  - https://auth0.com/docs/manage-users/user-accounts/user-account-linking
  - https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
  - https://openid.net/specs/openid-connect-core-1_0.html
---

**Rule.** Link a federated identity to an existing account only after proving control of both, and key the link on the pair `iss` and `sub`, never on an unverified email or another profile claim.

**Why.** An attacker who registers a victim's address first can wait for the victim to press "Sign in with Google" and inherit the account through an automatic merge. The same bug appears when an IdP asserts an address it never verified, or one that changed owner since it did. An authenticated session on the existing account, plus a freshly authenticated federated identity, proves both sides. `iss` and `sub` together are the only stable key; email, `preferred_username` and name can be reused or reassigned, so they are a lookup hint at best.

**FAIL**

```python
if user.email == claims["email"]:
    user.identities.append(claims["sub"])     # merges on an unverified claim
```

**PASS**

```python
if session.user is None:                         # control of the existing account
    raise PermissionDenied
if not (claims["iss"] and claims["sub"]):        # a stable federated key
    raise PermissionDenied
link(session.user, key=(claims["iss"], claims["sub"]))
# email stays a display field, never the lookup key
```

**Counterpoint.** "Users expect the Google button to find the account with their email." Find it by a verified address if you like, then stop and require the password or an authenticated session before linking. A verified flag is not always present, and an address verified at signup can belong to someone else today, so verify it yourself when the IdP does not. Treating the match as proof is what the attack needs. Google says that where it is authoritative for the address (a `@gmail.com` address, or `email_verified` with `hd` set) you may skip a password challenge. That settles who owns the address, not who controls the local account, so an IdP that is authoritative for the domain may be trusted for the lookup, and the merge still needs the authenticated local session when the local address was never verified.

**See also.** [[svc-auth-throttle-generic-errors]] covers the enumeration that makes pre-registration cheap.

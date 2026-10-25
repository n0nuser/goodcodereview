---
id: svc-auth-throttle-generic-errors
level: service
tags: [security, authn, rate-limit]
severity: block
status: stable
lang: core
applies_when: The service has a login, password-reset or one-time-code endpoint.
tool_gate: Rate-limit middleware on auth routes; test that known and unknown users get identical responses.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
  - https://pages.nist.gov/800-63-4/sp800-63b.html
  - https://portswigger.net/web-security/authentication/password-based
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228-upd1.pdf
  - https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity-configuration
  - https://auth0.com/docs/secure/attack-protection/brute-force-protection
  - https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection
---

**Rule.** Limit failed attempts per account, and return the same message and status code whether or not the account exists.

**Why.** Unlimited guesses make passwords and 6-digit codes brute-forceable. Different errors for "no such user" and "wrong password" let an attacker list valid accounts first. Limit per account, since a per-IP limit is bypassed by rotating addresses. Response time leaks the same fact: if the code hashes the password only when the user exists, a fast reply means "no such user", so hash on every attempt. Registration needs its own design: give the same reply whether or not the address is taken, and email the owner of an existing account instead of creating a second one.

**FAIL**

```text
if not user: return "No such user", 404
if not check(pw): return "Wrong password", 401      # no attempt limit
```

**PASS**

```text
if too_many_failures(account_key): return "Try again later", 429   # checked before the password
ok = check(pw, user.pw_hash if user else DUMMY_HASH)              # hash runs either way
if not (user and ok): record_failure(account_key); return "Invalid credentials", 401
```

**Counterpoint.** "A lockout lets attackers lock out real users." Use a rising delay, not a permanent lock, and keep the recovery flow reachable. Log every lockout so abuse shows up.

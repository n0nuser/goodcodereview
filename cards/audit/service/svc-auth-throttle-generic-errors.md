---
id: svc-auth-throttle-generic-errors
level: service
tags: [security, authn, rate-limit]
severity: block
status: draft
lang: core
applies_when: The service has a login, password-reset, registration or one-time-code endpoint.
tool_gate: Rate-limit middleware on auth routes; test that known and unknown users get identical responses.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
---

**Rule.** Limit failed attempts per account, and return the same message, status and timing whether or not the account exists.

**Why.** Unlimited guesses make passwords and 6-digit codes brute-forceable. Different errors for "no such user" and "wrong password" let an attacker list valid accounts first. Limit per account, since a per-IP limit is bypassed by rotating addresses.

**FAIL**

```text
if not user: return "No such user", 404
if not check(pw): return "Wrong password", 401      # no attempt limit
```

**PASS**

```text
if not (user and check(pw)): record_failure(account_key); return "Invalid credentials", 401
if too_many_failures(account_key): return "Try again later", 429   # same shape, unlock by email
```

**Counterpoint.** "A lockout lets attackers lock out real users." Use a rising delay, not a permanent lock, and keep the recovery flow reachable. Log every lockout so abuse shows up.

---
id: svc-password-reset
level: service
tags: [security, authn, passwords]
severity: block
status: stable
lang: core
applies_when: The service emails or texts a password-reset link or code.
context: [server]
tool_gate: none
note: single-use - OWASP, Auth0, Django; short-lived - OWASP, Auth0, NIST; revoke sessions - MSRC, Auth0, Django, with OWASP leaving it optional. Storing only a hash of the token (OWASP and NIST for recovery codes) and revoking other outstanding reset links (OWASP, after suspected compromise) have too few sources, so they are in Why. The practical gate is a test that redeems a token twice, redeems an expired one, and then replays an old session cookie; the request endpoint's reply and rate limit belong to svc-auth-throttle-generic-errors
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
  - https://pages.nist.gov/800-63-4/sp800-63b/events/
  - https://auth0.com/docs/authenticate/database-connections/password-change
  - https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks
  - https://docs.djangoproject.com/en/5.2/topics/auth/default/
---

**Rule.** Make the reset token single-use and short-lived, and on success revoke every session.

**Why.** A reset link is a bearer password that arrives in a mailbox. If it works twice, a forwarded mail, a mail scanner or a backup keeps the access alive. If it lives for days, an attacker has days to use it. And a reset that leaves the old sessions open changes the password without evicting the intruder who already had a session. Two further habits cost little: store only a hash of the token, so a database read or a backup hands over no working links, and revoke the other outstanding reset links on success.

**FAIL**

```text
token = f"{user.id}-{int(time.time())}"
user.reset_token = token             # predictable, stored in clear, usable again
send_email(link(token))
```

**PASS**

```python
raw = secrets.token_urlsafe(32)
db.store(sha256(raw), user=user, expires=now + 15 * MINUTE)
# the raw value exists only in the mail
consume_once(raw)
revoke_sessions(user)
revoke_other_resets(user)
```

**Counterpoint.** "The token is random, so hashing it adds nothing." The mail, the link and every log between you and the user still carry the raw value; the hash protects the copy at rest, which is the copy an attacker reads. OWASP treats session invalidation as the user's choice in the normal flow and requires it after suspected compromise; this card asks for it every time because the reset may be the owner's answer to a stolen session. Pick the lifetime from a number the support flow can meet, not from the word "short", and send a notification after the reset so a change the owner did not make is visible.

**See also.** [[svc-auth-throttle-generic-errors]] owns the identical reply and the rate limit on the request; [[fn-csprng-for-secrets]] owns the token source, and [[fn-password-slow-hash]] owns the new password.

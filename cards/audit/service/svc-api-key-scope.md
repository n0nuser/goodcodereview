---
id: svc-api-key-scope
level: service
tags: [security, secrets, api]
severity: should-fix
status: stable
lang: core
applies_when: The service issues an API key or long-lived access token to a caller.
context: [server]
tool_gate: none
note: exposure paths are covered by code-secret-scan, svc-no-secrets-in-url and sys-secrets-and-errors; this card covers what the issued key is allowed to do
borrowed_from:
  - https://cloud.google.com/docs/authentication/api-keys
  - https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens
  - https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure
  - https://docs.stripe.com/keys-best-practices
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
  - https://docs.gitlab.com/security/tokens/
---

**Rule.** Issue each API key with the narrowest scopes and a bounded lifetime, and rotate or revoke it after any exposure.

**Why.** A key with account-wide scope turns one leaked string into the whole account, and a key with no end date is still valid years after the integration was forgotten. Scopes bound what a leak can do; an expiry or a rotation bounds how long it can do it. Rotating on a schedule, as Google and Stripe advise, also shows whether you can replace the key before an incident forces the question. Show the secret once, at creation, as AWS does.

**FAIL**

```text
key = "sk_live_..."          # full account scope, no expiry
db.insert(user_id, key)      # plaintext, returned by every read
```

**PASS**

```python
key = issue(user, scopes=["orders:read"], expires_in=90 * DAY)
return key                   # shown once
# rotate on a schedule; revoke at once on exposure
```

**Counterpoint.** "Short expiry and rotation break integrations that nobody watches." That is the cost, and it is smaller than a key that never dies. Prefer a temporary credential where the platform offers one, give each integration its own key so rotation is one at a time, and keep the overlap window long enough for a deploy. A shared key with no owner cannot be rotated safely, which is the real defect.

**See also.** [[svc-no-secrets-in-url]] covers the key in a query string; [[code-secret-scan]] catches one committed to the repository.

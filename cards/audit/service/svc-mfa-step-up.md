---
id: svc-mfa-step-up
level: service
tags: [security, authn, mfa]
severity: should-fix
status: stable
lang: core
applies_when: The service offers multi-factor authentication, or lets a signed-in user change a password, email address, or authentication factor.
context: [server]
tool_gate: none
note: the practical gate is an integration test: a session that passed password-only login gets a step-up challenge on every sensitive route, including factor change; svc-session-lifecycle covers timeouts, not the assurance behind the current session
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
  - https://pages.nist.gov/800-63-4/sp800-63b/events/
  - https://pages.nist.gov/800-63-4/sp800-63b/session/
  - https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/protected-actions-overview
  - https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication
  - https://learn.microsoft.com/en-us/entra/identity/authentication/howto-registration-mfa-sspr-combined
---

**Rule.** Require a fresh authentication with an already-bound factor before sensitive actions and before adding, replacing or removing an MFA factor; an existing session alone is not enough.

**Why.** A session that passed a password check says nothing about who holds it now. Let that session enrol a new phone or replace an authenticator and an attacker with a stolen cookie keeps the account after the password is changed. The same gap covers password, email and admin-role changes. Step-up at the action asks for the factor only when it matters, and a short freshness window keeps the prompt rare. A session must not be treated as stronger than the authentication that created it. A user who lost the only factor needs a documented recovery path, such as single-use recovery codes or a temporary access pass. That path is part of the control, and it is judged as a separate recovery flow.

**FAIL**

```text
@login_required
def add_phone():
    user.phone = request.form["phone"]      # any old session can replace the second factor
```

**PASS**

```text
@login_required
@recent_auth(max_age=300, factor="existing")
def add_phone():
    user.phone = request.form["phone"]
    notify(user, "phone changed")
```

**Counterpoint.** "Prompting on every sensitive action annoys users, and a user who lost the only factor gets locked out." Use risk and a recent-auth window so the prompt appears only when the session is stale or the action is high risk, and keep the recovery path described above; without it, step-up becomes a denial of service against the account's owner.

**See also.** [[svc-auth-throttle-generic-errors]] covers guessing the factor; [[svc-session-lifecycle]] covers the session that carries the result.

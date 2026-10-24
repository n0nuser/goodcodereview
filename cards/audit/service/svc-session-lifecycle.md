---
id: svc-session-lifecycle
level: service
tags: [security, authn, sessions]
severity: block
status: draft
lang: core
applies_when: The service sets a session cookie or session ID after login.
tool_gate: Header test on the login response; session fixation test in the end-to-end suite.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control
---

**Rule.** Issue a new session ID at login, set `Secure`, `HttpOnly` and `SameSite` on the cookie, and end the session on the server at logout.

**Why.** A session ID that survives login can be planted by an attacker beforehand (fixation). A cookie without `HttpOnly` is readable by any injected script. A logout that only clears the browser leaves the stolen cookie valid. Also enforce an idle and an absolute timeout on the server.

**FAIL**

```text
Set-Cookie: sid=abc123
login():  keep the pre-login session id
logout(): response.delete_cookie("sid")      # server session still valid
```

**PASS**

```text
Set-Cookie: __Host-sid=<new random>; Secure; HttpOnly; SameSite=Lax; Path=/
login():  session.regenerate()
logout(): sessions.destroy(sid)             # then clear the cookie
```

**Counterpoint.** "JWT sessions are stateless, so there is nothing to destroy." Then keep the token short-lived and add a server-side revocation list for logout; see [[fn-jwt-verify-pinned]].

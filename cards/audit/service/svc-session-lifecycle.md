---
id: svc-session-lifecycle
level: service
tags: [security, authn, sessions]
severity: block
status: stable
lang: core
applies_when: The service sets a session cookie or session ID after login.
tool_gate: Header test on the login response; session fixation test in the end-to-end suite.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control
  - https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies
  - https://pages.nist.gov/800-63-4/sp800-63b/session/
  - https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html
  - https://guides.rubyonrails.org/security.html
---

**Rule.** Issue a new session ID at login, and set `Secure`, `HttpOnly` and `SameSite` on the session cookie.

**Why.** A session ID that survives login can be planted by an attacker beforehand (fixation). A cookie without `HttpOnly` is readable by any injected script, and one without `Secure` travels over plain HTTP. Also end the session on the server at logout, because clearing only the browser cookie leaves a stolen copy valid, and enforce idle and absolute timeouts on the server.

**FAIL**

```text
Set-Cookie: sid=abc123
login():  keep the pre-login session id
```

**PASS**

```text
Set-Cookie: __Host-sid=<new random>; Secure; HttpOnly; SameSite=Lax; Path=/
login():  session.regenerate()
```

**Counterpoint.** "The framework already does this." Some do: Spring Security changes the session ID at login by default, and Rails gives you `reset_session`. Hand-written login code and custom session stores often skip it, and cookie flags depend on configuration. Check the login handler and the real `Set-Cookie` header, not the framework's reputation.

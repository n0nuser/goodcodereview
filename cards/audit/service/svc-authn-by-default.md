---
id: svc-authn-by-default
level: service
tags: [security, authn]
severity: block
status: draft
lacks: evidence, MITRE, Microsoft, Django and Spring are listed, but no stable pass has read them for a recommendation versus a definition
lang: core
applies_when: The service has routes that need a signed-in user next to routes that are public.
tool_gate: A framework fallback that requires authentication (ASP.NET Core `FallbackPolicy`, Django `LoginRequiredMiddleware`, Spring Security `anyRequest().authenticated()`); a test that calls every route without credentials and expects 401 or a login redirect unless the route is on the public list.
note: svc-authz-central-deny-default decides what a known user may do; this card decides whether an anonymous caller gets in at all (CWE-306)
borrowed_from:
  - https://cwe.mitre.org/data/definitions/306.html
  - https://learn.microsoft.com/en-us/aspnet/core/security/authorization/secure-data
  - https://docs.djangoproject.com/en/5.2/ref/middleware/
  - https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html
---

**Rule.** Require authentication on every route by default, and mark each public route by name.

**Why.** When each handler opts in to authentication, the one that forgets is open to the internet, and nothing in the diff looks wrong. A global fallback flips the default: a new route is closed until someone marks it public, and that mark is a line a reviewer can question. Health checks and internal admin ports count as routes too.

**FAIL**

```python
@app.get("/invoices/<id>")          # no login check; anonymous callers get the invoice
def invoice(id): ...
```

**PASS**

```python
PUBLIC = {"login", "health", "static"}

@app.before_request
def require_login():
    if request.endpoint not in PUBLIC and not current_user.is_authenticated:
        abort(401)
```

**Counterpoint.** "Our gateway already checks the token." Then the service trusts every caller that can reach it without the gateway: another pod, a debug port, a misrouted path. Keep the gateway check and the fallback in the service. The fallback costs one middleware.

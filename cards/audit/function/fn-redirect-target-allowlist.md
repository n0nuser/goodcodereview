---
id: fn-redirect-target-allowlist
level: function
tags: [security, redirect, url]
severity: should-fix
status: draft
lacks: evidence, OWASP, Microsoft, PortSwigger and GitHub are listed, but no stable pass has read them for a recommendation versus a definition
lang: core
applies_when: A handler redirects to a URL taken from a query parameter, form field, header, or stored value, such as `?next=` after login.
tool_gate: CodeQL `py/url-redirection`; ASP.NET Core `LocalRedirect` or `Url.IsLocalUrl`.
note: ASVS 3.7.2 (allowlisted redirect hosts) and 1.2.2 (safe URL schemes); sys-ssrf covers the server following redirects, not sending users to them
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html
  - https://cwe.mitre.org/data/definitions/601.html
  - https://learn.microsoft.com/en-us/aspnet/core/security/preventing-open-redirects
  - https://portswigger.net/kb/issues/00500100_open-redirection-reflected
  - https://codeql.github.com/codeql-query-help/python/py-url-redirection/
---

**Rule.** Redirect only to a local path or to a host on a server-side allowlist, never to a URL taken from the request as is.

**Why.** A link such as `https://bank.example/login?next=https://evil.example` carries your domain, so users and mail filters trust it, and after login the user lands on a phishing page. When page script sets `location` from the same value, a `javascript:` URL runs as script. Parse the URL and compare its scheme and host. A `startswith("/")` check alone passes `//evil.example`, and browsers read `/\evil.example` the same way. Better still, accept a short name and map it to the URL on the server.

**FAIL**

```python
return redirect(request.args["next"])
```

**PASS**

```python
target = urlparse(request.args.get("next", "/"))
if target.scheme or target.netloc or not target.path.startswith("/") or "\\" in target.path:
    target = urlparse("/")
return redirect(target.path)
```

**Counterpoint.** "The redirect only matters after a successful login." That is when it hurts most: the user has just typed a password and trusts the next page. A phishing copy of the login form on that page collects the password a second time.

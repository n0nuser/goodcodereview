---
id: svc-host-header-trust
level: service
tags: [security, http, authn]
severity: block
status: stable
lang: core
applies_when: The service builds an absolute URL from the request, or reads `Host` or `X-Forwarded-*` to decide what to serve or where to send a user.
context: [server]
tool_gate: Framework host allowlist configured (`ALLOWED_HOSTS`, `AllowedHosts`, `config.hosts`, `trustHosts`), and a test that sends a hostile `Host` and expects 400.
note: fn-redirect-target-allowlist checks where a redirect points; this card checks how a URL is built and which Host values the service answers. configured base URL - PortSwigger, Fastly and Rails; allowlist - PortSwigger, Fastly, Django, Microsoft, Rails and Laravel; trusted proxy - Django, Microsoft, PortSwigger and Fastly; duplicate Host has IETF and Fastly only, so it is in Why
borrowed_from:
  - https://portswigger.net/web-security/host-header
  - https://www.fastly.com/learning/security/what-are-http-host-header-attacks
  - https://docs.djangoproject.com/en/5.2/ref/settings/
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/host-filtering
  - https://learn.microsoft.com/en-us/aspnet/core/host-and-deploy/proxy-load-balancer
  - https://guides.rubyonrails.org/action_mailer_basics.html
  - https://guides.rubyonrails.org/configuring.html
  - https://laravel.com/docs/12.x/passwords
  - https://www.rfc-editor.org/rfc/rfc9112.html
---

**Rule.** Build absolute URLs from configured values, answer only for a `Host` on an allowlist, and take `X-Forwarded-*` values only from a trusted proxy.

**Why.** A reset link built from the request `Host` carries whatever domain the attacker sent. The victim asks for a reset, the mail arrives with the attacker's host, and the token goes to the attacker when the link is opened. The same value drives routing, cache keys, and absolute redirects. A forwarded header is worse, because many stacks accept `X-Forwarded-Host` from any client and use it in place of `Host`. Two `Host` headers are a second route to the same disagreement: one component validates the first and another reads the last, so reject a request that carries more than one.

**FAIL**

```python
reset = f"https://{request.headers['Host']}/reset?token={token}"
# no allowlist, and X-Forwarded-Host is honoured from any client
```

**PASS**

```python
reset = f"{settings.PUBLIC_BASE_URL}/reset?token={token}"
ALLOWED_HOSTS = ["app.example.com"]      # Django; any other Host: 400
TRUSTED_PROXIES = {"10.0.0.10"}          # pseudo-config: your proxy middleware's setting
                                         # (Django: USE_X_FORWARDED_HOST stays off unless a proxy sets it)
```

**Counterpoint.** "A reverse proxy sets `Host`, so the value can be trusted." It can only be trusted when the proxy overwrites any client-supplied value and the app accepts requests only from the proxy's address. An app that is reachable directly, or a proxy that passes the client header through, hands the value back to the attacker.

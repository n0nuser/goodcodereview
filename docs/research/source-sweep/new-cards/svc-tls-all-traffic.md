---
id: svc-tls-all-traffic
level: service
tags: [security, tls, network]
severity: should-fix
status: draft
lacks: unreviewed, sources listed but no stable pass has checked them against rules 1 to 10
lang: core
applies_when: The service exposes an HTTP-based API, or the code calls one.
context: [server]
tool_gate: A scan in CI that the public API host refuses port 80, plus a lint that flags `http://` URL literals in client code.
borrowed_from:
  - https://infosec.mozilla.org/guidelines/web_security
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x21-V12-Secure-Communication.md
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228-upd1.pdf
---

**Rule.** Serve and call every HTTP-based API over TLS, with no plaintext fallback.

**Why.** A plaintext listener or an `http://` call lets anyone on the path read tokens and payloads, or rewrite them. A redirect from port 80 does not fix it: the first request already went out in the clear. Turn plain HTTP off for APIs instead of redirecting it. This card is about whether traffic is encrypted at all. Protocol versions and certificate checks are covered by [[svc-tls-modern-only]] and [[fn-tls-verify-on]].

**FAIL**

```nginx
server {
    listen 80;
    server_name api.example.com;
    location / { proxy_pass http://unix:/run/app.sock; }
}
```

**PASS**

```nginx
server {
    listen 443 ssl;
    server_name api.example.com;
    ssl_certificate     /etc/ssl/api.crt;
    ssl_certificate_key /etc/ssl/api.key;
    location / { proxy_pass http://unix:/run/app.sock; }
}
```

**Counterpoint.** "Traffic between our own services never leaves the private network." A flat network means one compromised host can read all of it. Terminating TLS in a mesh or sidecar makes internal encryption cheap, so the exception costs more than it saves.

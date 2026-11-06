---
id: svc-cache-key-completeness
level: service
tags: [security, http, caching]
severity: block
status: stable
lang: core
applies_when: A shared cache (CDN, reverse proxy, gateway, or framework cache) stores responses the service generates.
context: [server]
tool_gate: A test that sends an unkeyed header or a GET body and asserts the response body does not change.
note: svc-api-cache-control owns Cache-Control and Vary; the key and the unkeyed inputs are this card. key completeness - AWS, Cloudflare and Fastly (the Microsoft Front Door page covers only query-string keying, so it is not a source); unkeyed input kept out of the body - Cloudflare, PortSwigger and Fastly; static-only caching has Cloudflare, PortSwigger and Google but vendors disagree, so it is in Why
borrowed_from:
  - https://portswigger.net/web-security/web-cache-poisoning
  - https://developers.cloudflare.com/cache/cache-security/avoid-web-poisoning/
  - https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/understanding-the-cache-key.html
  - https://www.fastly.com/documentation/guides/full-site-delivery/caching/preventing-cache-poisoning/
  - https://www.fastly.com/documentation/guides/full-site-delivery/caching/manipulating-the-cache-key/
  - https://cloud.google.com/cdn/docs/caching
---

**Rule.** Key every request input that can change the response, and strip any other request value before it reaches a cached body.

**Why.** A cache keeps one response per key. If the origin echoes a header, a cookie, or a GET body that the key ignores, the first request stores content that every later visitor receives. An attacker can then place content on your domain without touching the origin: a link or a form. A value that reaches the body belongs in the key, or it must not reach the body at all. Caching only static types by default narrows the surface, though CDN defaults differ.

**FAIL**

```text
GET /home HTTP/1.1
X-Forwarded-Host: attacker.example

origin body: <a href="https://attacker.example/account">Account</a>
cache key: path only
```

The next visitor to `/home` receives the cached copy, with the attacker's host in the link.

**PASS**

```text
edge: strip X-Forwarded-Host, X-Original-URL and X-Rewrite-URL before the origin
edge: return 400 to a GET with a body, or bypass the cache for it
origin: echo a header only when it is in Vary or the cache key
Cache-Control: public, max-age=60   Vary: Accept-Language
```

**Counterpoint.** "We leave that header out of the key to keep the hit rate up." It does raise the hit rate, by serving one requester's variant to everyone. Strip or rewrite the value when the response does not need it, and key it when it does.

**See also.** [[svc-api-cache-control]] owns `Cache-Control` and `Vary`; an input that changes the body must appear in the key or in `Vary`.

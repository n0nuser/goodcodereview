---
id: svc-api-cache-control
level: service
tags: [performance, security, api, http, caching]
severity: should-fix
status: stable
lang: core
applies_when: A service returns responses that a browser, CDN, gateway or client library may cache.
context: [server]
tool_gate: Integration test or header lint that rejects a 200 GET without `Cache-Control`.
note: do not let an edge rule override the origin header - PortSwigger, AWS, Google and Microsoft; decide cacheability by Content-Type - PortSwigger, Cloudflare and Google; "the origin and the cache read the path the same way" has PortSwigger only, so it is in Why
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9111.html
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html
  - https://portswigger.net/web-security/web-cache-deception
  - https://developers.cloudflare.com/cache/cache-security/cache-deception-armor/
  - https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/Expiration.html
  - https://cloud.google.com/cdn/docs/caching
  - https://learn.microsoft.com/en-us/azure/frontdoor/front-door-caching
---

**Rule.** Set an explicit `Cache-Control` on every response a cache may store, use `private` or `no-store` for user-specific data, add `Vary` for any request header that changes the body, keep the origin's `Cache-Control` authoritative at the edge (no minimum TTL or force-cache override), and decide cacheability by the response `Content-Type`, not the URL extension.

**Why.** With no directive, a cache may guess a lifetime from `Last-Modified`. A shared cache may then serve one user's response to another, or serve stale data for hours after a write. A dynamic page requested at `/account/x.css` is the same failure from the cache side: a rule that decides by extension stores a private page, and an edge rule that overrides `no-store` keeps it. The origin and the cache must also read the path the same way. When they do not, a path the origin treats as private can look like a static file to the cache.

**FAIL**

```text
GET /me/orders  -> 200
(no Cache-Control, no Vary; body differs per Authorization)

edge: GET /account/x.css -> stored for 1 hour
edge: minimum TTL 3600 s, so origin Cache-Control: private, no-store is overridden
```

**PASS**

```text
GET /me/orders  -> 200  Cache-Control: private, no-store
GET /plans      -> 200  Cache-Control: public, max-age=300
                         Vary: Accept-Language

edge: minimum TTL 0, origin headers kept
edge: /account/x.css not stored; Content-Type: text/html does not match .css
```

**Counterpoint.** "Our CDN bypasses the cache for logged-in users." That config is a second place to get wrong, and it does not cover the browser. A cache rule that sets a minimum TTL, or a force-cache mode, can still beat the origin header. Check the specific policy value, and keep secrets out of cacheable URLs even when the header is right.

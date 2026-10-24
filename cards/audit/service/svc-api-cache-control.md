---
id: svc-api-cache-control
level: service
tags: [api, http, caching]
severity: should-fix
status: draft
lang: core
applies_when: A service returns responses that a browser, CDN, gateway or client library may cache.
tool_gate: Integration test or header lint that rejects a 200 GET without `Cache-Control`.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9111.html
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Set an explicit `Cache-Control` on every response a cache may store, use `private` or `no-store` for user-specific data, and add `Vary` for any request header that changes the body.

**Why.** With no directive, a cache may guess a lifetime from `Last-Modified`. A shared cache may then serve one user's response to another, or serve stale data for hours after a write.

**FAIL**

```text
GET /me/orders  -> 200
(no Cache-Control, no Vary; body differs per Authorization)
```

**PASS**

```text
GET /me/orders  -> 200  Cache-Control: private, no-cache
GET /plans      -> 200  Cache-Control: public, max-age=300
                         Vary: Accept-Language
```

**Counterpoint.** "Our CDN is configured to bypass the cache." That config is a second place to get wrong, and it does not cover browsers. The origin states the intent; the CDN may tighten it. `no-store` is not a privacy control against a cache that ignores it, so keep secrets out of cacheable URLs too.

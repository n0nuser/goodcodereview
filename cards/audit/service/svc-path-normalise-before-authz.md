---
id: svc-path-normalise-before-authz
level: service
tags: [security, http, authz]
severity: should-fix
status: draft
lacks: orgs, Envoy and Istio each state the normalise clause; escaped-slash rejection has Envoy only; PortSwigger and Cloudflare describe attacks or features
lang: core
applies_when: A proxy, gateway or CDN sits in front of the service and a deny, allow or cache rule matches on the URL path.
context: [server]
tool_gate: A test that requests `/admin`, `/%61dmin`, `/admin%2Fusers` and `/ADMIN` through the edge and expects the same denial as `/admin`, or 400.
note: Envoy (edge best practices) and Istio (authorization best practices) tell operators to normalise the path before policy. Istio builds on Envoy but is a separate CNCF project, so it counts as its own organisation. Cloudflare describes its normalisation feature and is soft. The PortSwigger page describes the attack and states no fix, so it does not count
borrowed_from:
  - https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/http/header_validators/envoy_default/v3/header_validator.proto.html
  - https://portswigger.net/web-security/web-cache-deception
  - https://www.envoyproxy.io/docs/envoy/latest/configuration/best_practices/edge
  - https://istio.io/latest/docs/ops/best-practices/security/
  - https://developers.cloudflare.com/rules/normalization/
---

**Rule.** Normalise the URL path once at the first hop, or reject escaped slashes there, so every hop resolves a path to the same resource before any routing or authorisation rule runs.

**Why.** A deny rule matches the string it sees. If the edge reads `/admin%2Fusers` as one segment and the origin decodes it to `/admin/users`, the rule passes a request the origin then serves. The same gap lets a cache store a private page as a static file. Resolve the path in one place, and refuse the forms you will not resolve.

**FAIL**

```yaml
# illustrative pseudo-config, not a real Envoy field
# edge: deny by literal prefix, path forwarded as received
- match: { prefix: "/admin" }
  action: deny
# GET /admin%2Fusers passes the prefix check; the origin decodes it and serves /admin/users
```

**PASS**

```yaml
# HTTP connection manager
normalize_path: true
merge_slashes: true
path_with_escaped_slashes_action: REJECT_REQUEST   # %2F and %5C get a 400
```

**Counterpoint.** "Some clients send escaped slashes on purpose, such as an ID that contains a slash." Put that value in a query parameter or a body field, or encode it in a form that is not a path separator. A path that means two things at two hops is the defect, and the legitimate caller can change.

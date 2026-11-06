# service

## svc-account-linking

severity: block  
concerns: security  
applies_when: The service links a federated identity to an existing account, or looks up an account by an email or profile claim.  
context: server  
Backed by: Microsoft (unjudged), OWASP (unjudged), NIST (unjudged), Okta (Auth0) (unjudged), Google (unjudged), OpenID Foundation (unjudged). Backing: unjudged.

**Rule.** Link a federated identity to an existing account only after proving control of both, and key the link on the pair `iss` and `sub`, never on an unverified email or another profile claim.

**Why.** An attacker who registers a victim's address first can wait for the victim to press "Sign in with Google" and inherit the account through an automatic merge. The same bug appears when an IdP asserts an address it never verified, or one that changed owner since it did. An authenticated session on the existing account, plus a freshly authenticated federated identity, proves both sides. `iss` and `sub` together are the only stable key; email, `preferred_username` and name can be reused or reassigned, so they are a lookup hint at best.

**FAIL**

```python
if user.email == claims["email"]:
    user.identities.append(claims["sub"])     # merges on an unverified claim
```

**PASS**

```python
if session.user is None:                         # control of the existing account
    raise PermissionDenied
if not (claims["iss"] and claims["sub"]):        # a stable federated key
    raise PermissionDenied
link(session.user, key=(claims["iss"], claims["sub"]))
# email stays a display field, never the lookup key
```

**Counterpoint.** "Users expect the Google button to find the account with their email." Find it by a verified address if you like, then stop and require the password or an authenticated session before linking. A verified flag is not always present, and an address verified at signup can belong to someone else today, so verify it yourself when the IdP does not. Treating the match as proof is what the attack needs. Google says that where it is authoritative for the address (a `@gmail.com` address, or `email_verified` with `hd` set) you may skip a password challenge. That settles who owns the address, not who controls the local account, so an IdP that is authoritative for the domain may be trusted for the lookup, and the merge still needs the authenticated local session when the local address was never verified.

**See also.** [svc-auth-throttle-generic-errors](service.md#svc-auth-throttle-generic-errors) covers the enumeration that makes pre-registration cheap.

## svc-api-cache-control

severity: should-fix  
concerns: performance, security  
applies_when: A service returns responses that a browser, CDN, gateway or client library may cache.  
context: server  
tool gate: Integration test or header lint that rejects a 200 GET without `Cache-Control`.  
Backed by: IETF (unjudged), Zalando (unjudged), OWASP (supports), PortSwigger (unjudged), Cloudflare (unjudged), AWS (unjudged), Google (unjudged), Microsoft (unjudged). Backing: mixed.

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

## svc-api-conditional-writes

severity: should-fix  
concerns: correctness  
applies_when: Two callers can update the same resource through PUT, PATCH or DELETE.  
context: server  
tool gate: Integration test that sends a write with a stale `If-Match` and expects 412.  
Backed by: IETF (unjudged), Microsoft (unjudged), Zalando (unjudged). Backing: unjudged.

**Rule.** Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.

**Why.** A read-modify-write over HTTP is a race. The second writer overwrites the first without knowing it, and no error appears anywhere.

**FAIL**

```text
GET /docs/4  -> 200 {title: "A"}
PUT /docs/4  {title: "B"}   -> 200   # overwrites a change made after the GET
```

**PASS**

```text
GET /docs/4  -> 200  ETag: "v7"
PUT /docs/4  If-Match: "v7"  -> 200  ETag: "v8"
PUT /docs/4  If-Match: "v7"  -> 412 Precondition Failed
```

**Counterpoint.** "Last write wins is fine here." For a log or a counter it is; say so in the spec. For a document, a profile or a config that two people edit, it loses work. The card applies to shared resources that people edit.

## svc-api-contract-tests

severity: should-fix  
concerns: compatibility, testing  
applies_when: A service calls, or is called by, another service owned by a different team or deployed on its own schedule.  
context: server  
tool gate: Contract test run in CI for both sides, and a gate that blocks deploy when a consumer's contract fails against the provider.  
Backed by: Pact (unjudged), OpenAPI Initiative (unjudged), Microsoft (supports), Paradigma Digital (supports), Thoughtworks (supports). Backing: strong.

**Rule.** Run a contract test for each cross-service call, derived from the consumer's real requests, and fail the provider's build when it breaks one.

**Why.** A provider's own tests check what the provider thinks callers need. A spec check says what could happen, not what the consumer relies on. Only a check built from the consumer's usage catches the removed field before deploy, without a full-system end-to-end run.

**FAIL**

```text
billing calls GET /customers/{id} and reads "vat_id"
customers team removes "vat_id"; its tests pass; billing breaks in production
```

**PASS**

```text
billing CI publishes a contract: GET /customers/{id} -> body has "vat_id"
customers CI verifies every published contract and fails on the removal
```

**Counterpoint.** "End-to-end tests cover it." They are slow, need every service running, and run late. Contract tests run per service in minutes. Pact is one way; a consumer-written example set replayed against the provider also passes. For services deployed together from one repo, mark the card N/A.

## svc-api-deprecation-sunset

severity: should-fix  
concerns: compatibility  
applies_when: A service retires an endpoint, field, version or parameter that outside callers use.  
context: server  
tool gate: Middleware that adds both headers for routes tagged deprecated; a spec linter on `deprecated: true` without a sunset date; a dashboard counting calls that carry the headers.  
Backed by: IETF (unjudged), Zalando (unjudged), OpenAPI Initiative (unjudged), GitHub (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers.

**Why.** The `Sunset` date must not be earlier than the `Deprecation` date (RFC 9745). Callers cannot read your roadmap. A removal with no signal in the responses is an outage for whoever has not read the changelog. Counting calls that carry the headers also tells you when removal is safe.

**FAIL**

```text
git: delete GET /v1/orders/{id}/summary
responses before removal: no header, spec not marked deprecated
```

**PASS**

```text
GET /v1/orders/9/summary -> 200
  Deprecation: @1767225600
  Sunset: Wed, 01 Jul 2026 00:00:00 GMT
  Link: <https://api.example.com/docs/summary-removal>; rel="deprecation"
spec: deprecated: true
```

**Counterpoint.** "Our only callers are internal." Then the call count with the header gives you the list of owners to ask, and removal is cheap. [chg-expand-contract](change.md#chg-expand-contract) covers the order of steps; this card covers what the response tells the caller. Both headers describe one resource, so send them on each deprecated route, not only on the API root.

## svc-api-documented-errors

severity: should-fix  
concerns: correctness, compatibility  
applies_when: A service has an OpenAPI description, or callers depend on its error responses.  
context: server  
tool gate: Spec linter that requires 4xx and 5xx responses with a schema on every operation, and an example on each.  
Backed by: OpenAPI Initiative (unjudged), Zalando (unjudged), Siemens (supports). Backing: mixed.

**Rule.** Document every error status each operation can return, with a schema and one example.

**Why.** Callers write error handling from the spec. An operation that lists only 200 teaches them nothing about 404, 409, 422 or 429, so they find out in production.

**FAIL**

```text
/orders/{id}:
  get:
    responses:
      "200": {description: ok}
```

**PASS**

```text
/orders/{id}:
  get:
    responses:
      "200": {description: ok}
      "404": {$ref: "#/components/responses/Problem"}   # has an example
      "429": {$ref: "#/components/responses/RateLimited"}
```

**Counterpoint.** "A shared `default` response covers everything." OpenAPI allows `default`, but it hides which codes carry which meaning. List the codes a caller must act on and use `default` for the rest.

## svc-api-error-code-stable

severity: should-fix  
concerns: compatibility  
applies_when: Callers of an HTTP or RPC API branch on the kind of error.  
context: server  
tool gate: Spec linter that requires an enumerated error `type` or `reason` per operation; a test that pins the codes.  
Backed by: IETF (unjudged), Google (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Give each error a stable machine-readable code that callers branch on, and never make them parse the message text.

**Why.** Message text gets reworded, translated and fixed. A client that matches on "already exists" breaks on the first edit. A published code is a contract.

**FAIL**

```text
if "already exists" in response.json()["detail"]:   # client
    handle_conflict()
```

**PASS**

```text
if response.json()["type"] == "https://api.example.com/problems/order-exists":   # client
    handle_conflict()
# the server keeps that type value for as long as the API version lives
```

**Counterpoint.** "The HTTP status is enough." It is too coarse: two different 409 conflicts need different handling. Add a code only where callers act differently; do not mint one for every branch.

## svc-api-key-scope

severity: should-fix  
concerns: security  
applies_when: The service issues an API key or long-lived access token to a caller.  
context: server  
Backed by: Google (unjudged), GitHub (unjudged), Stripe (unjudged), AWS (unjudged), GitLab (unjudged). Backing: unjudged.

**Rule.** Issue each API key with the narrowest scopes and a bounded lifetime, and rotate or revoke it after any exposure.

**Why.** A key with account-wide scope turns one leaked string into the whole account, and a key with no end date is still valid years after the integration was forgotten. Scopes bound what a leak can do; an expiry or a rotation bounds how long it can do it. Rotating on a schedule, as Google and Stripe advise, also shows whether you can replace the key before an incident forces the question. Show the secret once, at creation, as AWS does.

**FAIL**

```text
key = "sk_live_..."          # full account scope, no expiry
db.insert(user_id, key)      # plaintext, returned by every read
```

**PASS**

```python
key = issue(user, scopes=["orders:read"], expires_in=90 * DAY)
return key                   # shown once
# rotate on a schedule; revoke at once on exposure
```

**Counterpoint.** "Short expiry and rotation break integrations that nobody watches." That is the cost, and it is smaller than a key that never dies. Prefer a temporary credential where the platform offers one, give each integration its own key so rotation is one at a time, and keep the overlap window long enough for a deploy. A shared key with no owner cannot be rotated safely, which is the real defect.

**See also.** [svc-no-secrets-in-url](service.md#svc-no-secrets-in-url) covers the key in a query string; [code-secret-scan](codebase.md#code-secret-scan) catches one committed to the repository.

## svc-api-naming-consistent

severity: discuss  
concerns: maintainability  
applies_when: A service defines JSON fields, query parameters, headers or path segments for an HTTP API.  
context: server  
tool gate: Spec linter with a casing rule per location.  
Backed by: Zalando (unjudged), Microsoft (unjudged), Google (supports), Kubernetes (supports). Backing: mixed.

**Rule.** Use one casing convention per location (fields, query parameters, headers, paths) across the whole API, and state it in the API guide.

**Why.** Mixed casing in one API makes callers look up each name. A client that guesses `orderId` after meeting `order_id` gets a silent null.

**FAIL**

```text
GET /orders?pageSize=20 -> {"order_id": 1, "createdAt": "...", "Total-Cents": 500}
```

**PASS**

```text
GET /orders?page_size=20 -> {"order_id": 1, "created_at": "...", "total_cents": 500}
# snake_case everywhere, as docs/api-guide.md says
```

**Counterpoint.** "Pick the right convention." The sources disagree: Zalando asks for snake_case, Microsoft for camelCase in fields. Either passes. Do not change an existing API's casing to match a guide; that is a breaking change.

## svc-api-problem-json

severity: should-fix  
concerns: compatibility  
applies_when: A service returns errors from an HTTP API to other services or to clients.  
context: server  
tool gate: Middleware that builds every error body from one problem-details type; a test that fails on an error response without the media type.  
Backed by: IETF (unjudged), Zalando (unjudged), UKHSA (supports). Backing: mixed.

**Rule.** Return errors as `application/problem+json` with a `status` that equals the HTTP status, and leave stack traces and internal detail out.

**Why.** Callers then parse every error one way. A body that differs per endpoint, or a `status` that disagrees with the real code, makes generic client and proxy handling unreliable. A stack trace in `detail` hands an attacker the implementation.

**FAIL**

```text
HTTP/1.1 500
Content-Type: text/html

<pre>NullPointerException at OrderRepo.java:88 ...</pre>
```

**PASS**

```text
HTTP/1.1 404
Content-Type: application/problem+json

{"type": "https://api.example.com/problems/order-not-found",
 "title": "Order not found", "status": 404,
 "detail": "No order with id 7731 for this account."}
```

**Counterpoint.** "We already have our own error envelope." That is fine inside one team's API, if it is one envelope and documented. The card asks for one shape everywhere; problem details is the one with a registered media type and existing client support. See [sys-secrets-and-errors](system.md#sys-secrets-and-errors) for what must stay out of any error.

## svc-api-retry-after

severity: should-fix  
concerns: reliability  
applies_when: A service answers 429 or 503 to HTTP callers.  
context: server  
tool gate: Integration test that forces a 429 and a 503 and asserts a `Retry-After` header.  
Backed by: IETF (unjudged), Zalando (unjudged), Microsoft (supports), Shopify (supports), Slack (supports). Backing: strong.

**Rule.** Send `Retry-After` on every 429 and 503, and set it no earlier than the time capacity returns.

**Why.** Without it, every client invents its own backoff, and a hundred of them retry in the same second. The header lets the server pace its own recovery.

**FAIL**

```text
HTTP/1.1 429 Too Many Requests

{"error": "slow down"}
```

**PASS**

```text
HTTP/1.1 429 Too Many Requests
Retry-After: 30
Content-Type: application/problem+json
```

**Counterpoint.** "Clients should use exponential backoff anyway." They should, and [svc-retry-policy](service.md#svc-retry-policy) says so. A server hint narrows the guess; it does not replace the client's cap. The IETF `RateLimit` header fields are still an Internet-Draft, so the card requires only `Retry-After`, which is in the HTTP standard. The quota itself is [svc-rate-limit-quota](service.md#svc-rate-limit-quota).

## svc-api-specific-status-codes

severity: should-fix  
concerns: compatibility  
applies_when: A service returns HTTP responses that callers or intermediaries interpret by status code.  
context: server  
tool gate: Integration tests asserting status and headers per operation; a spec linter for 201 and 405 responses.  
Backed by: IETF (unjudged), Zalando (unjudged), Microsoft (supports). Backing: mixed.

**Rule.** Return the most specific status code that fits: 201 with `Location` for a create, 405 with `Allow` for a wrong method, and a 4xx or 5xx for any failure.

**Why.** Clients, proxies and monitors act on the status line. A 200 with an error in the body hides failures from retries, caches and error-rate alerts. A create that returns 200 without `Location` forces the caller to guess the new URL.

**FAIL**

```text
POST /orders -> 200 {"error": "out of stock"}
PATCH /orders (route is read-only) -> 404, no Allow header
```

**PASS**

```text
POST /orders -> 201  Location: /orders/9031
POST /orders (out of stock) -> 409 application/problem+json
PATCH /orders (not supported) -> 405  Allow: GET, POST
```

**Counterpoint.** "A 200 with a status field is easier for our clients." It breaks every generic tool that reads the status line, including your own dashboards. Choosing between two fitting codes is a style call; the card fails only a code that says the wrong thing.

## svc-api-versioning-policy

severity: should-fix  
concerns: compatibility  
applies_when: A service offers an HTTP API to callers you do not deploy together with it.  
context: server  
tool gate: Spec diff in CI that fails on a breaking change inside a published version.  
Backed by: Zalando (unjudged), Microsoft (unjudged), Stripe (unjudged). Backing: unjudged.

**Rule.** Write down one versioning scheme for the API, and ship no breaking change inside a version it has published.

**Why.** Callers upgrade on their own schedule. With no stated scheme, each breaking change is a surprise, and each team invents its own v2.

**FAIL**

```text
GET /orders   # renamed total -> amount_total
no version marker anywhere; README says "we try not to break things"
```

**PASS**

```text
docs/api-versioning.md: dated api-version query parameter, previews last 6 months, 90 days' notice
GET /orders?api-version=2026-03-01 keeps returning "total"
the rename ships under api-version=2026-09-01
```

**Counterpoint.** "We will cross that bridge later." Later arrives with a customer on the old shape. The scheme can be minimal. A media type, a dated query parameter and a pinned header all work. Pick one and write it down. What counts as breaking is in [chg-breaking-change-taxonomy](change.md#chg-breaking-change-taxonomy).

## svc-async-content-reserves-space

severity: should-fix  
concerns: usability, performance  
applies_when: A page loads images, embeds, fonts, ads, or fetched content after the first paint.  
context: ui  
tool gate: Lighthouse CI assertion on `cumulative-layout-shift`.  
Backed by: Google (unjudged), Apple (unjudged), Nielsen Norman Group (unjudged), Mozilla (unjudged), WHATWG (unjudged), Shopify (supports), Cloudflare (supports). Backing: mixed.

**Rule.** Reserve the space for late-loading content with set dimensions or an aspect ratio, so nothing already on screen moves.

**Why.** A page that jumps while someone reads or taps makes them hit the wrong target. A cumulative layout shift of 0.1 or less is good, and over 0.25 is poor, measured on real users at the 75th percentile.

**FAIL**

```html
<img src="/hero.jpg">
<div id="promo"></div>   <!-- script inserts a banner above the article -->
```

**PASS**

```html
<img src="/hero.jpg" width="1200" height="630" style="max-width: 100%; height: auto">
<div id="promo" style="min-height: 90px"></div>
```

**Counterpoint.** "Ads vary in height." Reserve the common height, or the largest, and accept some blank space. A banner that pushes the article down is the worse trade.

## svc-auth-throttle-generic-errors

severity: block  
concerns: security  
applies_when: The service has a login, password-reset or one-time-code endpoint.  
context: server  
tool gate: Rate-limit middleware on auth routes; test that known and unknown users get identical responses.  
Backed by: OWASP (unjudged), NIST (unjudged), PortSwigger (unjudged), Microsoft (unjudged), Okta (Auth0) (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Limit failed attempts per account, and return the same message and status code whether or not the account exists.

**Why.** Unlimited guesses make passwords and 6-digit codes brute-forceable. Different errors for "no such user" and "wrong password" let an attacker list valid accounts first. Limit per account, since a per-IP limit is bypassed by rotating addresses. Response time leaks the same fact: if the code hashes the password only when the user exists, a fast reply means "no such user", so hash on every attempt. Registration needs its own design: give the same reply whether or not the address is taken, and email the owner of an existing account instead of creating a second one.

**FAIL**

```text
if not user: return "No such user", 404
if not check(pw): return "Wrong password", 401      # no attempt limit
```

**PASS**

```text
if too_many_failures(account_key): return "Try again later", 429   # checked before the password
ok = check(pw, user.pw_hash if user else DUMMY_HASH)              # hash runs either way
if not (user and ok): record_failure(account_key); return "Invalid credentials", 401
```

**Counterpoint.** "A lockout lets attackers lock out real users." Use a rising delay, not a permanent lock, and keep the recovery flow reachable. Log every lockout so abuse shows up.

## svc-authn-by-default

severity: should-fix  
concerns: security  
applies_when: The service has routes that need a signed-in user next to routes that are public.  
context: server  
tool gate: A framework fallback that requires authentication (ASP.NET Core `FallbackPolicy`, Django `LoginRequiredMiddleware`, Spring Security `anyRequest().authenticated()`); a test that calls every route without credentials and expects 401 or a login redirect unless the route is on the public list.  
Backed by: MITRE (unjudged), Microsoft (unjudged), Django Software Foundation (unjudged), Spring (unjudged). Backing: unjudged.

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

## svc-authz-central-deny-default

severity: block  
concerns: security  
applies_when: The service exposes routes or functions that different roles may call.  
context: server  
tool gate: Router that denies routes with no policy; a test that lists every route and its required role.  
Backed by: OWASP (unjudged), PortSwigger (unjudged), AWS (unjudged), NIST (unjudged). Backing: unjudged.

**Rule.** Route every request through one authorization layer that denies when no rule allows it.

**Why.** Per-handler checks drift: one admin route ships without its decorator and any user can call it. A central layer with deny as the fallback turns a forgotten check into a 403 instead of a hole.

**FAIL**

```text
@app.route("/admin/export")        # no role check; framework default is allow
def export(): ...
```

**PASS**

```text
policy = {"export": {"admin"}}             # endpoint -> roles, reviewed in one place
@app.before_request
def gate(): require_role(policy.get(request.endpoint))   # missing entry -> 403
```

**Counterpoint.** "A central policy is a bottleneck for feature teams." Keep the engine central and let each team own its rows. The cost of a one-line policy entry is small next to an unguarded admin route.

## svc-best-effort-optional-deps

severity: should-fix  
concerns: reliability, observability  
applies_when: The critical path of a request or a job calls a dependency whose data the product can do without, such as enrichment, recommendations, analytics, or a rate-limit control plane.  
Backed by: Netflix (unjudged), Uber (unjudged), Cabify (unjudged), Spotify (supports), Zalando (supports). Backing: mixed.

**Rule.** Give each call to a non-critical dependency a short budget and a default, so its failure degrades the result instead of failing the critical path, and count every fallback.

**Why.** An order page should not fail because the recommendations service is slow. Netflix makes enrichment best-effort, so a slow dependency can degrade its knowledge graph but never block it. Uber's rate-limit clients let traffic through when the control plane is down, because blocking would cause an outage of its own. Cabify drops non-critical details from a driver offer when it cannot collect them in time. It also puts metrics and alerts on every such fallback, because SLO dashboards built for critical flows miss them.

**FAIL**

```python
def trip_offer(trip_id):
    trip = trips.get(trip_id, timeout=0.5)
    eta = traffic.eta(trip.route, timeout=2.0)   # optional detail, but an error here fails the offer
    return Offer(trip, eta)
```

**PASS**

```python
def trip_offer(trip_id):
    trip = trips.get(trip_id, timeout=0.5)
    try:
        eta = traffic.eta(trip.route, timeout=0.1)
    except (TimeoutError, ConnectionError):
        eta = None                                # the offer goes out without the ETA
        degraded.labels(dep="traffic").inc()      # alert on this rate
    return Offer(trip, eta)
```

**Counterpoint.** "A silent default hides an outage." It does when nobody counts it, so the PASS needs the metric and an alert on it. Call a dependency non-critical only when the product works without its data. Authentication, payment, and authorization checks are critical, and they fail closed. Failing open on a rate limiter gives up protection to keep availability, so write that choice into the design. For the timeout itself, see [svc-timeouts](service.md#svc-timeouts). To check that the fallback really runs, see [prod-kill-switch-fallback](production.md#prod-kill-switch-fallback).

## svc-bound-client-controlled-sizes

severity: should-fix  
concerns: security  
applies_when: A request parameter or body sets how many records, bytes, items or operations the server handles.  
context: server  
tool gate: Gateway request-size limit; schema `maxLength`/`maxItems`; test with a 10 MB body and `limit=1000000`.  
Backed by: OWASP (unjudged), NIST (unjudged), Google (unjudged), Django Software Foundation (unjudged). Backing: unjudged.

**Rule.** Cap every client-controlled size and count on the server: body bytes, string length, array items, page size and batch size.

**Why.** A request for `limit=10000000` or a batch of 50,000 operations lets one client exhaust memory or the bill for a paid backend. The cap has to sit in the server, since a UI limit is not one. [svc-rate-limit-quota](service.md#svc-rate-limit-quota) covers request rate; this card covers size.

**FAIL**

```text
limit = int(request.args["limit"])
rows = db.fetch(limit)                              # no ceiling
items: list[Item]                                    # schema with no maxItems
```

**PASS**

```text
limit = max(1, min(int(request.args.get("limit", 50)), 100))
items: list[Item] = Field(max_length=100)            # body capped at 1 MB by the proxy
```

**Counterpoint.** "Legit clients sometimes need big batches." Offer a documented bulk or export endpoint with its own quota. The default path stays capped.

## svc-bounded-background-tasks

severity: block  
concerns: reliability, correctness  
applies_when: The code starts a task, goroutine, or thread per item, request, or message.  
Backed by: Google (unjudged), Python Software Foundation (unjudged), Tokio project (unjudged), Cabify (unjudged), AWS (unjudged). Backing: unjudged.

**Rule.** Cap how many background tasks run at once, and never spawn one per input with no limit.

**Why.** Input size is not under your control. One task per item works for ten items and exhausts memory, connections, or the downstream service at ten thousand, and the failure lands on everything else in the process. Go's `errgroup.SetLimit`, asyncio's `Semaphore` and Tokio's `Semaphore` exist for exactly this.

**FAIL**

```python
for msg in batch:                       # batch size comes from the queue
    asyncio.create_task(handle(msg))    # 50k messages -> 50k concurrent handlers
```

**PASS**

```python
async def worker(queue):
    while (msg := await queue.get()) is not None:
        await handle(msg)

queue = asyncio.Queue(maxsize=100)
async with asyncio.TaskGroup() as tg:
    for _ in range(32):                 # at most 32 handlers at once
        tg.create_task(worker(queue))
    for msg in batch:
        await queue.put(msg)
    for _ in range(32):
        await queue.put(None)           # one stop signal per worker
```

**Counterpoint.** "Tasks are cheap." Creating them is, but what each one holds (a socket, a buffer, a database connection) is not. A semaphore around each handler also caps concurrency, though it still creates one task object per input. This card covers work that a service starts for itself. [sys-load-shedding-bounded-queues](system.md#sys-load-shedding-bounded-queues) covers refusing incoming requests under load.

## svc-cache-key-completeness

severity: block  
concerns: security  
applies_when: A shared cache (CDN, reverse proxy, gateway, or framework cache) stores responses the service generates.  
context: server  
tool gate: A test that sends an unkeyed header or a GET body and asserts the response body does not change.  
Backed by: PortSwigger (unjudged), Cloudflare (unjudged), AWS (unjudged), Fastly (unjudged), Google (unjudged). Backing: unjudged.

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

**See also.** [svc-api-cache-control](service.md#svc-api-cache-control) owns `Cache-Control` and `Vary`; an input that changes the body must appear in the key or in `Vary`.

## svc-circuit-breaker-bulkhead

severity: should-fix  
concerns: reliability  
applies_when: A service calls several dependencies from shared pools, or retries a dependency that may be down.  
Backed by: Microsoft (unjudged), AWS (supports), Netflix (supports). Backing: mixed.

**Rule.** Give each critical dependency its own concurrency limit.

**Why.** One shared pool lets a slow dependency use every thread and starve healthy paths. Retrying a dead dependency only adds load, so also fail fast through a breaker with limited half-open probing where retries are demonstrably harmful.

**FAIL**

```text
pool = ThreadPool(50)               # used by billing, search, email alike
breaker = None                      # retries a dead host every request
```

**PASS**

```text
pools = {"billing": asyncio.Semaphore(10), "search": asyncio.Semaphore(20)}
# pseudocode: breaker logs and counts every state change; half-open allows 1 probe
```

**Counterpoint.** "More moving parts than a timeout." True. Start with the timeout and the per-dependency limit, and add the breaker where retries are demonstrably harmful. Retry and breaker have opposite aims, so do not present one as a substitute for the other.

## svc-cli-destructive-dry-run

severity: should-fix  
concerns: reliability, maintainability  
applies_when: A command-line tool has a command that deletes, overwrites or sends something.  
context: cli  
tool gate: CLI test that runs the command with the preview flag and checks nothing changed.  
Backed by: Kubernetes (unjudged), Git (unjudged), GNU Project (unjudged), GitHub (unjudged), Microsoft (unjudged), Google (unjudged), HashiCorp (unjudged), Cursor (unjudged). Backing: unjudged. People cited: Command Line Interface Guidelines (unjudged).

**Rule.** Give a destructive command a preview flag that changes nothing and a flag that skips the confirmation prompt.

**Why.** Without a preview, the first run is the real one. Without a bypass, a script cannot run the command at all, so people write wrappers that pipe "yes" into it.

**FAIL**

```go
func main() {
	fmt.Printf("Delete %d backups? [y/N] ", len(old))
	var ans string
	fmt.Scanln(&ans) // no preview flag, no way to skip the prompt
	if ans == "y" {
		for _, b := range old {
			os.Remove(b)
		}
	}
}
```

**PASS**

```go
dry := flag.Bool("dry-run", false, "list what would be deleted, delete nothing")
yes := flag.Bool("yes", false, "do not ask for confirmation")
flag.Parse()
for _, b := range old {
	fmt.Println(b)
}
if *dry {
	return
}
if !*yes && !confirm(fmt.Sprintf("Delete %d backups?", len(old))) {
	os.Exit(1)
}
for _, b := range old {
	if err := os.Remove(b); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}
```

**Counterpoint.** "A bypass flag invites accidents." The prompt stays the default for people, and the flag has to be typed on purpose. Pair it with [svc-cli-non-interactive](service.md#svc-cli-non-interactive).

## svc-cli-exit-codes-and-streams

severity: should-fix  
concerns: correctness, maintainability  
applies_when: The code ships a command-line tool that scripts or other programs may run.  
context: cli  
tool gate: CLI test that runs a failing command and checks the exit code and that stdout is empty.  
Backed by: Google (unjudged), GitHub (unjudged), AWS (unjudged), HashiCorp (unjudged), The Open Group (unjudged), Heroku (unjudged), Rust project (unjudged). Backing: unjudged. People cited: Command Line Interface Guidelines (unjudged).

**Rule.** Exit non-zero when a command fails, and write results to stdout and errors and progress to stderr.

**Why.** Scripts branch on the exit code and pipe stdout into the next program. A failure that exits 0 reads as success, and an error line on stdout lands in the next program's input. Add a `--json` flag for structured results, and keep prompts out of non-terminal runs (see [svc-cli-non-interactive](service.md#svc-cli-non-interactive)).

**FAIL**

```go
if err := run(); err != nil {
	fmt.Println("error:", err) // error goes into the pipe
}
// main returns: exit status 0
```

**PASS**

```go
if err := run(); err != nil {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}
```

**Counterpoint.** "Some tools use exit codes for non-error results." Documented codes for states such as "differences found" are fine. The rule is that a failure never exits 0.

## svc-cli-non-interactive

severity: should-fix  
concerns: maintainability, process  
applies_when: The code ships a command-line tool that scripts or agents may run.  
context: cli  
tool gate: CLI test that runs every command with stdin closed.  
Backed by: GitHub (unjudged), Google (unjudged), HashiCorp (unjudged), Microsoft (unjudged), Cursor (unjudged). Backing: unjudged. People cited: Command Line Interface Guidelines (unjudged).

**Rule.** Let the caller turn every prompt off with a flag or an environment variable, so the command never waits on a terminal.

**Why.** A script or an agent has no one to answer a prompt, so the command hangs until a timeout kills it. When stdin is not a terminal, the best behaviour is to fail at once with an error that names the missing flag and shows an example call, so the caller fixes it in one step.

**FAIL**

```go
env := flag.String("env", "", "target environment")
flag.Parse()
if *env == "" {
	fmt.Print("Choose environment: ")
	fmt.Scanln(env) // always prompts: no way to turn it off, hangs in CI
}
```

**PASS**

```go
env := flag.String("env", "", "target environment")
noInput := flag.Bool("no-input", false, "never prompt")
flag.Parse()
if *env == "" {
	if *noInput || !term.IsTerminal(int(os.Stdin.Fd())) { // golang.org/x/term
		fmt.Fprintln(os.Stderr, "error: --env is required. Example: deploy --env staging")
		os.Exit(2)
	}
	fmt.Fprint(os.Stderr, "Choose environment: ")
	fmt.Scanln(env)
}
```

**Counterpoint.** "Prompts are friendlier for people." Keep them. The rule only asks that the caller can switch prompts off.

## svc-cors-allowlist

severity: should-fix  
concerns: security  
applies_when: The service sends CORS headers and browsers send credentials or cookies to it, or the API is not meant to be public. A public bearer-key API with `*` and no credentials is outside it.  
context: server  
tool gate: Integration test that sends a hostile `Origin` and asserts it is not echoed.  
Backed by: OWASP (unjudged), Mozilla (unjudged), PortSwigger (unjudged), GitHub (unjudged). Backing: unjudged.

**Rule.** Allow cross-origin access only to a fixed list of named origins, and never echo the request `Origin` header back unchecked.

**Why.** Reflecting any Origin, or allowing `*` on an endpoint that returns private data, lets a hostile page read responses. CORS also does not stop CSRF, so it is no substitute for [svc-csrf-state-changing](service.md#svc-csrf-state-changing). A subdomain regex that matches `evil-example.com` is the same bug, and so is allowing the `null` origin.

**FAIL**

```text
resp.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
resp.headers["Access-Control-Allow-Credentials"] = "true"
```

**PASS**

```text
ALLOWED = {"https://app.example.com"}
if request.headers.get("Origin") in ALLOWED:
    resp.headers["Access-Control-Allow-Origin"] = request.headers["Origin"]
resp.headers["Vary"] = "Origin"                # caches keep one copy per origin
```

**Counterpoint.** "`*` is fine for a public API." It is, for endpoints that return only public data and take no credentials. Keep it off any endpoint behind a login.

## svc-csp-strict-script-src

severity: should-fix  
concerns: security  
applies_when: The service serves HTML pages to browsers.  
context: server  
tool gate: Google CSP Evaluator on the policy; a CI header check against a staging URL.  
Backed by: OWASP (unjudged), Mozilla (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Send a `Content-Security-Policy` whose `script-src` uses a per-response nonce or script hashes, with `object-src 'none'` and `base-uri 'none'`.

**Why.** When an XSS bug slips through, CSP decides whether the injected script runs. A host allowlist such as `script-src 'self' cdn.example` usually has a bypass, because some allowed host serves JSONP or an old library. A nonce or hash only lets through scripts the server marked. `'strict-dynamic'` lets those scripts load their own children. Browsers that support nonces ignore an `'unsafe-inline'` fallback placed next to one, so that fallback is safe. `'unsafe-inline'` on its own turns the policy off for inline script.

**FAIL**

```text
Content-Security-Policy: script-src 'self' 'unsafe-inline' https://cdn.example.com
```

**PASS**

```text
Content-Security-Policy: script-src 'nonce-r4nd0m' 'strict-dynamic'; object-src 'none'; base-uri 'none'
<script nonce="r4nd0m" src="/app.js"></script>
```

**Counterpoint.** "A strict CSP breaks inline handlers and third-party tags." It does at first, so roll it out with `Content-Security-Policy-Report-Only`, move `onclick=` attributes into script files, and switch to enforce when the reports go quiet. A policy that never leaves report-only protects nothing, so give that step a date.

## svc-csrf-state-changing

severity: block  
concerns: security  
applies_when: The service authenticates browsers with cookies and changes state on requests.  
context: server  
tool gate: Framework CSRF middleware enabled; test that a POST without the token returns 403.  
Backed by: OWASP (unjudged), Mozilla (unjudged), Django Software Foundation (unjudged), IETF (unjudged). Backing: unjudged.

**Rule.** Require a CSRF token (or an equivalent header check) on every cookie-authenticated request that changes state, and never change state on GET.

**Why.** The browser attaches cookies to a cross-site request, so a hostile page can post as the user. `SameSite` helps but `Lax` still sends cookies on cross-site top-level GET, so it supports the token and does not replace it. Naive double-submit cookies fail when a sibling subdomain can set cookies.

**FAIL**

```text
@app.get("/account/delete")                    # state change on GET
@app.post("/transfer")                         # cookie auth, no token check
```

**PASS**

```text
@app.post("/transfer")
@csrf_protect                                  # token bound to the session
Set-Cookie: sid=...; SameSite=Lax; Secure; HttpOnly
```

**Counterpoint.** "Our API uses JSON, so browsers cannot forge it." A simple content type such as `text/plain` can carry a JSON body without a preflight. Reject it, or require a custom header such as `X-CSRF-Token`. Pure bearer-token APIs with no cookies are exempt.

## svc-decompression-cap

severity: should-fix  
concerns: security, performance  
applies_when: The code decompresses or decodes input whose size it does not control.  
context: server  
tool gate: Apache `DeflateInflateLimitRequestBody`; ASP.NET Core `MaxRequestBodySize`; a test that inflates a 1 MB gzip to about 1 GB and asserts the decoder stops at the cap.  
Backed by: OpenJS Foundation (unjudged), Microsoft (unjudged), Apache Software Foundation (unjudged), Python Software Foundation (unjudged). Backing: unjudged.

**Rule.** Cap the decompressed output of every decoder, and set the cap on the output rather than the compressed input.

**Why.** A small gzip can expand a thousand-fold: DEFLATE tops out near 1030:1, so a 1 MB gzip can inflate to about 1 GB, and nested archives or other codecs can go further. A body limit on the compressed bytes does not bound that expansion, so the decoder needs its own ceiling. `Content-Length` counts the compressed stream, not the inflated body, and Apache's inflated-body directive is unset by default. In Node, the convenience methods take `maxOutputLength`, whose default is `buffer.kMaxLength`, so pass a real number. The zip entry iterator is a separate case: `zipEntry.contentIterator()` has no default `maxSize` and is not covered by the zip-wide ceiling, so pass `maxSize` on that call. Python's tar filters address paths and links, and its docs say they do not prevent every unsafe archive, so size still needs its own bound. See also [svc-bound-client-controlled-sizes](service.md#svc-bound-client-controlled-sizes) for the request-body cap and [svc-upload-validate-store](service.md#svc-upload-validate-store) for archives in uploads.

**FAIL**

```javascript
const body = zlib.gunzipSync(req.body); // no maxOutputLength
parse(body);
```

**PASS**

```javascript
const body = zlib.gunzipSync(req.body, { maxOutputLength: 1 << 20 });
parse(body);
```

**Counterpoint.** "The proxy already caps the request body." It caps the compressed bytes, which is the wrong number. A 1 MB gzip can still inflate to about 1 GB, and `Content-Length` says nothing about the decompressed size. Set the inflated cap at the decoder and keep the body cap. Where the platform offers a decompression limit, check that it is on: Apache's directive falls back to the post-deflation `LimitRequestBody`, and a value of `0` removes the inflated-body limit.

## svc-dlq

severity: should-fix  
concerns: reliability  
applies_when: The code consumes from a queue or stream.  
context: server  
tool gate: A config check that every consumed queue has a dead-letter target (for SQS in Terraform, a `redrive_policy` with `maxReceiveCount`), and an alarm on dead-letter queue depth.  
Backed by: AWS (unjudged), Netflix (unjudged), Notion (supports), Uber (supports), Microsoft (unjudged), Google (unjudged). Backing: mixed.

**Rule.** Give every consumer queue a dead-letter queue and keep a way to replay it after the fix. On an ordered queue, key the group or session to the unit that must stay ordered, so a poison message holds only its own unit.

**Why.** A poison message otherwise loops forever, uses the consumers' capacity and hides the real backlog. On an ordered queue it also holds the messages behind it: in a FIFO queue no further messages from the same group are returned until the stuck message is deleted or becomes visible again, and an unacknowledged ordering key can delay the others. Give each independent stream its own group, session or queue, so one failure stays contained. Then cap the retries, so that a failing message moves to the dead-letter queue after a few attempts. Alarm on any message in the dead-letter queue, because each one is a bug to fix. Replay has a cost on these queues: a message put back after a dead-letter loses its place in the order, so replay only where order no longer matters, or reorder downstream.

**FAIL**

```hcl
resource "aws_sqs_queue" "orders" {
  name       = "orders.fifo"
  fifo_queue = true
  # no redrive_policy: a message that always fails is retried forever
  # and holds its whole message group
}
```

```python
# every producer uses one group, so one stuck message blocks all orders
sqs.send_message(QueueUrl=url, MessageBody=body, MessageGroupId="orders")
```

**PASS**

```hcl
resource "aws_sqs_queue" "orders_dlq" {
  name       = "orders-dlq.fifo"
  fifo_queue = true
}

resource "aws_sqs_queue" "orders" {
  name       = "orders.fifo"
  fifo_queue = true
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.orders_dlq.arn
    maxReceiveCount     = 5
  })
}
# replay after the fix: aws sqs start-message-move-task --source-arn <orders-dlq ARN>
```

```python
# one group per order, so one stuck order does not block the others
sqs.send_message(QueueUrl=url, MessageBody=body, MessageGroupId=order_id)
```

**Counterpoint.** "A dead-letter queue already stops the poison message." It stops it after the retry cap. Until then the redelivery holds its group, and in a FIFO queue that means every message behind it. Grouping and the dead-letter queue do different jobs, so keep both. Choose the group key from the unit that must stay ordered. A single group restores the head-of-line block you were trying to remove. On a standard queue with no ordering, there is no group to key and the second sentence of the Rule does not apply.

## svc-export-scope

severity: block  
concerns: security  
applies_when: An endpoint or job produces a file, archive or stream of many records.  
context: data  
tool gate: A test that exports as a second tenant and asserts the other tenant's rows are absent.  
Backed by: OWASP (unjudged), Atlassian (unjudged), Microsoft (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Scope an export to what the requesting principal may read.

**Why.** An export is a read that returns many rows at once. The per-object check on the detail page never runs, so a `SELECT *` with no tenant or access predicate hands the caller the table. Apply the same filter the list endpoint uses, including any role or ownership predicate and not only the tenant, and apply it inside the export query rather than on rows already fetched. OWASP's examples put the tenant scope in the query itself. Test it with two tenants. A restore asks the same question in reverse: a shared backup holds several tenants and old memberships, so restore one tenant into a separate resource and re-apply current access and retention before anyone can read it. A recovered environment also needs the production controls, not the ones it had when the backup was taken.

**FAIL**

```text
GET /export  ->  SELECT * FROM orders; streamed to any authenticated caller
```

**PASS**

```python
def export(user):
    rows = session.query(Order).filter(Order.tenant_id == user.tenant_id)
    return csv_stream(rows)
```

**Counterpoint.** "Some exports deliberately include everything." Some products ship an admin XML export that includes pages the exporter cannot view. That path is an administrative backup, so gate it on an admin permission and audit it. The user-facing exports in the same products contain only what the exporter can view, which is the rule here. Check which export path the change touches before calling a missing filter a bug.

## svc-fail-closed-defaults

severity: should-fix  
concerns: security  
applies_when: The service reads configuration for authentication, an allow-list, a safety check, or a signing secret.  
context: server  
tool gate: A startup check that raises on a missing or placeholder secret (Django refuses an unset `SECRET_KEY`; Pydantic Settings fields without a default); a test that boots the service with an empty environment and expects a failed start or denied requests.  
Backed by: OWASP (unjudged), Microsoft (unjudged), Google (unjudged), Django Software Foundation (unjudged), MITRE (unjudged), AWS (unjudged), CISA (unjudged), NIST (unjudged). Backing: unjudged.

**Rule.** Ship every security control switched on, with an empty allow-list denying everything.

**Why.** A control that is off until configured is off in the deployment where nobody read the setup page. An empty allow-list that means "allow all" and a built-in `changeme` key both boot cleanly, so nothing alerts anyone while the service runs open or signs tokens anyone can forge. Refuse to start when a secret is missing or still a placeholder: failing at startup moves the discovery from an incident to the first deploy.

**FAIL**

```python
import os

AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "false") == "true"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")  # "" means no filtering below
SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")

def host_ok(host):
    return not ALLOWED_HOSTS[0] or host in ALLOWED_HOSTS
```

**PASS**

```python
import os

AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "true") == "true"
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h]
SECRET_KEY = os.environ["SECRET_KEY"]          # KeyError stops the boot
if SECRET_KEY in {"", "changeme"}:
    raise RuntimeError("SECRET_KEY is a placeholder")

def host_ok(host):
    return host in ALLOWED_HOSTS               # empty list denies all
```

**Counterpoint.** "Developers need to run it locally without setup." Give them a separate dev entry point or a dev-only flag that is named for what it does (`INSECURE_DEV_MODE=1`) and that production images never set. The default stays closed, and the open mode is a visible, greppable choice.

## svc-host-header-trust

severity: block  
concerns: security  
applies_when: The service builds an absolute URL from the request, or reads `Host` or `X-Forwarded-*` to decide what to serve or where to send a user.  
context: server  
tool gate: Framework host allowlist configured (`ALLOWED_HOSTS`, `AllowedHosts`, `config.hosts`, `trustHosts`), and a test that sends a hostile `Host` and expects 400.  
Backed by: PortSwigger (unjudged), Fastly (unjudged), Django Software Foundation (unjudged), Microsoft (unjudged), Ruby on Rails (unjudged), Laravel (unjudged), IETF (unjudged). Backing: unjudged.

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

## svc-idempotency-key

severity: block  
concerns: reliability, correctness  
applies_when: A non-idempotent operation (charge, create, send) can be retried by a client, a queue, or a saga.  
context: server  
Backed by: Microsoft (unjudged), IETF (unjudged), Stripe (unjudged). Backing: unjudged.

**Rule.** Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.

**Why.** A timeout does not say whether the first attempt ran. Retrying without a key charges twice or sends two emails. A common way to answer the retry is to store the first result and return it again.

**FAIL**

```text
POST /payments {amount: 10}          # retried on timeout
INSERT INTO payment(amount) VALUES (10)
```

**PASS**

```text
POST /payments  Idempotency-Key: k-123
INSERT ... ON CONFLICT (idem_key) DO UPDATE SET idem_key = EXCLUDED.idem_key RETURNING *
```

**See also.** [sys-lock-fencing](system.md#sys-lock-fencing) shares the goal but uses a different mechanism (stale lock holders).

**Counterpoint.** "Our retries are rare." Queues redeliver and sagas retry by design, so rare is not never. The cost is a unique key and a stored result. No standard fixes how long the server keeps a key. Pick a window and publish it.

## svc-invalid-input-is-4xx

severity: should-fix  
concerns: correctness, reliability  
applies_when: A handler takes a number, an id, a header or a body field from the caller and uses it in a query, a calculation or an encoder.  
context: server  
tool gate: Schema or model constraints on every field (minimum, maximum, enum, format); a test that posts a negative number, an unknown id and a non-ASCII header and expects a 4xx.  
Backed by: OWASP (unjudged), Google (unjudged), Kubernetes (unjudged), IETF (unjudged), Microsoft (unjudged), Stripe (unjudged). Backing: unjudged.

**Rule.** Check each caller-supplied value against its allowed domain (range, allowed set, an id that must exist, an encoding the code can handle) at the boundary, and answer a failed check with a 4xx, never a 5xx.

**Why.** A negative quota, a limit of zero, an id with no row, or a header with a non-ASCII character is the caller's error. If it reaches the database or an `.encode("ascii")`, the user gets a 500: the caller retries, the error-rate alert fires, and a negative quota may be stored and later allow unlimited use. A schema constraint or an explicit lookup costs one line per field. [svc-bound-client-controlled-sizes](service.md#svc-bound-client-controlled-sizes) caps size and count; this card covers every other value.

**FAIL**

```python
@app.post("/quotas")
def set_quota(body: dict):
    db.execute("UPDATE plans SET quota=%s WHERE id=%s", (body["quota"], body["plan_id"]))
    # quota=-5 is stored; a plan_id with no row updates nothing and answers 200
    return {"ok": True}

def sign(request):
    return hmac_header(request.headers["X-Name"].encode("ascii"))   # "Zoë" -> UnicodeEncodeError -> 500
```

**PASS**

```python
class SetQuota(BaseModel):
    quota: int = Field(ge=0, le=10_000)
    plan_id: int

@app.post("/quotas")
def set_quota(body: SetQuota):
    if not db.exists("SELECT 1 FROM plans WHERE id=%s", (body.plan_id,)):
        raise HTTPException(404, "unknown plan_id")
    db.execute("UPDATE plans SET quota=%s WHERE id=%s", (body.quota, body.plan_id))

def sign(request):
    try:
        name = request.headers["X-Name"].encode("ascii")
    except UnicodeEncodeError:
        raise HTTPException(400, "X-Name must be ASCII")
    return hmac_header(name)
```

**Counterpoint.** "The database has a CHECK and a foreign key, so the data is safe." It is, but the constraint violation surfaces as a 500 unless the code maps it. Keep the constraint as the last line and validate first, so the caller gets a message that names the field. Catching the database error and mapping it to a 4xx also meets this card when a pre-check would race.

## svc-list-endpoint-paginates

severity: should-fix  
concerns: performance  
applies_when: The service exposes an endpoint or RPC that returns a collection.  
context: server  
tool gate: Contract test that calls the list with a huge page size and asserts the clamp or a 400.  
Backed by: Google (unjudged), Microsoft (unjudged), Zalando (unjudged), GitHub (unjudged), Stripe (unjudged). Backing: unjudged.

**Rule.** Paginate every list endpoint, with a default page size and a server-side maximum.

**Why.** A list that returns everything grows with the data until one request exhausts memory or the timeout. Adding pagination later breaks clients, so start with it. Without a maximum, a caller can ask for a page as big as the table.

**FAIL**

```text
GET /orders          -> every order the user ever placed
GET /orders?limit=1000000   (server honours it)
```

**PASS**

```text
GET /orders?page_size=50&page_token=abc   (default 25, values above 100 clamped to 100)
response: { "items": [...], "next_page_token": "def" }
```

**Counterpoint.** "This list is always small." Say so with a bounded type or a documented limit, since data tends to outgrow its first estimate. Cursors cost more than offsets to build, but they stay stable while rows change.

## svc-mfa-step-up

severity: should-fix  
concerns: security  
applies_when: The service offers multi-factor authentication, or lets a signed-in user change a password, email address, or authentication factor.  
context: server  
Backed by: OWASP (unjudged), NIST (unjudged), Microsoft (unjudged), Okta (Auth0) (unjudged). Backing: unjudged.

**Rule.** Require a fresh authentication with an already-bound factor before sensitive actions and before adding, replacing or removing an MFA factor; an existing session alone is not enough.

**Why.** A session that passed a password check says nothing about who holds it now. Let that session enrol a new phone or replace an authenticator and an attacker with a stolen cookie keeps the account after the password is changed. The same gap covers password, email and admin-role changes. Step-up at the action asks for the factor only when it matters, and a short freshness window keeps the prompt rare. A session must not be treated as stronger than the authentication that created it. A user who lost the only factor needs a documented recovery path, such as single-use recovery codes or a temporary access pass. That path is part of the control, and it is judged as a separate recovery flow.

**FAIL**

```text
@login_required
def add_phone():
    user.phone = request.form["phone"]      # any old session can replace the second factor
```

**PASS**

```text
@login_required
@recent_auth(max_age=300, factor="existing")
def add_phone():
    user.phone = request.form["phone"]
    notify(user, "phone changed")
```

**Counterpoint.** "Prompting on every sensitive action annoys users, and a user who lost the only factor gets locked out." Use risk and a recent-auth window so the prompt appears only when the session is stale or the action is high risk, and keep the recovery path described above; without it, step-up becomes a denial of service against the account's owner.

**See also.** [svc-auth-throttle-generic-errors](service.md#svc-auth-throttle-generic-errors) covers guessing the factor; [svc-session-lifecycle](service.md#svc-session-lifecycle) covers the session that carries the result.

## svc-no-redundant-entry

severity: should-fix  
concerns: usability, accessibility  
applies_when: A multi-step flow, such as checkout or signup, asks for data in more than one step.  
context: ui  
tool gate: none; a walk through the flow that lists each field asked twice.  
Backed by: W3C (unjudged), Nielsen Norman Group (unjudged), GOV.UK (unjudged), Baymard Institute (unjudged). Backing: unjudged. People cited: Ben Shneiderman (unjudged).

**Rule.** Do not ask for information the user already gave in the same flow. Fill it in, or let the user pick it.

**Why.** Typing the same address twice costs time and adds typos. People recognise what they gave more easily than they recall it, so show it and let them confirm it.

**FAIL**

```html
<!-- step 1 -->  <input name="ship_address">
<!-- step 2 -->  <input name="billing_address">   <!-- empty again -->
```

**PASS**

```html
<!-- step 2 -->
<label><input type="checkbox" name="same" checked> Billing address is the same as shipping</label>
<input name="billing_address" value="12 Elm Road, Leeds" hidden>   <!-- hidden while the box is checked; shown, pre-filled, when it is unchecked -->
```

**Counterpoint.** "Retyping a new password confirms it." That is a fair exception. So is data that is no longer valid, and re-entry that is the point of the task, such as a memory test. Browser autofill does not count: the page itself must supply the value.

## svc-no-secrets-in-url

severity: should-fix  
concerns: security  
applies_when: A client or server puts an API key, session token, bearer token, password, or personal data into a URL.  
context: server  
Backed by: OWASP (unjudged), IETF (unjudged), MITRE (unjudged), Mozilla (unjudged). Backing: unjudged.

**Rule.** Send tokens, keys, passwords, and personal data in a header or the request body, never in the path or query string.

**Why.** A URL is copied to places nobody reviews: proxy and access logs, browser history, the `Referer` header sent to third-party scripts and images, and links pasted into chat. A token there stays readable long after the request ends. The `Authorization` header and a POST body skip all of those copies.

**FAIL**

```text
GET /api/orders?api_key=sk_live_abc123
GET /reset?email=ana@example.com&token=9f2c
```

**PASS**

```text
GET /api/orders
Authorization: Bearer sk_live_abc123

POST /reset
Content-Type: application/json

{"token": "9f2c"}
```

**Counterpoint.** "Email links have to carry the token in the URL." Make that token single-use and short-lived, have the landing page swap it for a session at once, and send `Referrer-Policy: no-referrer` on that page. A long-lived API key has no such excuse.

## svc-oauth-code-flow-binding

severity: block  
concerns: security  
applies_when: The service acts as an OAuth 2.0 or OpenID Connect client and exchanges an authorization code for tokens.  
context: server  
Backed by: IETF (unjudged), OWASP (unjudged), OpenID Foundation (unjudged), Microsoft (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Finish the authorization-code flow with PKCE and a challenge method that keeps the verifier out of the authorization request (`S256`), send the exact registered `redirect_uri` (a native app on the loopback interface may vary the port), and reject the response unless this transaction's `state` or OIDC `nonce` matches and the ID token's signature, `iss`, `aud` and `exp` check out.

**Why.** A code that is not bound to the browser in front of you can be injected into another session, and an ID token minted for a different client or issuer can be replayed at your login. PKCE makes an intercepted code useless without the verifier, and `S256` is the method that does not reveal the verifier in the request. An exact redirect URI stops the code reaching an attacker's host. `state` or `nonce` ties the response to the login the user started. The ID-token checks reject a token that another app, another issuer or an expired clock made.

**FAIL**

```text
code = request.args["code"]
token = exchange(code, redirect_uri=request.args["redirect_uri"])
session["user"] = jwt.decode(token["id_token"], options={"verify_signature": False})["sub"]
# no PKCE, no state check, no ID-token validation, and the redirect_uri is taken from the request
```

**PASS**

```python
# the authorization request carried code_challenge=...&code_challenge_method=S256
if not secrets.compare_digest(request.args["state"], session.pop("oauth_state")):
    raise PermissionDenied
token = exchange(request.args["code"], redirect_uri=REDIRECT_URI,   # constant from config
                 code_verifier=session.pop("code_verifier"))
claims = verify_jwt(token["id_token"], jwks, iss=ISSUER, aud=CLIENT_ID,
                    nonce=session.pop("oauth_nonce"))
```

**Counterpoint.** "The OAuth client library already handles this." It handles the protocol, not your configuration. Some libraries decode the ID token unless you pass the issuer, audience and nonce, and the state or nonce store belongs to your session code. Test with a token minted for another client and a response with no state. The loopback exception is narrow: the port may differ, the host and path may not. The card is stricter than RFC 9700, which recommends PKCE for confidential clients and lets a confidential OIDC client use `nonce` instead; a reviewer may accept that alternative when the authorization server is known to bind the code another way.

**See also.** [fn-redirect-target-allowlist](function.md#fn-redirect-target-allowlist) covers redirect targets taken from a request; [svc-csrf-state-changing](service.md#svc-csrf-state-changing) covers the CSRF check on your own forms.

## svc-password-reset

severity: block  
concerns: security  
applies_when: The service emails or texts a password-reset link or code.  
context: server  
Backed by: OWASP (unjudged), NIST (unjudged), Okta (Auth0) (unjudged), Microsoft (unjudged), Django Software Foundation (unjudged). Backing: unjudged.

**Rule.** Make the reset token single-use and short-lived, and on success revoke every session.

**Why.** A reset link is a bearer password that arrives in a mailbox. If it works twice, a forwarded mail, a mail scanner or a backup keeps the access alive. If it lives for days, an attacker has days to use it. And a reset that leaves the old sessions open changes the password without evicting the intruder who already had a session. Two further habits cost little: store only a hash of the token, so a database read or a backup hands over no working links, and revoke the other outstanding reset links on success.

**FAIL**

```text
token = f"{user.id}-{int(time.time())}"
user.reset_token = token             # predictable, stored in clear, usable again
send_email(link(token))
```

**PASS**

```python
raw = secrets.token_urlsafe(32)
db.store(sha256(raw), user=user, expires=now + 15 * MINUTE)
# the raw value exists only in the mail
consume_once(raw)
revoke_sessions(user)
revoke_other_resets(user)
```

**Counterpoint.** "The token is random, so hashing it adds nothing." The mail, the link and every log between you and the user still carry the raw value; the hash protects the copy at rest, which is the copy an attacker reads. OWASP treats session invalidation as the user's choice in the normal flow and requires it after suspected compromise; this card asks for it every time because the reset may be the owner's answer to a stolen session. Pick the lifetime from a number the support flow can meet, not from the word "short", and send a notification after the reset so a change the owner did not make is visible.

**See also.** [svc-auth-throttle-generic-errors](service.md#svc-auth-throttle-generic-errors) owns the identical reply and the rate limit on the request; [fn-csprng-for-secrets](function.md#fn-csprng-for-secrets) owns the token source, and [fn-password-slow-hash](function.md#fn-password-slow-hash) owns the new password.

## svc-rate-limit-quota

severity: should-fix  
concerns: security, reliability  
applies_when: A shared API or queue serves several tenants or callers.  
context: server  
Backed by: AWS (unjudged), Google (unjudged), Microsoft (unjudged), NIST (unjudged), GitHub (unjudged), Shopify (unjudged). Backing: unjudged.

**Rule.** Enforce a per-tenant quota on shared APIs and queues.

**Why.** Without a quota, one noisy tenant consumes shared capacity for everyone. Key the count to the identity that owns the quota, such as the tenant, account or API key, and state the window and when capacity returns. Also add a per-tenant concurrency cap, and return 429 for over-quota but 503 for the service's own lack of capacity, so clients do not retry quota errors as capacity problems.

**FAIL**

```text
every tenant shares one worker pool and one request budget
no per-tenant limit: one tenant's batch job starves the rest
```

**PASS**

```text
limiter.check(tenant_id) -> 429 + Retry-After
per-tenant semaphore on workers
```

**Counterpoint.** "One global rate limit is simpler." A global limit protects the service, but one tenant can use all of it, and then every other tenant gets errors. A per-tenant limit costs one key per tenant in the limiter. Some older services return 503 for quota errors, so the status code is a convention. What matters is that a client can tell a quota error from a capacity error. Shuffle sharding (per-tenant worker subsets) isolates tenants further, and this card does not require it.

## svc-reflow-and-zoom

severity: should-fix  
concerns: accessibility, usability  
applies_when: A page or app is served to browsers on screens of any size.  
context: ui  
tool gate: axe `meta-viewport`; a rendered check at a 320 px viewport and at 200% text zoom.  
Backed by: W3C (unjudged), Deque (unjudged), The A11y Project (unjudged), WebAIM (unjudged), Mozilla (unjudged), Google (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Make the page usable at 320 CSS pixels wide and at 200% text zoom, with no sideways scrolling, no clipped content, and no blocked pinch-zoom.

**Why.** Low-vision users enlarge the page instead of using a small screen. A fixed width or a clipped container hides content from exactly those users. `user-scalable=no` takes away their only tool.

**FAIL**

```html
<meta name="viewport" content="width=device-width, user-scalable=no, maximum-scale=1">
```

```css
.layout { width: 960px; }
.card   { height: 120px; overflow: hidden; }
```

**PASS**

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

```css
.layout { max-width: 60rem; padding-inline: 1rem; }
.card   { min-height: 7.5rem; }
.table-wrap { overflow-x: auto; }   /* a data table scrolls in its own box */
```

**Counterpoint.** "Maps and data tables need two-way scrolling." They are exempt, but only the part that needs it. Wrap the table in its own scroll box, and keep the headings and controls around it reflowing.

## svc-request-framing

severity: block  
concerns: security  
applies_when: The service parses HTTP requests itself, or receives them through a proxy, load balancer, or CDN.  
context: server  
tool gate: A test that sends one request with both Content-Length and Transfer-Encoding and expects 400 or a closed connection.  
Backed by: IETF (unjudged), PortSwigger (unjudged), Microsoft (unjudged), Fastly (unjudged), Envoy (unjudged), Cloudflare (unjudged), OpenJS Foundation (unjudged). Backing: unjudged.

**Rule.** Reject a request that carries both `Transfer-Encoding` and `Content-Length`, or remove one field at the first hop, and parse header framing strictly rather than with a leniency flag.

**Why.** Two hops can disagree about where a request ends. The front end reads one body length and the back end reads another, so the leftover bytes become the start of the next request on the same connection. That request skips the front end's checks: it can reach an admin route, poison a cache, or splice one user's response into another user's connection. The ambiguity comes from a second framing field, a malformed header name, or a parser that accepts what the specification rejects. A front end that downgrades HTTP/2 to HTTP/1.1 reopens the gap, so validate the rewritten request as well.

**FAIL**

```text
POST /login HTTP/1.1
Host: app.example
Content-Length: 15
Transfer-Encoding: chunked

0

GET /admin
```

The proxy forwards this over a reused upstream connection. The front end reads fifteen bytes as the body. The back end finds the end of the chunked body and keeps `GET /admin` for the next request on the connection, so it reaches a route the front end never checked.

**PASS**

```text
# front end
if both framing fields are present:
    return 400 and close the connection      # or drop Content-Length, forward, then close

# parser
insecureHTTPParser: false                    # Node
allow_chunked_length: false                  # Envoy
whitespace before a header colon: 400
```

**Counterpoint.** "We speak HTTP/2 end to end, so there is nothing to smuggle." HTTP/2 has one framing mechanism, but many deployments still downgrade at the last hop, and compatibility flags keep the old leniency in parsers. Check both ends of every connection and the rewrite between them, not the version the client negotiated.

## svc-retry-policy

severity: block  
concerns: reliability  
applies_when: The code retries a failed call, or wraps a client that retries.  
Backed by: Microsoft (unjudged), AWS (unjudged), Google (unjudged), Stripe (unjudged), GitHub (unjudged). Backing: unjudged.

**Rule.** Retry only transient errors, with capped attempts and jittered exponential backoff.

**Why.** Immediate, unbounded, or synchronized retries turn a brief fault into a load spike on the struggling dependency. Retry at one layer only: three layers of three attempts is nine calls per user request. Make retried writes safe with [svc-idempotency-key](service.md#svc-idempotency-key).

**FAIL**

```text
while True:
    try: return client.call()
    except Exception: sleep(1)        # no cap, no jitter, retries 4xx too
```

**PASS**

```python
import random, time
for i in range(3):
    try:
        return client.call()
    except TransientError:
        if i == 2:
            raise
        time.sleep(random.uniform(0, min(CAP_S, BASE_S * 2**i)))
# retry at one layer only: the client's own retries are off
```

**Counterpoint.** "Retries make us more reliable." Only for transient faults and only within a budget. Past that they hurt, so a non-transient error should fail at once. A retry budget (retries capped as a share of traffic) helps further. This card leaves its size to the team.

## svc-saga-steps

severity: should-fix  
concerns: reliability, correctness  
applies_when: A business operation spans services, each with its own database, coordinated as a saga.  
context: server  
Backed by: Microsoft (unjudged), AWS (supports), Temporal (supports). Backing: mixed.

**Rule.** Make steps after the pivot idempotent and retryable, and make every compensation idempotent with a failure path.

**Why.** After the pivot there is no undo, only retry until done. A compensation can itself fail, and unhandled it leaves the system inconsistent with nobody told.

**FAIL**

```text
step 4 (after pivot): charge_card(order)     # retried -> double charge
compensate: release_stock(order)             # throws; exception swallowed
```

**PASS**

```text
step 4: charge_card(order, idempotency_key=order.id)   # safe to retry
compensate: release_stock(order) retried; on exhaustion -> alert + manual queue
```

**Counterpoint.** "Use a distributed transaction." Often unavailable across services. A saga has no isolation, so also guard against reading half-done data (semantic locks, re-reading values before acting). [svc-idempotency-key](service.md#svc-idempotency-key) covers keys, and [svc-dlq](service.md#svc-dlq) covers failed messages.

## svc-saml-assertion-binding

severity: block  
concerns: security  
applies_when: The service is a SAML 2.0 service provider and accepts a response or assertion at an assertion consumer service endpoint.  
context: server  
Backed by: OASIS (unjudged), OWASP (unjudged), NIST (unjudged), Microsoft (unjudged), SAML-Toolkits project (unjudged). Backing: unjudged.

**Rule.** Verify the XML signature over the assertion you read, with the IdP's configured key rather than a key carried in the response, then require the assertion's `Audience` and its bearer `SubjectConfirmationData` `Recipient` to name this SP, the response `Destination` to be this endpoint, `InResponseTo` to match your request (absent for an IdP-initiated response), `NotOnOrAfter` to be current, and the assertion ID to be unseen. These are one step, verify the assertion, and each check is cited.

**Why.** A valid signature elsewhere in the document proves nothing about the `<NameID>` your code just read. That gap is the signature-wrapping attack, and it lets an attacker choose which identity your service trusts. A lookup such as `.//NameID` is how the signed element and the read element get separated. Pinning the key to the IdP stops the document choosing its own verification key. The audience and destination checks stop an assertion minted for another SP from being posted here. `InResponseTo` catches a response injected into a browser that never started the request, and the time window plus the used-ID set stop a captured assertion from being replayed.

**FAIL**

```text
doc = etree.fromstring(base64.b64decode(form["SAMLResponse"]))
name_id = doc.find(".//NameID").text
login(name_id)      # no signature check, no audience, no replay set
```

**PASS**

```python
signed = verify_signature(response, key=IDP_CERT)     # returns the signed element
assertion = signed.assertion
if assertion.audience != SP_ENTITY_ID or response.destination != ACS_URL:
    raise InvalidAssertion
if assertion.subject_confirmation.recipient != ACS_URL:
    raise InvalidAssertion
if assertion.subject_confirmation.in_response_to != request_id:
    raise InvalidAssertion
if assertion.not_on_or_after <= now() or used_ids.seen(assertion.id, until=assertion.not_on_or_after):
    raise InvalidAssertion
```

**Counterpoint.** "The library validates the signature, so the assertion is trustworthy." The signature vouches for the bytes it covers, not for the element your handler reads. A strict mode that validates the response but leaves an unsigned assertion in the tree still passes a wrapped `NameID`. Require the assertion to be inside the signed content, take the key from IdP metadata, and record the ID of the assertion you accepted, not the ID of its wrapper.

**See also.** [fn-xml-no-external-entities](function.md#fn-xml-no-external-entities) covers the parser; [svc-session-lifecycle](service.md#svc-session-lifecycle) starts where this card ends.

## svc-session-lifecycle

severity: block  
concerns: security  
applies_when: The service sets a session cookie or session ID after login.  
context: server  
tool gate: Header test on the login response; session fixation test in the end-to-end suite.  
Backed by: OWASP (unjudged), Mozilla (unjudged), NIST (unjudged), Spring (unjudged), Ruby on Rails (unjudged). Backing: unjudged.

**Rule.** Issue a new session ID at login, and set `Secure`, `HttpOnly` and `SameSite` on the session cookie.

**Why.** A session ID that survives login can be planted by an attacker beforehand (fixation). A cookie without `HttpOnly` is readable by any injected script, and one without `Secure` travels over plain HTTP. Also end the session on the server at logout, because clearing only the browser cookie leaves a stolen copy valid, and enforce idle and absolute timeouts on the server. Scope the cookie to one host. With `Domain` omitted it is returned only to the host that set it, while a `Domain` set to the registrable domain sends it to every subdomain. Omitting `Domain` does not stop planting: a sibling subdomain that serves user content can still set a parent-domain cookie with the same name for the parent to accept. The `__Host-` prefix is what stops that, because the browser refuses a `__Host-` cookie that carries `Domain` or a path other than `/`. Use it on the session cookie.

**FAIL**

```text
Set-Cookie: sid=abc123
login():  keep the pre-login session id
```

**PASS**

```text
Set-Cookie: __Host-sid=<new random>; Secure; HttpOnly; SameSite=Lax; Path=/   # the __Host- name is optional hardening, not a Rule clause
login():  session.regenerate()
```

**Counterpoint.** "The framework already does this." Some do: Spring Security changes the session ID at login by default, and Rails gives you `reset_session`. Hand-written login code and custom session stores often skip it, and cookie flags depend on configuration. Check the login handler and the real `Set-Cookie` header, not the framework's reputation.

## svc-slow-operation-shows-progress

severity: should-fix  
concerns: usability, accessibility  
applies_when: A page action, such as a save, an upload, a search, or a page load, can take more than about a second.  
context: ui  
tool gate: none; throttle the network and run the action.  
Backed by: Nielsen Norman Group (unjudged), Apple (unjudged), W3C (unjudged), Microsoft (unjudged), Atlassian (unjudged). Backing: unjudged. People cited: Ben Shneiderman (unjudged).

**Rule.** Show that a slow action is under way, and show its progress when it runs long.

**Why.** With no feedback, users click again, reload, or leave, and a double click can run the action twice. A bar tells them whether to wait. A message that says what is happening is better than "Loading". As a guide, show feedback after about one second. Past about ten seconds, show how much is done and offer Cancel where stopping is safe.

**FAIL**

```jsx
<button onClick={upload}>Upload</button>   // 40 s, nothing changes
```

**PASS**

```jsx
<button onClick={busy ? undefined : upload} aria-disabled={busy}>Upload</button>
{busy && <progress value={sent} max={total} aria-label="Uploading report.pdf" />}
{busy && <button onClick={cancel}>Cancel</button>}
<div role="status">{message}</div>   // "Uploading report.pdf", then "Upload complete"
// aria-disabled keeps keyboard focus on the button; disabled would drop it
```

**Counterpoint.** "A spinner on a 200 ms call flickers." Right: below about a second, show nothing, or the placeholder just flashes. Skeleton screens suit page loads, and progress bars suit uploads and other long jobs.

## svc-soft-delete-default

severity: should-fix  
concerns: security, correctness  
applies_when: A table or model marks a row as deleted instead of removing it.  
context: data  
tool gate: A test per read path: soft-delete a row, then assert the endpoint returns 404 or leaves it out of the list.  
Backed by: Microsoft (unjudged), Laravel (unjudged), Sequelize (unjudged), OWASP (unjudged). Backing: unjudged.

**Rule.** Filter soft-deleted rows out of every read path by default, and make a read that includes them an explicit call.

**Why.** A soft delete sets a column. It does not remove the row, so any query that forgets the filter still returns the record. One raw query or one new endpoint is enough to expose it. Put the filter in the model's default scope, so new queries inherit it, and keep the escape hatch visible. A deletion policy has to reach caches, exports, replicas and object versions too, or the record lives on in a copy.

**FAIL**

```csharp
modelBuilder.Entity<Document>();                 // no HasQueryFilter
var doc = await context.Documents.FindAsync(42); // returns the soft-deleted row
```

**PASS**

```csharp
modelBuilder.Entity<Document>().HasQueryFilter(d => d.DeletedAt == null);

// The one admin report that needs deleted rows, behind an admin check:
var all = await context.Documents.IgnoreQueryFilters().ToListAsync();
```

**Counterpoint.** "The admin console has to see deleted rows." Keep that one call explicit, name it for what it does, and check the caller is an admin. The default stays closed. Raw SQL and reporting replicas are the usual bypass, so route them through the same helper or audit them. A service that hard-deletes does not need the filter, but backups and object versions can still hold the old copy.

## svc-sqli-authn

severity: block  
concerns: security  
applies_when: The code builds a SQL query that includes request data or other untrusted input.  
context: server, data  
tool gate: Bandit B608 (`hardcoded_sql_expressions`), CodeQL `py/sql-injection`.  
Backed by: OWASP (unjudged), Python Software Foundation (unjudged), GitHub (unjudged), PortSwigger (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Pass untrusted data to queries as bound parameters, never by string concatenation or formatting.

**Why.** Concatenated input becomes SQL, so a value of `1 OR 1=1` reads every row and a quote ends the string early. A bound parameter travels apart from the query text, and the database never parses it as SQL.

**FAIL**

```python
db.execute("SELECT * FROM users WHERE id = " + req.id)
db.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

**PASS**

```python
db.execute("SELECT * FROM users WHERE id = ?", (req.id,))     # the placeholder style depends on the driver
db.execute("SELECT * FROM users WHERE name = ?", (name,))
```

**Counterpoint.** "An ORM makes this moot." Raw fragments still bypass it, and so do table, column and `ORDER BY` names, which cannot be bound. Map those to a fixed allowlist in code.

## svc-stream-dont-materialise

severity: should-fix  
concerns: performance  
applies_when: A handler reads, transforms, or returns a result whose size depends on the data (files, query results, response bodies).  
tool gate: Memory limit in tests with a large fixture.  
Backed by: OpenJS Foundation (unjudged), PostgreSQL (supports), Reactive Streams (supports). Backing: mixed.

**Rule.** Process large results as a stream with backpressure; do not load them whole into memory.

**Why.** A fast source piles data into memory faster than a slow consumer drains it. In the Node docs' test, memory grew from about 88 MB to about 1.5 GB. Memory then scales with data size, not with the code.

**FAIL**

```python
rows = db.execute("SELECT * FROM events").fetchall()   # 50M rows
return json.dumps(rows)
```

**PASS**

```python
def generate():
    for row in db.execute("SELECT * FROM events"):     # server-side cursor
        yield encode(row)
return StreamingResponse(generate())
```

**Counterpoint.** "Streaming complicates errors and retries." Yes: a failure mid-stream cannot change the status code. For small, bounded results, loading the whole result is simpler and fine; state the bound. [sys-load-shedding-bounded-queues](system.md#sys-load-shedding-bounded-queues) covers queue limits.

## svc-tenant-id-in-telemetry

severity: should-fix  
concerns: security, observability  
applies_when: A shared log, metric or audit store holds records from more than one tenant.  
context: server  
tool gate: A test that writes an event for each of two tenants, then queries one tenant and asserts the other is absent.  
Backed by: OWASP (unjudged), AWS (unjudged), Microsoft (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Put the verified tenant id on every tenant-scoped log, metric and audit record.

**Why.** A shared store returns another tenant's activity to any query that does not filter. The id has to be written from the verified tenant context, not from a request header, and it has to be there when a batch job or a queue worker writes the record, since no request middleware runs in those paths. A centralized audit store is acceptable only when read access enforces tenant scope. Metric events need the field too, or a per-tenant dashboard shows another tenant's numbers. Platform events that belong to no tenant, such as a node restart, carry no tenant id and are outside the Rule.

**FAIL**

```python
log.info("order %s paid", order_id)
audit.write(action="order.paid", actor=user.id)
```

**PASS**

```python
log.info("order %s paid", order_id, extra={"tenant_id": tenant.id})
audit.write(action="order.paid", tenant_id=tenant.id, actor=user.id)
```

**Counterpoint.** "The pipeline adds the tenant from the request context." That works only for code that runs inside a request. Workers, schedulers and sidecars write records too, and a query cannot recover a field that was never written. If a shared layer injects the field, verify it with a two-tenant query, because a layer that silently skips one producer looks the same as a correct one until the query runs. Splitting logs into a store per tenant is stronger still where the operational cost is justified.

## svc-timeouts

severity: block  
concerns: performance, reliability  
applies_when: The code calls a remote service over a network.  
Backed by: Python Software Foundation (unjudged), Microsoft (unjudged), Google (unjudged), AWS (unjudged). Backing: unjudged.

**Rule.** Set an explicit timeout on every remote call.

**Why.** A call without a bound holds a thread, a connection, and a caller indefinitely, so one slow dependency becomes an outage. Many clients, gRPC and `requests` among them, set no timeout by default. Where the caller has a deadline of its own, pass the remaining time down: a per-hop timeout that ignores it keeps working for a client that already gave up, and a retry loop shares that one deadline across its attempts.

**FAIL**

```python
resp = requests.get(url)                   # no timeout: can wait forever
reply = stub.GetUser(request)              # gRPC sets no deadline by default
```

**PASS**

```python
client = httpx.Client(timeout=httpx.Timeout(10.0, connect=2.0))   # set once on the client
resp = client.get(url)

def GetProfile(self, request, context):
    # bounded, and no longer than what the caller has left
    return stub.GetUser(request, timeout=min(2.0, context.time_remaining()))
```

**Counterpoint.** "Defaults are fine; the library will time out eventually." Many defaults are infinite, and an eventual timeout longer than the caller's own deadline is wasted work. Configure the client's timeout once at construction, connect and read separately, then shrink it per call to what the caller has left. Pick the numbers from measured latency, such as the downstream p99.9, not folklore.

## svc-tls-modern-only

severity: should-fix  
concerns: security  
applies_when: The service or its load balancer terminates TLS.  
context: server  
tool gate: testssl.sh or a similar scan against the public endpoint in CI; the load balancer's named security policy checked in config review.  
Backed by: IETF (unjudged), NIST (unjudged), OWASP (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Accept only TLS 1.2 and TLS 1.3 on servers.

**Why.** TLS 1.0 and 1.1 lack modern cipher suites and are deprecated by RFC 8996, and SSL 3.0 is broken outright. A server that still offers them lets an attacker on the path force a downgrade, and it fails compliance scans. Library defaults have moved to TLS 1.2, but an explicit lower setting, an old base image, or a load-balancer policy from years ago keeps the old versions alive. With TLS 1.2, prefer AEAD suites with forward secrecy.

**FAIL**

```python
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version = ssl.TLSVersion.TLSv1
```

**PASS**

```python
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
```

**Counterpoint.** "Some of our users have old clients." Measure first: log the negotiated version, and if old clients are a real share, serve them from a separate endpoint with an end date instead of weakening every endpoint.

## svc-update-rollback-on-failure

severity: should-fix  
concerns: reliability  
applies_when: The code replaces its own binary or an installed program with a new version.  
tool gate: Test that makes the final step fail and checks the old version still runs.  
Backed by: Microsoft (unjudged), Google (unjudged), Mender (unjudged). Backing: unjudged. People cited: go-update (Alan Shreve) (unjudged).

**Rule.** When an update fails, restore the previous version instead of leaving a missing or half-written one.

**Why.** Deleting the old binary before the new one is in place leaves nothing to run if the copy fails, and the tool cannot update itself back. On Windows a running executable cannot be deleted but can be renamed, so move it aside first and restore it on failure.

**FAIL**

```go
exe, _ := os.Executable()
os.Remove(exe) // fails on Windows for a running exe; if the next line fails, no binary is left
return os.Rename(newBin, exe)
```

**PASS**

```go
exe, err := os.Executable()
if err != nil {
	return err
}
old := exe + ".old"
if err := os.Rename(exe, old); err != nil {
	return err
}
if err := os.Rename(newBin, exe); err != nil {
	if rerr := os.Rename(old, exe); rerr != nil {
		return fmt.Errorf("update failed (%v) and rollback failed: %w", err, rerr)
	}
	return err
}
os.Remove(old) // best effort; retry at next start if the OS still holds it
return nil
```

**Counterpoint.** "Keeping a second copy costs disk space and clutter." One binary-sized file, removed after success, is cheap next to a tool that cannot start.

## svc-update-verify-provenance

severity: should-fix  
concerns: security  
applies_when: The code downloads and installs or runs a new version of itself or of another program, such as a self-updater or an install script.  
Backed by: Sparkle (unjudged), Sigstore (unjudged), The Update Framework (unjudged), Debian (unjudged), GitHub (unjudged), Google (unjudged). Backing: unjudged. People cited: go-update (Alan Shreve) (unjudged).

**Rule.** Verify a downloaded update against a signature, an attestation or a pinned key, or against a checksum that reached you by another route than the file; a checksum fetched from the same host as the file does not count.

**Why.** An attacker who controls the download host replaces the archive and its checksum file together, so the check passes and the new binary runs with the user's rights. A signature made with a key that is not on that host, or a hash from a different channel, still fails for the attacker.

**FAIL**

```go
archive, _ := get(base + "/tool.tar.gz")
want, _ := get(base + "/tool.tar.gz.sha256") // same host as the archive
got := sha256.Sum256(archive)
if hex.EncodeToString(got[:]) != strings.TrimSpace(string(want)) {
	return errors.New("checksum mismatch")
}
install(archive)
```

**PASS**

```go
var releaseKey = mustDecodeKey("<base64 public key>") // compiled into the binary, never downloaded

archive, _ := get(base + "/tool.tar.gz")
sig, _ := get(base + "/tool.tar.gz.sig")
if !ed25519.Verify(releaseKey, archive, sig) {
	return errors.New("bad signature")
}
install(archive)
```

**Counterpoint.** "HTTPS already protects the download, and signing needs key management." TLS protects the connection to the host, not the files on it once the host or its account is breached. Keyless signing and build attestations remove most of the key handling.

## svc-upload-validate-store

severity: block  
concerns: security  
applies_when: The service accepts file uploads.  
context: server  
tool gate: Upload tests with a renamed `.php`, an oversized file and a zip bomb.  
Backed by: OWASP (unjudged), Microsoft (unjudged), PortSwigger (unjudged), Django Software Foundation (unjudged). Backing: unjudged.

**Rule.** Allowlist the file type, cap the size, and store each upload under a generated name where the server will not execute it.

**Why.** The client-supplied name and Content-Type are attacker text. A user-chosen name allows path tricks, and an upload served from the web root with its original extension can run as code. Count the decompressed size of archives. Storing outside the web root and serving files through a handler, or from a separate domain, keeps a file that slips past the type check from running. [fn-confine-file-path](function.md#fn-confine-file-path) covers the path check.

**FAIL**

```python
path = f"/var/www/uploads/{file.filename}"
file.save(path)                       # any type, any size, public URL
```

**PASS**

```python
if sniff_type(file.stream) not in {"image/png", "image/jpeg"} or size > 5_000_000: abort(400)   # type from the content, not the name
file.save(STORE / f"{uuid4()}.bin")   # outside web root; served by /files/<id>
```

**Counterpoint.** "The extension check is enough." The extension is attacker text, and double extensions or parser quirks get past a check on it. The generated name and a storage place that never executes files are what make a file that slips through harmless.

## svc-webhook-replay-window

severity: should-fix  
concerns: security  
applies_when: The code accepts signed webhooks or signed messages from another system.  
context: server  
tool gate: A test that replays a captured request with the timestamp moved outside the tolerance and asserts a 4xx, and one that changes only the timestamp header and asserts a 4xx.  
Backed by: Svix (unjudged), Slack (unjudged), IETF (unjudged), Stripe (unjudged). Backing: unjudged.

**Rule.** Reject an inbound signed message whose creation time is outside a short tolerance, and sign that time with the body so it cannot be swapped.

**Why.** A valid signature proves who sent the message, not when. A captured request keeps its signature and can be sent again. Put the timestamp inside the signed content, as Slack, Svix and Stripe do. A timestamp in a separate header that the signature does not cover can be replaced by the attacker. Compare the timestamp with local time before doing any work. Retries are normal, so also store the message id and skip an id already processed. Deduplication stops a replay inside the window. The window stops one outside it and bounds how long the id store must keep entries.

**FAIL**

```python
if not verify_hmac(body, headers["X-Signature"], secret):
    return 401
apply_event(body)   # a captured request replays for as long as the secret lives
```

**PASS**

```python
ts = headers["X-Timestamp"]
if abs(time.time() - int(ts)) > 300:
    return 401
if not verify_hmac(f"{ts}.".encode() + body, headers["X-Signature"], secret):
    return 401
apply_event(body)
```

**Counterpoint.** "A tight window drops delayed deliveries and retries." It does. RFC 9421 lets an application enforce a maximum signature age and leaves the number to it, and five minutes is the default of Slack and Stripe, not a standard. Pick a tolerance from the provider's retry schedule and your clock skew, log every reject with the offset, and keep deduplication by event id so a replay inside the window still does nothing. A signature with no timestamp at all cannot be bounded this way. The receiving endpoint has to rely on deduplication and on the sender's short-lived credential.

## py-cancellation

severity: should-fix  
concerns: reliability, correctness  
applies_when: Async code catches exceptions around awaits or uses asyncio.timeout.  
tool gate: Ruff BLE001 / S110 for broad swallow; lint for CancelledError needs custom rule.  
Backed by: Python Software Foundation (unjudged). Backing: unjudged. People cited: Pablo González (unjudged).

**Rule.** Re-raise `CancelledError` (do not catch it via bare `except` or `BaseException`), and catch `TimeoutError` outside the `asyncio.timeout()` block.

**Why.** TaskGroup and timeouts are built on cancellation, so swallowing it makes shutdown hang and timeouts silently not fire. The conversion to `TimeoutError` happens at context exit, so a handler inside the block never sees it.

**FAIL**

```python
async with asyncio.timeout(5):
    try: await fetch()
    except TimeoutError: ...        # never reached
    except BaseException: pass      # eats cancellation
```

**PASS**

```python
try:
    async with asyncio.timeout(5):
        await fetch()
except TimeoutError:
    handle_timeout()
```

**Counterpoint.** "Cleanup code must run even on cancel." Clean up in `finally`, then re-raise, and never suppress. `uncancel()` is task bookkeeping, not permission to swallow.

## py-task-reference

severity: should-fix  
concerns: correctness  
applies_when: Python code calls asyncio.create_task or ensure_future.  
tool gate: Ruff RUF006 (asyncio-dangling-task).  
Backed by: Python Software Foundation (unjudged). Backing: unjudged. People cited: Pablo González (unjudged).

**Rule.** Never discard the result of `create_task`; keep a reference and surface its exceptions, preferably through a `TaskGroup`.

**Why.** The event loop holds only weak references, so an unreferenced task can be garbage-collected mid-run. A task that nobody awaits also loses its exception ("never retrieved").

**FAIL**

```python
asyncio.create_task(send_email(user))   # fire and forget
```

**PASS**

```python
async with asyncio.TaskGroup() as tg:
    tg.create_task(send_email(user))
# or: t = create_task(...); bg.add(t); t.add_done_callback(bg.discard)
```

**See also.** [py-cancellation](service.md#py-cancellation); for retried background work, [svc-idempotency-key](service.md#svc-idempotency-key).

**Counterpoint.** "The set-and-discard recipe from the docs is enough." It keeps the task alive but still never retrieves the exception, and the docs point to TaskGroup for that. The same reference rule applies to tasks passed to `asyncio.shield`.

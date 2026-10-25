# service

## svc-api-conditional-writes

severity: should-fix  
concerns: correctness  
applies_when: Two callers can update the same resource through PUT, PATCH or DELETE.

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

## svc-api-deprecation-sunset

severity: should-fix  
concerns: compatibility  
applies_when: A service retires an endpoint, field, version or parameter that outside callers use.

**Rule.** Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers, with the `Sunset` date no earlier than the `Deprecation` date.

**Why.** Callers cannot read your roadmap. A removal with no signal in the responses is an outage for whoever has not read the changelog. Counting calls that carry the headers also tells you when removal is safe.

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

## svc-api-error-code-stable

severity: should-fix  
concerns: compatibility  
applies_when: Callers of an HTTP or RPC API branch on the kind of error.

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

## svc-api-versioning-policy

severity: should-fix  
concerns: compatibility  
applies_when: A service offers an HTTP API to callers you do not deploy together with it.

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

## svc-auth-throttle-generic-errors

severity: block  
concerns: security  
applies_when: The service has a login, password-reset or one-time-code endpoint.

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

## svc-authz-central-deny-default

severity: block  
concerns: security  
applies_when: The service exposes routes or functions that different roles may call.

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

## svc-bound-client-controlled-sizes

severity: should-fix  
concerns: security  
applies_when: A request parameter or body sets how many records, bytes, items or operations the server handles.

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

## svc-cors-allowlist

severity: should-fix  
concerns: security  
applies_when: The service sends `Access-Control-Allow-Origin` or similar CORS headers.

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

## svc-idempotency-key

severity: block  
concerns: reliability, correctness  
applies_when: A non-idempotent operation (charge, create, send) can be retried by a client, a queue, or a saga.

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

## svc-list-endpoint-paginates

severity: should-fix  
concerns: performance  
applies_when: The service exposes an endpoint or RPC that returns a collection.

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

## svc-no-redundant-entry

severity: should-fix  
concerns: usability, accessibility  
applies_when: A multi-step flow, such as checkout or signup, asks for data in more than one step.

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
<input name="billing_address" value="12 Elm Road, Leeds" hidden>   <!-- shown, filled in, if the box is unchecked -->
```

**Counterpoint.** "Retyping a new password confirms it." That is a fair exception. So is data that is no longer valid, and re-entry that is the point of the task, such as a memory test. Browser autofill does not count: the page itself must supply the value.

## svc-no-secrets-in-url

severity: should-fix  
concerns: security  
applies_when: A client or server puts an API key, session token, bearer token, password, or personal data into a URL.

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

## svc-rate-limit-quota

severity: should-fix  
concerns: security, reliability  
applies_when: A shared API or queue serves several tenants or callers.

**Rule.** Enforce a per-tenant quota on shared APIs and queues.

**Why.** Without a quota, one noisy tenant consumes shared capacity for everyone. Also add a per-tenant concurrency cap, and return 429 for over-quota but 503 for the service's own lack of capacity, so clients do not retry quota errors as capacity problems.

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

**Counterpoint.** "One global rate limit is simpler." A global limit protects the service, but one tenant can use all of it, and then every other tenant gets errors. A per-tenant limit costs one key per tenant in the limiter. Some older services return 503 for quota errors, so the status code is a convention; what matters is that a client can tell a quota error from a capacity error. Shuffle sharding (per-tenant worker subsets) isolates tenants further, and this card does not require it.

## svc-reflow-and-zoom

severity: should-fix  
concerns: accessibility, usability  
applies_when: A page or app is served to browsers on screens of any size.

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

## svc-retry-policy

severity: block  
concerns: reliability  
applies_when: The code retries a failed call, or wraps a client that retries.

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

## svc-session-lifecycle

severity: block  
concerns: security  
applies_when: The service sets a session cookie or session ID after login.

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

## svc-slow-operation-shows-progress

severity: should-fix  
concerns: usability, accessibility  
applies_when: A page action, such as a save, an upload, a search, or a page load, can take more than about a second.

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

## svc-sqli-authn

severity: block  
concerns: security  
applies_when: The code builds a SQL query that includes request data or other untrusted input.

**Rule.** Pass untrusted data to queries as bound parameters, never by string concatenation or formatting.

**Why.** Concatenated input becomes SQL, so a value of `1 OR 1=1` reads every row and a quote ends the string early. A bound parameter travels apart from the query text, and the database never parses it as SQL.

**FAIL**

```python
db.execute("SELECT * FROM users WHERE id = " + req.id)
db.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

**PASS**

```python
db.execute("SELECT * FROM users WHERE id = %s", (req.id,))
db.execute("SELECT * FROM users WHERE name = %s", (name,))
```

**Counterpoint.** "An ORM makes this moot." Raw fragments still bypass it, and so do table, column and `ORDER BY` names, which cannot be bound. Map those to a fixed allowlist in code.

## svc-timeouts

severity: block  
concerns: performance, reliability  
applies_when: The code calls anything over a network or process boundary.

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

## svc-upload-validate-store

severity: block  
concerns: security  
applies_when: The service accepts file uploads.

**Rule.** Allowlist the file type, cap the size, and store each upload under a generated name where the server will not execute it.

**Why.** The client-supplied name and Content-Type are attacker text. A user-chosen name allows path tricks, and an upload served from the web root with its original extension can run as code. Count the decompressed size of archives. Storing outside the web root and serving files through a handler, or from a separate domain, keeps a file that slips past the type check from running. [fn-confine-file-path](function.md#fn-confine-file-path) covers the path check.

**FAIL**

```python
path = f"/var/www/uploads/{file.filename}"
file.save(path)                       # any type, any size, public URL
```

**PASS**

```python
if ext(file.filename) not in {".png", ".jpg"} or size > 5_000_000: abort(400)
file.save(STORE / f"{uuid4()}.bin")   # outside web root; served by /files/<id>
```

**Counterpoint.** "The extension check is enough." The extension is attacker text, and double extensions or parser quirks get past a check on it. The generated name and a storage place that never executes files are what make a file that slips through harmless.

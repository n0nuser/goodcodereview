# service

## svc-api-conditional-writes

severity: should-fix  
concerns: correctness  
applies_when: Two callers can update the same resource through PUT, PATCH or DELETE.  
context: server  
Backed by: IETF, Microsoft, Zalando.

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
context: server  
Backed by: IETF, Zalando, OpenAPI Initiative, GitHub, Google.

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

## svc-api-error-code-stable

severity: should-fix  
concerns: compatibility  
applies_when: Callers of an HTTP or RPC API branch on the kind of error.  
context: server  
Backed by: IETF, Google, Microsoft.

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
context: server  
Backed by: Zalando, Microsoft, Stripe.

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
context: server  
Backed by: OWASP, NIST, PortSwigger, Microsoft, Okta (Auth0), Google.

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
context: server  
Backed by: OWASP, PortSwigger, AWS, NIST.

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
context: server  
Backed by: OWASP, NIST, Google, Django Software Foundation.

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
Backed by: Google, Python Software Foundation, Tokio project, Cabify, AWS.

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

## svc-cli-destructive-dry-run

severity: should-fix  
concerns: reliability, maintainability  
applies_when: A command-line tool has a command that deletes, overwrites or sends something.  
context: cli  
Backed by: Kubernetes, Git, GNU Project, GitHub, Microsoft, Google, HashiCorp, Cursor. People cited: Command Line Interface Guidelines.

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
Backed by: Google, GitHub, AWS, HashiCorp, The Open Group, Heroku, Rust project. People cited: Command Line Interface Guidelines.

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
Backed by: GitHub, Google, HashiCorp, Microsoft, Cursor. People cited: Command Line Interface Guidelines.

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
Backed by: OWASP, Mozilla, PortSwigger, GitHub.

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
Backed by: OWASP, Mozilla, Google.

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
Backed by: OWASP, Mozilla, Django Software Foundation, IETF.

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

## svc-fail-closed-defaults

severity: should-fix  
concerns: security  
applies_when: The service reads configuration for authentication, an allow-list, a safety check, or a signing secret.  
context: server  
Backed by: OWASP, Microsoft, Google, Django Software Foundation, MITRE, AWS, CISA, NIST.

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

## svc-idempotency-key

severity: block  
concerns: reliability, correctness  
applies_when: A non-idempotent operation (charge, create, send) can be retried by a client, a queue, or a saga.  
context: server  
Backed by: Microsoft, IETF, Stripe.

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
Backed by: OWASP, Google, Kubernetes, IETF, Microsoft, Stripe.

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
Backed by: Google, Microsoft, Zalando, GitHub, Stripe.

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
context: ui  
Backed by: W3C, Nielsen Norman Group, GOV.UK, Baymard Institute. People cited: Ben Shneiderman.

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
Backed by: OWASP, IETF, MITRE, Mozilla.

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
context: server  
Backed by: AWS, Google, Microsoft, NIST.

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
context: ui  
Backed by: W3C, Deque, The A11y Project, WebAIM, Mozilla, Google, Microsoft.

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
Backed by: Microsoft, AWS, Google, Stripe, GitHub.

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
context: server  
Backed by: OWASP, Mozilla, NIST, Spring, Ruby on Rails.

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
context: ui  
Backed by: Nielsen Norman Group, Apple, W3C, Microsoft, Atlassian. People cited: Ben Shneiderman.

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
context: server, data  
Backed by: OWASP, Python Software Foundation, GitHub, PortSwigger, Google.

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

## svc-timeouts

severity: block  
concerns: performance, reliability  
applies_when: The code calls a remote service over a network.  
Backed by: Python Software Foundation, Microsoft, Google, AWS.

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
Backed by: IETF, NIST, OWASP, Microsoft.

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
Backed by: Microsoft, Google, Mender. People cited: go-update (Alan Shreve).

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
Backed by: Sparkle, Sigstore, The Update Framework, Debian, GitHub, Google. People cited: go-update (Alan Shreve).

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
Backed by: OWASP, Microsoft, PortSwigger, Django Software Foundation.

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

## py-cancellation

severity: should-fix  
concerns: reliability, correctness  
applies_when: Async code catches exceptions around awaits or uses asyncio.timeout.  
Backed by: Python Software Foundation. People cited: Pablo González.

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
Backed by: Python Software Foundation. People cited: Pablo González.

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

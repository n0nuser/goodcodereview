# system

## sys-agent-tool-least-privilege

severity: block  
concerns: security, process  
applies_when: An LLM agent can call tools, run code, or act on external systems.  
Backed by: OWASP, NCSC, Microsoft.

**Rule.** Give the agent only the narrow tools and the minimal credentials its task needs.

**Why.** Hallucination or an injected instruction can drive any tool the model holds. An open-ended shell or URL fetch hands over everything the service account can do. Where you can, run each tool as the requesting user rather than a shared admin identity, and let the downstream system check that user's rights on every call. [sys-prompt-injection](system.md#sys-prompt-injection) covers validating model output and human approval; this card covers how much the agent can reach in the first place.

**FAIL**

```text
tools = [shell(), http_fetch(any_url), db(admin_role)]       # one shared service identity
```

**PASS**

```text
tools = [read_ticket(id), add_comment(id, text)]             # narrow functions
creds = user_scoped_token(user, scopes=["tickets:rw"])       # downstream checks the user
```

**Counterpoint.** "Narrow tools make the agent less useful." Add tools when a task needs them and remove those that no task uses. A tool the model never calls is risk without benefit.

## sys-cache-bounds-invalidation

severity: should-fix  
concerns: performance  
applies_when: The code adds an in-process or shared cache.  
Backed by: AWS, Redis, Caffeine project, IETF.

**Rule.** Bound every cache by size and give its entries an expiry.

**Why.** An unbounded cache is a memory leak that shows up only under production traffic. Redis has no memory limit by default on 64-bit builds. Choose the TTL from the staleness you can tolerate, because an arbitrary one either serves stale data or does not help. Also version the values, since old and new code read each other's entries during a rolling deploy, and give the cache hit, miss, and origin-request metrics and a way to invalidate.

**FAIL**

```text
CACHE = {}                         # grows forever, never expires
redis.conf: maxmemory 0            # unlimited, used as a cache
```

**PASS**

```text
cache = cachetools.TTLCache(maxsize=10_000, ttl=60)
redis.conf: maxmemory 2gb, maxmemory-policy allkeys-lru
```

**Counterpoint.** "Stale data is a business risk, not a review issue." It is one when the staleness window was never chosen. The rule asks for a decision, not a number. A soft TTL (refresh in the background) under a hard TTL (must refetch) balances freshness against load.

## sys-consistent-ui-terms

severity: discuss  
concerns: usability, accessibility  
applies_when: Several screens or apps show the same action, status, or concept to the same users.  
Backed by: Nielsen Norman Group, W3C, GOV.UK. People cited: Ben Shneiderman.

**Rule.** Use one label and one icon for the same action and the same concept across all screens.

**Why.** When "Remove", "Delete", and "Discard" all mean the same thing, users stop trusting any of them and ask whether each one differs. Keep the control in the same place on each screen, too. A familiar control costs no thought. A different one costs a pause, and in a destructive flow, a mistake.

**FAIL**

```text
Orders page:    [Delete]       (trash icon, right of row)
Customers page: [Remove]       (x icon, left of row)
Invoices page:  [Discard draft](no icon, menu)
```

**PASS**

```text
Orders, Customers, Invoices: [Delete] with the trash icon, last action in the row menu.
A different outcome, such as archive, gets a different label: [Archive].
```

**Counterpoint.** "Each team knows its users best." Consistent does not mean uniform. Differ where the job differs, and keep the wording and look of the shared actions the same. Drive the shared parts from the design-system component, so they cannot drift.

## sys-fanout-leg-deadlines

severity: should-fix  
concerns: performance, reliability  
applies_when: A request fans out to several backends, shards, or replicas and combines the answers.  
Backed by: Google, Apache Software Foundation, Elastic, Envoy.

**Rule.** Give every leg of a fan-out its own deadline, and decide in code what happens when a leg misses it: a partial result, a hedged request, or an error.

**Why.** Fan-out turns rare slowness into common slowness. If each of 100 backends is slow on 1 request in 100, about 63% of requests wait on at least one slow backend. Without a per-leg deadline the slowest leg sets the latency of every request.

**FAIL**

```text
results = await gather(*[shard.search(q) for shard in shards])   # waits for the slowest shard
```

**PASS**

```text
results = await asyncio.gather(
    *[asyncio.wait_for(shard.search(q), 0.08) for shard in shards],
    return_exceptions=True)
hits = [r for r in results if not isinstance(r, Exception)]
return merge(hits, partial=len(hits) < len(shards))
```

**Counterpoint.** "Hedging doubles the load." Sent at once to every replica, it does. Send the hedge only after a wait past about the 95th percentile, cap the attempts, and cancel the twin, and the extra load stays near 5%. Hedge only idempotent reads. A partial result needs a product decision. The deadline does not.

## sys-load-shedding-bounded-queues

severity: block  
concerns: reliability  
applies_when: Work is buffered in a queue, a channel, or a thread pool between components.  
Backed by: AWS, Google, Netflix.

**Rule.** Bound every queue and reject excess work cheaply.

**Why.** An unbounded queue turns overload into minutes of latency, and by the time old items are served, callers have given up. Also keep a way to sideline old or excess messages (see PASS).

**FAIL**

```text
q = Queue()                      # no maxsize
on overload: enqueue anyway; no age alarm, no spillover
```

**PASS**

```text
q = Queue(maxsize=1000); if full: return 503 fast
alarm on age of oldest item; spillover queue for old deltas
```

**Counterpoint.** "Dropping work loses data." A bounded queue only makes the loss explicit and early. For work that must not be lost, spill to durable storage rather than memory. Shedding itself must be cheap. Slowing fast errors on purpose can stop a load balancer from steering more traffic at a shedding host.

## sys-lock-fencing

severity: block  
concerns: reliability, correctness  
applies_when: A TTL lock or lease guards a write to an external store.  
Backed by: AWS, Google, Apache Software Foundation, Hazelcast. People cited: Martin Kleppmann, Salvatore Sanfilippo.

**Rule.** Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.

**Why.** A holder can pause past its TTL, lose the lock and still write. Only the store can reject the stale writer.

**FAIL**

```text
if redis.set(key, id, nx=True, px=10000):
    db.update(row)                 # pause here => two writers
```

**PASS**

```text
token = lock.acquire()             # monotonically increasing
db.update(row, where fence < token, set fence = token)
```


**Counterpoint.** "Our lock library is safe, so holding the lock is enough." Whether a given algorithm such as Redlock is safe is disputed, but that a paused holder can still write is not. Locks used only for efficiency (avoiding duplicate work) may be loose. For correctness, state that it is a correctness lock and make the store reject stale writers, with a monotonically increasing token or a unique token checked by compare-and-set, whatever the lock implementation.

**See also.** [svc-idempotency-key](service.md#svc-idempotency-key).

## sys-migration-expand-contract

severity: block  
concerns: reliability, compatibility  
applies_when: A change drops, renames, or retypes a column, or mixes schema change with a data backfill.  
Backed by: GitLab, Stripe, Ecto, CockroachDB. People cited: Andrew Kane.

**Rule.** Run data backfills in batches, in a migration separate from the schema change.

**Why.** A large backfill in one transaction holds locks for its whole run, and a failure halfway rolls all of it back. Batches with a pause between them keep each lock short and let the backfill resume. [chg-expand-contract](change.md#chg-expand-contract) covers the order of releases around it.

**FAIL**

```text
release N: RENAME COLUMN a TO b ; UPDATE big_table SET b = ... (one tx)
```

**PASS**

```text
N: add b, dual-write, ignore a in code ; N+1: batched backfill ; N+2: drop a
```

**Counterpoint.** "One `UPDATE` is simpler than a batched job." On a small table it is, and this card does not apply there. Once the update holds a lock long enough to block live traffic, batch it.

## sys-n-plus-one-pooling

severity: should-fix  
concerns: performance  
applies_when: Code loads related rows in a loop, or opens database connections per request.  
Backed by: Django Software Foundation, Ruby on Rails, SQLAlchemy, Microsoft, OpenJS Foundation, PgBouncer project, PostgreSQL.

**Rule.** Fetch related rows in one query or batch, never one query per row.

**Why.** A query per row multiplies latency by result size. Also back filter and join columns with an index and use a bounded connection pool: an unindexed filter turns each query into a scan, and a connection per request exhausts the database under load.

**FAIL**

```python
for o in Order.objects.all():
    print(o.user.email)                              # one query per order
```

**PASS**

```python
for o in Order.objects.select_related("user"):
    print(o.user.email)                              # one query with a join
```

**Counterpoint.** "Measure first." Yes, for micro-optimizations, but a query inside a loop over unbounded input is a defect by shape.

## sys-pii-minimise-retention

severity: should-fix  
concerns: security  
applies_when: The system stores, copies or logs personal or otherwise sensitive data.  
Backed by: OWASP, ICO, intersoft consulting.

**Rule.** Give every store of personal or sensitive data a retention period, and delete or anonymise the data when it ends.

**Why.** Data you do not keep cannot leak. Keep only the fields the feature needs, too. Full card numbers, national IDs and raw request bodies pile up in logs, analytics tables and backups, and nobody owns their deletion. Tokenise or truncate when the full value is not needed, and encrypt what you keep. This is a technical check, not a legal opinion.

**FAIL**

```text
analytics.events: full email, DOB and phone, no TTL
logs: raw request body with the national ID field, kept forever
```

**PASS**

```text
analytics.events: hashed user id, TTL 90 days
logs: id field masked; table has a retention policy and an owner
```

**Counterpoint.** "We might need it later." A guess is not a purpose. Keep it when a named feature or legal duty needs it, and write that reason next to the retention rule.

## sys-prompt-injection

severity: block  
concerns: security  
applies_when: An LLM reads untrusted text (user input, web pages, documents) and can call tools or produce output that code acts on.  
Backed by: OWASP, NCSC, Microsoft, Google.

**Rule.** Validate model output deterministically before code acts on it.

**Why.** Injected instructions in retrieved text can steer tool calls. No known prevention is fool-proof, and RAG or fine-tuning do not fully fix it, so the goal is to limit what a fooled model can make the code do. Also keep credentials in code, not in the model, and require human approval for high-risk actions.

**FAIL**

```text
tool_call = llm(user_doc); shell(tool_call.cmd)     # model holds the API token
```

**PASS**

```text
cmd = parse_strict(llm(...)); if cmd not in ALLOWED: reject
destructive actions -> human confirm ; untrusted text labelled in the prompt
```

**Counterpoint.** "Guardrail prompts block it." They reduce risk but are not a boundary. The permission model has to hold even when the model is fooled.

## sys-secrets-and-errors

severity: block  
concerns: security, correctness  
applies_when: The code handles credentials, logs data, or returns errors to clients.  
Backed by: OWASP, MITRE, Heroku, MIT, IETF.

**Rule.** Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.

**Why.** A catch-and-continue around a validation step grants access when the check crashes. Stack traces and SQL in a response show an attacker how the system is built, and a token there can be reused. Keep secrets out of source and logs too: read them from the environment or a secrets manager.

**FAIL**

```text
return {"error": traceback.format_exc()}
try: check_token(t)
except Exception: pass            # continues as authorized
```

**PASS**

```text
return {"error": "internal", "id": err_id}   # details to logs, redacted
try: check_token(t)
except Exception as err:
    log.warning("auth failed: %s", redact(err)); deny()
```

**Counterpoint.** "A broad `except Exception` breaks the specific-exceptions rule." At a security boundary, fail-closed wins: catch broadly, log redacted, deny, and never use a bare `except:`. "We need detail to debug." Log it server-side with a correlation id.

## sys-ssrf

severity: block  
concerns: security  
applies_when: The server fetches a URL that a user or external data supplies.  
Backed by: OWASP, GitHub, AWS, PortSwigger.

**Rule.** Fetch a user-supplied URL only when its host matches a server-side allowlist.

**Why.** The server can reach networks that the attacker cannot, such as internal services and the cloud metadata address, and an open fetch lets the attacker read them. A hostname allowlist alone does not stop DNS rebinding, so also check that the resolved address is not private and connect to that address. Turn off redirect following, or check each redirect target the same way.

**FAIL**

```python
requests.get(request.args["url"])
```

**PASS**

```python
u = urlparse(request.args["url"])
if u.scheme != "https" or u.hostname not in ALLOWED_HOSTS: abort(400)
requests.get(u.geturl(), allow_redirects=False, timeout=5)
```

**Counterpoint.** "Blocklisting private ranges is enough." Alternate IP forms, URL parser tricks and open redirects get past a blocklist. An allowlist fails closed when someone finds a new trick.

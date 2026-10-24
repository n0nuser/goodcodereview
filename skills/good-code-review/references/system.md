# system

## sys-cache-bounds-invalidation

severity: should-fix  
concerns: performance  
applies_when: The code adds an in-process or shared cache.

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

**See also.** [[svc-idempotency-key]].

## sys-migration-expand-contract

severity: block  
concerns: reliability, compatibility  
applies_when: A change drops, renames, or retypes a column, or mixes schema change with a data backfill.

**Rule.** Run data backfills in batches, in a migration separate from the schema change.

**Why.** A large backfill in one transaction holds locks for its whole run, and a failure halfway rolls all of it back. Batches with a pause between them keep each lock short and let the backfill resume. [[chg-expand-contract]] covers the order of releases around it.

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

## sys-secrets-and-errors

severity: block  
concerns: security, correctness  
applies_when: The code handles credentials, logs data, or returns errors to clients.

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

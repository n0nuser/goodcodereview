# system

## sys-load-shedding-bounded-queues

severity: block  
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

## sys-secrets-and-errors

severity: block  
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

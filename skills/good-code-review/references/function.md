# function

## fn-comments-explain-why

severity: should-fix  
concerns: maintainability  
applies_when: A comment sits next to code, or the code needs one to be understood.

**Rule.** Write comments that give a reason, a constraint, or a trade-off; rename before commenting, and never restate what the next line does.

**Why.** A restating comment rots silently and adds nothing. A missing reason makes the next person delete the code that mattered.

**FAIL**

```text
counter += 1  # increment the counter
retry = False  # see the PR, currently disabled
```

**PASS**

```text
# Business decision: activation and entitlement update in one transaction,
# so a user never has access without an active subscription.
# TODO: remove when billing emits entitlement events itself.
```

**Counterpoint.** "Good names make comments unnecessary." Names carry *what*. They cannot carry why a branch exists, a unit, or what callers may rely on, and a missing reason costs more than a slightly stale one. Rename first, then comment what the name cannot say. A stale comment is a defect either way. The test is whether the comment adds information that the code cannot carry.

## fn-fetch-only-needed-data

severity: should-fix  
concerns: performance  
applies_when: A function queries a database or an API and then filters, counts, or sums the result in application code.

**Rule.** Filter, count, and aggregate in the query, and select only the columns the code uses.

**Why.** Loading every row to count it, or every column to read one, moves data across the network and through memory for nothing. `SELECT *` also rules out an index-only scan.

**FAIL**

```python
total = sum(o.amount for o in Order.objects.all() if o.status == "paid")
n = len(Order.objects.filter(user=u))        # loads every row
emails = [u.email for u in User.objects.all()]   # loads every column
```

**PASS**

```python
total = Order.objects.filter(status="paid").aggregate(Sum("amount"))["amount__sum"]
n = Order.objects.filter(user=u).count()
emails = User.objects.values_list("email", flat=True)
```

**Counterpoint.** "Pushing logic into the database makes it the bottleneck." It does for formatting and business rules. Filtering and aggregation are what the database is built for, and moving them out usually ships far more data than it saves.

## fn-independent-work-concurrent

severity: should-fix  
concerns: performance, correctness  
applies_when: A function awaits or calls several I/O operations that do not depend on each other.

**Rule.** Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.

**Why.** Sequential awaits add their latencies. Three 200 ms calls take 600 ms in a row and 200 ms together.

**FAIL**

```python
user = await get_user(uid)
orders = await get_orders(uid)       # does not use `user`
prefs = await get_prefs(uid)
```

**PASS**

```python
user, orders, prefs = await asyncio.gather(
    get_user(uid), get_orders(uid), get_prefs(uid))
```

**Counterpoint.** "Parallel calls load the dependency harder and complicate errors." Cap fan-out with a semaphore or pool, and use a task group so one failure cancels the rest. A deliberate order, for rate limits or ordering, is a valid reason. Write it down.

## fn-join-dont-concat-in-loop

severity: should-fix  
concerns: performance  
applies_when: A function builds a string from pieces in a loop whose length depends on input.

**Rule.** Build a string from a loop with a builder or a join, never with repeated `+=`.

**Why.** Strings are immutable in Python, Go, Java, and .NET, so each `+=` copies everything built so far. Over n pieces the total cost grows with the square of the output length.

**FAIL**

```python
out = ""
for row in rows:
    out += f"{row.id},{row.name}\n"
```

**PASS**

```python
out = "".join(f"{row.id},{row.name}\n" for row in rows)
```

**Counterpoint.** "CPython optimises `+=` in place." Sometimes: only in CPython, and only while nothing else holds a reference to the string. Code that leans on it turns quadratic on other runtimes. A small fixed number of pieces is fine with `+` or an f-string, which read better. The rule covers loops over input-sized data.

## fn-no-blocking-call-in-async-code

severity: block  
concerns: performance, correctness  
applies_when: Code runs on an event loop or an async runtime (asyncio, Node.js, Tokio, ASP.NET async handlers).

**Rule.** Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.

**Why.** An event loop runs one callback at a time. A `time.sleep`, a synchronous HTTP call, or a big hash inside a handler stalls every other request on that loop, not just the slow one.

**FAIL**

```python
async def handler(req):
    data = requests.get(url).json()          # blocks the loop
    digest = hashlib.pbkdf2_hmac("sha256", pw, salt, 600_000)
```

**PASS**

```python
async def handler(req):
    data = (await client.get(url)).json()    # httpx.AsyncClient
    digest = await asyncio.to_thread(hashlib.pbkdf2_hmac, "sha256", pw, salt, 600_000)
```

**Counterpoint.** "This call is fast enough." A short read from a local SSD can be quicker synchronously. Measure it with asyncio debug mode or the runtime's equivalent. A call that crosses the network, or that waits on anything outside the process, is never in that class.

## fn-regex-compiled-once

severity: should-fix  
concerns: performance  
applies_when: Code builds a regular expression or similar compiled matcher inside a loop or a function that runs per request.

**Rule.** Compile a regular expression once, at module or startup level, and reuse it.

**Why.** Compiling costs far more than matching and throws away reusable allocations. Inside a loop or a per-request function, the cost repeats on every call.

**FAIL**

```go
func valid(s string) bool {
	return regexp.MustCompile(`^[a-z]+$`).MatchString(s)   // compiled per call
}
```

**PASS**

```go
var lower = regexp.MustCompile(`^[a-z]+$`)

func valid(s string) bool { return lower.MatchString(s) }
```

**Counterpoint.** "The library caches patterns." Python and .NET keep recently used patterns, so a few static calls are fine. A pattern built from input or an unbounded set of patterns defeats the cache.

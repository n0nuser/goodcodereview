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

**Counterpoint.** "Our only callers are internal." Then the call count with the header gives you the list of owners to ask, and removal is cheap. [[chg-expand-contract]] covers the order of steps; this card covers what the response tells the caller. Both headers describe one resource, so send them on each deprecated route, not only on the API root.

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

**Counterpoint.** "We will cross that bridge later." Later arrives with a customer on the old shape. The scheme can be minimal. A media type, a dated query parameter and a pinned header all work. Pick one and write it down. What counts as breaking is in [[chg-breaking-change-taxonomy]].

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

**See also.** [[sys-lock-fencing]] shares the goal but uses a different mechanism (stale lock holders).

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

**Why.** Immediate, unbounded, or synchronized retries turn a brief fault into a load spike on the struggling dependency. Retry at one layer only: three layers of three attempts is nine calls per user request. Make retried writes safe with [[svc-idempotency-key]].

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

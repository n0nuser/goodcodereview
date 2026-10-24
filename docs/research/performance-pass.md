# Performance pass: sources for a performance checklist at every level

Fetched 2026-10-24. Pages were read through WebFetch (a small model summarises the page), so every row is paraphrase. The Tail at Scale text was read from the author-hosted PDF. Each row gives the URL, the organisation behind it, how much was read, the distilled point, whether a reviewer can mark `FAIL`, and the card id it supports. Quotes are 15 words or fewer. "Topic only" means the page covers the subject but does not back the rule's requirement, so it does not count.

Org counting: one organisation counts once, whatever the number of pages. Google covers the SRE book, "The Tail at Scale", gRPC, web.dev, Lighthouse CI, Chromium, Cloud Profiler, and the Go project. AWS covers the Builders' Library and AWS docs. Microsoft covers every learn.microsoft.com page. CNCF projects (Prometheus, OpenTelemetry, Envoy, Istio, Linkerd) are counted as separate projects below, with the CNCF note so a later pass can count them conservatively. The promotion bar is 3 orgs that back the requirement itself. The notes at the end of each section give the count per rule and say `note:` where a card falls short.

## 1. Function level

### fn-join-dont-concat-in-loop

1. https://docs.python.org/3/faq/programming.html (org: Python; read: the string-concatenation FAQ). Strings are immutable, so building one with repeated `+` costs quadratic time in the total length. Collect the pieces in a list and join once. FAIL: yes, `s += piece` in a loop over caller-sized input. -> `fn-join-dont-concat-in-loop`.
2. https://pkg.go.dev/strings#Builder (org: Google, the Go project; read: the type docs). `strings.Builder` exists to avoid copying while a string is assembled from pieces. FAIL: yes, `s = s + x` in a loop. -> `fn-join-dont-concat-in-loop`.
3. https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/strings/common-tasks/concatenate (org: Microsoft; read: full, reached through the older how-to URL). Each `+` or `+=` allocates a new string. Use `StringBuilder` when the number of pieces is large or unknown. For a small fixed set, `+` or interpolation reads better. FAIL: yes, for unbounded counts only. -> `fn-join-dont-concat-in-loop`.
4. https://docs.python.org/3/tutorial/datastructures.html (org: Python; read: lists and sets). Lists are slow at the front (insert and pop shift every element) and sets give fast membership tests. Qualitative, no complexity table. -> topic only for this card. The `wiki.python.org/moin/TimeComplexity` page redirected to a 404, so it is a recorded gap, not a source.

Notes: 3 orgs (Python, Google/Go, Microsoft) back the string-building rule. The list-membership half has one org (Python) and is left out of the card. Counterpoint kept in the card: a small fixed number of pieces is fine.

### fn-regex-compiled-once

5. https://docs.rs/regex/latest/regex/ (org: Rust project; read: the usage section). Compiling a regex in a loop is an anti-pattern: each compile costs far more than a match and discards reusable allocations. Build it once and reuse it. FAIL: yes, `Regex::new` inside a loop or per call. -> `fn-regex-compiled-once`.
6. https://pkg.go.dev/regexp (org: Google, Go; read: the package overview). Compile a pattern once, normally at program start. `MustCompile` suits package-level variables, and a compiled `Regexp` is safe for concurrent use. The page has no explicit "not in a loop" sentence. FAIL: yes, `regexp.MustCompile` inside a function that runs per request. -> `fn-regex-compiled-once`.
7. https://docs.python.org/3/library/re.html (org: Python; read: `re.compile`). Keeping a compiled pattern is more efficient when the expression is used several times. The module also caches recent patterns, so a few module-level calls are not a real failure. FAIL: yes for `re.compile` inside the loop, weak for `re.match(pattern, s)`. -> `fn-regex-compiled-once`.
8. https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex (org: Microsoft; read: static versus instance methods). Static `Regex` methods are preferred over creating a new instance with the same pattern each time, because the engine caches the compiled form. FAIL: yes, `new Regex(p)` per call. -> `fn-regex-compiled-once`.

Notes: 4 orgs (Rust, Google/Go, Python, Microsoft). Only Rust states the loop rule in so many words. The card says "inside a loop or per call".

### fn-no-blocking-call-in-async-code

9. https://docs.python.org/3/library/asyncio-dev.html (org: Python; read: the blocking-code section). Blocking or CPU-bound code run directly in the event loop stalls every task. Hand it to `loop.run_in_executor`. Debug mode logs callbacks that take over 100 ms. FAIL: yes, `time.sleep`, `requests.get`, or heavy compute in `async def`. -> `fn-no-blocking-call-in-async-code`.
10. https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop (org: OpenJS, Node.js; read: full). Keep each callback short. Do not call synchronous crypto, zlib, filesystem, or child-process APIs in a server. Move heavy CPU to worker threads or split it into chunks. FAIL: yes, `fs.readFileSync` or `pbkdf2Sync` in a request handler. -> `fn-no-blocking-call-in-async-code`.
11. https://docs.rs/tokio/latest/tokio/ (org: Tokio project; read: the CPU-bound and blocking-code section). Tasks yield only at `.await`, so long compute with no await stalls the others. Run blocking work with `spawn_blocking`. FAIL: yes, `std::fs` or `std::thread::sleep` inside `async fn`. -> `fn-no-blocking-call-in-async-code`.
12. https://learn.microsoft.com/en-us/azure/architecture/antipatterns/synchronous-io/ (org: Microsoft; read: full). Blocking I/O on a request thread exhausts the thread pool under load, and requests then queue and time out. Use the async API. Short reads from a local SSD can be faster synchronously. FAIL: yes, with that caveat. -> `fn-no-blocking-call-in-async-code`.

Notes: 4 orgs (Python, OpenJS, Tokio, Microsoft). The Microsoft Azure page is the only one that gives the throughput numbers (about tenfold in its load test).

### fn-independent-work-concurrent (existing card, sources added)

13. https://docs.python.org/3/library/asyncio-task.html (org: Python; read: `gather` and `TaskGroup`). `gather` runs awaitables concurrently and returns results in input order. A `TaskGroup` cancels the siblings when one fails. FAIL: yes, independent awaits one after the other. -> `fn-independent-work-concurrent`.
14. https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all (org: Mozilla, MDN; read: full). `Promise.all` runs promises concurrently and rejects on the first failure without cancelling the rest. FAIL: yes, `await` in a `for` loop over independent items. -> `fn-independent-work-concurrent`.
15. https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap (org: Microsoft; read: full). Names `WhenAll` and `WhenAny` as combinators. Topic only; not counted.

Notes: 2 orgs back the requirement with a primary page (Python, Mozilla), plus the Cursor skill already in `second-pass.md` (an opinion source). Fewer than 3 independent orgs of data, so the card stays a draft. A third org would come from Go `errgroup` (cited in `svc-bounded-background-tasks`).

### fn-fetch-only-needed-data

16. https://learn.microsoft.com/en-us/azure/architecture/antipatterns/extraneous-fetching/ (org: Microsoft; read: full). Fetching more than the operation needs wastes I/O. Select the needed columns, filter and aggregate in the database, and paginate unbounded results. A client-side `AsEnumerable()` filter is the typical trap. FAIL: yes. -> `fn-fetch-only-needed-data`.
17. https://docs.djangoproject.com/en/stable/topics/db/optimization/ (org: Django Software Foundation; read: the database-work section). Filter and aggregate in the database. Fetch only what you need with `values`, `values_list`, `defer`, and `only`. Misusing `only` and `defer` can add queries. FAIL: yes, Python-side filter or sum over `.all()`. -> `fn-fetch-only-needed-data`.
18. https://docs.djangoproject.com/en/stable/ref/models/querysets/ (org: Django; read: first half). `len(qs)` loads every row, while `count()` runs `COUNT`, and `exists()` answers a yes/no question. FAIL: yes, `len(qs)` for a count. -> `fn-fetch-only-needed-data`.
19. https://use-the-index-luke.com/sql/clustering/index-only-scan-covering-index (org: Markus Winand, independent; read: the page). An index-only scan needs every selected column in the index. Selecting only the needed columns keeps that possible, and `select *` rules it out. FAIL: yes, `SELECT *` in a hot query. -> `fn-fetch-only-needed-data`.
20. https://docs.sqlalchemy.org/en/20/orm/queryguide/columns.html (org: SQLAlchemy; read: the page). Loading only some columns helps when a table has large, rarely used columns. `load_only` and `defer` do it, and `raiseload` flags unexpected lazy loads. FAIL: yes. -> `fn-fetch-only-needed-data`.
21. https://www.postgresql.org/docs/current/indexes-index-only-scans.html (org: PostgreSQL; read: full). An index-only scan answers from the index when all referenced columns are in it. Indirect support only: it does not forbid `select *`. -> topic only.
22. https://learn.microsoft.com/en-us/azure/architecture/antipatterns/busy-database/ (org: Microsoft; read: full). Counterpoint: let the database do what it is good at (aggregation), not formatting or business logic, and do not move work if the database then ships far more data. -> counterpoint for `fn-fetch-only-needed-data`.

Notes: 4 orgs back the requirement (Microsoft, Django, Winand, SQLAlchemy). PostgreSQL is indirect.

## 2. Module, service and system level: data access, clients, pagination, plans, caches

### sys-n-plus-one-pooling (existing card, sources added)

23. https://docs.djangoproject.com/en/stable/ref/models/querysets/ (org: Django; read: `select_related`, `prefetch_related`). `select_related` joins single-valued relations into the main query, and `prefetch_related` runs one extra query per lookup and joins in Python. Both stop per-row queries during iteration. FAIL: yes, a loop that reads `obj.fk.field` with neither. -> `sys-n-plus-one-pooling`.
24. https://guides.rubyonrails.org/active_record_querying.html (org: Ruby on Rails; read: eager loading). Looping over 10 books and reading the author runs 11 queries, and `includes(:author)` makes it 2. FAIL: yes. -> `sys-n-plus-one-pooling`.
25. https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html (org: SQLAlchemy; read: loader strategies). Default lazy loading costs N+1 selects for N parents. `selectinload` and `joinedload` fix it, and `raiseload` turns an accidental lazy load into an error. FAIL: yes. -> `sys-n-plus-one-pooling`.
26. https://learn.microsoft.com/en-us/azure/architecture/antipatterns/chatty-io/ (org: Microsoft; read: full). Many small I/O calls add up. It names the N+1 problem, fixes it with one query or `Include`, and batches HTTP calls. The fix can cause extraneous fetching, so size the batch. FAIL: yes, a query or HTTP call per row. -> `sys-n-plus-one-pooling`.
27. https://learn.microsoft.com/en-us/ef/core/querying/related-data/ (org: Microsoft; read: landing page only). Names eager, explicit, and lazy loading. Topic only.
28. https://nodejs.org/api/http.html#class-httpagent (org: OpenJS, Node.js; read: the Agent class). With `keepAlive`, idle sockets are pooled per host and port. `maxSockets` defaults to unlimited. FAIL: yes, an unbounded default or `agent: false` on a hot path. -> `sys-n-plus-one-pooling`, `mod-pooled-clients-built-once`.
29. https://www.pgbouncer.org/features.html (org: PgBouncer project; read: the page). Lets many clients share a small number of server connections, so the database connection count stays bounded. Partial support for "bounded pool". -> `sys-n-plus-one-pooling`.
30. https://www.postgresql.org/docs/current/runtime-config-connection.html (org: PostgreSQL; read: `max_connections`). Caps concurrent connections (default 100) and raising it costs shared memory. Topic-level for the pool bound. -> `sys-n-plus-one-pooling`.

Notes: the N+1 half has 4 orgs (Django, Rails, SQLAlchemy, Microsoft). The bounded-pool half has 3 partial sources (Node, PgBouncer, PostgreSQL). The "index the filter and join columns" clause has no source beyond Use The Index, Luke at topic level, so it stays in the card as `note:`. Not read: Hibernate fetching chapter and the EF Core sub-pages.

### mod-pooled-clients-built-once (existing card, sources added)

31. https://learn.microsoft.com/en-us/azure/architecture/antipatterns/improper-instantiation/ (org: Microsoft; read: full). Clients such as `HttpClient`, `CosmosClient`, and a Redis multiplexer are meant to be created once and shared. A new one per request exhausts sockets under load. FAIL: yes, `new HttpClient()` per call. -> `mod-pooled-clients-built-once`.
32. https://pkg.go.dev/net/http#Client (org: Google, Go; read: the `Client` docs). `Client` and `Transport` are safe for concurrent use, and `Transport` caches connections, so build one and reuse it. FAIL: yes, a client built in a handler. -> `mod-pooled-clients-built-once`.
33. https://requests.readthedocs.io/en/latest/user/advanced/ (org: Python Requests; read: Session objects, keep-alive). A `Session` pools connections through urllib3, and requests to one host reuse the TCP connection. The connection returns to the pool only after the body is read or the response is closed. FAIL: yes, `requests.get` in a loop. -> `mod-pooled-clients-built-once`.
34. https://nodejs.org/api/http.html#class-httpagent (see row 28). -> `mod-pooled-clients-built-once`.

Notes: 4 orgs (Microsoft, Google/Go, Requests, OpenJS).

### svc-list-endpoint-paginates

35. https://google.aip.dev/158 (org: Google, AIP; read: full). List methods paginate from the start, because adding it later breaks clients. `page_size` is optional with a documented default, and a value above the maximum is coerced down. FAIL: yes, no page size or no cap. -> `svc-list-endpoint-paginates`.
36. https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design (org: Microsoft; read: the pagination section). Use `limit` and `offset` with defaults, and cap the number of items per response to prevent denial of service. FAIL: yes, a client-controlled limit without an upper bound. -> `svc-list-endpoint-paginates`.
37. https://opensource.zalando.com/restful-api-guidelines/ (org: Zalando; read: rule titles and the `limit` parameter; the pagination body was cut off). Collection resources must support pagination, cursor-based is preferred. A hard maximum was not seen on the page. -> `svc-list-endpoint-paginates` (pagination only).
38. https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api (org: GitHub; read: the page). Most endpoints cap `per_page` at 100 and silently lower a larger value. FAIL: yes. -> `svc-list-endpoint-paginates`.
39. https://docs.stripe.com/api/pagination (org: Stripe; read: full). Every list endpoint takes `limit` (1 to 100, default 10) and a cursor, and returns `has_more`. FAIL: yes. -> `svc-list-endpoint-paginates`.

Notes: 5 orgs back pagination (Google, Microsoft, Zalando, GitHub, Stripe) and 4 state a server-side maximum (all but Zalando). A reviewer accepts a clamp or a 400. `svc-api-compat-pagination` keeps the compatibility rule, and `svc-bound-client-controlled-sizes` keeps the security cap.

### chg-new-query-has-plan

40. https://www.postgresql.org/docs/current/using-explain.html (org: PostgreSQL; read: summary). `EXPLAIN` shows the plan tree with estimated costs, and `EXPLAIN ANALYZE` adds actual rows and times. It helps spot a sequential scan where an index would serve. Small tables legitimately scan, so a plan on a tiny dev table does not extrapolate. FAIL: yes, a new query on a growing table with no plan shown. -> `chg-new-query-has-plan`.
41. https://dev.mysql.com/doc/refman/8.4/en/using-explain.html (org: Oracle, MySQL; read: the page). `EXPLAIN` shows whether and where an index helps row lookup, and the join order. FAIL: yes. -> `chg-new-query-has-plan`.
42. https://www.sqlite.org/eqp.html (org: SQLite; read: the page). `EXPLAIN QUERY PLAN` prints `SCAN` (every row) or `SEARCH` (a subset, usually through an index). The output format is not stable between releases. FAIL: yes, a `SCAN` on a large table. -> `chg-new-query-has-plan`.
43. https://use-the-index-luke.com/sql/explain-plan/postgresql/getting-an-execution-plan (org: Markus Winand; read: the page). How to read a plan and compare estimates with actuals. Topic only for "attach the plan to the change".

Notes: 3 orgs (PostgreSQL, Oracle, SQLite) back "the database shows its plan and index use". None says to attach the plan to the change. That step is the card's own practice, stated in `note:`.

### sys-cache-bounds-invalidation (existing card, tag and sources added)

44. https://builder.aws.com/content/3K9TeXp6strMiJ4vhakpRD7BQWO/caching-challenges-and-strategies (org: AWS; read: summary; the older aws.amazon.com/builders-library URL returns a 301 to this one). Size, expiry, and eviction are hard. Choose the TTL from the staleness you tolerate and watch hits, misses, and size. The page does not discuss invalidation. FAIL: yes, a cache with no TTL or size cap. -> `sys-cache-bounds-invalidation`.
45. https://redis.io/docs/latest/develop/reference/eviction/ (org: Redis; read: full). `maxmemory` defaults to unlimited on 64-bit builds, so set it with an eviction policy. `noeviction` makes writes fail instead. FAIL: yes, Redis used as a cache with no limit or policy. -> `sys-cache-bounds-invalidation`.
46. https://github.com/ben-manes/caffeine/wiki/Eviction (org: Caffeine, open source; read: summary). Cap by entry count or weight and expire by access or write time. FAIL: yes, a builder with no `maximumSize` or expiry. -> `sys-cache-bounds-invalidation`.
47. https://www.rfc-editor.org/rfc/rfc9111.html#name-invalidating-stored-response (org: IETF; read: the invalidation section). A cache invalidates the stored response for the target URI after an unsafe request succeeds. HTTP-specific. -> `sys-cache-bounds-invalidation` (invalidation half).

Notes: bounds and expiry have 3 orgs (AWS, Redis, Caffeine). Invalidation has one (IETF, HTTP only), so the card keeps `note:` and the tag is the only change besides the sources.

## 3. Service and system level: deadlines, fan-out, tail latency

### svc-timeouts (existing card, one source added)

48. https://builder.aws.com/content/3EumjoZascWd1oZiEgL8ORlv3qE/timeouts-retries-and-backoff-with-jitter (org: AWS; read: summary; the older aws.amazon.com/builders-library URL returns a 301 to this one). Choose a timeout from the downstream latency percentile that gives an acceptable false-timeout rate, such as p99.9 for 0.1%. Retries multiply across layers (three retries across five layers is about 243 times the load on the bottom service), so retry at one layer. The page calls these judgment calls. FAIL: yes, a timeout literal tied to no measured percentile, or per-try timeout times attempts beyond the caller's deadline. -> `svc-timeouts`.
49. https://grpc.io/docs/guides/deadlines/ (org: Google, gRPC; read: full). gRPC has no default deadline, so a call can hang. Set a realistic deadline and test it under load. The remaining time travels to the next hop. FAIL: yes, an outbound call with no deadline, or a downstream call that ignores the inbound deadline. -> `svc-timeouts`.
50. https://sre.google/sre-book/addressing-cascading-failures/ (org: Google, SRE; read: full). Set deadlines, pass the remaining deadline down the call chain, cap retries, keep queues short relative to the thread pool, and reject early. FAIL: yes. -> `svc-timeouts`, `sys-load-shedding-bounded-queues`.

Notes: no new system card for an end-to-end latency budget. Only Google and AWS state that the deadline passes down the chain. Microsoft, Finagle, and Istio back only bounded retries and per-try timeouts, and Linkerd says nothing on propagation. `svc-timeouts` already carries "derive from the caller's remaining deadline", so this pass refines it with the AWS source and a FAIL example for timeout times attempts. The latency-budget idea does not earn a second card.

### sys-fanout-leg-deadlines

51. https://www.barroso.org/publications/TheTailAtScale.pdf (org: Google; read: full, CACM Feb 2013). Fan-out amplifies rare slowness: with 100 servers that are each slow on 1 request in 100, about 63% of requests hit a slow one. Give sub-requests a strict deadline. Hedge by sending a second request after the first has waited past the 95th-percentile latency, which costs about 5% extra load. Tied requests cancel the twin. Return a good-enough result once enough leaves answered. Naive hedging adds unacceptable load. FAIL: yes, a fan-out that awaits every leg with no per-leg timeout and no partial-result path, or a hedge sent at once to every replica. -> `sys-fanout-leg-deadlines`.
52. https://research.google/pubs/the-tail-at-scale/ (org: Google; read: abstract only). Same paper, abstract page. Not used for any claim beyond row 51.
53. https://grpc.io/docs/guides/request-hedging/ (org: Google, gRPC; read: full). Hedging sends copies to several backends and keeps the first reply. At most 5 attempts, an optional delay between copies, and an overall deadline across copies. Token-based throttling cuts hedges when a budget runs low. Idempotency is not mentioned. FAIL: yes, a hedge with no attempt cap or delay. -> `sys-fanout-leg-deadlines`.
54. https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html (org: Apache Cassandra; read: `speculative_retry`). A read goes to an extra replica when a replica is slower than a percentile or a fixed time (default 99th percentile). The docs advise the default when unsure because extra reads add load. FAIL: yes, `ALWAYS` set with no reason. -> `sys-fanout-leg-deadlines`.
55. https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search (org: Elastic; read: first half). `timeout` bounds the time per shard, and there is no default timeout. `allow_partial_search_results` defaults to true, so a timed-out shard gives a partial result, and false turns it into an error. FAIL: yes, a multi-shard search with no timeout. -> `sys-fanout-leg-deadlines`.
56. https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto (org: Envoy, CNCF; read: the hedge policy section). Hedging starts only when the per-try timeout fires, the original request keeps running, and the first good response wins. It needs a retry policy with a retry count. FAIL: yes, hedging on per-try timeout without a bounded retry policy. -> `sys-fanout-leg-deadlines`.

Notes: 5 orgs back the per-leg deadline and tail handling (Google, AWS through row 48, Apache, Elastic, Envoy/CNCF). A cap on fan-out width has one org (Google), so it is not part of the Rule. Counterpoints: hedging suits idempotent reads, and extra load is the cost.

### sys-load-shedding-bounded-queues (existing stable card, corroboration only)

57. https://sre.google/sre-book/handling-overload/ (org: Google, SRE; read: full). Backends reject the least critical requests first as utilisation rises, clients throttle themselves, and retries stay near 3 attempts and 10% of traffic. -> `sys-load-shedding-bounded-queues`.
58. https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload (org: AWS; read: summary). Reject excess work early, bound queues, and drop requests that waited too long. Rejection costs something, fast failures skew latency metrics, and autoscaling needs testing. -> `sys-load-shedding-bounded-queues`.
59. https://github.com/Netflix/concurrency-limits (org: Netflix; read: README). Fixed limits go stale, so the library estimates a limit at runtime and sheds at once above it. -> `sys-load-shedding-bounded-queues`.
60. https://stripe.com/blog/rate-limiters (org: Stripe; read: summary). A load shedder drops low-priority traffic by system state, and a concurrent-request limiter caps in-flight work per user. -> `sys-load-shedding-bounded-queues`.
61. https://learn.microsoft.com/en-us/azure/architecture/antipatterns/retry-storm/ (org: Microsoft; read: full). Unbounded immediate retries hammer a struggling service. Limit attempts, back off, and honour `Retry-After`. -> `svc-retry-policy`, `sys-load-shedding-bounded-queues`.

Notes: no change to the card in this pass. These rows are for a later stable pass, which already has 5 solid orgs (Google, AWS, Netflix, Stripe, Envoy).

## 4. Codebase, production and incident level

### code-perf-budget-in-ci

62. https://github.com/GoogleChrome/lighthouse-ci/blob/main/docs/getting-started.md (org: Google, Lighthouse CI; read: full). An `assert` block in the config fails the CI build when a threshold is missed, with expected and found values. It warns against asserting on sites with a lot of room to improve. FAIL: yes, Lighthouse CI present with `warn` only or no CI job. -> `code-perf-budget-in-ci`.
63. https://web.dev/articles/performance-budgets-101 (org: Google; read: full). A budget is a limit on a metric, and checks belong in the build. The page does not say the build must fail. Topic plus partial. -> `code-perf-budget-in-ci`.
64. https://github.com/ai/size-limit (org: Size Limit, open source; read: full). Runs in CI on each commit and fails when the bundle cost passes a configured `limit` for size or time. FAIL: yes, a JavaScript bundle with no size check in CI. -> `code-perf-budget-in-ci`.
65. https://webpack.js.org/configuration/performance/ (org: webpack project; read: full). `performance.hints` takes `error`, `warning`, or `false`, and the production default is `warning` with a 250 kB asset limit. The page does not say `error` fails the build, so it is not cited for that. -> topic only.
66. https://grafana.com/docs/k6/latest/using-k6/thresholds/ (org: Grafana Labs, k6; read: full). Thresholds are pass or fail rules on metrics. A miss gives a non-zero exit, so CI halts. FAIL: yes, a load script with no `thresholds`. -> `code-perf-budget-in-ci`, `prod-load-test-before-launch`.
67. https://docs.gatling.io/concepts/assertions/ (org: Gatling; read: full). Assertions can target any response-time percentile, and any failed assertion fails the run. -> `code-perf-budget-in-ci`, `prod-load-test-before-launch`.
68. https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/performance-test (org: Microsoft; read: full). Set targets and acceptance criteria with pass/fail thresholds, run performance tests in the deployment pipeline, compare against a baseline, and test in a production-like environment. -> `code-perf-budget-in-ci`, `prod-load-test-before-launch`.
69. https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/perf_process_culture_load_test.html (org: AWS; read: full). Load test the whole workload on production-like infrastructure. Anti-patterns: testing only parts, testing on different infrastructure, and testing only up to expected load. Automate in the pipeline against KPIs and repeat after changes. FAIL: yes. -> `prod-load-test-before-launch`, `code-perf-budget-in-ci`.
70. https://firefox-source-docs.mozilla.org/testing/perfdocs/perf-sheriffing.html (org: Mozilla; read: full). Perfherder raises an alert when a test crosses its threshold (2% for Talos). Sheriffs triage, bisect, and file a regression bug. Alerts are marked invalid when noisy. FAIL: yes, no automated detection for perf-critical code. -> `code-perf-budget-in-ci`, `inc-perf-regression-guard`.
71. https://pkg.go.dev/golang.org/x/perf/cmd/benchstat (org: Google, Go; read: full). Compares before and after benchmark runs with confidence intervals. It needs 10 to 20 interleaved runs on a quiet machine, and about 5% of unchanged benchmarks can look changed by chance. FAIL: yes, a benchmark gate from a single run. -> `code-perf-budget-in-ci` (caveat).
72. https://github.com/rust-lang/rustc-perf (org: Rust project; read: full). Per-commit benchmarks and a bot that benchmarks PRs on demand. The page does not describe alerting. Topic only.

Notes: 7 orgs back "a CI job fails on a budget or threshold" (Google, Size Limit, Grafana, Gatling, Microsoft, AWS, Mozilla). web.dev and webpack are topic only for the fail step. The card ships the caveat from rows 62 and 71: gate a stable budget, and use repeated runs for benchmarks.

### prod-load-test-before-launch

73. https://sre.google/sre-book/reliable-product-launches/ (org: Google; read: full). Load test before most launches because overload behaviour is hard to predict, and launch traffic can far exceed estimates. Roll out in stages. FAIL: yes, a launch with no load test and no headroom beyond the estimate. -> `prod-load-test-before-launch`.
74. https://grafana.com/docs/k6/latest/testing-guides/test-types/ (org: Grafana Labs; read: full). Load, stress, spike, and soak tests answer different questions, so start with a smoke test. -> `prod-load-test-before-launch` (stress beyond peak).
75. Rows 68 and 69 (Microsoft, AWS) back the pre-launch test on production-like infrastructure and beyond expected load.

Notes: 3 orgs (Google, AWS, Microsoft) back the rule, with Grafana supporting. Counterpoints: Microsoft says to size tests to risk and use a scaled-down environment for non-critical workloads, and AWS rates the risk of skipping low.

### prod-latency-slo-percentile

76. https://sre.google/sre-book/service-level-objectives/ (org: Google; read: full). Averages hide slow outliers. The 99th and 99.9th percentiles show the plausible worst case, and latency SLOs are commonly written on percentiles. FAIL: yes, an SLO or alert written on mean latency. -> `prod-latency-slo-percentile`.
77. https://sre.google/sre-book/monitoring-distributed-systems/ (org: Google; read: full). A mean can look fine while the tail is slow. Use histogram buckets and watch tail percentiles. -> `prod-latency-slo-percentile`, `prod-alerts-symptoms-golden-signals`.
78. https://builder.aws.com/content/3EuxPBdIiiUhB5IK47p3O3fxhy7/instrumenting-distributed-systems-for-operational-visibility (org: AWS; read: full; the older aws.amazon.com/builders-library URL returns a 301 to this one). Amazon watches p99.9 and p99.99 rather than averages, because rare slow requests hurt customers. FAIL: yes, an alarm on average latency. -> `prod-latency-slo-percentile`.
79. https://prometheus.io/docs/practices/histograms/ (org: Prometheus, CNCF; read: full). Histograms aggregate across instances and allow any quantile later. Summaries fix their quantiles and cannot be combined across replicas. Never average pre-computed quantiles. Bucket edges need to suit the objective. FAIL: yes, `avg()` of per-instance quantiles. -> `prod-latency-slo-percentile`.
80. https://opentelemetry.io/docs/specs/otel/metrics/api/ (org: OpenTelemetry, CNCF; read: the Histogram instrument). A histogram instrument is for values whose distribution matters, such as request durations. Topic-level. -> `prod-latency-slo-percentile`.
81. https://qconsf.com/sf2012/dl/qcon-sanfran-2012/slides/GilTene_HowNotToMeasureLatency.pdf (org: Gil Tene, Azul; read: not read, the PDF is over 10 MB; search snippets only). Snippet: a load tool that waits on each response hides slow responses (coordinated omission). Recorded as a counterpoint, not a source.

Notes: 4 orgs back the rule (Google, AWS, Prometheus, and OpenTelemetry at topic level, 3 firm without OpenTelemetry). If a later pass counts CNCF once, Google, AWS, and CNCF still make 3.

### prod-profile-on-demand

82. https://go.dev/doc/diagnostics (org: Google, Go; read: full). `net/http/pprof` exposes CPU, heap, goroutine, block, and mutex profiles. Profiling production works, but a CPU profile adds overhead, so profile one replica at a time. FAIL: yes, a Go service with no profile endpoint and no runbook. -> `prod-profile-on-demand`.
83. https://pkg.go.dev/net/http/pprof (org: Google, Go; read: full). A blank import registers `/debug/pprof/*`, and the example binds to localhost. The page gives no exposure warning. FAIL: yes, the endpoint on a public listener. -> `prod-profile-on-demand` (counter-risk).
84. https://grafana.com/docs/pyroscope/latest/introduction/continuous-profiling/ (org: Grafana Labs; read: full). Continuous profiling keeps profiles from live systems for later review. Sampling overhead is about 2 to 5%. FAIL: yes, no way to get a historical production profile. -> `prod-profile-on-demand`.
85. https://docs.cloud.google.com/profiler/docs/about-profiler (org: Google, Cloud Profiler; read: full; the older cloud.google.com URL returns a 301 to this one). Test environments rarely match production load, so sample in production. Collection overhead stays under 5%. -> `prod-profile-on-demand`.
86. https://research.google/pubs/google-wide-profiling-a-continuous-profiling-infrastructure-for-data-centers/ (org: Google; read: abstract only). Always-on profiling of data-centre software at very low overhead. -> `prod-profile-on-demand`.
87. https://docs.python.org/3/library/profile.html (org: Python; read: full). Recommends a sampling profiler for debugging production, because the pure-Python profiler adds heavy overhead. It does not say to profile before optimising. -> `prod-profile-on-demand`.
88. https://www.brendangregg.com/flamegraphs.html (org: Brendan Gregg, independent; read: full). Flame graphs show sampled stacks. Sampling is used because tracing overhead distorts the result. -> `prod-profile-on-demand`, `inc-perf-fix-has-profile-evidence`.
89. https://docs.oracle.com/en/java/javase/21/jfapi/why-use-jfr-api.html (org: Oracle; read: full). JFR records application, JVM, and OS events. The page does not state low overhead. Topic only.

Notes: 4 orgs (Google, Grafana, Python, Gregg). Counterpoint in the card: profiling has a cost and the endpoint must not face the public network.

### inc-perf-fix-has-profile-evidence

90. https://go.dev/blog/pprof (org: Google, Go; read: full). A worked example: the CPU profile pointed at map lookups, replacing the map with a slice nearly halved the time, the memory profile guided the next step, and each step was measured. FAIL: yes, an optimisation PR with no before-and-after profile. -> `inc-perf-fix-has-profile-evidence`.
91. https://sre.google/sre-book/effective-troubleshooting/ (org: Google; read: full). Test each hypothesis against evidence from metrics and logs. Stabilise first, because a mitigation need not wait for the root cause. -> `inc-perf-fix-has-profile-evidence` (counterpoint: mitigation first).
92. https://www.brendangregg.com/usemethod.html (org: Brendan Gregg; read: full). For each resource, check utilisation, saturation, and errors to find the bottleneck before guessing. FAIL: yes, a fix that cites no resource or profile. -> `inc-perf-fix-has-profile-evidence`.
93. https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/ (org: Cloudflare; read: the remediation section). After a regex CPU outage the team added a CPU safeguard, reviewed the rules, and planned per-rule performance profiling in the test suite. After-the-fact evidence only. -> `inc-perf-regression-guard`.

Notes: only 2 firm orgs (Google, Gregg) back "profile or USE evidence before the fix", and Cloudflare is after-the-fact. The card is a draft with `note:` saying so. It cannot be promoted without a third org.

### inc-perf-regression-guard

94. https://sre.google/sre-book/postmortem-culture/ (org: Google; read: full). A postmortem aims at preventive actions that cut recurrence, and reviewers check the action plan. FAIL: yes, a performance postmortem with no preventive action. -> `inc-perf-regression-guard`.
95. https://web.dev/articles/lighthouse-ci (org: Google; read: full). Each assertion is off, warn, or fail. A fail blocks the build, and the server shows regressions between commits. -> `inc-perf-regression-guard`.
96. Rows 68, 69, 70, and 93 (Microsoft baselines in the pipeline, AWS repeat tests after changes, Mozilla alerts on regressions, Cloudflare per-rule profiling test).
97. https://chromium.googlesource.com/chromium/src/+show/798e59c5275d4131797e8ea2e96e6c6000256b58/docs/benchmark_performance_regressions.md (org: Google, Chromium; read: search snippet only). A detected regression gets a bug, and the patch is reverted if not fixed within a business day. Not fetched, so not cited by any card.

Notes: 5 orgs (Google, Microsoft, AWS, Mozilla, Cloudflare). The card overlaps `inc-postmortem-owned-actions`: that card asks for an owner on every action, and this one names what a performance action looks like.

## 5. Which levels have a new card

- change: `chg-new-query-has-plan`. A claim needs numbers (`chg-perf-claim-evidence`, stable). A query in a loop is `sys-n-plus-one-pooling`. No separate "benchmark for a hot-path change" card: a reviewer cannot tell which paths are hot without a profile, and the regression side is `code-perf-budget-in-ci`.
- function: `fn-join-dont-concat-in-loop`, `fn-regex-compiled-once`, `fn-no-blocking-call-in-async-code`, `fn-fetch-only-needed-data`. `fn-independent-work-concurrent` gets two sources.
- module: no new card, because no checkable rule is left. Cache bounds are `sys-cache-bounds-invalidation`, and client reuse is `mod-pooled-clients-built-once`, which gets sources and the `performance` tag.
- service: `svc-list-endpoint-paginates`. `svc-timeouts` gets one source and a FAIL line. Payload and request size limits are `svc-bound-client-controlled-sizes`. Connection reuse is `mod-pooled-clients-built-once`.
- system: `sys-fanout-leg-deadlines`. `sys-n-plus-one-pooling` and `sys-cache-bounds-invalidation` get sources, and the cache card gets the tag. The per-hop latency budget is no checkable rule beyond `svc-timeouts`, because only 2 orgs state it and `svc-timeouts` already derives the timeout from the caller's remaining deadline.
- codebase: `code-perf-budget-in-ci`. A separate "benchmarks stay runnable" card is no checkable rule on its own, because the budget job runs them, and the sources (Go, Rust, JMH docs) were not read in this pass.
- production: `prod-load-test-before-launch`, `prod-latency-slo-percentile`, `prod-profile-on-demand`. Saturation dashboards are covered by `prod-alerts-symptoms-golden-signals`.
- incident: `inc-perf-fix-has-profile-evidence`, `inc-perf-regression-guard`.

## 6. Read, not used, or not read

- https://learn.microsoft.com/en-us/azure/architecture/antipatterns/synchronous-io/ is used in row 12. The Azure "No Caching" antipattern page was not fetched.
- Not read: the Hibernate fetching chapter, EF Core sub-pages, cacm.acm.org (403), the Netflix Medium post (403), OpenSearch docs, Cloudflare tail-latency posts, the Go and JMH benchmark docs, Guava cache docs, and the Gil Tene PDF.
- Weak points to fix before a stable pass: a third org for `fn-independent-work-concurrent`, a third org for `inc-perf-fix-has-profile-evidence`, and an invalidation source other than RFC 9111 for `sys-cache-bounds-invalidation`.

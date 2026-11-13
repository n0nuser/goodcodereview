# performance cards

Every stable card that lists the `performance` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-perf-claim-evidence` [should-fix] {performance, testing} change.md:L432+25: Back a performance claim with measured before-and-after numbers.

## function

- `fn-fetch-only-needed-data` [should-fix] {performance} <data> function.md:L457+29: Filter, count, and aggregate in the query, and select only the columns the code uses.
- `fn-independent-work-concurrent` [should-fix] {performance, correctness} function.md:L712+27: Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.
- `fn-join-dont-concat-in-loop` [should-fix] {performance} function.md:L740+27: Build a string from a loop with a builder or a join, never with repeated `+=`.
- `fn-no-blocking-call-in-async-code` [block] {performance, correctness} function.md:L1026+29: Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.
- `fn-regex-compiled-once` [should-fix] {performance} function.md:L1539+29: Compile a regular expression once, at module or startup level, and reuse it.

## module

- `mod-pooled-clients-built-once` [should-fix] {performance} module.md:L544+29: Build pooled clients once at startup and reuse them.
- `py-httpx-client-lifespan` [should-fix] {performance} module.md:L746+30: Pass an explicit `httpx.Timeout` to every `httpx` client.
- `py-pytest-expensive-fixture-scope` [should-fix] {testing, performance} module.md:L829+49: Give an expensive pytest fixture `scope="session"` or `"module"` and isolate each test with a rollback, never a schema build or a seed load inside a function-scoped fixture.

## service

- `svc-api-cache-control` [should-fix] {performance, security} <server> service.md:L37+35: Set an explicit `Cache-Control` on every response a cache may store, use `private` or `no-store` for user-specific data, add `Vary` for any request header that changes the body, keep the origin's `Cache-Control` authoritative at the edge (no minimum TTL or force-cache override), and decide cacheability by the response `Content-Type`, not the URL extension.
- `svc-async-content-reserves-space` [should-fix] {usability, performance} <ui> service.md:L414+28: Reserve the space for late-loading content with set dimensions or an aspect ratio, so nothing already on screen moves.
- `svc-decompression-cap` [should-fix] {security, performance} <server> service.md:L920+28: Cap the decompressed output of every decoder, and set the cap on the output rather than the compressed input.
- `svc-list-endpoint-paginates` [should-fix] {performance} <server> service.md:L1186+28: Paginate every list endpoint, with a default page size and a server-side maximum.
- `svc-stream-dont-materialise` [should-fix] {performance} service.md:L1715+29: Process large results as a stream with backpressure; do not load them whole into memory.
- `svc-timeouts` [block] {performance, reliability} service.md:L1774+30: Set an explicit timeout on every remote call.

## system

- `sys-cache-bounds-invalidation` [should-fix] {performance} system.md:L30+26: Bound every cache by size and give its entries an expiry.
- `sys-fanout-leg-deadlines` [should-fix] {performance, reliability} system.md:L120+28: Give every leg of a fan-out its own deadline, and decide in code what happens when a leg misses it: a partial result, a hedged request, or an error.
- `sys-n-plus-one-pooling` [should-fix] {performance} <data> system.md:L318+28: Fetch related rows in one query or batch, never one query per row.

## codebase

- `code-perf-budget-in-ci` [should-fix] {performance, process} codebase.md:L333+27: Write the performance budget down as a CI check that fails the build when it is exceeded.
- `code-test-fixtures-built-once` [should-fix] {testing, performance} codebase.md:L497+32: Build an expensive fixture once per test run, and reset state between tests with a rollback or a truncate, never a rebuild.
- `code-test-selection-on-pr` [discuss] {testing, performance, process} codebase.md:L530+49: When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.

## production

- `prod-latency-slo-percentile` [should-fix] {performance, observability} production.md:L119+27: Define latency SLOs and alerts on high percentiles, never on the mean.
- `prod-load-test-before-launch` [should-fix] {performance, reliability} production.md:L147+27: Load test before launch, past the expected peak, with pass and fail thresholds written down.
- `prod-profile-on-demand` [discuss] {performance, observability} production.md:L175+26: Make a CPU and memory profile of a production instance obtainable, through a continuous profiler or a private profile endpoint.

## incident

- `inc-perf-fix-has-profile-evidence` [should-fix] {performance, testing} incident.md:L3+26: Tie the performance fix to evidence that names the bottleneck: a profile, a trace, or a USE check.

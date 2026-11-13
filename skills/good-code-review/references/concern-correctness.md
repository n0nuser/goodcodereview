# correctness cards

Every stable card that lists the `correctness` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-match-codebase-pattern` [should-fix] {correctness, maintainability} change.md:L258+29: Follow the established pattern nearby.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} change.md:L344+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.

## function

- `fn-bounded-read-fails-at-cap` [should-fix] {correctness, reliability, security} function.md:L60+36: When a size cap is reached, return an error; never hand back the first N bytes as if they were the whole input.
- `fn-distinct-types-for-ids` [should-fix] {correctness} function.md:L371+28: Give arguments with different meanings distinct types, so a call that swaps them fails to type-check.
- `fn-guard-uri-decoding` [should-fix] {reliability, correctness} <ui,server> function.md:L547+32: Wrap `decodeURIComponent` on user input in a `try`/`catch`, or parse with `URLSearchParams`, so that a malformed `%` sequence cannot throw.
- `fn-handle-rejected-promises` [should-fix] {reliability, correctness} function.md:L580+35: Handle the rejection of every promise you start: `await` it inside `try`/`catch`, end the chain with `.catch()`, or return it to a caller that does.
- `fn-independent-work-concurrent` [should-fix] {performance, correctness} function.md:L712+27: Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.
- `fn-no-blocking-call-in-async-code` [block] {performance, correctness} function.md:L1026+29: Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.
- `fn-no-caller-mutation` [should-fix] {correctness, testing} function.md:L1056+34: Do not mutate a parameter or an object the caller owns, unless the function is documented as mutating it.
- `fn-no-check-then-act-across-await` [should-fix] {correctness} function.md:L1091+28: Make check-and-write one atomic operation where the state lives, and never split it across a suspension point.
- `fn-specific-exceptions-only` [should-fix] {correctness} function.md:L1665+31: Catch only the specific exception you can handle in business code.
- `fn-test-oracle-independent` [should-fix] {correctness, testing} function.md:L1795+25: Take a test's expected value from the requirement, not from the code under test.
- `py-modern-typing` [should-fix] {correctness} function.md:L1942+26: Write `X | None` and builtin generics, not `typing` aliases.
- `py-no-cast` [should-fix] {correctness} function.md:L1969+27: Do not use `cast()`; parse the boundary into a typed model, or narrow with `isinstance`.
- `py-paths-from-file` [should-fix] {correctness} function.md:L1997+24: Resolve paths from `__file__`, not the current working directory.

## module

- `mod-no-logic-in-constructors` [should-fix] {correctness, testing} module.md:L371+29: Assign only in constructors, and put I/O, parsing, and heavy computation in a named factory.
- `mod-no-module-mutable-state` [should-fix] {correctness, testing} module.md:L401+36: Keep no mutable state at module level; hold it on an instance.
- `mod-single-writer-per-state` [should-fix] {correctness} module.md:L607+25: Let only one writer change a piece of state at a time, through a single owner, a queue that serialises the writes, or compare-and-swap, never by convention.
- `py-field-only-when-adds` [discuss] {correctness} module.md:L720+25: Use `Field()` only when it adds something (a constraint, an alias, or API docs), and set plain defaults directly.

## service

- `svc-api-conditional-writes` [should-fix] {correctness} <server> service.md:L73+29: Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.
- `svc-api-documented-errors` [should-fix] {correctness, compatibility} <server> service.md:L164+34: Document every error status each operation can return, with a schema and one example.
- `svc-bounded-background-tasks` [block] {reliability, correctness} service.md:L601+36: Cap how many background tasks run at once, and never spawn one per input with no limit.
- `svc-cli-exit-codes-and-streams` [should-fix] {correctness, maintainability} <cli> service.md:L756+32: Exit non-zero when a command fails, and write results to stdout and errors and progress to stderr.
- `svc-idempotency-key` [block] {reliability, correctness} <server> service.md:L1107+29: Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.
- `svc-invalid-input-is-4xx` [should-fix] {correctness, reliability} <server> service.md:L1137+48: Check each caller-supplied value against its allowed domain (range, allowed set, an id that must exist, an encoding the code can handle) at the boundary, and answer a failed check with a 4xx, never a 5xx.
- `svc-saga-steps` [should-fix] {reliability, correctness} <server> service.md:L1528+27: Make steps after the pivot idempotent and retryable, and make every compensation idempotent with a failure path.
- `svc-soft-delete-default` [should-fix] {security, correctness} <data> service.md:L1655+30: Filter soft-deleted rows out of every read path by default, and make a read that includes them an explicit call.
- `py-cancellation` [should-fix] {reliability, correctness} service.md:L2010+32: Re-raise `CancelledError` (do not catch it via bare `except` or `BaseException`), and catch `TimeoutError` outside the `asyncio.timeout()` block.
- `py-task-reference` [should-fix] {correctness} service.md:L2043+29: Never discard the result of `create_task`; keep a reference and surface its exceptions, preferably through a `TaskGroup`.

## system

- `sys-lock-fencing` [block] {reliability, correctness} system.md:L233+29: Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.
- `sys-secrets-and-errors` [block] {security, correctness} system.md:L401+30: Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.

## codebase

- `code-consistency-drift` [discuss] {correctness, maintainability} codebase.md:L116+27: For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.

## production

- `prod-shadow-compare-before-cutover` [should-fix] {correctness, reliability} <data> production.md:L202+35: Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.

# correctness cards

Every stable card that lists the `correctness` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-applied-migration-not-edited` [should-fix] {correctness, process} <data> change.md:L58+38: Do not edit or delete a migration that has already run in a shared environment; add a new migration that makes the change.
- `chg-match-codebase-pattern` [should-fix] {correctness, maintainability} change.md:L611+29: Follow the established pattern nearby.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} change.md:L765+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.

## function

- `fn-bounded-read-fails-at-cap` [should-fix] {correctness, reliability, security} function.md:L60+36: When a size cap is reached, return an error; never hand back the first N bytes as if they were the whole input.
- `fn-distinct-types-for-ids` [should-fix] {correctness} function.md:L435+28: Give arguments with different meanings distinct types, so a call that swaps them fails to type-check.
- `fn-doc-params-match-signature` [discuss] {maintainability, correctness} function.md:L498+37: Make the parameters a doc comment lists match the function's signature, by name and in number.
- `fn-explicit-locale-for-case-change` [should-fix] {correctness} function.md:L782+32: Change the case of a machine-read string with an explicit root or invariant locale, never the default one.
- `fn-flags-type-for-flag-sets` [should-fix] {maintainability, correctness} function.md:L845+32: Model a set of independent flags with the language's or ecosystem's flags type (a `[Flags]` enum in C#, the `bitflags` crate in Rust, `EnumSet` in Java), and do not use a plain enum for it.
- `fn-guard-uri-decoding` [should-fix] {reliability, correctness} <ui,server> function.md:L938+32: Wrap `decodeURIComponent` on user input in a `try`/`catch`, or parse with `URLSearchParams`, so that a malformed `%` sequence cannot throw.
- `fn-handle-rejected-promises` [should-fix] {reliability, correctness} function.md:L971+35: Handle the rejection of every promise you start: `await` it inside `try`/`catch`, end the chain with `.catch()`, or return it to a caller that does.
- `fn-honour-cancellation` [should-fix] {reliability, correctness} function.md:L1071+53: Take a cancellation signal in long-running work and check it between steps; when a handler catches a cancellation, finish the cleanup and re-raise it.
- `fn-independent-work-concurrent` [should-fix] {performance, correctness} function.md:L1157+27: Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.
- `fn-monotonic-clock-for-durations` [should-fix] {correctness, reliability} function.md:L1444+30: Measure elapsed time and timeouts with a monotonic clock, never by subtracting wall-clock readings.
- `fn-no-blocking-call-in-async-code` [block] {performance, correctness} function.md:L1604+29: Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.
- `fn-no-caller-mutation` [should-fix] {correctness, testing} function.md:L1634+34: Do not mutate a parameter or an object the caller owns, unless the function is documented as mutating it.
- `fn-no-check-then-act-across-await` [should-fix] {correctness} function.md:L1669+28: Make check-and-write one atomic operation where the state lives, and never split it across a suspension point.
- `fn-resource-lifetime` [should-fix] {correctness} function.md:L2313+29: Give every task and handle an owner that waits for it or closes it, on the error path too.
- `fn-side-effects-after-commit` [should-fix] {correctness, reliability} <data> function.md:L2372+46: Start side effects only after the transaction commits, with an `on_commit` or `after_commit` hook, or record them as an outbox row written inside the same transaction.
- `fn-specific-exceptions-only` [should-fix] {correctness} function.md:L2419+31: Catch only the specific exception you can handle in business code.
- `fn-test-oracle-independent` [should-fix] {correctness, testing} function.md:L2549+25: Take a test's expected value from the requirement, not from the code under test.
- `fn-timestamps-stored-in-utc` [should-fix] {correctness} function.md:L2575+32: Store and send instants in UTC.
- `py-modern-typing` [should-fix] {correctness} function.md:L2756+26: Write `X | None` and builtin generics, not `typing` aliases.
- `py-no-cast` [should-fix] {correctness} function.md:L2783+27: Do not use `cast()`; parse the boundary into a typed model, or narrow with `isinstance`.
- `py-paths-from-file` [should-fix] {correctness} function.md:L2811+24: Resolve paths from `__file__`, not the current working directory.

## module

- `mod-no-logic-in-constructors` [should-fix] {correctness, testing} module.md:L371+29: Assign only in constructors, and put I/O, parsing, and heavy computation in a named factory.
- `mod-no-module-mutable-state` [should-fix] {correctness, testing} module.md:L401+36: Keep no mutable state at module level; hold it on an instance.
- `mod-single-writer-per-state` [should-fix] {correctness} module.md:L607+25: Let only one writer change a piece of state at a time, through a single owner, a queue that serialises the writes, or compare-and-swap, never by convention.
- `py-field-only-when-adds` [discuss] {correctness} module.md:L752+25: Use `Field()` only when it adds something (a constraint, an alias, or API docs), and set plain defaults directly.

## service

- `svc-api-conditional-writes` [should-fix] {correctness} <server> service.md:L73+29: Return an `ETag` on reads and honour `If-Match` on writes, answering 412 when the entity tag is stale.
- `svc-api-documented-errors` [should-fix] {correctness, compatibility} <server> service.md:L165+34: Document every error status each operation can return, with a schema and one example.
- `svc-bounded-background-tasks` [block] {reliability, correctness} service.md:L674+36: Cap how many background tasks run at once, and never spawn one per input with no limit.
- `svc-cli-exit-codes-and-streams` [should-fix] {correctness, maintainability} <cli> service.md:L829+32: Exit non-zero when a command fails, and write results to stdout and errors and progress to stderr.
- `svc-idempotency-key` [block] {reliability, correctness} <server> service.md:L1310+29: Make every retryable write idempotent: the caller sends a unique key, and a retry with the same key never applies the write twice.
- `svc-invalid-input-is-4xx` [should-fix] {correctness, reliability} <server> service.md:L1340+48: Check each caller-supplied value against its allowed domain (range, allowed set, an id that must exist, an encoding the code can handle) at the boundary, and answer a failed check with a 4xx, never a 5xx.
- `svc-saga-steps` [should-fix] {reliability, correctness} <server> service.md:L1822+27: Make steps after the pivot idempotent and retryable, and make every compensation idempotent with a failure path.
- `svc-soft-delete-default` [should-fix] {security, correctness} <data> service.md:L1949+30: Filter soft-deleted rows out of every read path by default, and make a read that includes them an explicit call.
- `svc-tenant-scope-in-data-layer` [should-fix] {security, correctness} <data> service.md:L2068+37: Enforce tenant scope in the data layer by default, with a query filter or row-level security, not by a predicate at each call site.
- `py-cancellation` [should-fix] {reliability, correctness} service.md:L2380+32: Re-raise `CancelledError` (do not catch it via bare `except` or `BaseException`), and catch `TimeoutError` outside the `asyncio.timeout()` block.
- `py-task-reference` [should-fix] {correctness} service.md:L2413+29: Never discard the result of `create_task`; keep a reference and surface its exceptions, preferably through a `TaskGroup`.

## system

- `sys-lock-fencing` [block] {reliability, correctness} system.md:L270+29: Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.
- `sys-secrets-and-errors` [block] {security, correctness} system.md:L438+30: Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.

## codebase

- `code-consistency-drift` [discuss] {correctness, maintainability} codebase.md:L146+27: For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.

## production

- `prod-shadow-compare-before-cutover` [should-fix] {correctness, reliability} <data> production.md:L291+36: Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.

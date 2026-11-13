# testing cards

Every stable card that lists the `testing` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-perf-claim-evidence` [should-fix] {performance, testing} change.md:L432+25: Back a performance claim with measured before-and-after numbers.
- `chg-refactor-has-behaviour-pin` [should-fix] {testing, maintainability} change.md:L523+26: Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.
- `chg-tests-ship-with-change` [block] {testing} change.md:L688+27: Ship new or changed behaviour in the same change as a test that fails if the behaviour breaks.
- `chg-verify-before-claim` [block] {testing, process} change.md:L748+26: Back every "works" or "bug" claim with something run: a repro, a test or command output.

## function

- `fn-no-caller-mutation` [should-fix] {correctness, testing} function.md:L1056+34: Do not mutate a parameter or an object the caller owns, unless the function is documented as mutating it.
- `fn-test-behaviour-not-implementation` [should-fix] {testing, maintainability} function.md:L1760+34: Assert what a caller can observe through the public interface, so a change that keeps behaviour does not break the test.
- `fn-test-oracle-independent` [should-fix] {correctness, testing} function.md:L1795+25: Take a test's expected value from the requirement, not from the code under test.
- `py-pytest-parametrize` [should-fix] {testing} function.md:L2022+28: Write tests that differ only in inputs and expected values as one `@pytest.mark.parametrize` test.

## module

- `mod-inject-boundary-collaborators` [should-fix] {testing, maintainability} module.md:L206+26: Inject boundary collaborators through the constructor; do not construct them inside or reach for a global.
- `mod-no-import-side-effects` [should-fix] {testing, maintainability} module.md:L344+26: Keep I/O at the edges: importing a package must not touch the network, read files, or read the environment.
- `mod-no-logic-in-constructors` [should-fix] {correctness, testing} module.md:L371+29: Assign only in constructors, and put I/O, parsing, and heavy computation in a named factory.
- `mod-no-module-mutable-state` [should-fix] {correctness, testing} module.md:L401+36: Keep no mutable state at module level; hold it on an instance.
- `py-no-init-or-model-tests` [should-fix] {testing} module.md:L804+24: Cover `__init__` and plain models through the behaviour that uses them.
- `py-pytest-expensive-fixture-scope` [should-fix] {testing, performance} module.md:L829+49: Give an expensive pytest fixture `scope="session"` or `"module"` and isolate each test with a rollback, never a schema build or a seed load inside a function-scoped fixture.
- `py-test-hygiene` [discuss] {testing, reliability} module.md:L879+33: Keep unit tests off external I/O (the network, the shared filesystem and the database) and off the real clock, and run tests that need them in a separate, slower tier.
- `py-xdist-worker-isolated-state` [should-fix] {testing, reliability} module.md:L913+32: Under pytest-xdist, give each worker its own database or other mutable resource, keyed by `worker_id`, and build an expensive shared one once with a lock file.

## service

- `svc-api-contract-tests` [should-fix] {compatibility, testing} <server> service.md:L103+28: Run a contract test for each cross-service call, derived from the consumer's real requests, and fail the provider's build when it breaks one.

## codebase

- `code-a11y-check-in-ci` [should-fix] {accessibility, testing} <ui> codebase.md:L3+30: Run an automated accessibility check, such as axe on rendered pages, in the automated tests, and fail the test on a violation.
- `code-flaky-test-quarantine` [should-fix] {testing, process} codebase.md:L303+29: Report every test that passes only on retry, move it to a quarantine with a named owner and a ticket, and return it to the merge gate only after it passes many reruns.
- `code-scoped-validation-loop` [discuss] {testing, process} codebase.md:L443+26: Document a command that checks one package or path, with readable output, so a small change does not need the full-repo run.
- `code-test-fixtures-built-once` [should-fix] {testing, performance} codebase.md:L497+32: Build an expensive fixture once per test run, and reset state between tests with a rollback or a truncate, never a rebuild.
- `code-test-selection-on-pr` [discuss] {testing, performance, process} codebase.md:L530+49: When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.

## incident

- `inc-perf-fix-has-profile-evidence` [should-fix] {performance, testing} incident.md:L3+26: Tie the performance fix to evidence that names the bottleneck: a profile, a trace, or a USE check.

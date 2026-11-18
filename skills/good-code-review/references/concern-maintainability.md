# maintainability cards

Every stable card that lists the `maintainability` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-agent-grounded-code` [should-fix] {maintainability, process} change.md:L3+28: Verify that every import and external call the agent wrote exists with that signature.
- `chg-chestertons-fence` [should-fix] {maintainability, process} change.md:L142+26: Add a characterization test before rewriting code you do not understand.
- `chg-delete-legacy-after-migration` [should-fix] {compatibility, maintainability} <data> change.md:L169+30: When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.
- `chg-match-codebase-pattern` [should-fix] {correctness, maintainability} change.md:L258+29: Follow the established pattern nearby.
- `chg-no-per-user-ide-files` [should-fix] {process, maintainability} change.md:L344+37: Do not commit a file that holds one developer's editor or IDE state; ignore those paths in the repository or a machine-wide exclude file. An ignore entry does not untrack a file already committed: remove it from the index with `git rm --cached`.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} change.md:L382+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.
- `chg-no-special-case-branches` [should-fix] {maintainability} change.md:L413+29: Put a new case behind its own function or type; do not add a one-off branch to a shared flow.
- `chg-refactor-has-behaviour-pin` [should-fix] {testing, maintainability} change.md:L561+26: Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.
- `chg-refactor-separate` [should-fix] {maintainability, process} change.md:L588+27: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-reuse-before-write` [should-fix] {maintainability} change.md:L616+27: Do not add a helper that duplicates one already in the repo; search for it first.

## function

- `fn-bool-arg-at-callsite` [discuss] {maintainability} function.md:L34+25: Replace a boolean flag argument with an enum, keyword-only argument or two functions.
- `fn-comments-explain-why` [should-fix] {maintainability} function.md:L128+27: Write comments that give a reason, a constraint, or a trade-off, and never restate what the next line does.
- `fn-comments-survive-context` [should-fix] {maintainability} function.md:L156+25: Write comments that remain true without outside context: no "currently", "for now" or "see the PR", and give a TODO the date or event that ends it.
- `fn-complexity-cap` [discuss] {maintainability, testing} function.md:L182+37: Set a cyclomatic complexity limit in the linter and keep every function under it.
- `fn-early-return-no-else` [discuss] {maintainability} function.md:L438+37: Handle the error or edge case first and return early, so the main path is not nested.
- `fn-english-identifiers` [discuss] {maintainability} function.md:L476+25: Write identifiers and comments in English, unless the project policy names another language.
- `fn-length-budget` [discuss] {maintainability} function.md:L941+38: Split a function that passes the project's length limit (about 40 lines if it sets none) unless its body is one simple operation or one flat dispatch.
- `fn-name-intermediate-conditions` [discuss] {maintainability} function.md:L1044+26: Name each compound condition by assigning its sub-conditions to booleans that say what they mean.
- `fn-nesting-depth-cap` [discuss] {maintainability} function.md:L1102+37: Keep control-flow nesting shallow.
- `fn-no-getattr-for-known-names` [discuss] {maintainability} function.md:L1262+25: Use plain field access, and reserve dynamic access for genuinely dynamic names.
- `fn-no-magic-values` [should-fix] {maintainability} function.md:L1288+27: Give every meaningful literal a name: an enum member or a constant.
- `fn-parameter-limit` [should-fix] {maintainability} function.md:L1530+29: Set a parameter-count limit in the project's linter, and keep signatures within it.
- `fn-test-behaviour-not-implementation` [should-fix] {testing, maintainability} function.md:L1909+34: Assert what a caller can observe through the public interface, so a change that keeps behaviour does not break the test.
- `fn-variants-as-tagged-union` [should-fix] {maintainability} function.md:L1998+37: Model variants as a tagged union, and make every switch over it fail the build when a variant is unhandled.
- `py-docstrings-google` [discuss] {maintainability} function.md:L2064+27: Write a Google-style docstring only when it adds what the signature cannot say.

## module

- `mod-behaviour-lives-with-state` [discuss] {maintainability} module.md:L3+25: Put the invariants and calculations that read only one object's fields on that object.
- `mod-bounded-fan-out` [discuss] {maintainability} module.md:L29+26: Set a limit on how many other types or modules one unit depends on, and split a unit that passes it.
- `mod-class-size-budget` [discuss] {maintainability} module.md:L56+31: Split a class that passes the project's size limit for fields, public methods or lines, unless it is a data record.
- `mod-deep-modules` [discuss] {maintainability} module.md:L127+26: Prefer a small interface that hides its implementation, and add a member only when callers need it.
- `mod-derive-dont-duplicate` [should-fix] {compatibility, maintainability} module.md:L154+26: Derive a type, list or enum from the schema or list that owns it, or add a build check that fails when the two disagree.
- `mod-fowler-smells` [discuss] {maintainability} module.md:L181+24: Name the smell, point to the line, and suggest the refactoring; do not file smells as taste.
- `mod-inject-boundary-collaborators` [should-fix] {testing, maintainability} module.md:L206+26: Inject boundary collaborators through the constructor; do not construct them inside or reach for a global.
- `mod-internals-unreachable` [should-fix] {maintainability} module.md:L233+27: Keep a module's internals unimportable and untouched from outside it. A caller uses the public surface, not a private file or member.
- `mod-law-of-demeter` [discuss] {maintainability} module.md:L261+25: Call methods on your direct collaborators, and do not call a method on an object that another call returned (a chain of two or more getters).
- `mod-layers-point-inward` [should-fix] {maintainability} module.md:L287+27: Make dependencies point inward: surface, then logic, then boundary.
- `mod-no-import-cycles` [should-fix] {maintainability} module.md:L315+28: Keep the dependency graph between modules or packages acyclic, and break a cycle by moving the shared part into a third module that both depend on.
- `mod-no-import-side-effects` [should-fix] {testing, maintainability} module.md:L344+26: Keep I/O at the edges: importing a package must not touch the network, read files, or read the environment.
- `mod-no-shotgun-surgery` [discuss] {maintainability} module.md:L438+25: Keep one decision in one module, and when a single change needs edits in many classes, move the scattered parts together.
- `mod-no-utils-grab-bag` [should-fix] {maintainability} module.md:L464+24: Put a helper in the module that owns the concept, or in a new module named after the concept.
- `mod-no-wrong-abstraction` [should-fix] {maintainability} module.md:L489+25: Inline an abstraction that has grown flags for its callers.
- `mod-one-name-per-concept` [should-fix] {maintainability} module.md:L515+28: Use one name for one concept across the codebase.
- `mod-temporary-field` [discuss] {maintainability} module.md:L633+31: Make a field a local variable or a parameter when every method that uses it assigns it before reading it.
- `mod-yagni` [should-fix] {maintainability, process} module.md:L693+25: Do not build an abstraction or capability for a need that does not exist yet; add it when the need appears.
- `py-class-earns-its-instance` [discuss] {maintainability} module.md:L719+32: Give a class real state or a collaborator; otherwise write a module function.
- `py-imports` [should-fix] {maintainability} module.md:L809+26: Put imports at module top, absolute only.

## service

- `svc-api-naming-consistent` [discuss] {maintainability} <server> service.md:L261+27: Use one casing convention per location (fields, query parameters, headers, paths) across the whole API, and state it in the API guide. Name collections and array fields as plural nouns.
- `svc-api-version-on-every-request` [should-fix] {compatibility, maintainability} <server> service.md:L385+28: Name the API version on every request, in a header or a query parameter.
- `svc-cli-destructive-dry-run` [should-fix] {reliability, maintainability} <cli> service.md:L776+52: Give a destructive command a preview flag that changes nothing and a flag that skips the confirmation prompt.
- `svc-cli-exit-codes-and-streams` [should-fix] {correctness, maintainability} <cli> service.md:L829+32: Exit non-zero when a command fails, and write results to stdout and errors and progress to stderr.
- `svc-cli-non-interactive` [should-fix] {maintainability, process} <cli> service.md:L862+41: Let the caller turn every prompt off with a flag or an environment variable, so the command never waits on a terminal.

## codebase

- `code-adr` [discuss] {maintainability, process} codebase.md:L34+24: Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, the options ruled out, and its consequences.
- `code-consistency-drift` [discuss] {correctness, maintainability} codebase.md:L146+27: For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.
- `code-dead-code` [should-fix] {maintainability} codebase.md:L174+31: Delete unreferenced functions and variables, unreachable code, commented-out code, and expired feature flags with their branches and configuration.
- `code-docs-refs-resolve` [should-fix] {maintainability} codebase.md:L276+31: Run a link check in CI over the docs, so that every relative link and anchor they cite resolves.
- `code-file-lines-ceiling` [discuss] {maintainability, process} codebase.md:L308+27: Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.
- `code-rule-has-enforcer` [should-fix] {maintainability} codebase.md:L442+33: Back each written repo rule that a type, lint or CI check could enforce with that check, not with a line in an instruction file or a repeated review comment.
- `py-ruff-gate` [should-fix] {maintainability} codebase.md:L813+32: Enable the Ruff rule sets E, F, I, B, UP, SIM, BLE, TID and D in CI.

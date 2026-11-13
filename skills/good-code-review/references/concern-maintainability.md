# maintainability cards

Every stable card that lists the `maintainability` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-agent-grounded-code` [should-fix] {maintainability, process} change.md:L3+28: Verify that every import and external call the agent wrote exists with that signature.
- `chg-chestertons-fence` [should-fix] {maintainability, process} change.md:L142+26: Add a characterization test before rewriting code you do not understand.
- `chg-delete-legacy-after-migration` [should-fix] {compatibility, maintainability} <data> change.md:L169+30: When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.
- `chg-match-codebase-pattern` [should-fix] {correctness, maintainability} change.md:L258+29: Follow the established pattern nearby.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} change.md:L344+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.
- `chg-no-special-case-branches` [should-fix] {maintainability} change.md:L375+29: Put a new case behind its own function or type; do not add a one-off branch to a shared flow.
- `chg-refactor-has-behaviour-pin` [should-fix] {testing, maintainability} change.md:L523+26: Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.
- `chg-refactor-separate` [should-fix] {maintainability, process} change.md:L550+27: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-reuse-before-write` [should-fix] {maintainability} change.md:L578+27: Do not add a helper that duplicates one already in the repo; search for it first.

## function

- `fn-bool-arg-at-callsite` [discuss] {maintainability} function.md:L34+25: Replace a boolean flag argument with an enum, keyword-only argument or two functions.
- `fn-comments-explain-why` [should-fix] {maintainability} function.md:L128+27: Write comments that give a reason, a constraint, or a trade-off, and never restate what the next line does.
- `fn-comments-survive-context` [should-fix] {maintainability} function.md:L156+25: Write comments that remain true without outside context: no "currently", "for now" or "see the PR", and give a TODO the date or event that ends it.
- `fn-english-identifiers` [discuss] {maintainability} function.md:L400+25: Write identifiers and comments in English, unless the project policy names another language.
- `fn-length-budget` [discuss] {maintainability} function.md:L865+38: Split a function that passes the project's length limit (about 40 lines if it sets none) unless its body is one simple operation or one flat dispatch.
- `fn-name-intermediate-conditions` [discuss] {maintainability} function.md:L968+26: Name each compound condition by assigning its sub-conditions to booleans that say what they mean.
- `fn-no-getattr-for-known-names` [discuss] {maintainability} function.md:L1148+25: Use plain field access, and reserve dynamic access for genuinely dynamic names.
- `fn-no-magic-values` [should-fix] {maintainability} function.md:L1174+27: Give every meaningful literal a name: an enum member or a constant.
- `fn-parameter-limit` [should-fix] {maintainability} function.md:L1416+29: Set a parameter-count limit in the project's linter, and keep signatures within it.
- `fn-test-behaviour-not-implementation` [should-fix] {testing, maintainability} function.md:L1760+34: Assert what a caller can observe through the public interface, so a change that keeps behaviour does not break the test.
- `fn-variants-as-tagged-union` [should-fix] {maintainability} function.md:L1848+37: Model variants as a tagged union, and make every switch over it fail the build when a variant is unhandled.
- `py-docstrings-google` [discuss] {maintainability} function.md:L1914+27: Write a Google-style docstring only when it adds what the signature cannot say.

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
- `mod-yagni` [should-fix] {maintainability, process} module.md:L661+25: Do not build an abstraction or capability for a need that does not exist yet; add it when the need or a second use appears.
- `py-class-earns-its-instance` [discuss] {maintainability} module.md:L687+32: Give a class real state or a collaborator; otherwise write a module function.
- `py-imports` [should-fix] {maintainability} module.md:L777+26: Put imports at module top, absolute only.

## service

- `svc-api-naming-consistent` [discuss] {maintainability} <server> service.md:L260+27: Use one casing convention per location (fields, query parameters, headers, paths) across the whole API, and state it in the API guide.
- `svc-cli-destructive-dry-run` [should-fix] {reliability, maintainability} <cli> service.md:L703+52: Give a destructive command a preview flag that changes nothing and a flag that skips the confirmation prompt.
- `svc-cli-exit-codes-and-streams` [should-fix] {correctness, maintainability} <cli> service.md:L756+32: Exit non-zero when a command fails, and write results to stdout and errors and progress to stderr.
- `svc-cli-non-interactive` [should-fix] {maintainability, process} <cli> service.md:L789+41: Let the caller turn every prompt off with a flag or an environment variable, so the command never waits on a terminal.

## codebase

- `code-adr` [discuss] {maintainability, process} codebase.md:L34+24: Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, and its consequences.
- `code-consistency-drift` [discuss] {correctness, maintainability} codebase.md:L116+27: For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.
- `code-dead-code` [should-fix] {maintainability} codebase.md:L144+28: Delete unreferenced functions and variables, and the branches of expired feature flags.
- `code-docs-refs-resolve` [should-fix] {maintainability} codebase.md:L243+31: Run a link check in CI over the docs, so that every relative link and anchor they cite resolves.
- `code-file-lines-ceiling` [discuss] {maintainability, process} codebase.md:L275+27: Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.
- `code-rule-has-enforcer` [should-fix] {maintainability} codebase.md:L409+33: Back each written repo rule that a type, lint or CI check could enforce with that check, not with a line in an instruction file or a repeated review comment.
- `py-ruff-gate` [should-fix] {maintainability} codebase.md:L702+32: Enable the Ruff rule sets E, F, I, B, UP, SIM, BLE, TID and D in CI.

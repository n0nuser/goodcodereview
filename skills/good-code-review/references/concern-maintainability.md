# maintainability cards

Every stable card that lists the `maintainability` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-agent-grounded-code` [should-fix] {maintainability, process} change.md:L3+28: Verify that every import and external call the agent wrote exists with that signature.
- `chg-changelog-entry` [discuss] {maintainability, process} change.md:L142+27: Add a changelog entry to each change that adds, removes or changes a feature.
- `chg-chestertons-fence` [should-fix] {maintainability, process} change.md:L170+26: Add a characterization test before rewriting code you do not understand.
- `chg-commit-body-says-why` [discuss] {process, maintainability} change.md:L197+29: Use the commit body to say why the change was made, not to repeat what the diff shows.
- `chg-commit-subject-imperative` [discuss] {process, maintainability} change.md:L227+25: Write the commit subject as a short command in the imperative, about 50 characters and at most 72, with no trailing period.
- `chg-commit-title-area-prefix` [discuss] {process, maintainability} change.md:L253+25: Start the commit or PR title with the area it changes, such as `net: summary` or `importer: summary`, where the project uses area prefixes.
- `chg-delete-legacy-after-migration` [should-fix] {compatibility, maintainability} <data> change.md:L279+30: When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.
- `chg-docs-updated-with-code` [should-fix] {maintainability, process} change.md:L366+26: Change the comments, docstrings and docs that describe the code in the same diff as the code, or delete them.
- `chg-each-commit-builds` [discuss] {process, testing, maintainability} change.md:L393+28: Make each commit in a series build and pass the tests on its own.
- `chg-match-codebase-pattern` [should-fix] {correctness, maintainability} change.md:L451+29: Follow the established pattern nearby.
- `chg-no-per-user-ide-files` [should-fix] {process, maintainability} change.md:L537+37: Do not commit a file that holds one developer's editor or IDE state; ignore those paths in the repository or a machine-wide exclude file. An ignore entry does not untrack a file already committed: remove it from the index with `git rm --cached`.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} change.md:L575+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.
- `chg-no-special-case-branches` [should-fix] {maintainability} change.md:L606+29: Put a new case behind its own function or type; do not add a one-off branch to a shared flow.
- `chg-refactor-has-behaviour-pin` [should-fix] {testing, maintainability} change.md:L754+26: Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.
- `chg-refactor-separate` [should-fix] {maintainability, process} change.md:L781+27: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-reuse-before-write` [should-fix] {maintainability} change.md:L809+27: Do not add a helper that duplicates one already in the repo; search for it first.

## function

- `fn-bool-arg-at-callsite` [discuss] {maintainability} function.md:L34+25: Replace a boolean flag argument with an enum, keyword-only argument or two functions.
- `fn-comments-explain-why` [should-fix] {maintainability} function.md:L128+27: Write comments that give a reason, a constraint, or a trade-off, and never restate what the next line does.
- `fn-comments-survive-context` [should-fix] {maintainability} function.md:L156+25: Write comments that remain true without outside context: no "currently", "for now" or "see the PR", and give a TODO the date or event that ends it.
- `fn-complexity-cap` [discuss] {maintainability, testing} function.md:L182+37: Set a cyclomatic complexity limit in the linter and keep every function under it.
- `fn-deprecation-names-version-and-replacement` [should-fix] {compatibility, maintainability} function.md:L308+25: Say in a deprecation notice which version deprecated it and what replaces it.
- `fn-doc-documents-errors` [should-fix] {maintainability, reliability} function.md:L464+33: Document in the doc comment each error a public function can raise, each condition that makes it panic, and each precondition a caller must meet to call it safely.
- `fn-doc-params-match-signature` [discuss] {maintainability, correctness} function.md:L498+37: Make the parameters a doc comment lists match the function's signature, by name and in number.
- `fn-doc-summary-sentence` [discuss] {maintainability} function.md:L536+31: Open each doc comment with one short summary line, then a blank line before any detail.
- `fn-early-return-no-else` [discuss] {maintainability} function.md:L568+37: Handle the error or edge case first and return early, so the main path is not nested.
- `fn-english-identifiers` [discuss] {maintainability} function.md:L606+25: Write identifiers and comments in English, unless the project policy names another language.
- `fn-error-string-lowercase-no-period` [discuss] {maintainability, usability} function.md:L688+25: Start an error string in lowercase and end it without punctuation when it is wrapped or printed after other context.
- `fn-length-budget` [discuss] {maintainability} function.md:L1148+38: Split a function that passes the project's length limit (about 40 lines if it sets none) unless its body is one simple operation or one flat dispatch.
- `fn-log-or-return-not-both` [should-fix] {observability, maintainability} function.md:L1216+30: Handle an error once: return it or log it, not both.
- `fn-name-intermediate-conditions` [discuss] {maintainability} function.md:L1282+26: Name each compound condition by assigning its sub-conditions to booleans that say what they mean.
- `fn-nesting-depth-cap` [discuss] {maintainability} function.md:L1340+37: Keep control-flow nesting shallow.
- `fn-no-getattr-for-known-names` [discuss] {maintainability} function.md:L1500+25: Use plain field access, and reserve dynamic access for genuinely dynamic names.
- `fn-no-magic-values` [should-fix] {maintainability} function.md:L1526+27: Give every meaningful literal a name: an enum member or a constant.
- `fn-parameter-limit` [should-fix] {maintainability} function.md:L1768+29: Set a parameter-count limit in the project's linter, and keep signatures within it.
- `fn-public-api-has-docstring` [discuss] {maintainability} function.md:L1862+30: Give each public module, class, function and method a doc comment.
- `fn-test-behaviour-not-implementation` [should-fix] {testing, maintainability} function.md:L2178+34: Assert what a caller can observe through the public interface, so a change that keeps behaviour does not break the test.
- `fn-todo-has-owner-or-issue` [discuss] {maintainability, process} function.md:L2267+25: Give each TODO an owner or a tracking issue, such as `TODO(alice)` or `TODO(#1234)`.
- `fn-variants-as-tagged-union` [should-fix] {maintainability} function.md:L2293+37: Model variants as a tagged union, and make every switch over it fail the build when a variant is unhandled.
- `py-docstrings-google` [discuss] {maintainability} function.md:L2359+27: Write a Google-style docstring only when it adds what the signature cannot say.

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
- `code-dead-docs-deleted` [discuss] {maintainability} codebase.md:L206+25: Delete the docs for code or features that were removed or never shipped, instead of leaving or hiding them.
- `code-doc-examples-stay-true` [discuss] {maintainability, testing} codebase.md:L302+25: Run each code example in the docs as a test.
- `code-docs-link-dont-duplicate` [discuss] {maintainability} codebase.md:L328+24: Link to the existing page or guide instead of rewriting or restating it.
- `code-docs-no-future-promises` [discuss] {maintainability} codebase.md:L405+24: Do not promise unreleased features, versions or dates in published docs.
- `code-docs-redirect-on-move` [discuss] {maintainability, usability} codebase.md:L456+26: Add a redirect from the old URL in the same change that moves, renames or deletes a documentation page.
- `code-docs-refs-resolve` [should-fix] {maintainability} codebase.md:L483+31: Run a link check in CI over the docs, so that every relative link and anchor they cite resolves.
- `code-file-lines-ceiling` [discuss] {maintainability, process} codebase.md:L515+27: Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.
- `code-readme-per-module` [discuss] {maintainability} codebase.md:L601+25: Give each package, module or self-contained component a README at its root that says what it holds and how to use it.
- `code-rule-has-enforcer` [should-fix] {maintainability} codebase.md:L675+33: Back each written repo rule that a type, lint or CI check could enforce with that check, not with a line in an instruction file or a repeated review comment.
- `py-ruff-gate` [should-fix] {maintainability} codebase.md:L1046+32: Enable the Ruff rule sets E, F, I, B, UP, SIM, BLE, TID and D in CI.

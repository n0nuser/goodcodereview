# Change review index

One line per stable change card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `change.md`: read them with offset `<first>` and limit `<count>`.

- `chg-agent-grounded-code` [should-fix] {maintainability, process} L3+28: Verify that every import and external call the agent wrote exists with that signature.
- `chg-agent-independent-review` [should-fix] {process} L32+25: Get sign-off from a person or a fresh-context reviewer who has the spec but not the author's reasoning; self-review by the writing session does not count.
- `chg-approval-tied-to-patch` [should-fix] {process} L58+27: Treat an approval or verification verdict as current only if the patch is unchanged: compare `git patch-id` at the verdict commit with the current head. If the patches differ only in tests, docs, or lint config, the verdict can stand when the built output is the same; any other difference needs a fresh check.
- `chg-author-hygiene` [should-fix] {process} L86+27: Self-review the diff and write the description before requesting review.
- `chg-breaking-change-taxonomy` [block] {compatibility} L114+27: Treat any change that callers can observe in a signature, return values, error types, defaults, or side effects as breaking until a consumer check says otherwise.
- `chg-chestertons-fence` [should-fix] {maintainability, process} L142+26: Add a characterization test before rewriting code you do not understand.
- `chg-delete-legacy-after-migration` [should-fix] {compatibility, maintainability} <data> L169+30: When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.
- `chg-devex-breaking-config` [should-fix] {compatibility, process} L200+28: Flag a change that renames or removes an environment variable, moves a secret, or remaps a port as breaking for developers and operators, and update every place that documents or sets it.
- `chg-expand-contract` [block] {compatibility} <data> L229+28: Evolve shared contracts in steps: add the new form beside the old (expand), migrate every consumer, then remove the old form (contract) in a later change.
- `chg-match-codebase-pattern` [should-fix] {correctness, maintainability} L258+29: Follow the established pattern nearby.
- `chg-migration-add-column-rewrite` [should-fix] {compatibility} <data> L288+27: Add the column nullable or with a constant default, then fill volatile, computed, or identity values in batches.
- `chg-name-attack-surface` [should-fix] {security, process} L316+27: List any new attack surface in the description.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} L344+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.
- `chg-no-special-case-branches` [should-fix] {maintainability} L375+29: Put a new case behind its own function or type; do not add a one-off branch to a shared flow.
- `chg-one-concern` [should-fix] {process} L405+26: Make each change do one logical thing; if the description needs "and" between unrelated outcomes, split it.
- `chg-perf-claim-evidence` [should-fix] {performance, testing} L432+25: Back a performance claim with measured before-and-after numbers.
- `chg-proto-no-field-type-change` [should-fix] {compatibility} L458+31: Never change the type of a protobuf field, switch it between repeated and scalar, or rename it while any consumer reads JSON or text format; add a new field instead.
- `chg-proto-reserve-removed-fields` [should-fix] {compatibility} L490+32: When you delete a protobuf field or enum value, add `reserved` for its number and name in the same change, and never reuse a number.
- `chg-refactor-has-behaviour-pin` [should-fix] {testing, maintainability} L523+26: Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.
- `chg-refactor-separate` [should-fix] {maintainability, process} L550+27: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-reuse-before-write` [should-fix] {maintainability} L578+27: Do not add a helper that duplicates one already in the repo; search for it first.
- `chg-review-signal` [discuss] {process} L606+27: Do not spend review comments on what a tool enforces or on minor style points; spend them on the findings that matter.
- `chg-rollback-path` [should-fix] {reliability} L634+27: State in the description how to undo the change.
- `chg-size-ceiling` [discuss] {process} L662+25: Split a change past about 400 changed lines or about 20 files, or say in the description why not; aim for about 200.
- `chg-tests-ship-with-change` [block] {testing} L688+27: Ship new or changed behaviour in the same change as a test that fails if the behaviour breaks.
- `chg-ui-change-screenshots-and-keyboard-pass` [should-fix] {accessibility, usability, process} <ui> L716+31: A UI change shows before-and-after screenshots and says what a keyboard-only pass and a 200% zoom check found on the changed screens.
- `chg-verify-before-claim` [block] {testing, process} L748+26: Back every "works" or "bug" claim with something run: a repro, a test or command output.

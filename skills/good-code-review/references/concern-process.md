# process cards

Every stable card that lists the `process` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-agent-grounded-code` [should-fix] {maintainability, process} change.md:L3+28: Verify that every import and external call the agent wrote exists with that signature.
- `chg-agent-independent-review` [should-fix] {process} change.md:L32+25: Get sign-off from a person or a fresh-context reviewer who has the spec but not the author's reasoning; self-review by the writing session does not count.
- `chg-approval-tied-to-patch` [should-fix] {process} change.md:L58+27: Treat an approval or verification verdict as current only if the patch is unchanged: compare `git patch-id` at the verdict commit with the current head. If the patches differ only in tests, docs, or lint config, the verdict can stand when the built output is the same; any other difference needs a fresh check.
- `chg-author-hygiene` [should-fix] {process} change.md:L86+27: Self-review the diff and write the description before requesting review.
- `chg-chestertons-fence` [should-fix] {maintainability, process} change.md:L142+26: Add a characterization test before rewriting code you do not understand.
- `chg-devex-breaking-config` [should-fix] {compatibility, process} change.md:L200+28: Flag a change that renames or removes an environment variable, moves a secret, or remaps a port as breaking for developers and operators, and update every place that documents or sets it.
- `chg-name-attack-surface` [should-fix] {security, process} change.md:L316+27: List any new attack surface in the description.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} change.md:L344+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.
- `chg-one-concern` [should-fix] {process} change.md:L405+26: Make each change do one logical thing; if the description needs "and" between unrelated outcomes, split it.
- `chg-refactor-separate` [should-fix] {maintainability, process} change.md:L550+27: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-review-signal` [discuss] {process} change.md:L606+27: Do not spend review comments on what a tool enforces or on minor style points; spend them on the findings that matter.
- `chg-size-ceiling` [discuss] {process} change.md:L662+25: Split a change past about 400 changed lines or about 20 files, or say in the description why not; aim for about 200.
- `chg-ui-change-screenshots-and-keyboard-pass` [should-fix] {accessibility, usability, process} <ui> change.md:L716+31: A UI change shows before-and-after screenshots and says what a keyboard-only pass and a 200% zoom check found on the changed screens.
- `chg-verify-before-claim` [block] {testing, process} change.md:L748+26: Back every "works" or "bug" claim with something run: a repro, a test or command output.

## module

- `mod-yagni` [should-fix] {maintainability, process} module.md:L661+25: Do not build an abstraction or capability for a need that does not exist yet; add it when the need or a second use appears.

## service

- `svc-cli-non-interactive` [should-fix] {maintainability, process} <cli> service.md:L789+41: Let the caller turn every prompt off with a flag or an environment variable, so the command never waits on a terminal.

## system

- `sys-agent-tool-least-privilege` [block] {security, process} system.md:L3+26: Give the agent only the narrow tools and the minimal credentials its task needs.

## codebase

- `code-adr` [discuss] {maintainability, process} codebase.md:L34+24: Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, and its consequences.
- `code-build-hermetic` [should-fix] {process} codebase.md:L59+30: Build from declared inputs only, so that the same source revision gives the same artifact.
- `code-ci-gates` [should-fix] {process} codebase.md:L90+25: Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.
- `code-file-lines-ceiling` [discuss] {maintainability, process} codebase.md:L275+27: Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.
- `code-flaky-test-quarantine` [should-fix] {testing, process} codebase.md:L303+29: Report every test that passes only on retry, move it to a quarantine with a named owner and a ticket, and return it to the merge gate only after it passes many reruns.
- `code-perf-budget-in-ci` [should-fix] {performance, process} codebase.md:L333+27: Write the performance budget down as a CI check that fails the build when it is exceeded.
- `code-release-gated-on-ci` [should-fix] {reliability, process} codebase.md:L361+47: Make a release or publish job depend on the checks passing for the tagged commit, never on the tag alone.
- `code-scoped-validation-loop` [discuss] {testing, process} codebase.md:L443+26: Document a command that checks one package or path, with readable output, so a small change does not need the full-repo run.
- `code-secret-scan` [block] {security, process} codebase.md:L470+26: Scan for committed credentials, and treat any hit as leaked: revoke and replace it first. With no scanner present and no secret found, the FAIL is the missing control; evidence is "absent in <paths>". A platform scanner (GitHub secret scanning with push protection, GitLab secret detection) counts when it is enabled on the repo and covers history.
- `code-test-selection-on-pr` [discuss] {testing, performance, process} codebase.md:L530+49: When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.
- `code-vuln-remediation-window` [should-fix] {security, process} codebase.md:L580+27: Write down how long a known-vulnerable dependency may stay unfixed and fix or upgrade it inside that window.
- `code-workflow-supply-chain` [block] {security, process} codebase.md:L608+49: Pin every CI action to a full commit SHA, and keep code from an unreviewed change out of any job that holds secrets or can deploy.

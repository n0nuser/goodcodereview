# process cards

Every stable card that lists the `process` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-agent-grounded-code` [should-fix] {maintainability, process} change.md:L3+28: Verify that every import and external call the agent wrote exists with that signature.
- `chg-agent-independent-review` [should-fix] {process} change.md:L32+25: Get sign-off from a person or a fresh-context reviewer who has the spec but not the author's reasoning; self-review by the writing session does not count.
- `chg-applied-migration-not-edited` [should-fix] {correctness, process} <data> change.md:L58+38: Do not edit or delete a migration that has already run in a shared environment; add a new migration that makes the change.
- `chg-approval-tied-to-patch` [should-fix] {process} change.md:L97+27: Treat an approval or verification verdict as current only if the patch is unchanged: compare `git patch-id` at the verdict commit with the current head. If the patches differ only in tests, docs, or lint config, the verdict can stand when the built output is the same; any other difference needs a fresh check.
- `chg-author-hygiene` [should-fix] {process} change.md:L125+27: Self-review the diff and write the description before requesting review.
- `chg-changelog-entry` [discuss] {maintainability, process} change.md:L181+27: Add a changelog entry to each change that adds, removes or changes a feature.
- `chg-chestertons-fence` [should-fix] {maintainability, process} change.md:L209+26: Add a characterization test before rewriting code you do not understand.
- `chg-commit-body-says-why` [discuss] {process, maintainability} change.md:L236+29: Use the commit body to say why the change was made, not to repeat what the diff shows.
- `chg-commit-subject-imperative` [discuss] {process, maintainability} change.md:L266+25: Write the commit subject as a short command in the imperative, about 50 characters and at most 72, with no trailing period.
- `chg-commit-title-area-prefix` [discuss] {process, maintainability} change.md:L292+25: Start the commit or PR title with the area it changes, such as `net: summary` or `importer: summary`, where the project uses area prefixes.
- `chg-devex-breaking-config` [should-fix] {compatibility, process} change.md:L349+28: Flag a change that renames or removes an environment variable, moves a secret, or remaps a port as breaking for developers and operators, and update every place that documents or sets it.
- `chg-docs-updated-with-code` [should-fix] {maintainability, process} change.md:L405+26: Change the comments, docstrings and docs that describe the code in the same diff as the code, or delete them.
- `chg-each-commit-builds` [discuss] {process, testing, maintainability} change.md:L432+28: Make each commit in a series build and pass the tests on its own.
- `chg-flag-naming-convention` [discuss] {maintainability, process} change.md:L548+33: Name each new flag by the team's written convention, and never give a deleted flag's key to different behaviour.
- `chg-name-attack-surface` [should-fix] {security, process} change.md:L669+27: List any new attack surface in the description.
- `chg-no-per-user-ide-files` [should-fix] {process, maintainability} change.md:L727+37: Do not commit a file that holds one developer's editor or IDE state; ignore those paths in the repository or a machine-wide exclude file. An ignore entry does not untrack a file already committed: remove it from the index with `git rm --cached`.
- `chg-no-silenced-diagnostics` [should-fix] {correctness, maintainability, process} change.md:L765+30: Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.
- `chg-one-concern` [should-fix] {process} change.md:L826+26: Make each change do one logical thing; if the description needs "and" between unrelated outcomes, split it.
- `chg-refactor-separate` [should-fix] {maintainability, process} change.md:L971+27: Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.
- `chg-review-signal` [discuss] {process} change.md:L1027+27: Do not spend review comments on what a tool enforces or on minor style points; spend them on the findings that matter.
- `chg-size-ceiling` [discuss] {process} change.md:L1083+25: Split a change past about 400 changed lines or about 20 files, or say in the description why not; aim for about 200.
- `chg-ui-change-screenshots-and-keyboard-pass` [should-fix] {accessibility, usability, process} <ui> change.md:L1137+31: A UI change shows before-and-after screenshots and says what a keyboard-only pass and a 200% zoom check found on the changed screens.
- `chg-verify-before-claim` [block] {testing, process} change.md:L1169+26: Back every "works" or "bug" claim with something run: a repro, a test or command output.

## function

- `fn-todo-has-owner-or-issue` [discuss] {maintainability, process} function.md:L2636+25: Give each TODO an owner or a tracking issue, such as `TODO(alice)` or `TODO(#1234)`.

## module

- `mod-yagni` [should-fix] {maintainability, process} module.md:L693+25: Do not build an abstraction or capability for a need that does not exist yet; add it when the need appears.

## service

- `svc-cli-non-interactive` [should-fix] {maintainability, process} <cli> service.md:L862+41: Let the caller turn every prompt off with a flag or an environment variable, so the command never waits on a terminal.

## system

- `sys-agent-tool-least-privilege` [block] {security, process} system.md:L3+26: Give the agent only the narrow tools and the minimal credentials its task needs.

## codebase

- `code-adr` [discuss] {maintainability, process} codebase.md:L34+24: Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, the options ruled out, and its consequences.
- `code-ai-pr-disclosure` [should-fix] {process} codebase.md:L59+28: Disclose AI assistance in the PR, and have a human author who can explain and defend every changed line without the tool.
- `code-build-hermetic` [should-fix] {process} codebase.md:L88+30: Build from declared inputs only, so that the same source revision gives the same artifact.
- `code-ci-gates` [should-fix] {process} codebase.md:L119+26: Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.
- `code-file-lines-ceiling` [discuss] {maintainability, process} codebase.md:L544+27: Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.
- `code-flaky-test-quarantine` [should-fix] {testing, process} codebase.md:L572+29: Report every test that passes only on retry, move it to a quarantine with a named owner and a ticket, and return it to the merge gate only after it passes many reruns.
- `code-gate-new-violations-only` [should-fix] {maintainability, process} codebase.md:L602+37: Gate CI on new or modified code, and track pre-existing violations in a separate store without letting a build add to it.
- `code-perf-budget-in-ci` [should-fix] {performance, process} codebase.md:L640+27: Write the performance budget down as a CI check that fails the build when it is exceeded.
- `code-release-gated-on-ci` [should-fix] {reliability, process} codebase.md:L694+47: Make a release or publish job depend on the checks passing for the tagged commit, never on the tag alone.
- `code-scoped-validation-loop` [discuss] {testing, process} codebase.md:L776+26: Document a command that checks one package or path, with readable output, so a small change does not need the full-repo run.
- `code-secret-scan` [block] {security, process} codebase.md:L803+26: Scan for committed credentials, and treat any hit as leaked: revoke and replace it first. With no scanner present and no secret found, the FAIL is the missing control; evidence is "absent in <paths>". A platform scanner (GitHub secret scanning with push protection, GitLab secret detection) counts when it is enabled on the repo and covers history.
- `code-test-pyramid-shape` [discuss] {testing, process} codebase.md:L891+27: Keep most tests at the unit level, fewer at the integration level and fewest end-to-end.
- `code-test-selection-on-pr` [discuss] {testing, performance, process} codebase.md:L919+49: When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.
- `code-vuln-remediation-window` [should-fix] {security, process} codebase.md:L1007+27: Write down how long a known-vulnerable dependency may stay unfixed and fix or upgrade it inside that window.
- `code-workflow-supply-chain` [block] {security, process} codebase.md:L1035+49: Pin every CI action to a full commit SHA, and keep code from an unreviewed change out of any job that holds secrets or can deploy.

## incident

- `inc-postmortem-blameless` [should-fix] {process} incident.md:L30+29: Write a postmortem so that it names causes in the system and the decisions around it, never a person or team as the one at fault.
- `inc-single-incident-commander` [discuss] {process, reliability} incident.md:L87+27: Name one incident commander for each major incident, who holds the overall state of the response and oversees the other roles.

# Codebase-level clusters (input: cluster-in/codebase.tsv, 113 rows)

## code-signed-commits-protected | orgs: 3 | status: READY
Rule: Require signed commits on protected branches, so unsigned commits cannot merge or be pushed.
Concern tags: security, process
Severity guess: should-fix
Rows: 264, 308, 381
Orgs: owasp, github, nodejs
Conflicts/duplicates: none (code-ci-gates and code-workflow-supply-chain do not mention signing)
Notes: owasp says the SCM requires signing before merge, github enforces verified signatures on push, nodejs requires GPG signing on all branches except main and actions/*; narrowest clause is "protected branches".

## code-secrets-not-plaintext-in-repo | orgs: 3 | status: READY
Rule: Keep secrets out of source and plaintext config: read them from a secret store, or commit only encrypted values.
Concern tags: security
Severity guess: should-fix
Rows: 1039, 322, 970
Orgs: owasp, gitlab, pulumi
Conflicts/duplicates: none; code-secret-scan states scanning and rotation, not storage
Notes: owasp bans hard-coded keys, gitlab says store outside the repository, pulumi allows ciphertext in config files; common clause is "no plaintext". Row 265 (owasp, no secrets in shell history) is a separate single-org clause.

## code-workflow-token-per-job-write | orgs: 2 | status: NEAR
Rule: Set workflow token permissions to read-only or none at the top level and grant write only on the job that needs it.
Concern tags: security
Severity guess: should-fix
Rows: 384, 387, 294
Orgs: openssf, rust, github
Conflicts/duplicates: none; code-workflow-supply-chain mentions "least-privilege tokens" only in its Why
Notes: openssf and rust state the top-level-minimum practice; github 294 only says permissions can be set at job or workflow level (an option, weak), so it likely does not count; github also has an id-token:write at narrowest scope row, same direction. Counts 2 solid, 3 if github 294 is accepted.

## code-new-code-coverage | orgs: 2 | status: NEAR
Rule: Every added line has unit test coverage, or the reason it lacks one is written down.
Concern tags: testing, process
Severity guess: discuss
Rows: 375, 341, 288
Orgs: kubernetes, dropbox, django
Conflicts/duplicates: none with a card; rows disagree internally
Notes: kubernetes says "in principle" with a written reason as the escape; dropbox row quotes Envoy (check that the org map is right) and wants 100%; django says missing coverage is a warning, not a blocker, so it opposes a hard gate. Narrowest clause is kubernetes' soft form.

## code-gate-new-violations-only | orgs: 2 | status: NEAR
Rule: Gate CI on new or modified code, and track pre-existing violations in a separate store without letting a build add to it.
Concern tags: maintainability, process
Severity guess: should-fix
Rows: 154, 2326
Orgs: sonarsource, archunit
Conflicts/duplicates: none (code-ci-gates does not state a baseline)
Notes: sonarsource scopes to new and modified code; archunit freezes a violation store that CI may not grow. Sonar is a vendor.

## code-ci-job-pass-rate-threshold | orgs: 2 | status: NEAR
Rule: Set a numeric pass-rate threshold for the pipeline or each blocking job, and act when it falls below it.
Concern tags: reliability, process
Severity guess: discuss
Rows: 237, 378, 377
Orgs: gitlab, kubernetes
Conflicts/duplicates: partial overlap with code-flaky-test-quarantine (named owner, return to gate); none contradicted
Notes: gitlab: master pipeline above 95%; kubernetes: a blocking job above 75% of weekly runs, plus an owning team (377). Thresholds differ; the rule only asks that one exists.

## code-tests-order-independent | orgs: 2 | status: NEAR
Rule: Tests give the same result in any order and share no state between suites.
Concern tags: testing, reliability
Severity guess: should-fix
Rows: 909, 2495, 317, 258
Orgs: kent-beck, gitlab, alloy
Conflicts/duplicates: none; code-test-fixtures-built-once covers fixture cost, not order independence; code-flaky-test-quarantine covers retries
Notes: kent-beck is a person (rows 909 and 2495 are one source), so 2 organisations plus a reference; gitlab randomises spec order, alloy gives each suite its own database.

## code-unused-code-diagnostics-on | orgs: 2 | status: NEAR
Rule: Enable the compiler or linter diagnostics for unused or never-executed code, and fail the build on them.
Concern tags: maintainability
Severity guess: discuss
Rows: 277, 487
Orgs: cmu-sei, microsoft
Conflicts/duplicates: none; code-dead-code names an unused-code linter in tool_gate only
Notes: cmu-sei says enable warnings for no-effect or unreachable code; microsoft says set noUnusedLocals to report errors (TypeScript only). Linter-owned, thin review judgement.

## code-rule-enforcer-table | orgs: 1 | status: ONE
Rule: Keep a table in the agent instruction file pairing each rule with the check that enforces it.
Concern tags: process, maintainability
Severity guess: discuss
Rows: 160, 163, 2436
Orgs: cursor
Conflicts/duplicates: code-rule-has-enforcer is the nearest card; check it before drafting
Notes: 163 replaces a constraint comment with a type, test or lint; 2436 shows each new check failing on a past mistake.

## code-selection-full-suite-fallback | orgs: 1 | status: ONE
Rule: When test selection cannot understand a change, run the full suite, and confirm a selected run against the full suite.
Concern tags: testing, reliability
Severity guess: should-fix
Rows: 397, 398
Orgs: microsoft
Conflicts/duplicates: code-test-selection-on-pr mentions the full suite before deploy; check for overlap
Notes: nx rows 410 and 411 (declare task inputs; fetch-depth 0) are the same theme, one org.

## code-selection-deterministic-from-graph | orgs: 1 | status: ONE
Rule: Select tests deterministically from the change's call graph, and treat history-based ordering as a separate step.
Concern tags: testing, performance
Severity guess: discuss
Rows: 436, 287
Orgs: shopify, gradle
Conflicts/duplicates: none
Notes: gradle 287 says always run recently added, changed, failed or flaky tests (different clause).

## code-adr-immutable-superseded | orgs: 1 | status: ONE
Rule: Never edit an accepted decision record; record a change as a new record that supersedes and links the old one, and give each record a status.
Concern tags: maintainability, process
Severity guess: discuss
Rows: 400, 401, 285
Orgs: microsoft, aws
Conflicts/duplicates: none
Notes: aws 285 is a different clause (review checks a change against ADRs it could violate), so the immutability clause has microsoft only.

## code-docs-links-from-ui-linted | orgs: 1 | status: ONE
Rule: Check links from UI code to documentation with a linter in CI.
Concern tags: maintainability, process
Severity guess: discuss
Rows: 315, 2445, 372
Orgs: gitlab
Conflicts/duplicates: none
Notes: github 372 is a different clause (block links into private URLs from public docs); rows 315 and 2445 are the same gitlab page.

## code-contract-tests-in-pipeline | orgs: 1 | status: ONE
Rule: Run consumer contract tests in the deployment pipeline.
Concern tags: testing, compatibility
Severity guess: should-fix
Rows: 31
Orgs: aws
Conflicts/duplicates: none
Notes: single page.

## code-local-lint-matches-ci | orgs: 1 | status: ONE
Rule: Run on each push, locally, every lint step that CI would enforce.
Concern tags: process, maintainability
Severity guess: discuss
Rows: 141
Orgs: stripe
Conflicts/duplicates: none; nearest code-scoped-validation-loop
Notes: single page.

## code-build-provenance | orgs: 1 | status: ONE
Rule: Every build produces provenance naming the build platform, process and top-level inputs.
Concern tags: security
Severity guess: discuss
Rows: 442, 1635
Orgs: openssf, github
Conflicts/duplicates: code-workflow-supply-chain mentions provenance in its Why
Notes: github 1635 is a different clause (reusable workflow for SLSA Level 3).

## code-a11y-tests-not-disabled | orgs: 1 | status: ONE
Rule: Do not disable accessibility tests to make a build pass, and log incomplete results for manual review instead of failing on them.
Concern tags: accessibility, testing
Severity guess: discuss
Rows: 251, 248, 254
Orgs: arizona, govuk, civicactions
Conflicts/duplicates: none
Notes: each row is its own org and clause, so each has 1 org; the common "do not weaken the check" clause covers only 251.

## code-no-ai-generated-media | orgs: 1 | status: ONE
Rule: Contributions contain no AI-generated images, video or audio.
Concern tags: process
Severity guess: discuss
Rows: 369, 2454
Orgs: ghostty
Conflicts/duplicates: code-ai-pr-disclosure is nearest (disclosure, not ban); check overlap
Notes: same page twice; kernel 325 (agents must not add Signed-off-by) is a different clause.

## Dropped
- Linter-owned or vendor-specific: 183, 327 (trailing whitespace), 499, 261, 295, 1181, 1182, 413, 414, 487 (merged above), 2235, 2236, 448, 391.
- Advice or history: 262, 366, 234 style rows, 2461, 2234, 2135, 2456.
- Already in cards: 404 and 403 (chg-flag-owner-retirement, code-dead-code), 478 and 2462 (code-dead-code Why), 480 and 481 (code-dependency-licence-sbom).

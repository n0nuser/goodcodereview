# Clusters: change level (input: cluster-in/change.tsv, 70 rows)

No group reaches 3 orgs. Two NEAR groups, then the 10 most promising ONE groups, then dropped groups.

## chg-changelog-entry | orgs: 2 | status: NEAR
Rule: Add a changelog entry to each change that adds, removes or changes a feature.
Concern tags: maintainability, process
Severity guess: discuss
Rows: 2, 56
Orgs: usgs, rails
Conflicts/duplicates: none (no existing card mentions a changelog)
Notes: usgs wants an entry with every change; rails exempts bug fixes, so the narrowest clause is feature changes. Needs one more org.

## chg-link-tracked-issue | orgs: 2 | status: NEAR
Rule: Link each pull request to the issue it addresses.
Concern tags: process, maintainability
Severity guess: discuss
Rows: 58, 2431
Orgs: apache, wordpress
Conflicts/duplicates: none; adjacent to chg-author-hygiene (description) and chg-matches-spec (traces to requirement), neither requires an issue link
Notes: apache exempts hotfixes such as typo fixes; wordpress asks for a closing keyword (Closes, See, Follow up to).

## chg-migration-reversible | orgs: 1 | status: ONE
Rule: Make each database migration reversible, and have the reviewer check both the migrate and the rollback output.
Concern tags: reliability, process
Severity guess: should-fix
Rows: 38, 2089
Orgs: gitlab
Conflicts/duplicates: none; adjacent to chg-rollback-path (description states undo), which is generic
Notes: both rows are GitLab pages.

## chg-flag-retire-ci-and-tests | orgs: 1 | status: ONE
Rule: Fail CI when a feature flag passes its age limit, and delete the tests of a retired flag with it.
Concern tags: maintainability, process
Severity guess: discuss
Rows: 447, 2467
Orgs: statsig, uber
Conflicts/duplicates: chg-flag-owner-retirement covers owner, default and removal date, not the CI age check
Notes: actually 2 orgs (statsig, uber) but they back different clauses (CI age gate vs delete flag tests), so each clause has 1 org. Row 243 (google: deprecation needs an owner) is already in chg-flag-owner-retirement.

## chg-deprecation-notice-removal-date | orgs: 1 | status: ONE
Rule: Announce each deprecation in release notes and docs with a target removal date; for config, target the next major release.
Concern tags: compatibility, process
Severity guess: should-fix
Rows: 36, 37
Orgs: gitlab
Conflicts/duplicates: svc-api-deprecation-sunset (service level, endpoints only); chg-devex-breaking-config
Notes: GitLab deprecation policy only.

## chg-refactor-reader-load | orgs: 1 | status: ONE
Rule: Keep a refactor only if it lowers reader load somewhere; otherwise revert it.
Concern tags: maintainability
Severity guess: discuss
Rows: 81, 2416
Orgs: cursor
Conflicts/duplicates: none
Notes: judgement-heavy; hard to mark FAIL with file:line evidence.

## chg-fix-every-instance | orgs: 1 | status: ONE
Rule: In a bug fix, find and fix every place with the same fault, not only the reported instance.
Concern tags: correctness
Severity guess: should-fix
Rows: 83
Orgs: cursor
Conflicts/duplicates: partial overlap with chg-fix-root-cause-not-symptom; check before drafting
Notes: single source.

## chg-removed-field-access-raises | orgs: 1 | status: ONE
Rule: When removing a field, make access to the old field raise an error so no code keeps using it.
Concern tags: correctness, compatibility
Severity guess: should-fix
Rows: 231
Orgs: stripe
Conflicts/duplicates: adjacent to chg-delete-legacy-after-migration, chg-expand-contract
Notes: single source.

## chg-rehearse-in-non-prod | orgs: 1 | status: ONE
Rule: Run the same change plan, with the same steps, in a non-production environment before production.
Concern tags: reliability, process
Severity guess: should-fix
Rows: 2210
Orgs: gitlab
Conflicts/duplicates: adjacent to chg-verify-before-claim
Notes: GitLab change-management C1/C2 context.

## chg-prefer-expect-over-allow | orgs: 1 | status: ONE
Rule: Suppress a lint with a form that warns when it becomes unneeded (Rust #[expect], not #[allow]).
Concern tags: maintainability
Severity guess: discuss
Rows: 133
Orgs: rust
Conflicts/duplicates: adjacent to chg-no-silenced-diagnostics
Notes: language-specific; a linter could own it.

## chg-security-review-before-build | orgs: 1 | status: ONE
Rule: Get a security review before implementation for features touching PII, passwords, TLS or permissions.
Concern tags: security, process
Severity guess: should-fix
Rows: 142
Orgs: mozilla
Conflicts/duplicates: adjacent to chg-name-attack-surface, chg-review-rigour-by-risk
Notes: pre-implementation step is hard to see in a diff.

## chg-explain-wrapped-in-txn | orgs: 1 | status: ONE
Rule: Wrap INSERT, UPDATE, DELETE or CREATE TABLE AS in a transaction that is rolled back when running EXPLAIN ANALYZE.
Concern tags: correctness, reliability
Severity guess: discuss
Rows: 4
Orgs: aws
Conflicts/duplicates: adjacent to chg-new-query-has-plan
Notes: tutorial-like; weak at change level.

## Dropped groups

- Keyboard operability (rows 1414 deque, 1420 bcgov; 2 orgs): duplicate of chg-ui-change-screenshots-and-keyboard-pass, which already requires a keyboard-only pass.
- Human approval for privileged actions (2103 owasp, 2523 uber; 2 orgs): runtime agent/tool controls, not a diff check; duplicate of chg-sensitive-paths-human-owner / chg-bot-approval-not-human for the review side.
- Regression test with bug fix (688): duplicate of chg-tests-ship-with-change.
- Reviewer-independence rows (43, 137, 2209, 2433, 51): duplicate of chg-agent-independent-review; 2433 (readability certification) is org-specific process.
- Approver from OWNERS (47), apply exact plan (1551), single issue per change (87), validate patches by build (345): duplicate of chg-sensitive-paths-human-owner, chg-approval-tied-to-patch, chg-one-concern, chg-agent-grounded-code.
- Review-finding validation and traceability (49, 50, 6): about AI review tooling output; 50 duplicates chg-matches-spec, 6 and 177 chg-review-signal.
- Linter-owned or advice (689 matchers, 106 formatter, 2211 dbg!, 1208 plural names, 111, 148, 155, 917, 2458, 2459, 332, 78, 74): linter/style, history, advice or product behaviour.
- Single-source process (45 Signed-off-by, 52, 54, 98, 107, 109, 122, 135, 137, 2188, 2404, 30, 33, 88, 90): one org each, vendor-specific or not checkable at file:line; not in top 10.

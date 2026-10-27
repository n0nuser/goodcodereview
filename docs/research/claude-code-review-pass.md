# Claude Code team's code-review article

Source: https://x.com/addyosmani/status/2114604912520921136 (org: Anthropic). The post describes how the Claude Code team reviews changes written largely by agents. It is a vendor describing its own process and product, so it counts as one organisation, flagged as a vendor, and never as the third organisation of a stable card. Its figures (revert rate, merge volume, share of PRs with comments, the blame percentage, the claimed quality gain from verification) are self-reported and are not used in any card.

## Quotes and the cards they back

1. "Instead of saying the task is done, we ask it to show us the result." Extra source for the stable card `chg-verify-before-claim`.
2. "Findings that are only style/diagnostics/cleanup related are filtered out." Extra source for the tool-owned clause of the stable card `chg-review-signal`. The post treats taste as human work, so it does not back the taste clause.
3. "When we roll out publicly, changes go to the latest channel first, and the stable channel trails behind." Extra source for staged rollout in the stable card `prod-canary-staged-rollout`. The post says it has no circuit breaker yet, so it does not back abort by rule.
4. "Changes behind feature flags can be disabled without deploying." Extra source for the stable card `prod-kill-switch-fallback`.
5. "A PR approval is only good for one commit. If a new commit lands that can't be trusted ... the PR must be reapproved." Extra source for the draft `chg-approval-tied-to-patch`. It says nothing about patch ids or test-only changes.
6. "Update your PR template with 'Testing', 'Risk' and 'How to revert'." Extra source for the draft `chg-rollback-path`.
7. "The tier is determined by the change, not the author." Backs the draft `chg-review-rigour-by-risk`.
8. "Require that all review threads be resolved before merging." Backs the draft `chg-review-threads-resolved`. The post adds that each finding is fixed or its thread closed with a reason.
9. "Limit the number of cycles" and "Limit re-review to just diff after the initial cycles" (the how-to list says to limit rounds and, after a few, review only the new diff). Backs the draft `chg-review-rounds-capped`.
10. "Bot approvals cannot be used to satisfy a required approval" and "Agent approvals don't count as human approvals". Backs the draft `chg-bot-approval-not-human`.
11. "Designate humans as the approvers for code and policies controlling auth, billing, CI, and release workflows, as well as installers. Use CODEOWNERS and branch protection for this." Backs the draft `chg-sensitive-paths-human-owner`.
12. Incident reviews involve "looking back to see what layer should have caught the problem". Backs the draft `inc-review-asks-which-check`.

## Not used

The description of its AI reviewer (parallel bug hunters, a vote on each finding, severity labels) is the vendor's product behaviour, not a practice other teams can adopt, so it backs no Rule. The wording in `chg-matches-spec` and `chg-agent-independent-review` reaches further than the post: the reviewer sees the intent stated by the author, and the post does not make a fresh-context agent a sign-off.

Each of the six new drafts has only this one organisation, so each carries `lacks: orgs` until two more organisations state the same practice.

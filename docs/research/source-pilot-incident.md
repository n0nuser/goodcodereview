# Source pilot: incident level

Five pages checked against the card set. Coverage was read from `cards/`, `packs/` and `docs/COVERAGE.md` with `rg`, and the closest card was read for each rule.

Caveat: quotes come from WebFetch answers (a small model summarising the fetched page), so they are close paraphrases, not verified verbatim text. Re-check any quote before it goes into a card.

Coverage marks: **covered** (card id), **partial** (card id plus what is missing), **NEW** (nearest ids checked; a lead only).

Totals: 11 rules from 4 pages with rules. 3 covered, 4 partial, 4 NEW. One page (Gregg) states no code-review rule.

---

## 1. https://web.dev/articles/lighthouse-ci

- Fetch status: fetched.

**Rule 1.1.** Lighthouse CI is configured by a `lighthouserc` file at the repo root. For a non-static site, set `startServerCommand` under `ci.collect`.
- Mark: **partial**. `cards/audit/codebase/code-perf-budget-in-ci.md` (its `tool_gate` names Lighthouse CI assert). The config file location and `startServerCommand` are not in any card. This is tool setup, not a review rule, so it is not a card candidate.
- Evidence: "Lighthouse CI is configured by placing a `lighthouserc.js` file in the root of your project's repo." / "If your site is not static, add the `startServerCommand` property to the `ci.collect` object"

**Rule 1.2.** Assertions that should block a build use `error`, not `warn`. `error` prints failures to stderr and exits with a non-zero code.
- Mark: **covered**, `code-perf-budget-in-ci`. Its FAIL example is `"categories:performance": ["warn", { "minScore": 0.9 }]` and its Rule is "fails the build when it is exceeded".
- Evidence: "`error`: print failures to stderr and exit Lighthouse CI with a non-zero exit code"

---

## 2. https://blog.cloudflare.com/details-of-the-cloudflare-outage-on-july-2-2019/

- Fetch status: fetched. The page is a postmortem. It states process rules about deploys, not code-review rules.

**Rule 2.1.** CI tests must pass before a global deploy.
- Mark: **partial**. `cards/audit/codebase/code-ci-gates.md` ("Require review and passing build, tests, lint, and type checks on the default branch before merge"). It covers the merge gate, not a gate before global deploy.
- Evidence: "Continuous Integration (CI) tests must pass prior to a global deploy."

**Rule 2.2.** After approval, the build and the full test suite run again.
- Mark: **partial**. `cards/change/chg-approval-tied-to-patch.md` covers stale approvals after a push. It does not say the suite re-runs after approval.
- Evidence: "Once a pull request is approved the code is built and the test suite runs (again)."

**Rule 2.3.** A deploy needs approval from the relevant manager or technical lead.
- Mark: **NEW**. Nearest checked: `chg-approval-tied-to-patch`, `code-ci-gates`. This is a governance rule. It is not a code-level check a reviewer can mark PASS/FAIL from a diff.
- Other source needed: two more independent orgs that state a deploy-approval rule for code review.
- Evidence: "the change has to be approved by the relevant manager or technical lead."

---

## 3. https://www.brendangregg.com/flamegraphs.html

- Fetch status: fetched. No code-review rules stated. The page explains how to read flame graphs (a wider frame appears in more stacks; the x-axis is sorted alphabetically, not by time; clicking zooms). None of these is a checkable review rule for a diff. No rows.

---

## 4. https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/optimize-code-infrastructure

- Fetch status: fetched.

**Rule 4.1.** Don't mask performance problems with brute force. Adding compute instead of fixing the code is the wrong fix.
- Mark: **NEW**. Nearest checked: `chg-perf-claim-evidence` (measured before/after numbers), `code-perf-budget-in-ci`. Neither says a fix must change the code rather than add capacity.
- Other source needed: two more independent orgs on "fix in code, not by adding capacity", with a checkable form (for example, a diff that only raises instance counts or limits, with no code change, is a FAIL).
- Evidence: "Don't mask performance issues with brute force."

**Rule 4.2.** Minimise function calls and redundant calculations inside loops. Move computations outside the loop.
- Mark: **NEW**. Nearest checked: `fn-join-dont-concat-in-loop` (concatenation only). No card covers loop-invariant hoisting.
- Other source needed: two more independent orgs on loop-invariant hoisting. Likely a language performance guide.
- Evidence: "Minimize function calls within loops, and eliminate redundant calculations. Consider moving computations outside the loop or using loop unrolling."

**Rule 4.3.** Retrieve only the necessary information from the database. Avoid large amounts of unneeded data.
- Mark: **covered**, `fn-fetch-only-needed-data` ("Filter, count, and aggregate in the query, and select only the columns the code uses"). The batching half of the page's network advice is also in `sys-n-plus-one-pooling`.
- Evidence: "Ensure that database queries retrieve only the necessary information. Avoid retrieving large amounts of unnecessary data"

---

## 5. https://docs.gitlab.com/development/performance/

- Fetch status: fetched.

**Rule 5.1.** Every Ruby file starts with the `# frozen_string_literal: true` header. The page says RuboCop enforces it.
- Mark: **NEW**. Nearest checked: none (no card mentions frozen string literals). `docs/COVERAGE.md` drops linter-owned rules by policy (the "logging is linter-owned | dropped" row), so this is likely to be dropped, not carded. Ruby-specific as well.
- Other source needed: none if the policy holds. Otherwise two more orgs on the rule and a language-neutral form.
- Evidence: "add the following header to all Ruby files."

**Rule 5.2.** A use of `Gitlab::ExclusiveLease.skipping_transaction_check` outside spec or fixture files should link an infradev issue for removing it.
- Mark: **covered**, `chg-no-silenced-diagnostics` ("Name the rule, the reason, and a ticket on every suppression"). The card is about suppressions, and this is one.
- Evidence: "should include links to an infradev issue for plans to remove it."

**Rule 5.3.** Remove the `_perf` method (temporary `benchmark-swap` alternative) before committing.
- Mark: **partial**. `cards/change/chg-author-hygiene.md` covers stray debug lines found by self-review. `cards/change/chg-perf-claim-evidence.md` covers benchmark evidence. No card covers leftover benchmark scaffolding in a commit.
- Evidence: "Remove the `_perf` method before you commit."

---

## Summary

| Source | Fetch | Rules | Covered | Partial | NEW |
|---|---|---|---|---|---|
| web.dev Lighthouse CI | fetched | 2 | 1 | 1 | 0 |
| Cloudflare 2019 outage | fetched | 3 | 0 | 2 | 1 |
| Brendan Gregg flame graphs | fetched | 0 | 0 | 0 | 0 |
| Azure WAF PE:07 | fetched | 3 | 1 | 0 | 2 |
| GitLab performance | fetched | 3 | 1 | 1 | 1 |
| **Total** | 5 of 5 fetched, 0 blocked | **11** | **3** | **4** | **4** |

No card files were created or edited.

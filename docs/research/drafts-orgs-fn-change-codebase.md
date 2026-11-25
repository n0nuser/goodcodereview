# Draft cards short on organisations: fn, change, codebase

Method: each page fetched with a stdlib Python script (tags stripped, regex match on the stripped text). Fetch date 2026-11-24. Quotes are 10 words or fewer. Org grouping follows docs/PROMOTION.md (Google covers Go, Android, Chromium, Testing Blog; Microsoft covers Learn; GitHub covers docs). "soft" means the page documents a tool setting or describes a mechanism, not a rule for reviewers. Cards were not edited. Scope: the 29 drafts under cards/change, cards/audit/function and cards/audit/codebase whose `lacks:` starts with `orgs`.

## Summary

| Card | Orgs now | New orgs | New total | Verdict |
|---|---|---|---|---|
| code-ci-job-pass-rate-threshold | GitLab, Kubernetes | Slack | 3 | clears (Slack is a project metric, soft) |
| chg-api-spec-in-same-change | OpenAPI, Zalando | Kubernetes | 3 | clears (separate commit, same PR) |
| code-gate-new-violations-only | SonarSource, ArchUnit | Google (Android lint) | 3 | clears |
| chg-review-threads-resolved | Anthropic | GitHub, GitLab | 3 | soft (setting docs) |
| fn-no-logic-in-tests | Microsoft, Uber | Google | 3 | clears |
| fn-atomic-related-updates | (cursor/plugins) | PostgreSQL, Django, Rails | 3 | soft (describes transactions) |
| fn-error-summary | GOV.UK | NHS, Scottish Government | 3 | clears |
| fn-flags-type-for-flag-sets | Microsoft, Rust | Oracle | 3 | clears |
| fn-no-aria-hidden-on-focusable | Google, WebAIM | Mozilla, Deque | 4 | clears |
| fn-resource-lifetime | Google (Go) | Google C++, ISO C++ | 3 | clears for owner rule (Google counts once) |
| code-tests-order-independent | GitLab, Alloy | Go (Google), RSpec | 3 | soft (tool flags) |
| code-signed-commits-protected | OWASP, Node.js | GitLab | 3 | soft (push rule) |
| chg-link-tracked-issue | Apache, WordPress | CPython | 3 | soft |
| chg-sensitive-paths-human-owner | Anthropic | GitLab | 2 | short (GitHub page unverified) |
| chg-bot-approval-not-human | Anthropic | GitHub | 2 | short |
| chg-flag-owner-retirement | Dropbox, Statsig, GitLab | Chromium | partial | removal now 4; owner and ticket still short |
| fn-empty-collection-not-none | none independent | Microsoft | 1 | short |
| fn-propagate-dont-swallow | none independent | Google Go, SEI CERT | 2 | short by one |
| chg-matches-spec | Google, Dropbox | none | 2 | short |
| chg-agent-mock-asserting-tests | Google, cursor/plugins | none | 2 | short |
| fn-no-pass-through-wrapper, fn-no-anonymous-tuples, fn-known-keys-get-a-type, fn-no-stringly-typed-returns, chg-fix-root-cause-not-symptom, code-documented-setup-runs, code-test-suite-time-budget, chg-review-rigour-by-risk, chg-review-rounds-capped | unchanged | none found | unchanged | short |

## Cards that clear

### code-ci-job-pass-rate-threshold
Current: GitLab, Kubernetes.
- Slack. https://slack.engineering/handling-flaky-tests-at-scale-auto-detection-suppression/ . "Increase the main branch jobs passing to 95%" (success metric). Soft: an internal target for one project, not a published rule.
- Total 3.

### chg-api-spec-in-same-change
Current: OpenAPI, Zalando.
- Kubernetes. https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-architecture/api_changes.md . "Make sure you update the swagger and OpenAPI spec" by running `make update`. It adds the spec change should be a commit separate from the rest, still in the same PR.
- Total 3.

### code-gate-new-violations-only
Current: SonarSource, ArchUnit.
- Google (Android lint). https://developer.android.com/studio/write/lint . "so that only new issues are reported." The baseline lets you fail the build "without having to go back and address all existing issues."
- Total 3.

### fn-no-logic-in-tests
Current: Microsoft, Uber.
- Google Testing Blog. https://testing.googleblog.com/2014/07/testing-on-toilet-dont-put-logic-in.html . "Tests can avoid complexity by stating their inputs and outputs directly." Also "simplicity is more important than flexibility in tests."
- Total 3.

### fn-error-summary
Current: GOV.UK.
- NHS. https://service-manual.nhs.uk/design-system/components/error-summary . "You must link the errors in the error summary to the answer."
- Scottish Government. https://designsystem.gov.scot/components/error-summary . "Link the errors in the error summary to the answer they relate to."
- Total 3. (UK public bodies with separate design systems; GOV.UK is the origin of the pattern, so a reviewer may call them one lineage. The pages are independent.)

### fn-flags-type-for-flag-sets
Current: Microsoft, Rust.
- Oracle (Java). https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/EnumSet.html . EnumSet is "a high-quality, typesafe alternative to traditional int-based 'bit flags.'"
- Python enum docs describe `Flag` ("combined using the bitwise operations") but state no rule; not counted.
- Total 3.

### fn-no-aria-hidden-on-focusable
Current: Google, WebAIM.
- Mozilla (MDN). https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-hidden . "Do not use aria-hidden="true" on focusable elements."
- Deque. https://dequeuniversity.com/rules/axe/html/4.10/aria-hidden-focus . Rule title: "ARIA hidden element must not be focusable or contain focusable elements" (Serious impact; a vendor).
- Total 4.

### fn-resource-lifetime
Current: Google (Go cancel path); the structured-concurrency blog is one person.
- Google (C++). https://google.github.io/styleguide/cppguide.html . "Prefer to have single, fixed owners for dynamically allocated objects."
- ISO C++ (Core Guidelines). https://isocpp.github.io/CppCoreGuidelines/CppCoreGuidelines . "R.1: Manage resources automatically using resource handles and RAII."
- Total 3 for the owner rule, but both Google pages are one org under PROMOTION.md, so firm count is Google, ISO C++ plus the unaddressed blog: treat as 2 firm and 1 short unless a third non-Google org is added (Rust ownership chapter is the obvious candidate; not fetched).

## Soft or short

### chg-review-threads-resolved (soft, 3)
- GitHub. https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches . "Requires all comments on the pull request to be resolved before it can be merged."
- GitLab. https://docs.gitlab.com/user/project/merge_requests/ . "You can prevent merge requests from merging while threads remain open."
Both document a setting, not a rule for reviewers.

### fn-atomic-related-updates (soft, 3)
- PostgreSQL. https://www.postgresql.org/docs/current/tutorial-transactions.html . A transaction "bundles multiple steps into a single, all-or-nothing operation."
- Django. https://docs.djangoproject.com/en/5.1/topics/db/transactions/ . "Atomicity is the defining property of database transactions."
- Rails. https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html . Statements are permanent "only if they can all succeed as one atomic action."
All three describe the mechanism, none says "review for related writes outside a transaction". Counterpoint: sagas and idempotent retries across services.

### code-tests-order-independent (soft, 3)
- Go. https://pkg.go.dev/cmd/go . "-shuffle ... Randomize the execution order of tests." Off by default.
- RSpec. https://rspec.info/features/3-13/rspec-core/command-line/order/ . "Use rand to randomize the order of groups and examples." Documents the option only.

### code-signed-commits-protected (soft, 3)
- GitLab. https://docs.gitlab.com/user/project/repository/push_rules/ . "Reject unsigned commits: Commit must be signed." A push rule, with a caveat that it can block Web IDE commits.

### chg-link-tracked-issue (soft, 3)
- CPython. https://devguide.python.org/getting-started/pull-request-lifecycle/ . The NEWS entry file name carries "the issue number the change is for." This shows the practice, not an explicit "link the PR" rule.
- Django (https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/) lets trivial fixes skip a Trac ticket, which supports the counterpoint, not the rule.

### chg-sensitive-paths-human-owner (2)
- GitLab. https://docs.gitlab.com/user/project/codeowners/ . "Require owners to approve changes." Feature docs; names no auth, billing or CI paths. GitHub's code-owners page was fetched but no sentence was matched, so it does not count.

### chg-bot-approval-not-human (2)
- GitHub. https://docs.github.com/en/copilot/concepts/agents/code-review . "By default, Copilot's reviews do not count toward required approvals." A second org not found.

### chg-flag-owner-retirement (partial)
- Chromium (Google). https://raw.githubusercontent.com/chromium/chromium/main/docs/how_to_add_your_feature_flag.md . "When a feature flag is no longer used it should be removed." It also runs a test that every flag has expiry metadata. An owner field was not matched in the fetched text. Adds Chromium to the removal clause only.

### fn-empty-collection-not-none (1)
- Microsoft. https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/guidelines-for-collections . "DO NOT return null values from collection properties or from methods returning collections."
- SEI CERT MET55-J ("Return an empty array or collection instead of a null value") is the likely second; the fetch failed twice (connection reset), so not counted. SonarSource S1168 page is a JS shell. Needs one retry.

### fn-propagate-dont-swallow (2 independent)
- Google (Go). https://go.dev/wiki/CodeReviewComments . "Do not discard errors using _ variables."
- SEI CERT. https://wiki.sei.cmu.edu/confluence/display/java/ERR00-J.+Do+not+suppress+or+ignore+checked+exceptions . Rule title is the rule. Exception EX1 allows letting a higher level handle it, which fits the card's propagate clause.
- Third org not found (Microsoft exceptions page returned no match).

## Not found

- chg-matches-spec, chg-agent-mock-asserting-tests: the Microsoft playbook and unit-testing pages returned nothing usable (the playbook text is mostly navigation); Mockito javadoc did not load.
- fn-no-pass-through-wrapper, fn-no-anonymous-tuples, fn-known-keys-get-a-type, fn-no-stringly-typed-returns, chg-fix-root-cause-not-symptom, code-documented-setup-runs, code-test-suite-time-budget (Abseil ch. 11 talks about speed and test sizes but no matched time limit), chg-review-rigour-by-risk, chg-review-rounds-capped: searches returned blogs and AI-skill repos only; no org page found within budget.

## Drop candidates

- chg-review-rounds-capped and chg-review-rigour-by-risk: the only source is an X post (x.com is a JS shell, so unverifiable by fetch) and no org states either rule. Drop unless Pablo wants to keep them on a hunch.
- fn-no-pass-through-wrapper: backed by one author (Ousterhout), and the pass-through wrapper is often a legitimate adapter or seam; a reviewer will argue it. Hold or drop.
- chg-review-comment-format and chg-new-query-has-plan (not `orgs` lacks) have other gaps; not assessed here.
- chg-bot-approval-not-human, chg-sensitive-paths-human-owner: all same X-post lineage with only feature docs behind them; keep only if a second non-vendor org appears.

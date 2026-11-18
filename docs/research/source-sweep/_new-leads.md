# NEW leads from the source sweep

Generated from b*.md. Each lead needs 3 independent orgs before it can be a card. Quotes come from cached raw text.

- https://astrogeology.usgs.gov/docs/how-to-guides/software-management/guidelines-for-pull-requests/
  NEW - nearest chg-author-hygiene | Accompany each change with a changelog entry | "Ensure that your changes are accompanied by an entry in the changelog"
- https://aws.amazon.com/blogs/database/how-postgresql-processes-queries-and-how-to-analyze-them/
  NEW - nearest chg-new-query-has-plan | Wrap INSERT, UPDATE, DELETE or CREATE TABLE AS in BEGIN before EXPLAIN ANALYZE, because ANALYZE runs them | "wrapping these statements in a transaction block using BEGIN"
- https://blog.cloudflare.com/ai-code-review/
  NEW - nearest chg-review-signal | Flag only issues in code the change touches, not unchanged code | "Issues in unchanged code that this MR doesn't affect"
- https://buf.build/docs/breaking/rules/
  NEW - nearest chg-proto-reserve-removed-fields | Deprecate a message field instead of deleting it, since deletion breaks generated code | "This checks that no message field is deleted."
- https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/qa.nt.7-verify-service-integrations-through-contract-testing.html
  NEW - nearest chg-breaking-change-taxonomy | Consumers run the relevant contract tests before integrating with a producer. | "before a consumer service integrates with a producer, run the relevant contract tests"
- https://docs.aws.amazon.com/wellarchitected/latest/devops-guidance/qa.nt.7-verify-service-integrations-through-contract-testing.html
  NEW - nearest code-ci-gates | Embed contract tests in the deployment pipeline. | "Embed contract testing into your deployment pipeline."
- https://docs.github.com/en/get-started/git-basics/ignoring-files
  NEW - nearest chg-no-per-user-ide-files | A tracked file must be untracked before an ignore rule takes effect. | "you must untrack the file before you add a rule to ignore it."
- https://docs.gitlab.com/administration/package_information/deprecation_policy
  NEW - nearest chg-devex-breaking-config | Announce each config deprecation in release notes and docs with a removal date. | "The blog post item contains the deprecation notice together with the target removal date."
- https://docs.gitlab.com/administration/package_information/deprecation_policy
  NEW - nearest chg-flag-owner-retirement | Regular config removal targets the next major release. | "For regular configuration, the removal target should always be the date of the next major release."
- https://docs.gitlab.com/development/database_review/
  NEW - nearest chg-rollback-path | Reviewers check both migrate and rollback output for every new migration. | "database reviewers must review the output of both migrating (`db:migrate`) and rolling back (`db:rollback`) for all migrations."
- https://docs.gitlab.com/user/project/merge_requests/approvals/settings/
  NEW - nearest chg-agent-independent-review | Users who add commits, as Git author or committer, are excluded from approval. | "GitLab excludes both identities from approval."
- https://docs.kernel.org/process/submitting-patches.html
  NEW - nearest chg-author-hygiene | Every patch carries a Signed-off-by line from its author, certifying the Developer's Certificate of Origin. | "The sign-off is a simple line at the end of the explanation for the patch"
- https://docs.pact.io/pact_broker/can_i_deploy
  NEW - nearest svc-api-contract-tests | Before deploying, check the version is compatible with the other apps already in the target environment. | "To make sure you are safe to deploy an application, add the following line before deploying:"
- https://docs.prow.k8s.io/docs/components/plugins/approve/approvers/
  NEW - nearest chg-sensitive-paths-human-owner | Every file a PR modifies needs an approval from an approver listed in the OWNERS file for that directory before merge. | "every file modified by the PR must be approved (via `/approve`) by an approver from the OWNERs files"
- https://dropbox.tech/security/dropbox-mcp-dash-design-code-security
  NEW - nearest chg-review-signal | Validate every review finding against the actual code before it reaches the developer. | "Findings must be validated against the actual code before they reach a developer"
- https://dropbox.tech/security/dropbox-mcp-dash-design-code-security
  NEW - nearest chg-matches-spec | Every review finding traces back to a specific requirement and its source document. | "Every finding should be traceable back to a specific requirement and source document"
- https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
  NEW - nearest chg-agent-independent-review | Every diff must be reviewed before it merges, with no exceptions. | "every diff must be reviewed, without exception."
- https://firefox-source-docs.mozilla.org/testing/testing-policy/index.html
  NEW - nearest chg-no-silenced-diagnostics | Landing without tests under the "other" exception needs a reviewer comment explaining why that is appropriate. | "This **requires a comment** from the reviewer explaining why it’s appropriate to land without tests."
- https://flex.apache.org/flexunit/tutorial/flexunit/Unit-15.html
  NEW - nearest chg-refactor-has-behaviour-pin | Refactor in small steps, running the tests after each change before the next. | "Refactor slowly. Make changes, create and run tests, then move on to the next change."
- https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html
  NEW - nearest chg-author-hygiene | A change that adds, removes or changes a feature needs a CHANGELOG entry; a bug fix does not. | "If the change adds, removes, or changes a feature, be sure to include a CHANGELOG entry."
- https://flink.apache.org/how-to-contribute/code-style-and-quality-pull-requests/
  NEW - nearest chg-matches-spec | Tie each pull request to a tracked issue, except hotfixes such as typo fixes. | "Make sure that the pull request corresponds to a JIRA issue."
- https://github.com/cursor/plugins/blob/main/cursor-team-kit/skills/verify-this/SKILL.md
  NEW - nearest chg-verify-before-claim | Give a verdict of VERIFIED, NOT VERIFIED or INCONCLUSIVE; noisy or invalid baselines force INCONCLUSIVE. | "no valid baseline, noisy signal, failed measurement, or an environment difference invalidates the comparison."
- https://github.com/cursor/plugins/blob/main/pstack/skills/benchmark-checklist/SKILL.md
  NEW - nearest chg-perf-claim-evidence | Measure the end-to-end path a user waits on and report the micro result as a share of it. | "Next to any micro result, measure the end-to-end path a user waits on"
- https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md
  NEW - nearest chg-matches-spec | Keep a refactor only if it lowers reader load; revert it otherwise. | "If the diff does not lower reader load somewhere, revert it."
- https://github.com/cursor/plugins/blob/main/pstack/skills/principle-fix-root-causes/SKILL.md
  NEW - nearest chg-fix-root-cause-not-symptom | Find and fix every place that has the same fault, not just the instance | "Fix the pattern, not the instance. Find every place with the same fault."
- https://github.com/google/langextract/blob/main/CONTRIBUTING.md
  NEW - nearest chg-size-ceiling | Each change addresses a single issue and is one cohesive change | "Each PR should address a single issue and contain one cohesive change."
- https://github.com/google/langextract/blob/main/CONTRIBUTING.md
  NEW - nearest chg-no-per-user-ide-files | Contributors may not change infrastructure, build configuration, or core documentation files | "Contributors cannot modify infrastructure files, build configuration, and core documentation."
- https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide
  NEW - nearest chg-breaking-change-taxonomy | A change that removes multi-job support or changes startup behaviour is a breaking change to flag | "Running multiple batch jobs is no longer supported."
- https://go.dev/doc/effective_go
  NEW - nearest go-wrap-errors-with-w | Handle each error with an early return so the success path runs straight down the page | "successful flow of control runs down the page, eliminating error cases as they arise."
- https://go.dev/doc/effective_go
  NEW - nearest py-imports | Avoid dot-imports that pull a package's names into the local namespace | "Don't use the `import .` notation"
- https://learn.microsoft.com/en-us/aspnet/core/grpc/versioning
  NEW - nearest chg-proto-no-field-type-change | Adding a field to a request message must not break older clients; the service must work when the field is unset | "To be a non-breaking change, the service must succeed when the new field isn't set by older clients."
- https://llvm.org/docs/Contributing.html
  NEW - nearest chg-refactor-separate | Format the patch with the project formatter (clang-format) before requesting review | "please also ensure it is formatted properly"
- https://llvm.org/docs/Contributing.html
  NEW - nearest chg-one-concern | A patch is a single commit, up to date with upstream, with no merge commits | "have a single commit, up-to-date with the upstream `origin/main` branch"
- https://llvm.org/docs/SupportPolicy.html
  NEW - nearest chg-rollback-path | Broken main must be fixed quickly or the offending patch reverted | "Those must be fixed as soon as possible or patches must be reverted, as per review policy."
- https://michaelfeathers.silvrback.com/characterization-testing
  NEW - nearest chg-refactor-has-behaviour-pin | Read tests as descriptions of what the code does now, not as statements of correctness | "We can see them as descriptions of what we have rather than statements of correctness."
- https://raw.githubusercontent.com/elastic/eui/main/.github/pull_request_template.md
  NEW - nearest chg-ui-change-screenshots-and-keyboard-pass | Visual changes must say whether they affect style overrides and whether visual testing is needed | "Visual changes — May impact style overrides; could require visual testing."
- https://refactoring.guru/smells/duplicate-code
  NEW - nearest mod-fowler-smells | Identical code in every branch of a conditional moves outside the conditional | "place the identical code outside of the condition tree"
- https://retool.com/blog/running-safe-database-migrations-using-postgres
  NEW - nearest sys-migration-lock-timeout | Wrap each schema migration in a transaction, because the migration author must do it | "As the migration author, you are responsible for using a transaction in every migration you write."
- https://rust-lang.github.io/rust-clippy/master/index.html#allow_attributes_without_reason
  NEW - nearest chg-no-silenced-diagnostics | Prefer #[expect] over #[allow] so an unneeded suppression warns | "`#[expect]` attributes suppress the lint emission, but emit a warning, if the expectation is unfulfilled."
- https://rustc-dev-guide.rust-lang.org/tests/adding.html
  NEW - nearest chg-tests-ship-with-change | A test file opens with a comment naming its purpose and issue number | "If there is an issue number associated with the test, include the issue number."
- https://slack.engineering/how-about-code-reviews/
  NEW - nearest chg-agent-independent-review | A reviewer who does not understand the change reads the current code and asks, or hands it on | "If you don’t understand the code being changed, go read the current version."
- https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
  NEW - nearest code-scoped-validation-loop | Run the lint steps that CI would enforce locally, on each push | "any lint step that would fail in CI is enforced in the IDE or on a git push"
- https://wiki.mozilla.org/Security/Reviews
  NEW - nearest chg-name-attack-surface | Security-sensitive features (PII, passwords, TLS, permissions) get a security review before implementation | "this process is strongly encouraged for any security sensitive features"
- https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/
  NEW - nearest chg-chestertons-fence | Do not rewrite a working system from scratch; change it incrementally and keep the bug fixes it already has | "When you throw away code and start from scratch, you are throwing away all that knowledge."
- https://www.sonarsource.com/blog/legacy-codebases-are-a-devops-issue/
  NEW - nearest code-ci-gates | Enforce quality standards on new and modified code only, tracking legacy issues separately | "enforce quality standards on new and modified code while tracking legacy issues separately"
- https://www.sqlite.org/eqp.html
  NEW - nearest chg-new-query-has-plan | Do not parse EXPLAIN QUERY PLAN output in application code; its format may change between releases | "Applications should not depend on the output format of the EXPLAIN QUERY PLAN command."
- https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md
  NEW - nearest code-rule-has-enforcer | Keep a table in the agent instruction file pairing each rule with the check that enforces it | "Keep a table in the agent instruction file that pairs each rule with what enforces it."
- https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md
  NEW - nearest code-rule-has-enforcer | Replace a constraint comment with the cheapest type, test or lint that enforces it, where one can | "Offer the cheapest in-scope type, runtime, test, or CI lint."
- https://stripe.dev/blog/formatting-an-entire-25-million-line-codebase-overnight-the-rubyfmt-story
  NEW - nearest prod-canary-staged-rollout | Roll out a code-wide tool change gradually: opt files in first, then expand as confidence grows | "we built in a per-file opt-in so `rubyfmt` would only format files that explicitly asked for it"
- https://google.github.io/eng-practices/review/reviewer/standard.html
  NEW - nearest chg-review-signal | Approve a change once it clearly improves code health, even if it is not perfect | "reviewers should favor approving a CL once it is in a state where it definitely improves the overall code health"
- https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
  NEW - nearest prod-a11y-audit-before-launch | Publish an accessibility statement at public beta and review it at least yearly | "Your accessibility statement should be reviewed at least once a year"
- https://www.kernel.org/doc/html/latest/process/coding-style.html
  NEW - nearest code-ci-gates | Leave no whitespace at line ends, and enforce it with the editor or a lint check | "Get a decent editor and don’t leave whitespace at the end of lines."
- https://pmd.github.io/pmd/pmd_rules_java_design.html
  NEW - nearest fn-length-budget | Report methods whose cyclomatic complexity reaches 10 and split them into smaller methods. | "By default, this rule reports methods with a complexity >= 10."
- https://sre.google/workbook/canarying-releases/
  NEW - nearest prod-canary-staged-rollout | Select the few canary metrics that best show user problems, no more than about a dozen. | "Select the top few metrics to use in canary evaluations (perhaps no more than a dozen)."
- https://sre.google/workbook/canarying-releases/
  NEW - nearest prod-canary-staged-rollout | Run at most one canary deployment at a time. | "We strongly advise running only one canary deployment at a time."
- https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/
  NEW - nearest sys-pii-minimise-retention | Check each change for personal data written to logs. | "Are we logging any PII information?"
- https://dropbox.tech/infrastructure/lessons-learned-in-incident-management
  NEW - nearest prod-wide-events-bounded-labels | Make changes to experiments and feature gates visible so responders can find them. | "improved visibility for changes"
- https://spec.openapis.org/oas/v3.1.0.html
  NEW - nearest svc-api-spec-matches-impl | Every path template variable must match a declared path parameter. | "Each template expression in the path _MUST_ correspond to a path parameter"
- https://spec.openapis.org/oas/v3.1.0.html
  NEW - nearest svc-api-naming-consistent | Component map keys must match a fixed regex of letters, digits, dot, dash and underscore. | "All the fixed fields declared above are objects that _MUST_ use keys that match the regular expression"
- https://spec.openapis.org/oas/v3.1.0.html
  NEW - nearest svc-api-spec-matches-impl | An OpenAPI document must have a paths, components or webhooks field. | "The OpenAPI document _MUST_ contain at least one paths field, a components field or a webhooks field."
- https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/
  NEW - nearest sys-constraint-not-valid | Add a NOT NULL constraint only after application changes are deployed, in a post-deployment migration. | "Adding a `NOT NULL` constraint requires that any application changes are deployed _first_"
- https://stripe.com/blog/online-migrations
  NEW - nearest chg-delete-legacy-after-migration | Make access to the removed old field raise an error so no code keeps using it. | "by raising an error if the property is called"
- https://www.postgresql.org/docs/current/sql-altertable.html
  NEW - nearest sys-constraint-not-valid | Setting NOT NULL scans the whole table unless NOT VALID is given, so plan for that scan. | "Ordinarily this is checked during the `ALTER TABLE` by scanning the entire table, unless `NOT VALID` is specified"
- https://about.gitlab.com/blog/gitlab-top-devops-tooling-metrics-and-targets/
  NEW - nearest code-test-selection-on-pr | Time to first actionable failure should be under 15 minutes. | "Our TtFF target is less than 15 minutes."
- https://about.gitlab.com/blog/gitlab-top-devops-tooling-metrics-and-targets/
  NEW - nearest code-flaky-test-quarantine | Master branch pipeline should pass above 95 percent of the time. | "Our target percentage for master pipeline stability is above 95%."
- https://abseil.io/resources/swe-book/html/ch15.html
  NEW - nearest chg-flag-owner-retirement | A deprecation process needs an explicit owner, or it will not progress. | "a deprecation process is unlikely to make meaningful progress"
- https://accessibility-manual.dwp.gov.uk/best-practice/automated-testing-using-axe-core-and-pa11y
  NEW - nearest code-a11y-check-in-ci | Log incomplete accessibility results for manual review rather than failing the test on them. | "you would not want to fail your tests if you had any"
- https://accessibility.arizona.edu/web-apps/cicd-testing
  NEW - nearest code-a11y-check-in-ci | Do not disable accessibility tests to make a build pass. | "Disable tests to make builds pass"
- https://accessibility.civicactions.com/posts/automated-accessibility-testing-leveraging-github-actions-and-pa11y-ci-with-axe
  NEW - nearest code-a11y-check-in-ci | Test every page listed in the sitemap, not only the homepage. | "which will be used by pa11y-ci to test all pages"
- https://airbnb.tech/infrastructure/migrating-airbnbs-jvm-monorepo-to-bazel/
  NEW - nearest code-build-hermetic | Run build actions in identical containers with strict resource limits. | "running actions in identical containers with strict resource limits"
- https://alloy.ai/speeding-up-integration-tests-db
  NEW - nearest code-test-fixtures-built-once | Give each test suite its own database so that suites cannot share state. | "our current version still uses a dedicated database per test suite"
- https://alloy.ai/speeding-up-integration-tests-db
  NEW - nearest code-test-fixtures-built-once | Tests must read back a created row's ID instead of assuming a hard-coded one. | "query for the created row and use its ID"
- https://android.googlesource.com/platform/frameworks/support/+/17957fcb324a42599abc868ffe8204a0384b2aee/camera/AGENTS.md
  NEW - nearest mod-mock-at-boundaries-only | Prefer fakes and test doubles over mocking frameworks such as Mockito. | "Prioritize the use of fakes and test doubles"
- https://android.googlesource.com/platform/frameworks/support/+/17957fcb324a42599abc868ffe8204a0384b2aee/camera/AGENTS.md
  NEW - nearest code-ci-gates | Format every changed Kotlin file with ktfmt before finishing. | "When modifying any .kt file, format it using `ktfmt`"
- https://android.googlesource.com/platform/frameworks/support/+/17957fcb324a42599abc868ffe8204a0384b2aee/camera/AGENTS.md
  NEW - nearest code-rule-has-enforcer | Keep commit titles to 50 characters and body lines to 72 characters. | "The commit title should not exceed 50 characters, and body lines should not exceed 72 characters."
- https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html
  NEW - nearest code-ci-gates | Require signed commits before code can be merged. | "the SCM should require commits to be signed before the code can be merged"
- https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html
  NEW - nearest code-secret-scan | Never print, log, or write secrets to shell history. | "secrets must not be printed out to the console, logged, or stored in a system's command history files"
- https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html
  NEW - nearest chg-tests-ship-with-change | A backported patch needs a reproducing test that fails unpatched and passes patched. | "A test reproducing the vulnerability must fail against the unpatched dependency and pass against the patched one"
- https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html
  NEW - nearest code-dependency-licence-sbom | Suppress a scanner alert only after the fix is verified, never by changing the version string. | "changing a version string so that the tool stops matching it"
- https://cloud.google.com/iam/docs/workload-identity-federation
  NEW - nearest code-workload-identity | Grant roles to the federated identity with fully qualified names and the project number | "Use fully qualified resource names when granting roles to external identities"
- https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/recommendations/miscellaneous-msc/msc12-c
  NEW - nearest code-dead-code | Enable compiler or linter warnings for code that has no effect or is never executed | "Most modern compilers, in many cases, can warn about code that has no effect or is never executed."
- https://designsystem.digital.gov/documentation/accessibility/
  NEW - nearest code-a11y-check-in-ci | Never convey meaning with a visual element alone (colour, icon) | "Never use visual elements alone to convey meaning"
- https://devguide.python.org/testing/run-write-tests/
  NEW - nearest py-test-hygiene | Run the test suite in random order to catch tests that interfere with each other | "The `-r` flag to the test runner causes it to run tests in a more random order"
- https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
  NEW - nearest code-adr | Code review checks each change against the ADRs it could violate | "During the code review, a code reviewer might find changes that violate one or more ADRs."
- https://docs.develocity.ai/current/using-develocity/predictive-test-selection/
  NEW - nearest code-test-selection-on-pr | Always run tests that were recently added, changed, failed or found flaky | "Develocity always selects tests that were recently added, changed, failed, or found flaky."
- https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/
  NEW - nearest code-ci-gates | Missing test coverage is a review warning, not a merge blocker | "Missing coverage should be considered a warning rather than a blocker and should be evaluated in context."
- https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/
  NEW - nearest py-test-hygiene | Models defined inside a test are bound to a temporary app registry, not the global one | "models defined in a test method should be bound to a temporary `Apps` instance"
- https://docs.gatling.io/concepts/assertions/
  NEW - nearest code-perf-budget-in-ci | Set an error-rate budget per request as well as a response-time budget | "Assert that every request has no more than 5% of failing requests"
- https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws
  NEW - nearest code-workload-identity | Grant id-token: write at the job or workflow that requests the token, not more broadly | "permission can be added at job level or workflow level"
- https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs
  NEW - nearest code-ci-gates | Job IDs must start with a letter or underscore and contain only alphanumerics, hyphens or underscores | "The `<job_id>` must start with a letter or `_` and contain only alphanumeric characters, `-`, or `_`."
- https://docs.github.com/en/actions/reference/security/secure-use
  NEW - nearest fn-no-eval-untrusted | Pass untrusted context values (such as PR titles) to scripts through an intermediate env variable, not inline in the script | "the preferred approach to handling untrusted input is to set the value of the expression to an intermediate environment variable"
- https://docs.github.com/en/code-security/securing-your-organization/understanding-your-organizations-exposure-to-vulnerabilities/prioritizing-dependabot-alerts-using-metrics
  NEW - nearest code-vuln-remediation-window | Do not close or dismiss a vulnerability alert solely because a reachability analysis says it is unreachable | "but do not close or dismiss an alert solely because of its verdict."
- https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
  NEW - nearest code-workflow-supply-chain | Commits pushed to a protected branch must be signed and verified | "contributors and bots can only push commits that have been signed and verified"
- https://docs.gitlab.com/ci/pipelines/
  NEW - nearest code-workflow-supply-chain | Only grant merge rights to protected branches to people allowed to reach deployment credentials | "Only assign users the right to merge to protected branches if they have permission to access sensitive information"
- https://docs.gitlab.com/ci/secrets/id_token_authentication/
  NEW - nearest code-workload-identity | Never use a mutable user name or email as the only trust-policy condition | "Do not rely on `user_login` or `user_email` as the only condition, because a user can change them."
- https://docs.gitlab.com/development/documentation/testing/links/
  NEW - nearest code-docs-refs-resolve | Links from UI code to documentation are checked by a linter (eslint, rubocop, haml-lint) | "Links to documentation from the GitLab UI, we use `haml-lint`, `eslint`, and `rubocop`."
- https://docs.gitlab.com/development/testing_guide/best_practices/
  NEW - nearest code-flaky-test-quarantine | A new test must be seen to fail in the expected way before it is asserted to pass | "When writing a new test, verify it fails in the way you expect before asserting it passes."
- https://docs.gitlab.com/development/testing_guide/best_practices/
  NEW - nearest code-flaky-test-quarantine | New spec files run in random order, and a spec that fails the order-dependence check must be fixed before it runs randomised | "All new spec files are run in random order to surface flaky tests that are dependent on test order."
- https://docs.gitlab.com/user/application_security/secret_detection/
  NEW - nearest code-secret-scan | Store secrets outside the repository, not only scan for them | "always store secrets outside of the repository"
- https://docs.kernel.org/process/coding-assistants.html
  NEW - nearest code-ai-pr-disclosure | AI agents must not add Signed-off-by tags | "AI agents MUST NOT add Signed-off-by tags."
- https://docs.kernel.org/process/coding-style.html
  NEW - nearest code-ci-gates | Reject trailing whitespace at line ends | "Do not leave trailing whitespace at the ends of lines."
- https://docs.kernel.org/process/generated-content.html
  NEW - nearest chg-review-rigour-by-risk | Scale review scrutiny with how much content a tool generated | "expect additional scrutiny in proportion to how much of it was generated."
- https://docs.spring.io/spring-framework/reference/testing/testcontext-framework/tx.html
  NEW - nearest code-flaky-test-quarantine | Preemptive timeouts need care around test-managed transactions | "Caution must be taken when using any form of preemptive timeouts"
- https://dropbox.tech/infrastructure/how-we-migrated-dropbox-from-nginx-to-envoy
  NEW - nearest code-ci-gates | Require 100% unit test coverage on every change | "Open source Envoy development requires changes to have 100% unit test coverage."
- https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents
  NEW - nearest chg-agent-grounded-code | Validate agent-written patches by running the real build and tests before accepting them. | "keeps the agent grounded in the real build and test environment instead of stopping after generating a plausible-looking patch"
- https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/
  NEW - nearest code-flaky-test-quarantine | Retry failed tests several times to separate consistent failures from flaky ones before using their outcomes. | "we aggressively retry failed tests when collecting training data"
- https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/
  NEW - nearest code-dead-code | Each deletion change explains the analysis that proves the code is dead. | "These change requests incorporate human-readable descriptions informing engineers about the analysis that determined the targeted code is provably dead."
- https://github.com/ai/size-limit
  NEW - nearest code-perf-budget-in-ci | Measure the budget as execution time in the browser, not as bytes alone, for JS apps. | "File size limit (in kB) is not the best way to describe your JS application cost"
- https://github.com/envoyproxy/envoy/blob/main/RELEASES.md
  NEW - nearest code-ci-gates | Keep backport and release history linear: manage changes by rebase, not merge | "change should be managed using rebase rather than merge"
- https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
  NEW - nearest code-ai-pr-disclosure | Contributions must contain no AI-generated images, video, audio or other media | "No AI-generated media is allowed (art, images, videos, audio, etc.)."
- https://github.com/github/docs/blob/main/src/links/README.md
  NEW - nearest code-docs-refs-resolve | Block links into private github/github URLs from public docs | "Ensures that we don't accidentally link to private `github/github` URLs in public documentation."
- https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md
  NEW - nearest code-ci-gates | Every added line of code should have unit test coverage, or the reason for lacking it is written down | "In principle every added code should have complete unit test coverage"
- https://github.com/kubernetes/sig-release/blob/master/release-blocking-jobs.md
  NEW - nearest code-flaky-test-quarantine | Every blocking CI job must have an owning team that responds to failures and an alert address | "Be Owned by a SIG, or other team, that is responsive to addressing failures"
- https://github.com/kubernetes/sig-release/blob/master/release-blocking-jobs.md
  NEW - nearest code-flaky-test-quarantine | A blocking CI job must pass at least 75% of its runs in a week | "Have passed 75% of all of its runs in a week"
- https://github.com/nodejs/node/blob/main/doc/contributing/releases.md
  NEW - nearest code-workflow-supply-chain | Every commit on a protected branch other than main and actions/* must be GPG-signed | "All commits to branches in `nodejs/node` other than `main` and `actions/*` MUST be signed"
- https://github.com/ossf/scorecard/blob/main/docs/checks.md
  NEW - nearest code-workflow-supply-chain | Set workflow token permissions read-only at top level and grant write per job | "the permissions definitions in each workflow's"
- https://github.com/rust-lang/rustc-dev-guide/blob/master/.github/workflows/ci.yml
  NEW - nearest code-workflow-supply-chain | Set the workflow's default token permissions to none at top level and grant write per job | "permissions: {}"
- https://go.dev/doc/articles/race_detector
  NEW - nearest go-test-race-in-ci | When test coverage is incomplete, run a `-race` binary under a realistic workload | "running a binary built with `-race` under a realistic workload"
- https://hexdocs.pm/ecto_sql/Ecto.Adapters.SQL.Sandbox.html
  NEW - nearest code-test-fixtures-built-once | Do not run concurrent sandbox tests on MySQL, only on PostgreSQL | "do not run concurrent tests with MySQL as you may run into deadlocks"
- https://laravel.com/docs/12.x/database-testing
  NEW - nearest code-test-fixtures-built-once | Prefer the transaction-based reset over DatabaseMigrations or DatabaseTruncation, which are slower | "significantly slower than the `RefreshDatabase` trait"
- https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops
  NEW - nearest code-test-selection-on-pr | When the selector cannot understand a change, run the full suite | "it falls back to running all tests"
- https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops
  NEW - nearest code-test-selection-on-pr | After a selected run, run the full suite and confirm it reports the same result | "If T1 passes, check that T2 passes as well"
- https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
  NEW - nearest code-adr | Never edit an accepted ADR; a changed decision gets a new record that supersedes and links the old one | "Don't go back and edit accepted records."
- https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
  NEW - nearest code-adr | Each record carries a status, Proposed, Accepted or Superseded | "Tracking status makes the current state of each decision clear"
- https://learn.microsoft.com/en-us/devops/operate/progressive-experimentation-feature-flags
  NEW - nearest code-dead-code | A flag kept after rollout keeps its code path tested and maintained | "it needs to be tested and maintained until the option is removed"
- https://learn.microsoft.com/en-us/devops/operate/progressive-experimentation-feature-flags
  NEW - nearest code-dead-code | Each feature flag definition names an owner, so its removal can be implicit | "specifying owner to allow implicit removal of features"
- https://nx.dev/ci/features/affected
  NEW - nearest code-test-selection-on-pr | Declare inputs and outputs for every task, since task selection reads them and undeclared tasks are missed | "Declare inputs and outputs, even for tasks you don 't cache."
- https://nx.dev/ci/features/affected
  NEW - nearest code-test-selection-on-pr | CI checkout must fetch full git history (fetch-depth 0) so a base commit exists to compare | "`fetch-depth: 0` is required. Without the full Git history, there is no base commit to compare against."
- https://pip.pypa.io/en/stable/topics/secure-installs/
  NEW - nearest code-dependency-pinning | Install only binary distributions, disallowing source distributions at install time | "Disallow source distributions, by passing `--only-binary :all:`"
- https://pip.pypa.io/en/stable/topics/secure-installs/
  NEW - nearest code-dependency-pinning | Do not install the project with setuptools' deprecated interfaces; use pip with --no-deps | "by calling `python setup.py install`, `python setup.py develop`, or `easy_install`."
- https://pkg.go.dev/golang.org/x/perf/cmd/benchstat
  NEW - nearest code-perf-budget-in-ci | Run each benchmark at least 10 times before comparing, to get a statistically significant sample | "Each benchmark should be run at least 10 times to gather a statistically significant sample of results."
- https://pkg.go.dev/golang.org/x/perf/cmd/benchstat
  NEW - nearest inc-perf-fix-has-profile-evidence | Do not read a statistically significant difference as a large one; judge a change by its size and p-value | "Note that \"statistically significant\" is not the same as \"large\""
- https://playwright.dev/docs/accessibility-testing
  NEW - nearest code-a11y-check-in-ci | Call waitFor on the target state before running the axe analyze, or the scan misses elements | "It is important to waitFor() the page to be in the desired"
- https://shopify.engineering/mobile-e2e-testing
  NEW - nearest fn-test-behaviour-not-implementation | Every E2E test action must carry an assertion or refutation, so a step cannot pass without checking the result | "Require every action to include an assertion or refutation"
- https://shopify.engineering/spark-joy-by-running-fewer-tests
  NEW - nearest code-test-selection-on-pr | Discourage new metaprogramming with a type checker and linters, not review comments alone. | "We discourage new metaprogramming through Sorbet and other linters."
- https://shopify.engineering/test-budget-time-constrained-ci-feedback
  NEW - nearest code-test-selection-on-pr | Select tests deterministically from the change's call graph; history-based ordering is a separate step. | "Test selection selects all tests that correspond to the given changes using a call graph deterministically."
- https://shopify.engineering/unreasonable-effectiveness-test-retries-android-monorepo-case-study
  NEW - nearest svc-retry-policy | Retry only the failed test, capped at three attempts, rather than the whole job. | "If we detect a failure in a test, that single test is retried up to three times."
- https://slack.engineering/build-better-software-to-build-software-better/
  NEW - nearest code-build-hermetic | Build scripts depend on no application code and add no build dependencies beyond the standard library. | "no links to our backend code, and no additional build dependencies."
- https://slack.engineering/build-better-software-to-build-software-better/
  NEW - nearest code-build-hermetic | Cache each build output independently, keyed only on its direct inputs. | "Each output artifact can be cached independently, keyed only on its direct inputs."
- https://slsa.dev/spec/v1.0/levels
  NEW - nearest code-workflow-supply-chain | Every build produces provenance naming the build platform, the build process and the top-level inputs. | "Provenance exists describing how the artifact was built, including the build platform, build process, and top-level inputs."
- https://statsig.com/blog/feature-flag-code-cleanup
  NEW - nearest chg-flag-owner-retirement | Fail CI when a feature flag passes its age limit. | "Fail CI if a flag is older than X months"
- https://stripe.dev/blog/sorbet-stripes-type-checker-for-ruby
  NEW - nearest typescript-strict-mode | Files marked strict must annotate every method signature, with no assumed-untyped arguments. | "Sorbet stops assuming `T.untyped` and instead requires signatures for all methods."
- https://stripe.dev/blog/sorbet-stripes-type-checker-for-ruby
  NEW - nearest code-ci-gates | CI reports, on each pull request, a count of non-test files not at the strict typing level, shown to author and reviewer. | "Number of non-test files which are not strictly typed (typed below `strict`)."
- https://tech.cabify.com/blog/engineering/acceptance-testing-go-services-using-aceptadora
  NEW - nearest code-test-fixtures-built-once | Before a test runs a destructive command, check that the target is the instance under test. | "(a CONFIG GET for Redis, a CALL in MySQL)"
- https://tech.cabify.com/blog/engineering/acceptance-testing-go-services-using-aceptadora
  NEW - nearest code-test-fixtures-built-once | Check each dependency is healthy before starting the service under test. | "we were now able to check their healthiness before starting the service."
- https://tech.cabify.com/blog/engineering/cabify-container-certification
  NEW - nearest code-workflow-supply-chain | Reject deploys of images without a valid signature at cluster admission, and re-check on each restart. | "Upon restart, expired signatures block deployment, forcing teams to rebuild and recertify."
- https://www.cisa.gov/resources-tools/resources/product-security-bad-practices
  NEW - nearest svc-mfa-step-up | Enable MFA by default for administrator accounts in the baseline product. | "Software manufacturers should require MFA for administrators"
- https://www.jetbrains.com/help/inspectopedia/CommentedOutCode.html
  NEW - nearest code-dead-code | Flag comment blocks that contain code, such as two or more lines of commented-out Java. | "Reports comments that contain Java code."
- https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-security-supply-chains-software-1
  NEW - nearest code-dependency-licence-sbom | Keep SBOMs in a standard format (SPDX, CycloneDX or SWID) so they can be ingested automatically. | "Ensure that SBOMs received from third-party suppliers conform to industry standard formats"
- https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-security-supply-chains-software-1
  NEW - nearest code-dependency-licence-sbom | Keep SBOMs in a readily accessible, digitally signed repository. | "Require software producers to maintain readily accessible and digitally signed SBOM repositories"
- https://www.stepsecurity.io/blog/pinning-github-actions-for-enhanced-security-a-complete-guide
  NEW - nearest code-workflow-supply-chain | Let Dependabot or Renovate propose updates for pinned actions. | "Tools like Dependabot and Renovate can integrate with GitHub repos and automate the process of identifying secure updates"
- https://www.typescriptlang.org/tsconfig/
  NEW - nearest code-dead-code | Set noUnusedLocals so unused local variables are reported as errors. | "Report errors on unused local variables."
- https://github.com/uber-go/guide/blob/master/style.md
  NEW - nearest go-wrap-errors-with-w | Production code returns errors instead of panicking. | "Code running in production must avoid panics."
- https://docs.rubocop.org/rubocop/latest/cops_metrics.html
  NEW - nearest fn-length-budget | Cyclomatic complexity per method must stay within a configured maximum. | "Checks that the cyclomatic complexity of methods is not higher than the configured maximum."
- https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html
  NEW - nearest code-file-lines-ceiling | The linter flags lines longer than the configured limit. | "line-too-long / C0301"
- https://firefox-source-docs.mozilla.org/testing/perfdocs/perf-sheriffing.html
  NEW - nearest code-perf-budget-in-ci | A test that exceeds its framework threshold raises an alert. | "Any time a test exceeds the threshold set for its framework, one or more alerts are generated."
- https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/performance-test
  NEW - nearest code-perf-budget-in-ci | Record a performance baseline and compare each later run's results against it | "In subsequent runs, compare new results against this baseline to detect performance changes."
- https://docs.djangoproject.com/en/5.1/topics/testing/tools/
  NEW - nearest py-test-hygiene | Tests that run database queries must use TransactionTestCase or TestCase, not SimpleTestCase | "If your tests make any database queries, use subclasses `TransactionTestCase` or `TestCase`."
- https://docs.pmd-code.org/latest/pmd_rules_java_design.html
  NEW - nearest fn-length-budget | Methods with cyclomatic complexity of 10 or more are reported and should be split | "By default, this rule reports methods with a complexity >= 10."
- https://docs.pmd-code.org/latest/pmd_rules_java_design.html
  NEW - nearest fn-length-budget | Avoid if-statements nested more than 3 levels deep | "Avoid creating deeply nested if-then statements since they are harder to read and error-prone to maintain."
- https://docs.pmd-code.org/latest/pmd_rules_java_design.html
  NEW - nearest mod-class-size-budget | Keep the count of unique types a class couples to within a threshold of 20 | "A number higher than the specified threshold can indicate a high degree of coupling."
- https://docs.sqlalchemy.org/en/20/orm/session_transaction.html#joining-a-session-into-an-external-transaction-such-as-for-test-suites
  NEW - nearest py-pytest-expensive-fixture-scope | Bind the test session to the outer connection with join_transaction_mode "create_savepoint" so every test rolls back | "the `Session.join_transaction_mode` parameter is passed with the setting"
- https://github.com/NVIDIA/Model-Optimizer/blob/main/CONTRIBUTING.md
  NEW - nearest py-test-collection-and-imports | Test filenames mirror the production module: tests for foo.py go in test_foo.py | "Test filenames must mirror the production module they primarily cover: tests for `foo.py` belong in `test_foo.py`."
- https://github.com/NVIDIA/Model-Optimizer/blob/main/CONTRIBUTING.md
  NEW - nearest mod-mock-at-boundaries-only | Prefer the highest-level test that runs the real code path over a mock-heavy test | "Choose an end-to-end test over a mock-heavy one"
- https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  NEW - nearest code-dependency-pinning | Obtain components only from official trusted sources and prefer signed packages | "Prefer signed packages to reduce the chance of including a modified, malicious component"
- https://go.dev/blog/supply-chain
  NEW - nearest code-ci-gates | Dependency-tree changes are made deliberately and go through code review | "so changes to dependency trees must be made deliberately and have the opportunity to go through code review."
- https://angular.dev/best-practices/security
  NEW - nearest fn-no-raw-html-sink | Never build a template by concatenating user input with template syntax | "Never create templates by concatenating user input and template syntax."
- https://angular.dev/best-practices/security
  NEW - nearest fn-no-raw-html-sink | Bypass Angular sanitization only after inspecting the value and confirming it is secure | "tell Angular that you inspected a value, checked how it was created, and made sure it is secure."
- https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization
  NEW - nearest code-ci-gates | Write authorization tests and do not deploy changes that fail them | "Write tests to evaluate the vulnerability of the authorization mechanism."
- https://baymard.com/blog/inline-form-validation
  NEW - nearest fn-error-says-what-and-how | Do not validate a field while the user is still typing it | "should not be checked before the user has had a chance to"
- https://baymard.com/blog/inline-form-validation
  NEW - nearest fn-error-says-what-and-how | Check each field's validity when the user leaves that field | "the validity of each field input should be checked when the user leaves the field"
- https://baymard.com/blog/inline-form-validation
  NEW - nearest fn-error-says-what-and-how | Remove an error message as soon as the input becomes valid | "disappearing the moment users enter a valid input"
- https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
  NEW - nearest svc-timeouts | Server sets both read and write timeouts when clients or networks are untrusted | "You should set both timeouts when you deal with untrusted clients and/or networks"
- https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/
  NEW - nearest go-http-client-timeout | Use net/http's higher-level timeouts, not SetDeadline called directly | "You probably don't want to call `SetDeadline` yourself"
- https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html
  NEW - nearest fn-jwt-verify-pinned | Do not take the verification key from the token unless it chains to a trust anchor for the issuer. | "Do not take the verification key from the token unless that key can be tied"
- https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
  NEW - nearest fn-no-shell-with-input | Avoid calling OS commands directly; use a library call when one exists. | "The primary defense is to avoid calling OS commands directly."
- https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
  NEW - nearest fn-no-shell-with-input | Commands that run must be validated against a fixed allowlist of allowed commands. | "these must be validated against a list of allowed commands."
- https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html
  NEW - nearest fn-no-prototype-pollution | Do not rely on Object.seal to stop writes to existing property values. | "Do not rely on sealing to prevent those modifications."
- https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
  NEW - nearest fn-xml-no-external-entities | Stop parsing when a required security setting fails; never catch the error and continue. | "Stop processing if any required security setting fails; do not catch the exception and continue parsing."
- https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
  NEW - nearest fn-no-native-deserialise-untrusted | Do not use XMLDecoder with untrusted input, since blocking entities does not remove its risk. | "Do not use `XMLDecoder` with untrusted input."
- https://codeql.github.com/codeql-query-help/python/py-template-injection/
  NEW - nearest fn-no-eval-untrusted | Where user input must build a template, use a sandboxed template environment | "This can be used if constructing a template from user input is absolutely necessary."
- https://community.owasp.org/attacks/Path_Traversal
  NEW - nearest fn-confine-file-path | Reject NUL bytes in path input, since they can truncate the filename before validation | "In many operating systems, null bytes `%00` can be injected to terminate the filename."
- https://design-system.service.gov.uk/components/date-input/
  NEW - nearest fn-related-controls-in-fieldset | Do not move focus automatically between date fields when one fills up | "Never automatically tab users between the fields of the date input"
- https://design-system.service.gov.uk/components/text-input/
  NEW - nearest fn-form-control-has-label | Do not set maxlength on text inputs; error only when the normalised value is over the limit | "Using the `maxlength` attribute means there is no feedback"
- https://design-system.service.gov.uk/patterns/validation/
  NEW - nearest fn-error-says-what-and-how | Do not validate a field when the user leaves it; validate on submit | "Do not validate when the user moves away from a field."
- https://dev.mysql.com/doc/refman/8.4/en/innodb-locking-reads.html
  NEW - nearest fn-no-check-then-act-across-await | Use SKIP LOCKED only for queue-like tables, never for general transactional reads | "`SKIP LOCKED` is therefore not suitable for general transactional work."
- https://developer.apple.com/videos/play/wwdc2020/10680/
  NEW - nearest fn-no-stringly-typed-returns | An Objective-C method that returns false must set its error out-parameter, never leave it nil | "if a method returns a false value, that's a failure even if the error value is"
- https://developer.apple.com/videos/play/wwdc2020/10680/
  NEW - nearest mod-subtype-passes-parent-tests | Each Objective-C class must mark at least one initializer as designated | "each class must choose to follow by marking at least one initializer as designated"
- https://developer.gnome.org/documentation/guidelines/programming/coding-style.html
  NEW - nearest fn-name-intermediate-conditions | Do not compare boolean values for equality with TRUE or FALSE | "Do not check boolean values for equality."
- https://developer.gnome.org/documentation/guidelines/programming/coding-style.html
  NEW - nearest mod-behaviour-lives-with-state | Do not export global variables as public API; expose getters and setters instead | "Avoid exporting variables as public API, since this is cumbersome on some platforms."
- https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
  NEW - nearest fn-native-button-or-link | Do not set a positive tabindex to reorder tab stops; keep the source order | "This is nearly always a bad idea, as it can cause major confusion."
- https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/JavaScript
  NEW - nearest fn-constant-time-secret-compare | Use == or != only as `== null`; otherwise use strict equality. | "If you need to use `==` or `!=`, remember that `== null` is the only acceptable case."
- https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText
  NEW - nearest fn-tls-verify-on | Clipboard writes work only in a secure context (HTTPS). | "Writing to the clipboard can only be done in a secure context."
- https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
  NEW - nearest fn-status-announced-live-region | Set aria-atomic="true" when the whole region content must be announced on each update. | "`aria-atomic="true"` ensures that each time the live region is updated, the entirety of the content is announced in full"
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises
  NEW - nearest fn-handle-rejected-promises | A nested catch covers only its own scope, so place it to limit what it silences. | "Nesting is a control structure to limit the scope of `catch` statements."
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/all
  NEW - nearest fn-independent-work-concurrent | Pass promises to Promise.all, not async functions, which it does not call. | "Directly passing the functions to `Promise.all` does not work, since they are not promises."
- https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent
  NEW - nearest fn-guard-uri-decoding | Replace + with spaces before decodeURIComponent when decoding query parameters. | "return decodeURIComponent(p.replace(/\+/g, " "));"
- https://developer.wordpress.org/reference/functions/esc_url/
  NEW - nearest fn-no-raw-html-sink | Always escape URLs written into output with esc_url, in text and attributes alike. | "Always use esc_url when escaping URLs (in text nodes, attribute nodes or anywhere else)."
- https://doc.rust-lang.org/book/ch11-03-test-organization.html
  NEW - nearest fn-test-behaviour-not-implementation | Put unit tests in a tests module in the same file, annotated with cfg(test). | "annotate the module with `cfg(test)`"
- https://docs.appian.com/suite/help/26.9/sail/ux-progressive-disclosure.html
  NEW - nearest fn-disclosure-hides-only-secondary | In sequential flows, disable fields that are not yet available rather than hiding them. | "For sequential steps, fields that are not yet available should be disabled and not hidden."
- https://docs.djangoproject.com/en/5.2/ref/request-response/
  NEW - nearest fn-resource-lifetime | Return a streamed iterator only through StreamingHttpResponse, not a plain response. | "you must use the `StreamingHttpResponse` class instead"
- https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/
  NEW - nearest fn-no-pass-through-wrapper | An overridden clean() must call the parent class's clean() to keep model validation. | "you must call the parent class’s `clean()` method."
- https://docs.djangoproject.com/en/stable/topics/db/optimization/
  NEW - nearest fn-fetch-only-needed-data | Drop a default ordering with order_by() when the code does not need the order. | "remove it on a `QuerySet` by calling `order_by()` with no parameters"
- https://docs.gitlab.com/ee/development/testing_guide/frontend_testing.html
  NEW - nearest chg-fix-root-cause-not-symptom | Every bug fix needs a regression test that stops the bug from recurring. | "Regression tests should be written for bug fixes to prevent them from recurring"
- https://docs.gitlab.com/ee/development/testing_guide/frontend_testing.html
  NEW - nearest chg-agent-mock-asserting-tests | Do not assert with toBeTruthy or toBeFalsy, which pass on null or false; use exact matchers. | "We should not use them because they make tests weaker and produce false-positive results"
- https://docs.pytest.org/en/stable/how-to/parametrize.html
  NEW - nearest fn-no-caller-mutation | Do not pass a mutable parameter value that a test case mutates, because later cases see the change. | "if you pass a list or a dict as a parameter value, and the test case code mutates it"
- https://docs.python.org/3/faq/programming.html
  NEW - nearest fn-name-intermediate-conditions | Write a conditional expression `a if c else b`, not the `c and a or b` idiom, which fails when `a` is falsy. | "it is always better to use the `... if ... else ...` form"
- https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects
  NEW - nearest fn-no-caller-mutation | Do not use a mutable object as a default argument; default to None and create the object inside the function. | "it is good programming practice to not use mutable objects as default values"
- https://docs.python.org/3/library/asyncio-dev.html
  NEW - nearest fn-no-blocking-call-in-async-code | Schedule callbacks from other OS threads with loop.call_soon_threadsafe | "To schedule a callback from another OS thread, the `loop.call_soon_threadsafe()` method should be used."
- https://docs.python.org/3/library/asyncio-dev.html
  NEW - nearest fn-no-blocking-call-in-async-code | Close async generators explicitly with aclose() when exiting early | "explicitly close the generator by calling its `aclose()` method"
- https://docs.python.org/3/library/re.html
  NEW - nearest fn-distinct-types-for-ids | Do not mix str patterns with bytes strings or the reverse | "Unicode strings and 8-bit strings cannot be mixed"
- https://docs.python.org/3/library/secrets.html
  NEW - nearest fn-csprng-for-secrets | Security tokens need at least 32 bytes (256 bits) of randomness | "32 bytes (256 bits) of randomness is sufficient"
- https://docs.python.org/3/library/subprocess.html
  NEW - nearest fn-no-shell-with-input | Use a fully qualified path for the executable, resolving names with shutil.which | "For maximum reliability, use a fully qualified path for the executable."
- https://docs.python.org/3/library/subprocess.html
  NEW - nearest fn-no-shell-with-input | When setting user= for a child process, also pass extra_groups=() to drop supplementary groups | "Specifying _user_ will not drop existing supplementary group memberships!"
- https://docs.python.org/3/library/typing.html#typing.NewType
  NEW - nearest fn-distinct-types-for-ids | NewType distinctness is enforced only by a static type checker, never at runtime | "Note that these checks are enforced only by the static type checker."
- https://docs.rs/regex/latest/regex/
  NEW - nearest fn-regex-compiled-once | Regex searches are worst-case O(m * n) time, with no look-around or backreferences, so untrusted patterns are bounded | "In exchange, all regex searches in this crate have worst case `O(m * n)` time complexity"
- https://docs.webkit.org/Deep%20Dive/Web%20Inspector/Compatibility.html
  NEW - nearest fn-comments-explain-why | Tag each frontend compatibility guard with `// COMPATIBILITY (<platform> <version>): <description>` naming the platform and the version lacking the feature | "// COMPATIBILITY (<platform> <version>): <description>"
- https://engineering.atspotify.com/2018/01/11/testing-of-microservices
  NEW - nearest mod-mock-at-boundaries-only | Do not let a test pass or fail on another system's correctness, and do not run other services in test environments | "A test that will pass or fail based on the correctness of another system."
- https://flink.apache.org/how-to-contribute/code-style-and-quality-common/
  NEW - nearest fn-length-budget | Flip an if-condition and exit early rather than nesting the main path inside several ifs | "Avoid deep nesting of scopes, by flipping the if condition and exiting early."
- https://flink.apache.org/how-to-contribute/code-style-and-quality-common/
  NEW - nearest fn-empty-collection-not-none | Annotate every nullable field, parameter and method type with @javax.annotation.Nullable, and use Optional for nullable returns | "All fields, parameters and method types that can be null should be annotated with `@javax.annotation.Nullable`."
- https://github.blog/engineering/platform-security/staying-evergreen-how-we-automated-secure-access-and-repo-hygiene-in-a-shared-org
  NEW - nearest fn-atomic-related-updates | Mark a multi-step revocation done only after every step succeeds; if any step fails, keep it pending for retry | "It only records \"revoked\" once every removal actually succeeded."
- https://github.com/PyCQA/flake8-bugbear#readme
  NEW - nearest fn-specific-exceptions-only | Do not assert with pytest.raises(Exception) or assertRaises(Exception) in tests; name the specific exception | "`pytest.raises(Exception)` should be considered evil."
- https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md
  NEW - nearest fn-bool-arg-at-callsite | Use a state machine or typed model instead of a second boolean that must stay in sync with the first | "a second boolean that must stay in sync with the first."
- https://github.com/mozilla-ai/any-llm/blob/main/AGENTS.md
  NEW - nearest py-modern-typing | Use the @override decorator from typing_extensions on every override of a base-class method | "always use the `@override` decorator from `typing_extensions`"
- https://github.com/mozilla-ai/any-llm/blob/main/AGENTS.md
  NEW - nearest py-pytest-parametrize | Write every test as a standalone function, never as a class-based group | "Do not use class-based test grouping"
- https://github.com/mozilla/eslint-plugin-no-unsanitized
  NEW - nearest fn-no-raw-html-sink | A call to the Sanitizer API setHTML() is allowed as a sink by default | "calls to `.setHTML()` are also allowed by default"
- https://go.dev/blog/go1.13-errors
  NEW - nearest go-wrap-errors-with-w | When a function documents returning an error wrapping a sentinel, do not return the underlying error directly | "do not return the underlying error directly."
- https://go.dev/blog/osroot
  NEW - nearest fn-confine-file-path | Do not validate a path and then open it in a second step; the two steps race against symlink changes | "this two-step process is vulnerable to TOCTOU races"
- https://go.dev/wiki/TableDrivenTests
  NEW - nearest fn-test-behaviour-not-implementation | A test failure message must report the actual result and the expected result | "its result and expected result are provided"
- https://google.github.io/styleguide/javaguide.html
  NEW - nearest fn-comments-survive-context | Do not name a person or team as the context of a TODO. | "Avoid adding TODOs that refer to an individual or team as the context:"
- https://google.github.io/styleguide/javaguide.html
  NEW - nearest fn-resource-lifetime | Do not override Object.finalize; finalization is scheduled for removal. | "Do not override `Object.finalize`. Finalization support is _scheduled for removal_."
- https://google.github.io/styleguide/pyguide.html
  NEW - nearest py-docstrings-google | A docstring is mandatory for every public, nontrivial or non-obvious function. | "A docstring is mandatory for every function that has one or more of the following properties:"
- https://google.github.io/styleguide/pyguide.html
  NEW - nearest py-docstrings-google | A docstring must let a caller write a call without reading the function's code. | "A docstring should give enough information to write a call to the function without reading the function’s code."
- https://google.github.io/styleguide/pyguide.html#212-default-argument-values
  NEW - nearest fn-no-caller-mutation | Do not use mutable objects as default argument values. | "Do not use mutable objects as default values in the function or method definition."
- https://inclusive-components.design/notifications/
  NEW - nearest fn-status-announced-live-region | Do not move focus to a non-actionable status message. | "it's important that focus is _not_ moved to such messages"
- https://inclusive-components.design/toggle-button/
  NEW - nearest fn-native-button-or-link | Give a button inside a form type="button" so it does not submit the form. | "But if you do use it inside a form"
- https://kotlinlang.org/docs/coding-conventions.html
  NEW - nearest py-frozen-dataclass-over-tuple | Declare locals and properties as val, not var, when they are not reassigned. | "Always declare local variables and properties as `val` rather than `var` if they are not modified after initialization."
- https://kotlinlang.org/docs/coding-conventions.html
  NEW - nearest fn-no-caller-mutation | Do not declare an infix method that mutates its receiver. | "Do not declare a method as `infix` if it mutates the receiver object."
- https://learn.microsoft.com/en-us/aspnet/core/security/preventing-open-redirects
  NEW - nearest svc-security-event-logging | Log the rejected URL when a non-local URL arrives where only a local one was expected. | "You can log the details of the URL that was provided when a non-local URL is supplied"
- https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api
  NEW - nearest svc-fail-closed-defaults | Enable the Swagger UI only in the development environment, never in production. | "Swagger is only enabled in a development environment."
- https://learn.microsoft.com/en-us/azure/architecture/antipatterns/busy-database/
  NEW - nearest fn-fetch-only-needed-data | Keep formatting and business processing out of database queries; the database should do data access. | "Ideally, you should limit the database to performing data access operations"
- https://learn.microsoft.com/en-us/dotnet/csharp/fundamentals/strings/common-tasks/concatenate
  NEW - nearest fn-join-dont-concat-in-loop | Embed values with string interpolation, not `+` chains or positional `{0}` placeholders. | "prefer string interpolation over positional placeholders like the `{0}` and `{1}` tokens"
- https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex
  NEW - nearest svc-sqli-authn | Never build a regex pattern from untrusted input; escape user text with Regex.Escape. | "applications should not create regular expression patterns from untrusted user-provided values"
- https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-regex
  NEW - nearest svc-timeouts | Give regexes that see untrusted input a match timeout or RegexOptions.NonBacktracking. | "Features such as time-out values and RegexOptions.NonBacktracking"
- https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum
  NEW - nearest fn-no-stringly-typed-returns | Keep sentinel values out of an enum; its members must be real values of the set. | "DO NOT include sentinel values in enums."
- https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum
  NEW - nearest fn-no-stringly-typed-returns | Apply FlagsAttribute to flag enums only, never to simple enums. | "DO apply the System.FlagsAttribute to flag enums. Do not apply this attribute to simple enums."
- https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
  NEW - nearest fn-jwt-verify-pinned | Clients must treat access tokens as opaque strings and not validate them. | "Although client applications can receive and use access tokens, they should treat them as opaque strings."
- https://learn.snyk.io/lesson/prototype-pollution/
  NEW - nearest fn-no-prototype-pollution | Freeze Object.prototype so the shared default prototype cannot be changed. | "We can freeze the default prototype by invoking `Object.freeze(Object.prototype)`"
- https://llvm.org/docs/CodingStandards.html
  NEW - nearest fn-specific-exceptions-only | Do not use C++ exceptions or RTTI such as dynamic_cast in the code base. | "LLVM does not use exceptions or RTTI"
- https://llvm.org/docs/CodingStandards.html
  NEW - nearest fn-length-budget | Do not use else or else if after return, break, continue or goto. | "please do not use `'else'` or `'else if'` after something that interrupts control flow"
- https://llvm.org/docs/CodingStandards.html
  NEW - nearest py-no-cast | Use static_cast, reinterpret_cast or const_cast, not C-style casts. | "use `static_cast`, `reinterpret_cast`, and `const_cast`, rather than C-style casts."
- https://moodledev.io/general/development/policies/codingstyle
  NEW - nearest fn-bool-arg-at-callsite | Name variables and flags positively (allow, enable), not negated (prevent). | "Use **positive** variables names always (allow, enable not prevent, disable)."
- https://moodledev.io/general/development/policies/codingstyle
  NEW - nearest fn-bool-arg-at-callsite | Default an optional argument to null, not false, when no default is needed. | "Use `null` as the default value instead of `false` for situations like this where a default value isn't needed."
- https://mypy.readthedocs.io/en/stable/typed_dict.html
  NEW - nearest fn-known-keys-get-a-type | Annotate a TypedDict variable explicitly; without the annotation mypy infers a plain dict. | "without it, mypy will try to infer a regular, uniform `dict` type for `movie`"
- https://mypy.readthedocs.io/en/stable/typed_dict.html
  NEW - nearest fn-known-keys-get-a-type | Use only string literals as TypedDict keys; a computed key cannot be checked. | "You can only use string literals as `TypedDict` keys."
- https://nodejs.org/api/cli.html
  NEW - nearest mod-validate-at-boundary-once | Never load a configuration file from an untrusted source; Node does no validation on it. | "so **NEVER** use untrusted configuration files."
- https://nodejs.org/api/crypto.html
  NEW - nearest mod-vetted-crypto-only | Call setAAD before update on an authenticated cipher or decipher. | "The `cipher.setAAD()` method must be called before `cipher.update()`."
- https://nodejs.org/api/crypto.html
  NEW - nearest mod-vetted-crypto-only | Read the auth tag only after final has run on the cipher. | "should only be called after encryption has been completed using the `cipher.final()` method"
- https://nodejs.org/api/crypto.html
  NEW - nearest mod-pooled-clients-built-once | Import key material into a KeyObject once and reuse it, rather than re-parsing PEM on each call. | "import key material into a`KeyObject` once and reuse it"
- https://nodejs.org/api/querystring.html
  NEW - nearest fn-no-prototype-pollution | Do not call Object methods such as hasOwnProperty on a querystring.parse result; it has no prototype. | "This means that typical `Object` methods such as `obj.toString()`, `obj.hasOwnProperty()`, and others are not defined"
- https://nodejs.org/en/learn/asynchronous-work/dont-block-the-event-loop
  NEW - nearest fn-no-blocking-call-in-async-code | Avoid nested quantifiers such as (a+)* in regexps applied to input, since they can block the loop. | "Avoid nested quantifiers like `(a+)*`."
- https://peps.python.org/pep-0589/
  NEW - nearest fn-known-keys-get-a-type | A TypedDict class body holds only key: type lines; no methods. | "Methods are not allowed, since the runtime type of a TypedDict object will always be just `dict`"
- https://peps.python.org/pep-0589/
  NEW - nearest fn-known-keys-get-a-type | Never use isinstance or issubclass with a TypedDict type; they are not supported. | "TypedDict types can’t be used in `isinstance()` or `issubclass()` checks."
- https://pkg.go.dev/crypto/subtle
  NEW - nearest fn-constant-time-secret-compare | Wrap only code written with constant-time operations in WithDataIndependentTiming; it does not fix variable-time code. | "WithDataIndependentTiming does not make variable-time code constant-time."
- https://pkg.go.dev/crypto/subtle
  NEW - nearest fn-constant-time-secret-compare | Pass only 0 or 1 as the selector to ConstantTimeSelect or ConstantTimeCopy. | "Its behavior is undefined if v takes any other value."
- https://pkg.go.dev/crypto/tls#Config
  NEW - nearest fn-tls-verify-on | Keep KeyLogWriter unset outside debugging; it compromises TLS security. | "Use of KeyLogWriter compromises security and should only be"
- https://pkg.go.dev/io#LimitReader
  NEW - nearest go-wrap-errors-with-w | Return io.EOF unwrapped from Read, since callers compare it with ==; wrapping breaks that. | "Read must return EOF itself, not an error wrapping EOF, because callers will test for EOF using =="
- https://pkg.go.dev/io#LimitReader
  NEW - nearest fn-bounded-read-fails-at-cap | Return ErrUnexpectedEOF or a more detailed error when EOF arrives mid-structure, not plain EOF. | "the appropriate error is either ErrUnexpectedEOF or some other error giving more detail"
- https://pkg.go.dev/os/exec
  NEW - nearest fn-no-shell-with-input | Run a program from the current directory as ./prog, never as a bare name resolved through PATH | "Code that always wants to run a program from the current directory"
- https://pkg.go.dev/os/exec
  NEW - nearest fn-resource-lifetime | Never call Cmd.Wait concurrently from multiple goroutines | "Wait must not be called concurrently from multiple goroutines."
- https://pkg.go.dev/regexp
  NEW - nearest fn-regex-compiled-once | Do not call Regexp.Copy to avoid lock contention; it is no longer needed | "As of Go 1.12, using Copy is no longer necessary to avoid lock contention."
- https://pkg.go.dev/regexp
  NEW - nearest fn-regex-compiled-once | Write regex literals with backslashes as raw strings | "Use raw strings to avoid having to quote the backslashes"
- https://pkg.go.dev/strings#Builder
  NEW - nearest fn-join-dont-concat-in-loop | Never copy a non-zero strings.Builder by value | "Do not copy a non-zero Builder."
- https://pkg.go.dev/strings#Builder
  NEW - nearest inc-perf-fix-has-profile-evidence | Use strings.Clone only when a profile shows it is needed | "Clone should typically be used only rarely, and only when profiling indicates that it is needed"
- https://portswigger.net/kb/issues/00500100_open-redirection-reflected
  NEW - nearest fn-redirect-target-allowlist | Replace redirect endpoints with direct links to the target where possible | "Remove the redirection function from the application, and replace links to it with direct links"
- https://portswigger.net/web-security/prototype-pollution/preventing
  NEW - nearest fn-no-prototype-pollution | Do not rely on a key blocklist such as `__proto__` as the fix | "we only recommend this as a stopgap rather than a long-term solution"
- https://portswigger.net/web-security/server-side-template-injection
  NEW - nearest fn-no-eval-untrusted | Use a logic-less template engine such as Mustache unless logic is absolutely necessary | "always use a \"logic-less\" template engine, such as Mustache, unless absolutely necessary"
- https://portswigger.net/web-security/server-side-template-injection
  NEW - nearest fn-no-eval-untrusted | Do not let users modify or submit new templates | "to not allow any users to modify or submit new templates"
- https://portswigger.net/web-security/xxe
  NEW - nearest fn-xml-no-external-entities | Treat SVG and DOCX uploads as XML and parse them with the hardened parser | "Since the SVG format uses XML, an attacker can submit a malicious SVG image"
- https://primer.style/product/components/dialog/accessibility
  NEW - nearest fn-dialog-focus-managed | A modal dialog has an accessible, visible title and role dialog with aria-modal | "Modal Dialogs must be announced as dialogs by screen readers and have an accessible title"
- https://project.pages.drupalcode.org/coding_standards/
  NEW - nearest code-consistency-drift | New code follows the current coding standards regardless of version | "All new code should follow the current standards, regardless of (core) version."
- https://raw.githubusercontent.com/remix-run/react-router/main/packages/react-router/lib/router/utils.ts
  NEW - nearest fn-guard-uri-decoding | Re-encode a slash inside a decoded path segment as %2F, so one segment stays one segment. | "replace(/\//g, "%2F")"
- https://react.dev/learn/updating-objects-in-state
  NEW - nearest fn-no-caller-mutation | A nested state update copies every level above the change, because spread copies are shallow. | "To update a nested object, you need to create copies all the way up from the place you’re updating."
- https://refactoring.guru/smells/comments
  NEW - nearest fn-comments-explain-why | State the invariants the system needs with an assertion, not a comment. | "If you need to assert rules about a state that’s necessary for the system to work, use Introduce Assertion."
- https://rust-lang.github.io/api-guidelines/type-safety.html
  NEW - nearest fn-no-stringly-typed-returns | Use a bitflags type, not an enum, for a set of independent flags. | "Types for a set of flags are `bitflags`, not enums (C-BITFLAG)"
- https://stripe.dev/blog/how-stripe-uses-graph-search-and-state-machines-to-auto-remediate-a-global-database-fleet
  NEW - nearest fn-rerun-safe-after-crash | Check every intermediate state of a multi-step plan against safety invariants before accepting the plan. | "Each path is validated against invariants at every intermediate step."
- https://stripe.dev/blog/how-stripe-uses-graph-search-and-state-machines-to-auto-remediate-a-global-database-fleet
  NEW - nearest mod-inject-boundary-collaborators | Run one business-logic path in production and in simulation, behind an interface, so the planner cannot drift from execution. | "There’s no separate planning codebase that could diverge from the execution codebase."
- https://swehb.nasa.gov/display/SWEHBVD/5.14+-+Test+-+Software+Test+Procedures
  NEW - nearest fn-test-oracle-independent | Name every requirement that each test procedure verifies. | "Identify in each test procedure all requirements being verified by that test procedure."
- https://swehb.nasa.gov/display/SWEHBVD/5.14+-+Test+-+Software+Test+Procedures
  NEW - nearest fn-test-behaviour-not-implementation | Include negative tests that confirm the software does not do what it should not do. | "Confirm the software does not do what it should not do."
- https://tech.gr.vodafone.com/post/junit-parameterized-tests
  NEW - nearest py-pytest-parametrize | Give each parameterized case a readable name, so a failing run shows its inputs. | "use the third parameter as the test name"
- https://testdesiderata.com/
  NEW - nearest code-flaky-test-quarantine | Tests are deterministic: the same code gives the same result on every run. | "if nothing changes, the test result shouldn’t change."
- https://typescript-eslint.io/rules/no-floating-promises/
  NEW - nearest fn-handle-rejected-promises | Handle an array of promises as one promise, via Promise.all, allSettled, any or race. | "The main way to resolve this is by using one of the Promise concurrency methods"
- https://use-the-index-luke.com/sql/clustering/index-only-scan-covering-index
  NEW - nearest chg-new-query-has-plan | Do not add columns to an index for an index-only scan on suspicion alone; index the WHERE clause first. | "Do not design an index for an index-only scan on suspicion only"
- https://vitest.dev/guide/mocking/modules
  NEW - nearest typescript-mock-at-the-boundary | Do not expect a mock to replace calls a module makes to its own functions in the same file. | "it is not possible to mock calls to methods that are called inside other methods of the same file"
- https://web.dev/articles/async-clipboard
  NEW - nearest fn-bool-arg-at-callsite | Pass allowWithoutGesture explicitly in clipboard permission queries, since its default differs by browser. | "The default for this value varies by browser, so you should always include it."
- https://web.dev/articles/async-clipboard
  NEW - nearest svc-csp-strict-script-src | Iframes using the Clipboard API need an allow attribute listing clipboard-read and/or clipboard-write. | "you need to pass either or both of `clipboard-read` or `clipboard-write`"
- https://web.dev/articles/trusted-types
  NEW - nearest fn-no-raw-html-sink | Use the default Trusted Types policy sparingly; prefer named policies close to the data. | "Use the default policy sparingly, and prefer refactoring the application to use regular policies instead."
- https://web.dev/learn/accessibility/aria-html
  NEW - nearest fn-aria-role-has-state-and-keys | Never put aria-hidden="true" or role="presentation" on an element that needs focus. | "Don't add `role= "presentation"` or `aria-hidden= "true"` to elements that need to have focus"
- https://webaim.org/techniques/aria/
  NEW - nearest fn-aria-role-has-state-and-keys | Do not hide focused elements with CSS or with aria-hidden="true". | "Do not hide focused elements with CSS or with `aria-hidden="true"`."
- https://webaim.org/techniques/aria/
  NEW - nearest fn-form-control-has-label | A role="region" must have an aria-label or aria-labelledby that gives it a descriptive name. | "It must have a descriptive accessible name defined using `aria-label` or `aria-labelledby`"
- https://webaim.org/techniques/forms/advanced
  NEW - nearest fn-form-control-has-label | Use only one invisible-label technique; stacking a hidden label with a title repeats text to screen readers. | "Only one of these recommendations should be implemented."
- https://webaim.org/techniques/forms/advanced
  NEW - nearest fn-form-control-has-label | Do not add aria-labelledby to a control that already has a label element; the label is never announced. | "Screen reader users will never hear the `<label>` text."
- https://www.attrs.org/en/stable/why.html
  NEW - nearest py-frozen-dataclass-over-tuple | Do not hand-write __init__, __repr__, __eq__ and __hash__ boilerplate; use attrs or a dataclass. | "writing the same nine methods again and again doesn’t qualify"
- https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-cross-site-scripting-vulnerabilities
  NEW - nearest code-ci-gates | Automate a block on unsafe functions and run static analysis over how user input is handled. | "Automated safeguards should be implemented to prevent software from utilizing unsafe functions"
- https://www.django-rest-framework.org/api-guide/serializers/
  NEW - nearest mod-validate-at-boundary-once | Call is_valid() before reading validated_data or calling save(). | "you always need to call `is_valid()` before attempting to access the validated data"
- https://www.django-rest-framework.org/api-guide/serializers/
  NEW - nearest mod-validate-at-boundary-once | On partial updates, read fields missing from data in validate() from self.instance. | "To access fields not included in the partial update, you should retrieve them from the existing object instance using `self.instance`"
- https://www.django-rest-framework.org/api-guide/serializers/
  NEW - nearest fn-no-mass-assignment | Write create() and update() explicitly for nested writes; the default ModelSerializer methods do not support them. | "The default `ModelSerializer` `.create()` and `.update()` methods do not include support for writable nested representations."
- https://www.nngroup.com/articles/confirmation-dialog/
  NEW - nearest fn-destructive-confirm-or-undo | Make each confirmation specific: name the item and its consequence, never a bare "Are you sure?". | "Do not ask _Are you sure you want to do this?_ Instead, explain what _this_ is"
- https://www.nngroup.com/articles/confirmation-dialog/
  NEW - nearest fn-destructive-confirm-or-undo | Do not give a confirmation dialog a default Yes answer. | "Avoid giving confirmation dialogs a **default** _Yes_ answer."
- https://www.nngroup.com/articles/progressive-disclosure/
  NEW - nearest fn-disclosure-hides-only-secondary | Keep disclosure to two levels; beyond two, simplify the design or group the features. | "designs that go beyond 2 disclosure levels typically have low usability"
- https://www.nngroup.com/articles/web-form-design/
  NEW - nearest fn-destructive-confirm-or-undo | Avoid Reset and Clear buttons, since accidental deletion of entered data outweighs the rare need to start over. | "Avoid _Reset_ and _Clear_ buttons"
- https://www.postgresql.org/docs/current/applevel-consistency.html
  NEW - nearest fn-no-check-then-act-across-await | A locking read does not stop a concurrent update or delete; the row must actually be updated while locked. | "`SELECT FOR UPDATE` does not ensure that a concurrent transaction will not update or delete a selected row"
- https://www.pulumi.com/docs/iac/concepts/secrets/
  NEW - nearest code-secret-scan | Store a secret config value encrypted (set with a secret flag), never as plain text. | "encrypts the data and stores the resulting ciphertext instead of plain text"
- https://www.pulumi.com/docs/iac/concepts/secrets/
  NEW - nearest fn-mask-credentials-in-output | Read secret values with the secret variant of the config getter so they stay marked as secret. | "Use the secret variants of the configuration APIs instead"
- https://www.rfc-editor.org/rfc/rfc4086.html
  NEW - nearest fn-csprng-for-secrets | Passing statistical randomness tests does not prove a value is unpredictable enough for security. | "Statistically tested randomness in the traditional sense is NOT the same as the unpredictability required for security use."
- https://www.rfc-editor.org/rfc/rfc8725
  NEW - nearest fn-jwt-verify-pinned | Do not generate or consume unsigned "none" JWTs unless the caller explicitly asks for them. | "JWT libraries SHOULD NOT generate JWTs using \"none\" unless explicitly requested to do so by the caller."
- https://www.rfc-editor.org/rfc/rfc8725
  NEW - nearest fn-jwt-verify-pinned | Never use a human-memorable password directly as an HS256 key. | "human-memorizable passwords MUST NOT be directly used as the key"
- https://www.rfc-editor.org/rfc/rfc9110.html#name-413-content-too-large
  NEW - nearest fn-link-url-scheme-allowlist | Reject a received https URI reference with an empty host as invalid before using it. | "A recipient that processes such a URI reference MUST reject it as invalid."
- https://www.rfc-editor.org/rfc/rfc9110.html#name-413-content-too-large
  NEW - nearest fn-bounded-read-fails-at-cap | A parser must handle protocol lengths at least as long as the values it generates itself. | "At a minimum, a recipient MUST be able to parse and process protocol element lengths"
- https://www.swift.org/documentation/api-design-guidelines/
  NEW - nearest fn-name-intermediate-conditions | Name boolean methods and properties so they read as assertions about the receiver when nonmutating. | "Uses of Boolean methods and properties should read as assertions about the receiver"
- https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
  NEW - nearest fn-dialog-focus-managed | Mark a dialog aria-modal only when code blocks outside interaction and visuals obscure the outside content. | "Application code prevents all users from interacting in any way with content outside of it."
- https://www.w3.org/WAI/ARIA/apg/patterns/switch/
  NEW - nearest fn-form-control-has-label | Keep a switch's label unchanged while its state changes. | "it is critical the label on a switch does not change when its state changes."
- https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
  NEW - nearest fn-native-button-or-link | Do not put a role on a native element that overrides its meaning, such as role=log on a table. | "Authors can inadvertently override accessibility semantics."
- https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
  NEW - nearest fn-focus-indicator-visible | When a focusable component gets keyboard focus, author content must not entirely hide it. | "the component is not entirely hidden due to author-created content"
- https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
  NEW - nearest fn-dialog-focus-managed | A non-modal overlay that takes no focus and never closes on focus loss can hide focusable items. | "A dialog-like overlay that does not take focus on appearance"
- https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
  NEW - nearest fn-dialog-focus-managed | Dialogs and menus sit next to their trigger in the sequential focus order. | "dialogs or menus that are not adjacent to their trigger control in the sequential navigation order"
- https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
  NEW - nearest fn-no-positive-tabindex | A control must not receive focus twice because focusable elements are nested. | "a control appearing to receive focus multiple times due to the use of nested focusable elements"
- https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
  NEW - nearest fn-focus-indicator-visible | Do not use script to remove focus from an element when it receives focus. | "using script to remove focus when focus is received"
- https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
  NEW - nearest fn-heading-structure | In data tables, scope header cells so they associate with their data cells. | "H63: Using the scope attribute to associate header cells with data cells in data tables"
- https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  NEW - nearest fn-form-control-has-label | Give each custom user interface control a name, for example through aria-labelledby. | "ARIA16: Using aria-labelledby to provide a name for user interface controls"
- https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html
  NEW - nearest fn-dialog-focus-managed | If leaving a component needs more than Tab or arrows, tell the user the key that does it. | "the user is advised of the method for moving focus away"
- https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
  NEW - nearest fn-colour-not-sole-cue | A lightness difference counts as a second cue only at a contrast ratio of 3:1 or greater. | "the difference in relative luminance between the colors leads to a contrast ratio of 3:1 or greater"
- https://www.w3.org/WAI/tutorials/forms/grouping/
  NEW - nearest fn-related-controls-in-fieldset | Group long select options with optgroup, labelled by its label attribute. | "The `label` attribute of the `optgroup` element is used to provide a label for the group."
- https://www.w3.org/WAI/tutorials/forms/labels/
  NEW - nearest fn-form-control-has-label | Hide a visually redundant label with a clip pattern, not display:none, so assistive tech still reads it. | "keep the information technically visible but practically hidden"
- https://www.w3.org/WAI/tutorials/forms/notifications/
  NEW - nearest fn-error-says-what-and-how | After a failed submit, set focus to the first input that contains an error | "set the focus to the first `<input>` element that contains an error"
- https://www.w3.org/WAI/tutorials/page-structure/headings/
  NEW - nearest fn-heading-structure | Use aria-labelledby to tie each heading to the page region it labels | "Use `aria-labelledby` to associate headings with their page region"
- https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
  NEW - nearest code-secret-scan | Do not hard-code keys into the application source code | "Do not hard-code keys into the application source code."
- https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md
  NEW - nearest fn-length-budget | If a method can be meaningfully extracted into another named method, it does more than one thing | "If I can *meaningfully* extract one method from another, then the original method did more than one thing."
- https://google.github.io/styleguide/cppguide.html
  NEW - nearest mod-bounded-fan-out | Do not rely on transitive includes; a file includes each header that provides a symbol it uses | "Do not rely on transitive inclusions."
- https://google.github.io/styleguide/cppguide.html
  NEW - nearest fn-length-budget | Define a function in a header only if it is short, 10 lines or fewer | "Only define a function at its public declaration if it is short, say, 10 lines or fewer."
- https://google.github.io/styleguide/cppguide.html
  NEW - nearest none | Do not use using-directives such as `using namespace foo` | "Do not use _using-directives_ (e.g., `using namespace foo`)."
- https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices
  NEW - nearest fn-test-oracle-independent | Keep logic such as if, for, while and switch out of unit tests | "avoid manual string concatenation, logical conditions, such as `if`, `while`, `for`, and `switch`"
- https://www.a11yproject.com/checklist/
  NEW - nearest fn-error-says-what-and-how | List form errors above the form after submit, each linking to its invalid field | "Make sure that form input errors are displayed in list above the form after submission."
- https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  NEW - nearest svc-authz-central-deny-default | Never rely on client-side access control checks; enforce them on the server, gateway or serverless function | "Developers must never rely on client-side access control checks."
- https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  NEW - nearest svc-authz-central-deny-default | Only authorized users may upload files | "Only allow authorized users to upload files"
- https://design-system.service.gov.uk/components/error-summary/
  NEW - nearest fn-error-says-what-and-how | Always show an error summary when there is a validation error, even if there is only one | "Always show an error summary when there is a validation error, even if there’s only one."
- https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
  NEW - nearest fn-jwt-verify-pinned | When restricting access to members of certain domains, check the hd claim | "This must be used when restricting access to a resource to only members of certain domains."
- https://nodejs.org/api/http.html
  NEW - nearest fn-header-value-encoding | Compute Content-Length in bytes with Buffer.byteLength, not string length. | "`Content-Length` value should be in bytes, not characters. Use `Buffer.byteLength()`"
- https://nodejs.org/api/http.html
  NEW - nearest fn-bounded-read-fails-at-cap | Consume every response body that a response listener receives, by reading, a data handler or resume. | "the data from the response object **must** be consumed"
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228-upd1.pdf
  NEW - nearest svc-security-headers | Encrypt all API traffic in transit to keep messages authentic and private. | "Encryption in transit — To ensure message authenticity and prevent eavesdropping"
- https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228-upd1.pdf
  NEW - nearest svc-authn-by-default | Authenticate the calling service's identity on every API call, not only the end user. | "Authenticate the calling service"
- https://pages.nist.gov/800-63-4/sp800-63b.html
  NEW - nearest fn-password-slow-hash | Require at least 15 characters for passwords used as the single authentication factor. | "require passwords that are used as a single-factor authentication mechanism to be a minimum of 15 characters"
- https://pkg.go.dev/golang.org/x/sync/errgroup
  NEW - nearest fn-independent-work-concurrent | Cancel the shared context when the first task in a group fails. | "will cancel the associated Context"
- https://web.dev/articles/cls
  NEW - nearest fn-reduced-motion-respected | Animate with transform rather than top, right, bottom or left, to avoid layout shifts. | "avoid changing the `top`, `right`, `bottom`, or `left` properties"
- https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  NEW - nearest fn-header-value-encoding | Use structured log formats, since CR and LF in unstructured log text allow log injection. | "unstructured text log formats are susceptible to log entry injection through Carriage Return (CR) or Line Feed (LF) characters"
- https://www.cs.umd.edu/users/ben/goldenrules.html
  NEW - nearest fn-keep-input-on-error | An erroneous action leaves the interface state unchanged, or the UI gives steps to restore it | "Erroneous actions should leave the interface state unchanged"
- https://www.nngroup.com/articles/ten-usability-heuristics/
  NEW - nearest fn-destructive-confirm-or-undo | Give the user a clear, labelled exit from the current interaction | "Show a clear way to exit the current interaction"
- https://design-system.service.gov.uk/components/error-message/
  NEW - nearest fn-error-says-what-and-how | Summarise all validation errors in an error summary at the top of the page | "Summarise all errors at the top of the page the user is on"
- https://docs.djangoproject.com/en/stable/ref/models/querysets/
  NEW - nearest sys-n-plus-one-pooling | Use select_related only for single-valued relations; many-valued ones need prefetch_related | "`select_related` is limited to single-valued relationships - foreign key and one-to-one."
- https://slack.engineering/break-stuff-on-purpose/
  NEW - nearest inc-rollback-path-tested | Alert when a scheduled backup fails or stops running | "it didn’t have alerts to tell us if it wasn’t running correctly"
- https://slack.engineering/break-stuff-on-purpose/
  NEW - nearest code-documented-setup-runs | Keep each recovery runbook accurate to the system it describes | "our runbook was out of date"
- https://slack.engineering/deploy-safety/
  NEW - nearest sys-cells-limit-blast-radius | Catch a problematic deployment before it reaches 10% of the fleet | "Detect problematic deployments prior to reaching 10% of the fleet"
- https://sre.google/sre-book/effective-troubleshooting/
  NEW - nearest inc-rollback-path-tested | Mitigate user impact first (divert, shed, disable) and root-cause afterwards | "Stopping the bleeding should be your first priority"
- https://sre.google/sre-book/effective-troubleshooting/
  NEW - nearest svc-request-id-logging | Log every new version deployment and configuration change at every layer of the stack | "Well-designed systems should have extensive production logging to track new version deployments and configuration changes"
- https://sre.google/sre-book/postmortem-culture/
  NEW - nearest inc-postmortem-owned-actions | Every postmortem draft is reviewed before it is finalised | "To ensure that each completed draft is reviewed, we encourage regular review sessions"
- https://www.brendangregg.com/usemethod.html
  NEW - nearest inc-perf-fix-has-profile-evidence | Check utilization, saturation and errors for every resource in the system | "For every resource, check utilization, saturation, and errors."
- https://www.brendangregg.com/usemethod.html
  NEW - nearest prod-alerts-symptoms-golden-signals | Long averages can hide bursts that saturate a resource; check the short-interval peaks | "A burst of high utilization can cause saturation and performance issues"
- https://blog.cloudflare.com/5-december-2025-outage/
  NEW - nearest svc-update-rollback-on-failure | Roll out configuration gradually with health validation and quick rollback | "This includes health validation and quick rollback capabilities among other things."
- https://blog.cloudflare.com/5-december-2025-outage/
  NEW - nearest sys-secrets-and-errors | On corrupt config, log and fall back to a known-good state instead of dropping requests (conflicts with the fail-closed card) | "the system will log the error and default to a known-good state or pass traffic without scoring, rather than dropping requests."
- https://dropbox.tech/infrastructure/disaster-readiness-test-failover-blackhole-sjc
  NEW - nearest inc-rollback-path-tested | Express a failover runbook as an explicit task graph that can be rerun, skipping completed tasks | "the ability to easily rerun a runbook, skipping over completed tasks or tasks we do not want"
- https://shopify.engineering/four-steps-creating-effective-game-day-tests
  NEW - nearest inc-rollback-path-tested | Frame each game-day failure scenario as a written hypothesis about how the system will react | "you should start thinking about _how_ they will break, as a list of discrete hypotheses."
- https://airflow.apache.org/docs/apache-airflow/2.10.0/best-practices.html
  NEW - nearest svc-api-safe-idempotent-methods | A retried task must produce the same outcome on every re-run | "Thus, the tasks should produce the same outcome on every re-run."
- https://azure.github.io/azure-sdk/typescript_implementation.html
  NEW - nearest fn-propagate-dont-swallow | Produce an error whenever an HTTP request fails with a status not defined as success, and log it | "produce an error when any HTTP request fails with an HTTP status code that is not defined"
- https://azure.github.io/azure-sdk/typescript_implementation.html
  NEW - nearest svc-token-revocation | Do not persist, cache or reuse security credentials; treat them as short-lived | "persist, cache, or reuse security credentials"
- https://bazel.build/concepts/dependencies
  NEW - nearest mod-no-import-cycles | Declare every actual direct dependency of a rule, and no more | "file writers must explicitly declare all of the actual direct dependencies for every rule"
- https://bazel.build/concepts/dependencies
  NEW - nearest mod-internals-unreachable | Do not use directory labels in data; list the files so incremental rebuilds see every input | "try not to do this. In order to ensure correct incremental rebuilds"
- https://blog.ndepend.com/shotgun-surgery
  NEW - nearest mod-no-shotgun-surgery | Run a duplicate-code detector and treat copy-pasted blocks as a finding | "You can find this by looking for it, or by using a duplicate code detection tool."
- https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/
  NEW - nearest py-xdist-worker-isolated-state | Run the pytest suite in parallel with pytest-xdist, not serially | "We implemented parallel test execution using `pytest-xdist`, a popular plugin that distributes tests across multiple CPU cores."
- https://dagster.io/blog/dignified-python-10-rules-to-improve-your-llm-agents
  NEW - nearest fn-specific-exceptions-only | Check a condition before acting instead of using try/except KeyError as control flow | "check conditions proactively rather than relying on exceptions for control flow."
- https://deviq.com/domain-driven-design/anemic-model/
  NEW - nearest mod-internals-unreachable | Do not expose a domain object's collection as a public property | "Some code smells that may indicate an anemic domain model include exposed collection properties"
- https://deviq.com/domain-driven-design/anemic-model/
  NEW - nearest mod-behaviour-lives-with-state | Avoid setters on domain objects; change state through methods | "over-use of properties in general (especially setters)."
- https://doc.rust-lang.org/cargo/reference/resolver.html
  NEW - nearest code-dependency-pinning | Do not use a * version requirement in Cargo.toml | "Avoid `*` requirements, as they are not allowed on crates.io,"
- https://doc.rust-lang.org/cargo/reference/resolver.html
  NEW - nearest code-dependency-pinning | Set resolver = "2" or "3" in the top-level Cargo.toml | "The resolver is a global option that affects the entire workspace."
- https://docs.gitlab.com/development/software_design/
  NEW - nearest mod-cohesive-unit | Put each class inside a namespace for the bounded context where it operates | "should expect any class to be defined inside a module/namespace that represents the contexts where it operates"
- https://docs.gitlab.com/development/software_design/
  NEW - nearest mod-cohesive-unit | Do not move methods out of an omniscient class into a mixin; use composition | "Do not move methods out of an omniscient class into a mixin"
- https://docs.gitlab.com/development/software_design/
  NEW - nearest mod-cohesive-unit | Do not add methods to the legacy_methods.yml baseline files | "Do not add methods to these files."
- https://docs.gitlab.com/development/testing_guide/testing_levels/
  NEW - nearest fn-test-behaviour-not-implementation | Exported functions and classes need tests that document their public behaviour | "You should document the expected behavior of the public interface with tests."
- https://docs.pytest.org/en/stable/how-to/fixtures.html
  NEW - nearest py-pytest-expensive-fixture-scope | Use yield fixtures, not return, for fixtures that need teardown | "`yield` fixtures (recommended)"
- https://docs.pytest.org/en/stable/reference/reference.html
  NEW - nearest fn-specific-exceptions-only | Do not catch bare Exception with pytest.raises unless any exception is really meant | "Avoid using `pytest.raises` to catch `Exception` unless certain that you really want to catch **any** exception raised."
- https://docs.pytest.org/en/stable/reference/reference.html
  NEW - nearest fn-specific-exceptions-only | Expect grouped exceptions with pytest.RaisesGroup, not pytest.raises | "When expecting exceptions wrapped in `BaseExceptionGroup` or `ExceptionGroup`, you should instead use"
- https://docs.python.org/3/library/unittest.html
  NEW - nearest py-test-collection-and-imports | Test files must be modules or packages importable from the top-level directory | "all of the test files must be modules or packages importable from the top-level directory"
- https://docs.python.org/3/library/exceptions.html#NotImplementedError
  NEW - nearest mod-shim-fails-loudly | Do not raise NotImplementedError for an operation never meant to be supported; leave it undefined or set None | "It should not be used to indicate that an operator or method is not meant to be supported at all"
- https://docs.skypilot.ai/en/v0.10.0/developers/CONTRIBUTING.html
  NEW - nearest svc-api-versioning-policy | Warn the user when a new CLI flag is ignored because the server is too old | "we should add a warning message to inform the user that the new field is ignored"
- https://docs.spring.io/spring-framework/reference/testing/unit.html
  NEW - nearest mod-inject-boundary-collaborators | Make classes constructible with plain `new` and no container, so unit tests need no framework. | "objects instantiated by using the `new` operator, without Spring or any other container"
- https://dropbox.tech/infrastructure/courier-dropbox-migration-to-grpc
  NEW - nearest sys-fanout-leg-deadlines | Every RPC request carries a deadline set in the service definition; a method may opt out only explicitly. | "Every gRPC request includes a deadline, indicating how long the client will wait for a reply."
- https://dropbox.tech/infrastructure/courier-dropbox-migration-to-grpc
  NEW - nearest svc-circuit-breaker-bulkhead | Bound a request queue by time as well as by size, so a request waits only a limited time. | "A request can only spend so long in the queue."
- https://github.com/envoyproxy/envoy/blob/main/api/STYLE.md
  NEW - nearest chg-proto-no-field-type-change | Name every repeated field with a plural noun, such as `filters`. | "Always use plural field names for `repeated` fields, such as `filters`."
- https://github.com/envoyproxy/envoy/blob/main/api/STYLE.md
  NEW - nearest fn-no-stringly-typed-returns | Use `google.protobuf.Duration` or `Timestamp` for time fields, not raw integer seconds. | "For time-related fields, prefer using the well-known types"
- https://github.com/island-is/handbook/blob/master/docs/api-design-guide/naming-conventions.md
  NEW - nearest mod-one-name-per-concept | Do not use overly general names such as Info, Service or Application for an API concept. | "Overly general names that are ambiguous within the context of the API and the"
- https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md
  NEW - nearest svc-api-naming-consistent | Do not prefix boolean names with "is"; name them like `enabled`, not `isEnabled`. | "e.g. "enabled" not "isEnabled"."
- https://github.com/open-telemetry/opentelemetry-proto/raw/refs/heads/main/opentelemetry/proto/trace/v1/trace.proto
  NEW - nearest mod-validate-at-boundary-once | Reject a trace or span ID that is all zeroes or has the wrong byte length. | "of length other than 16 bytes is considered invalid"
- https://google.github.io/styleguide/pyguide.html#25-mutable-global-state
  NEW - nearest fn-no-caller-mutation | Do not use mutable objects as default argument values. | "Do not use mutable objects as default values in the function or method definition."
- https://laravel.com/docs/12.x/testing
  NEW - nearest typescript-shared-test-setup | A test class that overrides setUp or tearDown must call the parent's versions. | "be sure to call the respective `parent::setUp()` / `parent::tearDown()` methods on the parent class."
- https://learn.microsoft.com/en-us/dotnet/api/system.notsupportedexception
  NEW - nearest mod-shim-fails-loudly | Check the object's state, such as FileStream.CanRead, before calling a member that state may not support. | "examining the value of the FileStream.CanRead property and exiting the method if the stream is read-only."
- https://learn.microsoft.com/en-us/azure/architecture/antipatterns/improper-instantiation/
  NEW - nearest mod-pooled-clients-built-once | Set properties on a shared object once at startup, never before each request. | "Set such properties once (for example, during startup), and create separate instances if you need"
- https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
  NEW - nearest mod-layers-point-inward | Disallow direct navigation between aggregates; reference another aggregate by its foreign key only. | "disallow direct navigation between aggregates and only having the foreign key (FK) field"
- https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model
  NEW - nearest mod-internals-unreachable | Change entities inside an aggregate only through its aggregate root. | "You should make changes to entities within the aggregate only via the aggregate root."
- https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles
  NEW - nearest sys-cells-limit-blast-radius | Let bounded contexts talk through programmatic interfaces, never through a shared database. | "Communication between bounded contexts occurs through programmatic interfaces, rather than through a shared database"
- https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines
  NEW - nearest mod-inject-boundary-collaborators | Do not use the service locator pattern; take dependencies by injection, not by lookup. | "don't invoke GetService to obtain a service instance when you can use DI instead"
- https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/constructor
  NEW - nearest mod-no-logic-in-constructors | Do not call virtual members on the object from inside its constructor. | "AVOID calling virtual members on an object inside its constructor."
- https://legacy.reactjs.org/docs/react-component.html
  NEW - nearest mod-derive-dont-duplicate | Do not copy props into state; read the prop directly. | "Avoid copying props into state! This is a common mistake:"
- https://legacy.reactjs.org/docs/react-component.html
  NEW - nearest fn-no-caller-mutation | Never mutate this.state directly; change it through setState. | "Never mutate `this.state` directly, as calling `setState()` afterwards may replace the mutation you made."
- https://lucumr.pocoo.org/2020/1/1/async-pressure/
  NEW - nearest sys-load-shedding-bounded-queues | Await drain after each write; a bare write buffers without bound. | "not to use `write` at all on it's own but to follow up with `drain`"
- https://martinfowler.com/bliki/Yagni.html
  NEW - nearest mod-yagni | Refactoring that makes code easier to change is not a yagni violation | "expending effort on refactoring isn't a violation of yagni because refactoring makes the code more malleable."
- https://pkg.go.dev/crypto/cipher#NewGCM
  NEW - nearest mod-vetted-crypto-only | Use NewGCM with the standard nonce length unless a cryptosystem needs other sizes | "All other users should use NewGCM, which is faster and more resistant to misuse."
- https://pytest-django.readthedocs.io/en/latest/database.html
  NEW - nearest py-pytest-expensive-fixture-scope | Keep the test database across runs with --reuse-db; recreate it with --create-db after schema changes | "--reuse-db will not pick up schema changes between test runs."
- https://pytest-xdist.readthedocs.io/en/stable/how-to.html
  NEW - nearest py-xdist-worker-isolated-state | Key a database by testrun_uid so each whole test run gets its own | "create a separate database for each test run"
- https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/BEST_PRACTICES.md
  NEW - nearest code-dependency-pinning | Pin registry images in compose files to a tag or digest, never untagged or :latest | "must never use an untagged or `:latest` reference"
- https://refactoring.guru/smells/alternative-classes-with-different-interfaces
  NEW - nearest chg-delete-legacy-after-migration | After merging duplicate classes, delete the redundant one | "you may be able to delete one of the classes."
- https://refactoring.guru/smells/lazy-class
  NEW - nearest py-class-earns-its-instance | Collapse a subclass hierarchy when subclasses have few functions | "For subclasses with few functions, try Collapse Hierarchy."
- https://refactoring.guru/smells/switch-statements
  NEW - nearest mod-no-repeated-switches | When a switch only calls one method with different arguments, split it into explicit methods instead of polymorphism | "polymorphism will be superfluous. If this case, you can break that method into multiple smaller methods"
- https://rust-lang.github.io/api-guidelines/future-proofing.html
  NEW - nearest mod-internals-unreachable | A trait meant only for in-crate implementation gets a private sealed supertrait, so downstream code cannot implement it. | "Some traits are only meant to be implemented within the crate that defines them."
- https://rust-lang.github.io/api-guidelines/future-proofing.html
  NEW - nearest mod-deep-modules | Do not put derivable trait bounds (Clone, Debug, PartialEq) on generic struct definitions. | "Generic data structures should not use trait bounds that can be derived or do not otherwise add semantic value."
- https://sans-io.readthedocs.io/how-to-sans-io.html
  NEW - nearest mod-prefer-sync-api | Take network input as bytes the caller delivers, buffer it inside the implementation, and never read a socket. | "the calling code is responsible for delivering code to the implementation via a single input"
- https://shopify.engineering/managing-pii-shopify-scale
  NEW - nearest sys-pii-minimise-retention | Pseudonymise personal data (obfuscate or tokenise) before it enters the data warehouse, never store it raw. | "We perform two types of transformation on personal data before entering our data warehouse."
- https://tech.cabify.com/blog/engineering/what-to-do-when-your-code-is-starting-to-smell
  NEW - nearest mod-cohesive-unit | Keep search and query logic out of model classes, so models hold only business logic. | "We wanted to separate our searching logic from our models."
- https://thoughtbot.com/blog/the-case-for-wet-tests
  NEW - nearest typescript-shared-test-setup | Each test sets up only what it needs, not through one shared setup class that bundles unrelated setup. | "When each test sets up only the information it needs, it is much less likely to break"
- https://vitest.dev/config/setupfiles
  NEW - nearest typescript-shared-test-setup | With isolation disabled, a setup file must not repeat heavy work before every test file; guard it so it runs once. | "Make sure you are not doing the same thing more than necessary."
- https://www.eiffel.org/doc/solutions/Design_by_Contract_and_Assertions
  NEW - nearest mod-subtype-passes-parent-tests | A class invariant must hold before and after every exported routine, not only at creation. | "At runtime the invariant must be true for an instance at anytime that the instance is available to clients."
- https://www.mediawiki.org/wiki/Architecture_guidelines
  NEW - nearest none | New code must be internationalised and localisable, not hard-coded to one language. | "New MediaWiki code must be internationalised and localisable."
- https://www.rfc-editor.org/rfc/rfc5116.html
  NEW - nearest mod-vetted-crypto-only | On decryption failure return an error and never output partially decrypted data. | "partially encrypted or partially decrypted data MUST NOT be returned."
- https://blog.cloudflare.com/18-november-2025-outage/
  NEW - nearest prod-kill-switch-fallback | Review failure modes for error conditions across every core module. | "Reviewing failure modes for error conditions across all core proxy modules"
- https://stripe.dev/blog/how-api-changes-flow-into-stripes-developer-products
  NEW - nearest svc-api-spec-matches-impl | Block PR merge until automated tests validate API changes against design patterns. | "Before a PR can merge, a set of automated tests validate API changes against those patterns"
- https://stripe.dev/blog/how-api-changes-flow-into-stripes-developer-products
  NEW - nearest svc-api-spec-matches-impl | Every public API method, event, error, field and enum value should have a doc string. | "Every public API method, event, error, field, & enum value should have a doc string."
- https://nodejs.org/api/http.html#class-httpagent
  NEW - nearest mod-pooled-clients-built-once | Use a separate Agent, disable keep-alive, or pass agent:false when a request needs connection isolation. | "Applications that require per-request connection isolation can use a separate `Agent`, disable keep-alive, or pass `agent: false`."
- https://airbnb.tech/infrastructure/beyond-synthetic-testing-capturing-and-replaying-real-database-workloads-at-airbnb/
  NEW - nearest prod-shadow-compare-before-cutover | Captured production traffic is never replayed in lower environments or copied to dev tiers. | "Captured traffic is never replayed against lower environments or copied into a separate development tier."
- https://airbnb.tech/infrastructure/beyond-synthetic-testing-capturing-and-replaying-real-database-workloads-at-airbnb/
  NEW - nearest prod-kill-switch-fallback | Stop scheduling new replay tasks once tasks start failing. | "if tasks start failing, it stops scheduling new ones to avoid cascading issues"
- https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html
  NEW - nearest inc-rollback-path-tested | Roll back by redeploying the last known good revision, not by restoring the failed deployment. | "the last known good version of an application revision is deployed"
- https://docs.python.org/3/library/profile.html
  NEW - nearest prod-profile-on-demand | Use a sampling profiler for production debugging, not a deterministic one. | "`profiling.sampling` for production debugging with zero overhead"
- https://grafana.com/docs/k6/latest/testing-guides/test-types/
  NEW - nearest prod-load-test-before-launch | Use one simple load shape: ramp-up, plateau, ramp-down, with no repeated spikes. | "Stick to simple load patterns. For all test types, directions is enough: ramp-up, plateau, ramp-down."
- https://grafana.com/docs/pyroscope/latest/introduction/continuous-profiling/
  NEW - nearest prod-profile-on-demand | Use sampling profilers, not instrumenting ones, to profile production with minimal overhead. | "By using sampling profilers, Pyroscope and Cloud Profiles can collect data with minimal overhead"
- https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/monitoring
  NEW - nearest prod-alerts-symptoms-golden-signals | Keep production and nonproduction telemetry apart; only production data drives alerts. | "Production data reflects real user impact and should drive monitoring and alerts."
- https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/monitoring
  NEW - nearest prod-alerts-symptoms-golden-signals | Each alert names the threshold in sustained breach, its impact and its components. | "Each alert should indicate what threshold had a sustained breach, the potential impact, and the components involved"
- https://opentelemetry.io/docs/specs/otel/metrics/api/
  NEW - nearest svc-timeouts | Callback functions must not run for an unbounded time; give each one a time limit | "Callback functions SHOULD NOT take an indefinite amount of time."
- https://opentelemetry.io/docs/specs/otel/metrics/api/
  NEW - nearest prod-wide-events-bounded-labels | Callbacks must not report two measurements with the same attributes across all registered callbacks | "Callback functions SHOULD NOT make duplicate observations (more than one `Measurement` with the same `attributes`)"
- https://prometheus.io/docs/practices/alerting/
  NEW - nearest prod-alerts-symptoms-golden-signals | Alert that monitoring infrastructure itself (Prometheus, Alertmanager, Pushgateway) is up and working | "have alerts to ensure that Prometheus servers, Alertmanagers, PushGateways, and other monitoring infrastructure are available"
- https://prometheus.io/docs/practices/histograms/
  NEW - nearest prod-latency-slo-percentile | A classic-histogram SLO query needs an existing bucket at the SLO threshold, or it returns no result silently | "Note that this expression strictly requires a bucket boundary configured at 0.3."
- https://prometheus.io/docs/practices/histograms/
  NEW - nearest prod-latency-slo-percentile | Compute an average as rate of the sum divided by rate of the count, not from a single rate of a mean | "then divide the “rate of the sum” by the “rate of the count”."
- https://shopify.engineering/scaling-inventory-reservations
  NEW - nearest sys-lock-fencing | Every transaction path acquires locks on the same tables in the same order, to prevent deadlocks | "reserve always `DELETE`s from the units table first, then `INSERT`s into `reserved_quantities`."
- https://sre.google/sre-book/monitoring-distributed-systems/
  NEW - nearest prod-alerts-symptoms-golden-signals | Every page must be actionable, and a page that needs only a robotic response should not be a page | "Every page should be actionable."
- https://sre.google/sre-book/reliable-product-launches/
  NEW - nearest prod-load-test-before-launch | Size capacity so that peak load is served with spare replicas, so one or two can fail or be maintained | "you need to maintain four or five deployments, one or two of which are redundant"
- https://sre.google/sre-book/service-level-objectives/
  NEW - nearest prod-slo-error-budget | Choose only a few SLOs, and drop any that cannot win a priority argument | "Choose just enough SLOs to provide good coverage of your system’s attributes."
- https://sre.google/workbook/error-budget-policy/
  NEW - nearest inc-review-asks-which-check | An incident that burns over 20 percent of the error budget in four weeks requires a postmortem with a P0 action item | "If a single incident consumes more than 20% of error budget over four weeks"
- https://sre.google/workbook/error-budget-policy/
  NEW - nearest prod-slo-error-budget | An outage class that burns over 20 percent of the quarterly budget requires a P0 item in the quarterly plan | "the team must have a P0 item on their quarterly planning document"
- https://stripe.dev/blog/how-stripes-document-databases-supported-99.999-uptime-with-zero-downtime-data-migrations
  NEW - nearest sys-migration-lock-timeout | Keep the cutover pause shorter than a planned primary failover, so the switch stays within client retry budgets | "keep the key phase of the migration process shorter than the duration of a planned database primary failover"
- https://www.atlassian.com/blog/atlassian-engineering/unlocking-reliability-with-splunk-smartstore
  NEW - nearest mod-vetted-crypto-only | Encrypt object-store data at rest and block public access to its storage buckets | "Use S3 SSE to ensure encryption at rest and ensure that you use ACLs to disallow public access"
- https://www.atlassian.com/blog/atlassian-engineering/unlocking-reliability-with-splunk-smartstore
  NEW - nearest sys-cache-bounds-invalidation | Treat repeated re-downloads of the same cached item as the sign that the cache is too small | "Excessive repeated downloads of the same buckets indicate that you need to increase your cache size"
- https://www.datadoghq.com/blog/monitoring-101-alerting/
  NEW - nearest prod-alerts-symptoms-golden-signals | Log every alert, even one that never notifies anyone, to a central place for correlation | "All alerts should, at a minimum, be logged to a central location for easy correlation with other metrics and events"
- https://www.deque.com/web-accessibility-beginners-guide/
  NEW - nearest chg-ui-change-screenshots-and-keyboard-pass | Test each page with the keyboard alone, without a mouse or trackpad | "Do not use your mouse"
- https://www.honeycomb.io/blog/time-to-version-observability-signs-point-to-yes
  NEW - nearest prod-wide-events-bounded-labels | Make dashboards dynamic, so an engineer can drill down from a question | "Any dashboards should be dynamic, allowing you to drill down into a question"
- https://www2.gov.bc.ca/gov/content/home/accessible-government/toolkit/testing-and-auditing
  NEW - nearest chg-ui-change-screenshots-and-keyboard-pass | Anything operable with a mouse must also work with a keyboard | "Anything you can do with a mouse must also work with a keyboard"
- https://aws.amazon.com/builders-library/minimizing-correlated-failures-in-distributed-systems/
  NEW - nearest prod-canary-staged-rollout | Give operational tools velocity controls and feedback loops, so automated changes stay gradual | "we always make sure to introduce velocity controls and feedback loops"
- https://aws.amazon.com/builders-library/caching-challenges-and-strategies/
  NEW - nearest sys-cache-bounds-invalidation | Emit cache hit-rate and utilization metrics so the cache can be tuned | "Emit metrics on cache utilization and hit rate to ensure the cache is tuned appropriately"
- https://airbnb.tech/infrastructure/from-static-rate-limiting-to-adaptive-traffic-management-in-airbnbs-key-value-store/
  NEW - nearest sys-cache-bounds-invalidation | Give hot-key cache entries an expiry of seconds, so they vanish as demand cools | "Entries expire after roughly three seconds, so they vanish as soon as demand cools"
- https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
  NEW - nearest svc-rate-limit-quota | Configure spending limits, or billing alerts, for every third-party provider or API integration | "Configure spending limits for all service providers/API integrations."
- https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization
  NEW - nearest svc-authz-central-deny-default | Do not treat an endpoint as admin-only or regular based on its URL path | "assume that an API endpoint is regular or administrative only based on the URL path"
- https://atlassian.design/components/spinner/usage
  NEW - nearest svc-slow-operation-shows-progress | Use at most one spinner on a page at any time | "There should only be a single spinner on a page at any time."
- https://atlassian.design/components/spinner/usage
  NEW - nearest fn-status-announced-live-region | Give every spinner a label that says what process is running, for assistive technology | "to add context for assistive technologies."
- https://auth0.com/docs/manage-users/user-accounts/user-account-linking
  NEW - nearest svc-account-linking | Account linking must use access tokens, not ID tokens | "You will have to use Access Tokens in all cases."
- https://auth0.com/docs/secure/tokens/refresh-tokens/revoke-refresh-tokens
  NEW - nearest svc-token-revocation | With refresh token rotation, reuse of an invalidated token revokes every token issued since it | "the entire set of refresh tokens issued since that invalidated token was issued will immediately be revoked"
- https://aws.amazon.com/builders-library/dependency-isolation
  NEW - nearest svc-circuit-breaker-bulkhead | Timeouts alone do not bound concurrency; bound it with a limit | "tuning timeouts and retry policies is unlikely to prevent services from running out of concurrency"
- https://aws.amazon.com/builders-library/workload-isolation-using-shuffle-sharding/
  NEW - nearest sys-cells-limit-blast-radius | Assign each tenant or resource a unique shuffle shard, a combination of shared workers, so one customer's fault touches few others. | "We then assign every customer domain to a shuffle shard of four virtual name servers."
- https://baymard.com/blog/set-billing-equal-to-shipping
  NEW - nearest svc-no-redundant-entry | Ask for the shipping address fields, then derive billing from them, never the reverse. | "Ask users to fill out the shipping address fields instead of the billing address fields"
- https://blog.cloudflare.com/keeping-cloudflare-api-all-green-using-python-based-testing/
  NEW - nearest svc-api-contract-tests | Cover every API endpoint and each of its HTTP methods with a test. | "it is mandatory for us to have coverage of all the API endpoints and their possible methods"
- https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  NEW - nearest fn-password-slow-hash | Set a password length floor and a maximum of at least 64 characters, and never silently truncate a password. | "Do not silently truncate passwords."
- https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html
  NEW - nearest svc-security-headers | Block framing of pages with the CSP frame-ancestors directive, which replaces X-Frame-Options. | "it has been obsoleted by the `frame-ancestors` CSP directive"
- https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
  NEW - nearest svc-auth-throttle-generic-errors | Do not lock an account in response to a forgotten-password attack. | "Accounts should not be locked out in response to a forgotten password attack"
- https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html
  NEW - nearest svc-cors-allowlist | Give postMessage an explicit target origin, never a wildcard. | "explicitly state the expected origin as the second argument to `postMessage` rather than `*`"
- https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html
  NEW - nearest svc-session-lifecycle | Keep session identifiers out of localStorage, and carry them in HttpOnly cookies. | "Do not store session identifiers in local storage as the data is always accessible by JavaScript."
- https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
  NEW - nearest svc-security-headers | Forbid framing of the page, with frame-ancestors or X-Frame-Options DENY. | "Do not allow displaying of the page in a frame."
- https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html
  NEW - nearest svc-security-headers | Remove the X-Powered-By header from every response. | "Remove all `X-Powered-By` headers."
- https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
  NEW - nearest svc-authz-central-deny-default | Bind tenant context to a server-verified identity and a current tenant membership check. | "Bind tenant context to a server-verified identity and current tenant membership or service authorization."
- https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
  NEW - nearest svc-authz-central-deny-default | Enforce tenant isolation in the database with row-level security, forced on table owners. | "Force RLS for table owners (not superusers or BYPASSRLS roles)"
- https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
  NEW - nearest svc-mfa-step-up | Notify the user out of band whenever an MFA factor changes | "Notify the user through out-of-band channels (such as email or push notification) whenever an MFA factor is changed."
- https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html
  NEW - nearest fn-mask-credentials-in-output | Never return a stored TOTP seed to the client after enrollment | "Never return the seed to the client after enrollment."
- https://cli.github.com/manual/gh_repo_delete
  NEW - nearest svc-cli-destructive-dry-run | Ignore the skip-confirmation flag when no target is named, so the command still prompts | "For safety, when no repository argument is provided, the `--yes` flag is ignored"
- https://clig.dev/
  NEW - nearest svc-cli-non-interactive | Show no animations when stdout is not an interactive terminal | "If`stdout` is not an interactive terminal, don’t display any animations."
- https://cloud.google.com/architecture/dr-scenarios-planning-guide
  NEW - nearest none | Set RTO and RPO for each application first; they drive the DR design. | "DR planning begins with a business impact analysis that defines two key metrics:"
- https://cloud.google.com/architecture/dr-scenarios-planning-guide
  NEW - nearest none | Pick the DR pattern (cold, warm, hot) that meets each application's RTO and RPO. | "look at your RTO and RPO values and which DR pattern you can adopt to meet those values"
- https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
  NEW - nearest svc-idempotency-key | A duplicate that arrives while the original is still running gets a resource conflict error | "The resource SHOULD respond with a resource conflict error."
- https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/
  NEW - nearest svc-idempotency-key | Resource must publish an idempotency spec, including any key expiry policy | "Resources MUST publish an idempotency-related specification."
- https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/
  NEW - nearest svc-api-retry-after | Clients must not treat a positive remaining quota as a guarantee that requests will succeed | "Clients MUST NOT assume that a positive available quota is a guarantee that further requests will be served."
- https://design-system.service.gov.uk/patterns/question-pages
  NEW - nearest svc-no-redundant-entry | Ask one question per question page | "Start by asking one question per page"
- https://design-system.service.gov.uk/patterns/question-pages
  NEW - nearest svc-page-title-per-route | Do not use the same page heading across multiple pages | "Do not use the same page heading across multiple pages."
- https://devcenter.heroku.com/articles/cli-style-guide
  NEW - nearest svc-cli-exit-codes-and-streams | Commands that output data should offer --json and/or --terse for machine-readable output | "commands should offer a `--json` and/or a `--terse` flag when valuable"
- https://developer.apple.com/tutorials/data/design/human-interface-guidelines/feedback.json
  NEW - nearest svc-slow-operation-shows-progress | Show people when an action cannot be carried out, and explain why | "Show people when a command can’t be carried out and help them understand why."
- https://developer.apple.com/tutorials/data/design/human-interface-guidelines/progress-indicators.json
  NEW - nearest svc-slow-operation-shows-progress | Progress indicators appear only while the operation runs and disappear when it completes | "All progress indicators are transient, appearing only while an operation is ongoing and disappearing after it completes."
- https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform
  NEW - nearest chg-approval-tied-to-patch | Make the apply step run the exact plan that was approved, not a later plan. | "approving a plan passes along enough information to the apply step"
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img
  NEW - nearest fn-img-alt-text | Do not use the title attribute as a substitute for alt text. | "The `title` attribute is not an acceptable substitute for the `alt` attribute."
- https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/title
  NEW - nearest svc-page-title-per-route | Keep the title to about 55-60 characters, with the key words first. | "Search engines typically display about the first 55–60 characters of a page title."
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
  NEW - nearest svc-cors-allowlist | Send Vary: Origin when the allowed origin changes per request. | "the server should also include `Origin` in the `Vary` response header"
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS
  NEW - nearest svc-cors-allowlist | Preflight requests must never carry credentials. | "CORS-preflight requests must never include credentials."
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
  NEW - nearest svc-csp-strict-script-src | Use frame-ancestors 'none' to forbid all embedding, like X-Frame-Options: deny. | "Setting this directive to `'none'` is similar to `X-Frame-Options: deny`"
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Content-Security-Policy/frame-ancestors
  NEW - nearest svc-csp-strict-script-src | Set frame-ancestors explicitly, since default-src does not fall back to it. | "A policy that declares `default-src 'none'` still allows the resource to be embedded by anyone."
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
  NEW - nearest svc-security-headers | Send X-Content-Type-Options: nosniff, with a correct Content-Type on every resource. | "Site security testers usually expect this header to be set"
- https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/X-Content-Type-Options
  NEW - nearest svc-security-headers | With nosniff, the browser blocks script or style responses whose MIME type is wrong. | "the browser blocks the response if the MIME type doesn't match an expected type"
- https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides/Cookies
  NEW - nearest svc-token-revocation | Session identifiers expire as quickly as possible | "Session identifiers in particular should expire as quickly as possible."
- https://developer.mozilla.org/en-US/docs/Web/Security/Referer_header:_privacy_and_security_concerns
  NEW - nearest svc-no-secrets-in-url | Keep third-party embeds off login, reset and payment pages | "consider removing any third-party content (e.g., social networking widgets embedded in `<iframe>`) from secure areas"
- https://developer.siemens.com/guidelines/api-guidelines/rest/error.html
  NEW - nearest svc-api-specific-status-codes | A 401 response MUST send WWW-Authenticate with at least one challenge | "The server generating a 401 response **MUST** send a `WWW-Authenticate` header field"
- https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html
  NEW - nearest svc-dlq | Every FIFO send must carry a message group ID or the action fails | "You must associate a message group ID with each message."
- https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html
  NEW - nearest svc-api-key-scope | Monitor key usage in audit logs and alarm on denied access attempts | "Use AWS CloudTrail to monitor access key usage and detect any unauthorized access attempts."
- https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-request-throttling.html
  NEW - nearest svc-rate-limit-quota | Throttle requests above the steady-state rate and burst limits with 429 responses | "When request submissions exceed the steady-state request rate and burst limits, API Gateway begins to throttle requests."
- https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-choreography.html
  NEW - nearest svc-saga-steps | Update local data and publish its event atomically, for example through a transactional outbox | "The microservice has to atomically update the database and publish an event."
- https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection
  NEW - nearest svc-account-linking | Require email verification before accepting a sign-up or an email change | "We recommend that you don't allow users to sign up without an email verification flow."
- https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-tenant-logging
  NEW - nearest svc-tenant-id-in-telemetry | Route each tenant's logs to its own project with a sink whose filter matches only that tenant's namespace | "This command creates a log sink that sends all logs that are related to the `$TENANT_NAMESPACE` namespace to the tenant project."
- https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-tenant-logging
  NEW - nearest svc-tenant-id-in-telemetry | Add an exclusion filter on the main project's _Default sink so routed tenant logs are not kept twice | "We recommend that `_Default` sinks in main GKE projects include an exclusion filter."
- https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-tenant-logging
  NEW - nearest svc-tenant-id-in-telemetry | Scope the sink's write grant on the tenant project with an IAM condition naming that project | "The following command grants the main project permissions to write logs to the tenant project:"
- https://docs.djangoproject.com/en/5.2/ref/middleware/
  NEW - nearest svc-security-headers | Do not set Referrer-Policy to no-referrer on HTTPS sites, because CSRF checks need the Referer header | "so completely disabling the `Referer` header will interfere with CSRF protection."
- https://docs.djangoproject.com/en/5.2/topics/auth/default/
  NEW - nearest fn-password-slow-hash | Never write the password attribute directly; set passwords through set_password() | "do not attempt to manipulate the password attribute of the user directly"
- https://docs.djangoproject.com/en/5.2/topics/security/#user-uploaded-content
  NEW - nearest svc-upload-validate-store | Serve user uploads from a distinct top-level or second-level domain, not a subdomain | "always serving user uploaded content from a distinct top-level or second-level domain"
- https://docs.github.com/en/actions/concepts/security/artifact-attestations
  NEW - nearest svc-update-verify-provenance | Attest only released binaries and packages, not test builds or individual source files | "Frequent builds that are just for automated testing."
- https://docs.github.com/en/actions/concepts/security/artifact-attestations
  NEW - nearest code-workflow-supply-chain | Run the build in a reusable workflow shared across repositories to reach SLSA Build Level 3 | "have your build take place in a reusable workflow that many repositories across your organization share"
- https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api
  NEW - nearest svc-circuit-breaker-bulkhead | Pause at least a second between writes and avoid concurrent requests to stay under the limits | "you should pause at least 1 second between mutative requests and avoid concurrent requests"
- https://docs.github.com/en/rest/about-the-rest-api/api-versions
  NEW - nearest svc-api-versioning-policy | Require the client to name the API version on every request, in a header | "You should use the `X-GitHub-Api-Version` header to specify an API version."
- https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
  NEW - nearest svc-api-conditional-writes | On GET, send the saved ETag or Last-Modified value and treat a 304 response as unchanged. | "You can use the values of these headers to make conditional `GET` requests."
- https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api
  NEW - nearest svc-list-endpoint-paginates | When paging through a list, use a stable sort order so item updates do not reshuffle pages already fetched. | "If you page through a list, use a stable sort order."
- https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
  NEW - nearest svc-list-endpoint-paginates | Fetch further pages only by following the URLs in the link header, never by building page numbers. | "You can use the URLs from the `link` header to request another page of results."
- https://docs.mender.io/overview/introduction
  NEW - nearest svc-update-verify-provenance | After writing an update to the inactive partition, verify its checksum before switching the boot flag. | "When complete, the client verifies the checksum. If all is well, it sets a flag in the bootloader"
- https://docs.mender.io/overview/introduction
  NEW - nearest svc-update-rollback-on-failure | Keep files the device modifies on a separate partition, because an OS update replaces the whole filesystem. | "You have to store all files that you modify on the devices in a separate partition."
- https://docs.python.org/3/library/asyncio-sync.html
  NEW - nearest fn-resource-lifetime | Acquire an asyncio Lock with `async with`, not a manual acquire, so the release runs on the error path too. | "The preferred way to use a Lock is an `async with` statement"
- https://docs.python.org/3/library/asyncio-sync.html
  NEW - nearest svc-timeouts | Apply timeouts to asyncio primitives with asyncio.wait_for, since their acquire methods take no timeout argument. | "use the `asyncio.wait_for()` function to perform operations with timeouts."
- https://docs.python.org/3/library/tarfile.html
  NEW - nearest svc-upload-validate-store | Never extract an archive from an untrusted source without first inspecting its members. | "Never extract archives from untrusted sources without prior inspection."
- https://docs.python.org/3/library/tarfile.html
  NEW - nearest fn-confine-file-path | Extract archives with a filter that refuses members whose paths fall outside the destination directory. | "Raised to refuse extracting a member outside the destination directory."
- https://docs.rs/tokio/latest/tokio/sync/struct.Semaphore.html
  NEW - nearest svc-circuit-breaker-bulkhead | Limit how many incoming requests are handled at once, since unbounded concurrency invites denial of service. | "Allowing an unbounded amount of requests to be processed could result in a denial-of-service"
- https://docs.slack.dev/authentication/verifying-requests-from-slack/
  NEW - nearest svc-host-header-trust | Accept the client-certificate domain header only when it equals the exact expected name | "Do not accept header values with any other domain name, including other subdomains of slack.com."
- https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html
  NEW - nearest svc-session-lifecycle | Custom UserDetails classes must override equals() and hashCode() | "ensure you override the **equals()** and **hashCode()** methods"
- https://docs.spring.io/spring-security/reference/servlet/authentication/session-management.html
  NEW - nearest svc-session-lifecycle | A custom login that sets the security context must persist it through a SecurityContextRepository | "you will need to use a `SecurityContextRepository` to persist it across requests"
- https://docs.stripe.com/api/pagination
  NEW - nearest svc-list-endpoint-paginates | Reject a list request that sends both the forward and the backward cursor | "These parameters are mutually exclusive."
- https://docs.stripe.com/api/versioning
  NEW - nearest fn-no-stringly-typed-returns | Clients reading an open enum must handle unknown values with a fallback branch | "such as a default branch in a switch statement"
- https://docs.stripe.com/rate-limits
  NEW - nearest svc-rate-limit-quota | Pace outgoing calls on the client with a token bucket | "implementar en el lado del cliente un algoritmo de token bucket"
- https://docs.stripe.com/rate-limits
  NEW - nearest svc-circuit-breaker-bulkhead | Serialize writes to the same object instead of running them concurrently | "asegurarse de que las mutaciones en el mismo objeto se pongan en cola y se ejecuten de forma secuencial"
- https://docs.stripe.com/webhooks
  NEW - nearest svc-idempotency-key | Dedupe inbound webhook deliveries by recording processed event IDs and skipping events already recorded. | "registrando los ID de eventos que has procesado y no procesando los eventos ya registrados"
- https://docs.temporal.io/design-patterns/saga-pattern
  NEW - nearest svc-saga-steps | Run compensations in reverse order of registration when a later step fails. | "run in reverse order of registration"
- https://engineering.atspotify.com/2013/03/achieving-fault-tolerance-with-intelligent-daemons
  NEW - nearest svc-circuit-breaker-bulkhead | Fast-fail calls to a weak dependency once its recent failures show it is unhealthy, using a circuit breaker. | "Especially for weak dependencies, it can make sense to fast-fail requests."
- https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
  NEW - nearest fn-no-mass-assignment | PUT and POST must ignore the status block so read-modify-write cannot overwrite status | "The PUT and POST verbs on objects MUST ignore the `status` values"
- https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
  NEW - nearest svc-api-error-code-stable | Every status condition must carry a non-empty Reason field | "Use of the `Reason` field is required."
- https://google.aip.dev/140
  NEW - nearest svc-api-naming-consistent | Field names must not be verbs; they name a value, not an action | "Field names **must not** be named to reflect an intent or action. They **must not** be verbs."
- https://google.aip.dev/140
  NEW - nearest svc-api-naming-consistent | Boolean field names omit the prefix "is" | "Boolean fields **should** omit the prefix "is"."
- https://google.aip.dev/158
  NEW - nearest svc-list-endpoint-paginates | Page tokens must be opaque and not user-parseable | "Page tokens provided by APIs **must** be opaque (but URL-safe) strings, and **must not** be user-parseable."
- https://google.aip.dev/185
  NEW - nearest svc-api-versioning-policy | Send the API version in an X-Goog-Api-Version header or a query parameter | "API requests under IBV **must** send the API version identifier using either the `X-Goog-Api-Version` HTTP header"
- https://google.aip.dev/193
  NEW - nearest svc-api-error-code-stable | The error reason is UPPER_SNAKE_CASE, at most 63 characters, matching a fixed regex | "match a regular expression of `[A-Z][A-Z0-9_]+[A-Z0-9]`"
- https://google.github.io/building-secure-and-reliable-systems/raw/ch15.html
  NEW - nearest svc-security-event-logging | Make collected logs hard to alter and keep their writes immutable | "The system you build to collect logs should be immutable."
- https://google.github.io/building-secure-and-reliable-systems/raw/ch15.html
  NEW - nearest svc-security-event-logging | Ship logs remotely to a centralized, distributed log server so an attacker cannot erase them locally | "write your logs remotely to a centralized and distributed log server"
- https://grpc.io/docs/guides/deadlines/
  NEW - nearest svc-timeouts | Pass the remaining time, not an absolute deadline, to another server, to avoid clock skew | "converts the deadline to a timeout from which the already elapsed time is already deducted"
- https://grpc.io/docs/guides/status-codes/
  NEW - nearest svc-idempotency-key | A deadline error on a state-changing call may mean the call succeeded, so the caller must check before retrying | "this error may be returned even if the operation has completed successfully"
- https://httpd.apache.org/docs/2.4/mod/mod_deflate.html
  NEW - nearest svc-decompression-cap | Stop a request whose inflation ratio exceeds a set ratio, a burst limit on top of the size cap | "the maximum number of times the `DeflateInflateRatioLimit` can be crossed before terminating the request"
- https://infosec.mozilla.org/guidelines/web_security
  NEW - nearest svc-security-headers | On high-risk sites, add the preload directive to HSTS and submit the site to the preload list | "is recommended for all high risk websites"
- https://infosec.mozilla.org/guidelines/web_security
  NEW - nearest svc-tls-modern-only | Serve all communications over HTTPS or another secure protocol | "Sites should use HTTPS (or other secure protocols) for all communications"
- https://kubernetes.io/docs/reference/kubectl/generated/kubectl_delete/
  NEW - nearest svc-cli-non-interactive | Make the confirmation prompt opt-in, so a scripted run never waits for input unless asked | "If true, delete resource only when user confirms."
- https://laravel.com/docs/12.x/eloquent
  NEW - nearest svc-stream-dont-materialise | Use chunkById, not chunk, when the filter column is also updated during iteration | "If you are filtering the results of the `chunk` method based on a column that you will also be updating"
- https://learn.microsoft.com/en-us/aspnet/core/mvc/models/file-uploads
  NEW - nearest svc-upload-validate-store | Run a malware scan on each upload before the file is stored | "Run a virus/malware scanner on uploaded content before the file is stored."
- https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity-configuration
  NEW - nearest fn-password-slow-hash | Require a minimum password length; the default minimum is six characters | "Passwords must be at least six characters long."
- https://learn.microsoft.com/en-us/aspnet/core/security/authorization/secure-data
  NEW - nearest fn-no-mass-assignment | Set a record's status on the server, so a posted form value cannot create it in an approved state | "Set the contact status to _Submitted_ so a contact can't be created in the _Approved_ state"
- https://learn.microsoft.com/en-us/azure/api-management/rate-limit-policy
  NEW - nearest svc-rate-limit-quota | Limit call rate per subscription in a sliding window, returning 429 when exceeded (a rate limit, not a quota) | "limiting the call rate to a specified number per a specified time period"
- https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
  NEW - nearest svc-api-naming-consistent | Name resource URIs with nouns, not verbs, so no route encodes an operation | "Avoid using verbs in URIs to represent operations."
- https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data
  NEW - nearest fn-object-level-authz | On shared storage, authorise each tenant so tenants cannot read each other's data | "ensure that tenants can't access each other's data"
- https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/application-insights
  NEW - nearest sys-pii-minimise-retention | Apply tenant-specific redaction at ingestion without dropping other tenants' records | "ensure that tenant-specific transformations preserve records from other tenants"
- https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/application-insights
  NEW - nearest svc-rate-limit-quota | Cap telemetry ingestion with sampling so the daily ingestion limit is not hit | "You can implement ingestion rate limiting in Application Insights by using sampling"
- https://learn.microsoft.com/en-us/azure/architecture/patterns/bulkhead
  NEW - nearest prod-slo-error-budget | Monitor each bulkhead partition's performance against its own SLA | "Monitor each partition's performance and service-level agreement (SLA)."
- https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
  NEW - nearest svc-circuit-breaker-bulkhead | Open the breaker when recent failures pass a threshold within a time window, then fail calls at once | "If the number of recent failures exceeds a specified threshold within a given time period"
- https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
  NEW - nearest svc-circuit-breaker-bulkhead | In half-open, let only a limited number of trial requests through and reopen on failure | "A limited number of requests from the application are allowed to pass through and invoke the operation"
- https://learn.microsoft.com/en-us/azure/architecture/patterns/circuit-breaker
  NEW - nearest prod-alerts-symptoms-golden-signals | Give the breaker observability into failed and successful requests | "A circuit breaker should provide clear observability into both failed and successful requests"
- https://learn.microsoft.com/en-us/azure/architecture/patterns/retry
  NEW - nearest svc-retry-policy | Put retry logic only where the full context of the failing operation is known, so nested retries do not stack. | "Implement retry logic only where the full context of a failing operation is understood."
- https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling
  NEW - nearest svc-retry-policy | A service that throttles callers must pass on the 429 or 503 it gets from its own dependencies, not hide it behind silent retries. | "must also honor the throttling responses that it receives from its own downstream dependencies"
- https://learn.microsoft.com/en-us/azure/well-architected/security/monitor-threats
  NEW - nearest sys-secrets-and-errors | Keep secrets and sensitive data out of logs. | "Secrets and sensitive data must not appear in logs."
- https://learn.microsoft.com/en-us/ef/core/querying/filters
  NEW - nearest svc-tenant-id-in-telemetry | Scope every tenant query to the current tenant by default with a query filter on the context's tenant id. | "This provides strong tenant isolation for your queries by default"
- https://learn.microsoft.com/en-us/ef/core/querying/filters
  NEW - nearest svc-soft-delete-default | Name each query filter when a type has more than one, because a plain HasQueryFilter call overwrites the earlier filter. | "Calling HasQueryFilter with a simple filter overwrites any previous filter"
- https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens
  NEW - nearest svc-token-revocation | Securely delete the old refresh token after each refresh, since the server does not revoke it. | "Securely delete the old refresh token after acquiring a new one."
- https://learn.microsoft.com/en-us/entra/identity-platform/refresh-tokens
  NEW - nearest svc-token-revocation | When a refresh token is revoked, send the user to an interactive sign-in instead of failing. | "Your app should handle such revocations gracefully by redirecting the user to an interactive sign-in prompt"
- https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow
  NEW - nearest svc-oauth-code-flow-binding | Public clients (native and SPA) must not send a client secret or certificate when redeeming the code | "must not use secrets or certificates when redeeming an authorization code"
- https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-continuous-access-evaluation
  NEW - nearest svc-token-revocation | On a token rejected before expiry, return 401 with a claim challenge so the client drops its cache | "the resource provider denies access, and sends a 401+ claim challenge back to the client"
- https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/design/design-teams-app-layout-scaling
  NEW - nearest svc-reflow-and-zoom | Keep desktop layouts usable down to 550 CSS px wide | "The minimum size for desktop is 550 pixels."
- https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-export-data
  NEW - nearest svc-export-scope | Exported files carry the source's protection label and its controls | "Power BI applies these protection settings when exporting report data to Excel, PowerPoint, or PDF files."
- https://learn.microsoft.com/en-us/security/engineering/solving-tls1-problem
  NEW - nearest svc-tls-modern-only | Remove hardcoded protocol version selection and let the OS default choose | "remove the hardcoded protocol version selection and defer to the operating system default"
- https://learn.microsoft.com/en-us/security/engineering/solving-tls1-problem
  NEW - nearest svc-tls-modern-only | Scan source and service config for hardcoded protocol enum names | "scan source code and online service configuration files for the patterns below"
- https://learn.microsoft.com/en-us/windows/apps/design/controls/progress-controls
  NEW - nearest svc-slow-operation-shows-progress | Put one progress indicator on the collection, not on each list item | "do not put a progress indicator on each list item as they appear"
- https://learn.microsoft.com/en-us/windows/win32/msi/rollback-installation
  NEW - nearest svc-saga-steps | Custom steps must declare their own rollback or compensation to take part in rollback | "If an installation uses custom actions, additional authoring of the installation package is required to use rollback functionality."
- https://nodejs.org/api/zlib.html
  NEW - nearest svc-api-cache-control | Cache the results of compression operations rather than repeating them. | "It is strongly recommended that the results of compression operations be cached to avoid duplication of effort."
- https://nodejs.org/api/zlib.html
  NEW - nearest svc-stream-dont-materialise | Do not create a large number of zlib objects at once; the page warns of memory fragmentation. | "Creating and using a large number of zlib objects simultaneously can cause significant memory fragmentation."
- https://openid.net/specs/openid-connect-core-1_0.html
  NEW - nearest fn-jwt-verify-pinned | Clients must check that the ID Token nonce equals the nonce sent in the authentication request. | "Clients MUST verify that the `nonce` Claim Value is equal to the value"
- https://openid.net/specs/openid-connect-core-1_0.html
  NEW - nearest fn-jwt-verify-pinned | Reject an ID Token at or after its exp time. | "Expiration time on or after which the ID Token MUST NOT be accepted by the RP"
- https://pages.nist.gov/800-63-4/sp800-63b/session/
  NEW - nearest svc-session-lifecycle | End the session when either the overall or the inactivity timeout expires. | "When either timeout expires, the session SHALL be terminated."
- https://pages.nist.gov/800-63-4/sp800-63c/Federation/
  NEW - nearest svc-account-linking | Pairwise identifiers must contain no identifying information about the subscriber. | "The PPI SHALL contain no identifying information about the subscriber"
- https://pages.nist.gov/800-63-4/sp800-63c/Federation/
  NEW - nearest svc-saml-assertion-binding | An assertion relayed by a proxy must name the proxy as its issuer. | "The federated identifier of an assertion from a proxy SHALL indicate the proxy as the issuer of the assertion."
- https://pkg.go.dev/github.com/inconshreveable/go-update
  NEW - nearest svc-update-verify-provenance | Verify the signature over a hash of the final file, including when a patch was applied. | "Verification is performed by validating the signature of a hash of the new file."
- https://portswigger.net/web-security/access-control
  NEW - nearest svc-authz-central-deny-default | Match authorization rules on a normalised path so case or suffix variants cannot bypass a deny. | "they may tolerate inconsistent capitalization, so a request to `/ADMIN/DELETEUSER` may still be mapped"
- https://portswigger.net/web-security/authentication/password-based
  NEW - nearest svc-rate-limit-quota | Block an IP address that makes too many login attempts in quick succession. | "Blocking the remote user's IP address if they make too many login attempts in quick succession"
- https://portswigger.net/web-security/request-smuggling
  NEW - nearest svc-request-framing | When downgrading HTTP/2 to HTTP/1.1, reject newlines in headers, colons in header names, and spaces in the method. | "reject requests that contain newlines in the headers, colons in header names, and spaces in the request method"
- https://portswigger.net/web-security/request-smuggling
  NEW - nearest svc-request-framing | Never assume a request has no body; read and frame the body regardless of method. | "Never assume that requests won't have a body."
- https://portswigger.net/web-security/web-cache-deception
  NEW - nearest svc-api-cache-control | Make CDN caching rules leave the origin's Cache-Control header in control. | "Configure your CDN settings so that your caching rules don't override the `Cache-Control` header."
- https://portswigger.net/web-security/web-cache-deception
  NEW - nearest svc-cache-key-completeness | Make the origin and the cache resolve URL paths the same way. | "Verify that there aren't any discrepancies between how the origin server and the cache interpret URL paths"
- https://portswigger.net/web-security/web-cache-poisoning
  NEW - nearest svc-cache-key-completeness | Do not accept GET requests that carry a body. | "Don't accept fat `GET` requests."
- https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x12-V3-Web-Frontend-Security.md
  NEW - nearest svc-security-headers | Send X-Content-Type-Options: nosniff on every HTTP response. | "Verify that all HTTP responses contain an 'X-Content-Type-Options: nosniff' header field."
- https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x21-V12-Secure-Communication.md
  NEW - nearest svc-tls-modern-only | Use TLS for all external HTTP connectivity, with no fallback to unencrypted traffic. | "TLS is used for all connectivity between a client and external facing, HTTP-based services"
- https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x22-V13-Configuration.md
  NEW - nearest svc-fail-closed-defaults | Debug modes are disabled for all components in production | "Verify that debug modes are disabled for all components in production environments"
- https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x23-V14-Data-Protection.md
  NEW - nearest svc-session-lifecycle | Browser storage holds no sensitive data except session tokens | "does not contain sensitive data, with the exception of session tokens"
- https://shopify.dev/docs/api/admin-rest/usage/rate-limits
  NEW - nearest svc-rate-limit-quota | Client paces its calls to the bucket leak rate so it is never throttled | "To avoid being throttled, you can build your app to average two requests per second."
- https://shopify.dev/docs/storefronts/themes/best-practices/performance/prevent-image-layout-shift
  NEW - nearest svc-reflow-and-zoom | Images are responsive with CSS max-width 100% and height auto | "Combined with CSS that sets `max-width: 100%` and `height: auto`"
- https://source.android.com/docs/core/ota/ab
  NEW - nearest svc-update-rollback-on-failure | The update writes only to the inactive copy; the running version's partitions are never changed | "no partition used by the _current_ slot should be updated"
- https://sparkle-project.org/documentation/
  NEW - nearest svc-update-verify-provenance | The update signing key is kept off the machine that serves downloads | "not having your signing keys accessible from the machine that is hosting your product"
- https://sparkle-project.org/documentation/
  NEW - nearest svc-update-verify-provenance | The update feed and release notes are signed so a compromised server cannot redirect users | "For greater security, you can opt into signing your update feed and release notes"
- https://tech.cabify.com/blog/engineering/shadow-routing-providers
  NEW - nearest svc-best-effort-optional-deps | Background calls to a secondary provider must never block or delay the main request | "Do not block or delay the main request flow."
- https://theupdateframework.io/security/
  NEW - nearest svc-update-verify-provenance | Never accept a file older than one already seen (anti-rollback) | "Never accepting files older than those that have been seen previously."
- https://theupdateframework.io/security/
  NEW - nearest svc-token-revocation | Trust in signed metadata must expire unless it is renewed | "Trust should expire if it is not renewed."
- https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures
  NEW - nearest svc-security-event-logging | Audit trail of transactions needs integrity controls against tampering or deletion | "Ensure all transactions have an audit trail with integrity controls to prevent tampering or deletion"
- https://top10.owasp.org/2025/A09_2025-Security_Logging_and_Alerting_Failures
  NEW - nearest svc-security-event-logging | Log data must be encoded so that it cannot inject into the logging or monitoring systems | "Ensure log data is encoded correctly to prevent injections or attacks on the logging or monitoring systems."
- https://web.dev/articles/accessible-responsive-design
  NEW - nearest svc-reflow-and-zoom | Set the viewport meta tag to width=device-width and initial-scale=1 | "Setting `width=device-width` matches the screen's width in device-independent pixels"
- https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/http/header_validators/envoy_default/v3/header_validator.proto.html
  NEW - nearest svc-invalid-input-is-4xx | Reject a request whose URL path contains escaped slashes (%2F, %5C) | "rejecting requests with escaped slashes entirely"
- https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/http/header_validators/envoy_default/v3/header_validator.proto.html
  NEW - nearest svc-invalid-input-is-4xx | Reject by default a request whose URL path contains a fragment | "By default Envoy rejects requests with fragment in URL path."
- https://www.fastly.com/documentation/guides/full-site-delivery/caching/manipulating-the-cache-key/
  NEW - nearest svc-cache-key-completeness | Keep the request URL in the cache key | "you should always have `req.url` as one of your cache keys or as part of one."
- https://www.fastly.com/learning/security/what-is-http-request-smuggling
  NEW - nearest svc-request-framing | Reject a GET or HEAD request that carries a body with a 400 | "Fastly sends a `400 Bad Request` response, preventing the request from reaching the origin."
- https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks
  NEW - nearest svc-account-linking | Require the identifier verification to finish before any further action on the account | "required the verification to be completed before allowing any further actions on the account"
- https://www.nngroup.com/articles/skeleton-screens/
  NEW - nearest svc-async-content-reserves-space | Make a skeleton placeholder mirror the final page's layout | "The structure of the gray boxes mimics the structure of the final page"
- https://www.nngroup.com/articles/skeleton-screens/
  NEW - nearest svc-slow-operation-shows-progress | Do not use a frame-only skeleton (header, footer, background) as a progress indicator | "They should not be used as a progress indicator"
- https://www.nngroup.com/articles/skeleton-screens/
  NEW - nearest svc-slow-operation-shows-progress | Show a progress bar, not a skeleton, for downloads, uploads and conversions | "Instead, show a progress bar or a wizard that walks the user through the steps of the process."
- https://www.notion.com/blog/building-observability-into-notions-dead-letter-queue
  NEW - nearest svc-dlq | Record every DLQ replay with who triggered it, when and why | "Every re-enqueue operation is recorded, so you can see whether a task has been retried, when, and by whom."
- https://www.notion.com/blog/building-observability-into-notions-dead-letter-queue
  NEW - nearest svc-dlq | Require a stated reason before replaying dead tasks | "a confirmation modal requires a justification reason before the operation proceeds"
- https://www.reactive-streams.org/
  NEW - nearest svc-stream-dont-materialise | Keep backpressure signalling non-blocking and asynchronous | "care has to be taken to mandate fully non-blocking and asynchronous behavior"
- https://www.rfc-editor.org/rfc/rfc6750.html
  NEW - nearest svc-api-specific-status-codes | Answer an unauthenticated protected request with 401 and a WWW-Authenticate Bearer challenge | "the resource server MUST include the HTTP"
- https://www.rfc-editor.org/rfc/rfc7009
  NEW - nearest svc-api-specific-status-codes | Answer a revocation request with 200 when the token is revoked or was already invalid | "responds with HTTP status code 200 if the token has been revoked successfully"
- https://www.rfc-editor.org/rfc/rfc9110.html
  NEW - nearest svc-invalid-input-is-4xx | Accept received lengths at least as long as the service itself generates, so it parses its own long URIs | "a recipient MUST be able to parse and process protocol element lengths"
- https://www.rfc-editor.org/rfc/rfc9421.html
  NEW - nearest svc-webhook-replay-window | Require a fixed set of covered components in every signed message, and reject signatures that omit any of them | "that are expected and required to be included in the covered components list"
- https://www.rfc-editor.org/rfc/rfc9700.html
  NEW - nearest svc-oauth-code-flow-binding | Never use the resource owner password credentials grant | "The resource owner password credentials grant [RFC6749] MUST NOT be used."
- https://www.uber.com/es/en/blog/ubers-rate-limiting-system/
  NEW - nearest svc-best-effort-optional-deps | If the rate-limit control plane is unavailable, clients fail open and keep serving traffic. | "If the control plane became unavailable, clients failed open, allowing traffic to continue rather than risk self-inflicted outages"
- https://www.uber.com/es/en/blog/ubers-rate-limiting-system/
  NEW - nearest prod-shadow-compare-before-cutover | Run a new limit in shadow mode, monitored but not enforced, before turning enforcement on. | "teams can configure rate limits on shadow mode, where limits are generated and monitored but not enforced"
- https://www.w3.org/TR/trace-context/
  NEW - nearest svc-api-trace-context | At an edge gateway into a secure network, regenerate trace id, parent id and flags instead of forwarding them. | "This mutation is used in services that are defined as a front gate into secure networks"
- https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/
  NEW - nearest svc-retry-policy | Add jitter to periodic jobs and timers too, not only to retry delays. | "When building systems, we consider adding some jitter to all timers, periodic jobs, and other delayed work"
- https://sre.google/sre-book/addressing-cascading-failures/
  NEW - nearest svc-retry-policy | Do not stack retries at several layers, since attempts multiply down the call chain. | "avoid amplifying retries by issuing retries at multiple levels"
- https://sre.google/sre-book/addressing-cascading-failures/
  NEW - nearest svc-timeouts | Propagate the remaining deadline to downstream calls instead of inventing a new deadline per hop. | "Rather than inventing a deadline when sending RPCs to backends, servers should employ deadline propagation."
- https://12factor.net/config
  NEW - nearest mod-central-config | Do not group config into named environments such as staging or production; set each variable independently. | "They are never grouped together as “environments”, but instead are independently managed for each deploy."
- https://airbnb.tech/infrastructure/building-a-fault-tolerant-metrics-storage-system-at-airbnb/
  NEW - nearest sys-cells-limit-blast-radius | Shard each tenant onto a shuffled subset of nodes so one tenant's failure cannot reach every tenant. | "each tenant writes only to a subset of storage nodes"
- https://airbnb.tech/infrastructure/building-a-fault-tolerant-metrics-storage-system-at-airbnb/
  NEW - nearest svc-bound-client-controlled-sizes | Enforce per-tenant read limits on work per query, such as series or chunks fetched. | "limits on the number of fetched series/chunks per query"
- https://airbnb.tech/infrastructure/building-a-fault-tolerant-metrics-storage-system-at-airbnb/
  NEW - nearest svc-circuit-breaker-bulkhead | Isolate the critical query path from ad hoc and batch query traffic. | "The evaluation query path was isolated from the ad hoc query"
- https://americanexpress.io/cell-based-architecture-for-resilient-payment-systems/
  NEW - nearest svc-saga-steps | After a transaction has left the system, do not reroute or restart it in another cell. | "Once a transaction has been sent to an external system (e.g., card issuer), we consider that a point of no return"
- https://atlassian.design/foundations/iconography
  NEW - nearest sys-consistent-ui-terms | Draw system icons at 16x16 px by default; use 12 px only for the listed small-context uses. | "Medium icons are 16 × 16px in size and are the **default** size in our system."
- https://atlassian.design/foundations/iconography
  NEW - nearest sys-consistent-ui-terms | Give an icon a text label wherever possible, and drop the icon where it adds nothing. | "Use text labels to support icons wherever possible, and avoid using icons where they aren’t necessary."
- https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
  NEW - nearest sys-leader-two-leaders | Do not renew a lease from a background heartbeat thread. | "Avoid heartbeating leases in a background thread."
- https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/
  NEW - nearest sys-leader-two-leaders | Keep a record of who was leader at each time, and a log of leadership changes. | "Keep an audit trail or log of leadership changes."
- https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/
  NEW - nearest inc-rollback-path-tested | Test failure domains by taking each whole facility offline, not only its parts. | "we had never tested fully taking the entire PDX-04 facility offline"
- https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/
  NEW - nearest sys-cells-limit-blast-radius | Generally Available services must have no software dependency on any specific facility. | "without having any software dependencies on specific facilities"
- https://blog.google/security/mitigating-prompt-injection-attacks/
  NEW - nearest fn-link-url-scheme-allowlist | Do not render external image URLs in generated output. | "Our markdown sanitizer identifies external image URLs and will not render them"
- https://blog.google/security/mitigating-prompt-injection-attacks/
  NEW - nearest fn-link-url-scheme-allowlist | Redact suspicious URLs from generated output before the user sees it. | "the suspicious URLs will be redacted in Gemini’s response"
- https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload
  NEW - nearest sys-load-shedding-bounded-queues | Serve end() requests before start() requests so that started work can finish. | "the service should prioritize **end()** requests over **start()** requests."
- https://builder.aws.com/content/3Eun1EEyX6p2e3VYNyRLSJzLuMV/using-load-shedding-to-avoid-overload
  NEW - nearest prod-latency-slo-percentile | Keep fast-failed requests out of latency metrics for successful requests. | "it’s important not to pollute our services’ latency metrics with failed request latency"
- https://builder.aws.com/content/3K9TeXp6strMiJ4vhakpRD7BQWO/caching-challenges-and-strategies
  NEW - nearest sys-cache-bounds-invalidation | Cache error responses under a negative TTL distinct from the TTL of positive entries. | "cache the error response (that is, we use a “negative cache”) using a different TTL than positive cache entries"
- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  NEW - nearest sys-ssrf | Connect only to a resolved IP that passed the destination policy, so DNS rebinding cannot swap in a private address. | "ensure the HTTP client connects only to validated addresses."
- https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  NEW - nearest sys-ssrf | Disable following redirects in the outbound HTTP client so an allowed host cannot redirect the request elsewhere. | "Disable the support for the following of the redirection in your web client"
- https://cloud.google.com/memorystore/docs/redis/memory-management-best-practices
  NEW - nearest sys-cache-bounds-invalidation | Choose the eviction policy by data type: volatile-* for expiring data, allkeys-* for non-volatile data. | "If you are storing volatile data, choose one of the `volatile-*` eviction policies."
- https://cloud.google.com/memorystore/docs/redis/memory-management-best-practices
  NEW - nearest sys-cache-bounds-invalidation | Set an alert when the memory usage ratio exceeds 80 percent, before the cache runs out of memory. | "Set an alert to notify you if the **system memory usage ratio** metric exceeds 80%."
- https://codeql.github.com/codeql-query-help/python/py-full-ssrf/
  NEW - nearest sys-ssrf | Verify that a user-controlled host resolves to a public IP, and send the request through an adapter pinned to that verified IP. | "utilizing a custom HTTP adapter to ensure that future requests to that domain use the verified IP address."
- https://devcenter.heroku.com/articles/postgresql-indexes
  NEW - nearest py-await-check-then-act | Enforce uniqueness with a database constraint or unique index, not an application-level uniqueness validation. | "Always create the constraint at the database level, either with an index or a unique constraint."
- https://developers.cloudflare.com/cache/how-to/edge-browser-cache-ttl/
  NEW - nearest svc-api-cache-control | A CDN purge does not clear assets already stored in visitors' browsers, which keep them until the browser TTL expires. | "Purging Cloudflare’s cache does not affect assets stored by a visitor’s browser."
- https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html
  NEW - nearest py-await-check-then-act | Use a conditional update, not an atomic counter, where overcounting or undercounting cannot be tolerated. | "it is safer to use a conditional update instead of an atomic counter"
- https://docs.cockroachlabs.com/docs/stable/bulk-update-data
  NEW - nearest sys-migration-expand-contract | Run each batch UPDATE in its own transaction where possible | "Where possible, we recommend executing each `UPDATE` in a separate transaction."
- https://docs.docker.com/engine/logging/drivers/json-file/
  NEW - nearest sys-append-only-stores-have-retention | Log-driver option values in daemon.json must be strings, with numbers quoted | "`log-opts` configuration options in the `daemon.json` configuration file must be provided as strings."
- https://docs.docker.com/engine/logging/drivers/json-file/
  NEW - nearest sys-append-only-stores-have-retention | Do not read or write Docker's own log files with external tools | "Interacting with these files with external tools may interfere with Docker's logging system"
- https://docs.gitlab.com/development/migration_style_guide/
  NEW - nearest chg-rollback-path | Every migration must be reversible, with a working down path | "Your migration must be reversible."
- https://docs.sqlalchemy.org/en/20/orm/queryguide/relationships.html
  NEW - nearest sys-n-plus-one-pooling | Subquery loading with LIMIT or OFFSET needs an ORDER BY on a unique column | "should **always** include `Select.order_by()` against unique column(s) such as the primary key"
- https://ecto-sql.hexdocs.pm/backfilling_data.html
  NEW - nearest sys-migration-expand-contract | Backfill migrations run raw SQL and do not use application Ecto schemas | "Do not use Ecto schemas."
- https://gdpr-info.eu/art-5-gdpr/
  NEW - nearest sys-pii-minimise-retention | Collect and keep only personal data that is adequate, relevant and limited to its purpose | "adequate, relevant and limited to what is necessary in relation to the purposes"
- https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  NEW - nearest chg-bot-approval-not-human | Require human approval, with human-in-the-loop controls, for privileged or high-risk model actions | "Implement human-in-the-loop controls for privileged operations to prevent unauthorized actions."
- https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
  NEW - nearest fn-destructive-confirm-or-undo | Require a human to approve high-impact agent actions before they run | "Utilise human-in-the-loop control to require a human to approve high-impact actions before they are taken"
- https://github.com/Netflix/concurrency-limits
  NEW - nearest svc-rate-limit-quota | Give each request group a guaranteed share of one shared concurrency limit | "live traffic guaranteed 90% of throughput and 10% guaranteed to batch"
- https://github.com/Netflix/concurrency-limits
  NEW - nearest sys-load-shedding-bounded-queues | Raise or lower the concurrency limit from measured queue size each sampling window | "the limit is increased by 1 if the queue is less than alpha"
- https://github.com/ben-manes/caffeine/wiki/Eviction
  NEW - nearest sys-cache-bounds-invalidation | Prefer a size bound over soft or weak references for cache values | "we generally recommend using the more predictable maximum cache size instead"
- https://github.com/doctolib/safe-pg-migrations
  NEW - nearest sys-index-concurrently | Run migrations outside a transaction so locks are released early | "Do not wrap the migration in a transaction so that locks are held for a shorter time"
- https://gocardless.com/blog/zero-downtime-postgres-migrations-a-little-help
  NEW - nearest sys-migration-expand-contract | Split large schema migrations into files so each part runs in its own transaction | "split large schema migrations into multiple files so that ActiveRecord runs each part in a separate transaction"
- https://grpc.io/docs/guides/request-hedging/
  NEW - nearest sys-load-shedding-bounded-queues | Throttle hedged requests with a failure-driven token budget, and stop hedging when the budget runs low | "gRPC provides a way to throttle hedged RPCs to prevent server overload"
- https://grpc.io/docs/guides/request-hedging/
  NEW - nearest sys-load-shedding-bounded-queues | Stop sending hedged requests when the server pushes back not to retry | "If the pushback says not to retry, no further hedged requests will be sent"
- https://guides.rubyonrails.org/active_record_querying.html
  NEW - nearest sys-n-plus-one-pooling | Process large record sets in batches with find_each or find_in_batches, not all in memory | "intended for use in the batch processing of a large number of records"
- https://guides.rubyonrails.org/active_record_querying.html
  NEW - nearest sys-n-plus-one-pooling | Call unscope(:includes) before pluck so pluck does not trigger eager loading | "One way to avoid this is to `unscope` the includes"
- https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html
  NEW - nearest sys-leader-two-leaders | Run the journal quorum with at least three nodes | "There must be at least 3 JournalNode daemons"
- https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
  NEW - nearest sys-fanout-leg-deadlines | Give each scheduled run a start deadline and decide what happens when it is missed | "defines a deadline (in whole seconds) for starting the Job"
- https://kubernetes.io/docs/concepts/workloads/controllers/ttlafterfinished/
  NEW - nearest svc-webhook-replay-window | Expire finished objects on wall-clock timestamps only with a tolerance for clock skew | "Clocks aren't always correct, but the difference should be very small."
- https://learn.microsoft.com/en-us/azure/architecture/antipatterns/chatty-io/
  NEW - nearest sys-n-plus-one-pooling | Buffer many small file writes in memory and write them as one operation | "consider buffering data in memory and then writing the buffered data to a file as a single operation."
- https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching
  NEW - nearest sys-cache-bounds-invalidation | Keep the system of record authoritative; never store critical data only in the cache | "don't use the cache as the authoritative store of critical information."
- https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp
  NEW - nearest code-release-gated-on-ci | Define every stamp's infrastructure as code so all stamps deploy the same way | "Describe your infrastructure as code, by using Bicep or Terraform."
- https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp
  NEW - nearest sys-cells-limit-blast-radius | Deploy at least two stamps; do not hard-code single-stamp assumptions | "If you deploy only a single stamp, you can easily hard-code assumptions into your code or configuration"
- https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/security
  NEW - nearest code-dependency-pinning | Review and pin tool schemas and descriptions; re-approve any change before it takes effect | "Review and pin known-good tool schemas and descriptions, and require re-approval before updated tool metadata takes effect"
- https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk
  NEW - nearest sys-agent-tool-least-privilege | Require human approval before an agent runs a high-risk or irreversible action | "Require approval for high-risk or irreversible actions."
- https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
  NEW - nearest sys-lock-fencing | State at the lock call whether it guards efficiency or correctness, since correctness locks need fencing | "To distinguish these cases, you can ask what would happen if the lock failed"
- https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
  NEW - nearest sys-leader-two-leaders | Do not let a correctness lock's safety depend on timing assumptions such as lease length or clock behaviour | "Its safety depends on a lot of timing assumptions"
- https://learn.microsoft.com/en-us/purview/retention
  NEW - nearest sys-pii-minimise-retention | Record proof of disposition when content is deleted at the end of its retention period | "always have proof of disposition when content is deleted at the end of its retention period."
- https://postgres.ai/blog/20210923-zero-downtime-postgres-schema-migrations-lock-timeout-and-retries
  NEW - nearest sys-migration-lock-timeout | Take every lock a multi-statement migration needs at the start of its transaction, and retry the whole transaction if one fails. | "Acquire all locks we need at the very beginning of the transaction, explicitly (pessimistic locking)."
- https://prometheus.io/docs/prometheus/latest/storage/
  NEW - nearest sys-append-only-stores-have-retention | Keep the configured retention size at or below 80-85% of the disk, so compaction has room. | "we recommend setting the retention size to, at most, 80-85% of your allocated Prometheus disk space."
- https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x25-V16-Security-Logging-and-Error-Handling.md
  NEW - nearest svc-security-event-logging | Encode untrusted data in every log write so that it cannot inject log lines. | "Verify that all logging components appropriately encode data to prevent log injection."
- https://redis.io/docs/latest/develop/reference/eviction/
  NEW - nearest sys-cache-bounds-invalidation | With replication or persistence, set maxmemory below total RAM so the replication and AOF buffers have room. | "If you are using replication or persistence, we recommend that you set `maxmemory` to leave a little RAM free"
- https://slack.engineering/slacks-migration-to-a-cellular-architecture/
  NEW - nearest sys-cells-limit-blast-radius | Shift traffic away from a cell and back in small increments, down to 1%. | "Drains and undrains must be incremental."
- https://thoughtbot.com/blog/how-to-create-postgres-indexes-concurrently-in
  NEW - nearest sys-index-concurrently | Put each concurrent index migration in its own migration file. | "it's a good idea to isolate concurrent index migrations to their own migration files."
- https://web.mit.edu/Saltzer/www/publications/protection/Basic.html
  NEW - nearest sys-agent-tool-least-privilege | Give every program and every user only the privileges the job needs. | "Every program and every user of the system should operate using the least set of privileges necessary"
- https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search
  NEW - nearest svc-list-endpoint-paginates | Use one point-in-time ID for every slice of a parallel scan, or slices can overlap and miss documents. | "The same point-in-time ID should be used for all slices."
- https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto
  NEW - nearest mod-validate-at-boundary-once | Each route must set exactly one of route, redirect or direct_response; reject a config that sets none or several | "Precisely one of route, redirect, direct_response must be set"
- https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto
  NEW - nearest mod-validate-at-boundary-once | Reject a config where two mutually exclusive fields of one message are both set | "Only one of header_name, use_hash_policy may be set"
- https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto
  NEW - nearest mod-validate-at-boundary-once | Reject a config where two virtual hosts claim the same domain | "A domain must be unique across all virtual hosts or the config will fail to load"
- https://www.gov.uk/guidance/government-design-principles
  NEW - nearest svc-invalid-input-is-4xx | Put a hidden honeypot field in forms, marked for robots only, that people leave blank | "This field is for robots only. Please leave blank"
- https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
  NEW - nearest sys-agent-tool-least-privilege | Require the user's explicit consent before the agent performs a specific sensitive action it cannot otherwise secure | "we rely on the explicit consent of the user to perform a specific action"
- https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
  NEW - nearest svc-security-event-logging | Log enough of the LLM's input, output and tool use to spot suspicious activity | "logging enough information to identify suspicious activity"
- https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
  NEW - nearest sys-prompt-injection | Do not rely on deny-listing known injection phrases as the defense | "One technique to be wary of is any approach similar to"
- https://www.pgbouncer.org/features.html
  NEW - nearest sys-n-plus-one-pooling | Under transaction pooling, use no SET/RESET, LISTEN, PREPARE, WITH HOLD cursors or session advisory locks | "You can use it only when the application cooperates by not using features that break"
- https://www.postgresql.org/docs/current/ddl-partitioning.html
  NEW - nearest chg-migration-add-column-rewrite | Give partitions exactly the parent's columns; add a column to the parent and every partition in the same change | "For declarative partitioning, partitions must have exactly the same set of columns as the partitioned table"
- https://www.postgresql.org/docs/current/ddl-partitioning.html
  NEW - nearest sys-index-concurrently | A unique or primary key on a partitioned table must include every partition key column | "the constraint's columns must include all of the partition key columns"
- https://www.postgresql.org/docs/current/ddl-partitioning.html
  NEW - nearest sys-append-only-stores-have-retention | Create the partition for an incoming range before rows need it; an insert that maps to no partition fails | "an appropriate partition must be added manually"
- https://www.postgresql.org/docs/current/runtime-config-connection.html
  NEW - nearest svc-circuit-breaker-bulkhead | Set reserved_connections below max_connections minus superuser_reserved_connections | "The value must be less than `max_connections` minus `superuser_reserved_connections`"
- https://www.rfc-editor.org/rfc/rfc9111.html#name-invalidating-stored-response
  NEW - nearest sys-cache-bounds-invalidation | Forward unsafe requests to the origin and never answer them from cache | "A cache MUST write through requests with methods that are unsafe"
- https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows.pdf
  NEW - nearest sys-lock-fencing | Cap any client-requested lock-delay at a fixed maximum, so a faulty client cannot block a resource indefinitely. | "this limit prevents a faulty client"
- https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows.pdf
  NEW - nearest sys-lock-fencing | Require write permission to acquire a lock in either shared or exclusive mode, so unprivileged readers cannot block writers. | "acquiring a lock in either mode requires write"
- https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html
  NEW - nearest sys-consistent-ui-terms | When a labelled control collapses to an icon on small screens, keep its accessible name unchanged. | "a magnifying glass icon with the accessible name "Search""

# Source pass, 2026-11-04

Sources found for 105 draft cards by opencode workers (DeepSeek V4.1 Flash, free and Go tiers). A script fetched each URL and confirmed the quoted sentence is on the page (JavaScript-rendered and bot-blocked pages were checked in Chrome). Opus judged each source against its card's Rule. This note lists the sources that the judge marked as supporting the Rule for the 45 cards the pass moved to stable.

| Card | Source | Why it supports the Rule |
|---|---|---|
| `chg-approval-tied-to-patch` | https://docs.gitlab.com/user/project/merge_requests/approvals/settings/ | Resets approvals by comparing patch-id; exactly the rule |
| `chg-approval-tied-to-patch` | https://docs.prow.k8s.io/docs/components/plugins/approve/approvers/ | Approval label retracted on new commit; approval tied to code |
| `chg-approval-tied-to-patch` | https://gerrit-review.googlesource.com/Documentation/config-labels.html | Votes not carried to a changed patch set become outdated |
| `chg-delete-legacy-after-migration` | https://research.google/pubs/large-scale-automated-refactoring-using-clangmr | Google removes old APIs as new ones are introduced |
| `chg-delete-legacy-after-migration` | https://llvm.org/docs/SupportPolicy.html | Replacements made atomically in the same commit |
| `chg-devex-breaking-config` | https://docs.gitlab.com/administration/package_information/deprecation_policy | Config removal goes through deprecation with documented replacement syntax or removal date. |
| `chg-devex-breaking-config` | https://github.com/spring-projects/spring-boot/wiki/Spring-Boot-3.0-Migration-Guide | Migration guide flags renamed/removed config properties users must update. |
| `chg-no-silenced-diagnostics` | https://eslint.org/docs/latest/use/configure/rules | Asks for a reason comment on each disable directive; no ticket. |
| `chg-no-silenced-diagnostics` | https://rust-lang.github.io/rust-clippy/master/index.html#allow_attributes_without_reason | Lint requires a stated reason on each allow; no ticket. |
| `chg-proto-no-field-type-change` | https://buf.build/docs/breaking/rules/ | Protobuf tooling org says do not change field types |
| `chg-proto-no-field-type-change` | https://github.com/istio/api/blob/master/GUIDELINES.md | Istio proto API guidelines forbid changing or renaming field types |
| `chg-rollback-path` | https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/change-management/platform-leadership-review/ | Rollback plan must be documented in the change request |
| `chg-rollback-path` | https://learn.microsoft.com/en-us/compliance/assurance/assurance-microsoft-365-change-management | Change description includes a rollback plan |
| `chg-rollback-path` | https://docs.aws.amazon.com/wellarchitected/latest/framework/ops_mit_deploy_risks_plan_for_unsucessful_changes.html | Rollback plan documented before deployment |
| `code-a11y-check-in-ci` | https://accessibility.civicactions.com/posts/automated-accessibility-testing-leveraging-github-actions-and-pa11y-ci-with-axe | Hard-fails the CI action on axe/pa11y failures |
| `code-a11y-check-in-ci` | https://accessibility-manual.dwp.gov.uk/best-practice/automated-testing-using-axe-core-and-pa11y | UK department requires zero axe violations in automated tests |
| `code-a11y-check-in-ci` | https://accessibility.arizona.edu/web-apps/cicd-testing | Fails build on critical/serious violations; severity threshold |
| `code-flaky-test-quarantine` | https://www.atlassian.com/blog/atlassian-engineering/taming-test-flakiness-how-we-built-a-scalable-tool-to-detect-and-manage-flaky-tests | Detects flaky tests, assigns owners, files tickets with deadlines. |
| `code-flaky-test-quarantine` | https://handbook.gitlab.com/handbook/engineering/testing/quarantine-process/ | Quarantine exit needs 100+ passing runs and fixed root cause. |
| `code-flaky-test-quarantine` | https://medium.com/airtable-eng/how-airtable-manages-flaky-tests-in-a-large-scale-monorepo-5fe09922e90c | Releases from quarantine only after enough clean builds. |
| `code-release-gated-on-ci` | https://github.com/nodejs/node/blob/main/doc/contributing/releases.md | Release with failing CI workers must not be promoted |
| `code-release-gated-on-ci` | https://github.com/envoyproxy/envoy/blob/main/RELEASES.md | Release created only after tests pass |
| `code-release-gated-on-ci` | https://sre.google/sre-book/release-engineering/ | Re-runs tests on release branch with audit trail of passes |
| `fn-bool-arg-at-callsite` | https://kotlinlang.org/docs/coding-conventions.html | Official convention: named arguments for Boolean parameters |
| `fn-bool-arg-at-callsite` | https://www.swift.org/documentation/api-design-guidelines/ | Official guideline flags unlabelled Bool argument as unclear |
| `fn-bool-arg-at-callsite` | https://docs.astral.sh/ruff/rules/boolean-positional-value-in-call/ | Lint rule doc states the hazard and recommends keyword arguments |
| `fn-comments-survive-context` | https://docs.webkit.org/Deep%20Dive/Web%20Inspector/Compatibility.html | Compatibility comments name the event that ends them. |
| `fn-comments-survive-context` | https://github.com/PostHog/posthog/blob/master/.agents/skills/writing-code-comments/SKILL.md | Code-comment guide strips "currently"/"today" hedges. |
| `fn-distinct-types-for-ids` | https://rust-lang.github.io/api-guidelines/type-safety.html | API guideline: newtypes distinguish interpretations statically |
| `fn-distinct-types-for-ids` | https://docs.python.org/3/library/typing.html#typing.NewType | Recommends NewType for distinct id types (UserId example) |
| `fn-guard-uri-decoding` | https://raw.githubusercontent.com/remix-run/react-router/main/packages/react-router/lib/router/utils.ts | Production code guards malformed percent decoding of URL segments |
| `fn-link-url-scheme-allowlist` | https://developer.wordpress.org/reference/functions/esc_url/ | Platform's required URL escaper rejects non-allowlisted protocols. |
| `fn-mask-credentials-in-output` | https://docs.aws.amazon.com/cli/latest/reference/configure/list.html | Config list masks secret key to last four characters |
| `fn-mask-credentials-in-output` | https://kubernetes.io/docs/reference/kubectl/generated/kubectl_config/kubectl_config_view/ | Secrets redacted unless explicit --raw flag |
| `fn-mask-credentials-in-output` | https://www.pulumi.com/docs/iac/concepts/secrets/ | Config listing hides secret values by default |
| `fn-no-magic-values` | https://eslint.org/docs/latest/rules/no-magic-numbers | Recommends named constants for unexplained numbers; strings not covered. |
| `fn-no-magic-values` | https://wiki.sei.cmu.edu/confluence/display/c/DCL06-C.+Use+meaningful+symbolic+constants+to+represent+literal+values | CERT rule: use named symbolic constants instead of literals. |
| `fn-specific-exceptions-only` | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1031 | Analysis rule against catching general exception types |
| `fn-specific-exceptions-only` | https://peps.python.org/pep-0008/ | Catch specific exceptions instead of bare except |
| `fn-variants-as-tagged-union` | https://www.typescriptlang.org/docs/handbook/2/narrowing.html | Discriminated union with exhaustiveness check failing on new member |
| `fn-variants-as-tagged-union` | https://doc.rust-lang.org/book/ch06-02-match.html | Enums matched exhaustively; compiler rejects unhandled variants |
| `mod-inject-boundary-collaborators` | https://learn.microsoft.com/en-us/dotnet/core/extensions/dependency-injection-guidelines | Avoid direct instantiation of dependencies inside services |
| `mod-inject-boundary-collaborators` | https://symfony.com/doc/current/service_container.html | Avoid new for dependencies inside classes |
| `mod-inject-boundary-collaborators` | https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html | Google Testing Blog: ask for collaborators in the constructor |
| `mod-internals-unreachable` | https://bazel.build/concepts/visibility | Build fails when a target breaks a dependency's visibility. |
| `mod-internals-unreachable` | https://pkg.go.dev/cmd/go#hdr-Internal_packages | Toolchain blocks imports of internal packages; same org as Bazel (Google). |
| `mod-internals-unreachable` | https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/internal | Compiler error on referencing internal members outside the assembly. |
| `mod-no-logic-in-constructors` | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/constructor | Design guideline: constructors only capture parameters |
| `mod-no-logic-in-constructors` | https://google.github.io/styleguide/cppguide.html | Style guide: use factory or Init for real work |
| `mod-no-logic-in-constructors` | https://legacy.reactjs.org/docs/react-component.html | Forbids side effects and subscriptions in constructor |
| `mod-no-utils-grab-bag` | https://source.android.com/docs/setup/contribute/api-guidelines | Avoid Helper and Util classes for utility collections |
| `mod-no-utils-grab-bag` | https://docs.gitlab.com/development/software_design/ | Put behaviour in the bounded context that owns it |
| `mod-no-utils-grab-bag` | https://feature-sliced.design/docs/guides/issues/desegmented | Methodology rejects generic folders; name modules after the domain |
| `mod-proto-enum-zero-unspecified` | https://buf.build/docs/lint/rules/ | Protobuf tooling style rule requires _UNSPECIFIED zero value |
| `mod-proto-enum-zero-unspecified` | https://github.com/envoyproxy/envoy/blob/main/api/STYLE.md | API style mandates TYPE_NAME_UNSPECIFIED = 0 treated as error |
| `mod-proto-enum-zero-unspecified` | https://github.com/open-telemetry/opentelemetry-proto/raw/refs/heads/main/opentelemetry/proto/trace/v1/trace.proto | Practises meaningless UNSPECIFIED zero value in schema |
| `prod-a11y-audit-before-launch` | https://www2.gov.bc.ca/gov/content/home/accessible-government/toolkit/testing-and-auditing | Formal audit when launching a new public service |
| `prod-a11y-audit-before-launch` | https://design.va.gov/accessibility/ | All VA products must be tested before launch |
| `prod-shadow-compare-before-cutover` | https://americanexpress.io/migrating-the-payments-network-twice | Ran legacy and new side by side to find discrepancies. |
| `prod-shadow-compare-before-cutover` | https://microsoft.github.io/code-with-engineering-playbook/automated-testing/shadow-testing/ | Playbook recommends shadow testing: compare new responses to current. |
| `prod-shadow-compare-before-cutover` | https://shopify.engineering/scaling-inventory-reservations | Compared old and new systems side by side before trusting MySQL. |
| `svc-api-cache-control` | https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html | Security cheat sheet prescribes no-store header on sensitive REST responses. |
| `svc-api-contract-tests` | https://devblogs.microsoft.com/ise/pact-contract-testing-because-not-everything-needs-full-integration-tests | Provider tests against consumer-derived contract |
| `svc-api-contract-tests` | https://en.paradigmadigital.com/dev/architecture-patterns-microservices-consumer-driven-contract-testing/ | Failed provider verification stops the build |
| `svc-api-contract-tests` | https://www.thoughtworks.com/radar/techniques/consumer-driven-contract-testing | Recommends consumer-driven contract tests as essential |
| `svc-api-naming-consistent` | https://google.aip.dev/140 | API guide requires field names consistent with one another. |
| `svc-api-naming-consistent` | https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md | Follow conventions of existing fields across the API. |
| `svc-api-problem-json` | https://ukhsa-collaboration.github.io/standards-org/api-design-guidelines/api-guidelines/error-handling/ | API standard: problem details, no stack traces |
| `svc-api-retry-after` | https://learn.microsoft.com/en-us/azure/architecture/patterns/throttling | Include Retry-After on throttled responses |
| `svc-api-retry-after` | https://shopify.dev/docs/api/admin-rest/usage/rate-limits | Shopify returns Retry-After with 429 |
| `svc-api-retry-after` | https://docs.slack.dev/apis/web-api/rate-limits | Slack returns Retry-After with 429 |
| `svc-api-specific-status-codes` | https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-implementation | Create returns 201 with Location header. |
| `svc-async-content-reserves-space` | https://shopify.dev/docs/storefronts/themes/best-practices/performance/prevent-image-layout-shift | Set dimensions so space is reserved before images load |
| `svc-async-content-reserves-space` | https://www.cloudflare.com/learning/performance/what-are-core-web-vitals/ | Reserve space for late-loading elements before fetch |
| `svc-stream-dont-materialise` | https://jdbc.postgresql.org/documentation/query/ | Cursor-based fetch to avoid loading whole result set |
| `svc-stream-dont-materialise` | https://www.reactive-streams.org/ | Backpressure standard so fast source does not overwhelm consumer |
| `sys-cells-limit-blast-radius` | https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html | Well-Architected guidance: independent cells, no shared state |
| `sys-cells-limit-blast-radius` | https://americanexpress.io/cell-based-architecture-for-resilient-payment-systems/ | Runs cells with own services and data containing failures |
| `sys-cells-limit-blast-radius` | https://learn.microsoft.com/en-us/azure/architecture/patterns/deployment-stamp | Independent stamps limit outage to one stamp's tenants |
| `sys-index-concurrently` | https://devcenter.heroku.com/articles/postgresql-indexes | Use CREATE INDEX CONCURRENTLY to avoid blocking writes |
| `sys-index-concurrently` | https://thoughtbot.com/blog/how-to-create-postgres-indexes-concurrently-in | Concurrent indexes must be created outside a transaction |
| `sys-migration-lock-timeout` | https://gocardless.com/blog/zero-downtime-postgres-migrations-a-little-help | Sets lock_timeout automatically on every migration. |
| `sys-migration-lock-timeout` | https://postgres.ai/blog/20210923-zero-downtime-postgres-schema-migrations-lock-timeout-and-retries | Recommends low lock_timeout with retries for migrations. |
| `sys-migration-lock-timeout` | https://github.com/doctolib/safe-pg-migrations | Tool sets short lock timeout before each migration. |

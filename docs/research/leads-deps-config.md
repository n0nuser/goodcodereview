# Leads: dependencies and configuration

Method: each page fetched with `curl -sL`, tags stripped with `python3 -I`, sentence found with `rg` in the stripped text. Fetch date 2026-11-24. Quotes are 10 words or fewer; the rest is paraphrase. Org grouping follows docs/PROMOTION.md (Google covers Chromium, SRE and the SWE book). Vendor docs of flag tools (Unleash, LaunchDarkly, Statsig) state a practice but also sell the tool; marked "vendor".

Existing-card check (`rg` over `cards/`): already covered are `code-dependency-pinning` (lockfile, stable), `code-dependency-licence-sbom` (SBOM, scan, licence list), `code-vuln-remediation-window`, `code-secrets-not-plaintext-in-repo`, `code-secret-scan`, `svc-fail-closed-defaults`, `svc-debug-off-in-production`, `chg-devex-breaking-config`, `prod-canary-staged-rollout` (applies to config too), `mod-central-config` (draft, lacks orgs) and `chg-flag-owner-retirement` (draft, lacks orgs).

## Ranking

| # | Lead | Orgs | Verdict | Card action |
|---|---|---|---|---|
| 1 | Flag removed after rollout, owner and expiry named | removal 5, expiry 2, owner 2 | removal clears 3 | feeds `chg-flag-owner-retirement`; promote the removal clause |
| 2 | Local `.env` files ignored by git; committed template has placeholders only | 4 | clears 3 | new card, or clause on `code-secrets-not-plaintext-in-repo` |
| 3 | A new dependency is justified before it is added (need, alternative, licence, upkeep) | 3 | clears 3 | new card; near `chg-reuse-before-write` |
| 4 | Config changes live in version control, get review, ship through the code pipeline | 3 (+1 descriptive) | clears 3 | clause on `prod-canary-staged-rollout` or new card |
| 5 | Third-party dependencies are kept current by an update bot or autoroller | 3 (2 soft) | clears 3, soft | clause on `code-dependency-pinning` |
| 6 | Lockfile committed (more sources) | 4 more | clears | add `borrowed_from` to `code-dependency-pinning` |
| 7 | Vendored copy records upstream and version, no local edits | 1 firm, 3 soft | soft | not yet |
| 8 | Config validated before it runs (startup or pre-merge) | 1 firm, 3 soft | short | not yet |
| 9 | Environment-specific values live outside the code and image | 2 firm | short | feeds `mod-central-config` only |

## 1. Flag removed after rollout, with owner and expiry

Rule candidate: "A release flag has a removal path: remove the flag and the dead branch once rollout ends." A diff that adds a flag with no expiry, owner or cleanup ticket is a FAIL. Nearest card: `chg-flag-owner-retirement` (draft; lacks orgs for owner, removal ticket, default). This lead feeds its gaps.

Removal after rollout:
1. https://chromium.googlesource.com/chromium/src/+/main/docs/how_to_add_your_feature_flag.md . Chromium (Google). "When a feature flag is no longer used it should be removed." The same page asks for expiry metadata in `flag-metadata.json`.
2. https://docs.gitlab.com/development/feature_flags/ . GitLab. "Feature flags should remain in the codebase for as short a period as possible." Also: a new flag "must be disabled by default".
3. https://docs.getunleash.io/topics/feature-flags/feature-flag-best-practices . Unleash (vendor). "Keep feature flags short-lived and archive often." Also "Assign expiration dates to feature flags", and "Give them owners, set expiration dates, and add cleanup tasks".
4. https://launchdarkly.com/docs/guides/flags/technical-debt . LaunchDarkly (vendor). A temporary flag: "remove it from the codebase". The page also ties a maintainer to each set of flags for cleanup.
5. https://www.statsig.com/blog/feature-flag-code-cleanup . Statsig (vendor). Create a cleanup ticket when you add the flag, with a target date; link it from the rollout PR.

Count per clause: removal 5 (Chromium, GitLab, Unleash, LaunchDarkly, Statsig); expiry date 2 (Chromium, Unleash); owner 2 (Unleash, LaunchDarkly); cleanup ticket 2 (Statsig, Unleash); default off 1 (GitLab). Martin Fowler's toggles article calls flags "inventory" with a carrying cost; a person, not an org. Not counted: Kubernetes feature gates (lifecycle of a platform's alpha/beta/GA gates, descriptive). Counterpoint already in the card: kill switches and entitlements are permanent; label them. Verdict: the removal clause clears three and can go stable; owner, expiry and default need one more org each, or move them to the Why.

## 2. Local env files ignored by git; committed template holds placeholders only

Rule candidate: "Local environment files (`.env.local`, `.env`) are git-ignored; the committed template contains placeholder values only." Checkable: `.gitignore` lists them, and the committed file has no real credentials. Nearest card: `code-secrets-not-plaintext-in-repo` (stable; rule is "keep secrets out of source and config", sources OWASP, GitLab, CISA, none about env files). Clause or sibling card.

1. https://laravel.com/docs/12.x/configuration . Laravel. "Your .env file should not be committed" to source control; keep a `.env.example` with placeholder values for the team.
2. https://symfony.com/doc/current/configuration.html . Symfony. `.env.local`: "should be ignored by git and should not be committed"; `.env` is committed and holds defaults only.
3. https://nextjs.org/docs/app/guides/environment-variables . Next.js (Vercel). The template adds all `.env` files to `.gitignore`; "almost never want to commit these files"; `.env.*.local` stay ignored.
4. https://vite.dev/guide/env-and-mode . Vite. "You should add `*.local` to your `.gitignore`" because local env files can hold sensitive values.

Count: 4. Soft spot: Symfony, Next.js and Vite do commit a non-secret `.env` of defaults, so the rule must say "local override files" and "secrets", not "every .env". 12factor says env vars have "little chance of being checked into the code repo" (https://12factor.net/config), a related point. Counterpoint: encrypted env files may be committed (Laravel's own page says so; dotenv documents `.env.production` encrypted), so the card allows an encrypted file. Draft id: `code-env-files-ignored-template-committed`.

## 3. A new dependency is justified before it is added

Rule candidate: "A change that adds a third-party dependency states why it is needed, what existing code or library was considered, its licence, and who maintains it." A diff that adds a package with a bare description is a FAIL. Nearest cards: `chg-reuse-before-write` (reuse before writing; does not cover the cost of importing) and `code-dependency-licence-sbom` (licence list, team policy). New card, change level.

1. https://chromium.googlesource.com/chromium/src/+/main/docs/adding_to_third_party.md . Chromium (Google). The review email must give motivation and "alternatives you considered"; the owner commits to upkeep and the licence is classified and approved.
2. https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-architecture/vendor.md . Kubernetes. The checklist asks "Is there already a dependency in the project that does something similar?" and whether the licence is compatible with the project. Also: "Before you update a dependency, ... consider why" with a list of valid reasons.
3. https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software . OpenSSF. Evaluate candidates before use; "eliminate unnecessary ones" because every new dependency is a possible supply-chain or support problem; check licence clarity and maintenance.
4. https://abseil.io/resources/swe-book/html/ch21.html . Google (same org as 1). Asks "What incentives will we have to keep this dependency up to date?" and weighs ongoing maintenance cost.

Count: Google, Kubernetes, OpenSSF = 3. Counterpoint: review friction for a small utility; the Rule can scale by risk (security-critical, runtime vs dev-only) and still require one sentence of why. Draft id: `chg-new-dependency-justified`.

## 4. Config changes live in version control and ship like code

Rule candidate: "Configuration, flags and feature-gate values are changed through a reviewed commit and the same staged pipeline as code, not by hand on a host or console." Nearest card: `prod-canary-staged-rollout` (applies_when already lists config; sources Google SRE canarying, AWS, Azure safe deployments). The new part is review plus version control for config, not rollout. Clause or sibling.

1. https://sre.google/workbook/configuration-design/ . Google SRE. "We recommend storing configuration in version control", which gives history, rollback and code review of config changes. The page also says one config option can change behaviour as much as code, with less testing.
2. https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/ . Amazon. Runtime configuration values (rate limits, feature flags) go through a dedicated pipeline with the same safety mechanisms as code, and a flag pipeline uses the same safe deployment technique as the application pipeline.
3. https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments . Microsoft. A configuration update or feature flag brings risk like a code deploy; "Every deployment must follow a standard pattern".
4. https://opengitops.dev/ . OpenGitOps (CNCF). Desired state is "Versioned and Immutable". Descriptive of a method; soft.

Count: Google, Amazon, Microsoft = 3 firm; OpenGitOps soft. Counterpoint: an incident may need an out-of-band change; the card allows it with a follow-up commit. Cloudflare's 2025-11-18 post-mortem (https://blog.cloudflare.com/18-november-2025-outage/) lists, as its own fix, "hardening ingestion" of generated config like user input and more global kill switches; a remediation list, soft evidence for lead 8.

## 5. Dependencies are kept current by a bot or autoroller

Rule candidate: "The repo has an automated dependency-update job (Dependabot, Renovate, autoroll) enabled, and no dependency is far behind." Checkable: bot config file present; open update PRs not months old. Nearest card: `code-dependency-pinning` (its `tool_gate` names an update bot and the Counterpoint relies on one, but the Rule only says "commit a lockfile"). Add a clause, or a separate card if the lock rule should stay narrow.

1. https://chromium.googlesource.com/chromium/src/+/main/docs/adding_to_third_party.md . Chromium (Google). "It is Chromium policy that third party dependencies be kept up to date"; fresh means no minor or patch release older than 3 months, no major older than a year; use an autoroller.
2. https://raw.githubusercontent.com/ossf/scorecard/main/docs/checks.md . OpenSSF Scorecard. "Out-of-date dependencies make a project vulnerable to known flaws"; the Dependency-Update-Tool check looks for Dependabot or Renovate. Already a source of the pinning card.
3. https://docs.gitlab.com/development/dependencies/ . GitLab. "We have the goal of updating all dependencies with renovate." A stated goal, not a rule.
4. https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/about-dependabot-version-updates . GitHub. Version updates are PRs that keep dependencies updated "even when they don't have any vulnerabilities". Describes the feature; soft.

Count: Google, OpenSSF, GitLab = 3, GitLab and GitHub soft. Counterpoint: churn and supply-chain risk from taking every release at once; answer with cadence, grouping and a cooldown, as the pinning card already says. Sources already on cards, so this lead adds a clause plus Chromium, GitLab and GitHub.

## 6. Lockfile committed: sources to add to `code-dependency-pinning`

These back the existing rule; add to its `borrowed_from`.
- https://doc.rust-lang.org/cargo/faq.html . Cargo (Rust). Section "Why have Cargo.lock in version control?".
- https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json . npm. "This file is intended to be committed into source repositories". The card already cites `npm ci`.
- https://python-poetry.org/docs/basic-usage/ . Poetry. Section "Committing your poetry.lock file to version control".
- https://pnpm.io/cli/install . pnpm. `--frozen-lockfile` fails when the lock needs an update, the CI behaviour the card's PASS shows.
- https://docs.renovatebot.com/dependency-pinning/ . Mend Renovate. Recommends a lock file "regardless of whether you pin", and pinning even with one; also warns that a library should not pin every dependency, which is the lock-for-apps scope caveat the card could carry.

## 7. Vendored copy records upstream and version, no local edits (soft)

Rule candidate: "A vendored or `third_party` directory has a file naming its upstream, version and licence, and carries no local edits except documented patches." Nearest card: none (`code-build-hermetic` and `code-dependency-pinning` do not cover vendoring).

1. https://chromium.googlesource.com/chromium/src/+/main/docs/adding_to_third_party.md . Chromium (Google). A `README.chromium` with URL, version and licence is required and a presubmit checks the format; "do not reformat" vendored code to keep diffs against upstream clean. Firm.
2. https://firefox-source-docs.mozilla.org/mozbuild/vendor/index.html . Mozilla. Vendoring is "done through a descriptive moz.yaml file" beside the third-party code. Describes the tool; soft.
3. https://go.dev/ref/mod . Go. With `vendor/`, `vendor/modules.txt` must be consistent with `go.mod` or the build errors; a tool check, not a stated practice. Soft.
4. https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-architecture/vendor.md . Kubernetes. Review the `go.mod`, `go.sum` and `vendor/` diff to check "the only changes are what the PR claims". Soft.

Count: 1 firm, 3 soft. Not enough. Searched without luck: Android source site (no dependency page found), GitLab dependencies doc (about bot updates only).

## 8. Config validated before it runs (short)

Rule candidate: "An app validates its configuration at startup and exits with a clear error on an invalid value." Nearest card: none (`svc-fail-closed-defaults` is about security defaults; `mod-central-config` mentions validation in its Counterpoint only).

1. https://learn.microsoft.com/en-us/dotnet/core/extensions/options . Microsoft. Options validation "occurs at runtime, but you can configure it to occur at startup" with `ValidateOnStart`. An opt-in feature, not a rule. Soft.
2. https://www.elastic.co/guide/en/elasticsearch/reference/current/bootstrap-checks.html . Elastic. In production mode a failed bootstrap check makes Elasticsearch "refuse to start". Describes a product behaviour. Soft.
3. https://sre.google/workbook/configuration-design/ . Google SRE. "Semantic validation" of config, at commit time: ask whether a misconfiguration could be caught "at the moment the user commits". A different time (pre-merge), firm for that variant only.
4. https://docs.spring.io/spring-boot/reference/features/external-config.html . Spring Boot. `@ConfigurationProperties` classes are validated when annotated with `@Validated`. A feature, not a rule. Soft.

Count: no org states "fail at startup" as a rule. Pre-merge validation has Google SRE plus Cloudflare's remediation (lead 4); nginx `-t` and `promtool check config` are tools. Short.

## 9. Environment-specific values live outside the code and image (short)

1. https://12factor.net/config . Twelve-factor (Heroku authors). Config that varies between deploys belongs in environment variables; the open-source test is a codebase "made open source at any moment, without compromising any credentials".
2. https://kubernetes.io/docs/concepts/configuration/configmap/ . Kubernetes. A ConfigMap "decouple[s] environment-specific configuration from your container images".
3. https://devcenter.heroku.com/articles/config-vars . Heroku. Config vars reach the app as env vars; a platform description. Soft.
4. https://docs.getunleash.io/topics/feature-flags/feature-flag-best-practices . Unleash (vendor). Separates long-lived app config loaded at startup from short-lived flags. Soft.

Count: 2 firm. Already backed by Uber and Cabify for `mod-central-config`'s "no knobs in code". Short; add 12factor and Kubernetes to `mod-central-config` as sources at most. Per-environment config files (Rails, Spring profiles) conflict with 12factor's "no named environments" stance, so a rule on that would split orgs.

## Skipped

- Licence checks, SBOM, scan cadence, remediation window: all covered by `code-dependency-licence-sbom` and `code-vuln-remediation-window` with multiple sources.
- "No secrets in config": `code-secrets-not-plaintext-in-repo`; lead 2 adds the env-file angle.
- Removing unused dependencies: only tool docs (`go mod tidy`) and OpenSSF's "eliminate unnecessary ones" found; one org.
- Safe defaults: `svc-fail-closed-defaults`.

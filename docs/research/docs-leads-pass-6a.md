# Docs leads, pass 6a

Fetched 2026-11-22 with `curl -sL`, tags stripped with `python3 -I`, each sentence found with `rg` in the stripped text (scratch dir from `mktemp -d`). Paraphrases only. WebSearch was used for discovery only; no snippet counts. Prior counts come from `docs-leads-pass-5a.md`.

Result: no practice moved over the bar. N, P, K and E2 gain at most one soft or adjacent org each. Both STEP-5 feeds are confirmed (changelog fully, refactor-separate by Google only).

## N. Library or SDK has its own troubleshooting doc (no card)

1. https://embrace.io/docs/embrace-docs-style-guide/ . Embrace. The setup-page template ends with a Troubleshooting section for common issues. Found in raw text: "Troubleshooting Summarize common issues and solutions". Per-page template, not per library; not counted.
2. https://docs.github.com/en/enterprise-server@3.20/contributing/style-guide-and-content-model/troubleshooting-content-type . GitHub. Defines a troubleshooting content type and known-issues articles per product or feature. Found: "a dedicated "Known issues with NAME" article". Content type, not a per-library duty; not counted.
3. https://raw.githubusercontent.com/hashicorp/web-unified-docs/main/CONTRIBUTING.md . HashiCorp. Troubleshooting section is about previewing the docs site locally. Not the practice.
4. https://docs.newrelic.com/docs/style-guide/writing-docs/processes-procedures/use-content-types-text-formats/ . New Relic. Only 469 bytes came back (JS shell); unverified.

Count: 3 (Microsoft Azure SDK, PostHog, Sentry soft), unchanged. Tried and no rule found: Kubernetes (content-organization, style-guide, page-content-types raw), Rust API guidelines, Django contributing docs, Python devguide, TypeScript CONTRIBUTING (only a FAQ link), Docker CONTRIBUTING, Vue docs README, Elastic (format only). Existing card: none.

## P. Names built at runtime avoided or listed in a comment (no card)

1. https://www.canva.dev/docs/apps/localization/bad-practices.md . Canva. Do not use dynamic message `id` values; the extractor cannot see them, so pick among predefined messages. Found: "Don't use dynamic id values in your messages". Tool limit (extraction), not grep; adjacent. Canva is a new org.
2. https://www.i18next.com/principles/best-practices . i18next. Page fetched (4301 bytes), no match for dynamic or concatenat in the stripped text; not counted.
3. https://shopify.engineering/internationalization-i18n-best-practices-front-end-developers . Shopify. Fetched, no rule about dynamic keys; not counted.

Count, exact practice: 1 (Wikimedia, from 5a). Adjacent (names must be static so tools or search can see them): Wikimedia, Tailwind, Django, Elastic, GitLab, Canva. Not enough for the exact wording. Existing card: none. Nearest: `fn-no-getattr-for-known-names` (dynamic attribute lookup), not the same practice.

## K. Unreferenced orphan doc, image or example files are deleted

1. https://developers.cloudflare.com/style-guide/how-we-docs/image-maintenance . Cloudflare. Remove images that no docs page references. Found: "remove images that are no longer referenced".
2. https://architecture.learning.sap.com/docs/community/automated-checks/orphan-files . SAP. Raw response was 1556 bytes with no text after stripping (JS shell); search snippet only (link it or delete it); not counted.
3. https://raw.githubusercontent.com/mattermost/docs/master/README.md . Mattermost. No orphan guidance in the README.

Count: 1 firm (Cloudflare), plus 5a's Kubernetes soft, IBM and JetBrains partial. Unchanged, below the bar. Existing card: `code-dead-docs-deleted`.

## E2. Each doc page records an owner and a last-reviewed date

1. https://learn.microsoft.com/en-us/contribute/metadata . Microsoft. `ms.author` names the owner; `ms.date` is shown as the last substantial edit. Found: "Displayed on the published page". Owner and date.
2. https://docs.gitlab.com/development/documentation/metadata . GitLab. Every page carries stage and group; pages with no clear owner are marked unassigned. Found: "Documents with no clear group owner". Owner half; no date rule on this page.
3. https://grafana.com/docs/writers-toolkit/write/front-matter . Grafana. `review_date` is the date a page was last reviewed for correctness. Found: "set the date you last reviewed a page". Date half. The page itself shows "Last reviewed".
4. https://developers.cloudflare.com/style-guide/how-we-docs/metadata/index.md . Cloudflare. Tracks last modified for all pages and last reviewed for key content types. Found: "Last reviewed (optional)". Date half, optional.
5. https://docs.databricks.com/aws/en/internal/docs-content-model/content-atoms/frontmatter . Databricks. New. Lists `last_update` as an explicit last-reviewed date among the optional front-matter fields. Found: "an explicit last-reviewed date". Soft: it sits in a field list, the Rules section only requires description and content_type.
6. https://docs.newrelic.com/... use-content-types-text-formats . New Relic. 469-byte shell; unverified.

Count, date half: Microsoft, GitLab (handbook, from 5a), Grafana, Cloudflare (optional), Optimism (curated pages, from 5a), Databricks (soft) = 6, of which only Microsoft and Grafana are clean. Owner half: Microsoft, GitLab = 2. Owner plus date: Microsoft only. Existing card: none (`code-dead-docs-deleted` mentions it as a tool gate only).

## STEP-5 FEEDS

### (a) `chg-changelog-entry` (cards/change/chg-changelog-entry.md)

Card already lists Django, GitLab, Python, Kubernetes, Spark, USGS, Rails. New backing:

1. Django. https://raw.githubusercontent.com/django/django/main/docs/internals/contributing/writing-code/submitting-patches.txt (raw rst, 22434 bytes). Found: a checklist line "is there a release note in" `docs/releases/A.B.txt` for new features; a line says bug fixes applied only to main "don't need a release note". Backs the Rule and the fix counterpoint. Already in `borrowed_from`.
2. Ansible. https://docs.ansible.com/ansible/devel/community/development_process.html (HTML, 55340 bytes). Found: "you must add a changelog fragment to any PR that changes functionality or fixes a bug"; PRs that add new modules and plugins are exempt. Backs the Rule; note it also requires fragments for bug fixes, which cuts against the card's counterpoint ("fix needs entry only if users must act"). The `changelogs/README.md` on raw.githubusercontent (383 bytes) only says changelogs are built from fragments.
3. Grafana. https://raw.githubusercontent.com/grafana/grafana/main/contribute/merge-pull-request.md (9002 bytes). Found: "Does it need to be added to the changelog (release notes)?" in the pre-merge checklist; section "What to include in changelog and release notes" says a changelog decision is needed for every PR, enforced by a "Changelog Check" CI job, with a `no-changelog` label to opt out. Found also: "better to err on the side of inclusion" (so it includes more than the card's counterpoint wants). Backs the Rule.

Verdict: all three source the Rule. Ansible and Grafana are new `borrowed_from` candidates. Both lean toward including bug fixes, which contradicts the Counterpoint; if added, the note should say they differ on fixes.

### (b) `chg-refactor-separate` (cards/change/chg-refactor-separate.md)

1. Google. https://raw.githubusercontent.com/google/eng-practices/master/review/developer/small-cls.md (raw 12289 bytes). Found: heading "Separate Out Refactorings" and "It's usually best to do refactorings in a separate CL from feature changes or bug fixes". Small cleanups such as a local variable rename may stay inside the CL. Already in `borrowed_from` (matches the card's counterpoint).
2. HashiCorp. https://raw.githubusercontent.com/hashicorp/terraform/main/.github/CONTRIBUTING.md (33587 bytes). Not found for refactors or moves. Found a narrower rule: dependency changes are recorded as separate commits that contain only the dependency command output plus minimal compat changes. Found: "we prefer to record dependency changes as separate commits". Not the card's Rule (adjacent: separates dependency bumps). Not counted. Their Terraform CONTRIBUTING has no "refactor separate from behaviour" sentence.

Verdict: Google confirmed (already cited); HashiCorp not found for the card's Rule.

## Unreachable or unverified

- raw.githubusercontent paths that returned 14 bytes (404): ansible `development_process.rst` and `collection_changelogs.rst`, gitlab-org/gitlab `troubleshooting.md`, grafana/writers-toolkit troubleshooting template, DataDog integrations-core `integration-release.md` and `integration.md`, grafana/plugin-tools doc, home-assistant developers docs, github/docs content-model (234 bytes).
- JS shells or empty after stripping: SAP orphan-files page, New Relic style guide pages, grafana.com plugin publish page (1 byte).
- Fetched, no match: Kubernetes website style pages, Rust API guidelines, Django writing-documentation, Python devguide style guide, Docker CONTRIBUTING, Vue docs README, i18next best practices, Shopify i18n article, Airflow documentation building, Backstage plugin docs, HashiCorp terraform-provider-scaffolding.
- Search-snippet only, not counted: Mattermost image issue, Guild Wars 2 wiki, Optum "megadoc" guide, Customer.io and Facebook SDK troubleshooting pages, Roblox i18n thread.

## Parent outcome (2026-11-22)

No new card. Ansible and Grafana added to `chg-changelog-entry` (Ansible URL corrected to the devel path; the sentence matched raw). HashiCorp has no refactor sentence, so nothing was added to `chg-refactor-separate`. Troubleshooting doc, runtime-built names, orphan files and owner plus date stay below the bar.

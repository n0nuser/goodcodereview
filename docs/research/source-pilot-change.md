# Source pilot: change level

Scope: 5 source URLs, up to 3 checkable rules each, checked against `cards/`, `packs/` and `docs/COVERAGE.md`. No card files were created or edited. A NEW candidate is a lead only: a new card needs 3 independent orgs behind it.

Summary: 5 URLs, 3 fetched with content (CSA, ESLint, danluu), 2 blocked (programmingisterrible 403; Apple returned title only). Rules: 2 covered, 2 partial, 1 NEW candidate.

## 1. CSA research note, AI codegen vulnerability debt

- URL: https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-codegen-vulnerability-debt-20260406-csa/
- Fetch status: fetched. Published 2026-04-06 by the Cloud Security Alliance AI Safety Initiative.
- Note: this URL is already in `borrowed_from` of `cards/change/chg-agent-grounded-code.md`, so it is not a new source for that card.

Rules (3 of the page's 15 listed items, picked for checkability):

1. **Verify AI-suggested dependencies exist in the registry.** Quote: "any AI-suggested package dependency exists in the relevant registry". Coverage: **covered**, `chg-agent-grounded-code` (Rule: "Verify that every import and external call the agent wrote exists with that signature"; FAIL example imports `requests_cache_pro`; tool_gate: dependency-resolution in CI).
2. **Secret scanning runs before review.** Quote: secret scanning "should run immediately against any AI-assisted codebase that has not been subjected to prior review." Coverage: **covered**, `code-secret-scan` (severity block; scanner on every push, history included).
3. **Audit for missing database access controls.** Quote: auditing AI-generated apps "specifically for missing database access controls", naming Supabase RLS policies and Firebase security rules. Coverage: **NEW candidate**. `rg` for supabase, firebase, RLS, row-level security and security rules found no card or COVERAGE line. Nearest checked: `svc-authz-central-deny-default` (deny by default, COVERAGE line 438) and `fn-object-level-authz` (caller's right to the record, COVERAGE line 437). Both cover authorization in general, not database rule config. To become a card it needs 2 more independent orgs beyond CSA, for example OWASP ASVS access-control material. Vendor docs (Supabase, Firebase) would be vendor-level sources and are not verified here.

Other CSA items with partial overlap, not scored above: "treat AI output as untrusted" (closest `sys-prompt-injection`, which is system-level, COVERAGE line 462); high-risk paths deserve scrutiny (closest `chg-review-rigour-by-risk`, which tiers by risk but does not list paths); mandatory SAST and SCA gates (closest `code-dependency-licence-sbom`, which covers SCA in CI but not SAST); independent review by a person or fresh reviewer (`chg-agent-independent-review`, already in draft).

## 2. ESLint, configure rules

- URL: https://eslint.org/docs/latest/use/configure/rules
- Fetch status: fetched. This is configuration reference, not review guidance. The rules it names are examples only.

Rules (2 stated behaviours that can be checked in a diff):

1. **Unused suppression directives are reported.** Quote: "This setting defaults to `"warn"`." (for `reportUnusedDisableDirectives`). Coverage: **partial**, `chg-no-silenced-diagnostics`. The card requires a reason and ticket on each suppression. It does not cover a suppression left behind after the warning it hid is gone, which this setting reports.
2. **Inline configuration comments override config files.** Quote: "Rules configured via configuration comments have the highest priority." Coverage: **partial**, `chg-no-silenced-diagnostics`. The card covers inline suppressions. It does not cover an inline comment that changes a rule's severity or options rather than silencing it. The ESLint page is cited in that card's `borrowed_from` already.

## 3. Write code that is easy to delete (programmingisterrible)

- URL: https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
- Fetch status: **blocked**: HTTP 403 Forbidden. Body not retrieved. No rules recorded.

## 4. Tests v. reason (danluu)

- URL: https://danluu.com/tests-v-reason/
- Fetch status: fetched. Content read, but the essay states no code-review rules. It is about tests versus informal reasoning. Quote: "They're necessary for anything above a certain level of complexity." That is guidance on writing tests, not a checkable review rule.
- Rules recorded: 0.

## 5. Apple, set up a project for Xcode Cloud

- URL: https://developer.apple.com/documentation/xcode/setting-up-your-project-to-use-xcode-cloud
- Fetch status: **blocked**: the response contained only the page title ("Setting up your project to use Xcode Cloud | Apple Developer Documentation") and no body text. Not guessed. No rules recorded. It is a CI setup page, so it is unlikely to state review rules even with the body.

## Counts

- Covered: 2 (`chg-agent-grounded-code`, `code-secret-scan`)
- Partial: 2 (`chg-no-silenced-diagnostics` x2)
- NEW candidate: 1 (database access controls; nearest `svc-authz-central-deny-default`, `fn-object-level-authz`)
- Source URLs fetched with content: 3 of 5. Blocked: 2.

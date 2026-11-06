# Cloudflare security-audit-skill: what it does and what we can take

Fetched 2026-11-05 through the GitHub contents API (raw files read: README, SKILL.md, HUNTING.md, VALIDATION-AND-REPORTING.md, the eight companion files, report-schema.json) and WebFetch for the blog post. Source: https://github.com/cloudflare/security-audit-skill (MIT, 61k stars, last push 2026-09-14) and https://blog.cloudflare.com/build-your-own-vulnerability-harness. Paraphrase only; the one verbatim quote is marked. It is one vendor's practice with fleet-scale numbers from its own blog, not a standard.

## What it is

A coding-agent skill that runs a six-phase security audit: reconnaissance, coverage-led hunting, candidate validation, structured output, independent record verification, report. It is process, not a card list: the 8 companion files hold about 100 attack classes, each a short prose prompt, with no sources and no FAIL/PASS examples.

## How it works (the parts that matter to us)

1. **The finder never checks its own finding.** A fresh verifier gets only the candidate and tries to refute it from source. A second fresh verifier re-checks the final record. Any promotion to a stronger verdict goes to a third verifier. The blog says the discovery and validation models differ, and quotes: "If a Hunter is allowed to grade its own homework, it will confidently validate everything it outputs."
2. **Three verdicts, not two.** `confirmed` (full trace plus a bounded observed result), `needs_validation` (an exact unresolved fact outside the source, no severity), `rejected` (disproved, kept so later runs do not repeat the claim). `needs_validation` is "never a parking place for a speculative idea".
3. **A candidate gate.** A finding needs a lower-trust principal, an input, the control that should stop it, the boundary crossed, the affected resource and an observed result. A missing best practice with no affected principal is hardening, not a finding. Do not upgrade a crash to code execution or same-principal action to privilege gain.
4. **Severity needs demonstrated impact**, with five anchors and one discriminator: does the result fully defeat an explicit control for an action with real consequences, or only weaken it?
5. **A coverage ledger.** Work is split into units; a unit is covered, candidate, blocked, deferred or out of scope. A critic agent looks for gaps after every wave. Nothing is called covered without paths and checks. A quick, scoped or budget-limited run must say it is partial. Never imply one run exhausts the target.
6. **Profiles and a budget gate.** `quick`, `standard`, `deep` change breadth and redundancy, never the evidence bar. The budget is counted in agent calls, with critics and verification reserved before hunting.
7. **Runs are additive.** README: a single run found roughly half of what repeated runs found. Prior confirmed records are re-verified when their source changed and carried when it did not.
8. **Machine-checked output.** `findings.json` against a JSON schema with `additionalProperties: false`, plus zero-dependency validators. The validator proves format only.
9. **Execution safety.** Run target code only in an OS sandbox (no network, empty allowlisted environment, read-only target, scratch-only writes, resource limits). If a control is missing, do not run it; record the blocker.
10. **Blog numbers.** 20,799 raw candidates, about 12,057 survived validation; early validation rejected 40% and later 11%; the authors claim no false-negative rate.

## What we already have, and the gap

| Cloudflare idea | Ours today | Gap |
|---|---|---|
| Evidence-tagged findings | `proven / inferred / could not check`, and "drop a finding you cannot back with a line you read" (SKILL.md) | None on tagging. Ours has no `rejected` record, and no refutation step. |
| Candidate gate, hardening is not a finding | Nothing in SKILL.md or audit.md names it | A reviewer can FAIL a card for a missing control with no affected resource. A one-line rule fits. |
| Independent verifier | `chg-agent-independent-review` (card) and interrogate-style practice outside the repo | Not in the review procedure itself. |
| Coverage statement | audit.md has scope and read order | No "partial coverage" line, no unit ledger. |
| Profiles | `quick / default / deep / audit` depth | Matches. Their "never scale away the evidence bar" is worth copying. |
| Attack classes | about 45 security cards | Many classes have no card: see below. |

## Card gaps the companions point at

These attack classes have no card here today (checked by id against `cards/` and `packs/`): HTTP request framing and cache poisoning/deception, Host and forwarded-header trust, OAuth/OIDC callback binding, SAML assertion binding (only `fn-xml-no-external-entities` touches SAML), MFA/passkey and step-up binding, account linking and identity collision, password reset and recovery, API-key scope, soft-delete and tombstone bypass, search/cache/index ACL drift, export/backup scope expansion, quota reset gaps, decompression amplification (only touched by `svc-upload-validate-store`), poison-message head-of-line blocking, stale or out-of-order message acceptance, workload identity overreach, unpinned build inputs and untrusted code in a privileged workflow (partly `code-workflow-supply-chain`), RAG cross-tenant context bleed.
The companions give no sources, so each would need its own research pass (OWASP, PortSwigger, RFCs, cloud vendors) before it could be stable. Several already have strong org backing in the wild (OWASP cheat sheets for CSRF/session/JWT/SAML/OAuth/password reset; PortSwigger for cache poisoning and request smuggling; RFC 9110/9112).

## Source value of Cloudflare as an organisation

Cloudflare counts as one organisation (blog.cloudflare.com and the repo). It backs process claims (independent validation of findings, `needs_validation` instead of guessing, coverage tracking, multiple passes), not card rules directly. `tools/orgs.py` already maps `blog.cloudflare.com` to `cloudflare`; the repo URL `github.com/cloudflare/` has no prefix, so add one before citing it.

# Judge triage, 2026-11-06

Four judges, one shared brief: Opus and Sonnet on each partition (security: 21 cards, other: 21 cards). Reports: `judge-sec-opus.md`, `judge-sec-sonnet.md`, `judge-other-opus.md`, `judge-other-sonnet.md`. The DeepSeek judges stopped when the OpenCode Go quota ran out, so neither cross-family judge reported.

A finding is "both" when both judges raised it on their own (highest signal). The status decisions below are the coordinator's; no fix has been applied yet.

## Act on

| Card | Finding | Raised by | Decision |
|---|---|---|---|
| svc-oauth-code-flow-binding | PASS reads `redirect_uri` from the callback query (attacker-controlled) and uses `assert` for security checks | both | fix PASS; stays stable |
| svc-password-reset | single-use, short-lived and hash clauses at 2 orgs (OWASP, NIST) | both | draft, `lacks: orgs`, or Rule narrowed to the session-revocation clause (3) |
| svc-tenant-id-in-telemetry | 2 orgs (OWASP, AWS) | both | draft |
| fn-no-stringly-typed-returns | closed-type-for-returns has 1 to 2 orgs; the boolean half repeats a stable card | both | back to draft |
| mod-no-module-mutable-state | widening to class/static fields has 1 to 2 orgs | both | narrow the Rule back to module level; class fields go to Why |
| mod-law-of-demeter | Counterpoint threshold ("three or more") contradicts the PMD gate (trustRadius 1) | both | fix the threshold text; stable |
| svc-decompression-cap | "1 KB gzip to 1 GB" is wrong (DEFLATE tops out near 1030:1) | Sonnet (measured) | fix numbers; stable |
| svc-api-key-scope | NIST page does not back it; "rotate on a schedule" 2 orgs; unreachable PASS lines | both | drop NIST, move schedule to Why, fix PASS; stable |
| svc-export-scope | "filter inside the export query" 1 to 2 orgs | both | move to Why; stable |
| svc-webhook-replay-window | Stripe URL dead; PASS wrong; tolerance at 2 or 3 depending on Stripe | both | fix URL and PASS; stable only if Stripe re-fetch backs the window, else draft |
| svc-dlq | Dropbox is a proposal; Netflix/Uber not confirmed by Sonnet; `.fifo` names | both | fix names; re-fetch Netflix and Uber; draft if fewer than 3 |
| fn-no-caller-mutation | the Rust source does not back the Rule | Opus | drop Rust; stable on Airbnb, ESLint, Meta |
| mod-one-name-per-concept | a Google claim not backed | Sonnet | drop it; two-class case stays in Why |
| svc-soft-delete-default | PostgreSQL/S3 sentences off-topic | Sonnet | cut; stable |
| mod-temporary-field | Refactoring.Guru backs a different smell; Why and FAIL wrong | both | fix; stays draft |
| chg-no-per-user-ide-files | tool gate wrong; OS-metadata clause 0 orgs | both | fix gate, drop OS clause from Rule; draft until re-judged |
| code-workflow-supply-chain | FAIL YAML invalid | Opus | fix YAML |

## Consider (judges split; coordinator's call)

| Card | Opus | Sonnet | Decision |
|---|---|---|---|
| fn-length-budget | stable | draft: no org *recommends* setting a linter limit | reword the Rule to the split clause (4 orgs); keep the limit in tool_gate; stable |
| mod-class-size-budget | stable (4) | draft: rationale 2 | same shape as fn-length-budget: stable on enforcement, rationale in Why |
| svc-mfa-step-up | stable (factor change 3) | draft (sensitive actions 2) | keep stable on the clauses with 3; recovery path to Why; severity should-fix |
| fn-known-keys-get-a-type | draft (PSF and mypy same team) | stable after moving open-key clause to Why | draft: mypy and PEP 589 come from one team, so 2 independent orgs |
| code-test-selection-on-pr | draft until a threshold | stable with a time condition in applies_when | add the time condition; stable |
| svc-saml-assertion-binding | stable | stable if the checks count as one clause | stable: the checks are one "verify the assertion" clause, each step cited |
| svc-cache-key-completeness | stable | drop Microsoft as a source | drop Microsoft; stable on AWS, Fastly, Cloudflare |
| `assert` in PASS examples (oauth, saml, account-linking) | consider | n/a | replace with explicit raise in all three |

## Noted

- py-test-hygiene and py-class-earns-its-instance rest on the creator exception; both judges accept them as stable.
- fn-comments-explain-why, mod-internals-unreachable, mod-behaviour-lives-with-state, mod-no-shotgun-surgery, fn-parameter-limit, svc-request-framing, svc-host-header-trust, fn-header-value-encoding, code-workload-identity, svc-rate-limit-quota, svc-session-lifecycle, svc-api-cache-control: PASS, or consider-only findings. Apply the small prose and wording fixes.
- Service level is over two size caps (`service-index.md` > 12,000; `service.html` 132K > 120K). Cutting the long Why and Counterpoint text the judges flagged helps but will not be enough alone.

## Dismissed

None so far. Each judge finding cites a page or a line.

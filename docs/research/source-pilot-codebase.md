# Source pilot (codebase level): coverage of five source pages

Quotes come from WebFetch's summary of each page, not from a verbatim copy. Treat them as tight paraphrases and re-check wording against the page before citing.

## 1. OWASP Secrets Management Cheat Sheet

URL: https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html
Fetch status: fetched.

| # | Rule (checkable) | Evidence quote (section) | Coverage |
|---|---|---|---|
| 1 | Do not put secrets in Docker config: "secrets themselves should never be hardcoded using docker ENV or docker ARG commands" (5.1) | same | partial: `sys-secrets-and-errors` says "read them from the environment or a secrets manager" in Why, but has no build-time ENV/ARG check. `code-secret-scan` covers committed credentials, not build args. No Dockerfile card exists. |
| 2 | Secrets must never be logged in plaintext: "Never be logged" (8.3) | same | covered: `sys-secrets-and-errors` (tool_gate: log-redaction tests); also `fn-mask-credentials-in-output` for displayed config. |
| 3 | Keep secrets out of commits and revoke exposed ones: "avoid checking secrets into code before commit/PR" (8.1); "Keys that were exposed should undergo immediate revocation" (9.2) | same | covered: `code-secret-scan` (scanner on push, history scan, revoke-and-replace). |

## 2. Airtable: how Airtable manages flaky tests in a large-scale monorepo

URL: https://medium.com/airtable-eng/how-airtable-manages-flaky-tests-in-a-large-scale-monorepo-5fe09922e90c
Fetch status: blocked: HTTP 403 Forbidden. No content retrieved, no rules listed.

## 3. Palantir: code review best practices

URL: https://blog.palantir.com/code-review-best-practices-19e02780015f
Fetch status: blocked: HTTP 403 Forbidden. No content retrieved, no rules listed.

## 4. Spotify: "Code with Claude: coding is no longer the constraint"

URL: https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint
Fetch status: fetched. No checkable code-review rules stated. Closest statements (not rules): "auto-merging what's safe, focusing review where it matters most" (review triage, undefined criteria); lint feedback loop; CI build verification. Nothing to map.

## 5. Bazel: hermeticity

URL: https://bazel.build/basics/hermeticity
Fetch status: fetched.

| # | Rule (checkable) | Evidence quote | Coverage |
|---|---|---|---|
| 1 | The build should not write to the source tree: "Writing to the source tree during the build." | same | NEW candidate. Nearest: `code-build-hermetic` (covers declared inputs and host tools, not writes). No card covers writes to the source tree. Would need two more independent orgs (not Bazel) stating this as a rule before a card. |
| 2 | Actions must not create files non-deterministically, such as with build IDs or timestamps: "create files non-deterministically, usually involving build IDs or timestamps." | same | covered: `code-build-hermetic` (FAIL `date > BUILD_ID`; PASS `SOURCE_DATE_EPOCH`). |
| 3 | Tools and dependencies must be pinned, not taken from the host: "They depend on specific versions of build tools." / "Hermetic build systems treat tools as source code." | same | covered: `code-build-hermetic` (pin toolchain, no host binaries) and `code-dependency-pinning` (lockfile install in CI). |

## Summary

- Covered: 4 (OWASP #2, #3; Bazel #2, #3)
- Partial: 1 (OWASP #1, Docker ENV/ARG: `sys-secrets-and-errors`, missing build-time check)
- NEW candidate: 1 (Bazel #1, writes to the source tree; nearest `code-build-hermetic`)
- Blocked: 2 of 5 URLs (Airtable, Palantir). Spotify fetched with no rules.

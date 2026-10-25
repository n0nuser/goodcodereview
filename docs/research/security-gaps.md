# Security gaps: ASVS 5.0 and CWE Top 25 against the security cards

Checked 2026-10-24. ASVS requirement ids come from the `5.0/en` chapter files in github.com/OWASP/ASVS (V1 to V16 opened; V10 OAuth and V17 WebRTC not read). The CWE list is the 2025 CWE Top 25 (https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html); cwe.mitre.org/top25 shows no 2026 list yet. Each CWE id outside the Top 25 was opened on cwe.mitre.org, except 209 and 636, which `sys-secrets-and-errors` already cites. Fetched through WebFetch, so descriptions are paraphrases. ASVS ids mean "this requirement backs the Rule or part of it"; a "(part)" mark means the requirement covers only one clause.

## 1. Per-card mapping

| Card | ASVS 5.0 | CWE (Top 25 rank in brackets) |
| --- | --- | --- |
| `chg-name-attack-surface` | 15.1.5 (part: document where dangerous functionality sits) | none |
| `code-dependency-licence-sbom` | 15.1.1, 15.1.2, 15.2.1 | 1395 |
| `code-dependency-pinning` | 15.2.4, 15.1.2 | 494 |
| `code-secret-scan` | 13.3.1, 13.3.4 | 798 |
| `code-workflow-supply-chain` | 15.2.4, 15.2.5 (part) | 829, 494 |
| `fn-confine-file-path` | 5.3.2, 5.3.3, 5.4.1 | 22 [6] |
| `fn-csprng-for-secrets` | 11.5.1, 11.5.2, 7.2.3 | 338, 330 |
| `fn-jwt-verify-pinned` | 9.1.1, 9.1.2, 9.1.3, 9.2.1, 9.2.2, 9.2.3 | 347 |
| `fn-no-mass-assignment` | 15.3.3, 8.2.3 | 915 |
| `fn-no-native-deserialise-untrusted` | 1.5.2, 15.1.5 | 502 [15] |
| `fn-no-raw-html-sink` | 1.2.1, 1.2.3, 1.3.1, 3.2.2 | 79 [1], 80 |
| `fn-no-shell-with-input` | 1.2.5 | 78 [9], 77 [23] |
| `fn-object-level-authz` | 8.2.2, 8.3.1 | 639 [24], 862 [4], 863 [17] |
| `fn-password-slow-hash` | 11.4.2, 11.4.4 | 916 |
| `fn-response-fields-explicit` | 15.3.1, 8.2.3 | 200 [20], 213 |
| `fn-tls-verify-on` | 12.3.2, 12.2.1, 12.1.1 | 295 |
| `mod-vetted-crypto-only` | 11.2.1, 11.3.1, 11.3.2, 11.3.3, 11.3.4 | 327, 323 |
| `svc-api-no-internal-fields` | 15.3.1, 8.2.3 | 200 [20], 213 |
| `svc-auth-throttle-generic-errors` | 6.3.1, 6.3.8, 6.1.1, 2.4.1 | 307, 204 |
| `svc-authz-central-deny-default` | 8.1.1, 8.2.1, 8.3.1 | 862 [4], 863 [17], 284 [19] |
| `svc-bound-client-controlled-sizes` | 2.2.1, 2.4.1, 4.2.5, 4.3.1, 5.2.1, 5.2.3 | 770 [25], 400, 409 |
| `svc-cors-allowlist` | 3.4.2, 3.5.2 | 942, 346 |
| `svc-csrf-state-changing` | 3.5.1, 3.5.3, 3.3.2 | 352 [3] |
| `svc-rate-limit-quota` | 2.4.1, 5.2.4 (part), 15.2.2 | 770 [25] |
| `svc-security-event-logging` | 16.2.1, 16.2.5, 16.3.1, 16.3.2, 16.3.3, 16.4.1 | 778, 532, 117 |
| `svc-security-headers` | 3.4.1, 3.4.4, 3.4.6 | 693, 1021, 319 |
| `svc-session-lifecycle` | 7.2.4, 7.4.1, 3.3.1, 3.3.2, 3.3.4 | 384, 613, 614, 1004, 1275 |
| `svc-sqli-authn` | 1.2.4 | 89 [2] |
| `svc-upload-validate-store` | 5.1.1, 5.2.1, 5.2.2, 5.3.1, 5.3.2, 5.4.1 | 434 [12], 22 [6] |
| `sys-agent-tool-least-privilege` | 8.2.1, 8.3.3, 13.2.2 | 250 |
| `sys-pii-minimise-retention` | 14.1.2, 14.2.6, 14.2.7, 16.2.5 | 200 [20], 532 |
| `sys-prompt-injection` | none (ASVS 5.0 has no LLM chapter) | 1427 |
| `sys-secrets-and-errors` | 16.5.1, 16.5.3, 13.3.1, 13.4.2 | 209, 636, 798 |
| `sys-ssrf` | 1.3.6, 13.2.4, 13.2.5, 15.3.2 | 918 [22] |

## 2. Top 25 items with no card (notes only)

| CWE | Item | State |
| --- | --- | --- |
| 787, 125, 120, 121, 122 | Out-of-bounds write and read, classic, stack and heap buffer overflow | No card; skipped in pass 2 (`security-gaps-pass-2.md`). Language-specific (C, C++, unsafe Rust, FFI); a card needs a `lang:` tag and a rule such as "check length before copy, or use a bounds-checked type". |
| 416 | Use after free | No card. Same family as above. |
| 476 | NULL pointer dereference | No card. Reaches beyond security; `fn-empty-collection-not-none` is the nearest. |
| 94 | Code injection (`eval`, `exec`, template injection) | Draft `fn-no-eval-untrusted` (ASVS 1.3.2, 1.3.7). `fn-no-shell-with-input` covers commands only. |
| 20 | Improper input validation | Partial. `mod-validate-at-boundary-once` and `svc-bound-client-controlled-sizes` touch it, but neither is tagged security and neither states "allowlist at a trusted server layer" (ASVS 2.2.1, 2.2.2). |
| 306 | Missing authentication for critical function | Draft `svc-authn-by-default`. `svc-authz-central-deny-default` denies without a rule. |
| 284 | Improper access control | Covered at parent level by the authorization cards. |

## 3. ASVS areas with no card (not in the Top 25)

- XML external entities and parser hardening (1.5.1): draft `fn-xml-no-external-entities`.
- Open redirects and URL scheme checks (1.2.2; redirect allowlists are 3.7.2): draft `fn-redirect-target-allowlist`.
- Sensitive data in URLs and query strings (14.2.1): draft `svc-no-secrets-in-url`; anti-caching headers (14.3.2); `svc-api-cache-control` is not tagged security.
- TLS version and cipher policy for servers (12.1.1, 12.1.2): draft `svc-tls-modern-only`.
- Credential recovery, MFA enrolment, reset flows (6.4.x). Skipped in pass 2: no single Rule that can fail.
- OAuth and OIDC client and server rules (V10; not read).
- WebSocket origin and token rules (4.4.2, 4.4.3); GraphQL depth and introspection (4.3.1, 4.3.2); HTTP request smuggling (4.2.1 to 4.2.4).
- Time-of-check races on security checks (15.4.2); prototype pollution (15.3.6, draft `fn-no-prototype-pollution`); HTTP parameter pollution (15.3.7).
- Content Security Policy beyond `frame-ancestors` (3.4.3): draft `svc-csp-strict-script-src`; DOM clobbering (3.2.3).
- Log injection (16.4.1) is only a clause inside `svc-security-event-logging`.

## 4. Observations a promoter should know

- `svc-api-no-internal-fields` and `fn-response-fields-explicit` have the same Rule in different words and the same ASVS id (15.3.1). One may be redundant.
- `svc-sqli-authn` is about SQL injection only; the id suggests authentication. The Rule is fine, the name is not.
- `fn-no-native-deserialise-untrusted` says "never"; the Oracle Java page treats stream filters as a defence for cases that cannot avoid native deserialisation. Python, .NET and CodeQL pages back the stricter reading.
- `code-workflow-supply-chain`: GitHub's page says a workflow dependency lockfile, where a repo can adopt one, is stronger than SHA pinning. The Rule still holds; the Counterpoint could mention this.
- `svc-security-headers`: IETF backs HSTS only; Mozilla (guidelines and MDN) backs all three headers; OWASP backs all three. The `frame-ancestors` clause therefore has two orgs (OWASP, Mozilla). Mozilla marks `nosniff` "recommended" and HSTS and framing protection "mandatory".
- `svc-csrf-state-changing`: "never change state on GET" has OWASP and Mozilla behind it; Django's page does not discuss it.
- `svc-session-lifecycle`: "new session ID at login" has OWASP (ASVS 7.2.4) and Spring Security behind it; NIST's session page did not mention it, and the IETF cookie draft only says servers "SHOULD take care" to avoid fixation.
- `svc-auth-throttle-generic-errors`: NIST caps failed attempts per authenticator at 100 and ASVS 6.1.1 warns against throttling that enables malicious lockout. The Rule says "limit failed attempts per account"; a Counterpoint on lockout abuse would match the sources.
- `sys-ssrf`: the Rule says check the resolved address against an allowlist. CodeQL's preferred fix is an allowlist of URLs, with a resolved-IP non-private check as the fallback. The card may want to name both.
- `chg-name-attack-surface`: the "list in the description" clause is synthesis; the sources back a trigger for threat modelling and routing to a security reviewer. It also remains `block` severity with a one-line check; that is a severity call for the stable pass.
- `svc-rate-limit-quota` is a reliability control more than a security one; NIST 800-228 distinguishes rate limits (fairness) from quotas (billing tiers). The security tag is defensible only through CWE-770.

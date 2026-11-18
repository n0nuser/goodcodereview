# Source pilot: service level

Brief: find code-review rules in 5 source pages that the card set may not cover yet. Coverage checked with `rg` across `cards/`, `packs/` and `docs/COVERAGE.md`, reading the nearest card in each case. Fetch quotes come from WebFetch's summarising model, so they are tight paraphrase with quoted fragments, not verbatim page text. Re-check a quote against the live page before it goes into a card.

Totals: 6 covered, 8 partial, 1 NEW candidate (15 rules across 5 URLs). No card files were created or edited.

---

## 1. OWASP TLS Cheat Sheet

- URL: https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
- Fetch status: fetched

| # | Rule (paraphrase) | Evidence quote | Mark | Card |
|---|---|---|---|---|
| 1 | Web apps default to TLS 1.3 and may support TLS 1.2 | "Web applications must default to TLS 1.3 and may support TLS 1.2 for compatibility." | covered | `svc-tls-modern-only` (accept only 1.2 and 1.3) |
| 2 | TLS 1.0 and 1.1 must be disabled | "TLS 1.0 and TLS 1.1 are formally deprecated by RFC 8996 (March 2021) and must be disabled." | covered | `svc-tls-modern-only` |
| 3 | All cookies must carry `Secure` | "All cookies must be marked with the "Secure" attribute." | partial | `svc-session-lifecycle` covers the session cookie only. Missing: the rule for non-session cookies. |

## 2. Spring Security: Authorize HTTP requests

- URL: https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html
- Fetch status: fetched

| # | Rule (paraphrase) | Evidence quote | Mark | Card |
|---|---|---|---|---|
| 1 | Every request must be authenticated by default | "By default, Spring Security requires that every request be authenticated." | covered | `svc-authn-by-default` (its `borrowed_from` includes this URL) |
| 2 | Matchers are applied in listed order, and only the first match applies | "`AuthorizationFilter` processes these pairs in the order listed, applying only the first match to the request." | NEW candidate | Nearest: `svc-authz-central-deny-default`, `svc-authn-by-default`. Neither says anything about rule order. A grep for "first match", "rule order" and "matcher order" found nothing. To become a card it needs two more independent orgs on route or matcher ordering (for example ASP.NET Core or Django routing docs). The Spring page alone is one org. |
| 3 | Deny by default turns the rules into an allow list | "Denying the request by default is a healthy security practice since it turns the set of rules into an allow list." | covered | `svc-authz-central-deny-default`. Note: its `borrowed_from` does not list this URL. |

## 3. CodeQL: js-cors-misconfiguration-for-credentials

- URL: https://codeql.github.com/codeql-query-help/javascript/js-cors-misconfiguration-for-credentials/
- Fetch status: fetched

| # | Rule (paraphrase) | Evidence quote | Mark | Card |
|---|---|---|---|---|
| 1 | `Access-Control-Allow-Origin` must not be `*` (credentialed case) | "the `Access-Control-Allow-Origin` header must have a value different from `"*"`" | partial | `svc-cors-allowlist` says `*` is fine for a public API with no credentials. The page states the rule without that exception. The card's narrower wording is a deliberate choice, but it differs from the source and should be noted if this rule is adopted. |
| 2 | `null` origin is never a safe value | "it is never safe to use `"null"` as the value of the `Access-Control-Allow-Origin` header" | covered | `svc-cors-allowlist` ("allowing the `null` origin") |
| 3 | Origin-derived values must be sanitised if they come from user input | "must involve sanitization if it relies on user-controlled input." | covered | `svc-cors-allowlist` (reflecting any `Origin`, subdomain regex) |

## 4. RFC 8594 (Sunset HTTP header)

- URL: https://www.rfc-editor.org/rfc/rfc8594.html
- Fetch status: fetched

| # | Rule (paraphrase) | Evidence quote | Mark | Card |
|---|---|---|---|---|
| 1 | Send `Sunset` only once the resource is decommissioned, not while it is still operational but deprecated | Sec. 1.4: the Sunset header is "appropriate" once decommissioned, but "not appropriate" while still operational but deprecated. | partial, with conflict | `svc-api-deprecation-sunset` says to send `Deprecation` and `Sunset` on routes marked deprecated. Its PASS example sends `Sunset` on a live 200 response. That contradicts Sec. 1.4 as quoted. Resolve before relying on that card's PASS example. |
| 2 | `Sunset` value is an HTTP-date, and SHOULD be in the future | Sec. 3: "The Sunset value is an HTTP-date timestamp" and "SHOULD be a timestamp in the future." | partial | `svc-api-deprecation-sunset` uses an HTTP-date but does not state the future requirement. Its example date, `Wed, 01 Jul 2026`, is before today (2026-11-16). |
| 3 | Link relation `rel="sunset"` points to the retirement policy | Sec. 7.2: the "sunset" relation "Identifies a resource that provides information about the context's retirement policy." | partial | `svc-api-deprecation-sunset` uses `rel="deprecation"` in its example and never mentions `rel="sunset"`. |

## 5. NIST SP 800-63B-4 (events)

- URL: https://pages.nist.gov/800-63-4/sp800-63b/events/
- Fetch status: fetched

| # | Rule (paraphrase) | Evidence quote | Mark | Card |
|---|---|---|---|---|
| 1 | Record the date and time of significant authenticator lifecycle events | Sec. 3: "The record created by the CSP SHALL contain the date and time of significant authenticator life cycle events" | partial | `svc-security-event-logging` covers failed logins, with account and timestamp. Missing: enrolment, change, reset and other lifecycle events. |
| 2 | Verification of saved recovery codes is subject to throttling | Sec. 4.2.1: "The verification of saved recovery codes SHALL be subject to the throttling requirements" | partial | `svc-auth-throttle-generic-errors` covers login, reset and one-time-code endpoints with per-account limits. Recovery codes are not named. |
| 3 | An expired authenticator must not be usable | Sec. 4.4: "When an authenticator expires, it SHALL NOT be usable for authentication." | partial | Nearest: `svc-password-reset` (reset token expiry, tested by "redeems an expired one") and `svc-api-key-scope` (key expiry). No card states the general rule that an expired authenticator is refused. |

---

## Summary

| URL | Rules | Covered | Partial | NEW |
|---|---|---|---|---|
| OWASP TLS | 3 | 2 | 1 | 0 |
| Spring authorize requests | 3 | 2 | 0 | 1 |
| CodeQL CORS credentials | 3 | 2 | 1 | 0 |
| RFC 8594 Sunset | 3 | 0 | 3 | 0 |
| NIST 800-63B events | 3 | 0 | 3 | 0 |
| **Total** | **15** | **6** | **8** | **1** |

Fetch status: all 5 fetched, none blocked.

## Leads and follow-ups

- **Sunset conflict (RFC 8594 vs `svc-api-deprecation-sunset`).** The most important finding. The card's rule and PASS example send `Sunset` while the route is still live. Decide which reading is right, then fix the card's example and its `borrowed_from` list. This needs an edit to an existing card, which is outside this pilot.
- **Non-session cookie `Secure` (OWASP TLS).** Covered for session cookies only. Either widen `svc-session-lifecycle` or add a card, which would need a second source.
- **Route ordering (Spring, NEW).** Needs two more independent orgs before it can be a card.
- **Authenticator expiry and lifecycle logging (NIST).** Partial coverage. A general expiry card would need sources beyond NIST, so that is a candidate for a new card only once two more orgs are found.

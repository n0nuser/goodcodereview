# Security gaps, pass 2: sources for eight new draft cards

Checked 2026-10-25. Each URL was fetched with `curl -sL` and a browser User-Agent, and the tags were stripped. The NIST PDF was read with `pdftotext`. Quotes are text seen on the page, 15 words or fewer. Year is the date the page states, or `n.d.` when it states none. The gaps come from sections 2 and 3 of `docs/research/security-gaps.md`.

OWASP (ASVS and Cheat Sheets) counts as one org. MITRE (CWE), Mozilla (MDN), Google (web.dev), PortSwigger, Microsoft, GitHub (CodeQL), Snyk, IETF, NIST, the Django project, and Spring (Broadcom) count as separate orgs.

## fn-no-eval-untrusted (CWE-94, ASVS 1.3.2 and 1.3.7)

Orgs: OWASP, MITRE, Mozilla, PortSwigger (4).

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md | OWASP | 2025 | 1.3.2: avoid `eval()` and dynamic code features such as SpEL. 1.3.7: do not build templates from untrusted input. | Rule |
| https://cwe.mitre.org/data/definitions/94.html | MITRE | n.d. | "Refactor your program so that you do not have to dynamically generate code." | Rule |
| https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval | Mozilla | n.d. | "Never use direct eval()!" | Rule (JavaScript) |
| https://portswigger.net/web-security/server-side-template-injection | PortSwigger | n.d. | Best prevention is "to not allow any users to modify or submit new templates". Says sandboxing untrusted code is hard. | Rule (templates), Counterpoint |

Tool names seen: Bandit B307 `eval` (https://bandit.readthedocs.io/en/latest/blacklists/blacklist_calls.html, suggests `ast.literal_eval`), Bandit B102 `exec_used` (https://bandit.readthedocs.io/en/latest/plugins/b102_exec_used.html), CodeQL `py/code-injection` (https://codeql.github.com/codeql-query-help/python/py-code-injection/), ESLint `no-eval` (https://eslint.org/docs/latest/rules/no-eval) and `no-implied-eval` (https://eslint.org/docs/latest/rules/no-implied-eval).

## fn-redirect-target-allowlist (CWE-601, ASVS 3.7.2 and 1.2.2)

Orgs: OWASP, MITRE, Microsoft, PortSwigger, GitHub (5). ASVS puts redirect allowlists in 3.7.2, and 1.2.2 covers safe URL schemes such as rejecting `javascript:`.

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html | OWASP | n.d. | Map a short name or ID to the URL on the server; otherwise allowlist destinations by parsed scheme, host, and port. | Rule, Why |
| https://cwe.mitre.org/data/definitions/601.html | MITRE | n.d. | Input validation with a list of acceptable inputs. | Rule |
| https://learn.microsoft.com/en-us/aspnet/core/security/preventing-open-redirects | Microsoft | n.d. | Use `LocalRedirect` so only local URLs are followed. | Rule, tool_gate |
| https://portswigger.net/kb/issues/00500100_open-redirection-reflected | PortSwigger | n.d. | Use absolute URLs and check the user value starts with your own domain. | Rule |
| https://codeql.github.com/codeql-query-help/python/py-url-redirection/ | GitHub | n.d. | "maintain a list of authorized redirects on the server". Query `py/url-redirection`. | Rule, tool_gate |

## svc-no-secrets-in-url (ASVS 14.2.1, CWE-598)

Orgs: OWASP, IETF, MITRE, Mozilla (4).

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x23-V14-Data-Protection.md | OWASP | 2025 | 14.2.1: sensitive data goes in the body or headers; the URL and query string must not hold API keys or session tokens. | Rule |
| https://www.rfc-editor.org/rfc/rfc6750.html | IETF | 2012 | "Bearer tokens SHOULD NOT be passed in page URLs". | Rule (tokens) |
| https://cwe.mitre.org/data/definitions/598.html | MITRE | n.d. | The query string can be saved in browser history, sent in Referers, and stored in web logs. | Why |
| https://developer.mozilla.org/en-US/docs/Web/Security/Referer_header:_privacy_and_security_concerns | Mozilla | n.d. | Use POST over GET "to avoid passing sensitive data to other locations via URLs". Suggests single-use reset URLs. | Rule, Counterpoint |

No tool rule found that flags this, so `tool_gate` is `none`.

## fn-xml-no-external-entities (CWE-611, ASVS 1.5.1)

Orgs: OWASP, MITRE, PortSwigger, GitHub (4).

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html | OWASP | n.d. | "Disable document type definitions (DTDs) whenever possible." If DTDs are needed, disable external entities and limit expansion. ASVS 1.5.1 (V1 URL above) says the same. | Rule |
| https://cwe.mitre.org/data/definitions/611.html | MITRE | n.d. | "Many XML parsers and validators can be configured to disable external entity expansion." | Rule |
| https://portswigger.net/web-security/xxe | PortSwigger | n.d. | The easiest and most effective prevention is to disable the dangerous parser features. | Rule |
| https://codeql.github.com/codeql-query-help/python/py-xxe/ | GitHub | n.d. | Disable external entity handling; recommends `defusedxml`. Notes recent Python stdlib XML parsers disable entity expansion by default. | Rule, PASS, Counterpoint |

Tool names seen: CodeQL `py/xxe`; Bandit B313 to B319 (XML calls, listed on the blacklist_calls page above, B320 marked removed) and B405 to B410 (https://bandit.readthedocs.io/en/latest/blacklists/blacklist_imports.html). The card does not repeat CodeQL's claim that the default lxml parser resolves external entities: the lxml 5.0.0 changelog (https://lxml.de/changes-5.0.0.html, 2023) says the new default is `resolve_entities='internal'`. The FAIL opts in explicitly. Python's own `xml` page (https://docs.python.org/3/library/xml.html) now talks about Expat versions and was not used.

## svc-authn-by-default (CWE-306)

Orgs: MITRE, Microsoft, Django, Spring (4). No OWASP page was used.

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://cwe.mitre.org/data/definitions/306.html | MITRE | n.d. | Split the software into anonymous and other areas, decide which need a proven identity, and use central authentication. | Rule |
| https://learn.microsoft.com/en-us/aspnet/core/security/authorization/secure-data | Microsoft | n.d. | Sets `FallbackPolicy` to require an authenticated user; `[AllowAnonymous]` marks intentionally public endpoints. | Rule, tool_gate |
| https://docs.djangoproject.com/en/5.2/ref/middleware/ | Django | 2025 | `LoginRequiredMiddleware` "Redirects all unauthenticated requests to a login page", except views marked `login_not_required()`. | Rule, tool_gate |
| https://docs.spring.io/spring-security/reference/servlet/authorization/authorize-http-requests.html | Spring | n.d. | Examples end with `.anyRequest().authenticated()`. | Rule, tool_gate |

Overlap: `svc-authz-central-deny-default` (CWE-862, 863) denies a request no policy allows. This card is about the anonymous caller.

## svc-csp-strict-script-src (ASVS 3.4.3)

Orgs: OWASP, Mozilla, Google (3). W3C CSP3 (https://www.w3.org/TR/CSP3/) returned 403 and was not used.

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x12-V3-Web-Frontend-Security.md | OWASP | 2025 | 3.4.3: a CSP with `object-src 'none'` and `base-uri 'none'` and either an allowlist or nonces or hashes; L3 needs nonces or hashes per response. | Rule (minimum) |
| https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html | OWASP | n.d. | Gives nonce-based and hash-based "Strict Policy" samples with `object-src 'none'` and `base-uri 'none'`. | Rule |
| https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP | Mozilla | n.d. | Recommends nonce- or hash-based fetch directives ("strict CSP"); allowlist CSPs often allow unsafe domains. | Rule, Why |
| https://web.dev/articles/strict-csp | Google | n.d. | Host-allowlist CSPs "can be bypassed in most configurations". `'unsafe-inline'` next to a nonce is a fallback that recent browsers ignore. | Rule, Why |

Tool seen: Google CSP Evaluator (https://csp-evaluator.withgoogle.com/), which checks a policy for bypasses. The Rule is stricter than the ASVS 3.4.3 minimum, which still allows a host allowlist.

## fn-no-prototype-pollution (CWE-1321, ASVS 15.3.6)

Orgs: OWASP, MITRE, PortSwigger, GitHub, Snyk (5).

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md | OWASP | 2025 | 15.3.6: prevent prototype pollution, for example with `Set()` or `Map()` over object literals. | Rule |
| https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html | OWASP | n.d. | Use `new Set()` or `new Map()`; use `freeze` and `seal`. | Rule, Counterpoint |
| https://cwe.mitre.org/data/definitions/1321.html | MITRE | n.d. | Mitigations: `Object.create(null)`, `Map`, freezing the prototype, blocking `__proto__` and `prototype`, schema validation. | Rule, Counterpoint |
| https://portswigger.net/web-security/prototype-pollution/preventing | PortSwigger | n.d. | Sanitize property keys before merging; an allowlist of keys is the most effective way. | Rule |
| https://codeql.github.com/codeql-query-help/javascript/js-prototype-pollution-utility/ | GitHub | n.d. | Guard in the recursive copy: merge only own properties, or block `__proto__` and `constructor`. Query `js/prototype-pollution-utility`; `js/prototype-polluting-assignment` at https://codeql.github.com/codeql-query-help/javascript/js-prototype-polluting-assignment/. | Rule, tool_gate |
| https://learn.snyk.io/lesson/prototype-pollution/ | Snyk | n.d. | Solutions: `Object.create(null)` and `Object.freeze(Object.prototype)`. | Rule, Counterpoint |

## svc-tls-modern-only (ASVS 12.1.1 and 12.1.2)

Orgs: IETF, NIST, OWASP, Microsoft (4). The Mozilla Server Side TLS wiki page (https://wiki.mozilla.org/Security/Server_Side_TLS) now says the public guide moved to a community project outside Mozilla, so it was not counted.

| URL | Org | Year | What it says | Backs |
| --- | --- | --- | --- | --- |
| https://www.rfc-editor.org/rfc/rfc8996.html | IETF | 2021 | Deprecates TLS 1.0 and 1.1: "Implementations MUST NOT negotiate TLS version 1.0". | Rule |
| https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf | NIST | 2019 | Government-only servers shall use TLS 1.2 and shall not use TLS 1.0, SSL 3.0, or SSL 2.0. Public-facing servers may enable 1.0 and 1.1 "when necessary". | Rule, Counterpoint |
| https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html | OWASP | n.d. | Default to TLS 1.3, allow 1.2; disable TLS 1.0 and 1.1 and SSL; prefer AEAD suites. ASVS 12.1.1 and 12.1.2 (https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x21-V12-Secure-Communication.md) say the same. | Rule, Why |
| https://learn.microsoft.com/en-us/security/engineering/solving-tls1-problem | Microsoft | n.d. | A guide to migrating to a "TLS 1.2+ network environment" and removing TLS 1.0. | Rule |

Tool seen: testssl.sh (https://testssl.sh/) checks the protocols a server offers.

## Gaps skipped

- MFA and account recovery (ASVS 6.4, chapters 6 and 7): the requirements span reset tokens, enrolment, and factor rules, with no single Rule that can fail on a diff. `svc-auth-throttle-generic-errors` already names password reset and one-time codes in `applies_when` and keeps the recovery flow reachable in its Counterpoint.
- Memory safety in C, C++, and unsafe Rust (CWE-787, 125, 416): a card needs `lang:` and a `packs/<lang>/` pack, and no such pack exists. The rule would differ per language.

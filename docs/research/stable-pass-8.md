# Stable pass 8: the eleven unreviewed drafts

Checked 2026-10-25 against `docs/PROMOTION.md`. Each `borrowed_from` URL was fetched with `curl -sL -A "Mozilla/5.0"`. The text was saved to `~/dev/gcr-sweep/stable8/` and searched with `rg`. All 48 URLs returned the full page, with no JavaScript shell and no challenge page. Quotes are page text of 15 words or fewer.

A CWE entry counts as MITRE's own practice only when its Potential Mitigations section recommends the practice, as in pass 1 for `sys-secrets-and-errors`.

## Promoted

| Card | Rule clause | Organisations | Quote or evidence |
| --- | --- | --- | --- |
| svc-tls-modern-only | Only TLS 1.2 and 1.3 on servers | IETF, OWASP, Microsoft | RFC 8996: "MUST NOT negotiate TLS version 1.1". OWASP: "TLS 1.0 and TLS 1.1 ... must be disabled". Microsoft: "removing TLS 1.0 dependencies", and says TLS 1.0 includes 1.1 |
| svc-no-secrets-in-url | Sensitive values in a header or the body, never the URL | OWASP, IETF, MITRE, Mozilla | ASVS 14.2.1. RFC 6750: "Bearer tokens SHOULD NOT be passed in page URLs". CWE-598: "only include it in the request body or request headers". MDN: "use POST rather than GET wherever possible" |
| svc-csp-strict-script-src | Nonce or hash `script-src`, `object-src 'none'`, `base-uri 'none'` | OWASP (ASVS 3.4.3), Mozilla, Google | ASVS L3: "a per-response policy with nonces or hashes must be defined". MDN: "recommended practice is to use nonce- or hash- based fetch directives". web.dev: allowlists "can be bypassed in most configurations" |
| fn-xml-no-external-entities | External entity resolution off | OWASP, MITRE, PortSwigger, GitHub | OWASP: "disable external entity resolution and external DTD loading". CWE-611: "configured to disable external entity expansion". PortSwigger: "the easiest and most effective way". CodeQL: "disable external entity handling" |
| fn-no-eval-untrusted | `eval`, `exec`, `new Function` | OWASP, MITRE, Mozilla, GitHub | ASVS 1.3.2: "avoids the use of eval()". CWE-94: "do not have to dynamically generate code". MDN: "Never use direct eval()!". CodeQL `py/code-injection`: "Avoid including user input in any expression" |
| fn-no-eval-untrusted | Template compiler | OWASP, PortSwigger, GitHub | ASVS 1.3.7: "not allowing templates to be built based on untrusted input". PortSwigger: "not allow any users to modify or submit new templates". CodeQL `py/template-injection`: "an untrusted value is not used to directly construct a template" |
| fn-redirect-target-allowlist | Local path or allowlisted host only | OWASP, Microsoft, PortSwigger, GitHub | OWASP: "short name, ID or token which is mapped server-side". Microsoft: `LocalRedirect` "throws an exception if a non-local URL is specified". PortSwigger: "Maintain a server-side list of all URLs". CodeQL: "maintain a list of authorized redirects on the server" |
| fn-no-prototype-pollution | No untrusted key on a plain object; use `Map`, `Object.create(null)`, or an allowlist | OWASP, MITRE, PortSwigger, Snyk | ASVS 15.3.6: "using Set() or Map() instead of object literals". CWE-1321 lists `Object.create(null)` and `Map`. PortSwigger: "allowlist of permitted keys is the most effective". Snyk: "Create objects without prototypes" |
| fn-disclosure-hides-only-secondary | Do not hide what most users need behind a closed disclosure | NN/g, GOV.UK, Appian | Quotes confirmed again from review t39 |
| fn-related-controls-in-fieldset | Radio, checkbox, and multi-part groups in a `fieldset` with a `legend` | GOV.UK, W3C, USWDS, A11y Project | USWDS: "Group each set of thematically related controls in a fieldset". GOV.UK now reads "The first element inside a fieldset must be a legend" |
| fn-label-above-field | Label directly above a text input, select, or textarea | GOV.UK, Atlassian, NN/g | W3C names "left or directly above" as equal conventions, so it is not counted for this clause |

New source: https://codeql.github.com/codeql-query-help/python/py-template-injection/ (GitHub). It was fetched and confirmed, and it makes the third organisation behind the template clause of `fn-no-eval-untrusted`.

## Clauses moved out of the Rule

- svc-tls-modern-only: "set that minimum in the config instead of relying on the default" had no backer. Microsoft says the opposite: "remove the hardcoded protocol version selection and defer to the operating system default". The clause was dropped.
- fn-xml-no-external-entities: DTDs off has OWASP only, and network access off has no backer. Both moved to Why.
- fn-no-eval-untrusted: expression languages have ASVS (SpEL) and only a generic CWE-94 line. They moved to Why, and `applies_when` no longer lists them.
- fn-no-prototype-pollution: blocking `__proto__`, `constructor`, and `prototype` in a deep merge has GitHub and MITRE. PortSwigger calls a blocklist "a stopgap", and Snyk says to use a library instead. The clause moved to Why as a stopgap.
- fn-related-controls-in-fieldset: only GOV.UK says the legend comes first. That moved to Why.
- fn-label-above-field: "no link, button, or other field between them" has Atlassian ("directly above") and NN/g ("immediately above") only. It moved to Why, and the postcode-link lines left the FAIL.

## Kept draft: svc-authn-by-default

Microsoft and Spring give the reason. Microsoft says required by default "is more secure than relying on new controllers". Spring says "Denying the request by default is a healthy security practice". Three frameworks document the same default with no reason, so under rule 3 they do not count:

- Django: https://docs.djangoproject.com/en/5.2/releases/5.1/ ("Middleware to require authentication by default")
- Rails: https://guides.rubyonrails.org/getting_started.html ("will restrict all pages to authenticated users only")
- NestJS: https://raw.githubusercontent.com/nestjs/docs.nestjs.com/master/content/security/authentication.md ("every route requires a signed-in user"). docs.nestjs.com returns a JavaScript shell.

CWE-306 asks for "a centralized authentication capability" but says nothing about a default. A Django or Rails page that says why the default is safer would make the third organisation.

## Tool gates

Every named rule exists on its page: Bandit B307, B102, and B313 to B319. Bandit B405 to B409 exist, and B410 (`import_lxml`) is marked removed, so the XXE card now names B405 to B409. Also confirmed: CodeQL `py/code-injection`, `py/template-injection`, `py/url-redirection`, `py/xxe`, `js/prototype-pollution-utility`, and `js/prototype-polluting-assignment`, ESLint `no-eval` and `no-implied-eval`, ASP.NET `LocalRedirect` and `IsLocalUrl`, testssl.sh, and Google CSP Evaluator.

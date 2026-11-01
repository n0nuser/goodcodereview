# New cards: comments, doc references, vulnerable dependencies, release gating, front-end JS

Quotes were read on the live pages on 2026-11-01 (fetched with curl and stripped to text).

## fn-comments-survive-context (draft, lacks orgs)

Clause: a TODO or comment must not depend on the present moment; give a future-dated TODO a date or event.

- Google, https://google.github.io/styleguide/cppguide.html: "If your TODO is of the form “At a future date do something” make sure that you either include a very specific date (“Fix by November 2005”) or a very specific event (“Remove this code when all clients can handle XML responses.”)."
- Google, https://google.github.io/styleguide/pyguide.html: "make sure that you either include a very specific date (“Fix by November 2009”) or a very specific event (“Remove this code when all clients can handle XML responses.”) that future code maintainers will comprehend."
- Google, https://google.github.io/styleguide/javaguide.html: "A TODO comment begins with the word TODO in all caps, a following colon, and a link to a resource that contains the context, ideally a bug reference."
- Contradiction found: Google asks for a bug reference in the TODO, so the old Rule ("no ticket ids") was wrong. The card now allows ticket ids.
- Only Google states the time-bound clause. Kubernetes (https://www.kubernetes.dev/docs/guide/pull-requests/): "If you think there’s something pretty obvious that we could follow up on, add a TODO." It says nothing on dates or events. Chromium, LLVM, Mozilla, Linux kernel, WebKit, Dart and AOSP guides have no such text. Two more orgs are still missing.

## Stale or false comments: folded into an existing stable card, no new card

- Python Software Foundation, https://peps.python.org/pep-0008/: "Comments that contradict the code are worse than no comments. Always make a priority of keeping the comments up-to-date when the code changes!"
- fn-comments-explain-why already fails "a comment that states something false", with PEP 8 in its sources. Not duplicated.

## code-docs-refs-resolve (stable): link and path references in docs resolve, checked in CI

- GitHub, https://github.com/github/docs/blob/main/src/links/README.md: automation table lists "`link-check-on-pr.yml` | Every pull request" and "`link-check-internal.yml` | Mondays, 16:20 UTC". Backs: check runs in CI on every change.
- GitLab, https://docs.gitlab.com/development/documentation/testing/links/: "Relative links between documentation files, we use Lychee." and "Run `lychee --offline --include-fragments <doc_directory>`". Also https://docs.gitlab.com/development/documentation/testing/: "To check for broken links, merge requests containing changes to Markdown ( .md ) files run these jobs in their pipelines". Backs: relative links and anchors, on merge requests.
- Rust project, https://github.com/rust-lang/rustc-dev-guide/blob/master/.github/workflows/ci.yml: env "MDBOOK_LINKCHECK2_VERSION: 0.13.0", "MDBOOK_OUTPUT__LINKCHECK__FOLLOW_WEB_LINKS: ${{ github.event_name != 'pull_request' }}" and "# linkcheck needs the base commit." Backs: link check on pull requests, external links only off the pull-request path.
- Django (not counted: a manual procedure, not a CI practice): https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/: "Links in documentation can become broken or changed such that they are no longer the canonical link." It describes a manual `make linkcheck`.
- Google SWE book, https://abseil.io/resources/swe-book/html/ch10.html: "Over time, documents become stale, obsolete, or (often) abandoned." (context for the Why only).
- Not covered by these sources: commands cited in docs (stays in draft code-documented-setup-runs). File paths in code comments have no source; the card says "link, file path and anchor" cited in docs, and the link checkers cover relative file paths.

## code-vuln-remediation-window (stable): fix known-vulnerable dependencies inside a stated window

- OpenSSF, https://www.bestpractices.dev/en/criteria/0: "There MUST be no unpatched vulnerabilities of medium or higher severity that have been publicly known for more than 60 days." and "Projects SHOULD fix all critical vulnerabilities rapidly after they are reported."
- OpenSSF Scorecard, https://github.com/ossf/scorecard/blob/main/docs/checks.md: "This check determines whether the project has open, unfixed vulnerabilities in its own codebase or its dependencies using the OSV (Open Source Vulnerabilities) service. An open vulnerability is readily exploited by attackers and should be fixed as soon as possible." (same organisation, counts once).
- CISA, https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities: "Remediate each vulnerability according to the timelines set forth in the CISA-managed vulnerability catalog. The catalog will list exploited vulnerabilities ... with the requirement to remediate within 6 months for vulnerabilities with a Common Vulnerabilities and Exposures (CVE) ID assigned prior to 2021 and within two weeks for all other vulnerabilities."
- GitHub, https://docs.github.com/en/code-security/securing-your-organization/understanding-your-organizations-exposure-to-vulnerabilities/prioritizing-dependabot-alerts-using-metrics: "Establish Service Level Agreements (SLAs) for resolving vulnerabilities based on severity." and "Document decisions to provide transparency and support future prioritization."
- OWASP, https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html: "it's possible to decide to accept the risk represented by the security issue. However, this decision must be taken by the Chief Risk Officer (fallback possible to Chief Information Security Officer )".
- Clause "stated window per severity, fix inside it": OpenSSF, CISA, GitHub (three). Clause "record accepted risk": GitHub and OWASP only (two), so it sits in the Why, not in the Rule.
- Weak: CISA's directive binds US federal agencies and the exploited-vulnerability catalog, so it is a narrow instance of the practice. Its page also says CISA grants no waivers, which is why the accepted-risk text is not drawn from it.

## code-release-gated-on-ci (draft, lacks evidence)

- Kubernetes, https://github.com/kubernetes/sig-release/blob/master/release-blocking-jobs.md: "Jobs on the Blocking dashboard for a particular release should block that release if they do not have at least three successive "green" runs at go/nogo decision time." and "the general expectation is "jobs red, do not release.""  (a practice)
- GitHub, https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-jobs: "job1 must complete successfully before job2 begins" (feature description).
- GitHub, https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets: "Required status checks ensure that all required CI tests are passing before collaborators can make changes to a branch or tag targeted by your ruleset." (feature description)
- GitLab, https://docs.gitlab.com/ci/pipelines/: "later stages could have jobs that test and deploy code. If all jobs in a stage succeed, the pipeline moves on to the next stage." (feature description)
- Why draft: only Kubernetes states the practice for releases. GitHub and GitLab pages describe what the feature does. SLSA, Scorecard and Go/Rust release docs had no gating statement.
- Overlap check: code-ci-gates is "before merge"; code-workflow-supply-chain is about pins, permissions and provenance. Neither covers a tag that triggers a publish.

## fn-handle-rejected-promises (stable)

- Mozilla, https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises: "you can attach it to the end of the chain: ... .catch(failureCallback);" and "If a promise rejection event is not handled by any handler, it bubbles to the top of the call stack, and the host needs to surface it."
- Mozilla, https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText: "NotAllowedError DOMException Thrown if writing to the clipboard is not allowed." (the API can reject)
- Google, https://web.dev/articles/async-clipboard: "the writeText() function returns a Promise that resolves or rejects depending on whether the passed text is copied successfully" followed by an example with `try { await navigator.clipboard.writeText(...) } catch ( err ) { console.error('Failed to copy: ', err ); }`.
- typescript-eslint, https://typescript-eslint.io/rules/no-floating-promises/: "A "floating" Promise is one that is created without any code set up to handle any errors it might throw. Floating Promises can cause several issues, such as improperly sequenced operations, ignored Promise rejections, and more."
- OpenJS Foundation (Node.js), https://nodejs.org/api/cli.html, `--unhandled-rejections=mode`: "Changed default mode to throw." and "throw: Emit unhandledRejection. If this hook is not set, raise the unhandled rejection as an uncaught exception. This is the default."
- Backs: handle the rejection of each started promise (MDN, web.dev, typescript-eslint); effect on Node (Node.js). Rule is not browser-only, so no `context:`.

## fn-guard-uri-decoding (draft, lacks orgs)

- Mozilla, https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent: "URIError Thrown if encodedURI contains a % not followed by two hexadecimal digits, or if the escape sequence does not encode a valid UTF-8 character." and a "Catching errors" example with `try { const a = decodeURIComponent("%E0%A4%A"); } catch (e) { console.error(e); }`.
- OpenJS Foundation (Node.js), https://nodejs.org/api/querystring.html: "By default, the querystring.unescape() method will attempt to use the JavaScript built-in decodeURIComponent() method to decode. If that fails, a safer equivalent that does not throw on malformed URLs will be used."
- Two organisations. The WHATWG URL spec and MDN URLSearchParams describe lenient decoding but state no rule to prefer them, so they are not counted.

## fn-link-url-scheme-allowlist (draft, lacks orgs)

- OWASP, https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html: "Unvalidated URL values: React 19 blocks javascript: URLs in src and href , but this does not replace application-specific URL validation" and "Properties that accept URLs require URL validation as well."
- Google (Angular), https://angular.dev/best-practices/security: "Angular sanitizes untrusted values for HTML and URLs." and "javascript: URLs are dangerous if attacker controlled. Angular sanitizes them in data binding".
- MDN's javascript: URL page calls `href="javascript:..."` a bad practice for navigation, not for security, so it does not back this card. Existing cards fn-no-raw-html-sink (HTML sinks) and fn-redirect-target-allowlist (server redirects, mentions javascript: only for `location`) do not cover link targets from data.

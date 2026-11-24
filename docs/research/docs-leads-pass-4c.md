# Docs leads, pass 4c

Method: every page below was fetched with `curl -sL`, tags stripped with `python3 -I`, and the sentence found with `rg` in the stripped text. No summaries were used as evidence. Quotes are under 10 words. "Found" says where the sentence sits. Date of fetch: 2026-11-22. Org grouping follows docs/PROMOTION.md (Google covers Go, Chromium, web.dev, Angular, Fuchsia; Microsoft covers Learn and Azure SDK; a person's blog does not count).

## Part 1A. `code-docs-redirect-on-move`

Rule: "Add a redirect from the old URL in the same change that moves, renames or deletes a documentation page."

1. https://docs.gitlab.com/development/documentation/redirects/ . GitLab. Move, rename or delete requires a redirect: "you must add a redirect". Found: first paragraph. The same-change part is only implied: the page tells authors to assign a technical writer to "any merge request" that moves, renames or deletes a page. No literal "same MR".
2. https://developers.cloudflare.com/style-guide/how-we-docs/redirects/ . Cloudflare. "in the same pull request as the content change". Found: "How we add redirects", Workers paragraph. Also "When we add redirects": add one when you change the URL or delete the page. A bot comments on PRs that touch content paths ("Potential redirects").
3. https://learn.microsoft.com/en-us/hololens/contributing . Microsoft (Learn product docs). "If your change will rename or delete" an article, "be sure to add a redirect". Found: "Deleting or renaming an existing article" section. Same-change by wording.
4. https://learn.microsoft.com/en-us/contribute/docs-authoring/sort-redirects . Microsoft. "we're required to provide a redirect" when a file is deleted. Found: Summary. Same org as row 3: counts once.
5. https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/Advanced/Redirects.html . TYPO3 (TYPO3-Documentation, official repos). "a redirect for the old URL must be added" when a change renames or deletes a page; "Reviewers should ask for this" on any PR that omits it. Found: opening section. Same-change by wording. Not in `tools/orgs.py` as far as I know: check before use.
6. https://raw.githubusercontent.com/mdn/content/main/CONTRIBUTING.md . Mozilla (MDN). "You should always add a redirect when deleting documents." Found: "Moving documents" and the delete walk-through, inside a WARNING block. The move command "fixes up redirects automatically". The deletion steps end with "Commit all of the changes", so the redirect travels with the delete. It also says a forgotten redirect "can be done afterwards", so same-change is the preferred path, not a hard rule.
7. https://docs.github.com/en/contributing/writing-for-github-docs/configuring-redirects . GitHub. "we create a redirect" when title, version or file location changes. Found: "About redirects". No same-change wording. Backs the redirect clause only.
8. Weak, not counted: Hugo https://gohugo.io/content-management/urls/ ("essential for preventing broken links", feature page for aliases); PrestaShop https://devdocs.prestashop-project.org/9/contribute/documentation/how/moving-pages/ ("make sure URLs are preserved"); Read the Docs and Docusaurus redirect pages are tool docs only.
9. Not found: Kubernetes (content-organization, style-guide, open-a-pr, pr-wranglers have no redirect rule). Microsoft general `/contribute/content/redirection*` URLs return 404 (rows 3 and 4 were found by search instead).

Count, "add a redirect when a page moves or is deleted": GitLab, Cloudflare, Microsoft, TYPO3, Mozilla, GitHub = 6 organisations.
Count, "in the same change": Cloudflare (literal), Microsoft, TYPO3 (reviewers ask on the PR), GitLab (implied via MR) = 3 to 4. Mozilla is partial. GitHub does not count for this clause.
Verdict: reaches three on both clauses. Weakest on same-change is GitLab (implied). Microsoft and TYPO3 carry it by "If your change..." and "whenever a change...". Existing card: `code-docs-redirect-on-move` (draft, `lacks: unreviewed`). Suggested `borrowed_from` add: Microsoft hololens page, TYPO3, MDN CONTRIBUTING. The `lacks` line can go once the Rule check passes.

## Part 1B. `code-doc-examples-stay-true`

Rule: run each doc example as a test, or include it from a source file that CI builds.

Clause 1, run doc examples as tests:

1. https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html . Rust. "examples within your documentation are up to date". Found: intro, "supports executing your documentation examples as tests".
2. https://go.dev/blog/examples . Google (Go). "Examples are compiled (and optionally executed)". Found: "Examples are tests" section. Intro: examples are "verified by running them as tests".
3. https://hexdocs.pm/elixir/writing-documentation.html . Elixir. "To ensure examples do not get out of date", use doctests. Found: Doctests section; "We advise developers to include examples". Check whether `tools/orgs.py` maps hexdocs.pm / Elixir.
4. https://docs.python.org/3/library/doctest.html . Python. Use case listed: "docstrings are up-to-date" by verifying examples still work. Found: intro list. Tool page that names the practice as a use; partial.
5. https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md . Node.js. API doc code samples "will also be checked" by `make lint`. Lint, not run; partial.

Count, tested: Rust, Google, Elixir = 3 firm; Python partial; Node.js partial.

Clause 2, include examples from a source file instead of pasting:

6. https://kubernetes.io/docs/contribute/style/hugo-shortcodes/ . Kubernetes. "embed the contents of file in a code block". Found: "Source code files". Used "when the contents of the sample file is generic and reusable".
7. https://learn.microsoft.com/en-us/contribute/content/code-in-docs . Microsoft. The preferred way to include snippets is "by reference to a code file" (in-repo snippet references). Found: "In-repo snippet references". Also "Code validation": some repos "automatically compile all sample code" (the .NET repo), and authors of included code must keep it from going out of date.
8. https://devguide.python.org/documentation/markup/ . Python. Longer examples "may be included" from an external file with `literalinclude`; Found: "Showing code examples". Permissive wording; partial.
9. Spotify TechDocs (https://backstage.io/blog/2020/09/08/announcing-tech-docs): fetched; found docs-like-code in CI, but no sentence about embedding code samples. UNVERIFIED for this clause. Do not count.

Count, include from source: Kubernetes, Microsoft = 2 firm; Python partial; Spotify unverified. Needs one more clean organisation. Candidates not reached: Rust book (`{{#include}}`, same Rust org anyway), Angular (Google), Elastic (docs URLs 404).
Verdict: clause 1 reaches three. Clause 2 has two. Suggest moving clause 2 to the Why or keeping it as "or include it" only if a third is found. Existing card: `code-doc-examples-stay-true` (draft, lacks orgs).

## Part 1C. `code-dead-docs-deleted`

Rule: delete docs known to be wrong or obsolete instead of leaving or hiding them.

1. https://google.github.io/styleguide/docguide/best_practices.html . Google. "Dead docs are bad." Found: "Delete Dead Documentation": "First delete what you're certain is wrong".
2. https://google.github.io/eng-practices/review/reviewer/looking-for.html . Google. Reviewer question when a CL deletes or deprecates code: whether the docs should be deleted too. Found: "Documentation" section. Same org as row 1.
3. https://www.kernel.org/doc/html/latest/doc-guide/contributing.html . Linux kernel. "should do that anyway" about removing obsolete docs; "refer to code that was removed". Found: under "Documentation"; it also allows a warning banner when a doc cannot be fixed.
4. https://docs.gitlab.com/development/documentation/workflow/ . GitLab. "If documentation needs to be removed because it was added prematurely, delete it." Also: dropped features "leave orphaned content that clutters". Found: "Hiding documentation is problematic" list. Covers docs for features that never shipped or were dropped, not every wrong page. Partial.
5. https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Howto/Retiring_content . Mozilla (MDN). Retire a section when the "technology is deprecated or no longer relevant". Found: "When to consider retiring content". Content is archived, not lost. Section level, with a team decision; partial.
6. https://istio.io/latest/docs/releases/contribute/remove-content/ . Istio. Steps to remove a retired page: remove it, fix broken links. Found: page body. A procedure, not a statement that obsolete pages must go; partial.
7. https://fuchsia.dev/fuchsia-src/contribute/docs/deprecating-docs . Google (Fuchsia). Deprecate, wait about six months, then delete and redirect. Same org as Google.
8. https://make.wordpress.org/docs/2020/12/17/what-to-do-with-old-obsolete-documentation/ . WordPress. A proposal thread listing delete, mark or archive; commenters disagree. A plan, does not count.
9. Django (docs/internals/contributing/writing-documentation): `versionadded` and `versionchanged` notes are kept for two releases then removed. Adjacent practice (removing stale notes), not wrong pages. Not counted. Microsoft Learn: the only retire guide found is a 2016 copy on a third-party GitHub repo, and the official URLs 404. Red Hat, Atlassian, Debian, Fedora, Python devguide, Rust: nothing found.

Count, "delete docs known to be wrong or obsolete": Google, Linux kernel = 2 clean. GitLab, Mozilla, Istio partial.
Count, narrower clause "delete docs for code or features that were removed, dropped or never shipped": Google (eng-practices), Linux kernel, GitLab, plus Mozilla and Istio partial = 3 firm. Suggest rewording the Rule to the narrower clause and keeping "wrong page" in the Why. Existing card: `code-dead-docs-deleted` (draft). Risk: Linux also allows a warning banner for docs that cannot be fixed; the card's counterpoint should say so.

## Part 2. New leads (checked against `cards/` with `rg`)

Covered already, do not make cards:
- Timeless wording ("currently", "new", "now"): Google timeless page, Kubernetes "Avoid statements that will soon be out of date", GitLab word list "currently". Covered by `fn-comments-survive-context` (it cites all three).
- Heading levels: `fn-heading-structure` (HTML). Image alt text: `fn-img-alt-text`. Link-reference resolution: `code-docs-refs-resolve`. Repeated prose links: `code-docs-link-dont-duplicate`.
- Not reachable or not usable: Google `/style/command-line-syntax`, `/style/domain-names`, `/style/future-features` returned 404 (the live future page is `/style/future`). GitLab `/styleguide/text/`, `/markdown_and_lists/`, `/images/` returned 404. Microsoft `/style-guide/developer-content/code-examples-and-placeholders` 404. The Microsoft welcome page itself only links onward.

Candidate list (no existing card), with where each sentence lives:

| # | Practice | Org and URL | Found |
|---|---|---|---|
| a | Link text says where the link goes, not "here" | Google https://developers.google.com/style/link-text | "use clear and descriptive link text", linking summary |
| b | Do not put links in headings | Google https://developers.google.com/style/headings | "Don't put links in headings." |
| c | Docs do not announce or promise unreleased features | Google https://developers.google.com/style/future | opening: "Avoid documenting future features" |
| d | Doc examples use reserved example domains, no real names or PII | Google https://developers.google.com/style/examples | "Don't use real domain names" |
| e | Security warnings gathered in one section, not repeated per function | Python https://devguide.python.org/documentation/style-guide/ | "Security considerations" section; one org |
| f | No author byline on new docs | Python style guide, "Author attribution"; one org | |
| g | Link to an issue by number in the link text | GitLab https://docs.gitlab.com/development/documentation/styleguide/links/ | "Links to issues"; one org |
| h | Do not document a feature users cannot reach yet | GitLab workflow page | "no documentation should be included" for inaccessible components; one org |
| i | Interactive examples: no trailing prompt, copy-friendly | Python style guide, "Code examples"; one org | |

Top three, searched for more organisations:

### 1. Descriptive link text (a)

Proposed id: `code-docs-link-text-says-where`. A reviewer can FAIL a diff that adds `[here](...)` or `[this page](...)` to docs or a README.

1. https://developers.google.com/style/link-text . Google. "clear and descriptive link text". Found: summary paragraph at the top. Also the highlights page: "Use descriptive link text".
2. https://docs.gitlab.com/development/documentation/styleguide/links/ . GitLab. "Descriptive text rather than here". Found: "Text for links"; Don't examples `[here]` and `[this page]`.
3. https://learn.microsoft.com/en-us/style-guide/urls-web-addresses . Microsoft. "rather than a generic phrase like click here". Found: link text paragraph.
4. https://kubernetes.io/docs/contribute/style/style-guide/ . Kubernetes. Don't row: ambiguous terms such as "click here". Found: "Links" Do and Don't table.
5. https://www.w3.org/WAI/WCAG22/Techniques/general/G91 . W3C. "describe the purpose of a link in the text". Found: "About this Technique" objective. Technique page, not a requirement; partial.
6. GitHub style guide https://docs.github.com/en/contributing/writing-for-github-docs/style-guide fetched: no link-text sentence found. Not counted.

Count: Google, GitLab, Microsoft, Kubernetes = 4 firm, W3C partial. Strongest lead of the pass. Overlap check: `fn-native-button-or-link` is about HTML elements, not link wording.

### 2. Do not announce future features in docs (c)

Proposed id: `code-docs-no-future-promises`. FAIL on a diff that adds "support is planned" or "coming soon" to published docs. Some overlap with `fn-comments-survive-context` ("promises future work"), which is about comments and TODOs; keep this card on published docs and name the split in the PR.

1. https://developers.google.com/style/future . Google. "Avoid documenting future features or products". Found: opening paragraph. Highlights page: "Don't pre-announce anything in documentation."
2. https://kubernetes.io/docs/contribute/style/style-guide/ . Kubernetes. "Avoid making promises or giving hints" about the future. Found: "Avoid statements about the future". Exception: announced deprecations. Alpha features go under an alpha heading.
3. https://docs.gitlab.com/development/documentation/styleguide/ . GitLab. "Do not promise to deliver features" in a future release. Found: "Promising features in future versions". Exception: say an issue exists.

Count: Google, Kubernetes, GitLab = 3. Meets the bar, with exceptions for deprecations, alpha, and "an issue exists". Microsoft not searched.

### 3. No links in headings (b)

Proposed id: `code-docs-no-links-in-headings`. FAIL on a diff that wraps a heading in a link. Low severity.

1. https://developers.google.com/style/headings . Google. "Don't put links in headings." Found: Formatting and code.
2. https://docs.gitlab.com/development/documentation/styleguide/links/ . GitLab. "Do not use links in headings." Found: link rules list; reason given: headings with links cause errors.
3. https://devguide.python.org/documentation/style-guide/ . Python. "Do not use links in section headers." Found: "Links" section.

Count: Google, GitLab, Python = 3. Checkable but minor; may merge with card 1 as one card on link hygiene only if a reviewer would not call that two rules (rule 8 and "one practice per card").

Runner-up: (d) reserved example domains: Google plus the IETF standard https://www.rfc-editor.org/rfc/rfc2606 ("reserved for ... examples in documentation") = 2. Microsoft, GitLab, Kubernetes fetched, no sentence found. Needs one more.

## Unreachable or unverified

- Microsoft Learn `/contribute/content/redirection`, `/redirects`, `/redirect-articles`, `/rename-move-delete`, `/how-to-write-redirect`, `/move-and-rename-articles`, `/content-health`: 404.
- Stripe docs-style, Rust `src/doc/README.md`, GitBook redirects, HashiCorp redirect page, Elastic docs code-samples page, Docker formatting page, Atlassian knowledge-sharing page, Google SRE workbook team-management, MDN Deleting pages and Deprecation process pages, hacks.mozilla.org MDN revamp (403): 404 or 403.
- Spotify embedding claim: not found in raw text. Cloudflare and GitHub sentences were read here (rows 1A.2 and 1A.7).
- Not checked at all: Swift, Django doctest policy, Node.js deprecations page, Elastic.
- Python doctest and Node.js `make lint` rows describe a tool or a check, so they are partial evidence.

## Parent verification and outcome (2026-11-22)

Re-fetched raw and matched the sentence for every row counted below. New stable cards: `code-readme-per-module` (Google, Azure SDK, HashiCorp), `fn-doc-params-match-signature` (Drupal, Microsoft, Python), `code-docs-link-text-descriptive` (Google, GitLab, Microsoft, Kubernetes), `code-docs-no-future-promises` (Google, Kubernetes, GitLab). Promoted: `code-docs-redirect-on-move` (redirect clause six organisations, same-change clause Cloudflare, Microsoft, TYPO3); `code-doc-examples-stay-true` trimmed to the run-as-test clause (Rust, Go, Elixir; embedding has two, in the Why); `code-dead-docs-deleted` narrowed to docs of removed or never-shipped code (Google, kernel, GitLab). The no-restating-doc-comment lead (Flink, Google, kernel, Python) went to `fn-comments-explain-why` as a source, since the Rule is the same.

`fn-comments-stay-short` stays a draft and is now `lacks: contradiction`: only GitLab and Home Assistant set a length limit, Go says there is no fixed length, and CockroachDB values long comments (pass 4b). Left as leads: troubleshooting doc per library (Azure SDK), runtime-built identifiers (MediaWiki), orphan files (Kubernetes, Cloudflare images), dated docs (Microsoft, GitLab, Grafana, Cloudflare), no links in headings (Google, GitLab, Python; minor).

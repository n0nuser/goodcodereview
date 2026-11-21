# Docs and comments practices: org sources

Fetched 2026-11-21 with WebFetch and read as page text. Paraphrase only. Each row gives the URL, the org, a one-sentence paraphrase, and which practice it backs: (1) docs and comments change in the same change as the code, reviewers check; (2) delete wrong or obsolete docs; (3) keep code comments short, long explanation goes to docs with a link; (4) minimum viable docs, a README per directory, link to an existing guide instead of duplicating.

1. https://google.github.io/styleguide/docguide/best_practices.html. Google. Change docs in the same change list as the code, and reviewers can insist that docstrings, headers, and READMEs are updated with it. Backs 1.
2. https://google.github.io/styleguide/docguide/best_practices.html. Google. Stale docs mislead, so remove what is clearly wrong and default to deleting, since removed docs can be restored. Backs 2.
3. https://google.github.io/styleguide/docguide/best_practices.html. Google. Keep a small set of current, accurate docs, trimmed often, rather than a large neglected pile; link to the existing guide for a common technology instead of writing your own. Backs 4.
4. https://google.github.io/styleguide/docguide/READMEs.html. Google. Every top-level directory of a code package should have an up-to-date README that at least links to the fuller docs. Backs 4.
5. https://google.github.io/eng-practices/review/reviewer/looking-for.html. Google. When a change alters how users build, test, or release code, the reviewer checks that READMEs and reference docs are updated; when it deletes or deprecates code, the reviewer considers deleting the docs too. Backs 1, 2.
6. https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md. Chromium. Docs go in the same change as the related code so reviewers see both and docs stay current. Backs 1.
7. https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md. Chromium. Outdated or misleading docs should be removed, defaulting to delete when unsure. Backs 2.
8. https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md. Chromium. Keep each doc short, maintain few current docs, give each directory a README, and link to an existing guide instead of writing a new one. Backs 4.
9. https://docs.zephyrproject.org/latest/contribute/contributor_expectations.html. Zephyr Project. A PR that changes functionality must also update the docs the change affects. Backs 1.
10. https://devguide.python.org/getting-started/pull-request-lifecycle/. Python. A good PR includes doc changes, and the patchcheck checklist asks whether the docs were updated; not stated as a rejection rule. Backs 1.
11. https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/. Django. A patch that adds or changes a feature should contain its documentation, and the checklist asks for it. Backs 1.
12. https://github.com/nodejs/node/blob/main/doc/contributing/pull-requests.md. Node.js. When a PR adds or deprecates an API, the matching doc entry is added or updated in that same PR; other changes are not covered. Backs 1 (API changes only).
13. https://docs.gitlab.com/development/documentation/workflow/. GitLab. Docs added too early should be deleted, not hidden in HTML comments, because hidden docs go stale; same-MR docs are encouraged but not mandatory. Backs 2, weakly 1.
14. https://docs.gitlab.com/development/documentation/styleguide/. GitLab. If the docs already answer a question, share the link instead of rephrasing it. Backs 4.
15. https://go.dev/doc/comment. Go. Doc comments stay short and caller-focused, algorithm detail lives in ordinary comments inside the function body, and cross-references use doc links instead of restating. Backs 3.
16. https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide. Mozilla (MDN). Prefer concise pages, and cross-reference existing MDN content instead of repeating it. Backs 4.

Not counted: Microsoft engineering playbook (https://microsoft.github.io/code-with-engineering-playbook/documentation/) names docs not updated with code and stale design docs as problems but states no practice. Linux kernel coding-style (https://docs.kernel.org/process/coding-style.html) says explain what, not how, and avoid comments inside function bodies, but sets no length rule and gives no link-to-docs rule. Google eng-practices says comments explain why, which is not a length rule. Kubernetes PR guide, Rust rustc-dev-guide contributing page, Rust std-dev-guide writing page, Angular CONTRIBUTING.md, kernel submitting-patches, and Firefox contributing_code were read and state none of the four.

Not reached: Microsoft code-review author-guidelines URL (404), Grafana code style guide URL (404), Kubernetes style guide (only first 100,000 of 127,857 characters read). Not tried: Spotify, Stripe, Atlassian, Cloudflare, Shopify, Apache project guides, Mozilla firefox-source-docs beyond one page.

Count 1 (docs and comments change with the code): Google, Chromium, Zephyr, Python, Django, Node.js (API changes only) = 6 orgs; GitLab weakly, as encouraged not required.
Count 2 (delete wrong or obsolete docs): Google, Chromium, GitLab = 3 orgs. No page found on archiving implemented design docs; Chromium only says pre-implementation design material lives in shared Drive folders.
Count 3 (short comments, long explanation to linked docs): Go = 1 org. Kernel and Google fall short of the claim.
Count 4 (minimum viable docs, README per directory, link instead of duplicating): Google, Chromium, GitLab (link only), Mozilla MDN (link and concise only) = 4 orgs; README per directory and minimum viable docs are Google and Chromium only.

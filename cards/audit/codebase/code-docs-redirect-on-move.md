---
id: code-docs-redirect-on-move
level: codebase
tags: [maintainability, docs, usability]
severity: discuss
status: stable
note: Redirect on move or delete: GitLab, Cloudflare, Microsoft, TYPO3, MDN and GitHub. In the same change: Cloudflare, Microsoft and TYPO3 (reviewers ask for it). GitLab implies it through merge requests; MDN allows adding it later
lang: core
applies_when: A diff renames, moves or deletes a published documentation page.
tool_gate: A redirect-file check in CI that fails when a page is removed and no redirect names it.
borrowed_from:
  - https://docs.gitlab.com/development/documentation/redirects/
  - https://developers.cloudflare.com/style-guide/how-we-docs/redirects/
  - https://docs.github.com/en/contributing/writing-for-github-docs/configuring-redirects
  - https://learn.microsoft.com/en-us/hololens/contributing
  - https://docs.typo3.org/m/typo3/docs-how-to-document/main/en-us/Advanced/Redirects.html
  - https://raw.githubusercontent.com/mdn/content/main/CONTRIBUTING.md
---

**Rule.** Add a redirect from the old URL in the same change that moves, renames or deletes a documentation page.

**Why.** Links in issues, search results and other docs keep pointing at the old address. Without a redirect they land on a 404, and the broken links are found one reader at a time.

**FAIL**

```text
Diff: git mv docs/deploy.md docs/ops/deploy.md   (no redirect entry)
```

**PASS**

```text
Diff: git mv docs/deploy.md docs/ops/deploy.md
      redirects.yml: /docs/deploy -> /docs/ops/deploy
```

**Counterpoint.** "Internal docs have few outside links." Then the redirect is a one-line file. Skip it only for a page that was never published.

---
id: code-docs-link-text-descriptive
level: codebase
tags: [accessibility, docs, usability]
severity: discuss
status: stable
lang: core
applies_when: A diff adds or edits a link in documentation, a README or a user-facing message.
tool_gate: markdownlint `MD059` (descriptive link text) or a regex for "here" and "click here" link text.
note: Google, GitLab, Microsoft and Kubernetes state it in their docs style guides
borrowed_from:
  - https://developers.google.com/style/link-text
  - https://docs.gitlab.com/development/documentation/styleguide/links/
  - https://learn.microsoft.com/en-us/style-guide/urls-web-addresses
  - https://kubernetes.io/docs/contribute/style/style-guide/
---

**Rule.** Write link text that says where the link goes, never "here", "this page" or "click here".

**Why.** Readers scan links on their own, and screen readers list them out of context. "Here" tells neither what they will find.

**FAIL**

```text
For the deploy steps, click [here](docs/deploy.md).
```

**PASS**

```text
Follow the [deploy steps](docs/deploy.md).
```

**Counterpoint.** "Short link text reads better." The descriptive phrase is usually the words already in the sentence, so it costs no length.

---
id: code-docs-no-future-promises
level: codebase
tags: [maintainability, docs]
severity: discuss
status: stable
lang: core
applies_when: A diff adds text to published documentation that describes a feature, release or date that is not shipped.
tool_gate: none
note: Google, Kubernetes and GitLab state it. Comments and TODOs fall under `fn-comments-survive-context`; this card covers published docs
borrowed_from:
  - https://developers.google.com/style/future
  - https://kubernetes.io/docs/contribute/style/style-guide/
  - https://docs.gitlab.com/development/documentation/styleguide/
---

**Rule.** Do not promise unreleased features, versions or dates in published docs.

**Why.** A promise in the docs reads as a commitment. When the plan changes, the page is wrong, readers have planned around it, and nobody owns the fix.

**FAIL**

```text
Bulk export will arrive in the next release.
```

**PASS**

```text
Bulk export is not supported. Track the request in issue #482.
```

**Counterpoint.** "Users want a roadmap." Keep one, outside the reference docs. Link the issue, which says what is planned without a date.

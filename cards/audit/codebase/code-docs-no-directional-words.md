---
id: code-docs-no-directional-words
level: codebase
tags: [accessibility, docs]
severity: discuss
status: stable
lang: core
applies_when: A diff adds documentation text that points to other content or to something on screen.
tool_gate: A Vale rule (`Google.WordList`, `Microsoft.Avoid`) or a regex for "above", "below", "left" and "right" in docs.
note: Google, Microsoft, Mozilla (MDN), GitLab, Elastic and Red Hat state it. Docker only maps the words in a table
borrowed_from:
  - https://developers.google.com/style/word-list
  - https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/b/below
  - https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide
  - https://docs.gitlab.com/development/documentation/styleguide/word_list/
  - https://www.elastic.co/docs/contribute-docs/style-guide/
  - https://redhat-documentation.github.io/supplementary-style-guide/
---

**Rule.** Do not point to content with "above", "below", "left" or "right"; name it or link to it.

**Why.** A screen reader gives those words no meaning, and the page reflows on a phone. A reorder of the page also turns "the table below" into a false pointer.

**FAIL**

```text
See the example above, and the options in the table below.
```

**PASS**

```text
See [the retry example](#retry-example) and [the options table](#options).
```

**Counterpoint.** "Readers understand 'below'." Most do, until the section moves. A link survives a reorder, and "the following" works where a link is too heavy.

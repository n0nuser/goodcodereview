---
id: fn-img-alt-text
level: function
tags: [accessibility, frontend, html]
severity: should-fix
status: stable
lang: core
applies_when: Markup or a component renders an image, an icon, or a chart.
tool_gate: ESLint `jsx-a11y/alt-text` and axe `image-alt` catch a missing `alt`. Only a person can judge whether the text is accurate.
note: 5 orgs back the rule; no tool can check that the text is right
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
  - https://dequeuniversity.com/rules/axe/html/4.10/image-alt
  - https://www.a11yproject.com/checklist/
  - https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
---

**Rule.** Give every `<img>` an `alt` attribute: text that serves the image's purpose, or `alt=""` when the image is decorative.

**Why.** A screen reader has nothing to say about an image with no `alt`, and often reads the file name instead. An informative image with an empty `alt` hides its content. A decorative image with a long `alt` adds noise to every page view.

**FAIL**

```html
<img src="/img/IMG_0042.jpg">
<img src="/img/chart.png" alt="chart">
<img src="/img/divider.png" alt="divider line">
<button><img src="/img/trash.svg"></button>
```

**PASS**

```html
<img src="/img/q3-revenue.png" alt="Revenue grew from 4.1 to 5.3 million in Q3">
<img src="/img/divider.png" alt="">
<button><img src="/img/trash.svg" alt="Delete draft"></button>
```

**Counterpoint.** "A linter already checks `alt`." It checks that the attribute exists, not that the text fits the image or the context. Review the text itself. For a chart, give a short `alt` plus the data nearby as text.

---
id: fn-heading-structure
level: function
tags: [accessibility, usability, frontend, html]
severity: should-fix
status: stable
lang: core
applies_when: Markup or a component renders a title or a section heading.
tool_gate: axe `p-as-heading` (experimental) flags a bold paragraph styled as a heading; axe `heading-order` flags skipped levels.
note: 3 orgs (W3C, Mozilla, A11y Project) for real heading elements. No skipped levels has 2 (W3C, A11y Project), so it is in Why. The one-`h1`-per-page rule is the A11y Project's alone, so this card does not require it
borrowed_from:
  - https://www.w3.org/WAI/tutorials/page-structure/headings/
  - https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
  - https://www.a11yproject.com/checklist/
---

**Rule.** Mark every heading with a real `<h1>` to `<h6>` element, not a styled `div`, `span`, or `p`.

**Why.** Screen-reader users jump from heading to heading to scan a page. A `div` styled as a heading is invisible to that. Pick the level from the outline, not from the size you want: a skipped level, such as `h2` to `h4`, makes the outline look as if a section is missing.

**FAIL**

```html
<div class="title-large">Account</div>
<p><b>Billing</b></p>
<span class="bold">Invoices</span>
```

**PASS**

```html
<h1>Account</h1>
<h2>Billing</h2>
<h3>Invoices</h3>
<!-- size comes from CSS: h2 { font-size: 1rem } -->
```

**Counterpoint.** "The design needs a small `h2`." That is a CSS problem. Keep the level that matches the outline and set the size in the stylesheet. Jumping back up a level, such as `h4` to `h2`, is fine when a section ends.

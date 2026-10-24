---
id: svc-reflow-and-zoom
level: service
tags: [accessibility, usability, frontend, css, responsive]
severity: should-fix
status: stable
lang: core
applies_when: A page or app is served to browsers on screens of any size.
tool_gate: axe `meta-viewport`; a rendered check at a 320 px viewport and at 200% text zoom.
note: 3 orgs (W3C, Deque, A11y Project). The A11y Project checklist asks for zoom left on, text at 200%, and no horizontal scrolling
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/reflow.html
  - https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html
  - https://dequeuniversity.com/rules/axe/html/4.10/meta-viewport
  - https://www.w3.org/WAI/test-evaluate/preliminary/
  - https://www.a11yproject.com/checklist/
---

**Rule.** Make the page usable at 320 CSS pixels wide and at 200% text zoom, with no sideways scrolling, no clipped content, and no blocked pinch-zoom.

**Why.** Low-vision users enlarge the page instead of using a small screen. A fixed width or a clipped container hides content from exactly those users. `user-scalable=no` takes away their only tool.

**FAIL**

```html
<meta name="viewport" content="width=device-width, user-scalable=no, maximum-scale=1">
```

```css
.layout { width: 960px; }
.card   { height: 120px; overflow: hidden; }
```

**PASS**

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

```css
.layout { max-width: 60rem; padding-inline: 1rem; }
.card   { min-height: 7.5rem; }
.table-wrap { overflow-x: auto; }   /* a data table scrolls in its own box */
```

**Counterpoint.** "Maps and data tables need two-way scrolling." They are exempt, but only the part that needs it. Wrap the table in its own scroll box, and keep the headings and controls around it reflowing.

---
id: fn-no-positive-tabindex
level: function
tags: [accessibility, usability, frontend, keyboard]
severity: should-fix
status: stable
lang: core
applies_when: Markup sets `tabindex`, or a layout reorders content with CSS.
tool_gate: ESLint `jsx-a11y/tabindex-no-positive`; axe `tabindex`.
note: 4 orgs (W3C, Google, WebAIM, A11y Project); both tool-gate rule names checked against the jsx-a11y README and the axe rule list
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html
  - https://web.dev/learn/accessibility/focus
  - https://webaim.org/techniques/keyboard/
  - https://www.a11yproject.com/checklist/
---

**Rule.** Write the DOM in reading order and never set `tabindex` above 0.

**Why.** A positive `tabindex` jumps those elements to the front of the tab order, ahead of everything else on the page. Each new control then needs a new number, and the order stops matching what the user sees. CSS that moves items visually without moving them in the DOM does the same thing.

**FAIL**

```html
<input name="last" tabindex="2">
<input name="first" tabindex="1">
<button tabindex="3">Save</button>
```

**PASS**

```html
<input name="first">
<input name="last">
<button>Save</button>
<!-- tabindex="0" only to add a custom widget to the order; tabindex="-1" to focus it from script -->
```

**Counterpoint.** "The visual layout puts the sidebar first, but the main content comes first in the DOM." Reorder the DOM to match, or accept the difference only if the order still makes sense to a keyboard user. Do not patch it with numbers.

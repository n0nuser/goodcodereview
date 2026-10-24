---
id: fn-focus-indicator-visible
level: function
tags: [accessibility, usability, frontend, css, keyboard]
severity: block
status: stable
lang: core
applies_when: Styles or script change `outline`, `:focus`, or `:focus-visible`.
tool_gate: Stylelint `declaration-property-value-disallowed-list` with `outline: ["none", "0"]`.
note: SC 2.4.13 (AAA, size and contrast of the indicator) is not required here; the 3:1 figure comes from web.dev and SC 1.4.11. Focus hidden under a sticky bar (SC 2.4.11) has 2 orgs (W3C, Google), so it is in Why, not the Rule
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
  - https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html
  - https://web.dev/learn/accessibility/focus
  - https://webaim.org/techniques/keyboard/
  - https://www.a11yproject.com/checklist/
---

**Rule.** Keep a visible focus indicator on every focusable element. Never set `outline: none` without a replacement.

**Why.** A keyboard user finds their place by the focus ring. Remove it and they navigate blind. A sticky header that covers the focused link has the same effect once they tab down the page. `scroll-padding-top` on `html`, as tall as the header, keeps the focused element in view.

**FAIL**

```css
*:focus { outline: none; }
a:focus { outline: 0; }
```

**PASS**

```css
:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }
```

**Counterpoint.** "Designers dislike the ring on mouse clicks." `:focus-visible` shows the ring for keyboard focus and hides it for most mouse clicks. Restyle the ring if you must. Do not remove it.

---
id: fn-target-size
level: function
tags: [accessibility, usability, frontend, css]
severity: should-fix
status: stable
lang: core
applies_when: Styles size a button, icon button, checkbox, or link that a pointer or finger operates.
tool_gate: axe `target-size` (WCAG 2.2); a rendered check for the spacing exception.
note: 3 orgs for the 24 CSS px floor and the spacing exception (W3C, Deque, Mozilla); Apple (44 pt) and web.dev (48 px) ask for more; the Material 48 dp page was not readable
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json
  - https://www.a11yproject.com/checklist/
  - https://dequeuniversity.com/rules/axe/html/4.10/target-size
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Understanding_WCAG/Operable
---

**Rule.** Make each pointer target at least 24 by 24 CSS pixels, or space it so that a 24 px circle centred on it touches no other target and no other undersized target's circle.

**Why.** Small, tight controls cause mis-taps for anyone with a tremor, a large thumb, or a bumpy train. A mis-tap on "Delete" next to "Edit" costs more than a mis-tap on a menu item.

**FAIL**

```css
.icon-btn { width: 16px; height: 16px; margin: 0; }
```

```html
<button class="icon-btn">✎</button><button class="icon-btn">🗑</button>
```

**PASS**

```css
.icon-btn { min-width: 24px; min-height: 24px; padding: 4px; }
```

**Counterpoint.** "Inline links and dense tables are exempt." Targets inside a sentence are, and so are controls with an equivalent control that is big enough. A row of toolbar icons is neither, and nor are the action buttons on a table row. Touch platforms often ask for 44 px or more, so treat 24 px as the floor, not the goal.

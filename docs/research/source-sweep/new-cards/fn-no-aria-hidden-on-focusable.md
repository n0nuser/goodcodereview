---
id: fn-no-aria-hidden-on-focusable
level: function
tags: [accessibility, frontend, aria, keyboard]
severity: should-fix
status: draft
lacks: orgs, Google and WebAIM state it; a third independent organisation is missing
lang: core
applies_when: Markup or CSS hides an element, or sets role="presentation" on it, and the element can take keyboard focus.
context: [ui]
tool_gate: axe `aria-hidden-focus`.
borrowed_from:
  - https://web.dev/learn/accessibility/aria-html
  - https://webaim.org/techniques/aria/
---

**Rule.** Never put `aria-hidden="true"`, `role="presentation"` or CSS hiding on an element that can take focus.

**Why.** Keyboard focus still lands on the element, but a screen reader is told to skip it. The user tabs onto something that is not announced, or never reaches a control that does work. To hide a control, hide it for everyone, or remove it from the tab order too.

**FAIL**

```html
<a href="/help" aria-hidden="true">Help</a>
<button type="button" role="presentation">Save</button>
```

**PASS**

```html
<a href="/help">Help</a>
<button type="button">Save</button>
<nav hidden><a href="/admin">Admin</a></nav>
```

**Counterpoint.** "The icon button is decorative, so hide it." If it takes focus, it does something, and it needs a name. Hide the icon inside the button, not the button.

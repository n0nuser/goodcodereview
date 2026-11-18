---
id: fn-no-aria-hidden-on-focusable
level: function
tags: [accessibility, frontend, aria, keyboard]
severity: should-fix
status: draft
lacks: orgs, Google and WebAIM state it; a third independent organisation is missing
lang: core
applies_when: Markup or CSS hides an element that can take keyboard focus.
context: [ui]
tool_gate: axe `aria-hidden-focus`.
borrowed_from:
  - https://web.dev/learn/accessibility/aria-html
  - https://webaim.org/techniques/aria/
---

**Rule.** Never put `aria-hidden="true"` on an element that can take focus, or leave an element visually hidden while it has focus.

**Why.** Keyboard focus still lands on the element, but a screen reader is told to skip it. The user tabs onto something that is not announced, or never reaches a control that does work. To hide a control, hide it for everyone, or remove it from the tab order too. A `role="presentation"` on a focusable element conflicts the same way: browsers ignore the role there, so the control is still announced, and axe flags it.

**FAIL**

```html
<a href="/help" aria-hidden="true">Help</a>
<a href="#main" class="skip">Skip to content</a>
<style>.skip { position: absolute; left: -9999px; }</style>   <!-- no :focus rule: focus lands on nothing visible -->
```

**PASS**

```html
<a href="/help">Help</a>
<button type="button">Save</button>
<nav hidden><a href="/admin">Admin</a></nav>   <!-- hidden removes it from the tab order -->
<a href="#main" class="skip">Skip to content</a>
<style>.skip { position: absolute; left: -9999px; } .skip:focus { left: 0; }</style>
```

**Counterpoint.** "The icon button is decorative, so hide it." If it takes focus, it does something, and it needs a name. Hide the icon inside the button, not the button.

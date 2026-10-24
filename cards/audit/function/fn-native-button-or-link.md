---
id: fn-native-button-or-link
level: function
tags: [accessibility, usability, frontend, html]
severity: block
status: draft
lang: core
applies_when: A component handles a click or tap, or navigates.
tool_gate: ESLint `jsx-a11y/click-events-have-key-events` and `jsx-a11y/no-static-element-interactions`; `jsx-a11y/anchor-is-valid` for `href="#"`.
note: 4 orgs; Norman's perceived-affordance essay is context only
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
  - https://webaim.org/techniques/keyboard/
  - https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
  - https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
  - https://jnd.org/affordances-and-design/
---

**Rule.** Use `<button>` for an action and `<a href>` for navigation. Do not attach a click handler to a `div`, `span`, or `a` with no `href`.

**Why.** A `div` is not in the tab order, has no role, and ignores Enter and Space. A keyboard or screen-reader user cannot reach or operate it. A fake link also loses open-in-new-tab and copy-link. A native element gives all of that with no code.

**FAIL**

```jsx
<div className="btn" onClick={save}>Save</div>
<a href="#" onClick={openMenu}>Menu</a>
<span onClick={() => navigate("/billing")}>Billing</span>
```

**PASS**

```jsx
<button type="button" onClick={save}>Save</button>
<button type="button" onClick={openMenu}>Menu</button>
<a href="/billing">Billing</a>
```

**Counterpoint.** "Native buttons are hard to style." They are not: reset `border`, `background`, and `font` on the element. Rebuilding the keyboard, role, and focus behaviour by hand costs more and fails more often. Where a custom widget is unavoidable, see `fn-aria-role-has-state-and-keys`.

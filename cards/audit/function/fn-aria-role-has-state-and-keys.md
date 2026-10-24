---
id: fn-aria-role-has-state-and-keys
level: function
tags: [accessibility, frontend, aria, keyboard]
severity: should-fix
status: draft
lang: core
applies_when: A custom widget sets `role` or an `aria-*` attribute because no native element fits.
tool_gate: ESLint `jsx-a11y/role-has-required-aria-props`; axe `aria-required-attr`. Neither checks that the keys work.
note: 3 orgs (W3C, Mozilla, Heydon Pickering); both tool-gate rule names checked against the jsx-a11y README and the axe rule list; held at draft: the state and keys clauses have 2 orgs each, only W3C backs all three
borrowed_from:
  - https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/
  - https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
  - https://inclusive-components.design/toggle-button/
---

**Rule.** When a native element cannot do the job, give the custom widget its name, its state attribute, and the keys its role promises.

**Why.** A role only tells assistive technology what the element is. It adds no keyboard behaviour, and it says nothing about state. A `role="switch"` with no `aria-checked` is announced as a switch of unknown state. Wrong ARIA is worse than none, because it gives a screen-reader user a false picture.

**FAIL**

```jsx
<button type="button" role="switch" onClick={toggle}>Dark mode</button>
// no aria-checked: announced as a switch of unknown state
```

**PASS**

```jsx
<button type="button" role="switch" aria-checked={on} onClick={toggle}>
  Dark mode
</button>
// a native <button> already takes Tab, Enter, and Space
```

**Counterpoint.** "ARIA patterns are in the guide, so we copy them." Copy the keyboard table as well as the attributes. For a plain toggle, a `button` with `aria-pressed` is enough, and the label should stay the same when the state changes.

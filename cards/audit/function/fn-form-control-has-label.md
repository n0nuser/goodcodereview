---
id: fn-form-control-has-label
level: function
tags: [accessibility, usability, frontend, forms]
severity: block
status: stable
lang: core
applies_when: Markup or a component renders an input, a select, or a textarea.
tool_gate: ESLint `jsx-a11y/label-has-associated-control` and axe `label`.
note: 5 orgs back the rule; USWDS covers only fieldset and legend
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html
  - https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML
  - https://dequeuniversity.com/rules/axe/html/4.10/label
  - https://www.a11yproject.com/checklist/
  - https://github.com/jsx-eslint/eslint-plugin-jsx-a11y
---

**Rule.** Tie every form control to a visible `<label>`, with `for` and a matching `id` or by wrapping it. A placeholder is not a label.

**Why.** A screen reader announces a bare field as "edit text". Voice-control users cannot say its name. A label also enlarges the click target. A placeholder vanishes when the user types, so it fails every user who looks away and comes back.

**FAIL**

```html
<input type="email" placeholder="Email">
<div class="label">Name</div>
<input type="text" id="name">
```

**PASS**

```html
<label for="email">Email</label>
<input type="email" id="email" autocomplete="email">

<label>Name <input type="text" name="name" autocomplete="name"></label>
```

**Counterpoint.** "The design shows a floating placeholder label." A floating label is a real label if it stays visible and is wired to the input. Use `aria-label` only where the purpose is already visible, such as a search field next to a Search button.

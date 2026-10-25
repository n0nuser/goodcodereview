---
id: fn-disclosure-hides-only-secondary
level: function
tags: [usability, frontend, html]
severity: should-fix
status: stable
lang: core
applies_when: Markup or a component hides content behind a `<details>`, an accordion, a "Show more" link, or an "Advanced" toggle.
tool_gate: none
note: 3 orgs say not to hide what most users need (NN/g, GOV.UK, Appian). The two-level cap is NN/g's alone, so it sits in Why. Primer and Microsoft treat disclosure as a last resort but state neither part
borrowed_from:
  - https://www.nngroup.com/articles/progressive-disclosure/
  - https://design-system.service.gov.uk/components/details/
  - https://docs.appian.com/suite/help/26.9/sail/ux-progressive-disclosure.html
---

**Rule.** Do not hide a required field, the primary action, or information most users need behind a disclosure that starts closed.

**Why.** Users who never open the disclosure must still be able to finish the task. A closed `<details>` that holds the delivery date, or an "Advanced" section that holds a required field, sends most users hunting. Disclosure is for what only some users need. A field that appears because of the user's own answer, such as a follow-up field shown after they pick "Yes", is a conditional reveal, not a disclosure, and passes. Nesting adds its own cost. NN/g counts the first view as level one, so a disclosure inside a disclosure is already level three, and NN/g found designs past two levels lose people as they move between levels. In a step-by-step flow, such as picking a make and then a model, Appian says to disable fields that are not ready yet rather than hide them.

**FAIL**

```html
<details>
  <summary>Delivery options</summary>
  <label for="address">Delivery address</label>
  <input type="text" id="address" required>
</details>
```

**PASS**

```html
<label for="address">Delivery address</label>
<input type="text" id="address" required>
<details>
  <summary>Add an order reference</summary>
  <label for="ref">Order reference</label>
  <input type="text" id="ref">
</details>
```

**Counterpoint.** "Hiding fields makes the form shorter." It makes the first view shorter, but required content still has to be found. Measure who opens the disclosure. If most users open it, the content belongs on the default view.

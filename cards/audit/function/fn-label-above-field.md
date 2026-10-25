---
id: fn-label-above-field
level: function
tags: [usability, accessibility, frontend, forms, css]
severity: discuss
status: draft
lacks: evidence, NN/g backs it for mobile and short forms, W3C lists it as one of two conventions; needs a third org that recommends it outright
lang: core
applies_when: Markup or styles lay out a form field and its visible label.
tool_gate: none
note: 4 orgs put the label above a text field (GOV.UK, Atlassian, NN/g for mobile and short forms, W3C as one of two conventions). The checkbox and radio order is W3C's alone, so it sits in Why. W3C also says the choice depends on nearby fields, so the severity is discuss
borrowed_from:
  - https://design-system.service.gov.uk/components/text-input/
  - https://atlassian.design/components/textfield/usage
  - https://www.nngroup.com/articles/web-form-design/
  - https://www.w3.org/WAI/tutorials/forms/labels/
---

**Rule.** Put the visible label of a text input, select, or textarea directly above it, with no link, button, or other field between them.

**Why.** A label sitting below a field, or halfway between two fields, gets read as the label of the wrong one. W3C notes that a label above the field cuts sideways scrolling for low-vision and phone users, who can lose a side label off the edge of the screen. Hint and error text can go between the label and the field. A help link, a button, or another field cannot. Checkboxes and radios are the exception: W3C puts the control first and its label to the right, in left-to-right languages.

**FAIL**

```html
<input type="text" id="town">
<label for="town">Town or city</label>

<label for="postcode">Postcode</label>
<a href="/help/postcode">Why we ask</a>
<input type="text" id="postcode">
```

**PASS**

```html
<label for="town">Town or city</label>
<input type="text" id="town" autocomplete="address-level2">

<label for="postcode">Postcode</label>
<p id="postcode-hint">For example, SW1A 2AA</p>
<input type="text" id="postcode" aria-describedby="postcode-hint">
```

**Counterpoint.** "Labels to the left fit our long desktop admin form better." NN/g allows labels beside the field for very long desktop forms, and W3C names left as a convention too. Accept a left label on such a form if it stays next to its own field at every breakpoint. A wrapping label, as in the `fn-form-control-has-label` PASS, passes when CSS sets the label text to `display: block` so it sits above the field. A label below the field, or a link or another control between the label and the field, is still a `FAIL`. This card covers placement only. `fn-form-control-has-label` covers the code tie between label and field.

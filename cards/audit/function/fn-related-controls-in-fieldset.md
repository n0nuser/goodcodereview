---
id: fn-related-controls-in-fieldset
level: function
tags: [accessibility, usability, frontend, forms, html]
severity: should-fix
status: stable
lang: core
applies_when: Markup or a component renders a radio group, a checkbox group, or a value split across several inputs, such as a date or an address.
tool_gate: none
note: 4 orgs (GOV.UK, W3C, USWDS, A11y Project). NN/g asks to tag groups for screen readers but does not name fieldset, so it does not count. No source gives a spacing threshold, so spacing stays out of the Rule. Only GOV.UK says the legend comes first, so that sits in Why
borrowed_from:
  - https://design-system.service.gov.uk/components/fieldset/
  - https://design-system.service.gov.uk/components/date-input/
  - https://www.w3.org/WAI/tutorials/forms/grouping/
  - https://designsystem.digital.gov/components/form/
  - https://www.a11yproject.com/checklist/
---

**Rule.** Wrap each radio group, checkbox group, and multi-part value, such as day, month, and year, in a `<fieldset>` with a `<legend>` that names the group, often as the question.

**Why.** Each radio's own label says only "Yes" or "No". Without a group, a screen reader user hears the option but not the question it answers. Put the `legend` first inside the `fieldset`. It acts as the group's heading, so assistive technology can tie each option to its question. The same holds for a date split into three boxes labelled "Day", "Month", and "Year". The visual group needs a matching code group, or the two drift apart.

**FAIL**

```html
<p>Do you have a passport?</p>
<input type="radio" id="pp-yes" name="passport" value="yes">
<label for="pp-yes">Yes</label>
<input type="radio" id="pp-no" name="passport" value="no">
<label for="pp-no">No</label>
```

**PASS**

```html
<fieldset>
  <legend>Do you have a passport?</legend>
  <input type="radio" id="pp-yes" name="passport" value="yes">
  <label for="pp-yes">Yes</label>
  <input type="radio" id="pp-no" name="passport" value="no">
  <label for="pp-no">No</label>
</fieldset>
```

**Counterpoint.** "A `fieldset` draws a border we don't want." Remove the border in CSS with `border: 0; padding: 0; margin: 0`. The grouping still reaches assistive technology. A `div` with `role="group"` and `aria-labelledby` is a fallback for a design system that cannot render a `fieldset`. VoiceOver on iOS ignores `fieldset` and `legend`. That is a reason to add `aria-labelledby` on each input as well, not to drop the group. A single checkbox, such as "I agree", needs no `fieldset`.

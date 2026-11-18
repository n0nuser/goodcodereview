---
id: fn-error-summary
level: function
tags: [accessibility, usability, frontend, forms]
severity: should-fix
status: draft
lacks: orgs, "links each error to its field" has GOV.UK only; needs two more orgs that show a linked summary
lang: core
applies_when: Code renders a form again after validation fails.
context: [ui]
tool_gate: none; a rendered check that submits an invalid form and looks for the summary.
borrowed_from:
  - https://design-system.service.gov.uk/components/error-summary/
  - https://design-system.service.gov.uk/components/error-message/
  - https://www.a11yproject.com/checklist/
---

**Rule.** After a failed submit, show a summary at the top of the page that lists every error and links each one to its field.

**Why.** On a long form, an error below the fold goes unseen, and a screen reader user hears none of it until they reach the field. A summary at the top shows the whole problem at once and lets the user jump to each field. Show it even when there is only one error. Keep the message next to each field too; see [[fn-error-says-what-and-how]].

**FAIL**

```html
<form>
  <label for="email">Email</label>
  <input id="email" name="email">
  <label for="dob">Date of birth</label>
  <input id="dob" name="dob">
  <p class="error">Enter a valid date</p>
</form>
```

**PASS**

```html
<div class="error-summary" role="alert" tabindex="-1">
  <h2>There is a problem</h2>
  <ul>
    <li><a href="#email">Enter an email address</a></li>
    <li><a href="#dob">Enter a valid date of birth</a></li>
  </ul>
</div>
<form>
  ...
</form>
```

**Counterpoint.** "The summary repeats the per-field messages and adds noise." It repeats them on purpose: the summary is for finding the errors, and the field message is for fixing one. The cost is one short list.

---
id: fn-error-says-what-and-how
level: function
tags: [usability, accessibility, frontend, forms]
severity: should-fix
status: stable
lang: core
applies_when: Code builds the message shown when user input fails validation.
tool_gate: none; a rendered check that submits each invalid field.
borrowed_from:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.nngroup.com/articles/error-message-guidelines/
  - https://design-system.service.gov.uk/components/error-message/
  - https://design-system.service.gov.uk/components/error-summary/
  - https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html
  - https://www.w3.org/WAI/tutorials/forms/notifications/
  - https://designsystem.digital.gov/components/form/
  - https://www.cs.umd.edu/users/ben/goldenrules.html
---

**Rule.** Show each validation error next to its field, in plain words that name what is wrong and how to fix it.

**Why.** "Invalid input" or an error code leaves the user to guess which field and what to change. A message at the top of a long form, or in a toast that fades, sends a magnifier user searching. Naming the fix is the shortest path to a valid form.

**FAIL**

```html
<input id="dob" name="dob" class="red">
<div class="toast">Error 422: invalid data</div>
```

**PASS**

```html
<label for="dob">Date of birth</label>
<p id="dob-err"><span class="visually-hidden">Error:</span>
   Enter a date of birth in the past, such as 27 3 1986</p>
<input id="dob" name="dob" aria-invalid="true" aria-describedby="dob-err">
```

**Counterpoint.** "Detailed messages leak information." For a login, that is true: say "Email or password is wrong". For ordinary fields, the specific message is the fix. Hold back the suggestion only where it would weaken security.

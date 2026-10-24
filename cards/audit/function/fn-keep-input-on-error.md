---
id: fn-keep-input-on-error
level: function
tags: [usability, frontend, forms]
severity: should-fix
status: stable
lang: core
applies_when: A form handler or component re-renders after a failed validation or a failed submit.
tool_gate: none; a test that submits an invalid form and asserts the entered values are still there.
note: GOV.UK says validate on submit and Baymard says validate when the user leaves a field; this card takes no side on timing. Shneiderman's rule 8 is about re-entry across screens and is related, not the same.
borrowed_from:
  - https://www.nngroup.com/articles/error-message-guidelines/
  - https://design-system.service.gov.uk/components/error-message/
  - https://design-system.service.gov.uk/patterns/validation/
  - https://baymard.com/blog/inline-form-validation
  - https://www.cs.umd.edu/users/ben/goldenrules.html
---

**Rule.** After a failed validation or submit, show the form again with every value the user entered, correct or not.

**Why.** A form that wipes its fields turns one typo into ten minutes of retyping, and some users give up. The user fixes one field, not the whole page.

**FAIL**

```jsx
async function submit(e) {
  e.preventDefault();
  const res = await post("/signup", values);
  if (!res.ok) { setErrors(res.errors); setValues(EMPTY); }
}
```

**PASS**

```jsx
async function submit(e) {
  e.preventDefault();
  const res = await post("/signup", values);
  if (!res.ok) setErrors(res.errors);   // values stay as typed
}
```

**Counterpoint.** "Clear a password or card number on error for safety." That is a fair exception for secrets, and the message should say so. Everything else the user typed stays.

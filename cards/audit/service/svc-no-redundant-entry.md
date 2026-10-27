---
id: svc-no-redundant-entry
level: service
tags: [usability, accessibility, frontend, forms]
severity: should-fix
status: stable
lang: core
applies_when: A multi-step flow, such as checkout or signup, asks for data in more than one step.
tool_gate: none; a walk through the flow that lists each field asked twice.
note: 3 orgs (W3C, GOV.UK, Baymard); Baymard sells research, so it is closer to a vendor. NN/g and Shneiderman back the Why (recognition over recall), not the practice
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.cs.umd.edu/users/ben/goldenrules.html
  - https://design-system.service.gov.uk/patterns/question-pages
  - https://baymard.com/blog/set-billing-equal-to-shipping
---

**Rule.** Do not ask for information the user already gave in the same flow. Fill it in, or let the user pick it.

**Why.** Typing the same address twice costs time and adds typos. People recognise what they gave more easily than they recall it, so show it and let them confirm it.

**FAIL**

```html
<!-- step 1 -->  <input name="ship_address">
<!-- step 2 -->  <input name="billing_address">   <!-- empty again -->
```

**PASS**

```html
<!-- step 2 -->
<label><input type="checkbox" name="same" checked> Billing address is the same as shipping</label>
<input name="billing_address" value="12 Elm Road, Leeds" hidden>   <!-- hidden while the box is checked; shown, pre-filled, when it is unchecked -->
```

**Counterpoint.** "Retyping a new password confirms it." That is a fair exception. So is data that is no longer valid, and re-entry that is the point of the task, such as a memory test. Browser autofill does not count: the page itself must supply the value.

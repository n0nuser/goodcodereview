---
id: fn-destructive-confirm-or-undo
level: function
tags: [usability, frontend, forms]
severity: should-fix
status: stable
lang: core
applies_when: A handler deletes user data, spends money, or sends something that cannot be recalled.
tool_gate: none; a test that triggers the action and asserts a confirm step or an undo path exists.
note: 4 orgs (NN/g, Apple, W3C, Shneiderman) for undo or confirm. Naming the outcome on the buttons and not defaulting to Cancel has 2 (NN/g, Apple), so it is in Why. Norman's undo chapter is a table of contents only, so topic only
borrowed_from:
  - https://www.nngroup.com/articles/confirmation-dialog/
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/alerts.json
  - https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html
  - https://www.cs.umd.edu/users/ben/goldenrules.html
---

**Rule.** Make a destructive action reversible with undo, or ask the user to confirm it before it runs.

**Why.** People click the wrong thing. If the action cannot be reversed and nothing stops it, one slip deletes their work. Undo costs a successful user nothing, while a dialog on every click trains them to click through. A dialog works best when its buttons name the outcome, such as "Delete project" and "Cancel", because "OK" and "Are you sure?" say nothing about what happens next.

**FAIL**

```jsx
<button onClick={() => api.deleteProject(id)}>Delete</button>
```

**PASS**

```jsx
async function remove() {
  await api.softDelete(id);
  toast("Project deleted", { action: { label: "Undo", onClick: () => api.restore(id) } });
}
// irreversible case: a dialog "Delete project “Q3 plan”?" with buttons "Delete project" and "Cancel"
```

**Counterpoint.** "Confirm everything to be safe." Frequent prompts are dismissed without reading, so they protect nothing. Use undo for common actions and reserve the dialog for rare, irreversible ones. Do not make Cancel the default button.

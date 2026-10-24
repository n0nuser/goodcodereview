---
id: sys-consistent-ui-terms
level: system
tags: [usability, accessibility, frontend, design-system]
severity: discuss
status: draft
lang: core
applies_when: Several screens or apps show the same action, status, or concept to the same users.
tool_gate: none; list the labels and icons for one action across all screens.
note: This card is about words and controls a user sees. Names in code are `mod-one-name-per-concept`, and API field names are `svc-api-naming-consistent`.
borrowed_from:
  - https://www.nngroup.com/articles/ten-usability-heuristics/
  - https://www.cs.umd.edu/users/ben/goldenrules.html
  - https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html
  - https://www.gov.uk/guidance/government-design-principles
  - https://design-system.service.gov.uk/components/error-message/
---

**Rule.** Use one label, one icon, and one place for the same action and the same concept across all screens.

**Why.** When "Remove", "Delete", and "Discard" all mean the same thing, users stop trusting any of them and ask whether each one differs. A familiar control costs no thought. A different one costs a pause, and in a destructive flow, a mistake.

**FAIL**

```text
Orders page:    [Delete]       (trash icon, right of row)
Customers page: [Remove]       (x icon, left of row)
Invoices page:  [Discard draft](no icon, menu)
```

**PASS**

```text
Orders, Customers, Invoices: [Delete] with the trash icon, last action in the row menu.
A different outcome, such as archive, gets a different label: [Archive].
```

**Counterpoint.** "Each team knows its users best." The standard asks for consistent, not uniform. Differ where the job differs, and keep the wording and look of the shared actions the same. Drive the shared parts from the design-system component, so they cannot drift.

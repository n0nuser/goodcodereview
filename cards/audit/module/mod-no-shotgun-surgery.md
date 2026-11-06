---
id: mod-no-shotgun-surgery
level: module
tags: [maintainability, design, coupling]
severity: discuss
status: stable
lang: core
applies_when: A change to one rule, format or decision needs small edits in many classes or files.
tool_gate: none
note: smell "Shotgun Surgery" (Fowler and Beck, through Refactoring.Guru); Microsoft says behaviour spread over several places is a frequent source of errors, and NDepend asks where the knowledge lives; Microsoft's warning about the wrong abstraction is the counterpoint
borrowed_from:
  - https://refactoring.guru/smells/shotgun-surgery
  - https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles
  - https://blog.ndepend.com/shotgun-surgery
---

**Rule.** Keep one decision in one module, and when a single change needs edits in many classes, move the scattered parts together.

**Why.** One change repeats in file after file, and the copy you miss is the defect. Refactoring.Guru describes the smell as "a single responsibility has been split up among a large number of classes". Microsoft says behaviour spread over several places is "a frequent source of errors" and asks for one construct to own it. NDepend says knowledge should exist in one place. The test is concrete: the same rule changes in the same set of files every time.

**FAIL**

```text
Adding a currency edits: pricing.py, invoice.py, tax.py, export.py, email.py, api.py, report.py
# the last two currency changes edited the same seven files
```

**PASS**

```text
Adding a currency edits: money.py   (rounding, formatting and tax rules live there)
```

**Counterpoint.** "A feature naturally touches many files." A new field does touch the model, the API and the UI. The smell is one internal rule that spreads. Duplication beats coupling to the wrong abstraction, and that is the limit: if the edits are unrelated decisions, merging them would create the wrong abstraction. The signal is that every change of this kind edits the same files.

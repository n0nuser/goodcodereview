---
id: svc-boolean-no-is-prefix
level: service
tags: [maintainability, api, naming]
severity: discuss
status: draft
lacks: orgs, Google and Microsoft only; needs one more org that drops the "is" prefix on boolean API fields
lang: core
applies_when: A new API defines a boolean field or query parameter.
context: [server]
tool_gate: Spec linter with a naming rule for boolean fields.
borrowed_from:
  - https://google.aip.dev/140
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md
---

**Rule.** Name a new boolean field for its state (`enabled`, `required`), not with an `is` prefix.

**Why.** The type already says it is a boolean. The prefix adds length and mixes two styles in one API (`isEnabled` next to `required`), so callers must look up each name.

**FAIL**

```json
{"id": 7, "isEnabled": true, "isRequired": false}
```

**PASS**

```json
{"id": 7, "enabled": true, "required": false}
```

**Counterpoint.** "Our code base names booleans with `is`." That fits a method or a local variable. Fields in a public API are read by many languages, and the name outlives yours. Do not rename a field that clients already use; the card applies to new fields.

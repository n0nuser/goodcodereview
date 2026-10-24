---
id: mod-internals-unreachable
level: module
tags: [encapsulation, boundaries]
severity: should-fix
status: draft
lang: core
applies_when: A module has an intended public surface and internal files or symbols.
tool_gate: Import-boundary lint (import-linter, ESLint `no-restricted-imports`, package `exports`).
note: one vendor's engineering guidance (opinion), from pstack architect/references/design-red-flags
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/architect/references/design-red-flags.md
---

**Rule.** Make a module's internals unimportable from outside it, and have a check fail the build when a caller reaches in.

**Why.** Anything a caller can import becomes the interface. A naming convention such as a leading underscore stops no one, and the module can no longer change its internals without breaking callers.

**FAIL**

```python
from billing.internal.tax_tables import RATES   # nothing stops this
```

**PASS**

```text
billing/__init__.py exports calculate_tax; import-linter contract forbids billing.internal.* from outside billing
```

**Counterpoint.** "A boundary check is overhead for a small repo." One lint contract is cheap, and the first outside import of an internal costs more. For a single-file module, there is no inside to protect, so mark `N/A`.

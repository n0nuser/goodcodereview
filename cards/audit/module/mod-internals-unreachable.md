---
id: mod-internals-unreachable
level: module
tags: [maintainability, encapsulation, boundaries]
severity: should-fix
status: stable
lang: core
applies_when: A module has an intended public surface, with internal files, symbols or members.
tool_gate: Import-boundary lint (import-linter, ESLint `no-restricted-imports`, package `exports`), Pylint protected-access (W0212).
note: the import half has Google (Go internal packages and Bazel visibility), Cursor's design red flags and Microsoft (the `internal` keyword, a definition); the member half has Refactoring.Guru, PEP 8 and Pylint. A test may use a documented test-only export
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/architect/references/design-red-flags.md
  - https://bazel.build/concepts/visibility
  - https://pkg.go.dev/cmd/go#hdr-Internal_packages
  - https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/internal
  - https://refactoring.guru/smells/inappropriate-intimacy
  - https://peps.python.org/pep-0008/
  - https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/protected-access.html
---

**Rule.** Keep a module's internals unimportable and untouched from outside it. A caller uses the public surface, not a private file or member.

**Why.** Anything a caller can import becomes the interface, and a field a caller writes becomes part of the contract. A naming convention such as a leading underscore stops no one, and the module can no longer change its internals without breaking callers.

**FAIL**

```python
from billing.internal.tax_tables import RATES   # nothing stops this
order._lines.append(line)                       # outside Order
```

**PASS**

```text
billing/__init__.py exports calculate_tax; import-linter contract forbids billing.internal.* from outside billing
order.add_line(line)
```

**Counterpoint.** "A boundary check is overhead for a small repo, and tests need internals." One lint contract is cheap, and the first outside import of an internal costs more. Tests may use a documented test-only export, and Java's qualified `exports ... to` or C#'s `InternalsVisibleTo` give them a door. For a single-file module, there is no inside to protect, so mark `N/A`.

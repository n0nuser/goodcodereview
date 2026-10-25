---
id: py-ruff-gate
level: change
tags: [maintainability, python, tooling]
severity: should-fix
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: python
applies_when: The project is Python and has a linter configuration.
tool_gate: ruff
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Enable the Ruff rule sets E, F, I, B, UP, SIM, BLE, TID and D in CI.

**Why.** The tool owns formatting, import order, the choice between `Optional` and `X | None`, bare `except`, and relative imports. Human review time goes to what tools cannot see. `D1xx` stays ignored: the gate checks docstring format, not presence. Anything the gate decides is not a review comment; the comment is "add the gate".

**FAIL**

```toml
[tool.ruff.lint]
select = ["E", "F"]
```

**PASS**

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "BLE", "TID", "D"]
ignore = ["D100", "D101", "D102", "D103", "D104", "D105", "D106", "D107"]
[tool.ruff.lint.pydocstyle]
convention = "google"
[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"
```

**Counterpoint.** "Strict lint slows contributors." It speeds review: repeated nitpicks are a sign of a missing gate (Google, Pragmatic Engineer notes).

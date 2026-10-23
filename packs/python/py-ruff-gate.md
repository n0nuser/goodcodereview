---
id: py-ruff-gate
level: change
tags: [python, tooling]
severity: should-fix
status: draft
lang: python
applies_when: The project is Python and has a linter configuration.
tool_gate: ruff
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Configure Ruff with at least E, F, I, B, UP, SIM, BLE, TID, D. Anything the gate can decide is not a review comment: the comment is "add the gate".

**Why.** Formatting, import order, `Optional` vs `X | None`, bare `except` and relative imports belong to the tool. Human review time goes to what tools cannot see. `D1xx` stays ignored: the gate checks docstring format, not presence.

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

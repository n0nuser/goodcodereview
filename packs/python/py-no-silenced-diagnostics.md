---
id: py-no-silenced-diagnostics
level: change
tags: [python, tooling]
severity: block
status: draft
lang: python
applies_when: A diff adds `# noqa`, `# type: ignore`, widens the ignore list, or skips a test.
tool_gate: ruff PGH003/PGH004
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Never silence a diagnostic to get green. A justified suppression names one code and a reason on the same line. Remove the shim and its ignore when the cause is fixed.

**Why.** A bare suppression turns off a whole class of future errors on that line and hides the real bug.

**FAIL**

```python
total = compute(order)  # type: ignore
```

**PASS**

```python
import numpy_stubs  # type: ignore[import-untyped]  # no stubs published upstream
```

**Counterpoint.** "CI is red for unrelated reasons." Then fix or mark the unrelated cause on its own; do not widen the ignore list.

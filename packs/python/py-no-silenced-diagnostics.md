---
id: py-no-silenced-diagnostics
level: change
tags: [maintainability, python, tooling]
severity: should-fix
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: python
applies_when: A diff adds `# noqa` or `# type: ignore`.
tool_gate: ruff PGH003, PGH004
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Suppress a Python diagnostic only with a single named code and a reason on the same line.

**Why.** Core rule: [[chg-no-silenced-diagnostics]]. A bare `# type: ignore` silences every error on the line, including the next one someone introduces.

**FAIL**

```python
total = compute(order)  # type: ignore
x = risky()  # noqa
```

**PASS**

```python
import numpy_stubs  # type: ignore[import-untyped]  # no stubs published upstream
except Exception:  # noqa: BLE001  # process boundary: log and continue
```

**Counterpoint.** "A reason on every line is noise." Only suppressions need one, and they should be rare. A pile of them is the finding.

---
id: chg-refactor-has-behaviour-pin
level: change
tags: [refactoring, tests]
severity: should-fix
status: draft
lang: core
applies_when: The change restructures code and claims to keep its behaviour.
tool_gate: Snapshot or golden-file tests in CI.
note: one vendor's engineering guidance (opinion), from poteto-mode/playbooks/refactoring.md; type checks and lint do not pin behaviour
borrowed_from:
  - https://github.com/cursor/plugins
---

**Rule.** Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.

**Why.** A type check and a linter pass on code that now does something else. Without a pin, "no behaviour change" is a claim nobody ran.

**FAIL**

```text
PR "split billing.py into three modules": 900 lines moved, no test touched or added.
```

**PASS**

```text
Commit 1: golden-file test of invoice output for 12 fixtures (passes on old code).
Commit 2: the split. The same test passes unchanged.
```

**Counterpoint.** "The code is already well tested." Then name the test that covers the moved paths. If you cannot, the pin is missing. See [[chg-refactor-separate]] for keeping the refactor apart from behaviour changes.

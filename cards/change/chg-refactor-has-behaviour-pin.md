---
id: chg-refactor-has-behaviour-pin
level: change
tags: [testing, maintainability, refactoring, tests]
severity: should-fix
status: stable
lang: core
applies_when: The change restructures code and claims to keep its behaviour.
tool_gate: Snapshot or golden-file tests in CI.
note: Rule backed by cursor/plugins (refactoring playbook), GitHub (existing visual regression snapshots matched before and after the CSS Modules move) and Stripe (a tool diffed parse trees across files rubyfmt formatted)
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/refactoring.md
  - https://github.blog/engineering/architecture-optimization/improving-site-performance-by-shipping-more-css
  - https://stripe.dev/blog/formatting-an-entire-25-million-line-codebase-overnight-the-rubyfmt-story
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

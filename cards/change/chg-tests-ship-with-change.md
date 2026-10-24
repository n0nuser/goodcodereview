---
id: chg-tests-ship-with-change
level: change
tags: [testing]
severity: block
status: stable
lang: core
applies_when: The change alters behaviour of non-trivial code.
tool_gate: Coverage-delta or "changed source without changed tests" check in CI.
borrowed_from:
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
---

**Rule.** New or changed behaviour arrives in the same change as a test that fails if the behaviour breaks; a code-only change needs a stated reason.

**Why.** "Tests later" mostly means never, and the reviewer cannot tell from reading whether the code does what the author intended.

**FAIL**

```text
PR touches billing/discount.py (+90 lines). No file under tests/ changed.
Description: "will add tests in a follow-up".
```

**PASS**

```text
PR adds discount.py change and test_discount.py with the edge cases
(zero quantity, stacked coupons); the test was seen failing before the fix.
```

**Counterpoint.** "Holding a good change for tests blocks progress." Approve changes that improve the code even if imperfect, but the test is part of the change, not polish. Untestable cases exist (config, pure docs, emergency fixes), and the rule allows them with a written reason and a ticket for the test.

---
id: chg-tests-ship-with-change
level: change
tags: [testing]
severity: block
status: stable
lang: core
applies_when: The change alters behaviour of non-trivial code.
tool_gate: Coverage-delta or "changed source without changed tests" check in CI.
note: Rust and Rails state the test that fails without the change; Microsoft and Google state the same-change arm. Only Mozilla (the reviewer writes the reason) and GitLab (open an issue for the gap) touch the stated-reason arm, so it sits in the Counterpoint, not the Rule
borrowed_from:
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://rustc-dev-guide.rust-lang.org/tests/adding.html
  - https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html
  - https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/
  - https://firefox-source-docs.mozilla.org/testing/testing-policy/index.html
---

**Rule.** Ship new or changed behaviour in the same change as a test that fails if the behaviour breaks.

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

**Counterpoint.** "Holding a good change for tests blocks progress." Approve changes that improve the code even when imperfect, but the test is part of the change, not polish. Untestable cases exist (config, pure docs, emergency fixes), and a written reason plus a ticket for the test is the usual way to ship without one.

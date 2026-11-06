---
id: fn-length-budget
level: function
tags: [maintainability, readability, size]
severity: discuss
status: stable
lang: core
applies_when: A function has grown past the length limit the project sets, or the project has no limit yet.
tool_gate: ESLint max-lines-per-function (default 50), Pylint too-many-statements (R0915, max-statements default 50), Checkstyle MethodLength (default 150), RuboCop Metrics/MethodLength (default 10), PMD NcssCount (methodReportLevel default 60). PMD CognitiveComplexity (default 15) and Microsoft CA1505 (maintainability index threshold 10) measure complexity, not length.
note: length is a signal, not a defect. ESLint, Checkstyle, Pylint, RuboCop and PMD ship a size gate. Google (about 40 lines, no hard limit), the Linux kernel, Pylint and Microsoft CA1505 back the split clause and keep a long simple body, so the card asks for an inspection when a function passes the limit
borrowed_from:
  - https://eslint.org/docs/latest/rules/max-lines-per-function
  - https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html
  - https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-statements.html
  - https://checkstyle.sourceforge.io/checks/sizes/methodlength.html
  - https://docs.rubocop.org/rubocop/latest/cops_metrics.html
  - https://pmd.github.io/pmd/pmd_rules_java_design.html
  - https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1505
  - https://google.github.io/styleguide/pyguide.html#318-function-length
  - https://www.kernel.org/doc/html/latest/process/coding-style.html
---

**Rule.** Split a function that passes the project's length limit (about 40 lines if it sets none) unless its body is one simple operation or one flat dispatch.

**Why.** A long body hides its steps. Validation, pricing, a charge, the order write and the receipt become one block, and a reader cannot test, skip or reorder one of them. Linters ship a limit because a long method is hard to understand and does too many things, so set one in the project's linter. The number is where the inspection starts, not a verdict. A body that is one flat dispatch can stay long, because its reader follows one dispatch rule.

**FAIL**

```javascript
// eslint max-lines-per-function: checkout has 140 lines (max 50)
function checkout(cart, user) {
  // 30 lines validating the cart
  // 25 lines pricing it
  // 35 lines charging the card
  // 25 lines writing the order
  // 25 lines emailing the receipt
}
```

**PASS**

```javascript
function checkout(cart, user) {
  const total = price(validateCart(cart), user);
  charge(user, total);
  saveOrder(user, cart);
  emailReceipt(user);
}
// each helper is under the project's limit
```

**Counterpoint.** "A long function is one operation, and the split scatters the sequence." Length alone does not decide. A hard limit can force bad splits, which is why Google sets none, so treat the limit as a prompt to inspect. Keep the function when its body is one simple operation or one flat dispatch table. Split when the lines serve different jobs, and let each new function own one of them.

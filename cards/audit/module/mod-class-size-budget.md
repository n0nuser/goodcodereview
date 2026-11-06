---
id: mod-class-size-budget
level: module
tags: [maintainability, design, size]
severity: discuss
status: stable
lang: core
applies_when: One class or type passes the project's size limit for fields, public methods or lines, or the project sets no limit. A long file that holds several units belongs to code-file-lines-ceiling, and a module that mixes concepts is judged for cohesion, not size.
tool_gate: Pylint too-many-instance-attributes (R0902, max-attributes default 7) and too-many-public-methods (R0904, default 20), PMD NcssCount (classReportLevel default 1500) or GodClass, RuboCop Metrics/ClassLength (default 100).
note: Pylint, PMD and RuboCop enforce a class-size limit but measure different things (fields, public methods, lines, NCSS); Pylint and PMD also give the rationale (a simpler class; split a god class). Microsoft CA1505 is a maintainability index, not a size gate, so it is not listed. The card asks for the project's limit and treats the result as a prompt to ask what the class owns
borrowed_from:
  - https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html
  - https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-instance-attributes.html
  - https://pmd.github.io/pmd/pmd_rules_java_design.html
  - https://docs.rubocop.org/rubocop/latest/cops_metrics.html
---

**Rule.** Split a class that passes the project's size limit for fields, public methods or lines, unless it is a data record.

**Why.** A class that owns too much has too many reasons to change, and the project's linter should carry a limit for it. Pricing, tax, invoicing, dunning and notification in one type means five sets of fields, five test setups and a constructor nobody can call correctly. The linters count different things: fields, public methods, lines, source statements or a maintainability index. Any of them is a prompt to ask what the class owns. A data record with many fields is a different case, and a wide but cohesive API can be justified.

**FAIL**

```text
class BillingService:        # 25 fields, 40 public methods
    price(); tax(); invoice(); dunning(); notify()
```

**PASS**

```text
class Pricing: ...
class Tax: ...
class Invoice: ...
class Dunning: ...
class Notifier: ...
# each owns its state and stays under the project's limit
```

**Counterpoint.** "Splitting a large class leaves shallow pieces that call each other." That happens when the split follows methods instead of knowledge. Move the state with the methods that use it, and keep one thin entry point for callers. If the pieces would only forward, the class is not too large. It is one concept with a wide surface, and the limit is the wrong signal. A data record is judged by its shape, not by this card.

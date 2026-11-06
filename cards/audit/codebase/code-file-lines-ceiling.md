---
id: code-file-lines-ceiling
level: codebase
tags: [maintainability, process, structure, size]
severity: discuss
status: stable
lang: core
applies_when: Auditing a repo for files that have grown past comprehension.
tool_gate: Pylint too-many-lines (C0302, max-module-lines default 1000), ESLint max-lines, or Checkstyle FileLength, with an allowlist for generated files.
note: a documented file-length limit - Pylint (default 1000), ESLint (default 300; recommendations "usually range from 100 to 500"), Checkstyle (default 2000), RuboCop (class and module length, default 100) and PMD (size and complexity caps); the numbers differ, so the Rule asks for a limit and not for 1,000
borrowed_from:
  - https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html
  - https://eslint.org/docs/latest/rules/max-lines
  - https://checkstyle.sourceforge.io/checks/sizes/filelength.html
  - https://docs.rubocop.org/rubocop/latest/cops_metrics.html
  - https://docs.pmd-code.org/latest/pmd_rules_java_design.html
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
---

**Rule.** Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.

**Why.** Huge files hide unrelated decisions, attract merge conflicts, and cannot be understood in one read. Linters ship a default for this because a file that passes it is "hard to understand" (Checkstyle). The defaults differ from 300 to 2,000 lines, so pick one and enforce it.

**FAIL**

```text
$ wc -l src/*.py | sort -n | tail -2
  4,812 src/utils.py
  3,105 src/app.py
```

**PASS**

```text
pylint: max-module-lines = 1000; no hand-written file over it; generated files listed in an allowlist.
```

**Counterpoint.** Ousterhout favours deep modules and a long file can be coherent. Splitting for its own sake adds shallow pieces. 1,000 lines is a trigger for a look, not a verdict. The fix is to separate decisions (his information-leakage and temporal-decomposition flags).

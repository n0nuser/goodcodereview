---
id: code-file-lines-ceiling
level: codebase
tags: [maintainability, process, structure, size]
severity: discuss
status: draft
lacks: evidence, backers are a dev.to summary and a blog post; no org states a file-length ceiling or the 1,000-line figure
lang: core
applies_when: Auditing a repo for files that have grown past comprehension.
tool_gate: CI check on lines per file (cloc, wc) with an allowlist.
note: 1,000-line figure is a heuristic with no source
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
---

**Rule.** Keep every hand-written source file under about 1,000 lines unless it has a listed exception, and split larger files by knowledge owned, not by execution order.

**Why.** Huge files hide unrelated decisions, attract merge conflicts, and cannot be understood in one read.

**FAIL**

```text
$ wc -l src/*.py | sort -n | tail -2
  4,812 src/utils.py
  3,105 src/app.py
```

**PASS**

```text
No hand-written file over 1,000 lines; generated files listed in an allowlist.
```

**Counterpoint.** Ousterhout favours deep modules and a long file can be coherent. Splitting for its own sake adds shallow pieces. 1,000 lines is a trigger for a look, not a verdict. The fix is to separate decisions (his information-leakage and temporal-decomposition flags).

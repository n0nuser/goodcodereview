---
id: code-file-size-ceiling
level: codebase
tags: [structure, size]
severity: discuss
status: draft
lang: core
applies_when: Auditing a repo for files that have grown past comprehension.
tool_gate: CI check on lines per file (cloc, wc) with an allowlist.
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
---

**Rule.** No hand-written source file exceeds about 1,000 lines without a listed exception; larger files are split by knowledge owned, not by execution order.

**Why.** Huge files hide unrelated decisions, attract merge conflicts and cannot be understood in one read.

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

**Counterpoint.** Ousterhout favours deep modules and a long file can be coherent; splitting for its own sake adds shallow pieces. Answer: 1,000 is a trigger for a look, not a verdict; the fix is to separate decisions (see his information-leakage and temporal-decomposition flags). The 1k figure has no source in the notes (our heuristic), hence draft.

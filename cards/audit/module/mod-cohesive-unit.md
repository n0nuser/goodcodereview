---
id: mod-cohesive-unit
level: module
tags: [architecture]
severity: discuss
status: draft
lang: core
applies_when: A module or package is large, mixes concepts, or holds a very large literal.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Keep one cohesive unit per module. Split an oversized package into subpackages, move big literals out, and inline a folder that holds one module.

**Why.** Banner comments and `# ---- section ----` markers show a module doing several jobs. Large literals bury the logic around them.

**FAIL**

```text
service.py (1800 lines): prompts, parsing, billing, formatting; with # ==== banners
pkg/only_one.py   # a folder for a single module
```

**PASS**

```text
service.py (logic), prompts.py (the big literal), billing.py ...
only_one.py       # folder inlined
```

**Counterpoint.** "Splitting scatters related code." True when the split is by layer or time rather than by concept; Ousterhout warns about temporal decomposition. Split by owned knowledge, not by when things run.

---
id: fn-bool-arg-at-callsite
level: function
tags: [maintainability, readability, api]
severity: discuss
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: core
applies_when: A call passes a literal `True` or `False` for a parameter.
tool_gate: ruff FBT
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Replace a boolean flag argument with an enum, keyword-only argument or two functions.

**Why.** `render(doc, True, False)` says nothing. A boolean also hides that a third state is coming, and when it does, every caller changes.

**FAIL**

```text
export(report, true, false)
```

**PASS**

```text
export(report, fmt=Format.CSV, header=Header.OMIT)
```

**Counterpoint.** "A keyword flag is fine and shorter." A named keyword-only flag is acceptable when it is truly binary and will stay so. The FAIL is the positional literal, which is why the severity is discuss.

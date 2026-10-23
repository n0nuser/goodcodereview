---
id: fn-no-magic-values
level: function
tags: [readability, types]
severity: should-fix
status: draft
lang: core
applies_when: A literal string or number carries meaning the reader must guess (status codes, mode names, limits).
tool_gate: none (partial: ruff PLR2004)
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
---

**Rule.** Give every meaningful literal a name: an enum member or a constant.

**Why.** Literals drift. `"canceled"` in one file and `"cancelled"` in another is a silent bug, and nobody can grep for what `3` means.

**FAIL**

```text
if resp.status == 404 or retries > 3:
    mode = "fast"
```

**PASS**

```text
if resp.status == HTTPStatus.NOT_FOUND or retries > MAX_RETRIES:
    mode = Mode.FAST
```

**Counterpoint.** "A constant used once is noise." True for self-evident values (`0`, `1`, `""`, an index into a pair). The rule is for literals whose meaning is not visible at the use site, or that appear twice. Two spellings of one concept is the failure, not the literal itself.

---
id: chg-abstraction-needs-two-callers
level: change
tags: [abstraction, layering]
severity: discuss
status: draft
lang: core
applies_when: The change extracts shared logic, adds a shared module, or moves logic into another layer.
tool_gate: none
borrowed_from:
  - https://kentcdodds.com/blog/aha-programming
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Move logic into a shared module or the owning layer only when two or more real call sites exist today; and reject an abstraction that its callers bend with growing flags.

**Why.** An abstraction guessed from one use encodes the wrong seams. Callers then add parameters and conditionals, and the "shared" code becomes harder to change than copies would have been.

**FAIL**

```python
# helper extracted for one caller, already taking behaviour flags
def format_row(r, *, legacy=False, for_csv=False, skip_total=False): ...
```

**PASS**

```python
# two callers share the same stable steps -> extract
# a third caller needs a variant -> inline back and re-split
```

**Counterpoint.** Ousterhout's red-flag list counts repetition as a smell, while Dodds and Metz prefer duplication over the wrong abstraction. They reconcile: repeated knowledge (a format, a rule) must live in one place; repeated code shape is cheap to leave until the pattern is proven. No data backs either side. The "second vs third copy" threshold is a weak heuristic.

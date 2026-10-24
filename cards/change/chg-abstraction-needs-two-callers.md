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
  - https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction
---

**Rule.** Extract shared logic only once two or more real call sites exist today.

**Why.** An abstraction guessed from one use encodes the wrong seams. Callers then bend it with flags and conditionals, and the shared code becomes harder to change than copies would have been. When that happens, inline it and re-split.

**FAIL**

```python
# helper extracted for one caller, already taking behaviour flags
def format_row(r, *, legacy=False, for_csv=False, skip_total=False): ...
```

**PASS**

```python
# two callers share the same stable steps -> extract
def render_total(items):
    return sum(i.price * i.qty for i in items)

# a third caller needs a variant -> inline back and re-split,
# do not add render_total(items, legacy=True, skip_tax=True)
```

**Counterpoint.** Ousterhout's red-flag list counts repetition as a smell, while Dodds and Metz prefer duplication over the wrong abstraction. They reconcile: repeated knowledge (a format, a rule) must live in one place, and repeated code shape is cheap to leave until the pattern is proven. Neither side has data. Dodds and Metz point to the third copy as the moment to ask. This card takes two real call sites as the earliest point to extract. See also [[mod-no-wrong-abstraction]].

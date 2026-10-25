---
id: mod-deep-modules
level: module
tags: [maintainability, design]
severity: discuss
status: draft
lacks: orgs, Ousterhout is the only backer, and Martin disagrees; needs two more orgs
lang: core
applies_when: A new class or module is introduced, or an existing interface grows.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md
---

**Rule.** Prefer a small interface that hides real work, and flag modules whose interface is nearly as complex as their implementation.

**Why.** A shallow module charges the reader the cost of learning an interface and returns nothing. The complexity moves; it does not shrink.

**FAIL**

```text
class Reader:
    def open(self); def read_line(self); def set_encoding(self, e); def close(self)
    # caller must sequence all four; same work in a function would be one call
```

**PASS**

```text
def read_lines(path, encoding="utf-8") -> list[str]: ...
```

**Counterpoint.** Ousterhout and Martin disagree. Martin favours many very small functions, and Ousterhout says that yields shallow, entangled pieces. Evidence is thin on both sides. Ask the local question: does the split help a reader here?
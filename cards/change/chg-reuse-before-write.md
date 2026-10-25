---
id: chg-reuse-before-write
level: change
tags: [maintainability, reuse, duplication]
severity: should-fix
status: draft
lacks: evidence, the backers are the kernel style guide and secondary summaries; no source describes searching for an existing helper first
lang: core
applies_when: The change adds a helper, util, type or constant.
tool_gate: Clone-detection in CI (jscpd, PMD CPD, or similar) can flag near-duplicate blocks.
note: only the kernel coding style backs "use the existing helper"; the Orosz post has no reuse check, and the Ousterhout summary and refactoring.guru are secondary and back the Why (duplication drifts), not the search; no source describes searching first
borrowed_from:
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://www.kernel.org/doc/html/latest/process/coding-style.html
  - https://refactoring.guru/smells/duplicate-code
---

**Rule.** Search the repo for an existing helper before adding a new one.

**Why.** Reviewers see only the diff, so a reimplementation of a helper a few files away looks fine in isolation. Two copies then drift and get fixed once. The author names where they searched.

**FAIL**

```python
# utils/dates.py already has parse_iso(s)
def _parse_date(s):  # new, in billing/invoice.py
    return datetime.strptime(s, "%Y-%m-%d")   # drops timezone handling
```

**PASS**

```python
from utils.dates import parse_iso
```

**Counterpoint.** "Searching costs more than writing ten lines." For tiny code that is true. Then the duplicate is tolerable and `mod-yagni` governs extraction. The cost flips once the logic holds a rule (parsing, money, auth) that must stay in one place.

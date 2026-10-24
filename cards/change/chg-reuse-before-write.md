---
id: chg-reuse-before-write
level: change
tags: [maintainability, reuse, duplication]
severity: should-fix
status: draft
lang: core
applies_when: The change adds a helper, util, type or constant.
tool_gate: Clone-detection in CI (jscpd, PMD CPD, or similar) can flag near-duplicate blocks.
borrowed_from:
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://www.kernel.org/doc/html/latest/process/coding-style.html
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

**Counterpoint.** "Searching costs more than writing ten lines." For tiny code that is true. Then the duplicate is tolerable and `chg-abstraction-needs-two-callers` governs extraction. The cost flips once the logic holds a rule (parsing, money, auth) that must stay in one place.

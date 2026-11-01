---
id: chg-reuse-before-write
level: change
tags: [maintainability, reuse, duplication]
severity: should-fix
status: stable
lang: core
applies_when: The change adds a helper, util, type or constant.
tool_gate: Clone-detection in CI (jscpd, PMD CPD, or similar) can flag near-duplicate blocks.
note: GitHub (reviewer repo search for each new helper), Cursor (explore before changing, since the agent may create a utility that exists) and Google's Gemini CLI team (review-duplication skill) back the search; the kernel style guide backs only "use the existing helper"; Ousterhout and refactoring.guru back the Why; "author names where they searched" had no source, so it left the Rule
borrowed_from:
  - https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/
  - https://cursor.com/learn/understanding-your-codebase
  - https://github.com/google-gemini/gemini-cli/blob/main/.gemini/skills/review-duplication/SKILL.md
  - https://www.kernel.org/doc/html/latest/process/coding-style.html
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://refactoring.guru/smells/duplicate-code
---

**Rule.** Do not add a helper that duplicates one already in the repo; search for it first.

**Why.** Reviewers see only the diff, so a reimplementation of a helper a few files away looks fine in isolation. Two copies then drift and get fixed once.

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

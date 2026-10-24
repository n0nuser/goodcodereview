---
id: chg-review-signal
level: change
tags: [reviewer, etiquette, signal]
severity: discuss
status: stable
lang: core
applies_when: A reviewer is deciding what to comment on.
tool_gate: Formatter, linter and type checker own style and mechanical rules.
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://slack.engineering/how-about-code-reviews/
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
---

**Rule.** Do not comment on what a tool enforces or on taste with no written rule; spend comments on a few high-conviction findings, and if there are many, talk to the author.

**Why.** Noise buries the real defects and trains authors to dismiss review. A rubber-stamp approval is just as harmful: an approval must reflect real reading.

**FAIL**

```text
27 comments: 18 whitespace and import-order, 6 "I'd write it differently",
the null dereference on line 90 never mentioned.
```

**PASS**

```text
3 comments: the null dereference, a missing test for the empty case,
one nit. Formatting left to the formatter, which CI enforces.
```

**Counterpoint.** Limiting comments risks missing issues. The cap applies to opinion, not to defects, so every real defect is still raised. The written style guide or the formatter settles style, and repeated nits mean a missing gate.

---
id: chg-review-signal
level: change
tags: [process, reviewer, etiquette, signal]
severity: discuss
status: stable
lang: core
applies_when: A reviewer is deciding what to comment on.
tool_gate: Formatter, linter and type checker own style and mechanical rules.
note: Anthropic (a vendor) backs only the tool-owned clause: its reviewer filters out findings that are only style, diagnostics or cleanup; not a counted third org and not the taste clause
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://slack.engineering/how-about-code-reviews/
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
  - https://x.com/addyosmani/status/2114604912520921136
---

**Rule.** Do not spend review comments on what a tool enforces or on minor style points; spend them on the findings that matter.

**Why.** Noise buries the real defects and trains authors to dismiss review. Prefer a few high-conviction comments, and when a first pass turns up many, talk to the author instead of posting a long list; both are common advice but have fewer than three organisations behind them, and a style point outside the written guide is the reviewer's taste. A rubber-stamp approval is just as harmful: an approval must reflect real reading.

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

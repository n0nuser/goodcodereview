---
id: chg-review-signal
level: change
tags: [reviewer, etiquette, signal]
severity: discuss
status: draft
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

**Why.** Noise buries the real defects and trains authors to dismiss review. A rubber-stamp approval is as harmful: Meta tracks "eyeball time" as a guardrail for that reason.

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

**Counterpoint.** Limiting comments risks missing issues. Answer: the cap applies to opinion, not to defects; every real defect is still raised. Sources split on style: Google says the style guide wins, Slack says leave formatting to tools. Both agree repeated nits mean a missing gate.

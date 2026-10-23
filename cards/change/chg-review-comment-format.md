---
id: chg-review-comment-format
level: change
tags: [reviewer, etiquette]
severity: discuss
status: draft
lang: core
applies_when: A reviewer writes feedback on a change.
tool_gate: none
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://slack.engineering/how-about-code-reviews/
---

**Rule.** Give each review comment one finding and a severity label (block, should-fix, nit).

**Why.** Phrase comments as a question or a fact, not a verdict on the person. Bundled or unlabelled comments leave the author unable to tell what blocks merge, and blame-shaped wording stalls the discussion.

**FAIL**

```text
"This whole function is bad, also naming, and your loop has a bug."
```

**PASS**

```text
"[block] items[i+1] reads past the end when len==1. Repro: ..."
"[nit] could this be named `retry_count`?"
```

**Counterpoint.** Labels add ceremony for tiny reviews. Answer: two labels are enough, and unlabelled comments default to non-blocking so the author is never guessing. Slack stresses people and tone over mechanics and Palantir bans absolute wording; Google's tool is "Nit:" only. Take the common core.

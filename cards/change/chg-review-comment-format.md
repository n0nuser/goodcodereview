---
id: chg-review-comment-format
level: change
tags: [process, reviewer, etiquette]
severity: discuss
status: draft
lang: core
applies_when: A reviewer writes feedback on a change.
tool_gate: none
note: a severity label on each comment is backed by Google (prefix a non-blocking comment with "Nit:"), Gergely Orosz (make clear which comments are non-blocking), Cloudflare (each review finding carries critical, warning or suggestion) and Dropbox (most review findings advisory, blocking only for confirmed gaps); one finding per comment has no three-org backing and sits in Why
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://slack.engineering/how-about-code-reviews/
  - https://blog.cloudflare.com/ai-code-review/
  - https://dropbox.tech/security/dropbox-mcp-dash-design-code-security
---

**Rule.** Label each review comment with its severity: block, should-fix, or discuss.

**Why.** Unlabelled comments leave the author unable to tell what blocks merge. Keep one finding per comment, so each label covers one thing and each thread can close on its own. Wording that blames the person stalls the discussion. Phrase comments as a question or a fact, not a verdict on the person.

**FAIL**

```text
"This whole function is bad, also naming, and your loop has a bug."
```

**PASS**

```text
"[block] items[i+1] reads past the end when len==1. Repro: ..."
"[discuss] could this be named `retry_count`?"
```

**Counterpoint.** "Labels add ceremony to a tiny review." A label is one word, and it saves a round trip in which the author asks whether a comment blocks the merge. A team that marks only its nits still leaves the author to guess about every other comment, so label those too.

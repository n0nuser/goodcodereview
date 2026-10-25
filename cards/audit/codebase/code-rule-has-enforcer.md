---
id: code-rule-has-enforcer
level: codebase
tags: [maintainability, tooling, conventions]
severity: should-fix
status: stable
lang: core
applies_when: Auditing a repo's instruction files, review history or comments that state a rule.
tool_gate: The enforcer itself: a type, a lint rule or a CI check.
note: Spotify, Stripe and Cabify back the Rule without cursor/plugins
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/rubric.md
  - https://engineering.atspotify.com/2026/9/portal-by-spotify-cut-my-claude-code-token-usage-by-90
  - https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint
  - https://stripe.dev/blog/formatting-an-entire-25-million-line-codebase-overnight-the-rubyfmt-story
  - https://stripe.dev/blog/sorbet-stripes-type-checker-for-ruby
  - https://tech.cabify.com/blog/engineering/cabify-container-certification
---

**Rule.** Back each rule that a type, lint or CI check could enforce with that check, not with a line in an instruction file or a repeated review comment.

**Why.** A rule that relies on memory gets broken, and reviewers then repeat the same correction. An instruction file is advisory: a person or an agent can skip it. A lint message that names the fix teaches it at the moment of the mistake. A "do not remove" code comment has the same weakness as an instruction file line.

**FAIL**

```text
CONTRIBUTING.md: "never call requests.get without a timeout"   (no lint rule)
Review history: the same comment on 6 PRs
```

**PASS**

```text
pyproject.toml: [tool.ruff.lint] select = ["S113"]   # request-without-timeout, run in CI
```

**Counterpoint.** "Not every rule is checkable." Right, and judgement rules stay as prose. The FAIL is a checkable rule with no check. See [[code-ci-gates]] for where checks run, and [[chg-review-signal]] for what reviewers stop commenting on once a tool owns it.

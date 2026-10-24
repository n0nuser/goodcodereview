---
id: code-rule-has-enforcer
level: codebase
tags: [maintainability, tooling, conventions]
severity: should-fix
status: draft
lang: core
applies_when: Auditing a repo's instruction files, review history or comments that state a rule.
tool_gate: The enforcer itself: a type, a lint rule or a CI check.
note: one vendor's engineering guidance (opinion), from pstack correct, principle-encode-lessons-in-structure and no-comments
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-encode-lessons-in-structure/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/rubric.md
---

**Rule.** Back each rule that a type, lint or CI check could enforce with that check, rather than with an instruction file line, a review comment or a "do not remove" comment.

**Why.** A rule that relies on memory gets broken, and reviewers then repeat the same correction. A lint message that names the function to use teaches the fix at the moment of the mistake.

**FAIL**

```text
CONTRIBUTING.md: "never call requests.get without a timeout"   (no lint rule)
Review history: the same comment on 6 PRs
```

**PASS**

```text
ruff flake8-bandit S113 enabled; the message says "pass timeout="
```

**Counterpoint.** "Not every rule is checkable." Right, and judgement rules stay as prose. The FAIL is a checkable rule with no check. See [[code-ci-gates]] for where checks run.

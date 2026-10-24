---
id: chg-no-silenced-diagnostics
level: change
tags: [correctness, maintainability, process, errors, lint, ci]
severity: should-fix
status: draft
lang: core
applies_when: The diff adds a suppression (lint ignore, type ignore, skipped test, swallowed error) or deletes a failing check.
tool_gate: Linter rule that requires a reason and ticket on each suppression.
note: extends Palantir (TODO without issue, red checks) and Go (discarded errors) to suppressions
borrowed_from:
  - https://go.dev/wiki/CodeReviewComments
  - https://blog.palantir.com/code-review-best-practices-19e02780015f
  - https://github.com/cursor/plugins/blob/main/pstack/skills/correct/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/no-comments/SKILL.md
---

**Rule.** Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.

**Why.** Silencing a diagnostic hides the problem it reports and removes the safety net for the next author.

**FAIL**

```python
x = load(cfg)  # type: ignore
try: sync()
except Exception: pass
@pytest.mark.skip   # flaky
```

**PASS**

```python
x = load(cfg)  # type: ignore[arg-type]  # lib stub wrong, TICKET-42
try: sync()
except SyncTimeout as e: log.warning("sync timeout", exc_info=e); retry()
```

**Counterpoint.** Sometimes a warning is a false positive. Then suppress narrowly with a reason and an expiry date, which keeps the gate useful. A suppression of a rule that guards correctness or safety should be removed, not documented. Palantir's list covers TODOs without issue references and merging with checks red. The Go list covers discarded errors. This card extends both to suppressions.

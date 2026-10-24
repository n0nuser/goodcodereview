---
id: code-scoped-validation-loop
level: codebase
tags: [testing, onboarding]
severity: discuss
status: draft
lang: core
applies_when: Auditing how a contributor checks a small change.
tool_gate: A documented command that runs tests and lint for one path or package.
note: one vendor's engineering guidance (opinion), from agent-compatibility validation-review
borrowed_from:
  - https://github.com/cursor/plugins
---

**Rule.** Document a command that checks one package or path, with readable output, so a small change does not need the full-repo run.

**Why.** If the only check takes twenty minutes or prints thousands of lines, people skip it and push to CI, and agents cannot tell which failure is theirs.

**FAIL**

```text
CONTRIBUTING.md: "run `make test` (all 14,000 tests, ~25 min)"
```

**PASS**

```text
pytest tests/billing -q        # about 20 s
ruff check src/billing
```

**Counterpoint.** "CI runs everything anyway." CI is the last check, not the loop. A scoped command lets the author find a failure in seconds instead of after a push.

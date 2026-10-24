---
id: code-documented-setup-runs
level: codebase
tags: [docs, onboarding]
severity: should-fix
status: draft
lang: core
applies_when: Auditing a repo's README or contribution guide.
tool_gate: CI job that runs the documented setup on a clean checkout.
note: one vendor's engineering guidance (opinion), from agent-compatibility docs-reliability-review
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/agent-compatibility/agents/docs-reliability-review.md
---

**Rule.** Make every setup, build and run command in the README or contribution guide succeed on a clean checkout.

**Why.** A stale step costs each new contributor and each agent the same time, and they cannot tell a doc error from their own mistake.

**FAIL**

```text
README: `make dev`    ->  make: *** No rule to make target 'dev'
```

**PASS**

```text
CI job: fresh clone, run the README's commands in order, fail on any non-zero exit
```

**Counterpoint.** "Setup depends on the machine." Document the prerequisites, and run the commands in a clean container to prove them. Judge a miss by the damage it causes, not by its existence.

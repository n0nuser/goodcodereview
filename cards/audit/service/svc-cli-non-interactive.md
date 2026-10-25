---
id: svc-cli-non-interactive
level: service
tags: [maintainability, process, cli, automation]
severity: should-fix
status: draft
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs
lang: core
applies_when: The code ships a command-line tool that scripts or agents may run.
tool_gate: CLI test that runs every command with stdin closed.
note: one vendor's engineering guidance (opinion), from cli-for-agent skills/cli-for-agents (the id was proposed as mod-cli-non-interactive; a CLI is a process boundary, so service level)
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/cli-for-agent/skills/cli-for-agents/SKILL.md
---

**Rule.** Give every input a flag, use a prompt only as a fallback, and exit at once with an example call when a required flag is missing.

**Why.** A script or an agent has no one to answer a prompt, so the command hangs until a timeout kills it. A failure with a usable example lets the caller fix the call in one step.

**FAIL**

```text
$ deploy
Choose environment: _          # waits on stdin forever in CI
```

**PASS**

```text
$ deploy
error: --env is required.  Example: deploy --env staging --yes
```

**Counterpoint.** "Prompts are friendlier for people." Keep them, but only when stdin is a terminal and a flag can always replace them.

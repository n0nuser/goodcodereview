---
id: svc-cli-destructive-dry-run
level: service
tags: [reliability, maintainability, cli, safety]
severity: should-fix
status: draft
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs
lang: core
applies_when: A command-line tool has a command that deletes, overwrites or sends something.
tool_gate: CLI test that runs the command with the preview flag and checks nothing changed.
note: one vendor's engineering guidance (opinion), from cli-for-agent skills/cli-for-agents (the id was proposed as mod-cli-destructive-dry-run; a CLI is a process boundary, so service level)
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/cli-for-agent/skills/cli-for-agents/SKILL.md
---

**Rule.** Give a destructive command a preview flag that changes nothing and a flag that skips the confirmation prompt.

**Why.** Without a preview, the first run is the real one. Without a bypass, a script cannot run the command at all, so people write wrappers that pipe "yes" into it.

**FAIL**

```text
$ prune-backups
Delete 41 backups? [y/N]       # no --dry-run, no --yes
```

**PASS**

```text
$ prune-backups --dry-run      # lists the 41 backups, deletes none
$ prune-backups --yes          # deletes without asking
```

**Counterpoint.** "A bypass flag invites accidents." The prompt stays the default for people, and the flag has to be typed on purpose. Pair it with [[svc-cli-non-interactive]].

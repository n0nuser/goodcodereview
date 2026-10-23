---
id: fn-comments-survive-context
level: function
tags: [docs]
severity: should-fix
status: draft
lang: core
applies_when: A comment or TODO refers to a ticket, a PR, a sprint or the present moment.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Write comments that remain true without outside context: no "see the PR", "currently", "not yet", ticket ids or codenames.

**Why.** The PR vanishes from memory and the "currently" never gets updated. Comments with expired context are lies by the next release.

**FAIL**

```text
# TODO(JIRA-4412): handle the legacy case for now
```

**PASS**

```text
# TODO: drop this branch once every client sends v2 payloads
```

**Counterpoint.** "Ticket links help traceability." Traceability belongs in the commit message and the PR, which are tied to the change. A removal condition in the TODO is what a later reader can act on.

---
id: chg-bot-approval-not-human
level: change
tags: [process, review, security, agents]
severity: should-fix
status: draft
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that bar bot or agent approvals from a required human review
lang: core
applies_when: Branch protection or policy requires a human approval and a bot or agent can also approve.
tool_gate: Branch protection that counts approvals from human code owners only.
note: Anthropic only (a vendor, in a post about its own Claude Code team); "Bot approvals cannot be used to satisfy a required approval" and "Agent approvals don't count as human approvals"
borrowed_from:
  - https://x.com/addyosmani/status/2114604912520921136
---

**Rule.** Do not let a bot or agent approval satisfy a required human approval.

**Why.** An automated reviewer can clear a low-risk change, but a required approval exists so that a person answers for the change. If a bot's approval counts, the gate passes with nobody accountable.

**FAIL**

```text
Branch protection: 1 approval required, any account.
review-bot[bot] approves the auth change. The PR merges with no person having read it.
```

**PASS**

```text
Branch protection: 1 approval required from a code owner, and bot accounts are not code owners.
review-bot[bot] comments; a named engineer approves.
```

**Counterpoint.** "The bot catches more than a tired human." It can still comment and block, and a low-risk path may need no human at all. The rule applies only where policy requires a person, so the bot cannot stand in for one there.

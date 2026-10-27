---
id: chg-review-rigour-by-risk
level: change
tags: [process, review, risk]
severity: should-fix
status: draft
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that set review depth by what the change touches
lang: core
applies_when: A repository sets how many approvals or how deep a review a change needs.
tool_gate: CODEOWNERS plus branch-protection rules keyed to paths; a risk label set by a classifier or by path.
note: Anthropic only (a vendor, in a post about its own Claude Code team); "The tier is determined by the change, not the author"
borrowed_from:
  - https://x.com/addyosmani/status/2114604912520921136
---

**Rule.** Set the review tier from what the change touches, such as auth, billing, migrations or CI, and not from who wrote it.

**Why.** An author's seniority says little about the blast radius of a diff. A tier keyed to the author lets a risky change from a trusted person skip the scrutiny it needs, and sends a docs fix from a newcomer through the same slow path as a billing change.

**FAIL**

```text
Policy: "senior engineers self-merge, juniors need two approvals."
A senior self-merges a change to the payment retry logic.
```

**PASS**

```text
Policy: paths under billing/ and .github/workflows/ need a code-owner approval, whoever the author is.
A docs-only change merges with one approval from anyone.
```

**Counterpoint.** "Trust in the author is real information." It is, and it can relax the tier for routine paths, but it must not lower the floor for high-risk paths. Start strict and relax as the revert record shows it is safe.

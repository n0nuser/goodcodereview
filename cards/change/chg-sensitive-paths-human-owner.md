---
id: chg-sensitive-paths-human-owner
level: change
tags: [security, process, review]
severity: should-fix
status: draft
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that name human owners for auth, billing, CI and release paths
lang: core
applies_when: The change touches code or config for auth, billing, CI or release workflows.
tool_gate: CODEOWNERS entries for these paths plus branch protection that requires code-owner review.
note: Anthropic only (a vendor, in a post about its own Claude Code team); "Designate humans as the approvers for code and policies controlling auth, billing, CI, and release workflows"
borrowed_from:
  - https://x.com/addyosmani/status/2114604912520921136
---

**Rule.** Name a human owner in CODEOWNERS for auth, billing, CI and release paths, and require that owner's approval.

**Why.** These paths decide who can act, who pays, and what ships. A change to a CI workflow can widen its own permissions, so a reviewer who is not an owner of the path can approve what they cannot judge.

**FAIL**

```text
# CODEOWNERS
*    @org/everyone
(no entry for .github/workflows/, billing/ or auth/)
```

**PASS**

```text
# CODEOWNERS
.github/workflows/   @org/release-owners
billing/             @org/payments-team
auth/                @org/security-team
```

**Counterpoint.** "Owners become a bottleneck." Keep the list to the few paths where a mistake is costly, and give each more than one named owner. A wide default owner list is the same as having none.

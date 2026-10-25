---
id: chg-approval-tied-to-patch
level: change
tags: [process, review]
severity: should-fix
status: draft
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs
lang: core
applies_when: A review approval or verification result exists and the branch has been pushed or rebased since.
tool_gate: Branch protection that dismisses stale approvals on new commits.
note: one vendor's engineering guidance (opinion), from poteto-mode/playbooks/shipping.md; patch-id comparison is the source's method
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/playbooks/shipping.md
---

**Rule.** Treat an approval or verification verdict as current only if no push since then changed non-test content, and compare patch ids after a rebase.

**Why.** A verdict covers one patch. After a push or rebase the reviewer approved code that no longer exists.

**FAIL**

```text
Approved at abc123. Two later pushes change src/auth.py. Merged on the old approval.
```

**PASS**

```text
Approved at abc123. Rebase onto main: `git patch-id` matches for every changed file, so the approval stands.
Push that edits src/auth.py: approval dismissed, re-requested.
```

**Counterpoint.** "Re-approving after every push is noisy." Only a change to non-test content voids the verdict, and a rebase that keeps the patch id does not. Branch protection can enforce this without human effort.

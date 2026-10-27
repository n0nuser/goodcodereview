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

**Rule.** Treat an approval or verification verdict as current only if the patch is unchanged: compare `git patch-id` at the verdict commit with the current head. If the patches differ only in tests, docs, or lint config, the verdict can stand when the built output is the same; any other difference needs a fresh check.

**Why.** A verdict covers one patch. After a push or rebase the reviewer approved code that no longer exists.

**FAIL**

```text
Approved at abc123. Two later pushes change src/auth.py. Merged on the old approval.
```

**PASS**

```text
Approved at abc123. Rebase onto main: `git patch-id` of the diff at abc123 equals the one at the new head, so the approval stands.
Push that edits src/auth.py: patch ids differ, approval dismissed, re-requested.
Push that only edits a README: approval stands once the build output is shown to be the same.
```

**Counterpoint.** "Re-approving after every push is noisy." A rebase that keeps the patch id does not void the verdict, and neither does a change to tests, docs, or lint config that leaves the built output the same. Branch protection can enforce this without human effort.

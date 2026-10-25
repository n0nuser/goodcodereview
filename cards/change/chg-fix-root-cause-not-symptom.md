---
id: chg-fix-root-cause-not-symptom
level: change
tags: [correctness, testing, bugfix, verification]
severity: block
status: draft
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs
lang: core
applies_when: A change fixes a bug, a failing test, or an incident.
tool_gate: Lint rules for `as any`, `ts-ignore`, `.skip` and empty `catch`.
note: one vendor's engineering guidance (opinion), from principle-fix-root-causes/SKILL.md; the symptom-fix list comes from several of its skills
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-fix-root-causes/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/interrogate/references/rubric.md
  - https://github.com/cursor/plugins/blob/main/dyl-stack/skills/dyl-mode/SKILL.md
---

**Rule.** In a bug fix, state the cause you saw in evidence, and reject a guard, retry, sleep, longer timeout, swallowed error, cast, skipped or weakened test, or special case for the failing input that the cause does not justify.

**Why.** Each of these hides the first wrong decision and leaves the bad state to surface somewhere else. The next caller hits the same fault, and the fix now needs a comment to explain why it works.

**FAIL**

```text
Bug: report total is None for some users.
Diff: if total is None: total = 0     # no cause given
```

**PASS**

```text
Cause: the loader skips users with no orders (query output attached), so total is never set.
Diff: the loader returns an empty list for those users; the other two callers of the loader are checked.
```

**Counterpoint.** "A guard is the quick safe fix during an outage." Mitigate first if you must, but label it a mitigation and open the root-cause fix. A guard that ships as the fix is the FAIL.

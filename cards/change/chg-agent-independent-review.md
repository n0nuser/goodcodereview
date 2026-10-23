---
id: chg-agent-independent-review
level: change
tags: [agents, review, process]
severity: should-fix
status: draft
lang: core
applies_when: An agent wrote the change and an agent (or the same session) is asked to review it.
tool_gate: none
borrowed_from:
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
---

**Rule.** Self-review by the writing session does not count as review; a person or a fresh-context reviewer with the spec, not the author's reasoning, signs off.

**Why.** The same context repeats the same blind spots and assumptions. Approvals without real reading are rubber-stamps.

**FAIL**

```text
Session writes the diff, then "reviews" it: "no issues found". Merged.
```

**PASS**

```text
Fresh reviewer given spec + diff + test output, runs the branch, files findings.
A human who can explain the change approves.
```

**Counterpoint.** A same-session pass still catches typos and leftovers; keep it as the author's self-review step, just not as the gate. Evidence for this card is thin: sources cover disclosure and rubber-stamp guardrails, not agent-specific studies.

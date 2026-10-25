---
id: chg-agent-independent-review
level: change
tags: [process, agents, review]
severity: should-fix
status: stable
lang: core
applies_when: An agent wrote the change, or most of it.
tool_gate: Branch protection that requires an approving review from a person before merge.
note: Stripe, Uber, Spotify and Kubernetes back a person's sign-off on agent-written changes; no source backs a fresh agent as the sign-off
borrowed_from:
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
  - https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
  - https://www.uber.com/blog/efficient-software-factory/
  - https://engineering.atspotify.com/2026/4/background-coding-agents-dataset-migrations-honk-part-4
---

**Rule.** Get sign-off from a person on an agent-written change; a review by the session that wrote it does not count.

**Why.** The same context repeats the same blind spots and assumptions. An approval without real reading is a rubber stamp. A reviewer agent in a fresh context, given the spec and the diff but not the author's reasoning, catches more than a self-review and makes the person's review faster, but it does not replace it. The person who submits the change must also be able to explain each hunk.

**FAIL**

```text
Session writes the diff, then "reviews" it: "no issues found". Auto-merged.
```

**PASS**

```text
Fresh reviewer agent given spec + diff + test output files findings; the author fixes them.
A person who can explain the change reads it and approves.
```

**Counterpoint.** "A fresh reviewer agent finds more than a tired person." It often does, so run it first. But the person carries the accountability and knows context the spec leaves out. A same-session pass still catches typos and leftovers: keep it as the author's self-review step ([[chg-author-hygiene]]), not as the gate.

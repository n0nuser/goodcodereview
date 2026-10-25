---
id: chg-agent-independent-review
level: change
tags: [process, agents, review]
severity: should-fix
status: draft
lacks: orgs, a person's sign-off has Stripe and Dropbox; the fresh-context reviewer option has 0 orgs; needs one more firm org or that option cut
lang: core
applies_when: An agent wrote the change, and an agent or the same session is asked to review it.
tool_gate: none
note: a person's sign-off on agent-written changes has Stripe and Dropbox (firm) and Uber (maintenance tasks only); Kubernetes covers AI-assisted PRs with a human author; Spotify auto-merges some agent PRs; nobody backs a fresh agent as the sign-off (Cloudflare's separate-session AI reviewers review engineer-written code)
borrowed_from:
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/
  - https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
  - https://www.uber.com/blog/efficient-software-factory/
  - https://dropbox.tech/culture/beyond-code-generation-rethinking-engineering-productivity-in-the-age-of-ai-agents
---

**Rule.** Get sign-off from a person or a fresh-context reviewer who has the spec but not the author's reasoning; self-review by the writing session does not count.

**Why.** The same context repeats the same blind spots and assumptions. An approval without real reading is a rubber stamp. The person who submits the change must also be able to explain each hunk.

**FAIL**

```text
Session writes the diff, then "reviews" it: "no issues found". Merged.
```

**PASS**

```text
Fresh reviewer given spec + diff + test output, runs the branch, files findings.
A human who can explain the change approves.
```

**Counterpoint.** A same-session pass still catches typos and leftovers. Keep it as the author's self-review step, not as the gate. Meta tracks "eyeball time" as a guardrail against rubber-stamping, the failure this card targets.

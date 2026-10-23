---
id: code-adr
level: codebase
tags: [documentation, decisions]
severity: discuss
status: draft
lang: core
applies_when: Auditing whether the reasons behind significant design choices are recorded.
tool_gate: none
borrowed_from:
  - https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
---

**Rule.** Significant choices (datastore, framework, deviation from a pattern) have a short written record stating the problem, alternatives considered and cost of the chosen option.

**Why.** Without it, the next reader reverses a decision blindly or cargo-cults it. Listing only the chosen design's flaws is not a trade-off analysis.

**FAIL**

```text
Repo uses Kafka for one 10-msg/day job. No record why; nobody dares remove it.
```

**PASS**

```text
docs/adr/0007-queue.md: problem, 2 alternatives, chosen, consequences, status.
```

**Counterpoint.** ADRs rot and become paperwork. Answer: keep each to a page, write them only for hard-to-reverse choices, and mark superseded ones. The notes support stating the problem and alternatives; the ADR format itself has no source in them, so this card is draft.

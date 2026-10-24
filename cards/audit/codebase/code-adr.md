---
id: code-adr
level: codebase
tags: [maintainability, process, documentation, decisions]
severity: discuss
status: draft
lang: core
applies_when: Auditing whether the reasons behind significant design choices are recorded.
tool_gate: none
note: ADR format unsourced; problem-and-alternatives practice from Hickey and Orosz
borrowed_from:
  - https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
---

**Rule.** Keep a short written record for significant choices (datastore, framework, deviation from a pattern) that states the problem, the alternatives considered, and the cost of the chosen option.

**Why.** Without a record, the next reader reverses a decision blindly or cargo-cults it. Listing only the chosen design's flaws is not a trade-off analysis.

**FAIL**

```text
Repo uses Kafka for one 10-msg/day job. No record why; nobody dares remove it.
```

**PASS**

```text
docs/adr/0007-queue.md: problem, 2 alternatives, chosen, consequences, status.
```

**Counterpoint.** ADRs rot and become paperwork. Keep each to a page, write them only for hard-to-reverse choices, and mark superseded ones.

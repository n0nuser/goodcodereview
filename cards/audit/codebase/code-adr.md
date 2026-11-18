---
id: code-adr
level: codebase
tags: [maintainability, process, documentation, decisions]
severity: discuss
status: stable
lang: core
applies_when: Auditing whether the reasons behind significant design choices are recorded.
tool_gate: none
borrowed_from:
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html
  - https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record
  - https://cloud.google.com/architecture/architecture-decision-records
  - https://www.gov.uk/government/publications/architectural-decision-record-framework/architectural-decision-record-framework
  - https://engineering.atspotify.com/2020/04/when-should-i-write-an-architecture-decision-record
  - https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions
  - https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md
  - https://github.com/rust-lang/rfcs/blob/master/0000-template.md
  - https://peps.python.org/pep-0012/
  - https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md
  - https://rfd.shared.oxide.computer/rfd/0001
---

**Rule.** Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, the options ruled out, and its consequences.

**Why.** Without a record, the next reader reverses a decision blindly or cargo-cults it. A record that weighs only the chosen design, its strengths or its flaws, is not a trade-off analysis, so say why each ruled-out option lost. Give each record a status (proposed, accepted, superseded). Do not edit an accepted record: write a new one that supersedes it and keep the old one. If review finds an undocumented decision, write its record then.

**FAIL**

```text
Repo uses Kafka for one 10-msg/day job. No record why; nobody dares remove it.
```

**PASS**

```text
docs/adr/0007-queue.md: context, decision, consequences, status, and the 2 options ruled out.
```

**Counterpoint.** ADRs rot and become paperwork. Keep each to a page, write them only for hard-to-reverse choices, and mark superseded ones.

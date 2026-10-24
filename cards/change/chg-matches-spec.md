---
id: chg-matches-spec
level: change
tags: [process, scope, requirements]
severity: block
status: draft
lang: core
applies_when: The change links a ticket, spec or issue.
tool_gate: none
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md
---

**Rule.** Trace every behaviour change in the diff to the stated requirement, and flag missing requirements and any change nobody asked for.

**Why.** Unrequested changes carry unreviewed risk and surprise the owners. As a heuristic, a misunderstood requirement does more damage than a typo, so check the diff against the ask first.

**FAIL**

```text
Ticket: "return 404 for deleted users".
Diff also changes pagination defaults and adds a retry wrapper.
```

**PASS**

```text
Diff only changes the lookup path and its tests; the pagination idea
is filed as a separate ticket.
```

**Counterpoint.** "Obvious small fixes while I'm there are free." Sometimes, and Google wants reviewers to look at surrounding code too. Tiny same-file hygiene is fine if the description names it. Behaviour changes are not.

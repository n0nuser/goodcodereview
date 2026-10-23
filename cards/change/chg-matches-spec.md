---
id: chg-matches-spec
level: change
tags: [scope, requirements]
severity: block
status: draft
lang: core
applies_when: The change links a ticket, spec or issue.
tool_gate: none
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md
---

**Rule.** Every behaviour change in the diff traces to the stated requirement; flag missing requirements and any change nobody asked for.

**Why.** Unrequested changes carry unreviewed risk and surprise the owners. Misunderstood problems, not typos, are the source of the serious defects.

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

**Counterpoint.** "Obvious small fixes while I'm there are free." Sometimes, and Google wants reviewers to look at surrounding code too. Answer: tiny same-file hygiene is fine if named in the description; behaviour changes are not.

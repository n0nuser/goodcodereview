---
id: svc-timeouts            # level prefix + short name, unique
level: service              # change | function | module | service | system | codebase | production | incident
tags: [reliability, io]     # at least one concern: correctness security performance reliability compatibility testing maintainability accessibility usability observability process; then any topic tags
severity: block             # block | should-fix | discuss
status: draft               # draft | stable
lang: core                  # core | python | ...
applies_when: The code calls anything over a network or process boundary.
tool_gate: none             # what a linter/CI could own; if set, the review comment is "add the gate"
borrowed_from:
  - https://example.com/source
---

**Rule.** One line, imperative.

**Why.** The failure this prevents.

**FAIL**

```text
code or config that breaks the rule
```

**PASS**

```text
the fix
```

**Counterpoint.** The strongest objection, answered.

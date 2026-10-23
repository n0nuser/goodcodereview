---
id: mod-inject-boundary-collaborators
level: module
tags: [testing, design]
severity: should-fix
status: draft
lang: core
applies_when: A class uses a database, HTTP, cloud or clock collaborator.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Inject boundary collaborators through the constructor. Do not construct them inside or reach for a global.

**Why.** Hard-wired collaborators force tests to patch module internals and tie the class to one environment.

**FAIL**

```text
class Billing:
    def charge(self, o): return StripeClient(KEY).charge(o)
```

**PASS**

```text
class Billing:
    def __init__(self, gateway): self._gateway = gateway
```

**Counterpoint.** "Injection everywhere is enterprise bloat." Inject the boundary (DB, HTTP, cloud, clock) only. Internal collaborators stay plain and real in tests.

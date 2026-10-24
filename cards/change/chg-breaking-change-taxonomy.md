---
id: chg-breaking-change-taxonomy
level: change
tags: [compatibility, api]
severity: block
status: stable
lang: core
applies_when: The change alters anything a caller can observe, documented or not.
tool_gate: Contract tests and API-diff tooling.
borrowed_from:
  - https://www.hyrumslaw.com/
  - https://michaelfeathers.silvrback.com/characterization-testing
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
---

**Rule.** Treat any observable difference in signature, return shape, error type, ordering, timing, defaults, or side effects as breaking until a consumer check says otherwise.

**Why.** With enough users, every observable behaviour is depended on, so "undocumented" does not mean "safe to change".

**FAIL**

```text
list_orders() now returns newest-first (was insertion order).
PR says "no API change"; docs never promised an order.
```

**PASS**

```text
PR states: "ordering changes, known consumers A and B checked,
flag orders_newest_first defaults off for one release".
```

**Counterpoint.** Treating everything as breaking freezes the code. Weigh each change by known consumers and blast radius, and use a staged rollout instead of a ban. Optional parameters with defaults are the safe way to add.

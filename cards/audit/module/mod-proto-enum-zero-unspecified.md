---
id: mod-proto-enum-zero-unspecified
level: module
tags: [api, protobuf, compatibility]
severity: should-fix
status: draft
lang: core
applies_when: A `.proto` file defines an enum.
tool_gate: Protobuf linter (`buf lint`, ENUM_ZERO_VALUE_SUFFIX).
borrowed_from:
  - https://protobuf.dev/best-practices/dos-donts/
---

**Rule.** Give every protobuf enum a zero value named `<ENUM>_UNSPECIFIED` with no real meaning.

**Why.** A reader that sees an unset or unknown field gets zero. If zero means a real state, such as `PAID`, a missing field reads as a payment.

**FAIL**

```proto
enum Status {
  PAID = 0;
  REFUNDED = 1;
}
```

**PASS**

```proto
enum Status {
  STATUS_UNSPECIFIED = 0;
  PAID = 1;
  REFUNDED = 2;
}
```

**Counterpoint.** "Zero as the common default saves a field on the wire." The saving is a byte on a field already at its most common value, and the cost is a silent wrong state. Published enums keep their numbers, so the fix for an existing enum is a new unspecified name only if no value has to be renumbered.

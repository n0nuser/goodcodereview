---
id: chg-proto-reserve-removed-fields
level: change
tags: [api, protobuf, compatibility]
severity: block
status: draft
lang: core
applies_when: The diff deletes a field or enum value from a `.proto` message or enum.
tool_gate: `buf breaking` or an equivalent descriptor diff in CI.
borrowed_from:
  - https://protobuf.dev/best-practices/dos-donts/
---

**Rule.** When you delete a protobuf field or enum value, add `reserved` for its number and name in the same change, and never reuse a number.

**Why.** Old data and old clients still carry the number. A new field that takes it is read as the old type, and the failure is silent corruption, not an error.

**FAIL**

```proto
message Order {
-  string coupon = 4;
+  int32 loyalty_points = 4;   // number 4 reused
}
```

**PASS**

```proto
message Order {
  reserved 4;
  reserved "coupon";
  int32 loyalty_points = 5;
}
```

**Counterpoint.** "Nobody sends field 4 any more." Stored messages, queued messages and a client on last month's build do. Reserving costs one line and cannot be undone by accident.

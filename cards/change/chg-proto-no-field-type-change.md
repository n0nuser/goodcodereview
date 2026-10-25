---
id: chg-proto-no-field-type-change
level: change
tags: [compatibility, api, protobuf]
severity: block
status: draft
lacks: orgs, "no field type change" has Google only; Uber and Cabify back renumbering and the buf breaking gate instead
lang: core
applies_when: The diff changes an existing field's type, default, label or name in a `.proto` file.
tool_gate: `buf breaking` with the wire and JSON rule sets.
borrowed_from:
  - https://protobuf.dev/best-practices/dos-donts/
---

**Rule.** Never change the type of a protobuf field, switch it between repeated and scalar, or rename it while any consumer reads JSON or text format; add a new field instead.

**Why.** The wire format carries numbers and types, not names, so a type change is read as garbage by anything not yet redeployed. The JSON and text formats carry names, so a rename breaks those readers.

**FAIL**

```proto
message Invoice {
-  int32 amount = 2;
+  string amount = 2;
}
```

**PASS**

```proto
message Invoice {
  int32 amount = 2 [deprecated = true];
  string amount_decimal = 3;
}
```

**Counterpoint.** "Both ends deploy together." A rolling deploy runs both versions at once, and stored data does not redeploy. If the message never leaves one binary, mark the card N/A.

---
id: svc-api-no-internal-fields
level: service
tags: [api, security, contracts]
severity: block
status: draft
note: protobuf.dev gives the separate-messages rule for RPC versus storage; applying it to REST responses is inference
lang: core
applies_when: A handler builds a response body from a database row, entity, ORM model or internal message.
tool_gate: Response-schema test that lists the allowed fields and fails on extras.
borrowed_from:
  - https://protobuf.dev/best-practices/dos-donts/
---

**Rule.** Build every response from an explicit response type that names the exposed fields, never by serialising a stored or internal object.

**Why.** Every column you add later is published automatically, including password hashes, internal ids, tenant flags and soft-delete markers. Callers then depend on them, and removing one is a breaking change.

**FAIL**

```text
return jsonify(order_row._asdict())   # also sends cost_basis, internal_note, tenant_shard
```

**PASS**

```text
return OrderResponse(id=row.id, status=row.status, total_cents=row.total_cents).model_dump()
```

**Counterpoint.** "Mapping is boilerplate." It is a few lines per type, and it is the contract. Generating the type from the response schema removes the repetition. For an internal admin API with the same owner, the rule still protects secrets.

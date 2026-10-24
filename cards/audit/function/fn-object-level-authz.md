---
id: fn-object-level-authz
level: function
tags: [security, authz]
severity: block
status: draft
lang: core
applies_when: A handler loads, changes or deletes a record by an ID that comes from the request.
tool_gate: Authorization tests that call each endpoint as a second user; no static gate catches a missing check.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  - https://api-security.owasp.org/editions/2023/en/0xa1-broken-object-level-authorization
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control
---

**Rule.** Check that the caller may act on the specific record before returning or changing it.

**Why.** A login proves who the caller is, not which records they own. Without a per-object check, changing `id=41` to `id=42` reads or edits another user's data (IDOR, called BOLA in the API Top 10). Random IDs only hide the problem.

**FAIL**

```text
order = db.get(Order, request.args["id"])     # any logged-in user, any order
return order.to_json()
```

**PASS**

```text
order = db.get(Order, request.args["id"])
if order is None or order.owner_id != user.id: raise NotFound()   # same error for both
return order.to_json()
```

**Counterpoint.** "The IDs are UUIDs, nobody can guess them." A UUID leaks through logs, links and shared screenshots, and it is not an access check. Keep it as a second layer. Scope the query itself (`WHERE owner_id = :me`) so the check cannot be forgotten on the next endpoint.

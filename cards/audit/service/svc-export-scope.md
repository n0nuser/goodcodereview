---
id: svc-export-scope
level: service
tags: [security, data, multi-tenant]
severity: block
status: stable
lang: core
applies_when: An endpoint or job produces a file, archive or stream of many records.
context: [data]
tool_gate: A test that exports as a second tenant and asserts the other tenant's rows are absent.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
  - https://confluence.atlassian.com/display/CONF719/Export+Content+to+Word,+PDF,+HTML+and+XML
  - https://learn.microsoft.com/en-us/power-bi/visuals/power-bi-visualization-export-data
  - https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data
  - https://cloud.google.com/architecture/dr-scenarios-planning-guide
---

**Rule.** Scope an export to what the requesting principal may read.

**Why.** An export is a read that returns many rows at once. The per-object check on the detail page never runs, so a `SELECT *` with no tenant or access predicate hands the caller the table. Apply the same filter the list endpoint uses, including any role or ownership predicate and not only the tenant, and apply it inside the export query rather than on rows already fetched. OWASP's examples put the tenant scope in the query itself. Test it with two tenants. A restore asks the same question in reverse: a shared backup holds several tenants and old memberships, so restore one tenant into a separate resource and re-apply current access and retention before anyone can read it. A recovered environment also needs the production controls, not the ones it had when the backup was taken.

**FAIL**

```text
GET /export  ->  SELECT * FROM orders; streamed to any authenticated caller
```

**PASS**

```python
def export(user):
    rows = session.query(Order).filter(Order.tenant_id == user.tenant_id)
    return csv_stream(rows)
```

**Counterpoint.** "Some exports deliberately include everything." Some products ship an admin XML export that includes pages the exporter cannot view. That path is an administrative backup, so gate it on an admin permission and audit it. The user-facing exports in the same products contain only what the exporter can view, which is the rule here. Check which export path the change touches before calling a missing filter a bug.

---
id: svc-tenant-scope-in-data-layer
level: service
tags: [security, correctness, multi-tenant, data]
severity: should-fix
status: draft
lacks: orgs, Microsoft (EF Core query filter) and OWASP (row-level security) only; needs one more org that scopes tenants in the data layer by default
lang: core
applies_when: Several tenants share one table or database and the service reads tenant data.
context: [data]
tool_gate: A test that reads as a second tenant and asserts the first tenant's rows are absent; Postgres FORCE ROW LEVEL SECURITY.
borrowed_from:
  - https://learn.microsoft.com/en-us/ef/core/querying/filters
  - https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
---

**Rule.** Enforce tenant scope in the data layer by default, with a query filter or row-level security, not by a predicate at each call site.

**Why.** A tenant predicate written per query is one forgotten `WHERE` away from showing one customer another's rows. Put the scope where every query inherits it, and make the unscoped read an explicit, visible call. Set the tenant from the verified identity, not from a request field. In Postgres, `FORCE` row-level security so the table owner is filtered too.

**FAIL**

```csharp
// Each caller must remember the tenant predicate.
var orders = await db.Orders.ToListAsync();   // returns every tenant's orders
```

**PASS**

```csharp
modelBuilder.Entity<Order>()
    .HasQueryFilter(o => o.TenantId == _tenantId);   // _tenantId comes from the verified identity

var orders = await db.Orders.ToListAsync();          // scoped by default
```

```sql
ALTER TABLE orders ENABLE ROW LEVEL SECURITY;
ALTER TABLE orders FORCE ROW LEVEL SECURITY;
CREATE POLICY tenant_isolation ON orders
    USING (tenant_id = current_setting('app.tenant_id')::uuid);
```

**Counterpoint.** "A hidden filter surprises people and costs performance." The surprise is the point: a missing filter fails safe. Index the tenant column, and keep the escape hatch (`IgnoreQueryFilters()`, or a separate admin role) rare, named, and audited.

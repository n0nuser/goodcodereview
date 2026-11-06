---
id: svc-soft-delete-default
level: service
tags: [security, correctness, data]
severity: should-fix
status: stable
lang: core
applies_when: A table or model marks a row as deleted instead of removing it.
context: [data]
tool_gate: A test per read path: soft-delete a row, then assert the endpoint returns 404 or leaves it out of the list.
borrowed_from:
  - https://learn.microsoft.com/en-us/ef/core/querying/filters
  - https://laravel.com/docs/12.x/eloquent
  - https://sequelize.org/docs/v6/core-concepts/paranoid/
  - https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
---

**Rule.** Filter soft-deleted rows out of every read path by default, and make a read that includes them an explicit call.

**Why.** A soft delete sets a column. It does not remove the row, so any query that forgets the filter still returns the record. One raw query or one new endpoint is enough to expose it. Put the filter in the model's default scope, so new queries inherit it, and keep the escape hatch visible. A deletion policy has to reach caches, exports, replicas and object versions too, or the record lives on in a copy.

**FAIL**

```csharp
modelBuilder.Entity<Document>();                 // no HasQueryFilter
var doc = await context.Documents.FindAsync(42); // returns the soft-deleted row
```

**PASS**

```csharp
modelBuilder.Entity<Document>().HasQueryFilter(d => d.DeletedAt == null);

// The one admin report that needs deleted rows, behind an admin check:
var all = await context.Documents.IgnoreQueryFilters().ToListAsync();
```

**Counterpoint.** "The admin console has to see deleted rows." Keep that one call explicit, name it for what it does, and check the caller is an admin. The default stays closed. Raw SQL and reporting replicas are the usual bypass, so route them through the same helper or audit them. A service that hard-deletes does not need the filter, but backups and object versions can still hold the old copy.

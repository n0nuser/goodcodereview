---
id: svc-tenant-id-in-telemetry
level: service
tags: [security, observability, multi-tenant]
severity: should-fix
status: stable
lang: core
applies_when: A shared log, metric or audit store holds records from more than one tenant.
context: [server]
tool_gate: A test that writes an event for each of two tenants, then queries one tenant and asserts the other is absent.
note: tenant id on tenant-scoped records backed by OWASP (server-verified tenant context in security and audit events), AWS SaaS Lens (inject tenant context into log messages and metric events) and Microsoft (a telemetry initializer injects the tenant ID into every telemetry item; the noisy-neighbor page asks for the tenant identifier in telemetry); Google GKE routes logs to a store per tenant, which is the alternative in the Counterpoint
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Multi_Tenant_Security_Cheat_Sheet.html
  - https://docs.aws.amazon.com/wellarchitected/latest/saas-lens/layers-hide-tenant-details.html
  - https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/service/application-insights
  - https://learn.microsoft.com/en-us/azure/architecture/antipatterns/noisy-neighbor/noisy-neighbor
  - https://docs.cloud.google.com/kubernetes-engine/docs/how-to/multi-tenant-logging
  - https://learn.microsoft.com/en-us/azure/architecture/guide/multitenant/approaches/storage-data
---

**Rule.** Put the verified tenant id on every tenant-scoped log, metric and audit record.

**Why.** A shared store returns another tenant's activity to any query that does not filter. The id has to be written from the verified tenant context, not from a request header, and it has to be there when a batch job or a queue worker writes the record, since no request middleware runs in those paths. A centralized audit store is acceptable only when read access enforces tenant scope. Metric events need the field too, or a per-tenant dashboard shows another tenant's numbers. Platform events that belong to no tenant, such as a node restart, carry no tenant id and are outside the Rule.

**FAIL**

```python
log.info("order %s paid", order_id)
audit.write(action="order.paid", actor=user.id)
```

**PASS**

```python
log.info("order %s paid", order_id, extra={"tenant_id": tenant.id})
audit.write(action="order.paid", tenant_id=tenant.id, actor=user.id)
```

**Counterpoint.** "The pipeline adds the tenant from the request context." That works only for code that runs inside a request. Workers, schedulers and sidecars write records too, and a query cannot recover a field that was never written. If a shared layer injects the field, verify it with a two-tenant query, because a layer that silently skips one producer looks the same as a correct one until the query runs. Splitting logs into a store per tenant is stronger still where the operational cost is justified.

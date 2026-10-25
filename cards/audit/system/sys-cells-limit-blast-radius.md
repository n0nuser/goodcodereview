---
id: sys-cells-limit-blast-radius
level: system
tags: [reliability, isolation, availability]
severity: discuss
status: draft
note: Netflix (each Titus region is divided into independent cells that bound any one control plane), Slack (moved critical user-facing services to cells to limit the blast radius of site failures), Airbnb (moved its metrics store to multiple clusters to set up separate failure domains), Cloudflare (control-plane postmortem: test the blast radius of failures and minimise the services one failure hits); per-tenant caps are left to svc-rate-limit-quota
lang: core
applies_when: Many tenants, regions, or product surfaces share one cluster, control plane, or data store.
tool_gate: none
borrowed_from:
  - https://netflixtechblog.com/single-tenant-titus-vm-level-isolation-on-a-multi-tenant-container-platform-6d8b1909d163
  - https://slack.engineering/slacks-migration-to-a-cellular-architecture/
  - https://airbnb.tech/infrastructure/building-a-fault-tolerant-metrics-storage-system-at-airbnb/
  - https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/
---

**Rule.** Split shared infrastructure into independent cells, each with its own control plane and storage, and route each tenant or request to one cell, so one failure stops only that cell.

**Why.** With one global cluster, every failure is global. A bad config push, an overloaded control plane, or a corrupt index stops every customer at once. Netflix divides each region into independent cells, which also caps how large any one control plane can grow. Slack moved its critical user-facing services to cells to limit the blast radius of site failures. Airbnb moved its metrics store to several clusters to get separate failure domains.

**FAIL**

```yaml
# one cluster and one control plane serve every tenant
clusters:
  - name: metrics-prod
    tenants: all
```

**PASS**

```yaml
# each cell has its own control plane and storage; no cross-cell call on the request path
clusters:
  - name: metrics-cell-1
    tenants: [payments, search]
  - name: metrics-cell-2
    tenants: [checkout, ads]
```

**Counterpoint.** "Cells cost more and add a routing layer." They do, with spare capacity in every cell, and a small service with one team may not earn them. Ask what one failure takes down. If one cluster outage or one bad deploy stops every customer, and that matters at your scale, mark `FAIL`. Cloudflare's postmortem asks for exactly that test of the blast radius. A per-tenant quota inside one cluster stops a noisy tenant but not a failed control plane. See [[svc-rate-limit-quota]]. Cells help only if a change reaches them one at a time. See [[prod-canary-staged-rollout]].

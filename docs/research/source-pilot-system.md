# Source pilot, system level

Checks five source pages for code-review rules that the card set may not cover. Coverage came from `cards/` and `packs/` reads, plus `docs/COVERAGE.md` for overload terms only (see gaps). No card files were created or edited. A NEW candidate is a lead, not a card: each needs three independent organisations.

Totals: 14 rules. covered 7, partial 4, NEW 3.

## 1. AWS Builders' Library: Fairness in multi-tenant systems

- URL: https://aws.amazon.com/builders-library/fairness-in-multi-tenant-systems/
- Fetch status: redirected (301) to https://builder.aws.com/content/3Eupj3d2bo4fEvlzYbICMZNhQ3B/fairness-in-multi-tenant-systems. The redirect was followed and that page was fetched.

| Rule | Mark | Evidence |
|---|---|---|
| Load shedding: reject excess work cheaply | covered: `sys-load-shedding-bounded-queues` | "Load shedding is the act of cheaply rejecting work instead of spending limited resources on it." |
| Give each caller a default per-tenant quota | covered: `svc-rate-limit-quota` | "Service owners define rules that give each caller a default quota." |
| Quota rejection returns 429 | covered: `svc-rate-limit-quota` (429 for quota, 503 for own lack of capacity) | "'API rate limit exceeded' responses 'generally are returned with a 429 status code.'" |

## 2. Google SRE book: Handling overload

- URL: https://sre.google/sre-book/handling-overload/
- Fetch status: fetched.

| Rule | Mark | Evidence |
|---|---|---|
| Serve degraded responses under overload | partial: `sys-load-shedding-bounded-queues` covers rejecting work and `svc-best-effort-optional-deps` covers degraded results for slow non-critical dependencies. Missing: a degraded answer served as the response to overload itself. | "One option for handling overload is to serve degraded responses" |
| Retry only at the layer directly above the one rejecting | covered: `svc-retry-policy` ("Retry at one layer only") | "requests should only be retried at the layer immediately above the layer that is rejecting them" |
| Client-side throttling: stop sending once requests exceed K times accepts (K = 2 by default) | NEW candidate. Nearest checked: `svc-rate-limit-quota` (server-side per-tenant quota) and `svc-retry-policy` (retry caps). Needs two more independent orgs. Not checked: whether Netflix concurrency-limits, already cited in `sys-load-shedding-bounded-queues`, states this rule. | "Clients can continue to issue requests to the backend until `requests` is K times as large as `accepts`." |

## 3. Apache Cassandra: CQL DDL

- URL: https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html
- Fetch status: fetched.

| Rule | Mark | Evidence |
|---|---|---|
| Primary key of a table cannot be altered after creation | NEW candidate. Nearest checked: none. Cards searched for cassandra, cql, keyspace, clustering and tombstone: only `sys-fanout-leg-deadlines` and `fn-rerun-safe-after-crash` cite Cassandra URLs, and neither states this. Needs two more independent orgs (not checked). | "The primary key of a table cannot ever be altered." |
| An INSERT with an existing primary key is an UPSERT, not an error | NEW candidate. Nearest checked: none. Needs two more orgs (not checked). | "if another row is inserted using the same primary key, then an `UPSERT` occurs" |
| Set a table default TTL so rows expire | covered: `sys-append-only-stores-have-retention` (every grow-only store needs a max age or count and an enforcing setting). Card cites Elastic and Kubernetes, not Cassandra. | "Default expiration time (\"TTL\") in seconds for a table" |

## 4. AWS Well-Architected: Cell-based architecture

- URL: https://docs.aws.amazon.com/wellarchitected/latest/reducing-scope-of-impact-with-cell-based-architecture/what-is-a-cell-based-architecture.html
- Fetch status: fetched.

| Rule | Mark | Evidence |
|---|---|---|
| Each cell is independent and shares no state with other cells | covered: `sys-cells-limit-blast-radius` (PASS: "no cross-cell call on the request path") | "Each cell is independent, does not share state with other cells, and handles a subset of the overall workload requests." |
| The cell router is the thinnest layer and only routes | partial: `sys-cells-limit-blast-radius` requires routing each tenant to one cell but does not say the router must hold no other logic. | "Cell router — ... the responsibility of routing requests to the right cell, and only that." |
| Roll out changes compartment by compartment | partial: only in the card's Counterpoint ("Cells help only if a change reaches them one at a time"), not as a Rule. Cross-referenced `prod-canary-staged-rollout`, not opened. | "When provisioning a new customer or tenant, or applying a workload change, you can do this gradually, compartment by compartment" |

## 5. Elastic: Index lifecycle management

- URL: https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html
- Fetch status: fetched. The page gives no default `min_age`, shard counts or rollover thresholds. The 50GB, 7-day and 30-day figures are illustrative only and are not used as rules.

| Rule | Mark | Evidence |
|---|---|---|
| Data moves through phases and the index is deleted at the end of retention | covered: `sys-append-only-stores-have-retention` (its PASS drops monthly partitions past 13 months; its Elastic source is cited) | "transitions through phases (`hot`, `warm`, `cold`, `frozen`, `delete`) based on pre-defined conditions." |
| Roll over to a new write index on size, document count or age | partial: the card requires a bound and an enforcing job but does not name rollover triggers. | "Creates a new write index when the current one reaches a certain size, number of docs, or age." |

## Gaps

- Bash was denied by the auto-mode classifier for three COVERAGE.md searches (Cassandra, cell and ILM terms), so `docs/COVERAGE.md` was not searched for those terms. The cell and ILM marks rest on card reads only. A COVERAGE.md check is still open.
- Cassandra marks rest on a cards-only search. COVERAGE.md was not searched for them.
- Lead sources for the three NEW candidates were not fetched, so no third-org evidence is in hand.

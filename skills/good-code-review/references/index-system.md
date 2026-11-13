# System audit index

One line per stable system card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `system.md`: read them with offset `<first>` and limit `<count>`.

- `sys-agent-tool-least-privilege` [block] {security, process} L3+26: Give the agent only the narrow tools and the minimal credentials its task needs.
- `sys-cache-bounds-invalidation` [should-fix] {performance} L30+26: Bound every cache by size and give its entries an expiry.
- `sys-cells-limit-blast-radius` [discuss] {reliability} L57+32: Split shared infrastructure into independent cells, each with its own control plane and storage, and route each tenant or request to one cell, so one failure stops only that cell.
- `sys-consistent-ui-terms` [discuss] {usability, accessibility} <ui> L90+29: Use one label and one icon for the same action and the same concept across all screens.
- `sys-fanout-leg-deadlines` [should-fix] {performance, reliability} L120+28: Give every leg of a fan-out its own deadline, and decide in code what happens when a leg misses it: a partial result, a hedged request, or an error.
- `sys-health-liveness-readiness` [should-fix] {reliability} L149+25: Wire load balancers and restarters to liveness and local checks only, never to shared-dependency checks.
- `sys-index-concurrently` [should-fix] {compatibility} <data> L175+28: Create indexes with `CONCURRENTLY`, outside a transaction block, and handle a failed build that leaves an INVALID index.
- `sys-load-shedding-bounded-queues` [block] {reliability} <server> L204+28: Bound every queue and reject excess work cheaply.
- `sys-lock-fencing` [block] {reliability, correctness} L233+29: Check a correctness lock on the resource side (fencing token or compare-and-set), never by lock possession alone.
- `sys-migration-expand-contract` [block] {reliability, compatibility} <data> L263+26: Run data backfills in batches, in a migration separate from the schema change.
- `sys-migration-lock-timeout` [should-fix] {compatibility} <data> L290+27: Set `lock_timeout` for the migration session and retry on timeout.
- `sys-n-plus-one-pooling` [should-fix] {performance} <data> L318+28: Fetch related rows in one query or batch, never one query per row.
- `sys-pii-minimise-retention` [should-fix] {security} L347+27: Give every store of personal or sensitive data a retention period, and delete or anonymise the data when it ends.
- `sys-prompt-injection` [block] {security} L375+25: Validate model output deterministically before code acts on it.
- `sys-secrets-and-errors` [block] {security, correctness} L401+30: Fail closed: a validation or auth error must deny, never continue, and an error response must not carry internals such as stack traces, SQL or tokens.
- `sys-ssrf` [block] {security} L432+27: Fetch a user-supplied URL only when its host matches a server-side allowlist.

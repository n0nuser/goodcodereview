sys-ssrf-pin-resolved-ip: rejected, stable sys-ssrf Why already says to check the resolved address and connect to it, and to turn off redirects (clause of an existing card; also covers sys-ssrf-no-redirects).
sys-ssrf-no-redirects: rejected, one org, and sys-ssrf already states the redirect clause.
sys-no-single-facility-dependency: rejected, sys-cells-limit-blast-radius already cites the Microsoft stamp page; the Cloudflare row is a service-class policy, so a reviewer cannot FAIL it from a diff.
sys-timing-free-lock-safety: rejected, the timing clause is in stable sys-lock-fencing (same Kleppmann and antirez sources); the monotonic-clock clause has only antirez, a person.
sys-tx-per-batch-migration: rejected, overlaps stable sys-migration-expand-contract (batching, CockroachDB already cited) and source conflict on transactions is unreconciled per the clusters file.

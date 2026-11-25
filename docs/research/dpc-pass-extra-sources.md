# Sources read in the data, privacy and cost pass

Fetch date 2026-11-24. Each page was fetched with `curl -sL`, tags stripped, and the sentence matched in the text. These sources back cards beyond the lead notes.

## fn-side-effects-after-commit

- https://guides.rubyonrails.org/active_job_basics.html : "Transactional Integrity on Jobs". A queue in the same database enqueues inside the surrounding transaction. `enqueue_after_transaction_commit` defers the enqueue until the commit.
- https://docs.spring.io/spring-modulith/reference/events.html : the event publication registry writes an entry per transactional listener into a log "as part of the original business transaction" (an outbox).
- https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html : the transactional outbox resolves the dual-write problem; the database update and the event notification should run atomically.
- https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-outbox-cosmos : how to use the transactional outbox pattern for reliable messaging and guaranteed delivery.

## sys-cache-cold-start (soft)

- https://pkg.go.dev/golang.org/x/sync/singleflight : the package description, a duplicate function call suppression mechanism. Tool description, not counted.

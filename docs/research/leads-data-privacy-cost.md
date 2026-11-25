# Leads: data, privacy and cost

Method: each page fetched with `curl -sL`, tags stripped with `python3 -I`, sentence found with `rg` in the stripped text. Fetch date 2026-11-24. About 125 fetches were made (over the 60 target, because many cost and privacy pages are JS shells or 404s). Quotes are 10 words or fewer; the rest is paraphrase. Org grouping follows docs/PROMOTION.md (Google SRE book and Google Cloud docs are one org; Microsoft Learn is one org; OWASP is one org).

Existing-card check: `rg` over `cards/` for backup, restore, consent, transaction, on_commit, resource limits, tag, budget, lifecycle, timestamp, foreign key, migration. Covered already: `sys-migration-expand-contract`, `sys-migration-lock-timeout`, `sys-index-concurrently`, `sys-constraint-not-valid`, `chg-migration-add-column-rewrite`, `sys-n-plus-one-pooling`, `sys-pii-minimise-retention`, `sys-append-only-stores-have-retention`, `svc-soft-delete-default`, `svc-sqli-authn`, `svc-list-endpoint-paginates`, `fn-fetch-only-needed-data`, `chg-new-query-has-plan` (draft), `fn-atomic-related-updates`, `svc-saga-steps`, `svc-idempotency-key`. No card mentions restore testing, consent, container resource requests, cost tags, budgets, or after-commit side effects.

## Ranking

| # | Rule | Orgs | Verdict |
|---|---|---|---|
| 1 | Backups are restore-tested on a schedule | 5 (AWS, Google, CISA, Microsoft, GitLab) | clears 3, new card |
| 2 | Side effects (jobs, email, cache, HTTP) run after commit, not inside the transaction | 5 (Django, Rails, Spring, Sidekiq, GitLab) | clears 3, new card |
| 3 | Every container sets resource requests (and a memory limit) | 3 (Microsoft, AWS, Google) | clears 3, new card |
| 4 | An applied migration is never edited; fix with a new one | 3 (Redgate Flyway, Rails, Prisma) | clears 3, new card |
| 5 | Taggable cloud resources carry owner and cost tags, enforced by policy or provider defaults | 3 (Microsoft, AWS, FinOps Foundation) | clears 3 but soft |
| 6 | Cloud spend has a budget with an alert | 3 tool pages | soft |
| 7 | Storage buckets that grow have a lifecycle expiry or tiering rule | 3 vendor pages | soft |
| 8 | Store timestamps as UTC / timestamptz | 2 firm (PostgreSQL wiki, Django) + descriptive | short |
| 9 | Keep a dated consent record and allow one-step withdrawal | 1 firm (ICO) + law | short |
| 10 | Index the referencing column of a foreign key | 2 (PostgreSQL, GitLab) | short |
| 11 | Inspect and test generated migration SQL before production | 1 to 2 (Microsoft EF, GitLab reversibility) | short |

## 1. Backups are restore-tested on a schedule

Rule candidate: "A system that keeps backups of its data has a scheduled, automated restore test that checks the restored data, with a named owner." A reviewer reads the repo or runbook for a restore job, a test plan resource (for example AWS Backup restore testing), or a recurring drill, and marks FAIL when backups exist and nothing restores them. Nearest card: `inc-rollback-path-tested` (deploy rollback, not data) and `svc-soft-delete-default` (mentions backup only in passing). New card, level `system` or `production`, `context: [data]`.

1. AWS. https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html . REL09-BP04: "perform periodic recovery of the data to verify backup integrity". It says to validate RTO and RPO "by performing a recovery test". A product feature backs it: https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html (automated, periodic restore evaluation).
2. Google. https://sre.google/sre-book/data-integrity/ . "Continuously test the recovery process" and alert when a recovery heartbeat fails. https://cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-data-loss (same org) says to run consistency checks after each backup and restore in a non-production environment.
3. CISA. https://www.cisa.gov/stopransomware/ransomware-guide . "regularly test the availability and integrity of backups". Also says keep backups offline.
4. Microsoft. https://learn.microsoft.com/en-us/azure/well-architected/reliability/disaster-recovery . "Regularly test restores to validate backups".
5. GitLab. https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/ . Postmortem: backups failed when needed; the root-cause answer is that no one owned testing them, and the fix list includes "Automated testing of recovering PostgreSQL database backups". A team describing its own practice and why; counts.

Count: AWS, Google, CISA, Microsoft, GitLab = 5. Not found: NCSC backup pages (404), PostgreSQL docs (describe how, never say test). Scope caveat: state held only in a managed service with no backup duty, or fully derived data that can be rebuilt, is N/A. Counterpoint: restore tests cost money and need a spare environment; answer: a sampled restore (one table, one volume) is enough, and AWS and Google both automate it. Weak clause not carried: "keep one copy offline or in a separate account" is only CISA and Microsoft (offline copies of DR assets); soft, leave out or move to Why.

## 2. Side effects run after commit, not inside the transaction

Rule candidate: "Enqueue a job, send an email or call an external service after the transaction commits (on_commit, after_commit, transactional event listener), not inside the transaction block." A diff that calls `send_mail`, `perform_async` or an HTTP client inside `with transaction.atomic()` or `transaction do` is a FAIL. Nearest cards: `fn-atomic-related-updates` (what goes inside the transaction), `svc-saga-steps`, `svc-idempotency-key`; none states the after-commit rule. New card, `context: [data]`. Two clauses share the evidence: the job can run before the data exists (race), and an open transaction holds locks while the network call runs.

1. Django. https://docs.djangoproject.com/en/5.2/topics/db/transactions/ . "Performing actions after commit": for work that should happen "only if the transaction successfully commits", for example a background task, email or cache invalidation, use `on_commit()`.
2. Rails. https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html . `after_commit` callbacks are for "interacting with other systems"; they run "only executed when the database is in a permanent state". It also names clearing a cache inside the transaction as a hazard.
3. Spring. https://docs.spring.io/spring-framework/reference/data-access/transaction/event.html . A `@TransactionalEventListener` is "bound to the commit phase of the transaction by default", so the listener runs only after success.
4. Sidekiq. https://github.com/sidekiq/sidekiq/wiki/FAQ . The "Can't find ModelName with ID" error happens because "Sidekiq is trying to execute your job before the transaction has actually committed"; fix is the `transactional_push` feature.
5. GitLab. https://docs.gitlab.com/development/database/transaction_guidelines/ . "Ideally, a transaction should only contain database statements." Avoid in a transaction block: triggering Sidekiq jobs, sending emails, HTTP API calls.

Count: 5 organisations, all firm. Scope caveat: transactional outbox or a queue that lives in the same database (Solid Queue, per the Rails jobs guide) is a valid PASS, since the enqueue is part of the transaction by design. Counterpoint: after-commit work can be lost if the process dies between commit and enqueue; answer: that is why the card can point to an outbox row for work that must not be lost, and keeps the rule for best-effort side effects. Not found for the "no network call inside a transaction" clause alone beyond GitLab; it rides on the after-commit clause here.

## 3. Every container sets resource requests (and a memory limit)

Rule candidate: "Each container in a workload manifest sets CPU and memory requests, and a memory limit." A reviewer reads the manifest or Helm values; a container with no `resources:` block is a FAIL. Nearest card: none (`svc-bound-inbound-concurrency` and `sys-cache-bounds-invalidation` bound in-process resources, not containers). New card, level `module` or `system`, `context: [server]`, tag `cost`/`reliability`.

1. Microsoft (AKS). https://learn.microsoft.com/en-us/azure/aks/developer-best-practices-resource-management . "Set pod requests and limits on all pods in your YAML manifests." Without requests the scheduler cannot place pods well.
2. AWS (EKS). https://docs.aws.amazon.com/eks/latest/best-practices/cost-opt-compute.html . Each container, sidecars included, "should have their own requests and limits set" so the pod totals are accurate; over-high requests waste cost.
3. Google (GKE). https://cloud.google.com/kubernetes-engine/docs/best-practices/cost-optimization . "Specify precise container CPU and memory requests before deployment". It adds: leave CPU limits unrestricted and match memory requests to limits.

Count: 3 firm. The Kubernetes docs page (https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/) describes the mechanism and does not state "always set"; not counted. Caveat and counterpoint: the vendors disagree on CPU limits (GKE says leave them off), so the Rule must say requests for CPU and memory, limit for memory only. Cluster policy (LimitRange defaults) can satisfy the rule outside the manifest; PASS if the repo shows it.

## 4. An applied migration is never edited

Rule candidate: "Never edit a migration file that has already run anywhere beyond your own machine; add a new migration instead." Checkable from the diff: a changed or deleted file under `migrations/` that is already on the main branch. Nearest cards: `chg-delete-legacy-after-migration` (deleting old code), `sys-migration-expand-contract` (how to change a schema). None covers editing history. New card, level `change`, `context: [data]`.

1. Redgate Flyway. https://documentation.red-gate.com/flyway/flyway-concepts/migrations/versioned-migrations . "It is best practice not to make changes to existing versioned migrations once they have been applied". Flyway stores a checksum to detect it.
2. Rails. https://guides.rubyonrails.org/active_record_migrations.html . "editing existing migrations that have been already committed to source control is not a good idea"; it causes extra work and breaks when someone already ran the old version.
3. Prisma. https://www.prisma.io/docs/orm/prisma-migrate/workflows/troubleshooting . "You should never purposefully delete or edit a migration", since it causes dev and production to diverge.

Count: 3 firm. Soft extra: Liquibase compares a stored checksum with the changeset (https://docs.liquibase.com/concepts/changelogs/changeset-checksums.html); that is a mechanism, not a stated rule. Rails allows editing a migration that has not yet been pushed or run elsewhere, and Flyway limits the rule to "permanent downstream" environments, so the scope is "merged or deployed". Counterpoint: a broken migration that never ran in production is cheaper to fix in place; answer: the rule applies once any shared environment has run it.

## 5. Taggable cloud resources carry owner and cost tags (soft)

Rule candidate: "Resources defined in infrastructure code carry the organisation's required tags (owner, environment, cost centre), set through provider default tags or an enforced policy." Checkable in a Terraform or Bicep diff. Nearest card: none (`chg-flag-owner-retirement` is the same owner idea for flags). Clears three, but each source mostly describes a tool.

1. Microsoft. https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-tagging . "Enforce tagging compliance with Azure Policy." Also states clear governance defines which tags are mandatory, and tags support cost allocation.
2. AWS. https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_tag-policies.html . Tag policies "standardize the tags attached to the AWS resources" in an organisation. https://developer.hashicorp.com/terraform/tutorials/aws/aws-default-tags says AWS recommends a consistent tagging strategy for audit, cost and access control (HashiCorp, tutorial; not counted as its own org).
3. FinOps Foundation. https://www.finops.org/framework/capabilities/allocation/ . Measures "percentage of resource deployments with missing allocation metadata" and tag-policy violations prevented; a stated practice, framed as a KPI.

Count: Microsoft, AWS, FinOps = 3, soft. Google's labels page (https://cloud.google.com/resource-manager/docs/labels-overview) gives only caveats (no PII in labels, avoid high-cardinality labels); no "always label" sentence found. Related clause worth a note: Microsoft and Google both say never put sensitive values in tags or labels. Counterpoint: tags are not free to maintain and not every resource type is taggable; answer: scope to taggable resources, and let policy report the rest.

## 6. Cloud spend has a budget with an alert (soft)

Pages found describe the tool, not a rule: AWS Budgets (https://docs.aws.amazon.com/cost-management/latest/userguide/budgets-managing-costs.html, example alert at 80 percent), Azure Cost Management (https://learn.microsoft.com/en-us/azure/cost-management-billing/costs/tutorial-acm-create-budgets, "help you plan for and drive organizational accountability"), Google Cloud Billing (https://cloud.google.com/billing/docs/how-to/budgets), FinOps (https://www.finops.org/framework/capabilities/budgeting/, "Set budgets to create healthy constraints on application teams"). Only FinOps states a practice. Verdict: soft, one firm org. The Azure and AWS Well-Architected pages that would state it were JS shells (Azure) or not found (AWS cost pillar). Nearest card: `prod-slo-error-budget` (reliability budget, unrelated). Do not draft.

## 7. Storage that grows has a lifecycle rule (soft)

AWS S3 (https://docs.aws.amazon.com/AmazonS3/latest/userguide/cost-optimization.html: use Lifecycle configuration to "automatically delete expired objects"), Azure Blob (https://learn.microsoft.com/en-us/azure/storage/blobs/lifecycle-management-overview: rule-based policies "transition data to cooler tiers or expire it"), Google Cloud Storage (https://cloud.google.com/storage/docs/lifecycle). All three say what the feature can do; none says every bucket must have one. Nearest card: `sys-append-only-stores-have-retention` (stable, covers append-only stores and retention). Verdict: add the three URLs to that card's `borrowed_from` as support for object stores, not a new card. Same for log groups: AWS CloudWatch log groups have a retention setting (https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html), already within that card's scope.

## 8. Store timestamps as UTC or timestamptz (short)

1. PostgreSQL wiki. https://wiki.postgresql.org/wiki/Don%27t_Do_This . "Don't use the timestamp type to store timestamps, use timestamptz". Firm.
2. Django. https://docs.djangoproject.com/en/5.2/topics/i18n/timezones/ . "it's still good practice to store data in UTC in your database". Firm.
3. Descriptive only, not counted: Ecto (https://hexdocs.pm/ecto_sql/Ecto.Migration.html, creates databases in UTC and asks you to configure production the same), Rails (config default `:utc`), CockroachDB (stores in UTC). Microsoft .NET guidance recommends `DateTimeOffset` for unambiguous instants but does not say "store UTC"; no sentence matched. GitHub's API returns UTC; that is an API output, not storage.
Verdict: 2 firm, short. Nearest card: none. Worth one more search (Google Cloud Spanner/BigQuery docs, AWS, Stripe) before drafting.

## 9. Consent is recorded and withdrawal is one step (short)

1. ICO. https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/lawful-basis/consent/how-should-we-obtain-record-and-manage-consent/ . Keep records of who consented, when (a timestamp), what they were told, how, and whether they withdrew. Also says withdrawal should be "as easy" as giving consent, a one-step process.
2. GDPR Art. 7 (https://gdpr-info.eu/art-7-gdpr/) states both duties; it is law, not an organisation.
3. EDPB and CNIL pages returned 404 or a shell, so no second regulator was confirmed. Not found: any engineering organisation (Google, Mozilla, W3C) stating a consent-record schema; the W3C DPV page was a shell.
Verdict: 1 firm org. Short. Nearest card: `sys-pii-minimise-retention` (already notes GDPR Art. 5 is law, not an org). Do not draft; retry with the EDPB guidelines PDF fetched from another mirror.

## 10. Index the referencing column of a foreign key (short)

PostgreSQL docs (https://www.postgresql.org/docs/current/ddl-constraints.html): "it is often a good idea to index the referencing columns too". GitLab (https://docs.gitlab.com/development/database/foreign_keys/): "when adding a foreign key, you must always add an index first". Two orgs; Rails and Django index foreign keys by default, which makes the rule a tool convention for them. Nearest cards: `sys-constraint-not-valid`, `sys-index-concurrently`. Verdict: short; a third org (for example MySQL, which creates the index automatically, or Cockroach) was not confirmed.

## 11. Inspect and test generated migration SQL before production (short)

Microsoft EF Core (https://learn.microsoft.com/en-us/ef/core/managing-schemas/migrations/applying): "always inspect the generated migrations and test them before applying to a production database". GitLab (https://docs.gitlab.com/development/migration_style_guide/): a migration "must be reversible". Different claims; each has one org. Nearest: `chg-new-query-has-plan` (draft, plan on production-sized data). Verdict: short.

## Checked and dropped

- Statement and idle-in-transaction timeouts for the application role: PostgreSQL documents the settings (`idle_in_transaction_session_timeout`) and GitLab sets 15 s on GitLab.com, but no page states a recommendation. Heroku, Crunchy and AWS RDS pages had no matching sentence. `sys-migration-lock-timeout` covers migrations only.
- Production data in non-production environments: only OWASP's database cheat sheet says to use separate databases and accounts per environment; the PCI and NIST pages were PDFs or shells. One org.
- Erasure reaching backups and processors: no source fetched states it beyond the ICO and law.
- Kubernetes autoscaler max bounds and idle-resource cleanup: not searched (fetch budget spent).
- Money as decimal, not float: not searched.

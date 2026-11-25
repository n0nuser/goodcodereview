---
id: sys-backup-restore-tested
level: system
tags: [reliability, resilience, data]
severity: should-fix
status: stable
lang: core
applies_when: The system keeps backups of its own data, such as database dumps, snapshots or object-store copies.
context: [data]
tool_gate: A scheduled restore job that exits non-zero when the restored data fails its checks; an alert when the job has not run for longer than its schedule.
note: The three clauses (a restore on a schedule, a check on the restored data, an owner) share the evidence. AWS, Google, CISA and Microsoft state the regular restore test. AWS, Google and CISA add the integrity check. GitLab is a team's own postmortem, with the automated restore test in its fix list. Keeping a copy offline is stated by CISA and Microsoft only, so it is left out of the Rule
borrowed_from:
  - https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/rel_backing_up_data_periodic_recovery_testing_data.html
  - https://docs.aws.amazon.com/aws-backup/latest/devguide/restore-testing.html
  - https://sre.google/sre-book/data-integrity/
  - https://cloud.google.com/architecture/framework/reliability/perform-testing-for-recovery-from-data-loss
  - https://www.cisa.gov/stopransomware/ransomware-guide
  - https://learn.microsoft.com/en-us/azure/well-architected/reliability/disaster-recovery
  - https://about.gitlab.com/blog/2017/02/10/postmortem-of-database-outage-of-january-31/
---

**Rule.** Restore every backup set on a schedule, check the restored data, and alert when the restore fails or stops running.

**Why.** A backup that has never been restored is a guess. The dump can be empty, the credentials expired, the schema changed, or the job can have failed quietly for months, and the first restore then happens during an outage. Run the restore from a job, not from a person's memory, and give the job an owner who gets the alert. A sampled restore is enough: one table, one volume, one day. Data you can rebuild from another source, and state held only in a managed service that has no backup duty, are out of scope.

**FAIL**

```text
# crontab on the db host: the only backup job
0 2 * * *  pg_dump -Fc orders | aws s3 cp - s3://acme-backups/orders/$(date +\%F).dump
# nothing ever reads the dump back
```

**PASS**

```bash
#!/usr/bin/env bash
# restore-check.sh: weekly job with an owner and an alert on non-zero exit
set -euo pipefail
aws s3 cp "s3://acme-backups/orders/$(date +%F).dump" /tmp/orders.dump
createdb restore_check
pg_restore --no-owner -d restore_check /tmp/orders.dump
psql -d restore_check -tAc "select count(*) from orders" | awk '$1 < 1000 { exit 1 }'
dropdb restore_check
```

**Counterpoint.** "Restore tests cost money and need a spare environment." Restore a sample into a scratch instance that lives for the length of the job. The bill is small next to finding out during an incident that the backup is unusable. Managed backup services can schedule the restore and run the checks for you, which also meets the Rule.

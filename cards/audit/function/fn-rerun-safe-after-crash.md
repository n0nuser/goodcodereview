---
id: fn-rerun-safe-after-crash
level: function
tags: [reliability, idempotency]
severity: block
status: stable
lang: core
applies_when: A function or job changes state and can be run twice, or can be killed partway.
tool_gate: none
note: second run - cursor/plugins, Uber, Stripe, Dropbox, GitHub, Netflix; crash at any step - cursor/plugins, Stripe, Dropbox (workers die mid-task and retries must stay correct), Netflix; derive from current state - cursor/plugins, Stripe, Netflix, GitHub; leftovers recognisable - cursor/plugins, Netflix (a marker tied to the backup timestamp, a size check against the manifest), GitHub (a review records done only after every removal succeeds)
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-make-operations-idempotent/SKILL.md
  - https://www.uber.com/blog/high-throughput-processing/
  - https://stripe.dev/blog/how-stripe-uses-graph-search-and-state-machines-to-auto-remediate-a-global-database-fleet
  - https://dropbox.tech/infrastructure/asynchronous-task-scheduling-at-dropbox
  - https://netflixtechblog.com/timeseries-tiered-storage-journey-kafka-flink-streams-to-native-cassandra-cold-reads-e59d597c9d60
  - https://github.blog/engineering/platform-security/staying-evergreen-how-we-automated-secure-access-and-repo-hygiene-in-a-shared-org
---

**Rule.** Make a state-changing operation give the same result on a second run and after a crash at any step, by deriving each step from current state and making leftovers recognisable as stale.

**Why.** Jobs get retried and processes get killed. An append, a counter bump, or a lock file with no owner and time leaves the next run unable to tell finished work from half-done work. Record "done" only after the last step succeeds, so a crash leaves the work visibly pending.

**FAIL**

```python
cur.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, acct))  # a retry applies it twice
open("out.json", "w").write(data)                                                       # a crash leaves a truncated file
```

**PASS**

```python
cur.execute("INSERT INTO applied_ops (op_id) VALUES (%s) ON CONFLICT DO NOTHING", (op_id,))
if cur.rowcount == 1:  # first run of this operation; same transaction as the update
    cur.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, acct))
tmp = path.with_suffix(".tmp")
tmp.write_text(data)
os.replace(tmp, path)  # the reader sees the old file or the new one, never half of one
```

**Counterpoint.** "Retries are rare." Crashes are not. For API calls that cross a network, [[svc-idempotency-key]] covers the key-based form of this rule.

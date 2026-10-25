---
id: fn-rerun-safe-after-crash
level: function
tags: [reliability, idempotency]
severity: block
status: draft
lang: core
applies_when: A function or job changes state and can be run twice, or can be killed partway.
tool_gate: none
note: rerun clause has cursor/plugins, Uber and Stripe; the crash clause (derive from current state) has cursor/plugins and Stripe; stale leftovers are cursor/plugins only
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-make-operations-idempotent/SKILL.md
  - https://www.uber.com/blog/high-throughput-processing/
  - https://stripe.dev/blog/how-stripe-uses-graph-search-and-state-machines-to-auto-remediate-a-global-database-fleet
---

**Rule.** Make a state-changing operation give the same result on a second run and after a crash at any step, by deriving each step from current state and making leftovers recognisable as stale.

**Why.** Jobs get retried and processes get killed. An append, a counter bump, or a lock file with no owner and time leaves the next run unable to tell finished work from half-done work.

**FAIL**

```text
balance += amount                      # a retry applies it twice
open("out.json", "w").write(data)      # a crash leaves a truncated file
```

**PASS**

```text
set the row to the target state keyed by the operation id
write out.json.tmp, then rename to out.json
lock holds owner and timestamp, so the next run can judge it stale
```

**Counterpoint.** "Retries are rare." Crashes are not. For API calls that cross a network, [[svc-idempotency-key]] covers the key-based form of this rule.

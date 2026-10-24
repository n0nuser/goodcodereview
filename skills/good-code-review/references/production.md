# production

## prod-canary-staged-rollout

severity: block  
applies_when: A change, config or dependency update is rolled out to production.

**Rule.** Roll out in stages behind a canary, and abort by rule, not by judgment.

**Why.** A 100% push exposes everyone to the bug. A canary must be large and long enough to be representative. Errors of 20% on 5% of traffic are only 1% overall, so tie the canary to your error budget.

**FAIL**

```text
deploy: all hosts at once, no comparison, rollback = "ask someone"
```

**PASS**

```text
# compare the canary to a control on a few chosen metrics
5% canary 30m -> compare error rate, p99 -> auto-rollback if worse -> 25% -> 100%
```

**See also.** [[chg-rollback-path]] (describe the undo), [[inc-rollback-path-tested]] (drill it).

**Counterpoint.** "Hotfixes can't wait." Then keep the canary short, not absent. Fleet tools should also have velocity limits. A hermetic, reproducible build tied to one revision is the precondition for rollback to mean anything.

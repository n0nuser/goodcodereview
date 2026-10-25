---
id: prod-shadow-compare-before-cutover
level: production
tags: [correctness, reliability, migration, release]
severity: should-fix
status: draft
note: Netflix (ran the old and new ad-event pipelines in parallel and diffed their output on live traffic), Stripe (compared point-in-time snapshots of source and target shards before the traffic switch), Airbnb (replayed captured production queries on MySQL 5.7 and 8.0 and diffed the results), GitHub (a Scientist experiment ran a candidate code block beside the control and compared results and timing); Cabify checks for zero replication lag before a swap, which is a precondition and not a diff, so it is not cited
lang: core
applies_when: Reads, writes, or a pipeline's traffic move from an old system to a new one, such as a new data store, a database upgrade, or a rewritten service.
tool_gate: none
borrowed_from:
  - https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb
  - https://stripe.dev/blog/how-stripes-document-databases-supported-99.999-uptime-with-zero-downtime-data-migrations
  - https://airbnb.tech/infrastructure/beyond-synthetic-testing-capturing-and-replaying-real-database-workloads-at-airbnb/
  - https://github.blog/engineering/engineering-principles/how-we-improved-availability-through-iterative-simplification
---

**Rule.** Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.

**Why.** Fixtures cover the cases someone thought of, and production holds the rest. Airbnb's replay of real queries against MySQL 5.7 and 8.0 found queries whose row order was never fixed, and an application that sent the same cacheable query over and over. Neither shows up in a test suite. A diff on real traffic finds these while the old system still answers users, so a mismatch costs a log line instead of an incident.

**FAIL**

```python
def get_order(order_id):
    return new_store.get(order_id)    # cut over in one step; never compared on real reads
```

**PASS**

```python
def get_order(order_id):
    old = old_store.get(order_id)     # users still get the old answer
    try:
        if new_store.get(order_id) != old:
            shadow_mismatch.inc()
            log.info("shadow mismatch", extra={"order_id": order_id})
    except Exception:
        shadow_error.inc()
    return old
# the cutover flag flips once shadow_mismatch is zero or every mismatch is explained
```

**Counterpoint.** "Running both is slow and doubles the load." It is slower than a flag-day switch, and Netflix says that is the reason it trusts the result. Keep the cost down: shadow a sample, call the new system off the request path, and never shadow a call with side effects such as a charge or an email. For writes, compare data snapshots after replication, as Stripe does, instead of sending each write twice. A refactor inside one process needs a characterization test, not production traffic. See [[chg-refactor-has-behaviour-pin]].

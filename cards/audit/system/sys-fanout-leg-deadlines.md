---
id: sys-fanout-leg-deadlines
level: system
tags: [performance, latency, resilience]
severity: should-fix
status: draft
lang: core
applies_when: A request fans out to several backends, shards, or replicas and combines the answers.
tool_gate: none
note: a cap on fan-out width has one org (Google) and is left out of the Rule
borrowed_from:
  - https://www.barroso.org/publications/TheTailAtScale.pdf
  - https://grpc.io/docs/guides/request-hedging/
  - https://cassandra.apache.org/doc/latest/cassandra/developing/cql/ddl.html
  - https://www.elastic.co/docs/api/doc/elasticsearch/operation/operation-search
  - https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto
---

**Rule.** Give every leg of a fan-out its own deadline, and decide in code what happens when a leg misses it: a partial result, a hedged request, or an error.

**Why.** Fan-out turns rare slowness into common slowness. If each of 100 backends is slow on 1 request in 100, about 63% of requests wait on at least one slow backend. Without a per-leg deadline the slowest leg sets the latency of every request.

**FAIL**

```text
results = await gather(*[shard.search(q) for shard in shards])   # waits for the slowest shard
```

**PASS**

```text
results = await gather(*[with_timeout(shard.search(q), 80ms) for shard in shards],
                       return_exceptions=True)
return merge(ok(results), partial=any_timed_out(results))
```

**Counterpoint.** "Hedging doubles the load." Sent at once to every replica, it does, which is why the sources hedge only after a wait past about the 95th percentile, cap the attempts, and cancel the twin. Hedge only idempotent reads. A partial result needs a product decision. The deadline does not.

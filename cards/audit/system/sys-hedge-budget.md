---
id: sys-hedge-budget
level: system
tags: [reliability, performance, hedging, retries]
severity: should-fix
status: draft
lacks: orgs, Google and Envoy back it; needs one more org that caps hedged requests or honours server pushback
lang: core
applies_when: The code sends a second copy of a request to another replica when the first is slow.
context: [server]
tool_gate: none
borrowed_from:
  - https://grpc.io/docs/guides/request-hedging/
  - https://www.envoyproxy.io/docs/envoy/latest/api-v3/config/route/v3/route_components.proto
---

**Rule.** Cap hedged requests with a retry budget or retry limit, and stop hedging when the server asks clients not to retry.

**Why.** A hedge adds load exactly when a backend is slow. With no cap, a slow backend gets more traffic and slows further. A budget and a respected pushback keep hedging a small, bounded cost.

**FAIL**

```yaml
# gRPC service config: hedging with no throttle
methodConfig:
  - name: [{service: "example.Search"}]
    hedgingPolicy:
      maxAttempts: 5
      hedgingDelay: 0.05s
```

**PASS**

```yaml
methodConfig:
  - name: [{service: "example.Search"}]
    hedgingPolicy:
      maxAttempts: 3
      hedgingDelay: 0.05s
      nonFatalStatusCodes: [UNAVAILABLE]
retryThrottling:
  maxTokens: 10
  tokenRatio: 0.1
```

**Counterpoint.** "The hedge delay already limits the extra load." It does when the backend is healthy. In an outage every request passes the delay, so every request is hedged. Only a cap holds then.

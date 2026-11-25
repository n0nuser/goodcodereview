---
id: svc-logs-structured
level: service
tags: [observability, logging]
severity: should-fix
status: stable
lang: core
applies_when: A service ships its logs to an aggregator or search tool and its logger supports key/value fields.
context: [server]
tool_gate: Pylint logging-fstring-interpolation (W1203), .NET analyzer CA2254, or a logger wrapper that accepts only a constant message plus fields.
note: Structured fields - Microsoft (prefer structured telemetry), Kubernetes (unstructured klog calls such as Infof are no longer recommended) and OWASP (do not use unstructured text log formats). No interpolation into the message - Kubernetes, Microsoft (avoid string interpolation in logging) and Python (log variable data as format arguments). The Go slog post describes the benefit and is descriptive only
borrowed_from:
  - https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/observability
  - https://learn.microsoft.com/en-us/dotnet/core/extensions/logging-library-authors
  - https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-instrumentation/logging.md
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://docs.python.org/3/howto/logging.html
  - https://go.dev/blog/slog
---

**Rule.** Log an event as a constant message plus key/value fields; do not build the message by interpolating variable data into it.

**Why.** A formatted string can only be searched by text. Fields can be filtered, grouped and counted, and the message stays one searchable pattern however many orders fail. Interpolation also formats the string even when the level is off, and a value with a newline can forge a log line ([[svc-log-input-neutralised]]). Put the request id in the fields too.

**FAIL**

```go
log.Printf("order %s failed for %s: %v", orderID, userID, err)
```

```python
logger.error(f"order {order_id} failed for {user_id}")
```

**PASS**

```go
slog.Error("order failed", "order_id", orderID, "user_id", userID, "err", err)
```

```python
logger.error("order failed", extra={"order_id": order_id, "user_id": user_id})
```

**Counterpoint.** CLIs and small scripts print text for a person, and a service with no aggregator gains little from fields. The card covers services whose logs are searched by machine. Where the logger has no field support, a format string with arguments (`logger.error("order %s failed", order_id)`) still avoids eager formatting.

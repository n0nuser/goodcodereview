---
id: svc-stream-dont-materialise
level: service
tags: [performance, memory, io]
severity: should-fix
status: draft
lang: core
applies_when: A handler reads, transforms, or returns a result whose size depends on the data (files, query results, response bodies).
tool_gate: Memory limit in tests with a large fixture.
note: Node-specific source, general claim; the unbounded-background-tasks half of the gap has no source and is covered by sys-load-shedding-bounded-queues
borrowed_from:
  - https://nodejs.org/en/learn/modules/backpressuring-in-streams
---

**Rule.** Process large results as a stream with backpressure; do not load them whole into memory.

**Why.** A fast source piles data into memory faster than a slow consumer drains it. In the Node docs' test, memory grew from about 88 MB to about 1.5 GB. Memory then scales with data size, not with the code.

**FAIL**

```python
rows = db.execute("SELECT * FROM events").fetchall()   # 50M rows
return json.dumps(rows)
```

**PASS**

```python
def generate():
    for row in db.execute("SELECT * FROM events"):     # server-side cursor
        yield encode(row)
return StreamingResponse(generate())
```

**Counterpoint.** "Streaming complicates errors and retries." Yes: a failure mid-stream cannot change the status code. For small, bounded results, loading the whole result is simpler and fine; state the bound. [[sys-load-shedding-bounded-queues]] covers queue limits.

---
id: py-httpx-client-lifespan
level: module
tags: [python, resources]
severity: block
status: draft
lang: python
applies_when: A Python service creates `httpx` or DB clients.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Build the pooled client once in the app lifespan and reuse it, with explicit connect and read timeouts. Scope short-lived clients with `with`/`async with`. Never `read=None`. Core rules: [[mod-pooled-clients-built-once]], [[fn-timeouts-on-external-calls]].

**Why.** Per-call clients drop pooling; `read=None` hangs forever.

**FAIL**

```python
async def fetch(u):
    return await httpx.AsyncClient().get(u)
```

**PASS**

```python
@asynccontextmanager
async def lifespan(app):
    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=2.0)) as c:
        app.state.http = c
        yield
```

**Counterpoint.** "Defaults are fine." httpx's default is 5s per phase; whatever the default, set it explicitly so a version change doesn't change behaviour.

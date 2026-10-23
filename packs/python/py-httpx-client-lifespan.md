---
id: py-httpx-client-lifespan
level: module
tags: [python, resources]
severity: should-fix
status: draft
lang: python
applies_when: A Python service creates an `httpx` client.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Pass an explicit `httpx.Timeout` to every `httpx` client.

**Why.** Core rules: [[svc-timeouts]], [[mod-pooled-clients-built-once]]. `read=None` disables the read timeout. Build the client once in the app lifespan and reuse it.

**FAIL**

```python
async def fetch(url):
    async with httpx.AsyncClient(timeout=None) as c:
        return await c.get(url)
```

**PASS**

```python
@asynccontextmanager
async def lifespan(app):
    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=2.0)) as c:
        app.state.http = c
        yield
```

**Counterpoint.** "httpx defaults are fine." They are (5s), but set the value explicitly so a library change cannot silently change behaviour.

---
id: mod-prefer-sync-api
level: module
tags: [correctness, api, concurrency]
severity: discuss
status: draft
lang: core
applies_when: A module wraps protocol, parsing or business logic and offers it to callers that may be sync or async.
tool_gate: none
note: both sources are opinion and neither states this as a rule; the card combines them
borrowed_from:
  - https://sans-io.readthedocs.io/how-to-sans-io.html
  - https://lucumr.pocoo.org/2020/1/1/async-pressure/
---

**Rule.** Keep logic in plain synchronous functions with no I/O, and add async wrappers at the edge only.

**Why.** An async-only API forces every caller into an event loop, doubles testing, and makes accepting work so cheap that overload goes unnoticed. A synchronous core is tested without a loop and serves both worlds.

**FAIL**

```python
async def parse_frame(reader):          # parsing and socket reads fused
    header = await reader.read(4)
    ...
```

**PASS**

```python
def parse_frame(buf: bytes) -> Frame | None: ...   # pure, sync
async def read_frame(reader):                        # thin I/O shell
    return parse_frame(await reader.read(4))
```

**Counterpoint.** "Everything here is async anyway." That is fine for the shell. The test is whether the logic needs I/O to run. If it does not, it should not need `await` either.

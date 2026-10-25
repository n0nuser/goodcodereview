---
id: py-settings-pydantic-settings
level: module
tags: [maintainability, python, config]
severity: should-fix
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: python
applies_when: Python code reads configuration from the environment.
tool_gate: ruff TID251 (banned-api) on `os.environ`
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Load env config with `BaseSettings` from `pydantic_settings`.

**Why.** Core rule: [[mod-central-config]]. `os.environ.get` returns untyped strings with silent defaults, while `BaseSettings` parses, validates, and fails at startup. In pydantic v2, `BaseSettings` is no longer importable from `pydantic`.

**FAIL**

```python
timeout = float(os.environ.get("TIMEOUT", "5"))
```

**PASS**

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    request_timeout_s: float = 5.0
```

**Counterpoint.** "os.environ is stdlib and enough." For one flag, maybe. Past two, you re-implement parsing and error messages at every call site.

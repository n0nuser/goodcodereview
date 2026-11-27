---
id: py-settings-pydantic-settings
level: module
tags: [maintainability, python, config]
severity: should-fix
status: draft
lacks: orgs, no organisation backs it yet; needs three that load environment config through pydantic-settings
lang: python
applies_when: Python code reads configuration from the environment.
tool_gate: ruff TID251 (banned-api) on `os.environ`
borrowed_from:
  - https://pablogonzalez.me/posts/python-code-review-guide/
note: from the author's own Python review guide
---

**Rule.** Load env config with `BaseSettings` from `pydantic_settings`.

**Why.** `os.environ.get` returns untyped strings with silent defaults, while `BaseSettings` parses, validates, and fails at startup. In pydantic v2, `BaseSettings` is no longer importable from `pydantic`.

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

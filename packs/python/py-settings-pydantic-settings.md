---
id: py-settings-pydantic-settings
level: module
tags: [python, config]
severity: should-fix
status: draft
lang: python
applies_when: Python code reads configuration from the environment.
tool_gate: ruff (custom ban on os.environ) or grep gate
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Load env config through `pydantic-settings`, importing `BaseSettings` from `pydantic_settings`, not `pydantic`. Core rule: [[mod-central-config]].

**Why.** `os.environ.get` returns untyped strings with silent defaults. `BaseSettings` parses, validates and fails at startup. Importing from `pydantic` breaks on v2.

**FAIL**

```python
timeout = float(os.environ.get("TIMEOUT", "5"))
```

**PASS**

```python
class Settings(BaseSettings):
    database_url: str
    request_timeout_s: float = 5.0
```

**Counterpoint.** "os.environ is stdlib and enough." For one flag, maybe. Past two, you re-implement parsing and error messages by hand, per call site.

---
id: py-test-collection-and-imports
level: module
tags: [testing, performance, python]
severity: discuss
status: draft
lacks: orgs, "set testpaths" has Trail of Bits; the pytest page only defines the option; needs two more orgs that recommend it
lang: python
applies_when: A pytest run spends seconds collecting tests or importing modules before the first test starts.
tool_gate: pytest `testpaths` in the configuration; `pytest --collect-only` to measure collection.
note: Trail of Bits (testpaths cut collection of 3,900 tests from 7.84 s to 2.60 s; -X importtime found a heavy import) and pytest (the option limits collection to known test directories, a definition) back the Rule. The -X importtime advice in the Why has Trail of Bits and SkyPilot (LazyImport for an import over 100 ms) and has no FAIL or PASS case of its own
borrowed_from:
  - https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/
  - https://docs.pytest.org/en/stable/reference/reference.html
  - https://docs.skypilot.ai/en/v0.10.0/developers/CONTRIBUTING.html
---

**Rule.** Set `testpaths` in the pytest configuration.

**Why.** Collection and imports run before every test run, local or CI, and on every parallel worker. The PyPI suite spent over 6 seconds on discovery alone, 10% of its run after parallelisation. When start-up is still slow, `python -X importtime -m pytest` shows which import costs the time. The `testpaths` setting only helps a run that passes no path, so a CI job that runs `pytest tests/` already skips the walk.

**FAIL**

```toml
[tool.pytest.ini_options]
addopts = "-q"        # pytest walks the whole repository to find tests
```

**PASS**

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q"
```

**Counterpoint.** "A few seconds of start-up is not worth a rule." It is not for a small suite. It matters when the run repeats on every worker and every save, so measure first and skip the card below a few seconds.

---
id: py-paths-from-file
level: function
tags: [correctness, python, io]
severity: should-fix
status: draft
lang: python
applies_when: Python code builds a path to a data file or fixture.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Resolve paths from `__file__`, not the current working directory.

**Why.** A cwd-relative path works from the repo root and fails from CI, an IDE, or an installed package.

**FAIL**

```python
Path("tests/fixtures/data.json")
```

**PASS**

```python
Path(__file__).parent / "fixtures" / "data.json"
```

**Counterpoint.** "Tests always run from the root." That holds until someone runs one test from its directory, or an installer moves it.

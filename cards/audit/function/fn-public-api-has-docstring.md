---
id: fn-public-api-has-docstring
level: function
tags: [maintainability, docs]
severity: discuss
status: stable
lang: core
applies_when: A diff adds a public module, class, function or method.
tool_gate: Ruff `D100` to `D107` (pydocstyle), Checkstyle `MissingJavadocMethod`, Rust `missing_docs` (allow by default).
note: Home Assistant, Python, Microsoft (Azure SDK), Apache Kafka and Drupal state it. Only Home Assistant says a linter enforces it, so the Rule leaves the gate to `tool_gate`
borrowed_from:
  - https://developers.home-assistant.io/docs/development_guidelines/
  - https://peps.python.org/pep-0257/
  - https://azure.github.io/azure-sdk/python_documentation.html
  - https://kafka.apache.org/community/developer/
  - https://project.pages.drupalcode.org/coding_standards/php/documentation/
---

**Rule.** Give each public module, class, function and method a doc comment.

**Why.** The doc comment is the contract a caller reads. Without one, callers read the body and depend on what it happens to do. Keep it short: see `fn-comments-explain-why` for what it adds.

**FAIL**

```python
def retry(fn, times=3):
    for _ in range(times):
        ...
```

**PASS**

```python
def retry(fn, times=3):
    """Call fn until it succeeds or times attempts are used up."""
    for _ in range(times):
        ...
```

**Counterpoint.** "Getters and obvious one-liners get a restating docstring." Skip those, or give them a one-line summary that adds the unit or the failure case. A docstring that only repeats the name is worse than none.

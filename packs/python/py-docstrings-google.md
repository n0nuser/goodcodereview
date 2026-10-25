---
id: py-docstrings-google
level: function
tags: [maintainability, python, docs]
severity: discuss
status: draft
lacks: orgs, Google's review guide is the only backer; needs two more orgs
lang: python
applies_when: A Python function or class has, or lacks, a docstring.
tool_gate: ruff D (convention=google, D1xx ignored)
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
---

**Rule.** Write a Google-style docstring only when it adds what the signature cannot say.

**Why.** Forced docstrings restate the signature and rot. The ones that matter state units, side effects, and what callers may rely on. The gate never forces presence; it checks format only.

**FAIL**

```python
def add(a, b):
    """Add a and b. :param a: first number"""
```

**PASS**

```python
def charge(order):
    """Charge the card once; safe to retry with the same order id (idempotent)."""
```

**Counterpoint.** "Every public function needs a docstring." Ousterhout would sympathise (missing docs cost more than wrong ones), and Martin would not. The compromise here is to require content that adds information, not presence.

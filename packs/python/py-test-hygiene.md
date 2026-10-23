---
id: py-test-hygiene
level: module
tags: [python, testing]
severity: discuss
status: draft
lang: python
applies_when: A Python test suite is added or changed.
tool_gate: none
borrowed_from:   []  # first-hand: author's own Python review guide
---

**Rule.** Mirror the source layout, keep shared fixtures in `tests/fixtures/` and single-use fixtures local with the narrowest scope, freeze time, and no outbound network. Blank lines separate arrange/act/assert; no section comments. A bug gets a failing regression test first.

**Why.** Tests that depend on clock or network flake; a fixture used once but defined globally is noise; a fix without a failing test may not fix anything.

**FAIL**

```python
# Arrange
user = ...
# Act
r = f(user)
```

**PASS**

```python
user = ...

r = f(user)

assert r == expected
```

**Counterpoint.** "The comments help newcomers." The blank-line structure does the same without comments that are trivially stale.

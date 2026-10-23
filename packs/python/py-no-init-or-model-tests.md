---
id: py-no-init-or-model-tests
level: module
tags: [python, testing]
severity: should-fix
status: draft
lang: python
applies_when: The diff adds `test_init_*` or a test file for a plain model or dataclass.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Cover `__init__` and plain models through the behaviour that uses them.

**Why.** Such tests restate the class and break on every field change without proving behaviour.

**FAIL**

```python
def test_init_sets_name(): assert User(name="a").name == "a"
```

**PASS**

```python
def test_welcome_email_uses_user_name(): ...
```

**Counterpoint.** "Validators on the model need tests." Yes: test the validator's behaviour (valid and invalid input), not that assignment works.

---
id: fn-no-native-deserialise-untrusted
level: function
tags: [security, deserialisation]
severity: block
status: draft
lang: core
applies_when: Code turns bytes or text from outside the process into objects.
tool_gate: SAST rules for `pickle.load`, `yaml.load`, `ObjectInputStream`, `BinaryFormatter`, `unserialize`.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Deserialization_Cheat_Sheet.html
  - https://docs.python.org/3/library/pickle.html
  - https://learn.microsoft.com/en-us/dotnet/standard/serialization/binaryformatter-security-guide
  - https://docs.oracle.com/en/java/javase/21/core/serialization-filtering1.html
  - https://codeql.github.com/codeql-query-help/python/py-unsafe-deserialization/
---

**Rule.** Parse untrusted input with a data-only format and a schema, never with a native object deserialiser.

**Why.** `pickle`, `ObjectInputStream`, `BinaryFormatter` and full-power YAML loaders can run attacker-chosen code while they load, so validating after the call is too late. JSON or a schema-checked format cannot instantiate arbitrary classes.

**FAIL**

```python
obj = pickle.loads(request.data)
cfg = yaml.load(body, Loader=yaml.Loader)
```

**PASS**

```python
obj = Model.model_validate_json(request.data)
cfg = yaml.safe_load(body)
```

**Counterpoint.** "The data comes from our own queue." Anyone who can write to the queue can run code on every consumer. If native serialisation stays, sign the payload and verify the signature before reading it.

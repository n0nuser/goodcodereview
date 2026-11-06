---
id: fn-known-keys-get-a-type
level: function
tags: [correctness, types]
severity: should-fix
status: draft
lacks: orgs, "record type for fixed keys" has PSF and attrs; mypy and PEP 589 share an author; needs one more org
lang: core
applies_when: A function takes or returns a dictionary whose keys are fixed and known.
tool_gate: partial: mypy --disallow-any-explicit flags a `dict[str, Any]` annotation; once the code uses a TypedDict, an invalid key is an error under mypy
note: Python Software Foundation (PEP 589: Dict[str, Any] is too lenient) and attrs ("Dictionaries are not for fixed fields") state the practice; PEP 589 and mypy come from the same author, so mypy's page counts as a feature description; attrs alone says to keep a map for open keys, so that clause sits in the Why
borrowed_from:
  - https://mypy.readthedocs.io/en/stable/typed_dict.html
  - https://peps.python.org/pep-0589/
  - https://www.attrs.org/en/stable/why.html
---

**Rule.** Give a fixed key set a record type: a model, a dataclass or a typed dict.

**Why.** A bag of keys hides the contract. A mistyped key is a runtime `KeyError` or, worse, a silently absent value. PEP 589 says `Dict[str, Any]` is "too lenient, as arbitrary string keys can be used", and mypy reports an invalid TypedDict key as an error. A map stays the right type when the keys are open: attrs puts it as "if your dict has a fixed and known set of keys, it is an object, not a hash".

**FAIL**

```text
def summary(o) -> dict[str, Any]:
    return {"id": o.id, "totl": o.total}
```

**PASS**

```text
@dataclass(frozen=True)
class Summary:
    id: int
    total: Decimal
```

**Counterpoint.** "A dict serialises for free and JSON is dictionary-shaped." A typed dict is still a dict at runtime, so the wire format does not change; use it for JSON-shaped records. A dataclass or model needs a dump step, so pick the record type that matches the boundary. A map with open keys stays generic.

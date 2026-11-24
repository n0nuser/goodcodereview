---
id: fn-doc-params-match-signature
level: function
tags: [maintainability, docs, correctness]
severity: discuss
status: stable
lang: core
applies_when: A diff changes the parameters of a function that has a doc comment, or adds a doc comment that lists parameters.
tool_gate: Ruff `D417` (missing argument descriptions), `DOC102`, Checkstyle `JavadocMethod`, or the compiler's doc warning (C# `CS1572`, `CS1573`).
note: Drupal, Microsoft (.NET) and Python PEP 257 state it. Google's guide only says to list each parameter, which is coverage
borrowed_from:
  - https://project.pages.drupalcode.org/coding_standards/php/documentation/
  - https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags
  - https://peps.python.org/pep-0257/
---

**Rule.** Make the parameters a doc comment lists match the function's signature, by name and in number.

**Why.** Callers pass keyword arguments by the documented name. A renamed, added or removed parameter left out of the doc sends them to a name that no longer exists.

**FAIL**

```python
def send(to, subject, body):
    """Send a message.

    Args:
        recipient: Who gets it.
    """
```

**PASS**

```python
def send(to, subject, body):
    """Send a message.

    Args:
        to: Who gets it.
        subject: The subject line.
        body: The message text.
    """
```

**Counterpoint.** "Obvious parameters need no description." Then leave the list out. The rule is against a list that disagrees with the signature, not against a short one.

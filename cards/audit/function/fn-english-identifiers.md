---
id: fn-english-identifiers
level: function
tags: [naming, readability]
severity: discuss
status: draft
lang: core
applies_when: The project has a written language policy, or its code may be read by people outside one language group.
tool_gate: Spell-check or non-ASCII identifier lint.
note: weak source; PEP 8 states this for the standard library only, so the card is a project-policy check
borrowed_from:
  - https://peps.python.org/pep-0008/
---

**Rule.** Write identifiers and comments in English, unless the project policy names another language.

**Why.** Mixed languages split search, break naming conventions and exclude readers. Tools, libraries and error messages the code touches are English already.

**FAIL**

```text
def calcular_precio_total(carrito): ...   # next to total_price() and cart.items
```

**PASS**

```text
def calculate_total_price(cart): ...
```

**Counterpoint.** "Domain terms have no English word." Keep the local term, once, in a glossary and comment it ([[mod-one-name-per-concept]]). If the code will never leave one language group, a team may choose otherwise; write that choice down so the check can pass.

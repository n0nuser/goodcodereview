---
id: fn-english-identifiers
level: function
tags: [maintainability, naming, readability]
severity: discuss
status: draft
lacks: orgs, PEP 8 and LLVM give the rule and PEP 3131 argues the other way; needs a third org that mandates English
lang: core
applies_when: The project has a written language policy, or its code may be read by people outside one language group.
tool_gate: Spell-check or non-ASCII identifier lint.
note: no source makes English universal; PEP 8 and LLVM give the rule, PEP 3131 the counter-view, so the card stays a project-policy check
borrowed_from:
  - https://peps.python.org/pep-0008/
  - https://peps.python.org/pep-3131/
  - https://llvm.org/docs/CodingStandards.html
---

**Rule.** Write identifiers and comments in English, unless the project policy names another language.

**Why.** Mixed languages split search, break naming conventions, and exclude readers. The tools, libraries, and error messages the code touches are already in English.

**FAIL**

```text
def calcular_precio_total(carrito): ...   # next to total_price() and cart.items
```

**PASS**

```text
def calculate_total_price(cart): ...
```

**Counterpoint.** "Domain terms have no English word." Keep the local term, once, in a glossary, and comment it ([[mod-one-name-per-concept]]). Python itself allows non-ASCII identifiers so that teams can name things in their own language (PEP 3131). If the code will never leave one language group, a team may choose that language. Write the choice down so the check can pass.

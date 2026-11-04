---
id: mod-one-name-per-concept
level: module
tags: [maintainability, naming]
severity: should-fix
status: stable
lang: core
applies_when: The change introduces or reuses names for domain concepts.
tool_gate: none
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://github.com/island-is/handbook/blob/master/docs/api-design-guide/naming-conventions.md
  - https://github.com/tum-esi/common-coding-conventions
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md
---

**Rule.** Use one name for one concept across the codebase.

**Why.** If `customer`, `client`, and `account` all mean the same thing, readers wonder whether they differ. A name that misdescribes behaviour is worse than a vague one. Follow the project glossary, and never choose a name that says something the code does not do.

**FAIL**

```text
get_customer(); load_client(); fetch_account()   # same entity
def profile_data(df): ...   # inspects column types, not performance
```

**PASS**

```text
get_customer(); load_customer(); fetch_customer()
def discover_structure(df): ...
```

**Counterpoint.** "Names are bikeshedding." Reviewers should not argue taste. They should check that the name is consistent and true. Vague names (names that could mean many things) are a design smell in Ousterhout's list. Do not rename wholesale in a feature change; make the rename a separate change.

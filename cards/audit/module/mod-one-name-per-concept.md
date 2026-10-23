---
id: mod-one-name-per-concept
level: module
tags: [naming]
severity: should-fix
status: draft
lang: core
applies_when: The change introduces or reuses names for domain concepts.
tool_gate: none
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** Use one name per concept across the codebase, the project's glossary terms, and never a name that says something the code does not do.

**Why.** If `customer`, `client` and `account` all mean the same thing, readers wonder whether they differ. A name that misdescribes behaviour is worse than a vague one.

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

**Counterpoint.** "Names are bikeshedding." Reviewers should not argue taste. They should check that the name is consistent and true. Vague names (could mean many things) are a design smell in Ousterhout's list. Do not rename wholesale in a feature change; mark it separately.

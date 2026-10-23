---
id: fn-no-pass-through-wrapper
level: function
tags: [design, readability]
severity: should-fix
status: draft
lang: core
applies_when: A method's whole body calls a collaborator's method of the same name with the same arguments.
tool_gate: none
borrowed_from:
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md
---

**Rule.** Delete a method that only forwards. Keep wrappers that validate, adapt or narrow.

**Why.** A pass-through adds an interface to learn and a hop to step over, and gives no abstraction. Changing the signature now means editing two places.

**FAIL**

```text
class UserService:
    def get(self, id): return self.repo.get(id)
```

**PASS**

```text
# callers use repo.get(id) directly,
# or the service adds something: check access, map to a domain error
```

**Counterpoint.** "The service layer should expose everything for uniformity." Uniform emptiness is still emptiness. If a layer boundary is the goal, say what the layer adds. The Clean Code side of the Ousterhout debate favours small forwarding methods more readily, so treat this as a design call, not a law.
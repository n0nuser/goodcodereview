---
id: chg-new-api-has-usage
level: change
tags: [maintainability, api, yagni]
severity: should-fix
status: draft
lang: core
applies_when: The change adds a public function, endpoint, option, interface or extension point.
tool_gate: Unused-export or dead-code detection in CI.
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://go.dev/wiki/CodeReviewComments
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
---

**Rule.** Ship new API with at least one real caller in the same change, and fail speculative interfaces and options that nothing uses.

**Why.** Unused API has no proof it fits real needs, yet once published it must be kept. Interfaces designed before a consumer exists usually get the shape wrong. See also [[mod-yagni]].

**FAIL**

```text
+ class StorageBackend(Protocol): ...      # one implementation, no second planned
+ def export(fmt="csv", compress=False, ...)  # nothing calls compress=True
```

**PASS**

```text
+ export_csv(rows)   # called by the report job in the same PR
```

**Counterpoint.** Library authors must ship API ahead of users. Then the usage is an example or test in the change, and the surface stays minimal. The Go guidance (declare interfaces where consumed, return concrete types) points the same way.

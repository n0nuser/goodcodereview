---
id: mod-single-writer-per-state
level: module
tags: [concurrency, ownership]
severity: should-fix
status: draft
lang: core
applies_when: More than one module, worker or process writes the same state.
tool_gate: none
note: one vendor's engineering guidance (opinion), from pstack principle-separate-before-serializing-shared-state
borrowed_from:
  - https://github.com/cursor/plugins
---

**Rule.** Give each writer its own state and merge on read, and where sharing is unavoidable, enforce one writer with a lock, a single owner or compare-and-swap.

**Why.** A convention such as "only write your own field" is not concurrency control. Two workers writing different fields of one file still overwrite each other, and a change needs edits in every writer.

**FAIL**

```text
worker A and worker B each load state.json, set their own key, and save the whole file
```

**PASS**

```text
state/a.json and state/b.json, one writer each; readers merge them
```

**Counterpoint.** "Separate files complicate reads." A merge on read is one function. Shared state with a real lock is acceptable when the actors truly need the same object; [[sys-lock-fencing]] covers the lock case.

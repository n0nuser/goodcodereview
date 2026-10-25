---
id: mod-single-writer-per-state
level: module
tags: [correctness, concurrency, ownership]
severity: should-fix
status: stable
lang: core
applies_when: More than one module, worker or process writes the same state.
tool_gate: none
note: one writer at a time is backed by cursor/plugins, Netflix (an exclusive queue lets one worker evaluate a workflow at a time), Cabify (CI deploy runs that were not mutually exclusive reverted each other, replaced by one GitOps controller) and GitHub (writes to one reference are serialised); giving each writer its own state and merging on read has cursor/plugins and GitHub only, so it sits in Why
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-separate-before-serializing-shared-state/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/architect/references/design-red-flags.md
  - https://netflixtechblog.com/netflix-conductor-the-next-chapter-41ad21067649
  - https://tech.cabify.com/blog/engineering/scaling-argocd-to-dozens-testing-environments
  - https://github.blog/engineering/architecture-optimization/the-bridge-to-agent-scale-git-infrastructure
---

**Rule.** Let only one writer change a piece of state at a time, through a single owner, a queue that serialises the writes, or compare-and-swap, never by convention.

**Why.** A convention such as "only write your own field" is not concurrency control. Two workers writing different fields of one file still overwrite each other, and two deploy runs that overlap can undo each other's changes. Better still, split the state so that each writer owns its part and readers merge the parts: writers to different parts then never wait for each other.

**FAIL**

```text
worker A and worker B each load state.json, set their own key, and save the whole file
```

**PASS**

```text
workers send updates to one queue; a single consumer applies them to state.json in order
or: state/a.json and state/b.json, one writer each; readers merge them
```

**Counterpoint.** "A lock is simpler than a queue or an owner." A lock works only when the store rejects a writer whose lock has expired; see [[sys-lock-fencing]]. Without that check, a paused holder can wake up and write after another writer took over.

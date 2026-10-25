---
id: fn-variants-as-tagged-union
level: function
tags: [maintainability, types, modelling]
severity: should-fix
status: draft
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs
lang: core
applies_when: A type or function models a value that is one of several variants or states.
tool_gate: A type checker with exhaustiveness checking (`never` in TypeScript, `assert_never` in Python).
note: one vendor's engineering guidance (opinion), from pstack principle-model-the-domain and typescript-best-practices
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-model-the-domain/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/typescript-best-practices/SKILL.md
---

**Rule.** Model variants as a tagged union, and make every switch over it fail the build when a variant is unhandled.

**Why.** A bag of optional fields or booleans that must stay in sync allows states that mean nothing, and each reader has to know which combinations are legal. A new variant then slips past every switch that lacks an exhaustiveness check.

**FAIL**

```ts
type Job = { running: boolean; failed: boolean; error?: string; result?: Result }
```

**PASS**

```ts
type Job =
  | { kind: "running" }
  | { kind: "failed"; error: string }
  | { kind: "done"; result: Result }

default: { const _: never = job; throw new Error("unhandled") }
```

**Counterpoint.** "Two booleans are simpler." They are until a third state appears or the booleans disagree. For a true on/off flag with no related fields, a boolean is fine.

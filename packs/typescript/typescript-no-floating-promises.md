---
id: typescript-no-floating-promises
level: function
tags: [correctness, reliability, typescript]
severity: should-fix
status: draft
lacks: duplicate, the stable card fn-handle-rejected-promises covers unhandled rejections; merge or delete
lang: typescript
applies_when: TypeScript code calls an async function or creates a Promise.
tool_gate: "@typescript-eslint/no-floating-promises"
borrowed_from:
  - https://typescript-eslint.io/rules/no-floating-promises/
---

**Rule.** Every Promise is awaited, returned, or given a `.catch`; enable `@typescript-eslint/no-floating-promises`.

**Why.** A Promise nobody handles turns a failure into an unhandled rejection, or into work that finishes after the code assumed it was done.

**FAIL**

```ts
async function onSave() {
  saveDraft(doc); // returns a Promise; errors vanish
  closeDialog();
}
```

**PASS**

```ts
async function onSave() {
  await saveDraft(doc);
  closeDialog();
}
```

**Counterpoint.** "Fire-and-forget is intended." Mark it with `void saveDraft(doc).catch(report)` so the choice is visible and failures are still reported.

---
id: typescript-strict-mode
level: codebase
tags: [correctness, maintainability, typescript]
severity: should-fix
status: draft
lacks: orgs, only Microsoft's tsconfig reference states it; needs two more organisations
lang: typescript
applies_when: The repository has a `tsconfig.json`.
tool_gate: tsc
borrowed_from:
  - https://www.typescriptlang.org/tsconfig/
---

**Rule.** `tsconfig.json` sets `"strict": true`; switch off a single strict flag only with a written reason.

**Why.** The strict family (null checks, implicit `any`, strict function types) is where most type errors that reach users are caught. Without it, `tsc` passing says little.

**FAIL**

```json
{ "compilerOptions": { "target": "ES2022", "strict": false } }
```

**PASS**

```json
{ "compilerOptions": { "target": "ES2022", "strict": true } }
```

**Counterpoint.** "Migrating a big codebase is too costly." Enable it per flag, or per package with project references, and ratchet; do not leave it off by default for new code.

---
id: code-gate-new-violations-only
level: codebase
tags: [maintainability, process, ci, quality-gates]
severity: should-fix
status: draft
lacks: orgs, SonarSource (a vendor) and ArchUnit back it; needs one more org that gates on new code and keeps old violations apart
lang: core
applies_when: Auditing a codebase that adopted a linter, a quality gate or an architecture rule after most of its code existed.
tool_gate: A baseline or frozen violation store with CI set to read it but not rewrite it (ArchUnit `FreezingArchRule`, a linter baseline file).
borrowed_from:
  - https://www.sonarsource.com/blog/legacy-codebases-are-a-devops-issue/
  - https://www.archunit.org/userguide/html/000_Index.html
---

**Rule.** Gate CI on new or modified code, and track pre-existing violations in a separate store without letting a build add to it.

**Why.** A gate that fails on thousands of old findings gets switched off, and a gate with no record of them lets the debt grow unseen. Failing only on new findings keeps the gate on and stops the debt growing, and the store shows what is left to pay down.

**FAIL**

```properties
# archunit.properties
freeze.store.default.allowStoreCreation=true
freeze.store.default.allowStoreUpdate=true
```

CI regenerates the store on each run, so a new violation is absorbed and the build stays green.

**PASS**

```properties
# archunit.properties
freeze.store.default.path=archunit_store
freeze.store.default.allowStoreCreation=false
freeze.store.default.allowStoreUpdate=false
```

```java
@ArchTest
static final ArchRule no_cycles =
    FreezingArchRule.freeze(slices().matching("com.app.(*)..").should().beFreeOfCycles());
```

**Counterpoint.** "A baseline hides real problems." It lists them in a file under version control, in plain view, and a change that touches a baselined spot is held to the full rule. Pair it with a plan to shrink the store.

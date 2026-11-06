# Coupling research: organisations behind E1, E2, E3

Goal: find independent ORGANISATION sources so three draft cards on coupling can become stable. Each claim is a candidate Rule line. A source counts when it states a practice (recommendation, rule with a documented default/threshold, or a team describing what it does and why). People are listed apart and never count toward the three.

Org convention used here (from `docs/PROMOTION.md`): Go, Bazel, web.dev, SRE books and the Go blog are all **Google** (one org). GitHub hosts count by repository owner, so the ESLint import plugin is **import-js**, ArchUnit is **TNG**, Pylint is **PyCQA**.

---

## E1 — No circular dependencies between modules/packages/files (acyclic dependency graph)

1. `https://go.dev/ref/spec` (org: Google). The Go spec's "Import declarations" section makes cycles a hard error: "An import declaration declares a dependency relation between the importing and imported package. It is illegal for a package to import itself, directly or indirectly, or to directly import a package without referring to any of its exported identifiers." A compile error, so it is a language-level gate, not just style. Backs **E1**.

2. `https://bazel.build/concepts/dependencies` (org: Google, same org as #1). "The *depends upon* relation induces a Directed Acyclic Graph (DAG) over targets, and it is called a *dependency graph*." Build targets form a DAG by definition. Backs **E1** (no new org).

3. `https://doc.rust-lang.org/cargo/reference/resolver.html` (org: Rust / Cargo team). "Usually the resolver does not allow cycles in the graph, but it does allow them for dev-dependencies." and, on the dev-dependency exception, "If possible, try to split your package into multiple packages and restructure it so that it remains strictly acyclic." Crate-level cycles are disallowed. Backs **E1**.

4. `https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/no-cycle.md` (org: import-js). "Ensures that there is no resolvable path back to this module via its dependencies." Detects cycles "of depth 1 … to ∞". Also: "Cyclic dependency are **always** a dangerous anti-pattern". Tool gate: `import/no-cycle` (no numeric threshold; on/off, `maxDepth` defaults to ∞). Backs **E1**.

5. `https://nx.dev/docs/kb/resolve-circular-dependencies` (org: Nrwl). "A circular dependency is when a project transitively depends on itself. This can cause problems in the design of your software… The lint rule, `@nx/enforce-module-boundaries`, will produce an error if any circular dependencies are created…". Tool gate: `@nx/enforce-module-boundaries`. Backs **E1**.

6. `https://www.archunit.org/userguide/html/000_Index.html` (org: TNG Technology Consulting). The intro says ArchUnit can "check for cyclic dependencies and more"; the Library API has `SlicesRuleDefinition.slices().matching("..myapp.(*)..").should().beFreeOfCycles()` and the guide says to "check those slices for cyclic dependencies". Tool gate: ArchUnit `beFreeOfCycles()`. Backs **E1**.

7. `https://pylint.pycqa.org/en/stable/user_guide/messages/refactor/cyclic-import.html` (org: PyCQA / Pylint). Rule `cyclic-import / R0401`; "Message emitted: Cyclic import (%s). Description: Used when a cyclic import between two or more modules is detected." Tool gate: `R0401` (`cyclic-import`). Backs **E1**.

Distinct organisations for E1: **Google, Rust, import-js, Nrwl, TNG, PyCQA** = 6 (high confidence).

Tool-gate notes for E1: `import/no-cycle` (ESLint), `R0401` (Pylint), `@nx/enforce-module-boundaries` (Nx), ArchUnit `beFreeOfCycles()` all exist as rules and act as CI gates. Ruff does **not** implement a cyclic-import rule yet (`PLR0401` is an open request, astral-sh/ruff issue #2914).

---

## E2 — Do not reach through objects (Law of Demeter / "tell, don't ask")

1. `https://pmd.github.io/pmd/pmd_rules_java_design.html#lawofdemeter` (org: PMD). "The law of Demeter is a simple rule that says 'only talk to friends'. It forbids fetching data from 'too far away', for some definition of distance, in order to reduce coupling between classes or objects of different levels of abstraction." It models call-chain "degree" and reports getter chains past a threshold: "The default `trustRadius` of 1 corresponds to the original law of Demeter (you're only allowed one getter call on untrusted values)." Tool gate: PMD `LawOfDemeter` (property `trustRadius`, default 1). Backs **E2** and documents the chain-length threshold.

2. `https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html` (org: Google). Item 2 of the "Writing Testable Code" list is "**Ask for things, Don't look for things (aka Dependency Injection / Law of Demeter)**", and the body says "Only ask for things you directly need, If you are a CarEngine, don't ask for FuelTank, only ask for Fuel." It links a companion post "Breaking the Law of Demeter is Like Looking for a Needle in the Haystack". Backs **E2**.

Distinct organisations for E2: **PMD, Google** = 2 (needs one more). I could not find a third organisation with a clean, fetchable rule or guidance page:

- **JetBrains / ReSharper**: searches for an official "Law of Demeter" inspection page returned nothing on jetbrains.com. Likely not a ReSharper inspection. UNFETCHED/absent.
- **SonarSource**: community forum threads reference a "Law of Demeter violation" in the context of rule `java:S5778`, but I could not fetch a canonical `rules.sonarsource.com` page for a LoD rule (RSPEC-5778 returned 404 on my guessed path). Not confirmed as a LoD rule. UNFETCHED (canonical page).
- **Swift API Design Guidelines / Rust clippy / RuboCop / Checkstyle**: none has a Law-of-Demeter rule or guidance that I could locate.

---

## E3 — High fan-out: a unit that depends on too many others

1. `https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1506` (org: Microsoft). Rule CA1506 "Avoid excessive class coupling": "This rule measures class coupling by counting the number of unique type references that a type, method, field, property, or event contains. The default coupling threshold is 95 for types and 40 for other symbol kinds." And the rationale: "Types, methods, and other symbols that have a high degree of class coupling can be difficult to maintain." Tool gate: `CA1506` (thresholds 95 / 40). Note: it lists "Enabled by default in .NET 10: No". Backs **E3**.

2. `https://checkstyle.sourceforge.io/checks/metrics/classfanoutcomplexity.html` (org: Checkstyle). `ClassFanOutComplexity`: "Checks the number of other types a given class/record/interface/enum/annotation relies on. Also, the square of this has been shown to indicate the amount of maintenance required." Property `max` default **20**. Tool gate: Checkstyle `ClassFanOutComplexity` (default 20). Backs **E3**.

3. `https://github.com/import-js/eslint-plugin-import/blob/main/docs/rules/max-dependencies.md` (org: import-js). `import/max-dependencies`: "Forbid modules to have too many dependencies (`import` or `require` statements). This is a useful rule because a module with too many dependencies is a code smell, and usually indicates the module is doing too much." Option `max` default **10**. Tool gate: `import/max-dependencies` (default 10). Backs **E3**.

4. `https://pmd.github.io/pmd/pmd_rules_java_design.html` (org: PMD). Two rules. `CouplingBetweenObjects`: "This rule counts the number of unique attributes, local variables, and return types within an object. A number higher than the specified threshold can indicate a high degree of coupling." Property `threshold` default **20**. `ExcessiveImports`: "A high number of imports can indicate a high degree of coupling within an object." Property `minimum` default **30**. Tool gates: PMD `CouplingBetweenObjects` (20) and `ExcessiveImports` (30). Backs **E3**.

Distinct organisations for E3: **Microsoft, Checkstyle, import-js, PMD** = 4 (high confidence).

---

## Counter-evidence

- **E1** — `https://docs.python.org/3/faq/programming.html` "How can I have modules that mutually import each other?" answers with workarounds rather than a ban ("It is sometimes necessary to move imports to a function or class to avoid problems with circular imports"), so Python the language does not forbid cycles. Rust likewise permits module-level cycles (only *crate* dependencies must be acyclic), and Cargo explicitly allows dev-dependency cycles. So E1's claim holds at the module/package *boundary* where the language/build tool forbids it, but is not universal.
- **E2** — The Law of Demeter is contested: Ted Kaminski, "You should break the Law of Demeter" (personal blog, `tedinski.com`), argues chaining is often fine. Martin Fowler's "TellDontAsk" (person) is the same idea from the other direction. Neither is an organisation.
- **E3** — No direct counter-evidence found. Note CA1506 is not on by default in .NET 10, and every E3 gate except `import/max-dependencies` is an opt-in/configured rule rather than a default error.

## Also read, no rule

- `Pylint too-many-imports` (default `max-imports`): present only in old Pylint 1.x (`docs.pylint.org/features.html`); removed from current Pylint (4.x), whose messages list no import-count rule. Do not use as a tool gate.
- **Ruff**: no `too-many-imports`/fan-out rule, and no cyclic-import rule yet (astral-sh/ruff #2914 is an open feature request for `PLR0401`). PLR0914 is `too-many-locals`, not import fan-out.
- **SonarSource**: does have circular-dependency rules for Java/JS — `S7027` ("Circular dependencies between classes in the same package") and `S7197` ("Circular file imports should be resolved") per SonarSource's own community announcements — but I did not fetch a canonical `rules.sonarsource.com` page, so they are listed here, not counted.
- **Gradle / Maven**: cyclic project dependencies are a build error in practice, but I found no single canonical "the dependency graph must be acyclic" practice page to cite (Stack Overflow / forum threads only).
- **Google SWE book** (Dependency Management chapter): the task named it; I did not fetch it (it is Google, already counted via the Go spec and Bazel, so it would add no new organisation for E1).

## People cited (never count)

- Miško Hevery (Google Testing Blog, E2) — speaks for Google, counted through Google's page.
- Karl Lieberherr — Law of Demeter originator (PMD cites Lieberherr & Holland 1989).
- Martin Fowler — "TellDontAsk" (person).

## Per-claim confidence

- **E1**: 6 distinct organisations (Google, Rust, import-js, Nrwl, TNG, PyCQA). Strong — meets the three-org bar with margin. The Rule should be scoped to "the dependency graph must be acyclic at the module/package boundary" to respect the Python/Rust counter-evidence.
- **E2**: 2 distinct organisations (PMD, Google). Not yet promotable — needs a third independent org with a fetchable rule or practice page. PMD is the only tool that sets a chain-length threshold (`trustRadius`, default 1).
- **E3**: 4 distinct organisations (Microsoft, Checkstyle, import-js, PMD). Strong — meets the bar. Tool gates exist with real defaults (95/40, 20, 10, 20/30).

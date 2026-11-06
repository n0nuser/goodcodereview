# Judge report: other cards (Sonnet), read 2026-11-06

Method: read AGENTS.md, CONTRIBUTING.md, PROMOTION.md, tools/orgs.py, `git diff` for the 9 edited cards, then fetched every `borrowed_from` URL once and searched the text for the quoted or claimed practice. A hostile-bot block means a page is UNFETCHED. Org counts use `tools/orgs.py`; a person never counts; the creator exception (ADR 0001) is noted where it carries a card.

UNFETCHED (HTTP 403, no usable text): `checkstyle.sourceforge.io` (2 URLs), `intellij-support.jetbrains.com/.../206544839`, `medium.com/alan/...`, and `code.visualstudio.com/docs/configure/settings`. For Checkstyle I read the defaults from the project's source (`DEFAULT_MAX_PARAMETERS = 7`, `DEFAULT_MAX_LINES = 150`). For VS Code I read the page's source Markdown (`microsoft/vscode-docs`, `docs/configure/settings.md`). The Alan article and the JetBrains support article stay UNFETCHED. Apple's Xcode Cloud page renders by script, so I read its JSON feed.

Severity key: **act** = fix before the card ships or stays stable; **consider** = maintainer's call.

---

## fn-comments-explain-why — ISSUES

1. **consider**, check 6. The new Why sentence "The comment is evidence that the code needs one." has no clear antecedent for "one" (a rename? an extraction?). "Rename before commenting" is also now said twice in the same paragraph (`fn-comments-explain-why.md`, Why). Fix: merge into "When a comment explains how the code works, rename the thing or extract the step first."
2. **consider**, check 4. The second FAIL line `retry = False  # see the PR, currently disabled` is the FAIL case of stable `fn-comments-survive-context` ("no 'currently', 'for now' or 'see the PR'"). Using it here blurs the two cards. Fix: use a pure restating line or a comment with no reason.

Sources, all fetched. "Reason, not restatement":
- Google eng-practices: "comments are useful when they explain why some code exists, and should not be explaining what some code is doing … If the code isn't clear enough to explain itself, then the code should be made simpler."
- MDN: "restating the code in prose is not a good use of comments"; "If the purpose or logic of the code isn't obvious, add a comment with your intention." The page is guidance for documentation code examples, which is a scope caveat.
- Apache Flink: "In-code comments help explain the 'why'"; they "should not state redundant information about the 'what' and 'how'".
- PEP 8: "Inline comments are unnecessary … if they state the obvious"; `x = x + 1  # Compensate for border` is "useful".

For the Why (rename or extract first):
- Google: "the code should be made simpler".
- Linux kernel: "NEVER try to explain HOW your code works in a comment: it's much better to write the code so that the working is obvious". The kernel also says comments should say "WHAT your code does, not HOW", at function-head level. That is compatible, but it is not "give a reason".
- Refactoring.Guru Comments smell: "If a comment explains a section of code, this section can be turned into a separate method via Extract Method"; "give the method a self-explanatory name".

---

## fn-known-keys-get-a-type — ISSUES

1. **act**, check 2. The Rule's second clause, "use a generic map only for open keys", has one backer, attrs: "Dictionaries are not for fixed fields. If you have a dict, it maps something to something else … if your dict has a fixed and known set of keys, it is an object, not a hash." mypy and PEP 589 only back the first clause. PROMOTION rule 2: a clause with fewer than three orgs moves to the Why. Fix: move "use a generic map only for open keys" to the Why, or add two organisations that say it.
2. **consider**, check 1 and 3. mypy's TypedDict page describes a feature: "TypedDict lets you give precise types for dictionaries that represent objects with a fixed schema." That is a definition page (PROMOTION rule 3). PEP 589's rationale ("`Dict[str, Any]` … is too lenient, as arbitrary string keys can be used") is the stronger text, but PEP 589 came from the mypy team, so the two are one source in practice. Independent practice statements for clause 1 come from attrs and PEP 589.
3. **consider**, check 3. `tool_gate: mypy --strict; an invalid TypedDict key is an error` does not catch the card's FAIL. mypy's `--strict` flag list starts `--disallow-any-generics, --disallow-subclassing-any, --disallow-untyped-calls, --disallow-untyped-defs …`. `--disallow-any-explicit` is a separate flag, so `-> dict[str, Any]` passes strict mode. A TypedDict key error only fires after the code already uses a TypedDict. Fix: name `--disallow-any-explicit` in the gate, or set the gate to `none`.

---

## fn-no-stringly-typed-returns — ISSUES

1. **act**, check 4 and 3. The edited Rule, "a closed type … for a closed set of API values, not a bare string or boolean", now overlaps stable `fn-bool-arg-at-callsite` ("Replace a boolean flag argument with an enum, keyword-only argument or two functions") and `fn-variants-as-tagged-union`. "Or boolean" also over-reaches: `def is_valid(x) -> bool` returns a closed two-value set and would FAIL by the letter. PROMOTION rule 8: merge or delete. Fix: revert the Rule to strings (or "string or status code"), and leave booleans to `fn-bool-arg-at-callsite`.
2. **act**, check 1 and 2. Per-clause support for "closed type, not a bare string" on **returns**:
   - Microsoft: yes. "DO use an enum to strongly type parameters, properties, and return values that represent sets of values"; "DO NOT use an enum for open sets".
   - Rust API guidelines C-CUSTOM-TYPE: "Arguments convey meaning through types … use a deliberate type (whether enum, struct, or tuple)". It covers arguments and `bool`, not returns or strings.
   - Apple WWDC20 10680: a talk on refining Objective-C for Swift ("these collections of string constants could use the same treatment … NS_STRING_ENUM"). It is interop advice for ObjC constants, not API-return guidance.
   - Kotlin sealed classes: a language-feature page ("the Kotlin compiler [can] check exhaustively that all possible cases are covered"). It does not say to prefer it over strings. Definition page, PROMOTION rule 3.
   Clean practice statements for the Rule: Microsoft, plus Rust and Apple on neighbouring clauses. That is below three. Fix: draft, or narrow the Rule to what Microsoft and Rust state (parameters and flags) and find two more organisations for returns.
3. **consider**, check 3. `tool_gate: mypy --strict` flags nothing on the FAIL `-> str`; only a `Literal`/`Enum` return type plus a `match` with `assert_never` would. Name `assert_never` or an exhaustive-match check.

---

## mod-behaviour-lives-with-state — PASS

Verified quotes:
- Microsoft microservice-domain-model: "The entity's methods take care of the invariants and rules of the entity instead of having those rules spread across the application layer." The CRUD exception is on the same page.
- PMD DataClass: "The lack of functionality may indicate that their behaviour is defined elsewhere, which is a sign of poor data-behaviour proximity."
- DevIQ: "the objects that model the behavior of the problem space … should use encapsulation to manage their internal state and behavior", with the functional-programming exception ("anemic models are expected").

Orgs: Microsoft, PMD, NimblePros (DevIQ) = 3 for the whole Rule. The FAIL and PASS parse, and the counterpoint is a real objection with an answer.

Notes (consider): the Counterpoint is seven sentences, and the last two (Microsoft CRUD, DevIQ functional) could move to `applies_when` or be cut. Microsoft and DevIQ both paraphrase Fowler's AnemicDomainModel (Microsoft's page quotes it), so independence is thinner than the org count.

---

## mod-internals-unreachable — ISSUES

1. **consider**, check 1 and 2. Import half ("unimportable"): Go `cmd/go` internal packages ("Code in or below a directory named 'internal' is importable only by code that shares the same import path above the internal directory") and Bazel visibility ("help other developers distinguish between your library's public API and its implementation details") are both Google, so one org. Microsoft's `internal` page is a definition ("You can access internal types or members only within files in the same assembly"). Cursor's pstack is the only direct practice: "Make internals unreachable from outside the module, so an import from outside fails the build." Lenient count 3 (Google, Microsoft, Cursor); strict count 2, because definitions do not count. The card was stable before this edit, so I report it, not fault the writer.
2. **consider**, check 3. Rule wording "unimportable and unread": the FAIL's second line `order._lines.append(line)` is a write. Fix: "untouched".

Member half, three organisations confirmed:
- Refactoring.Guru Inappropriate Intimacy: "One class uses the internal fields and methods of another class … Good classes should know as little about each other as possible."
- PEP 8: "backwards compatibility guarantees apply only to public interfaces", and `_single_leading_underscore` is a "weak 'internal use' indicator".
- Pylint W0212: "Used when a protected member … is accessed outside the class or a descendant of the class where it's defined."

Edit check: the new FAIL/PASS lines parse, and the Counterpoint test-door addition (`opens`, `InternalsVisibleTo`) is accurate (language facts, not cited).

---

## mod-no-module-mutable-state — ISSUES

1. **act**, check 3. The edited Rule "Keep no mutable state outside an instance" is wrong as written. A local `out = []` inside a function (the PASS example does exactly this in `Loader.get`, and `fn-no-caller-mutation` blesses it) is mutable state "outside an instance". Fix: "Keep no mutable state at module or class level; hold it on an instance."
2. **act**, check 1 and 2. The new class and static-field clause has two organisations:
   - Google Python guide §2.5: "Module-level values or class attributes that can get mutated during program execution". The same section's Decision allows module or class state "made internal by prepending an _" when the design reasons are explained.
   - Microsoft CA2211: its Cause is "A public or protected static field is not constant nor is it read-only". It does not cover a private static field, so the FAIL's `_clients = {}` is outside it.
   - Uber guide: "Avoid mutating global variables, instead opting for dependency injection". Go package variables only; Go has no class or static fields.
   Fix: keep the class-attribute clause in the Why (Google), or add one more organisation that covers class or static fields.
3. **consider**, check 3. Google permits justified `_`-prefixed module or class state, which the absolute Rule forbids. The Counterpoint covers a bounded cache but not a documented exception. Add one clause, or accept the Rule as stricter than its sources.

Module-level clause: Google, Uber, Microsoft (CA2211 for statics) = 3.

---

## mod-one-name-per-concept — ISSUES

1. **act**, check 1. The `note` and `borrowed_from` say Google review guidance backs the same-name rule. The page's Naming item says: "A good name is long enough to fully communicate what the item is or does, without being so long that it becomes hard to read." Its "Consistency" section is about following the style guide. Nothing says one name per concept. Fix: drop the Google claim from the note and from the clause count.
2. **act**, check 2. Per-clause count for "one name for one concept":
   - island.is: "Use the same name or term for the same concept … Name overloading should be avoided. Use different names for different concepts."
   - Microsoft Azure API guidelines: "a clear name that you use consistently throughout your API and documentation".
   - TUM ESI: "Avoid useless noise-terms … What would be the difference between Product, ProductData, and ProductInfo?" This is partial, and "Be consistent with the existent" is about project style.
   - Ousterhout (via dev.to): a person.
   Two firm organisations plus one partial. Fix: find one more, or re-read TUM as the third and say so in the note.
3. **consider**, check 1 and 4. New two-class sentence, FAIL and PASS (`UserRepo.fetch / AccountRepo.load`): Refactoring.Guru backs it ("Two classes perform identical functions but have different method names … Rename Methods to make them identical"). Rust API guidelines C-CONV is a prefix convention for conversions (`as_`, `to_`, `into_`). The `google.aip.dev/130` page is an index of method categories with no statement on naming. So one organisation backs a case the FAIL now asserts. Fix: drop the Rust and AIP-130 URLs, or cite AIP-131 and similar standard-method pages.
4. **consider**, check 3. The adapter exemption in the Counterpoint is sound but unsourced.

---

## py-class-earns-its-instance — ISSUES

1. **consider**, check 6. The added Counterpoint sentence ("A class can also be left to mark future work; that is the same speculation …") does not answer the stated objection ("Protocols make testing easy"). It restates Refactoring.Guru's Lazy Class reason ("designed to support future development work that never got done"). Move it to the Why or drop it.
2. **consider**, check 2. Per clause:
   - Class with no state or one method → function: Refactoring.Guru ("if a class doesn't do enough to earn your attention, it should be deleted"), Pylint too-few-public-methods ("be sure it's really worth it", fix shown as dataclass plus module function), creator.
   - `Protocol` with one implementation: Go wiki ("Do not define interfaces on the implementor side of an API 'for mocking'") plus creator.
   Independent orgs: 2 and 1. The card stands on ADR 0001 (creator source), which the `note` already says. Say so in `lacks`-style terms in the PR.

The FAIL `TaxCalc.total` and PASS `tax.py` parse and fit the Rule.

---

## py-test-hygiene — ISSUES

Per-clause confirmed organisations:

| Clause | Orgs I confirmed |
|---|---|
| network | Google ("small tests aren't allowed to access the network or disk") = 1 |
| filesystem | Google, Microsoft ("no dependencies on any outside factors, such as a file system or database") = 2 |
| database | Microsoft, Spring ("stubbing or mocking DAO or repository interfaces, without needing to access persistent data"), Django ("SimpleTestCase disallows database queries by default"), Laravel ("unable to access your application's database"), Google = 5 |
| real clock | Microsoft (seam for `DateTime.Now`), GitLab ("Unit and component tests use fake timers"), Rails (`travel_to`) = 3 |
| separate slower tier | Laravel (Unit vs Feature), Google (test sizes), GitLab (testing levels), Rails ("bin/rails test will not run [system tests], since they can be slow. … add another CI step") = 4 |

1. **consider**, check 2. The network and filesystem clauses have one and two independent organisations. The creator's guide carries them under ADR 0001; without it the Rule needs two more for network and one more for filesystem. Say so in the PR, or split the Rule.
2. **consider**, check 6. The Rule bundles three prohibitions (I/O, clock, tiering). The Counterpoint (Laravel: "most of your tests should be feature tests") is real and answered. No change needed beyond noting the bundle.

The FAIL and PASS parse. `pytest --disable-socket` is real pytest-socket.

---

## code-test-selection-on-pr — ISSUES

Per clause:
- Run only affected tests on a PR: Meta ("catch more than 99.9 percent of all regressions … while running just a third of all tests that transitively depend on modified code"), Microsoft TIA, Shopify ("what tests have that file in its call graph … we look up the tests we need to run"), Develocity ("runs only those tests"), Nx = 5.
- Full run before deploy or on a schedule: Shopify ("run the full test suite every deploy"), Microsoft ("TIA can be conditioned to run all tests at a configured periodicity. Setting this option is recommended"), Develocity ("Remaining tests mode … post-merge or nightly builds to ensure complete coverage") = 3.

1. **consider**, check 3 and 6. `applies_when` has no size or time condition. A repo whose full suite takes two minutes FAILs this card, and the Counterpoint does not raise that objection. Fix: add "when the full suite exceeds the team's feedback target", or an N/A line.
2. **consider**, check 1. The note says Google "runs a subset on presubmit". Abseil ch. 23 says each team creates "a fast subset of tests, often a project's unit tests", before submit. That is a team-chosen fast subset, not change-based selection. Do not count Google for clause 1.
3. **consider**, check 4. Stable `code-ci-gates` requires "passing build, tests, lint, and type checks … before merge". The Counterpoint's "The full run is before deploy or on a schedule, not before merge" reads as the opposite. Cross-reference it or reword to "the selected tests gate the merge".

Meta, the Shopify 0.06% figure (about pull requests with failing tests merged because the mapping lags), and Microsoft's "falls back to running all tests" all verify.

---

## code-test-suite-time-budget — PASS

The draft status and `lacks: orgs` are correct. Clause "fail the build when the total or a single test passes a written budget":
- thoughtbot: yes. "Total suite budget is set 10% above your current total", per-type budget at "the 99th percentile", allowlist entries expire and the audit fails.
- SciPy: yes. `pytest-fail-slow` with `--fail-slow=5.0`.
- Shopify: no. Its Test Budget is "the predetermined time we terminate test execution", a stop-and-prioritise limit, not a failing gate. The note describes it correctly.
- GitLab: no. A 45-minute pipeline target.

Two organisations, as the card says. Clause "record the total and slowest tests on every run": thoughtbot, SciPy, GitLab = 3. Keep as draft until a third failing-gate source appears.

---

## fn-length-budget — ISSUES

1. **act**, check 1 and 2. Clause "set a function-length limit in the linter": no cited page recommends a project to set one. Google's guide says the opposite: "We recognize that long functions are sometimes appropriate, so no hard limit is placed on function length. If a function exceeds about 40 lines, think about whether it can be broken up." The linters (ESLint default 50, Pylint `max-statements` 50, Checkstyle 150, RuboCop 10, PMD NcssCount 60) describe a check, not a practice. The "split unless one simple operation" clause is well backed: Google, Linux kernel ("it's OK to have a longer function" for "one long (but simple) case-statement"), Pylint ("You should then split it in smaller functions"), Microsoft CA1505 ("split it into smaller and more focused types or methods"). Fix: reword the Rule to the Google/kernel form ("Review a function past about 40 lines; split it unless it is one simple operation") and keep the linter as a gate, or move the limit clause to the Why.
2. **act**, check 3. `tool_gate` and `note` list PMD `CognitiveComplexity` and Microsoft CA1505 as length gates. CognitiveComplexity "reports methods with a complexity of 15 or more" (control flow, not lines). CA1505's threshold of 10 is a maintainability index "calculated by using … lines of code, program volume, and cyclomatic complexity". The note's "CA1505 ships a size gate" is wrong. Fix: remove both from the length gate, or label them complexity gates.
3. **consider**, check 5. The FAIL block is a config line plus `// 140 lines: validate, price, charge, save order, email receipt`. It shows no long body, so a reviewer cannot mark it FAIL from the code shown. Show a real stub or say "FAIL: linter reports max-lines-per-function".

Defaults verified: ESLint `max` 50, Pylint `max-statements` 50, RuboCop MethodLength `Max` 10, PMD `methodReportLevel` 60, CA1505 threshold 10. Checkstyle 150 from source (page UNFETCHED).

---

## fn-no-caller-mutation — ISSUES

1. **consider**, check 1 and 2. Rule orgs: Airbnb ("7.12 Never mutate parameters … Manipulating objects passed in as parameters can cause unwanted variable side effects in the original caller"), Meta/React ("you should treat them as if they were immutable … Instead of mutating them, you should always replace them"), ESLint (`no-param-reassign` with `props`) = 3. Airbnb's rule is the ESLint rule, so independence is thin. Google pyguide §2.12 ("Do not use mutable objects as default values") and the Python FAQ back the shared-default clause in the Why only. The Rust book page is language semantics, and Kotlin's "Prefer using immutable data to mutable" is about `val`/`var` and collection types, not parameters. Neither adds a count.
2. **consider**, check 3. `tool_gate: Rust borrow checker (E0596, E0499)`: `fn f(v: &mut Vec<_>) { v.push(1) }` is idiomatic and flagged by nothing, so the borrow checker is not a gate for this Rule. Name Clippy's `needless_pass_by_ref_mut` or drop Rust.
3. **consider**, check 6. The Rule is absolute. The "in-place API whose name says so" exception sits only in the Counterpoint. Add it to the Rule as "unless the function is documented as mutating".

Scope of `fn-no-caller-mutation` versus `mod-no-module-mutable-state` is stated in the note and holds.

---

## fn-parameter-limit — PASS

Backing, verified:
- ESLint `max-params`: "Functions that take numerous parameters can be difficult to read and write because it requires the memorization of what each parameter is, its type, and the order they should appear in"; default 3.
- Pylint `too-many-arguments`: "Used when a function or method takes too many arguments", fix shown as a dataclass; defaults 5 and 5.
- PMD `ExcessiveParameterList`: shows the Builder fix; `minimum` 10.
- RuboCop `Metrics/ParameterLists` `Max 5`.
- Checkstyle `ParameterNumber` default 7 (read from source; docs page UNFETCHED).

Three organisations state the problem and the fix (ESLint, Pylint, PMD). The FAIL and PASS parse. The note on the spread of defaults (3 to 10) is accurate, and the Counterpoint exempts signatures the author cannot change.

Note (consider): the Checkstyle `ignoreOverriddenMethods` claim that backs the exemption is on the UNFETCHED page.

---

## mod-class-size-budget — ISSUES

1. **act**, check 3. `tool_gate` and `note` list Microsoft CA1505 as a class-size gate. It measures a maintainability index (lines of code, program volume, cyclomatic complexity) with threshold 10, not size. Fix: drop it from the gate, as for `fn-length-budget`.
2. **consider**, check 2. Organisations that give a rationale or a fix:
   - Pylint: "try to reduce this to get a simpler (and so easier to use) class".
   - PMD GodClass: "God classes do too many things … They should be split apart".
   RuboCop `Metrics/ClassLength` (`Max 100`) and PMD `NcssCount` state only the measure. Microsoft is the index case above. Two organisations state the practice; the card says "four enforce a limit", which is true of enforcement and not of PROMOTION rule 3. Either find a third (a style guide that says to split large classes) or record that the card reads tool pages as practice, and do so for the other budget cards too.

`applies_when` references `code-file-lines-ceiling`, which exists and is stable. The FAIL and PASS are pseudo-code in a `text` block and read fine.

---

## mod-law-of-demeter — ISSUES

1. **act**, check 3 and 5. The Rule, FAIL and tools disagree with the Counterpoint on when to flag. PMD's `trustRadius` default 1 means "you're only allowed one getter call on untrusted values". JetBrains: "never call a method on an object received from another call". The Counterpoint says "flag a chain only when the caller depends on three or more layers". Under that, `a.b().c()` is not flagged though both tools flag it, and a reviewer cannot tell which line applies. Fix: pick one threshold, state it in the Rule, and keep the Counterpoint as the exception.
2. **consider**, check 1. The Google Testing Blog post (Hevery, "Writing Testable Code") names the law once, in the heading "Ask for things, Don't look for things (aka Dependency Injection / Law of Demeter)". The body is about constructors asking for collaborators, not call chains. Two firm organisations (PMD: "only talk to friends … forbids fetching data from 'too far away'"; JetBrains) plus one weak. Note: my first text extraction of that page lost the post body; I re-read it from the raw HTML.
3. **consider**, check 6. JetBrains says the law "is not really a law, but specifies a style guideline", which supports `severity: discuss`. The last Counterpoint sentence ("The law is also contested") is fine.

JetBrains `ignoreLibraryCalls` defaults to selected, as the card says.

---

## mod-no-repeated-switches — ISSUES

1. **consider**, check 1. The `note` credits the smell name "Repeated Switches" to Fowler and Beck via Refactoring.Guru. The page is titled "Switch Statements" and says "Often code for a single switch can be scattered in different places in the program. When a new condition is added, you have to find all the switch code and modify it. As a rule of thumb, when you see switch you should think of polymorphism." The "second and third copy" threshold is the card's own reading.
2. **consider**, check 8. Stable `fn-variants-as-tagged-union` says "Model variants as a tagged union, and make every switch over it fail the build when a variant is unhandled": keep the switch and make it exhaustive. This card says replace repeated switches with polymorphism. Both are sound but pull in opposite directions; add a cross-reference or say which one applies (open-ended behaviour, or a closed variant set).
3. **consider**, check 6. The Counterpoint's exemption matches RG ("When a switch operator performs simple actions, there's no reason to make code changes. Often switch operators are used by factory design patterns").

Organisations: Refactoring.Guru, and Google Testing Blog ("If you see the same if condition repeated in many places in your class you should again think polymorphism"). That is 2, so the draft and its `lacks` line are correct.

---

## mod-no-shotgun-surgery — ISSUES

Organisations (3): Refactoring.Guru ("A single responsibility has been split up among a large number of classes"), Microsoft architectural principles (DRY: "a frequent source of errors … Make this construct the single authority over this behavior"; "Duplication is always preferable to coupling to the wrong abstraction"), NDepend ("Knowledge should only exist in a single place in your codebase"; "When you find yourself changing the same four files or classes for each simple change … reconsider your design"). The NDepend post is by a person on a vendor blog, which `tools/orgs.py` counts as NDepend. All quotes verified. Clause 2 ("move the scattered parts together"): Refactoring.Guru (Move Method, Move Field), NDepend, Microsoft (encapsulate in one construct) = 3.

1. **consider**, check 4. Microsoft's DRY text is about duplicated logic. Shotgun surgery is split responsibility, not copies. Close enough to cite, but say "behaviour spread over several places".
2. **consider**, check 3 and 5. A reviewer sees one diff. The FAIL ("Adding a currency edits seven files") needs the history to judge ("every change of this kind edits the same files"). Add how to mark FAIL from one change: "the change edits one internal rule in several places and a sibling change did the same".

No duplicate: `mod-derive-dont-duplicate` and `mod-single-writer-per-state` are narrower.

---

## mod-temporary-field — ISSUES

1. **act**, check 3. The Why says "the next method that reads it sees a stale or empty value". The Rule triggers only when every read follows an assignment in the same method, so no read sees a stale value. The real harm per the tools: Sonar "it is not being used to store class information … prevent any misunderstanding"; PMD "the value that the field had before the method call may not be observed, so it might as well not be stored". Rewrite the Why around misleading state and per-call scratch space.
2. **act**, check 5. The FAIL uses a public attribute `self.subtotal`. `applies_when` says "A private field", and all three tools restrict to private fields: JetBrains "Reports private fields"; Sonar "the value of a private field"; PMD "We can only check private fields for now". A public attribute can be read by callers after `total()`, so it is legitimate state. Fix: `self._subtotal`.
3. **consider**, check 1. Pylint W0201 `attribute-defined-outside-init` fixes the opposite way: "Correct code" moves the assignment into `__init__`. It does not back this Rule and would push the author toward more fields. Remove it from `tool_gate` and `borrowed_from`.
4. **consider**, check 1. Refactoring.Guru's Temporary Field is a different shape: "Temporary fields get their values … only under certain circumstances. Outside of these circumstances, they're empty", with Extract Class as the treatment. It backs the name, not the "assigned before read in every method" trigger.

Rule trigger organisations: JetBrains FieldCanBeLocal ("If all local usages of a field are preceded by an assignment to that field, the field can be replaced with one or more local variables"), SonarSource S1450, PMD SingularField = 3. PMD's threading caveat is quoted correctly. Recommended: stay draft until findings 1 and 2 are fixed, then stable.

---

## chg-no-per-user-ide-files — ISSUES

1. **act**, check 1 and 2. The operating-system-metadata clause (`.DS_Store`, `Thumbs.db`) in the Rule and Why has no backing. I searched all cited pages: docs.github.com ignoring-files, git-scm gitignore, the github/gitignore VSCode template, Azure DevOps ignore-files, JetBrains, VS Code, Apple. None mentions OS metadata files. Zero organisations for this clause. Fix: cite the github/gitignore `Global/macOS.gitignore` and `Global/Windows.gitignore` (still only GitHub), or cut the clause.
2. **act**, check 3 and 4. `tool_gate: git ls-files -ci --exclude-standard` cannot catch the card's FAIL. It lists tracked files that match an ignore pattern. In a scratch repo with `.idea/workspace.xml` committed and no `.gitignore` entry, it printed nothing; only after adding the entry did it print `.idea/workspace.xml`. The FAIL is the "no entry" case. Fix: a path-list check such as `git ls-files | rg '(^|/)(\.idea/workspace\.xml|xcuserdata/|\.DS_Store)'`.
3. **consider**, check 1. Clause-by-clause:
   - Do not commit per-user state: JetBrains ("This folder contains both user-specific settings that should not be placed under version control and project settings that are normally shared among developers", from the configure-project-settings page), Git (`gitignore`: patterns "specific to one user's workflow" go in `info/exclude`; editor files go in `core.excludesFile`), GitHub (docs: global ignore for "temporary backup files that your text editor creates"; the VisualStudioCode template ignores `.vscode/*` except settings, tasks, launch, extensions) = 3.
   - Keep shared settings in the repo: JetBrains, Microsoft (VS Code docs: "When you add a Workspace Settings settings.json file to your project or source control, the settings for the project will be shared by all users of that project"), Apple (Xcode Cloud: "Use shared schemes"), GitHub template = 4.
   - Ignore in the repo or a machine-wide exclude: Git, GitHub = 2. The Azure DevOps ignore-files page is about `.gitignore` in Visual Studio and says nothing on editor state.
4. **consider**, check 6. The Why and Rule are long; the Why quotes three sources in a row.

The github/gitignore template agrees with the card's PASS (it un-ignores `settings.json`, `launch.json`).

---

## py-test-collection-and-imports — ISSUES

1. **act**, check 3 and 5. The Rule's second clause, "measure imports with `-X importtime` before you accept a slow start", has no FAIL or PASS case and no way to mark FAIL from code or config; it is a process step. The `lacks` line covers only `testpaths`. Fix: split it into its own card with a checkable case, or drop it.
2. **consider**, check 2. `testpaths`: pytest ("Useful when all project tests are in a known location to speed up test collection"), Trail of Bits ("For PyPI's 4,700+ tests, this discovery process alone consumed over 6 seconds—10% of our total test execution time after parallelization"; `testpaths` took 3,900+ tests from 7.84s to 2.60s) = 2, as `lacks` says. `-X importtime`: Trail of Bits ("use python -X importtime to identify slow-loading modules"), SkyPilot ("Use LazyImport … significant import time (e.g. > 100ms) … python -X importtime") = 2, plus Alan UNFETCHED. The `lacks` line should name this clause too if it stays.
3. **consider**, check 3. The FAIL only bites when pytest runs with no path arguments. A CI job running `pytest tests/` is unaffected. `applies_when` ("spends seconds collecting") partly covers it.

---

## Summary table

| id | verdict | confirmed orgs per clause | recommended status |
|---|---|---|---|
| fn-comments-explain-why | ISSUES (consider) | reason 4; no restating 4; rename first 3 | stable |
| fn-known-keys-get-a-type | ISSUES | record type 3 (mypy feature doc, PEP 589 same team, attrs); open-key map 1 | stable after the open-key clause moves to Why |
| fn-no-stringly-typed-returns | ISSUES | closed type for returns 1 (Microsoft); args and bool 1 (Rust); strings 1 partial (Apple); Kotlin definition | draft (or narrow to strings and merge the bool part away) |
| mod-behaviour-lives-with-state | PASS | 3 (Microsoft, PMD, DevIQ) | stable |
| mod-internals-unreachable | ISSUES (consider) | import 3 lenient / 2 strict; member 3 | stable |
| mod-no-module-mutable-state | ISSUES | module level 3; class/static 2 | stable after the Rule is reworded and the class clause moves to Why |
| mod-one-name-per-concept | ISSUES | same name 2 firm + 1 partial; two-class case 1 | stable after the Google claim is dropped; keep the two-class case in Why |
| py-class-earns-its-instance | ISSUES (consider) | class 2 + creator; Protocol 1 + creator | stable (creator exception) |
| py-test-hygiene | ISSUES (consider) | network 1; filesystem 2; database 5; clock 3; tier 4 | stable (creator exception) or split |
| code-test-selection-on-pr | ISSUES (consider) | select 5; full run 3 | stable after `applies_when` gets a time condition |
| code-test-suite-time-budget | PASS | record 3; fail the build 2 | draft |
| fn-length-budget | ISSUES | split-unless-simple 4; set a linter limit 0 recommendations | draft until the Rule is reworded |
| fn-no-caller-mutation | ISSUES (consider) | 3 (Airbnb, Meta, ESLint; thin independence) | stable |
| fn-parameter-limit | PASS | 3 (ESLint, Pylint, PMD) | stable |
| mod-class-size-budget | ISSUES | rationale 2 (Pylint, PMD); enforcement 4 | draft unless a third rationale is found |
| mod-law-of-demeter | ISSUES | 2 firm + 1 weak (Google blog) | stable after the threshold is fixed |
| mod-no-repeated-switches | ISSUES (consider) | 2 (Refactoring.Guru, Google blog) | draft |
| mod-no-shotgun-surgery | ISSUES (consider) | 3 per clause | stable |
| mod-temporary-field | ISSUES | trigger 3 (JetBrains, SonarSource, PMD) | draft until the Why and the FAIL are fixed |
| chg-no-per-user-ide-files | ISSUES | per-user state 3; shared settings 4; machine-wide exclude 2; OS metadata 0 | draft |
| py-test-collection-and-imports | ISSUES | testpaths 2; importtime 2 (+ Alan UNFETCHED) | draft |

Counts: 3 PASS, 18 ISSUES (act-level on 10 cards: fn-known-keys-get-a-type, fn-no-stringly-typed-returns, mod-no-module-mutable-state, mod-one-name-per-concept, fn-length-budget, mod-class-size-budget, mod-law-of-demeter, mod-temporary-field, chg-no-per-user-ide-files, py-test-collection-and-imports).

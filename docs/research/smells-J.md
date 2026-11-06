# Fowler smells, part 1 (Task J) — organisation sources and card decisions

Pass for J1–J6 from Martin Fowler's smell catalogue. Every page below was fetched and read on 2026-11-05/06; quotes are verbatim in quote marks, paraphrases are marked "(paraphrase)". Pages I could not fetch are marked UNFETCHED and excluded from the org counts. Linter defaults are the tool's documented threshold, as the brief asks.

Cards read first, so the decisions below do not duplicate them: `mod-one-name-per-concept`, `chg-reuse-before-write`, `mod-behaviour-lives-with-state`, `fn-no-anonymous-tuples`, `fn-known-keys-get-a-type`, `fn-no-stringly-typed-returns`, `mod-no-repeated-switches`, `mod-no-shotgun-surgery`, `mod-cohesive-unit`, `mod-yagni`, `mod-law-of-demeter`, `fn-no-pass-through-wrapper`, `mod-subtype-passes-parent-tests`, `mod-fowler-smells`, `fn-join-dont-concat-in-loop`, `fn-atomic-related-updates`, `mod-no-module-mutable-state`, `mod-deep-modules`, `mod-derive-dont-duplicate`.

**Decision summary:** J1 NEW (`fn-length-budget`), J2 NEW (`fn-parameter-limit`), J3 NEW (`mod-class-size-budget`), J4 MERGE into stable `mod-no-module-mutable-state`, J5 NEW (`fn-no-caller-mutation`), J6 SKIP.

---

## J1 — Long Function

**Decision: NEW card.** Suggested id `fn-length-budget`, level `function`, lang `core`. The Rule line is language-neutral; the number comes from the project's linter, not from this card.

**Candidate Rule.** Keep every function under the project's length limit; a longer function may stay only when its body is simple, such as one dispatch table.

**FAIL / PASS idea.** FAIL: a 140-line `checkout()` that validates the cart, prices it, charges the card, writes the order and sends the receipt. PASS: the same work as `validate_cart`, `price`, `charge`, `save_order`, `email_receipt`, called in order. PASS exception: a 140-line table-driven dispatch, if it is one step.

1. https://google.github.io/styleguide/pyguide.html#318-function-length (org: Google). "Prefer small and focused functions." And: "We recognize that long functions are sometimes appropriate, so no hard limit is placed on function length. If a function exceeds about 40 lines, think about whether it can be broken up without harming the structure of the program." **Backs J1 clause A** (a ~40-line review trigger) **and clause B** (long is sometimes appropriate). No linter gate; style-guide practice.

2. https://www.kernel.org/doc/html/latest/process/coding-style.html (org: Linux kernel project). §6: "Functions should be short and sweet, and do just one thing. They should fit on one or two screenfuls of text (the ISO/ANSI screen size is 80x24, as we all know), and do one thing and do that well." And: "if you have a conceptually simple function that is just one long (but simple) case-statement, where you have to do lots of small things for a lot of different cases, it's OK to have a longer function." Remedy: "Use helper functions with descriptive names". **Backs J1 clause A and B.**

3. https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1505 (org: Microsoft). **Default threshold `10`** (maintainability index). "The rule reports a violation when the maintainability index of a type, method, field, property, or event is less than 10." The index uses "lines of code, program volume, and cyclomatic complexity". How to fix: "redesign the type or method and try to split it into smaller and more focused types or methods." Suppression: "You can suppress this warning when the type or method cannot be split or is considered maintainable despite its large size." **Backs J1 clause A** (a size gate) **and clause B** (the size exception). Tool gate: `CA1505`.

4. https://eslint.org/docs/latest/rules/max-lines-per-function (org: ESLint / OpenJS Foundation). "Some people consider large functions a code smell. Large functions tend to do a lot of things and can make it hard following what's going on." `"max"` **default `50`**. **Backs J1 clause A.** Tool gate: `max-lines-per-function` (default 50).

5. https://checkstyle.sourceforge.io/checks/sizes/methodlength.html (org: Checkstyle). "Checks for long methods and constructors." Rationale: "If a method becomes very long it is hard to understand. Therefore, long methods should usually be refactored into several individual methods that focus on a specific task." `max` **default `150`**. **Backs J1 clause A.** Tool gate: `MethodLength` (default 150).

6. https://pmd.github.io/pmd/pmd_rules_java_design.html (org: PMD). `NcssCount`: "This rule uses the NCSS (Non-Commenting Source Statements) metric to determine the number of lines of code in a class, method or constructor." Defaults: `methodReportLevel` **60**, `classReportLevel` **1500**. `CognitiveComplexity`: "By default, this rule reports methods with a complexity of 15 or more. Reported methods should be broken down into less complex components." **Backs J1 clause A.** Tool gates: `NcssCount` (method 60 NCSS), `CognitiveComplexity` (15).

7. https://docs.rubocop.org/rubocop/latest/cops_metrics.html (org: RuboCop). `Metrics/MethodLength`: "Checks if the length of a method exceeds some maximum value." Default `Max` **10**. **Backs J1 clause A.** Tool gate: `Metrics/MethodLength` (default 10).

8. https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html (org: Pylint). `--max-statements`: "Maximum number of statements in function / method body." **Default `50`**. The message page https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-statements.html says: "Used when a function or method has too many statements. You should then split it in smaller functions / methods." **Backs J1 clause A.** Tool gate: `too-many-statements` (R0915, default 50).

**J1 org count:** Google, Linux kernel, Microsoft, ESLint, Checkstyle, PMD, RuboCop, Pylint = **8 organisations**. Clause A (under a limit): all 8. Clause B (a longer function may stay when simple): Google, Linux kernel, Microsoft (`CA1502` large-switch exclusion, `CA1505` "maintainable despite its large size") = 3. Confidence: **high** on the practice; **low** on a single consensus number (defaults range 10–150).

---

## J2 — Long Parameter List

**Decision: NEW card.** Suggested id `fn-parameter-limit`, level `function`, lang `core`. The remedy (a named record or builder) belongs in the Why and the examples; the Rule itself is the count.

**Candidate Rule.** Keep a function's parameter count at or below the project's limit.

**FAIL / PASS idea.** FAIL: `create_user(name, email, street, city, zip, country, plan, trial_days)` with eight positional values, most of them strings. PASS: `create_user(Contact(name, email, address), Subscription(plan, trial_days))`, or a builder that names each value.

1. https://eslint.org/docs/latest/rules/max-params (org: ESLint / OpenJS Foundation). "Functions that take numerous parameters can be difficult to read and write because it requires the memorization of what each parameter is, its type, and the order they should appear in. As a result, many coders adhere to a convention that caps the number of parameters a function can take." `"max"` **default `3`**. **Backs J2.** Tool gate: `max-params` (default 3).

2. https://checkstyle.sourceforge.io/checks/sizes/parameternumber.html (org: Checkstyle). "Checks the number of parameters of a method or constructor." `max` **default `7`**. The documented rationale for `ignoreOverriddenMethods` is: "developer may need to override method with many parameters from 3-rd party library. In this case developer has no control over number of parameters." **Backs J2 and supplies the override exception.** Tool gate: `ParameterNumber` (default 7).

3. https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html (org: Pylint). `--max-args`: "Maximum number of arguments for function / method." **Default `5`**. `--max-positional-arguments`: "Maximum number of positional arguments for function / method." **Default `5`**. The message page https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-arguments.html says: "Used when a function or method takes too many arguments." **Backs J2.** Tool gates: `too-many-arguments` (R0913), `too-many-positional-arguments` (R0917).

4. https://pmd.github.io/pmd/pmd_rules_java_design.html (org: PMD). `ExcessiveParameterList`: "Methods with numerous parameters are a challenge to maintain and increase the risk of bugs." "long parameter lists violate the Single Responsibility Principle". Default `minimum` **10**. Documented alternatives: "Builder Pattern", "Multiple Parameter Objects", "Method Overloading", "Method Decomposition". **Backs J2 and the record/builder remedy.** Tool gate: `ExcessiveParameterList` (default 10).

5. https://docs.rubocop.org/rubocop/latest/cops_metrics.html (org: RuboCop). `Metrics/ParameterLists`: "Checks for methods with too many parameters." Default `Max` **5**; `MaxOptionalParameters` **3**. **Backs J2.** Tool gate: `Metrics/ParameterLists` (default 5).

**J2 org count:** ESLint, Checkstyle, Pylint, PMD, RuboCop = **5 organisations**. The single Rule clause has 5. Confidence: **high** on the practice; **note** the defaults diverge (3/5/7/10) and Checkstyle documents an override exemption.

---

## J3 — Large Class

**Decision: NEW card.** Suggested id `mod-class-size-budget`, level `module`, lang `core`. It is a class-level size gate, distinct from `mod-cohesive-unit` (a draft about module cohesion and large literals) and from stable `mod-deep-modules` (interface size).

**Candidate Rule.** Keep a class within the project's size limit.

**FAIL / PASS idea.** FAIL: `BillingService` with 25 fields and 40 public methods covering pricing, tax, invoices, dunning and notifications. PASS: `Pricing`, `Tax`, `Invoice`, `Dunning`, `Notifier`, each with its own state. A data record with many fields is a separate case: judge it by the data-shape rules, not this card.

1. https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html (org: Pylint). `--max-attributes`: "Maximum number of attributes for a class (see R0902)." **Default `7`**. `--max-public-methods`: "Maximum number of public methods for a class (see R0904)." **Default `20`**. The message page https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-instance-attributes.html says: "Used when class has too many instance attributes, try to reduce this to get a simpler (and so easier to use) class." Its example comment: "max of 7 attributes by default, can be configured". **Backs J3.** Tool gates: `too-many-instance-attributes` (R0902, default 7), `too-many-public-methods` (R0904, default 20).

2. https://pmd.github.io/pmd/pmd_rules_java_design.html (org: PMD). `NcssCount` class default: `classReportLevel` **1500** (NCSS). `GodClass`: "God classes do too many things, are very big and overly complex. They should be split apart to be more object-oriented." Its detector requires "High WMC", "High ATFD", "Low TCC". **Backs J3** (a class-size gate, with cohesion as part of the judgement). Tool gates: `NcssCount` (class 1500), `GodClass`.

3. https://docs.rubocop.org/rubocop/latest/cops_metrics.html (org: RuboCop). `Metrics/ClassLength`: "Checks if the length of a class exceeds some maximum value." Default `Max` **100**. **Backs J3.** Tool gate: `Metrics/ClassLength` (default 100).

4. https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1505 (org: Microsoft). `CA1505` applies to a "type, method, field, property, or event"; **default threshold `10`** on the maintainability index (which includes "lines of code"). Fix: "redesign the type or method and try to split it into smaller and more focused types or methods." **Backs J3.** Tool gate: `CA1505` (type threshold 10).

**J3 org count:** Pylint, PMD, RuboCop, Microsoft = **4 organisations**. The single Rule clause has 4. Confidence: **high** that four orgs enforce a class-size limit; **low** that any one number is the consensus (7 fields, 20 methods, 100 lines, 1500 NCSS, MI 10 are different metrics).

---

## J4 — Global Data

**Decision: MERGE into the stable card `mod-no-module-mutable-state`; no new card.** The stable card already has the three organisations and the Rule "Keep no mutable state at module level." The one gap: its `applies_when` says "A module defines a variable that changes after load", which does not mention class/static fields. Google's definition does. Recommended edit: extend `applies_when` to "A module or class defines a variable that changes after load: a module-level value, a static/class field, list, dict, counter, cache, client or singleton." No new `borrowed_from` entry is needed; the three pages below are the sources already on the card.

1. https://google.github.io/styleguide/pyguide.html#25-mutable-global-state (org: Google). "Avoid mutable global state." Definition: "Module-level values or class attributes that can get mutated during program execution." "Module-level constants are permitted and encouraged." **Backs J4** (including the class-attribute scope).

2. https://github.com/uber-go/guide/blob/master/style.md#avoid-mutable-globals (org: Uber). "Avoid mutating global variables, instead opting for dependency injection. This applies to function pointers as well as other kinds of values." The example replaces `var _timeNow = time.Now` with a `signer` struct holding `now`, so tests inject a clock (paraphrase). **Backs J4** and the injection remedy.

3. https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2211 (org: Microsoft). "Static fields that are neither constants nor read-only are not thread-safe." "static fields are best used to store data that does not change." Fix: "make the static field constant or read-only." **Backs J4.** Tool gate: `CA2211`.

**J4 org count:** Google, Uber, Microsoft = **3 organisations**, all already on the stable card. Confidence: **high**; no new research needed. The card's existing counterpoint (a bounded, injected, lifetime-tied cache is acceptable) already answers the "simplest cache" objection.

---

## J5 — Mutable Data

**Decision: NEW card.** Suggested id `fn-no-caller-mutation`, level `function`, lang `core`. Scope it to caller-owned data, so it does not repeat stable `mod-no-module-mutable-state` (module-level state). The card should say that local mutation of a fresh object is fine.

**Candidate Rule.** Do not mutate a parameter or a caller-owned object; return a new value instead.

**FAIL / PASS idea.** FAIL: `def apply_discount(order): order.total *= 0.9; return order` changes the caller's `order`. PASS: `return dataclasses.replace(order, total=order.total * 0.9)`, or a reducer that returns `{...state, items: [...state.items, item]}`. Local `next = {}; next.x = ...` before returning is PASS.

1. https://airbnb.io/javascript/#functions--mutate-params (org: Airbnb). "Never mutate parameters." Why: "Manipulating objects passed in as parameters can cause unwanted variable side effects in the original caller." The same guide also prefers `const` over `var` (2.1), copies objects with spread instead of mutating `Object.assign` (3.8), and forbids mutable exports (10.5) (paraphrase). **Backs J5.** Tool gate: `no-param-reassign` (see row 5).

2. https://doc.rust-lang.org/book/ch04-02-references-and-borrowing.html (org: Rust project). "Just as variables are immutable by default, so are references. We're not allowed to modify something we have a reference to." And: "Mutable references have one big restriction: If you have a mutable reference to a value, you can have no other references to that value." **Backs J5** (mutation only when the value is uniquely borrowed). Tool gate: the compiler's borrow checker (`E0596`, `E0499`).

3. https://react.dev/learn/updating-objects-in-state (org: Meta / React). "you should treat any JavaScript object that you put into state as read-only." "Instead, when you want to update an object, you need to create a new one (or make a copy of an existing one), and then set the state to use that copy." **Backs J5.** Tool gate: none in React itself; for the JavaScript case use `no-param-reassign` (row 5).

4. https://docs.python.org/3/faq/programming.html#why-are-default-values-shared-between-objects (org: Python Software Foundation). "Default values are created exactly once, when the function is defined. If that object is changed, like the dictionary in this example, subsequent calls to the function will refer to this changed object." "Because of this feature, it is good programming practice to not use mutable objects as default values." **Backs J5** (shared objects and mutable defaults). Tool gate: Pylint `dangerous-default-value` (W0102).

5. https://eslint.org/docs/latest/rules/no-param-reassign (org: ESLint / OpenJS Foundation). "Assignment to variables declared as function parameters can be misleading and lead to confusing behavior". "This rule can be also configured to fail when function parameters are modified." Important default: `"props"` is `false` by default; only with `props: true` does it catch `param.field = value`. **Backs J5 and gives the exact gate limitation.** Tool gate: `no-param-reassign` (set `props: true` for object mutation).

6. https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2227 (org: Microsoft). "A writable collection property lets users replace the collection with a completely different collection." Fix: "Change the property type to a read-only collection type." **Backs J5** (do not expose mutable state; return a read-only view or copy). Tool gate: `CA2227`.

7. https://github.com/uber-go/guide/blob/master/style.md#copy-slices-and-maps-at-boundaries (org: Uber). "Keep in mind that users can modify a map or slice you received as an argument if you store a reference to it." And: "be wary of user modifications to maps or slices exposing internal state." The guide shows copying on receive and on return. **Backs J5** (aliasing at boundaries). Tool gate: none.

8. https://kotlinlang.org/docs/coding-conventions.html#immutability (org: JetBrains / Kotlin). "Prefer using immutable data to mutable. Always declare local variables and properties as `val` rather than `var` if they are not modified after initialization." "Always use immutable collection interfaces (`Collection`, `List`, `Set`, `Map`) to declare collections which are not mutated." Also: "The name should also suggest if the method is mutating the object or returning a new one. For instance, `sort` is sorting a collection in place, while `sorted` is returning a sorted copy of the collection." **Backs J5** (prefer read-only; name the mutation). Tool gate: IntelliJ/Kotlin inspections; no single numeric gate.

9. https://google.github.io/styleguide/pyguide.html#212-default-argument-values (org: Google). "Do not use mutable objects as default values in the function or method definition." The guide's correct form is `def foo(a, b=None):` with `if b is None: b = []` (paraphrase of the code sample). **Backs J5.** Tool gate: Pylint `dangerous-default-value` (W0102).

**J5 org count:** Airbnb, Rust, Meta/React, Python Software Foundation, ESLint, Microsoft, Uber, JetBrains, Google = **9 organisations**. The single Rule clause has 9. Confidence: **high** on "do not mutate caller-owned data"; the card must state the local-mutation exception or it will contradict React, Rust and Kotlin.

---

## J6 — Loops (replace a loop with a pipeline)

**Decision: SKIP; do not add a card.** Two organisations state the practice and only one of them states it without a performance caveat. Modern practice does not treat a loop as a smell, and several organisations use loops as the readable default. A draft would be `lacks: orgs` and would need a language-specific scope (JavaScript and Kotlin), which the repo avoids.

**Candidate Rule, if the maintainer overrules the skip.** "Iterate a collection with its own iterator or a pipeline, not with an index that only indexes." That narrow rule has a Rust project gate (`needless_range_loop`) and Airbnb's broader JavaScript rule; it still has only 2 orgs.

1. https://airbnb.io/javascript/#iterators--nope (org: Airbnb). "Don't use iterators. Prefer JavaScript's higher-order functions instead of loops like `for-in` or `for-of`." Why: "This enforces our immutable rule. Dealing with pure functions that return values is easier to reason about than side effects." The text names `for-in`/`for-of`, while the example also marks a classic indexed `for` loop as bad, so this is a broad JavaScript rule. **Backs J6.**

2. https://kotlinlang.org/docs/coding-conventions.html#loops (org: JetBrains / Kotlin). "Prefer using higher-order functions (`filter`, `map` etc.) to loops. Exception: `forEach` (prefer using a regular `for` loop instead, unless the receiver of `forEach` is nullable or `forEach` is used as part of a longer call chain)." And: "When making a choice between a complex expression using multiple higher-order functions and a loop, understand the cost of the operations being performed in each case and keep performance considerations in mind." **Backs J6, conditionally.**

3. https://martinfowler.com/articles/refactoring-pipelines.html (person: Martin Fowler; not counted). "loops aren't the only way to represent list processing" and the collection pipeline "is an appealing alternative". The article is a refactoring demonstration, not a rule that loops are a smell. **Reference only for J6.**

4. https://rust-lang.github.io/rust-clippy/master/index.html#needless_range_loop (org: Rust project). "Checks for looping over the range of `0..len` of some collection just to get the values by index." Why: "Just iterating the collection itself makes the intent more clear and is probably faster because it eliminates the bounds check that is done when indexing." **Backs the narrow index-loop version of J6.** Tool gate: `clippy::needless_range_loop` (style, warn).

**J6 org count:** Airbnb, JetBrains = **2 organisations** state the practice. No Rule clause reaches 3. Confidence: **high** that the general smell should be skipped; **medium** that no third organisation exists (a future pass could check JetBrains inspections, SonarJS, or a JavaScript style guide from a company such as Google or Microsoft).

---

## Counter-evidence

- **J1 Long Function.** Google: "long functions are sometimes appropriate, so no hard limit is placed on function length." Linux: a "conceptually simple function that is just one long (but simple) case-statement ... it's OK to have a longer function." Microsoft `CA1502` (https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1502): "a method that contains a large `switch` ... statement is a candidate for exclusion." Microsoft `CA1505`: "You can suppress this warning when the type or method cannot be split or is considered maintainable despite its large size." So length alone is not the defect: the card must treat the project's limit as a trigger to inspect the steps, and must exempt a simple dispatch. The thresholds also conflict: RuboCop `Max 10`, ESLint `50`, Pylint `50`, PMD `60` NCSS, Checkstyle `150`. A card that hard-codes one number would be wrong for most projects; "the project's limit" is the only defensible phrasing.
- **J2 Long Parameter List.** Checkstyle's own `ignoreOverriddenMethods` rationale: "developer may need to override method with many parameters from 3-rd party library. In this case developer has no control over number of parameters." PMD's own alternatives include "Method Overloading", which keeps the parameter count high in one signature. A parameter object can hide required values behind optional fields or become a god object. The card should exempt signatures the author cannot change and group only values that already travel together.
- **J3 Large Class.** Microsoft: suppress when the type "is considered maintainable despite its large size." PMD's `GodClass` does not fire on size alone; it requires "High WMC", "High ATFD" and "Low TCC", so a large but cohesive class is not a god class. Pylint's attribute count does not distinguish a DTO from a service. The card should say that a data record is judged by its data shape, and that a cohesive wide API may be justified; the limit is a signal to split by responsibility.
- **J4 Global Data.** Google permits global state in rare cases if it is module-level or a class attribute, internal (`_` prefix), accessed through functions, and the reason is documented; constants are "permitted and encouraged". Uber's fix is dependency injection, not a ban on all process-wide values. The stable card already makes the frozen/load-once constant the exception and asks for a bounded, injected cache.
- **J5 Mutable Data.** React: "Mutation is only a problem when you change existing objects that are already in state. Mutating an object you've just created is okay because no other code references it yet. This is called a 'local mutation'." Kotlin allows `var` when the value is modified. Rust allows mutation through `&mut` when the borrow is unique. The card must target caller-owned or aliased data, not local construction or an explicitly unique mutable borrow.
- **J6 Loops.** Go's `Effective Go` treats `range` as the idiom for arrays, slices, strings and maps: "If you're looping over an array, slice, string, or map, or reading from a channel, a `range` clause can manage the loop." Google's Python guide says "Comprehensions are allowed, however multiple `for` clauses or filter expressions are not permitted. Optimize for readability, not conciseness." and shows a nested `for` loop as a "Yes" example. Kotlin itself warns to "keep performance considerations in mind" before replacing a loop with multiple higher-order functions. Rust's book teaches `for` loops over iterators and presents iterator chains as an option, not a mandate. Airbnb's text names `for-in`/`for-of` but its example also marks a classic indexed loop as bad, so it is a broad JavaScript rule; even counting it, only two orgs state the general practice.

---

## Also read, no rule / UNFETCHED

- **UNFETCHED (excluded from counts): SonarSource S107, S138, S1448.** `https://rules.sonarsource.com/java/RSPEC-107/`, `.../RSPEC-138/`, `.../RSPEC-1448/` and the lowercase `rspec-...` forms all returned 404 to the fetcher. A search result surfaced the S1448 text ("A class that grows too much tends to aggregate too many responsibilities...") and a mirror gave its default `maximumMethodThreshold` as `35`, but I did not fetch the canonical page, so none of these is counted or quoted in a row. If a future pass renders `docs.sonarsource.com` or a live SonarQube rule page, SonarSource would add a 5th org to J3, a 6th to J2, and a 9th to J1.
- **PMD URL discrepancy.** I fetched `https://pmd.github.io/pmd/pmd_rules_java_design.html` (PMD 7.30.0-SNAPSHOT). `NcssCount` **is** present there with `methodReportLevel` 60 and `classReportLevel` 1500, and `CognitiveComplexity` is present with 15. `docs/research/size-branches-types-orgs-F.md` says `NcssCount` is absent from the PMD 7 design ruleset; that pass used the `docs.pmd-code.org` copy. One of the two URLs is serving a different build. The parent should pin the URL the repo wants before promoting a card that names `NcssCount`.
- **Fowler and Beck are persons.** `https://martinfowler.com/articles/refactoring-pipelines.html` is a reference for J6 only; it is not counted. I did not fetch the book text, so I do not claim what the 2nd edition's catalogue does or does not contain.
- **Existing cards, not sources:** `mod-fowler-smells` already tells a reviewer to name the smell and the line; it does not set a length or parameter limit, so J1/J2/J3 do not duplicate it. `mod-cohesive-unit` is a draft about modules and large literals; it overlaps J3's "split by responsibility" remedy, so the new J3 card should cross-reference it rather than restate it. `mod-deep-modules` is about interface size, not class size. J2 does not duplicate `fn-known-keys-get-a-type` or `fn-no-anonymous-tuples`: those replace a bag/tuple with a type, while J2 is about arity; a parameter object is one remedy, not the rule. J5 does not duplicate `fn-atomic-related-updates` (all-or-nothing writes) or `mod-no-module-mutable-state` (module-level state).
- **Not fetched this pass, possible future orgs:** Refactoring.Guru's smell pages (the repo already has rows from them in `smells-2026-11-05.md`), JetBrains/IntelliJ inspection pages for "long method"/"too many parameters", and Google's Java/C++ style guides (not fetched this pass). Redux's style guide and Swift's value-type documentation were also not needed: J5 already has nine organisations without them, and J4 has three.

---

## Per-claim summary

| Claim | Decision | Distinct orgs (fetched, quoted) | Clauses at ≥3 orgs | Confidence |
|---|---|---|---|---|
| J1 Long Function | NEW `fn-length-budget` | 8 (Google, Linux kernel, Microsoft, ESLint, Checkstyle, PMD, RuboCop, Pylint) | A=8, B=3 | high on practice; low on one number (10–150) |
| J2 Long Parameter List | NEW `fn-parameter-limit` | 5 (ESLint, Checkstyle, Pylint, PMD, RuboCop) | single clause = 5 | high; defaults 3–10, override exemption documented |
| J3 Large Class | NEW `mod-class-size-budget` | 4 (Pylint, PMD, RuboCop, Microsoft) | single clause = 4 | high on practice; low on one metric |
| J4 Global Data | MERGE into `mod-no-module-mutable-state` | 3 (Google, Uber, Microsoft), already on the stable card | single clause = 3 | high |
| J5 Mutable Data | NEW `fn-no-caller-mutation` | 9 (Airbnb, Rust, Meta/React, PSF, ESLint, Microsoft, Uber, JetBrains, Google) | single clause = 9 | high; must state the local-mutation exception |
| J6 Loops | SKIP | 2 (Airbnb, JetBrains) | none | high on skip; medium that no third org exists |

---

## Doubts / notes for the maintainer

1. **The numbers are not a consensus, they are local gates.** J1: 10 (RuboCop), 50 (ESLint, Pylint), 60 NCSS (PMD), 150 (Checkstyle), "about 40" (Google), "one or two screenfuls" (Linux). J2: 3 (ESLint), 5 (Pylint, RuboCop), 7 (Checkstyle), 10 (PMD). J3: 7 fields / 20 public methods (Pylint), 100 lines (RuboCop), 1500 NCSS (PMD), MI 10 (Microsoft). A card that names one number will fail on projects that use another tool. The candidate Rules therefore say "the project's limit" and the `tool_gate` names each tool's default.
2. **Pylint `too-many-statements` page vs default.** The message page's example config sets `max-statements=7`, but the documented default in `all-options` is `50`. I used 50; do not copy the 7 from the example into a card.
3. **PMD `NcssCount` URL conflict.** See "Also read" above. Confirm whether `pmd.github.io/pmd/...` or `docs.pmd-code.org/latest/...` is the canonical page for the repo before a stable card cites `NcssCount`.
4. **`airbnb.io` is not in `tools/orgs.py`.** The map has `airbnb.tech` but not `airbnb.io` (the style-guide host). J5 and J6 rows would fail `tools/validate.py` on that URL. Add `airbnb.io` → `Airbnb` to the map, or cite `https://github.com/airbnb/javascript` (also not mapped as `github.com/airbnb/`) once a fetched page is used.
5. **`checkstyle.org` is not in the map; `checkstyle.sourceforge.io` is.** I fetched both; they serve the same page. The rows above cite the `sourceforge.io` URL so validation can pass.
6. **J4 merge edit.** Extend `applies_when` to mention class/static fields. Google's 2.5 definition explicitly covers "class attributes", and Microsoft `CA2211` covers "static fields"; the three sources already on the stable card support the broader scope, so no new `borrowed_from` is needed.
7. **J5 boundary with the stable card.** `mod-no-module-mutable-state` owns module-level and (after the J4 edit) class/static state. `fn-no-caller-mutation` must say "parameter or caller-owned object" and must mention that local mutation of a fresh object is allowed (React's "local mutation", Rust's unique `&mut`, Kotlin's `var` when modified), or it will contradict those sources.
8. **J5 tool-gate caveat.** ESLint `no-param-reassign` defaults to `props: false`; it catches `param = x` but not `param.field = x` unless the project sets `props: true`. A card that claims the default rule catches object mutation would be wrong.
9. **J6 could be a narrow draft, not a general one.** If the maintainer wants a card, the defensible one is "do not index a collection just to iterate it" (Rust `needless_range_loop` + Airbnb's iterator rule), not "replace every loop with a pipeline". Even that is 2 orgs and language-specific, so my recommendation is to skip.
10. **J1/J2 severity.** I did not assign severity in the candidate lines; the parent should decide whether the card is `discuss` (the sources treat length/count as a signal) or `should-fix` (the tools make it a gate). The counter-evidence supports `discuss` for J1/J3 and `should-fix` for J2/J5 when the project's linter already enforces a limit.

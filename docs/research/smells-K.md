# Smells K: organisations behind Lazy Element, Temporary Field, Insider Trading, Alternative Classes, Data Class, Comments as deodorant

Fetched 2026-11-05 and 2026-11-06 with `curl`; every quote below is copied from the fetched page. Organisation counting follows `docs/PROMOTION.md`: a company, foundation or project's own maintainers count once, whatever the number of pages. Refactoring.Guru is a single-author site but is mapped as an organisation in `tools/orgs.py`, so it counts, though it is the weakest organisation in each row. Martin Fowler and Kent Beck are people and never count. A row marked `PREFIX?` names a URL that no prefix in `tools/orgs.py` covers yet.

Fowler's 2nd edition renamed two smells: *Lazy Class* is **Lazy Element**, and *Inappropriate Intimacy* is **Insider Trading**. Refactoring.Guru still uses the older names, so the rows below quote those pages.

## K1 — Lazy Element (Lazy Class)

1. https://refactoring.guru/smells/lazy-class (org: Refactoring.Guru). "Understanding and maintaining classes always costs time and money. So if a class doesn’t do enough to earn your attention, it should be deleted." The page also names the origin: "Perhaps a class was designed to support future development work that never got done." Treatment (paraphrase): inline the class or collapse the hierarchy. Backs K1, class half. Its "When to Ignore" is in Counter-evidence.

2. https://pylint.readthedocs.io/en/latest/user_guide/messages/refactor/too-few-public-methods.html (org: Pylint). Rule `too-few-public-methods / R0903`: "Used when class has too few public methods, so be sure it's really worth it." The rule's "Correct code" replaces the class with a `@dataclasses.dataclass` plus a module function, which is the same split `py-class-earns-its-instance` asks for. The documented threshold is not on the message page; the checker source sets `min-public-methods` to **2** (https://github.com/pylint-dev/pylint/blob/main/pylint/checkers/design_analysis.py, same organisation), and the checker exempts dataclasses, Enums, NamedTuple and TypedDict. Tool gate for the class half. Backs K1.

3. https://pmd.github.io/pmd/pmd_rules_java_design.html (org: PMD). Rule `UselessOverridingMethod`: "The overriding method merely calls the same method defined in a superclass." A method that adds no behaviour beyond the call is exactly the method half of Lazy Element. Tool gate (no threshold; the rule is a boolean). Backs K1, method half, and strengthens `fn-no-pass-through-wrapper`.

4. https://eslint.org/docs/latest/rules/no-useless-constructor (org: ESLint). `no-useless-constructor`: "ES2015 provides a default class constructor if one is not specified. As such, it is unnecessary to provide an empty constructor or one that simply delegates into its parent class, as in the following examples:" Tool gate (boolean). Backs K1, method half, and strengthens `fn-no-pass-through-wrapper`.

**Candidate Rule.** Delete a class or method that adds no behaviour; keep a type only when it owns state, enforces an invariant, or names a boundary.

**Level.** module.

**Tool gate.** Pylint `R0903` (`min-public-methods=2`, dataclasses exempt); PMD `UselessOverridingMethod`; ESLint `no-useless-constructor`.

**FAIL / PASS idea.** FAIL: `class TaxCalculator: def total(self, o): return o.total` and a constructor that only calls `super()`. PASS: `def total(order):` at module level, or a class that holds the rates and validates them.

**Decision: MERGE, no new card.** The class half is already `py-class-earns-its-instance` ("Give a class real state or a collaborator; otherwise write a module function"), which is stable and has Google plus the author behind it; add Refactoring.Guru and Pylint `R0903` to it. The method half is already `fn-no-pass-through-wrapper`; add PMD `UselessOverridingMethod` and ESLint `no-useless-constructor`. The "designed for future work that never came" origin is `mod-yagni` (stable). A new `mod-lazy-element` would repeat all three and fail rule 8. The only new fact worth recording is Pylint's default of 2 and its dataclass exemption, which makes `R0903` usable only as a prompt, not a hard gate.

## K2 — Temporary Field

5. https://refactoring.guru/smells/temporary-field (org: Refactoring.Guru). "Temporary fields get their values (and thus are needed by objects) only under certain circumstances. Outside of these circumstances, they’re empty." And: "This kind of code is tough to understand. You expect to see data in object fields but for some reason they’re almost always empty." Treatment: "Temporary fields and all code operating on them can be put in a separate class via Extract Class." Backs K2.

6. https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/attribute-defined-outside-init.html (org: Pylint). Rule `attribute-defined-outside-init / W0201`: "Used when an instance attribute is defined outside the __init__ method." The "Correct code" moves the assignment into `__init__` (`self.is_registered = False`) and leaves the later method to change it. Tool gate for the Python mechanism. Backs K2.

7. https://www.jetbrains.com/help/inspectopedia/FieldCanBeLocal.html (org: JetBrains). Inspection `FieldCanBeLocal`: "Reports private fields that are redundant and can be replaced with a local variable. If all local usages of a field are preceded by an assignment to that field, the field can be replaced with one or more local variables." The .NET sibling, `PrivateFieldCanBeConvertedToLocalVariable` (https://www.jetbrains.com/help/inspectopedia/PrivateFieldCanBeConvertedToLocalVariable.html, same organisation), says the same for C#. Tool gate. Backs K2's fix: if the field cannot be a local because it must survive across calls, it is real state; if it can, it was temporary.

**Candidate Rule.** Keep a field for state that lives as long as the object; move state used by one method to a parameter, a local, or a method object.

**Level.** module.

**Tool gate.** Pylint `W0201`; JetBrains `FieldCanBeLocal` (Java) and `PrivateFieldCanBeConvertedToLocalVariable` (C#).

**FAIL / PASS idea.** FAIL: `self.tax_base = ...` set inside `calculate_tax()` and read only there. PASS: `def calculate_tax(self, tax_base): ...`, or a field initialised in the constructor to a documented empty value and valid for the whole lifetime.

**Decision: NEW `mod-temporary-field`.** This is the only smell in the batch with no existing card. It is adjacent to `py-init-assign-only` (constructor body) but not the same rule: a class can keep `__init__` to assignments and still hide one algorithm's state in a field. `py-init-assign-only` is about *where* the work happens; this card is about *how long* the state lives.

**Counterpoint.** Lazily computed caches and genuinely optional state are fields that are empty until used. The Rule must say "state used by one algorithm", not "every field must always have a value"; a cache initialises to an explicit empty value and documents its invalidation, and serialisation models (ORM, pydantic) assign fields after construction, so mark those `N/A`. Pylint `W0201` has the same false positives on such frameworks.

## K3 — Insider Trading (Inappropriate Intimacy)

8. https://refactoring.guru/smells/inappropriate-intimacy (org: Refactoring.Guru). "One class uses the internal fields and methods of another class." Also: "Good classes should know as little about each other as possible. Such classes are easier to maintain and reuse." Backs K3's member-access half.

9. https://pkg.go.dev/cmd/go#hdr-Internal_packages (org: Google). "Code in or below a directory named "internal" is importable only by code that shares the same import path above the internal directory." A language-level gate for the import half. Backs K3.

10. https://openjdk.org/jeps/261 (org: OpenJDK). The Module System "provide for the reliable configuration and strong encapsulation of modules in all phases of development." And the reflection paragraph: access is denied to "public members of packages that are not exported or opened by their defining modules, or to non-public members of packages that are not opened by their defining modules". Backs K3; the strongest language-level statement that a module's internals are unreadable without an explicit export. `PREFIX?` `openjdk.org` is not in `tools/orgs.py`; add it to the `openjdk` org.

11. https://peps.python.org/pep-0008/ (org: Python Software Foundation). "Use one leading underscore only for non-public methods and instance variables." And: "Non-public attributes are those that are not intended to be used by third parties; you make no guarantees that non-public attributes won’t change or even be removed." Convention, not enforcement, which is why the coding-guidelines card pairs it with a linter. Backs K3's member-access half.

12. https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/protected-access.html (org: Pylint). Rule `protected-access / W0212`: "Used when a protected member (i.e. class member with a name beginning with an underscore) is accessed outside the class or a descendant of the class where it's defined." Tool gate for Python member access. Backs K3.

13. https://pmd.github.io/pmd/pmd_rules_java_design.html (org: PMD). Rule `LoosePackageCoupling`: "Avoid using classes from the configured package hierarchy outside of the package hierarchy, except when using one of the configured allowed classes." Tool gate for Java package access. Backs K3.

14. https://checkstyle.sourceforge.io/checks/imports/importcontrol.html (org: Checkstyle). `ImportControl`: "Controls what can be imported in each package and file. Useful for ensuring that application layering rules are not violated, especially on large projects." Tool gate for Java imports. Backs K3.

15. https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/internal (org: Microsoft). "You can access internal types or members only within files in the same assembly". A language boundary, not a linter, but the same practice: the default surface is closed until explicitly opened. Backs K3.

**Candidate Rule.** Keep a module's internals unreachable and unread: do not import its internal modules, and do not read or write another object's non-public members; expose a public method or move the behaviour.

**Level.** module.

**Tool gate.** Go `internal/` packages, Java modules (`exports`), Pylint `W0212`, PMD `LoosePackageCoupling`, Checkstyle `ImportControl`, import-linter contracts.

**FAIL / PASS idea.** FAIL: `from billing.internal.tax_tables import RATES` and `order._lines.append(line)` from outside `Order`. PASS: `from billing import calculate_tax` and `order.add_line(line)`, with a boundary check that fails the build on the import.

**Decision: MERGE into `mod-internals-unreachable`.** That card already owns the import half with Google (Go internal, Bazel visibility) and Microsoft (the `internal` keyword), and its tool gate is the build check. Add one clause for member access (the Refactoring.Guru + PEP 8 + Pylint trio gives it three organisations) and add OpenJDK, PMD and Checkstyle to the import half. Do not create a second card: "imports the internals" and "reads the internals" are the same boundary, enforced at two layers.

**Counterpoint.** Tests legitimately need internals, and Java's module `opens` and C#'s `InternalsVisibleTo` exist for that. The Rule applies to production callers; a test may use a documented test-only export, and the export is itself a commitment to maintain. Performance-critical code that reaches into a peer's buffer should move the operation onto that peer, not widen the field.

## K4 — Alternative Classes with Different Interfaces

16. https://refactoring.guru/smells/alternative-classes-with-different-interfaces (org: Refactoring.Guru). "Two classes perform identical functions but have different method names." Treatment: "Try to put the interface of classes in terms of a common denominator", then "you may be able to delete one of the classes." Backs K4. Its "When to Ignore" is in Counter-evidence.

17. https://rust-lang.github.io/api-guidelines/naming.html (org: Rust project). Rule C-CONV: "Conversions should be provided as methods, with names prefixed as follows:" (`as_`, `to_`, `into_`). Rule C-GETTER: "With a few exceptions, the get_ prefix is not used for getters in Rust code." Equivalent operations get one name, which is the naming half of K4. Backs K4.

18. https://google.aip.dev/130 (org: Google). Standard methods are fixed by category — "Standard resource methods: fetch or mutate a single resource (Get, Update, Delete)" — and the rationale is that they "offer the most uniform experience that allows users to apply their knowledge of one API to another." A naming standard for one operation, across APIs; the weakest of the three for the two-class case. Backs K4.

**Candidate Rule.** Give two types that do the same job the same method names, or merge them.

**Level.** module.

**Tool gate.** none; a reviewer compares the two surfaces.

**FAIL / PASS idea.** FAIL: `UserRepo.fetch(id)` and `AccountRepo.load(id)` for the same lookup. PASS: both `get(id)`, or one class that owns both.

**Decision: MERGE into `mod-one-name-per-concept`.** Its Rule ("Use one name for one concept across the codebase") and its FAIL example (`get_customer(); load_client(); fetch_account() # same entity`) are already this smell. Add the Refactoring.Guru and Rust sources; note that the duplicate-implementation half is `code-consistency-drift`. No new card: a second card would repeat a stable Rule, and the existing card's counterpoint (names are not bikeshedding; the test is consistency and truth) already answers the objection.

**Counterpoint.** Libraries you do not own cannot be merged, and an adapter's whole job is to present a different interface (Refactoring.Guru's own "When to Ignore"). The Rule applies to two classes in this repo that do the same job, not to an adapter at a boundary; the adapter should say which interface it adapts and why.

## K5 — Data Class

19. https://refactoring.guru/smells/data-class (org: Refactoring.Guru). "A data class refers to a class that contains only fields and crude methods for accessing them (getters and setters). These are simply containers for data used by other classes. These classes don’t contain any additional functionality and can’t independently operate on the data that they own." Its treatment says: "If a class contains public fields, use Encapsulate Field to hide them from direct access and require that access be performed via getters and setters only." Backs the candidate Rule, and is the source of the contradiction below.

20. https://openjdk.org/jeps/395 (org: OpenJDK). Records are "classes that act as transparent carriers for immutable data. Records can be thought of as nominal tuples." And: "Because record classes make the semantic claim of being transparent carriers for their data, a record class acquires many standard members automatically." Counter-evidence: the language now ships a data-carrier type on purpose. `PREFIX?` `openjdk.org`.

21. https://docs.python.org/3/library/dataclasses.html (org: Python Software Foundation). "This module provides a decorator and functions for automatically adding generated special methods such as `__init__()` and `__repr__()` to user-defined classes." And: "The member variables to use in these generated methods are defined using PEP 526 type annotations." Counter-evidence.

22. https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/builtin-types/record (org: Microsoft). "The `record` modifier provides built-in functionality for encapsulating data." And: "Built-in behavior useful for a data-centric reference type". Counter-evidence.

23. https://kotlinlang.org/docs/data-classes.html (org: JetBrains). "Data classes in Kotlin are primarily used to hold data." Counter-evidence.

**Candidate Rule.** A class that only holds data and accessors is a smell; move the behaviour onto it.

**Level.** module.

**Tool gate.** none. Pylint `R0903` deliberately exempts dataclasses, which is the opposite of a gate.

**FAIL / PASS idea.** FAIL: `class Order: lines; total(order)` where `total` reads only `order.lines`. PASS: `class Order: lines; def total(self): ...`, or a record that carries the data and a separate policy object that needs collaborators.

**Decision: SKIP as a card.** The smell's treatment is contradicted by four independent organisations that ship data-carrier types: OpenJDK records, Python dataclasses, C# records, Kotlin data classes. The part that survives is not "a class should have behaviour" but "a calculation that reads only one object's fields belongs on that object", which is exactly `mod-behaviour-lives-with-state`. That card is a draft with only the author's guide behind it; the Refactoring.Guru treatment ("you may find functionality that would be better located in the data class itself... use Move Method and Extract Method to migrate this functionality to the data class") is one more organisation backing it, though that draft still needs two more. Add that page there instead of resurrecting Data Class.

**Counterpoint.** A data bag is still a problem when a service reaches into it and re-implements the invariant in three places. That is the anemic-domain objection, and it is already the Why of `mod-behaviour-lives-with-state`; it does not justify a rule against records, dataclasses or DTOs.

## K6 — Comments as deodorant

24. https://refactoring.guru/smells/comments (org: Refactoring.Guru). "Comments are usually created with the best of intentions, when the author realizes that his or her code isn’t intuitive or obvious. In such cases, comments are like a deodorant masking the smell of fishy code that could be improved." Also: "The best comment is a good name for a method or class." Backs K6. Its "When to Ignore" is in Counter-evidence.

25. https://www.kernel.org/doc/html/latest/process/coding-style.html (org: Linux kernel). Section 8: "NEVER try to explain HOW your code works in a comment: it’s much better to write the code so that the working is obvious, and it’s a waste of time to explain badly written code." Also: "Generally, you want your comments to tell WHAT your code does, not HOW." Backs K6.

26. https://google.github.io/styleguide/cppguide.html#Comments (org: Google). "But remember: while comments are very important, the best code is self-documenting. Giving sensible names to types and variables is much better than using obscure names that you must then explain through comments." Backs K6.

27. https://flink.apache.org/how-to-contribute/code-style-and-quality-common/ (org: Apache Software Foundation). "Golden rule: Comment as much as necessary to support code understanding, but don’t add redundant information." And: "In-code comments should not state redundant information about the “what” and “how” that is already obvious in the code itself." Backs K6.

**Candidate Rule.** If a comment explains what the code does, rewrite the code; keep comments for a reason, a constraint, or a trade-off.

**Level.** function.

**Tool gate.** none; the comment is the artefact under review.

**FAIL / PASS idea.** FAIL: `i += 1  # increment i` and `# this loop is messy but works` above a nested loop. PASS: extract the loop into `retry_transient_calls()`; keep `# Billing rounds half-up; the ledger does not, so this is deliberately not Decimal.quantize().`

**Decision: MERGE into `fn-comments-explain-why`.** Its Rule already says "never restate what the next line does", and its FAIL already has `counter += 1  # increment the counter`. Add the Linux kernel and Refactoring.Guru sources; the card's note currently says only Google and the Linux kernel say to rewrite before commenting, so this pass gives that point four organisations and lets it stay firmly in the Why. `fn-comments-survive-context` is a different rule (a comment must still make sense without the ticket), so do not merge there.

**Counterpoint.** Refactoring.Guru's own "When to Ignore" allows comments that explain why a particular implementation was chosen and comments that explain a complex algorithm after simplification has been tried; a regulatory formula can deserve a comment even when the code is clean. The Rule keeps those: it bans comments that explain *what* as a substitute for readable code, not comments that carry information the code cannot carry.

## Counter-evidence

- **K1**: Refactoring.Guru's "When to Ignore" says "Sometimes a Lazy Class is created in order to delineate intentions for future development, In this case, try to maintain a balance between clarity and simplicity in your code." Pylint exempts dataclasses and Enums from `R0903`, so the gate does not fire on the data carriers K5 discusses. The Clean Code position (Robert Martin, a person) favours many small functions, which is the standing objection to deleting forwarding methods; `fn-no-pass-through-wrapper` already records it.
- **K2**: no fetched source disagrees with the narrow Rule. The general tension is that caches, optional state and ORM/pydantic models are fields that are not valid at construction time. No organisation page was found that endorses a field as one method's scratch space, so the conflict sits in the card's scope, not in the sources.
- **K3**: Go's `internal` and Microsoft's `internal` are import/assembly boundaries, not member privacy; Java modules can `opens` a package to reflection; Python's underscore is a convention with no enforcement. So the Rule must be scoped to "internals the module has not exported", not "every name with an underscore". ArchUnit and import-linter were not fetched in this pass.
- **K4**: Refactoring.Guru's "When to Ignore": "Sometimes merging classes is impossible or so difficult as to be pointless. One example is when the alternative classes are in different libraries that each have their own version of the class." An adapter that presents a third-party interface is not this smell. Google AIP-130 is a taxonomy of standard methods; its consistency rationale is real, but it does not say two arbitrary classes must share names.
- **K5**: the four counter-organisations above are the strongest evidence in the batch. Refactoring.Guru's advice to encapsulate public fields and add getters/setters is the part modern records and dataclasses reject; its advice to move a one-object calculation onto the object survives and belongs in `mod-behaviour-lives-with-state`.
- **K6**: Refactoring.Guru's "When to Ignore": comments are useful "When explaining why something is being implemented in a particular way" and "When explaining complex algorithms (when all other methods for simplifying the algorithm have been tried and come up short)." The card's counterpoint already answers this by keeping the why.

## Also read, no rule

- **SonarSource**: `rules.sonarsource.com` and the RSPEC repository are gone (Sonar community, "Online reference rules.sonarsource.com is gone", 10 Feb 2026: https://community.sonarsource.com/t/online-reference-rules-sonarsource-com-is-gone/177440). `S1450` ("Private fields only used as local variables in methods should become local variables") and `S2094` ("Classes should not be empty") would have been K2/K1 gates, but no rule page or rule source could be fetched. Excluded, not counted.
- **Microsoft, General Naming Conventions** (https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/general-naming-conventions): read; it asks for a consistent set of conventions and readable names, but states no "same name for the same concept" rule. Not counted for K4. The page is the 2nd-edition reprint and carries a stale-content note.
- **Microsoft, Names of Type Members** (https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/names-of-type-members): read; no same-name-for-equivalent-operation rule found. Not counted for K4.
- **PEP 8, Comments** (https://peps.python.org/pep-0008/#comments): says "Comments that contradict the code are worse than no comments" and asks for up-to-date comments; that is the stale-comment problem, not deodorant. Not counted for K6.
- **PMD 7 performance ruleset**: `SingularField` is not in PMD 7.29's performance page, so no K2 gate from PMD. The old 6.x page was not used.
- **Refactoring.Guru `/smells/lazy-element`** returns 404; the live page is `/smells/lazy-class`.
- **Pylint all-options page** did not render the `min-public-methods` option; the default of 2 was read from the checker source instead.

## People cited (never count)

- Martin Fowler and Kent Beck, *Refactoring: Improving the Design of Existing Code*, 2nd ed. (2018): the catalogue names used in this file, including Lazy Element and Insider Trading. The book was not fetched; no quote is attributed to it.
- Alexander Shvets, the author of Refactoring.Guru, a single-author site that `tools/orgs.py` maps as an organisation.
- John Ousterhout: pass-through methods and deep modules, already a person in `fn-no-pass-through-wrapper` and `mod-deep-modules`.
- Robert C. Martin: many small functions, the counterpoint to K1's method half.

## Per-claim organisation count

| Smell | Distinct organisations | Confidence |
|---|---|---|
| K1 Lazy Element | Refactoring.Guru, Pylint, PMD, ESLint (4) | High for each half separately: class half 2 (Refactoring.Guru, Pylint) plus stable `py-class-earns-its-instance`; method half 2 (PMD, ESLint) plus the 3 already assembled for `fn-no-pass-through-wrapper` in `design-depth-orgs-D.md` |
| K2 Temporary Field | Refactoring.Guru, JetBrains, Pylint (3) | Medium: Pylint `W0201` is a gate on the mechanism, not a prose statement of "one method's state must not be a field" |
| K3 Insider Trading | Refactoring.Guru, Google, OpenJDK, PSF, Pylint, PMD, Checkstyle, Microsoft (8) | High; the member-access clause alone has 3 (Refactoring.Guru, PSF, Pylint) |
| K4 Alternative Classes | Refactoring.Guru, Rust, Google (3) | Medium: Google AIP-130 backs standard method names, not the two-class case; the merge into stable `mod-one-name-per-concept` does not need a new count |
| K5 Data Class | Refactoring.Guru (1) against OpenJDK, PSF, Microsoft, JetBrains (4) | High confidence to skip |
| K6 Comments as deodorant | Linux kernel, Refactoring.Guru, Google, Apache Flink (4) | High; Google and Apache Flink are already in `fn-comments-explain-why`, so this adds 2 new organisations |

## Prefix gaps for the maintainer

- `openjdk.org` -> `openjdk` (`openjdk` is already an org; only `wiki.openjdk.org` has a prefix today). Needed for JEP 261 and JEP 395.
- Everything else cited here is covered: `refactoring.guru`, `pylint.readthedocs.io`, `eslint.org`, `pmd.github.io`, `jetbrains.com`, `pkg.go.dev`, `peps.python.org`, `checkstyle.sourceforge.io`, `learn.microsoft.com`, `rust-lang.github.io`, `google.aip.dev`, `docs.python.org`, `kotlinlang.org`, `kernel.org`, `google.github.io`, `flink.apache.org`.

# Design depth: organisation sources for D1–D5

Backs five design-depth claims. Each quote below was read on the live page named (for the Pylint rule, on the checker source, since the docs page renders a nav sidebar and the message is the same text). People never count toward the three organisations. A URL that no prefix in `tools/orgs.py` covers is flagged `PREFIX?` so the maintainer can map it.

## D1 — a module should have a small, simple interface that hides substantial implementation; an interface nearly as complex as the implementation is a smell

Backs `mod-deep-modules`.

- **Microsoft**, https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/abstractions-abstract-types-and-interfaces: "The main difficulty is getting the right set of members, no more and no fewer. If an abstraction has too many members, it becomes difficult or even impossible to implement. If it has too few members for the promised functionality, it becomes useless in many interesting scenarios." Also "Too many abstractions in a framework also negatively affect usability of the framework." Backs both halves — small interface ("no more and no fewer") and big-interface-is-a-smell ("too many members … difficult to implement"). Note the page is the .NET Framework Design Guidelines (Cwalina/Abrams), reprinted by Microsoft.
- **Rust (Rust project)**, https://rust-lang.github.io/api-guidelines/future-proofing.html, C-NEWTYPE-HIDE: "this use of newtypes allows us to promise less to the client. The client does not know *how* the result iterator is constructed or represented, which means the representation can change in the future without breaking client code." Same page, C-STRUCT-PRIVATE: "Making a field public is a strong commitment: it pins down a representation choice … consider providing getter/setter methods and hiding fields instead." Backs "small interface that hides substantial implementation" (information hiding).
- **Google**, https://go.dev/wiki/CodeReviewComments (Interfaces section): "Do not define interfaces before they are used: without a realistic example of usage, it is too difficult to see whether an interface is even necessary, let alone what methods it ought to contain." And "The implementing package should return concrete (usually pointer or struct) types: that way, new methods can be added to implementations without requiring extensive refactoring." Backs the narrow/minimal-interface half. Supporting convention, https://go.dev/doc/effective_go (Interface names): "By convention, one-method interfaces are named by the method name plus an `-er` suffix". Google backs "narrow interface" strongly and "hides substantial implementation" only indirectly — treat Google as the weakest of the three D1 orgs.

Counterpoint (person, not counted): the card already records that Ousterhout and Robert Martin disagree about many small functions vs deep modules; Martin favours small functions.

## D2 — delete a method/class that only forwards; keep wrappers that validate, adapt, or narrow

Backs `fn-no-pass-through-wrapper`.

- **ESLint**, https://eslint.org/docs/latest/rules/no-useless-constructor: "ES2015 provides a default class constructor if one is not specified. As such, it is unnecessary to provide an empty constructor or one that simply delegates into its parent class". The rule's "correct" examples keep constructors that do something extra (`super('foo')`, `doSomething()`), which matches the card's "keep wrappers that validate, adapt, or narrow". Tool gate (a rule with a documented threshold).
- **Pylint (PyCQA)**, https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/useless-parent-delegation.html — rule W0246 "useless-parent-delegation": "Useless parent or super() delegation in method", "Used whenever we can detect that an overridden method is useless, relying on parent or super() delegation to do the same thing as another method from the MRO." (Verbatim text read on the checker source, `github.com/pylint-dev/pylint`, `pylint/checkers/classes/class_checker.py`.) Tool gate. `PREFIX?` `pylint.readthedocs.io` (and `github.com/pylint-dev/`) are not in `tools/orgs.py`; add a prefix to `pycqa`.
- **Refactoring.Guru**, https://refactoring.guru/smells/middle-man: "If a class performs only one action, delegating work to another class, why does it exist at all?" and "If most of a method's classes delegate to another class, Remove Middle Man is in order." Its "When to Ignore" matches the card's keep-clause: "Don't delete middle man that have been created for a reason … Some design patterns create middle man on purpose (such as Proxy or Decorator)." This is a single-author site (Alexander Shvets) mapped as an org in `tools/orgs.py` (`refactoring-guru`), so it counts but is the weakest of the three.

D2 is also covered from the Go side by the same "Do not define interfaces before they are used" line, but that is the same Google org already used for D3, and it is about interfaces rather than forwarding methods, so it is not double-counted here.

## D3 — a seam/adapter is real only with two implementations; one adapter is a hypothetical seam

Backs the `mod-yagni` second-use clause ("add it when the need or a second use appears"); also informs any single-implementation-interface finding. `mod-yagni` is already stable, so these are further sources.

- **Microsoft**, https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/abstractions-abstract-types-and-interfaces: "❌ DO NOT provide abstractions unless they are tested by developing several concrete implementations and APIs consuming the abstractions." This is the exact D3 claim — no abstraction without several concrete implementations.
- **Google**, https://go.dev/wiki/CodeReviewComments (Interfaces): "Do not define interfaces before they are used: without a realistic example of usage, it is too difficult to see whether an interface is even necessary, let alone what methods it ought to contain." And "Do not define interfaces on the implementor side of an API 'for mocking'; instead, design the API so that it can be tested using the public API of the real implementation."
- **AWS**, https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html (Issues and considerations): "The additional adapter code that makes the architecture pluggable is justified only if the application component requires several input sources and output destinations to write to, or when the inputs and output data store has to change over time. Otherwise, the adapter becomes another additional layer to maintain, which introduces maintenance overhead." This is the caveat that a one-implementation adapter is a hypothetical seam.

Counter-evidence / tension: the same AWS page's "Applicability" lists reasons to adopt hexagonal even without several adapters ("You want to decouple your application architecture to create components that can be fully tested"), so AWS's support for D3 is a caveat, not a blanket rule. Joshua Bloch's "program to an interface" (Effective Java, a person, not fetched) is the classic counter-tension and is not cited.

## D4 — test through the public interface, not internals

Backs `fn-test-behaviour-not-implementation` (already stable). Only new organisations, not already in its `borrowed_from` (Google, Microsoft, Spotify, plus persons Kent Beck and Kent C. Dodds).

- **Rust (Rust project)**, https://doc.rust-lang.org/book/ch11-03-test-organization.html: "Integration tests are entirely external to your library and use your code in the same way any other external code would, using only the public interface and potentially exercising multiple modules per test." On private functions it stays neutral, which is why the card already names it as the debate: "There's debate within the testing community about whether or not private functions should be tested directly … If you don't think private functions should be tested, there's nothing in Rust that will compel you to do so." New org.

Google's "Change-Detector Tests Considered Harmful" (testing.googleblog.com, Testing on the Toilet) is a strong restatement but the same Google org as the existing SWE ch.12, so it adds no new org.

## D5 — design twice: record alternatives before committing

Backs `code-adr` (already stable). Only what adds beyond its `borrowed_from` (AWS, Microsoft, Google, GOV.UK, Spotify, Cognitect). Each template below mandates an "alternatives considered" section.

- **Rust (Rust project)**, https://github.com/rust-lang/rfcs/blob/master/0000-template.md, "Rationale and alternatives": "What other designs have been considered and what is the rationale for not choosing them?" plus a "Drawbacks: Why should we *not* do this?" section.
- **Python Software Foundation**, https://peps.python.org/pep-0012/ (PEP 12 template, "Suggested Sections"): "Rejected Ideas — [Why certain ideas that were brought while discussing this PEP were not ultimately pursued.]"
- **Kubernetes**, https://github.com/kubernetes/enhancements/blob/master/keps/NNNN-kep-template/README.md: the KEP template mandates a "Drawbacks" and an "Alternatives" section (both in the required outline).
- **Oxide Computer Company**, https://rfd.shared.oxide.computer/rfd/0001 (RFD 1): "Document the viable options (or a subset of options if we can easily rule some out) and the benefits and drawbacks of each option." `PREFIX?` `rfd.shared.oxide.computer` is not in `tools/orgs.py`; add an `oxide` org and prefix.

Google design docs, the Microsoft engineering playbook's design reviews, and AWS's ADR guidance restate the same practice but are the orgs already in `code-adr`, so they add no new org here.

## Counter-evidence (whole pass)

- D1: Martin Fowler's Clean-Code-flavoured preference for many small functions is the Ousterhout–Martin disagreement already recorded in the card; it argues against "deep" modules.
- D3: see the AWS "Applicability" tension and the unverified "program to an interface" counter-tension above.
- D2: Refactoring.Guru's "When to Ignore" (Proxy/Decorator) is not counter-evidence but confirms the card's "keep wrappers that adapt" clause.

## Also read, no rule (excluded)

- Google API Design Guide, https://cloud.google.com/apis/design — fetched; the landing page is a table of contents and states no small-surface rule on that page, so it is not cited.
- Google AIP, https://google.aip.dev/general — fetched; a directory of AIPs, no small-interface rule on the page itself.
- SonarSource and JetBrains ("Interface never implemented" / single-implementation-interface) — not reached; neither is cited.
- Go Proverbs ("The bigger the interface, the weaker the abstraction"; "A little copying is better than a little dependency") — Rob Pike, a person, and `go-proverbs.github.io` is not in the org map, so not cited.

## Per-claim organisation count

| Claim | Organisations (distinct) | Confidence |
|---|---|---|
| D1 | Microsoft, Rust, Google (3) | High for Microsoft + Rust; Google backs "narrow interface" indirectly |
| D2 | ESLint, Pylint/PyCQA, Refactoring.Guru (3) | High for ESLint + Pylint (tool gates); Refactoring.Guru is single-author |
| D3 | Microsoft, Google, AWS (3) | High |
| D4 | Rust (1 new; 3 already in the card) | High |
| D5 | Rust, Python/PSF, Kubernetes, Oxide (4 new) | High |

Prefix gaps for the maintainer: `pylint.readthedocs.io` (and `github.com/pylint-dev/`) → `pycqa`; `rfd.shared.oxide.computer` → `oxide` (new org).

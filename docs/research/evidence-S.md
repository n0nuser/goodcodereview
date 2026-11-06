# Evidence for writer S: smell merges and one promotion (2026-11-06)

Every URL below was fetched by writer S on 2026-11-06 and the quote copied from the fetched page. Format: `card-id | URL | org | "verbatim quote" | clause it backs`.

## Rows

mod-no-module-mutable-state | https://google.github.io/styleguide/pyguide.html#25-mutable-global-state | Google | "Module-level values or class attributes that can get mutated during program execution." | widened applies_when: class attributes, not only module values

mod-no-module-mutable-state | https://google.github.io/styleguide/pyguide.html#25-mutable-global-state | Google | "Module-level constants are permitted and encouraged." | the frozen constant exception

mod-no-module-mutable-state | https://github.com/uber-go/guide/blob/master/style.md#avoid-mutable-globals | Uber | "Avoid mutating global variables, instead opting for dependency injection." | widened Rule: package-level mutable state is the same failure

mod-no-module-mutable-state | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2211 | Microsoft | "Static fields that are neither constants nor read-only are not thread-safe." | widened Rule: static fields carry mutable state

mod-no-module-mutable-state | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2211 | Microsoft | "static fields are best used to store data that does not change" | the frozen constant exception

py-class-earns-its-instance | https://refactoring.guru/smells/lazy-class | Refactoring.Guru | "Understanding and maintaining classes always costs time and money. So if a class doesn’t do enough to earn your attention, it should be deleted." | Rule: a class must earn its place

py-class-earns-its-instance | https://pylint.readthedocs.io/en/latest/user_guide/messages/refactor/too-few-public-methods.html | Pylint | "Used when class has too few public methods, so be sure it's really worth it." | Rule: a class with almost no public methods needs a reason; tool_gate R0903

py-class-earns-its-instance | https://raw.githubusercontent.com/pylint-dev/pylint/main/pylint/checkers/design_analysis.py | Pylint | "min-public-methods" with "default": 2 | tool_gate: the threshold Pylint applies

py-class-earns-its-instance | https://raw.githubusercontent.com/pylint-dev/pylint/main/pylint/checkers/design_analysis.py | Pylint | "Check if a class is exempt from too-few-public-methods." | note: the dataclass exemption (checked in the same file, `_is_exempt_from_public_methods`)

mod-internals-unreachable | https://refactoring.guru/smells/inappropriate-intimacy | Refactoring.Guru | "One class uses the internal fields and methods of another class." | member-access clause

mod-internals-unreachable | https://peps.python.org/pep-0008/ | Python Software Foundation | "Use one leading underscore only for non-public methods and instance variables." | member-access clause

mod-internals-unreachable | https://peps.python.org/pep-0008/ | Python Software Foundation | "Non-public attributes are those that are not intended to be used by third parties; you make no guarantees that non-public attributes won’t change or even be removed." | member-access clause: no caller contract for non-public members

mod-internals-unreachable | https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/protected-access.html | Pylint | "Used when a protected member (i.e. class member with a name beginning with an underscore) is accessed outside the class or a descendant of the class where it's defined." | member-access clause; tool_gate W0212

mod-one-name-per-concept | https://refactoring.guru/smells/alternative-classes-with-different-interfaces | Refactoring.Guru | "Two classes perform identical functions but have different method names." | Why/FAIL: two classes doing the same job

mod-one-name-per-concept | https://refactoring.guru/smells/alternative-classes-with-different-interfaces | Refactoring.Guru | "Try to put the interface of classes in terms of a common denominator" | PASS: share the method name or merge

mod-one-name-per-concept | https://rust-lang.github.io/api-guidelines/naming.html | Rust project | "Conversions should be provided as methods, with names prefixed as follows:" | one name for one operation

mod-one-name-per-concept | https://rust-lang.github.io/api-guidelines/naming.html | Rust project | "With a few exceptions, the get_ prefix is not used for getters in Rust code." | equivalent operations get one name

mod-one-name-per-concept | https://google.aip.dev/130 | Google | "offer the most uniform experience that allows users to apply their knowledge of one API to another" | same name for the same operation across surfaces

fn-comments-explain-why | https://www.kernel.org/doc/html/latest/process/coding-style.html | Linux kernel | "NEVER try to explain HOW your code works in a comment: it’s much better to write the code so that the working is obvious, and it’s a waste of time to explain badly written code." | Why: rewrite the code instead of commenting it

fn-comments-explain-why | https://www.kernel.org/doc/html/latest/process/coding-style.html | Linux kernel | "Generally, you want your comments to tell WHAT your code does, not HOW." | Why: comments carry what the code does, not its mechanism

fn-comments-explain-why | https://refactoring.guru/smells/comments | Refactoring.Guru | "The best comment is a good name for a method or class." | Why: rename before commenting

fn-comments-explain-why | https://refactoring.guru/smells/comments | Refactoring.Guru | "comments are like a deodorant masking the smell of fishy code that could be improved" | Why: a comment that explains the code is evidence the code is unclear

mod-law-of-demeter | https://pmd.github.io/pmd/pmd_rules_java_design.html#lawofdemeter | PMD | "The law of Demeter is a simple rule that says \"only talk to friends\"." | Rule: call your direct collaborators

mod-law-of-demeter | https://pmd.github.io/pmd/pmd_rules_java_design.html#lawofdemeter | PMD | "It forbids fetching data from \"too far away\", for some definition of distance, in order to reduce coupling between classes or objects of different levels of abstraction." | Rule: do not reach through one object to another

mod-law-of-demeter | https://pmd.github.io/pmd/pmd_rules_java_design.html#lawofdemeter | PMD | "The default trustRadius of 1 corresponds to the original law of Demeter (you’re only allowed one getter call on untrusted values)." | tool_gate: PMD's chain threshold

mod-law-of-demeter | https://pmd.github.io/pmd/pmd_rules_java_design.html#lawofdemeter | PMD | "Be aware that this rule is prone to many false-positives and low-priority warnings." | counterpoint: flag a chain, do not ban every chain

mod-law-of-demeter | https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html | Google | "Only ask for things you directly need, If you are a CarEngine, don't ask for FuelTank, only ask for Fuel." | Rule: ask the collaborator you need, not the object it happens to hold

mod-law-of-demeter | https://www.jetbrains.com/help/inspectopedia/LawOfDemeter.html | JetBrains | "The Law of Demeter is not really a law, but specifies a style guideline: never call a method on an object received from another call." | Rule: no call on an object returned by another call

mod-law-of-demeter | https://www.jetbrains.com/help/inspectopedia/LawOfDemeter.html | JetBrains | "On the other hand, you may need to write many wrapper methods to meet this guideline." | counterpoint: the wrapper cost

mod-law-of-demeter | https://www.jetbrains.com/help/inspectopedia/LawOfDemeter.html | JetBrains | "Ignore calls to library methods and access to library fields" with "Default value: Selected" | counterpoint: leave a stable library chain alone

## Organisation count per card, after the edits

- `mod-no-module-mutable-state`: Google (module values and class attributes), Uber (mutable globals), Microsoft (*static* fields) = 3 for "state outside an instance".
- `py-class-earns-its-instance`: Google (Go review guide), the creator (pablogonzalez.me), Refactoring.Guru, Pylint = 4, and the creator alone satisfies the stable floor.
- `mod-internals-unreachable`: import half has Google (Go internal), Bazel, Microsoft; member half has Refactoring.Guru, PSF (PEP 8), Pylint = 3 each.
- `mod-one-name-per-concept`: already stable with 5 orgs; the two-class case adds Refactoring.Guru, Rust and Google (AIP-130).
- `fn-comments-explain-why`: Rule has Google, Mozilla, Apache Flink and PEP 8; the rewrite point in the Why has Google, the Linux kernel and Refactoring.Guru.
- `mod-law-of-demeter`: PMD, Google and JetBrains = 3 for the Rule, promoted to stable.

## Doubts

1. `mod-no-module-mutable-state`: widening `applies_when` to class/static fields while the Rule said "at module level" would make a class-field FAIL impossible to mark against the Rule. I widened the Rule to "Keep no mutable state outside an instance." The three sources above back that wording; Google and Microsoft cover class/static state and Uber covers package-level state. Reverse this if the coordinator wants the old Rule text.
2. `mod-law-of-demeter`: promotion leaves `severity: discuss`. PMD and JetBrains gate it, but both document false positives and the counterpoint narrows the rule to three or more layers, so `discuss` matches the card's own advice.

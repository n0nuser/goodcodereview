# Judge report: other cards (Opus)

Scope: the 21 cards in `part-other.txt`. I fetched every `borrowed_from` URL once with curl, saved it under the session scratchpad, and grepped the text. Two pages were blocked (HTTP 403 to curl and WebFetch) and are marked UNFETCHED: `intellij-support.jetbrains.com/hc/en-us/articles/206544839` and `medium.com/alan/how-we-improved-our-python-backend-start-up-time-2c33cd4873c8`. For edited cards I judged the `git diff` plus whether the card still holds. Org counts follow `tools/orgs.py` (`org_of`): Bazel and Go both map to Google, and Refactoring.Guru counts.

Cross-cutting point (rule 7, sourcing chatter in the Counterpoint): fn-no-stringly-typed-returns, mod-behaviour-lives-with-state, py-test-hygiene, mod-no-shotgun-surgery, py-class-earns-its-instance and mod-one-name-per-concept all name a source in the Counterpoint. Rule 7 allows it in the Why only.

## fn-comments-explain-why — ISSUES

1. consider, check 6. The new Why sentences say the same thing twice: "Rename before commenting: clearer code needs fewer comments. When a comment explains how the code works, rename the thing or extract the step. The comment is evidence that the code needs one." In "needs one", "one" has no clear referent. Fix: cut it to "Rename or extract a step before you comment how the code works."
2. consider, check 1. The kernel page says "you want your comments to tell WHAT your code does, not HOW" (coding-style.html, section 8). It backs the rewrite point in the Why, but at function level it asks for WHAT comments, which pulls against the Rule's "never restate what". Keep the kernel for the Why only; the note already says so.

The Rule clause has 4 orgs, confirmed: Google ("comments ... explain why some code exists"), Mozilla ("restating the code in prose is not a good use of comments"), Flink ("In-code comments help explain the 'why'"), PSF/PEP 8 (inline comments are "distracting if they state the obvious").

## fn-known-keys-get-a-type — ISSUES

1. act, check 2 (independence). PEP 589's author is "Jukka Lehtosalo", who also created mypy. The mypy TypedDict page and PEP 589 come from the same author and describe the same feature, so they are not independent. The mypy page is also a feature description ("TypedDict lets you give precise types for dictionaries that represent objects with a fixed schema"), which rule 3 treats as a definition. That leaves 2 independent practice sources: PSF/PEP 589 ("too lenient, as arbitrary string keys can be used") and attrs ("Dictionaries are not for fixed fields ... if your dict has a fixed and known set of keys, it is an object, not a hash"). Fix: go back to `status: draft`, `lacks: orgs`, or add a third independent org that recommends a record type over a dict.
2. consider, check 3. `tool_gate: mypy --strict; an invalid TypedDict key is an error` cannot catch the FAIL. `dict[str, Any]` type-checks under `--strict`; mypy flags bad keys only once the code already uses a TypedDict. Fix: name `--disallow-any-explicit` (or `disallow_any_explicit`) as the gate for the FAIL shape, or say "partial".

## fn-no-stringly-typed-returns — ISSUES

1. act, check 6/rule 7. Counterpoint: "Microsoft says not to use an enum for one." This is sourcing chatter. Fix: "An open set stays a string."
2. act, check 4. The widened Rule ("an enum, a tagged union or a sealed hierarchy ... not a bare string or boolean") now overlaps two stable cards. One is `fn-bool-arg-at-callsite` ("Replace a boolean flag argument with an enum ..."). The other is `fn-variants-as-tagged-union` ("Model variants as a tagged union, and make every switch ... fail the build"). Fix: limit the Rule to strings, which the id names, and point to the other two cards.
3. act, check 2. Counted per clause, the string half has two orgs that state it: Microsoft ("DO use an enum to strongly type parameters, properties, and return values that represent sets of values") and Apple (WWDC20 10680: "turn these constants into an enum or a struct with a raw value of type String"). Rust's C-CUSTOM-TYPE is about `bool` and `Option` arguments, not strings ("Arguments convey meaning through types, not bool or Option"). The Kotlin page is a language-feature page (sealed classes), with no advice against strings. If finding 2 cuts the boolean half, the card has 2 orgs plus one feature page. Fix: `status: draft`, `lacks: orgs`, or add a third org that advises against string status values.
4. consider, check 3. `tool_gate: mypy --strict` does not check that matches are exhaustive. mypy's "Error codes for optional checks" page lists `exhaustive-match` as on only "If enabled with --enable-error-code exhaustive-match". Fix: name that flag or `assert_never`.
5. consider, check 3. The id says "returns", but `applies_when` now says "returns or accepts". Rename the id, or drop "accepts".

## mod-behaviour-lives-with-state — ISSUES

1. act, rule 7. The Counterpoint has "Microsoft's CRUD exception still holds" and "DevIQ expects an anemic model in a functional design". Fix: state the exceptions without naming sources ("A simple CRUD context can keep a data-only model; a functional design keeps behaviour in functions over data").
2. consider, check 6. The Counterpoint runs to six sentences. The sentence listing Java, C#, Kotlin and Python records can go.

Sources confirmed: Microsoft ("The entity's methods take care of the invariants and rules of the entity instead of having those rules spread across the application layer"), PMD DataClass ("poor data-behaviour proximity"), DevIQ ("should use encapsulation to manage their internal state and behavior"). The Rule now has one clause, with 3 orgs.

## mod-internals-unreachable — ISSUES

1. consider, check 2. The note counts "Google (Go internal packages), Bazel and Microsoft" as if Bazel were a separate org. `org_of("https://bazel.build/...")` returns `google`. The import half has 3 orgs only because the Cursor page also says "Make internals unreachable from outside the module, so an import from outside fails the build." Fix the note to say Google (Go, Bazel), Microsoft and Cursor.
2. consider, check 4. The new Why sentence "Code that reaches through another object also has to know how that object is built" restates the new `mod-law-of-demeter` card. Cut it here.
3. consider, check 3. Counterpoint: "Java's `opens` ... give them a door." `opens` grants only runtime reflective access. A test that compiles against an internal package needs a qualified `exports ... to` or `--add-exports` / `--patch-module`. Fix: say "a qualified `exports ... to`".

Member half, confirmed: Refactoring.Guru ("One class uses the internal fields and methods of another class"), PSF/PEP 8 ("Non-public attributes are those that are not intended to be used by third parties"), Pylint W0212 ("accessed outside the class"). 3 orgs.

## mod-no-module-mutable-state — ISSUES

1. act, check 1/2. The Rule widened from "at module level" to "outside an instance", which pulls in static and class fields. CA2211 does not back that widening. Its Cause is "A public or protected static field is not constant nor is it read-only", and it says "It is safe to suppress a warning from this rule if you are developing an application". The Uber Go guide has no class fields. Only Google 2.5 names class attributes ("Module-level values or class attributes that can get mutated"). The class-field clause has 1 org, and the new FAIL `class Registry: _clients = {}` is a private class attribute that CA2211 would not flag. Fix: keep the Rule at module level and put the class-field point in the Why, or find two more orgs.
2. consider, check 3. Google 2.5 does not ban mutable globals outright: "In those rare cases where using global state is warranted, mutable global entities should be declared at the module level ... and made internal by prepending an _". The note says "each says to avoid mutable global or static state and allow constants". Fix: say Google allows a rare internal global behind functions.

## mod-one-name-per-concept — ISSUES

1. consider, check 1. `google.aip.dev/130` was added but the note does not mention it. Its guidance is about choosing a method category ("API authors should choose from the defined categories"), not one name per concept, and it adds no org because Google is already cited. Drop it, or say what it backs.
2. consider, check 1. Rust C-CONV ("Ad-hoc conversions follow as_, to_, into_ conventions") is a conversion-prefix convention. It backs the two-class case only loosely. Refactoring.Guru ("Two classes perform identical functions but have different method names") is the real backer.
3. consider, rule 7 (unchanged text). Counterpoint: "a design smell in Ousterhout's list".

Rule backers, confirmed: island.is ("Use the same name or term for the same concept"), tum-esi ("Each concept should be described by a single word"), Microsoft ("DO use the same name for the same concept"). 3 orgs.

## py-class-earns-its-instance — ISSUES

1. consider, check 1. The Why says Pylint "shows the fix as a dataclass plus a module function". The R0903 page shows three fixes: `dataclass_and_function.py`, `function.py`, and `larger_api.py`, which adds a method. Fix: "shows a dataclass plus a function, or a larger API, as fixes".
2. consider, check 3. R0903's own "Problematic code" is a class with state (`self.name`, `self.fruit_of_residence`), which this Rule passes. A static-only class with two methods passes R0903. The note already calls the gate "a prompt", which is accurate. Say in `tool_gate` that R0903 measures method count, not state.
3. consider, check 3 (rule 5). The PASS block is fenced as `python` but `dates.py:  def parse(s): ...` and `tax.py:    def total(order): ...` do not parse. Use a `text` fence.
4. consider, rule 7. Counterpoint: "The Go review guide takes the same stance".

The creator source satisfies the stable floor (ADR 0001). Refactoring.Guru ("if a class doesn't do enough to earn your attention, it should be deleted") and Pylint back the Rule. The Go wiki backs only the Protocol point in the Why.

## py-test-hygiene — ISSUES

1. act, rule 7. Counterpoint: "Laravel says most tests should be feature tests, and Google prefers real dependencies". Fix: "Many teams keep most tests at the feature level and prefer real dependencies ...".
2. consider, check 3. "Off ... the real filesystem" fails every test that uses pytest's `tmp_path`, which is the standard pytest fixture. Say whether a per-test temporary directory counts as the real filesystem.

Per clause, confirmed. Off network, disk and DB: Google ("small tests aren't allowed to access the network or disk"), Microsoft ("no dependencies on any outside factors, such as a file system or database"), Spring ("no runtime infrastructure"), Laravel (Unit tests "are unable to access your application's database"), Django ("SimpleTestCase disallows database queries by default"). Off the real clock: Microsoft (`DateTime.Now` seam), GitLab ("Unit and component tests use fake timers"), Rails (`travel_to`). Separate tier: Google (medium and large sizes), Rails ("bin/rails test will not run [system tests] ... add another CI step"), GitLab testing levels, Laravel. Each clause has at least 3.

## code-test-selection-on-pr — ISSUES

1. act, check 1. The note says "Meta, Microsoft and Shopify ... keep a full run before deploy or on a schedule". The Meta post says only that selection catches "more than 99.9 percent of all regressions ... while running just a third of all tests that transitively depend on modified code". It does not mention a full run. Fix: drop Meta from the full-run clause. That clause still has Microsoft ("TIA can be conditioned to run all tests at a configured periodicity. Setting this option is recommended"), Shopify ("we run the full test suite every deploy"), Gradle/Develocity ("Use this for post-merge or nightly builds") and Google ch23 (post-submit).
2. act, check 3. The Rule fails any repo that runs its whole suite on each pull request, including a 90-second suite. Google's own rule is presubmit "only fast, reliable ones", not a demand for selection. Fix: add a condition, "when the full suite exceeds the pull-request time budget", and mark small suites `N/A`.
3. consider, check 3 (rule 5). Both workflows lack `runs-on`, which GitHub Actions requires, and a `checkout` step, so they would not run as written. Add `runs-on: ubuntu-latest` and `- uses: actions/checkout@v4`.

## code-test-suite-time-budget — PASS

The draft status and the `lacks: orgs` line are correct. The fail-the-build clause has thoughtbot ("Allowlist entries have an expiration date. When they expire, the test starts failing the audit") and SciPy ("--fail-slow=5.0 is used in a 'full' test job"). Shopify's Test Budget stops test execution when time runs out ("the best time to stop executing tests and enforce it"), and the post is a feasibility study ("analyzed the feasibility"), so it does not back failing the build. GitLab's "Merge request pipeline duration ... target ... below 45 minutes" is a target, as the note says.

## fn-length-budget — ISSUES

1. consider, check 3/6. Google 3.18 says "no hard limit is placed on function length. If a function exceeds about 40 lines, think about whether it can be broken up". That argues directly against clause 1 ("Set a function-length limit in the linter"). The note records it, but the Counterpoint does not answer it. Fix: answer "a hard limit forces bad splits" in the Counterpoint, and say the limit is a prompt to inspect.
2. consider, check 3. The Counterpoint's exception ("Keep the function when each line is one step of the same job") is wider than the Rule's ("unless its body is one simple operation"), and it could cover the FAIL (checkout steps). Fix: use the Rule's wording, "one simple operation or one flat dispatch".

Defaults verified: ESLint 50, Pylint max-statements 50, Checkstyle 150, RuboCop 10, PMD NcssCount methodReportLevel 60 and CognitiveComplexity 15, CA1505 threshold 10. The kernel's "one long (but simple) case-statement ... it's OK to have a longer function" backs the exception. Clause 1 has ESLint, Pylint, Checkstyle, RuboCop, PMD and Microsoft (6); clause 2 has the kernel, Google and the linters.

## fn-no-caller-mutation — ISSUES

1. act, check 1/3. The Rust book page teaches mutating a caller's value through `&mut` (`fn change(some_string: &mut String)`, `change(&mut s)`), and the borrow checker accepts that. E0596 means "cannot borrow as mutable" for a binding that was not declared `mut`, not "do not mutate the caller's object". Rust backs "make mutation explicit", not this Rule. Fix: drop Rust from `borrowed_from` and `tool_gate`, or recast it as the Counterpoint's honest in-place API.
2. consider, check 1. Kotlin coding conventions say "Prefer using immutable data to mutable" in general and nothing about parameters. The Python FAQ and Google 2.12 back only the mutable-default case, which is shared function state, not a caller-owned object. They are fine in the Why but do not count for the Rule.

Rule backers, confirmed: Airbnb ("7.12 Never mutate parameters"), ESLint no-param-reassign ("Side effects on parameters can cause counter-intuitive execution flow"; `props` "is false by default", which matches the gate text), Meta/React ("treat any JavaScript object that you put into state as read-only"; state only). 3 orgs, with React the narrowest.

## fn-parameter-limit — ISSUES

1. consider, check 3. The Rule counts all parameters, but the Why argues from positional slots. In Python, keyword-only parameters (`def create_user(*, name, email, ...)`) fix the call-site problem, and Pylint has a separate R0917 for positional parameters. Say whether keyword-only parameters count.

Defaults verified: ESLint max-params 3 ("requires the memorization of what each parameter is, its type, and the order"), Pylint max-args 5 and max-positional-arguments 5, Checkstyle max 7 with `ignoreOverriddenMethods`, RuboCop Max 5, PMD ExcessiveParameterList minimum 10. 5 orgs.

## mod-class-size-budget — ISSUES

1. consider, check 3. The Rule ("keep classes within it") has no record exemption, but the Why and the Counterpoint exempt data records. Pylint R0902 fires on field count whatever the class is. Fix: put "A data record is exempt" in the Rule or `applies_when`.

Confirmed: Pylint R0902 ("try to reduce this to get a simpler ... class", max-attributes 7, max-public-methods 20), PMD (NcssCount classReportLevel 1500; GodClass "should be split apart"), RuboCop ClassLength Max 100, Microsoft CA1505. 4 orgs.

## mod-law-of-demeter — ISSUES

1. act, check 3/6. The Rule forbids any reach-through ("do not reach through one object to use another"), and the gate is PMD with `trustRadius` default 1 ("you're only allowed one getter call on untrusted values"). The Counterpoint says "flag a chain only when the caller depends on three or more layers". So the Rule, the gate and the Counterpoint set three different thresholds. Fix: put the threshold in the Rule, or drop the three-layer sentence.
2. consider, check 1. The note cites "Kaminski argues chaining is often fine (a person, counter-view)", but no Kaminski URL is in `borrowed_from`. Add the URL or drop the mention.

Confirmed: PMD ("fetching data from 'too far away'"), Google Testing Blog, Hevery 2008 ("Ask for things, Don't look for things (aka Dependency Injection / Law of Demeter)"), and JetBrains ("never call a method on an object received from another call ... you may need to write many wrapper methods"; `ignoreLibraryCalls` default Selected, which matches the card). 3 orgs.

## mod-no-repeated-switches — ISSUES

1. act, check 4. This card contradicts stable `fn-variants-as-tagged-union`. That card prescribes switching over a tagged union with an exhaustive `never` default in every switch. This Rule says to replace repeated switches with polymorphism, and its Why ("the missed one fails at run time") is false when the switch is exhaustive and the compiler finds every copy. Fix: exempt exhaustive switches over a closed type, or merge the two cards. Until then the `lacks:` reason should be `duplicate` (conflicts with a stable card), which comes before `orgs` in the table order.

Orgs: Refactoring.Guru ("When a new condition is added, you have to find all the switch code and modify it"; "When a switch operator performs simple actions, there's no reason to make code changes") and Google (Hevery: "If you see the same if condition repeated in many places in your class you should again think polymorphism"). That is 2, so the draft is correct.

## mod-no-shotgun-surgery — ISSUES

1. act, rule 7. Counterpoint: "Microsoft warns that duplication is preferable to coupling to the wrong abstraction". Fix: "Duplication beats coupling to the wrong abstraction".

Confirmed: Refactoring.Guru ("A single responsibility has been split up among a large number of classes"), Microsoft ("specifying behavior related to a particular concept in multiple places ... is a frequent source of errors"), NDepend ("Knowledge should only exist in a single place in your codebase"). 3 orgs. It does not duplicate `mod-cohesive-unit` (the inverse case) or `mod-derive-dont-duplicate`.

## mod-temporary-field — ISSUES

1. act, check 1. Refactoring.Guru's Temporary Field is a different smell from the Rule. Its fields are "created for use in an algorithm that requires a large amount of inputs" and are read across methods, and its treatment is "Extract Class" or "Introduce Null Object", not a local variable. The Rule (make the field a local) is JetBrains FieldCanBeLocal, Sonar S1450 and PMD SingularField. Fix: drop Refactoring.Guru from the Rule backing, or rename the card (for example `mod-field-can-be-local`).
2. act, check 3/6. The Why says "the next method that reads it sees a stale or empty value". Under the Rule's trigger, every read follows an assignment in the same method, so no method can see a stale value. The sentence describes Refactoring.Guru's smell, not this Rule. Fix: "A reader looks for state the object does not keep."
3. consider, check 3. The FAIL uses a public `self.subtotal`. JetBrains ("Reports private fields"), PMD ("We can only check private fields") and Sonar check private fields only, because a public field may be read by callers. Use `self._subtotal`.
4. consider, check 3. The PMD Counterpoint gets the false positive backwards. PMD says the rule "is not aware of threading, so it may cause false positives in concurrent code". The false positive is a field that another thread reads on purpose; turning it into a local would break that. "Suppress it there or use a local" gives contradictory advice. Fix: "suppress it where another thread reads the field".
5. consider, check 3. Pylint W0201 (attribute-defined-outside-init) is a different check. It is not a gate for this Rule.

Rule backers, confirmed: JetBrains ("If all local usages of a field are preceded by an assignment to that field, the field can be replaced with one or more local variables"), SonarSource S1450 ("always assigned to ... before being read ... should become a local variable"), PMD SingularField. 3 orgs.

## chg-no-per-user-ide-files — ISSUES

1. act, check 3. `git ls-files -ci --exclude-standard` lists tracked files that match an ignore pattern. The card's FAIL has "no entry for either path" in `.gitignore`, so this gate prints nothing and passes the FAIL. Fix: add a gate that matches a fixed path list (for example `git ls-files | rg '(^|/)(\.idea/workspace\.xml|xcuserdata/|\.DS_Store$|Thumbs\.db$)'`), or say the gate only catches files committed despite an ignore entry.
2. noted, check 1. `intellij-support.jetbrains.com/hc/en-us/articles/206544839` is UNFETCHED (403). The JetBrains help page covers the same point ("This folder contains both user-specific settings that should not be placed under version control and project settings that are normally shared"; workspace.xml goes to `.gitignore`).

Per clause, confirmed. Do not commit per-user state: Git ("specific to one user's workflow ... should go into ... $GIT_DIR/info/exclude"; editor files go in `core.excludesFile`), JetBrains, GitHub (`.vscode/*` ignored in the template), Microsoft (global `.gitignore`). Ignore in the repo or machine-wide: Git, GitHub (`~/.config/git/ignore`, `.git/info/exclude`), Microsoft. Keep shared settings: JetBrains, Microsoft/VS Code ("shared by all users of that project"), Apple Xcode Cloud ("Use shared schemes"), GitHub (`!.vscode/settings.json`). Each clause has at least 3, so the card can be stable once the gate is fixed.

## py-test-collection-and-imports — ISSUES

1. consider, check 1/2. The `lacks:` line counts "testpaths has pytest and Trail of Bits". The pytest reference only defines the option ("Sets list of directories that should be searched for tests ...") and recommends nothing, which rule 3 treats as a definition. Only Trail of Bits states the practice ("Optimizing test discovery with strategic testpaths configuration"; "collected in 7.84s" to "2.60s"). Fix: "testpaths has Trail of Bits; needs two more orgs".
2. noted, check 1. The Alan Medium post is UNFETCHED (403). The importtime clause has Trail of Bits ("profiling import times using Python's -X importtime option", ddtrace) and SkyPilot ("python -X importtime -c 'import sky'", LazyImport over 100 ms). That is 2 confirmed, or 3 if the Alan post says what the note claims.

The Why figure is correct: "this discovery process alone consumed over 6 seconds—10% of our total test execution time after parallelization."

## Summary

| id | verdict | confirmed orgs per clause | recommended status |
|---|---|---|---|
| fn-comments-explain-why | ISSUES | Rule 4 (Google, Mozilla, Apache, PSF) | stable |
| fn-known-keys-get-a-type | ISSUES | 2 independent (PSF/mypy same author, attrs) | draft |
| fn-no-stringly-typed-returns | ISSUES | strings 2 (Microsoft, Apple) + Kotlin feature page; boolean half duplicates stable card | draft |
| mod-behaviour-lives-with-state | ISSUES | 3 (Microsoft, PMD, NimblePros) | stable after rule-7 fix |
| mod-internals-unreachable | ISSUES | import 3 (Google, Microsoft, Cursor); member 3 (Refactoring.Guru, PSF, Pylint) | stable |
| mod-no-module-mutable-state | ISSUES | module 3 (Google, Uber, Microsoft); class field 1 (Google) | stable after narrowing the Rule back to module level |
| mod-one-name-per-concept | ISSUES | 3 (island.is, tum-esi, Microsoft) | stable |
| py-class-earns-its-instance | ISSUES | creator + 2 (Refactoring.Guru, Pylint) | stable |
| py-test-hygiene | ISSUES | I/O 5, clock 3, tier 4 | stable after rule-7 fix |
| code-test-selection-on-pr | ISSUES | select 6; full run 4 (Microsoft, Shopify, Gradle, Google; not Meta) | draft until the Rule has a threshold |
| code-test-suite-time-budget | PASS | fail gate 2 (thoughtbot, SciPy) | draft |
| fn-length-budget | ISSUES | limit 6 linters (Google dissents); split 3+ | stable |
| fn-no-caller-mutation | ISSUES | 3 (Airbnb, ESLint, Meta/React); Rust does not back it | stable after dropping Rust |
| fn-parameter-limit | ISSUES | 5 (ESLint, Pylint, Checkstyle, RuboCop, PMD) | stable |
| mod-class-size-budget | ISSUES | 4 (Pylint, PMD, RuboCop, Microsoft) | stable |
| mod-law-of-demeter | ISSUES | 3 (PMD, Google, JetBrains) | stable after the threshold fix |
| mod-no-repeated-switches | ISSUES | 2 (Refactoring.Guru, Google); conflicts with fn-variants-as-tagged-union | draft (`lacks: duplicate`) |
| mod-no-shotgun-surgery | ISSUES | 3 (Refactoring.Guru, Microsoft, NDepend) | stable after rule-7 fix |
| mod-temporary-field | ISSUES | 3 (JetBrains, SonarSource, PMD); Refactoring.Guru backs a different smell | draft until the Why and sources are fixed |
| chg-no-per-user-ide-files | ISSUES | 4 / 3 / 4 | draft until the gate is fixed, then stable |
| py-test-collection-and-imports | ISSUES | testpaths 1 (Trail of Bits); importtime 2 (+Alan UNFETCHED) | draft |

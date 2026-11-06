# Evidence, fix round C (other cards), 2026-11-06

Format: card-id | URL | org | "quote" | clause | result. Fetched with curl on 2026-11-06; text normalised (tags stripped, curly quotes folded).

fn-comments-explain-why | https://google.github.io/eng-practices/review/reviewer/looking-for.html | Google | "comments are useful when they explain why some code exists" | reason not restatement | CONFIRMED (HTTP 200)
fn-comments-explain-why | https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/JavaScript | Mozilla | "restating the code in prose is not a good use of comments" | reason not restatement | CONFIRMED (HTTP 200)
fn-comments-explain-why | https://flink.apache.org/how-to-contribute/code-style-and-quality-common/ | Apache Flink | "help explain the" | reason not restatement | CONFIRMED (HTTP 200)
fn-comments-explain-why | https://peps.python.org/pep-0008/ | PSF | "if they state the obvious" | reason not restatement | CONFIRMED (HTTP 200)
fn-known-keys-get-a-type | https://peps.python.org/pep-0589/ | PSF | "too lenient, as arbitrary string keys can be used" | record type | CONFIRMED (HTTP 200)
fn-known-keys-get-a-type | https://www.attrs.org/en/stable/why.html | attrs | "it is an object, not a hash" | record type | CONFIRMED (HTTP 200)
fn-no-stringly-typed-returns | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum | Microsoft | "to strongly type parameters, properties, and return values that represent sets of values" | closed type | CONFIRMED (HTTP 200)
fn-no-stringly-typed-returns | https://developer.apple.com/videos/play/wwdc2020/10680/ | Apple | "enum or a struct with a raw value" | closed type | CONFIRMED (HTTP 200)
mod-behaviour-lives-with-state | https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model | Microsoft | "take care of the invariants and rules of the entity" | behaviour on object | CONFIRMED (HTTP 200)
mod-behaviour-lives-with-state | https://docs.pmd-code.org/latest/pmd_rules_java_design.html | PMD | "poor data-behaviour proximity" | behaviour on object | CONFIRMED (HTTP 200)
mod-behaviour-lives-with-state | https://deviq.com/domain-driven-design/anemic-model/ | NimblePros | "manage their internal state and behavior" | behaviour on object | CONFIRMED (HTTP 200)
mod-internals-unreachable | https://pkg.go.dev/cmd/go | Google | "importable only by code that shares the same import path above the internal directory" | import | CONFIRMED (HTTP 200)
mod-internals-unreachable | https://raw.githubusercontent.com/cursor/plugins/main/pstack/skills/architect/references/design-red-flags.md | Cursor | "unreachable from outside the module" | import | CONFIRMED (HTTP 200)
mod-internals-unreachable | https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/keywords/internal | Microsoft | "only within files in the same assembly" | import (definition) | CONFIRMED (HTTP 200)
mod-internals-unreachable | https://refactoring.guru/smells/inappropriate-intimacy | Refactoring.Guru | "uses the internal fields and methods of another class" | member | CONFIRMED (HTTP 200)
mod-internals-unreachable | https://peps.python.org/pep-0008/ | PSF | "not intended to be used by third parties" | member | CONFIRMED (HTTP 200)
mod-internals-unreachable | https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/protected-access.html | Pylint | "accessed outside the class" | member | CONFIRMED (HTTP 200)
mod-no-module-mutable-state | https://google.github.io/styleguide/pyguide.html | Google | "Module-level values or class attributes that can get mutated" | module | CONFIRMED (HTTP 200)
mod-no-module-mutable-state | https://github.com/uber-go/guide/raw/master/style.md | Uber | "Avoid mutating global variables" | module | CONFIRMED (HTTP 200)
mod-no-module-mutable-state | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2211 | Microsoft | "not constant nor is it read-only" | module | CONFIRMED (HTTP 200)
mod-one-name-per-concept | https://raw.githubusercontent.com/island-is/handbook/master/docs/api-design-guide/naming-conventions.md | Island.is | "same name or term for the same concept" | one name | CONFIRMED (HTTP 200)
mod-one-name-per-concept | https://github.com/tum-esi/common-coding-conventions | TUM ESI | "Pick one word for one concept." (section heading) | one name | CONFIRMED
mod-one-name-per-concept | https://raw.githubusercontent.com/microsoft/api-guidelines/vNext/azure/ConsiderationsForServiceDesign.md | Microsoft | "consistently" | one name | CONFIRMED (HTTP 200)
mod-one-name-per-concept | https://refactoring.guru/smells/alternative-classes-with-different-interfaces | Refactoring.Guru | "Two classes perform identical functions but have different method names" | two-class (Why) | CONFIRMED (HTTP 200)
py-class-earns-its-instance | https://refactoring.guru/smells/lazy-class | Refactoring.Guru | "doesn't do enough to earn your attention" | class | CONFIRMED on re-check (curly apostrophe in the page)
py-class-earns-its-instance | https://pylint.readthedocs.io/en/latest/user_guide/messages/refactor/too-few-public-methods.html | Pylint | "worth it" | class | CONFIRMED (HTTP 200)
py-class-earns-its-instance | https://go.dev/wiki/CodeReviewComments | Google | "for mocking" | Protocol | CONFIRMED (HTTP 200)
py-test-hygiene | https://abseil.io/resources/swe-book/html/ch11.html | Google | "aren't allowed to access the network or disk" | I/O | CONFIRMED on re-check (curly apostrophe in the page)
py-test-hygiene | https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices | Microsoft | "such as a file system or database" | I/O | CONFIRMED (HTTP 200)
py-test-hygiene | https://docs.spring.io/spring-framework/reference/testing/unit.html | Spring | "without needing to access persistent data" | I/O | CONFIRMED (HTTP 200)
py-test-hygiene | https://docs.djangoproject.com/en/5.1/topics/testing/tools/ | Django | "disallows database queries" | I/O | CONFIRMED (HTTP 200)
py-test-hygiene | https://laravel.com/docs/12.x/testing | Laravel | "unable to access your application" | I/O | CONFIRMED (HTTP 200)
py-test-hygiene | https://docs.gitlab.com/development/testing_guide/testing_levels/ | GitLab | "fake timers" | clock | CONFIRMED (HTTP 200)
py-test-hygiene | https://guides.rubyonrails.org/testing.html | Rails | "travel_to" | clock | CONFIRMED (HTTP 200)
py-test-hygiene | https://guides.rubyonrails.org/testing.html | Rails | "add another CI step" | separate tier | CONFIRMED (HTTP 200)
code-test-selection-on-pr | https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/ | Meta | "more than 99.9 percent of all regressions" | select | CONFIRMED (HTTP 200)
code-test-selection-on-pr | https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops | Microsoft | "run all tests at a configured periodicity" | full run | CONFIRMED (HTTP 200)
code-test-selection-on-pr | https://shopify.engineering/spark-joy-by-running-fewer-tests | Shopify | "run the full test suite every deploy" | full run | CONFIRMED (HTTP 200)
code-test-selection-on-pr | https://nx.dev/ci/features/affected | Nx | "affected" | select | CONFIRMED (HTTP 200)
code-test-selection-on-pr | https://docs.develocity.ai/current/using-develocity/predictive-test-selection/ | Gradle | "post-merge or nightly" | full run | CONFIRMED (HTTP 200)
fn-length-budget | https://eslint.org/docs/latest/rules/max-lines-per-function | ESLint | "max-lines-per-function" | limit | CONFIRMED (HTTP 200)
fn-length-budget | https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-statements.html | Pylint | "split it in smaller functions" | split | CONFIRMED (HTTP 200)
fn-length-budget | https://docs.rubocop.org/rubocop/latest/cops_metrics.html | RuboCop | "MethodLength" | limit | CONFIRMED (HTTP 200)
fn-length-budget | https://google.github.io/styleguide/pyguide.html | Google | "If a function exceeds about 40 lines" | split | CONFIRMED (HTTP 200)
fn-length-budget | https://www.kernel.org/doc/html/latest/process/coding-style.html | Linux kernel | "it's OK to have a longer function" | exception | CONFIRMED on re-check (curly apostrophe in the page)
fn-length-budget | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1505 | Microsoft | "split it into smaller and more focused" | split | CONFIRMED (HTTP 200)
fn-no-caller-mutation | https://airbnb.io/javascript/ | Airbnb | "Never mutate parameters" | rule | CONFIRMED (HTTP 200)
fn-no-caller-mutation | https://eslint.org/docs/latest/rules/no-param-reassign | ESLint | "Side effects on parameters can cause counter-intuitive" | rule | CONFIRMED (HTTP 200)
fn-no-caller-mutation | https://react.dev/learn/updating-objects-in-state | Meta | "treat any JavaScript object that you put into state as read-only" | rule | CONFIRMED (HTTP 200)
fn-parameter-limit | https://eslint.org/docs/latest/rules/max-params | ESLint | "memorization of what each parameter is" | limit | CONFIRMED (HTTP 200)
fn-parameter-limit | https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-arguments.html | Pylint | "too many arguments" | limit | CONFIRMED (HTTP 200)
fn-parameter-limit | https://pmd.github.io/pmd/pmd_rules_java_design.html | PMD | "ExcessiveParameterList" | limit | CONFIRMED (HTTP 200)
mod-class-size-budget | https://pylint.readthedocs.io/en/stable/user_guide/messages/refactor/too-many-instance-attributes.html | Pylint | "too many instance attributes" | limit | CONFIRMED (HTTP 200)
mod-class-size-budget | https://pmd.github.io/pmd/pmd_rules_java_design.html | PMD | "should be split apart" | split | CONFIRMED (HTTP 200)
mod-class-size-budget | https://docs.rubocop.org/rubocop/latest/cops_metrics.html | RuboCop | "ClassLength" | limit | CONFIRMED (HTTP 200)
mod-law-of-demeter | https://pmd.github.io/pmd/pmd_rules_java_design.html | PMD | "too far away" | rule | CONFIRMED (HTTP 200)
mod-law-of-demeter | https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html | Google | "Law of Demeter" | rule | CONFIRMED (HTTP 200)
mod-law-of-demeter | https://www.jetbrains.com/help/inspectopedia/LawOfDemeter.html | JetBrains | "method on an object received from another call" | rule | CONFIRMED (HTTP 200)
mod-no-repeated-switches | https://refactoring.guru/smells/switch-statements | Refactoring.Guru | "you have to find all the switch code and modify it" | rule | CONFIRMED (HTTP 200)
mod-no-shotgun-surgery | https://refactoring.guru/smells/shotgun-surgery | Refactoring.Guru | "split up among a large number of classes" | rule | CONFIRMED (HTTP 200)
mod-no-shotgun-surgery | https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles | Microsoft | "frequent source of errors" | rule | CONFIRMED (HTTP 200)
mod-no-shotgun-surgery | https://blog.ndepend.com/shotgun-surgery | NDepend | "only exist in a single place" | rule | CONFIRMED (HTTP 200)
mod-temporary-field | https://www.jetbrains.com/help/inspectopedia/FieldCanBeLocal.html | JetBrains | "preceded by an assignment to that field" | trigger | CONFIRMED (HTTP 200)
mod-temporary-field | https://raw.githubusercontent.com/SonarSource/sonar-dotnet/master/analyzers/rspec/cs/S1450.html | SonarSource | "local variable" | trigger | CONFIRMED (HTTP 200)
mod-temporary-field | https://docs.pmd-code.org/latest/pmd_rules_java_design.html | PMD | "SingularField" | trigger | CONFIRMED (HTTP 200)
chg-no-per-user-ide-files | https://git-scm.com/docs/gitignore | Git | "specific to one user" | per-user | CONFIRMED (HTTP 200)
chg-no-per-user-ide-files | https://docs.github.com/en/get-started/git-basics/ignoring-files | GitHub | "text editor creates" | per-user | CONFIRMED (HTTP 200)
chg-no-per-user-ide-files | https://raw.githubusercontent.com/github/gitignore/main/Global/VisualStudioCode.gitignore | GitHub | "!.vscode/settings.json" | shared | CONFIRMED (HTTP 200)
chg-no-per-user-ide-files | https://www.jetbrains.com/help/idea/configure-project-settings.html | JetBrains | "user-specific settings" | per-user | CONFIRMED (HTTP 200)
chg-no-per-user-ide-files | https://learn.microsoft.com/en-us/azure/devops/repos/git/ignore-files | Microsoft | "global" | per-user | CONFIRMED (HTTP 200)
py-test-collection-and-imports | https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/ | Trail of Bits | "testpaths" | testpaths | CONFIRMED (HTTP 200)
py-test-collection-and-imports | https://docs.pytest.org/en/stable/reference/reference.html | pytest | "speed up test collection" | testpaths (definition) | CONFIRMED (HTTP 200)
mod-one-name-per-concept | https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md | Microsoft | "DO use the same name for the same concept and different names for different concepts wherever possible." | one name | CONFIRMED (raw file, line 104; the earlier "consistently" row is the weaker sentence)
chg-no-per-user-ide-files | https://code.visualstudio.com/docs/configure/settings | Microsoft | "the settings for the project will be shared by all users of that project" | shared settings | CONFIRMED in microsoft/vscode-docs docs/configure/settings.md (the rendered page is script-only)
chg-no-per-user-ide-files | https://developer.apple.com/documentation/xcode/setting-up-your-project-to-use-xcode-cloud | Apple | "Use shared schemes." | shared settings | CONFIRMED in the page's JSON feed
chg-no-per-user-ide-files | https://learn.microsoft.com/en-us/azure/devops/repos/git/ignore-files | Microsoft | "You can designate a .gitignore file as a global ignore file that applies to all local Git repos" | machine-wide exclude | CONFIRMED
chg-no-per-user-ide-files | https://git-scm.com/docs/gitignore | Git | "auxiliary files that live inside the repository but are specific to one user's workflow" | per-user state, machine-wide exclude | CONFIRMED
chg-no-per-user-ide-files | https://www.jetbrains.com/help/idea/configure-project-settings.html | JetBrains | "user-specific settings that should not be placed under version control" | per-user state | CONFIRMED

## Org counts per Rule clause (final)

- fn-comments-explain-why: reason not restatement 4 (Google, Mozilla, Apache Flink, PSF)
- fn-known-keys-get-a-type: record type 2 independent (PSF, attrs); mypy shares PEP 589's author -> draft
- fn-no-stringly-typed-returns: closed type for a string return 2 (Microsoft, Apple) -> draft
- mod-behaviour-lives-with-state: 3 (Microsoft, PMD, NimblePros)
- mod-internals-unreachable: import 3 (Google, Cursor, Microsoft by definition); member 3 (Refactoring.Guru, PSF, Pylint)
- mod-no-module-mutable-state: module level 3 (Google, Uber, Microsoft)
- mod-one-name-per-concept: 3 (Ísland.is, TUM ESI, Microsoft)
- py-class-earns-its-instance: creator exception (ADR 0001) + Refactoring.Guru + Pylint; Protocol clause: creator + Google Go wiki
- py-test-hygiene: I/O 5, clock 3, separate tier 4 (creator source also)
- code-test-selection-on-pr: select 5 (Meta, Microsoft, Shopify, Nx, Gradle); full run 3 (Microsoft, Shopify, Gradle)
- code-test-suite-time-budget: unchanged, draft (fail gate 2: thoughtbot, SciPy)
- fn-length-budget: split 4 (Google, Linux kernel, Pylint, Microsoft)
- fn-no-caller-mutation: 3 (Airbnb, ESLint, Meta); Airbnb's rule is the ESLint rule, so independence is thin
- fn-parameter-limit: 5 (ESLint, Pylint, Checkstyle, RuboCop, PMD); Checkstyle page 403, default read from source by the judge
- mod-class-size-budget: enforcement 3 (Pylint, PMD, RuboCop); CA1505 dropped
- mod-law-of-demeter: 3 (PMD, JetBrains, Google heading only)
- mod-no-repeated-switches: 2 (Refactoring.Guru, Google) -> draft
- mod-no-shotgun-surgery: 3 (Refactoring.Guru, Microsoft, NDepend)
- mod-temporary-field: trigger 3 (JetBrains, SonarSource, PMD); draft
- chg-no-per-user-ide-files: per-user state 3 (JetBrains, Git, GitHub); ignore location 3 (Git, GitHub, Microsoft); shared settings 4 (JetBrains, Microsoft, Apple, GitHub); draft
- py-test-collection-and-imports: testpaths 1 recommending (Trail of Bits) -> draft

# Evidence V — promotions, test practices, IDE files

Fetched 2026-11-06 with a plain HTTP client and, for the Apple pages, Apple's documentation JSON. Every quote below was read on the page in this pass. Lines are `card-id | URL | org | "verbatim quote" | clause it backs`.

## mod-no-shotgun-surgery (promoted)

- mod-no-shotgun-surgery | https://refactoring.guru/smells/shotgun-surgery | Refactoring.Guru | "A single responsibility has been split up among a large number of classes." | one decision in one module (Why)
- mod-no-shotgun-surgery | https://refactoring.guru/smells/shotgun-surgery | Refactoring.Guru | "Making any modifications requires that you make many small changes to many different classes." | one change edits many classes (Why)
- mod-no-shotgun-surgery | https://refactoring.guru/smells/shotgun-surgery | Refactoring.Guru | "Use Move Method and Move Field to move existing class behaviors into a single class." | move the scattered parts together
- mod-no-shotgun-surgery | https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles | Microsoft | "The application should avoid specifying behavior related to a particular concept in multiple places as this practice is a frequent source of errors." | one decision in one module
- mod-no-shotgun-surgery | https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles | Microsoft | "Make this construct the single authority over this behavior" | move the scattered parts together
- mod-no-shotgun-surgery | https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/architectural-principles | Microsoft | "Duplication is always preferable to coupling to the wrong abstraction." | Counterpoint (wrong abstraction)
- mod-no-shotgun-surgery | https://blog.ndepend.com/shotgun-surgery | NDepend | "Shotgun surgery happens when you have to make many changes in your codebase to achieve seemingly simple tasks." | the smell
- mod-no-shotgun-surgery | https://blog.ndepend.com/shotgun-surgery | NDepend | "Knowledge should only exist in a single place in your codebase." | one decision in one module
- mod-no-shotgun-surgery | https://blog.ndepend.com/shotgun-surgery | NDepend | "When you find yourself changing the same four files or classes for each simple change, such as the addition of a menu item, reconsider your design." | one change edits many classes

## mod-no-repeated-switches (stays draft)

- mod-no-repeated-switches | https://refactoring.guru/smells/switch-statements | Refactoring.Guru | "Often code for a single switch can be scattered in different places in the program." | the repeated switch
- mod-no-repeated-switches | https://refactoring.guru/smells/switch-statements | Refactoring.Guru | "When a new condition is added, you have to find all the switch code and modify it." | Why
- mod-no-repeated-switches | https://refactoring.guru/smells/switch-statements | Refactoring.Guru | "As a rule of thumb, when you see switch you should think of polymorphism." | replace with polymorphism
- mod-no-repeated-switches | https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html | Google | "Favor polymorphism over conditionals : If you see a switch statement you should think polymorphisms. If you see the same if condition repeated in many places in your class you should again think polymorphism." | repeated condition, replace with polymorphism
- mod-no-repeated-switches | https://testing.googleblog.com/2008/08/by-miko-hevery-so-you-decided-to.html | Google | "Polymorphism will break your complex class into several smaller simpler classes which clearly define which pieces of the code are related and execute together." | Why
- mod-no-repeated-switches | https://shopify.engineering/other-driven-developments | Shopify | (no quote) | dropped: the page never mentions switches, conditionals in a type hierarchy, or polymorphism; it does not back the Rule

## mod-behaviour-lives-with-state (promoted)

- mod-behaviour-lives-with-state | https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model | Microsoft | "A domain entity in DDD must implement the domain logic or behavior related to the entity data" | put the rule on the object
- mod-behaviour-lives-with-state | https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model | Microsoft | "The entity's methods take care of the invariants and rules of the entity instead of having those rules spread across the application layer." | Why
- mod-behaviour-lives-with-state | https://learn.microsoft.com/en-us/dotnet/architecture/microservices/microservice-ddd-cqrs-patterns/microservice-domain-model | Microsoft | "if your microservice or Bounded Context is very simple (a CRUD service), the anemic domain model in the form of entity objects with just data properties might be good enough" | Counterpoint (CRUD exception)
- mod-behaviour-lives-with-state | https://docs.pmd-code.org/latest/pmd_rules_java_design.html | PMD | "The lack of functionality may indicate that their behaviour is defined elsewhere, which is a sign of poor data-behaviour proximity." | put the rule on the object
- mod-behaviour-lives-with-state | https://docs.pmd-code.org/latest/pmd_rules_java_design.html | PMD | "Refactoring a Data Class should focus on restoring a good data-behaviour proximity. In most cases, that means moving the operations defined on the data back into the class." | the fix
- mod-behaviour-lives-with-state | https://deviq.com/domain-driven-design/anemic-model/ | DevIQ (NimblePros) | "objects are said to be anemic if they have state but lack behavior" | Why
- mod-behaviour-lives-with-state | https://deviq.com/domain-driven-design/anemic-model/ | DevIQ (NimblePros) | "the objects that model the behavior of the problem space within the application should use encapsulation to manage their internal state and behavior" | put the rule on the object
- mod-behaviour-lives-with-state | https://deviq.com/domain-driven-design/anemic-model/ | DevIQ (NimblePros) | "if you are taking a functional programming approach with Domain-Driven Design, anemic models are expected, as functional programming takes an approach with immutable data structures and behaviors implemented as functions that operate on those immutable records" | Counterpoint (functional exception)

## code-test-suite-time-budget (stays draft)

- code-test-suite-time-budget | https://thoughtbot.com/blog/introducing-test-budget | thoughtbot | "The total suite budget is set 10% above your current total" | written budget for the suite
- code-test-suite-time-budget | https://thoughtbot.com/blog/introducing-test-budget | thoughtbot | "The per-test-type budgets are based on the 99th percentile." | written budget for the slow tests
- code-test-suite-time-budget | https://thoughtbot.com/blog/introducing-test-budget | thoughtbot | "1) spec/system/signup_spec.rb -- creates account (11.20s) exceeds system limit (6.00s)" | fail a test over its budget
- code-test-suite-time-budget | https://thoughtbot.com/blog/introducing-test-budget | thoughtbot | "When they expire, the test starts failing the audit again." | fail the build
- code-test-suite-time-budget | https://shopify.engineering/test-budget-time-constrained-ci-feedback | Shopify | "The time budget is an upper bound. The CI system executes the tests up to that time bound." | written budget for the whole run
- code-test-suite-time-budget | https://scipy.github.io/devdocs/dev/contributor/continuous_integration.html | SciPy project | "Some CI jobs install pytest-fail-slow and report failures when the test execution time exceeds a threshold duration." | fail a test over its budget
- code-test-suite-time-budget | https://scipy.github.io/devdocs/dev/contributor/continuous_integration.html | SciPy project | "By default, all tests are subject to a 5 second limit" | per-test budget
- code-test-suite-time-budget | https://about.gitlab.com/blog/gitlab-top-devops-tooling-metrics-and-targets/ | GitLab | "When a pipeline is started for a merge request, how long does it take to run?" | whole-run budget
- code-test-suite-time-budget | https://about.gitlab.com/blog/gitlab-top-devops-tooling-metrics-and-targets/ | GitLab | "Our target for this metric is below 45 minutes." | whole-run budget; does not fail the build
- code-test-suite-time-budget | https://firefox-source-docs.mozilla.org/testing/xpcshell/index.html | Mozilla | (no quote) | dropped: the page documents a timeout factor and does not say to profile a slow test or set a time budget

## py-test-collection-and-imports (stays draft)

- py-test-collection-and-imports | https://docs.pytest.org/en/stable/reference/reference.html | pytest project | "Useful when all project tests are in a known location to speed up test collection and to avoid picking up undesired tests by accident." | set testpaths
- py-test-collection-and-imports | https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/ | Trail of Bits | "# 3,900+ tests collected in 7.84s" | set testpaths
- py-test-collection-and-imports | https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/ | Trail of Bits | "# 3,900+ tests collected in 2.60s" | set testpaths
- py-test-collection-and-imports | https://blog.trailofbits.com/2025/05/01/making-pypis-test-suite-81-faster/ | Trail of Bits | "we turned to profiling import times using Python’s -X importtime option" | measure imports
- py-test-collection-and-imports | https://medium.com/alan/how-we-improved-our-python-backend-start-up-time-2c33cd4873c8 | Alan | "30% reduction of the start-up time of the application, from 9 seconds to 6 seconds" | measure imports
- py-test-collection-and-imports | https://medium.com/alan/how-we-improved-our-python-backend-start-up-time-2c33cd4873c8 | Alan | "python -X importtime" | measure imports
- py-test-collection-and-imports | https://docs.skypilot.ai/en/v0.10.0/developers/CONTRIBUTING.html | SkyPilot project | "To measure import time: Basic check: python -X importtime -c \"import sky\"" | measure imports
- py-test-collection-and-imports | https://docs.skypilot.ai/en/v0.10.0/developers/CONTRIBUTING.html | SkyPilot project | "The module has a significant import time (e.g. > 100ms)" | measure imports

## fn-no-stringly-typed-returns (promoted, Rule widened to "named closed type")

- fn-no-stringly-typed-returns | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum | Microsoft | "DO use an enum to strongly type parameters, properties, and return values that represent sets of values." | named closed type for a set
- fn-no-stringly-typed-returns | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum | Microsoft | "DO favor using an enum instead of static constants." | instead of a bare value
- fn-no-stringly-typed-returns | https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/enum | Microsoft | "DO NOT use an enum for open sets" | Counterpoint (open sets)
- fn-no-stringly-typed-returns | https://developer.apple.com/videos/play/wwdc2020/10680/ | Apple | "what Swift sees is this function takes a string" | the stringly-typed problem
- fn-no-stringly-typed-returns | https://developer.apple.com/videos/play/wwdc2020/10680/ | Apple | "You'd just turn these constants into an enum or a struct with a raw value of type String, and then change the function to take only that type." | the fix
- fn-no-stringly-typed-returns | https://rust-lang.github.io/api-guidelines/type-safety.html | Rust project | "Use a deliberate type (whether enum, struct, or tuple) to convey interpretation and invariants." | named closed type
- fn-no-stringly-typed-returns | https://rust-lang.github.io/api-guidelines/type-safety.html | Rust project | "Core types like bool , u8 and Option have many possible interpretations." | instead of a bare primitive
- fn-no-stringly-typed-returns | https://kotlinlang.org/docs/sealed-classes.html | JetBrains | "with a sealed hierarchy of error classes, library authors can be sure that they know all the possible error types and that other error types can't appear later" | named closed type
- fn-no-stringly-typed-returns | https://kotlinlang.org/docs/sealed-classes.html | JetBrains | "The when expression, used with a sealed class, allows the Kotlin compiler to check exhaustively that all possible cases are covered." | Why (exhaustive check)

## fn-known-keys-get-a-type (promoted)

- fn-known-keys-get-a-type | https://mypy.readthedocs.io/en/stable/typed_dict.html | mypy project | "TypedDict lets you give precise types for dictionaries that represent objects with a fixed schema" | fixed keys get a record type
- fn-known-keys-get-a-type | https://mypy.readthedocs.io/en/stable/typed_dict.html | mypy project | "This is clearly not a good fit for movie above." | generic map for open keys only
- fn-known-keys-get-a-type | https://mypy.readthedocs.io/en/stable/typed_dict.html | mypy project | "Mypy will detect an invalid key as an error" | Why
- fn-known-keys-get-a-type | https://peps.python.org/pep-0589/ | Python Software Foundation | "The PEP 484 type Dict[str, Any] would be suitable, but it is too lenient, as arbitrary string keys can be used, and arbitrary values are valid." | generic map is too loose
- fn-known-keys-get-a-type | https://peps.python.org/pep-0589/ | Python Software Foundation | "a dictionary object has a specific set of string keys, each with a value of a specific type" | fixed keys get a record type
- fn-known-keys-get-a-type | https://www.attrs.org/en/stable/why.html | attrs project | "Dictionaries are not for fixed fields." | fixed keys get a record type
- fn-known-keys-get-a-type | https://www.attrs.org/en/stable/why.html | attrs project | "if your dict has a fixed and known set of keys, it is an object, not a hash" | fixed keys get a record type
- fn-known-keys-get-a-type | https://www.attrs.org/en/stable/why.html | attrs project | "You should be able to add and remove values." | generic map for open keys only

## mod-temporary-field (new)

- mod-temporary-field | https://refactoring.guru/smells/temporary-field | Refactoring.Guru | "Temporary fields get their values (and thus are needed by objects) only under certain circumstances. Outside of these circumstances, they’re empty." | the smell
- mod-temporary-field | https://refactoring.guru/smells/temporary-field | Refactoring.Guru | "This kind of code is tough to understand. You expect to see data in object fields but for some reason they’re almost always empty." | Why
- mod-temporary-field | https://www.jetbrains.com/help/inspectopedia/FieldCanBeLocal.html | JetBrains | "Reports private fields that are redundant and can be replaced with a local variable. If all local usages of a field are preceded by an assignment to that field, the field can be replaced with one or more local variables." | make it a local when every read follows an assignment
- mod-temporary-field | https://raw.githubusercontent.com/SonarSource/sonar-dotnet/master/analyzers/rspec/cs/S1450.html | SonarSource | "When the value of a private field is always assigned to in a class' methods before being read, then it is not being used to store class information. Therefore, it should become a local variable in the relevant methods to prevent any misunderstanding." | make it a local
- mod-temporary-field | https://docs.pmd-code.org/latest/pmd_rules_java_design.html | PMD | "Reports fields which may be converted to a local variable. This is so because in every method where the field is used, it is assigned before it is first read." | make it a local
- mod-temporary-field | https://docs.pmd-code.org/latest/pmd_rules_java_design.html | PMD | "The rule is not aware of threading, so it may cause false positives in concurrent code." | Counterpoint (threading)
- mod-temporary-field | https://pylint.readthedocs.io/en/latest/user_guide/messages/warning/attribute-defined-outside-init.html | Pylint | "Used when an instance attribute is defined outside the __init__ method." | tool gate for a field first assigned outside the constructor

## py-test-hygiene (merged N1; promoted content)

- py-test-hygiene | https://abseil.io/resources/swe-book/html/ch11.html | Google | "This means that small tests aren’t allowed to access the network or disk." | unit tests stay off external I/O
- py-test-hygiene | https://abseil.io/resources/swe-book/html/ch11.html | Google | "Testing code that relies on these sorts of operations requires the use of test doubles" | replace with a double
- py-test-hygiene | https://abseil.io/resources/swe-book/html/ch11.html | Google | "Teams at Google will frequently isolate their large tests from their small or medium tests, running them only during the build and release process so as not to impact developer workflow." | separate slower tier
- py-test-hygiene | https://abseil.io/resources/swe-book/html/ch11.html | Google | "at Google, we prefer to keep the real dependencies in place when it is feasible to do so" | Counterpoint (do not double everything)
- py-test-hygiene | https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices | Microsoft | "Unit tests are standalone, can run in isolation, and have no dependencies on any outside factors, such as a file system or database." | unit tests stay off external I/O
- py-test-hygiene | https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices | Microsoft | "The dependencies make the tests slow and brittle and should be reserved for integration tests." | separate slower tier
- py-test-hygiene | https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices | Microsoft | "You can also keep your unit tests in a separate project from your integration tests." | separate slower tier
- py-test-hygiene | https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices | Microsoft | "One principle of a unit test is that it must have full control of the system under test. However, this principle can be problematic when production code includes calls to static references (for example, DateTime.Now)." | unit tests stay off the real clock
- py-test-hygiene | https://docs.spring.io/spring-framework/reference/testing/unit.html | Spring | "you can test service layer objects by stubbing or mocking DAO or repository interfaces, without needing to access persistent data while running unit tests" | unit tests stay off the database
- py-test-hygiene | https://docs.spring.io/spring-framework/reference/testing/unit.html | Spring | "True unit tests typically run extremely quickly, as there is no runtime infrastructure to set up." | Why
- py-test-hygiene | https://docs.gitlab.com/development/testing_guide/testing_levels/ | GitLab | "All server requests : When running frontend unit tests, the backend may not be reachable, so all outgoing requests need to be mocked." | unit tests stay off the network
- py-test-hygiene | https://docs.gitlab.com/development/testing_guide/testing_levels/ | GitLab | "Unit and component tests use fake timers, so the test can advance time instead of waiting." | unit tests stay off the real clock
- py-test-hygiene | https://docs.gitlab.com/development/testing_guide/testing_levels/ | GitLab | "Most of our tests should be at the unit level, with fewer tests as we move up each layer." | separate slower tier
- py-test-hygiene | https://docs.djangoproject.com/en/5.1/topics/testing/tools/ | Django Software Foundation | "SimpleTestCase disallows database queries by default." | unit tests stay off the database
- py-test-hygiene | https://guides.rubyonrails.org/testing.html | Ruby on Rails | "Inside the travel_to block Date.current is stubbed" | unit tests stay off the real clock
- py-test-hygiene | https://guides.rubyonrails.org/testing.html | Ruby on Rails | "If you are using System Tests, bin/rails test will not run them, since they can be slow. To also run them, add another CI step that runs bin/rails test:system" | separate slower tier
- py-test-hygiene | https://laravel.com/docs/12.x/testing | Laravel | "Tests within your \"Unit\" test directory do not boot your Laravel application and therefore are unable to access your application's database or other framework services." | unit tests stay off the database
- py-test-hygiene | https://laravel.com/docs/12.x/testing | Laravel | "Generally, most of your tests should be feature tests." | Counterpoint (tier balance)

## code-test-selection-on-pr (new)

- code-test-selection-on-pr | https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/ | Meta | "This method needs to run only a small subset of tests in order to reliably detect faulty changes." | affected tests on the PR
- code-test-selection-on-pr | https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/ | Meta | "catch more than 99.9 percent of all regressions before they are visible to other engineers in the trunk code, while running just a third of all tests that transitively depend on modified code" | Why
- code-test-selection-on-pr | https://engineering.fb.com/2018/11/21/developer-tools/predictive-test-selection/ | Meta | "Every code change undergoes exhaustive testing before it is deployed from the trunk to production" | full suite before deploy
- code-test-selection-on-pr | https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops | Microsoft | "It automatically selects only the subset of tests required to validate the code being committed." | affected tests on the PR
- code-test-selection-on-pr | https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops | Microsoft | "For commits and scenarios that TIA can't understand, it falls back to running all tests." | Counterpoint (fallback)
- code-test-selection-on-pr | https://learn.microsoft.com/en-us/azure/devops/pipelines/test/test-impact-analysis?view=azure-devops | Microsoft | "You can run all tests at a configured periodicity." | full suite on a schedule
- code-test-selection-on-pr | https://shopify.engineering/spark-joy-by-running-fewer-tests | Shopify | "it became apparent that the right solution was to only run the tests related to the code change" | affected tests on the PR
- code-test-selection-on-pr | https://shopify.engineering/spark-joy-by-running-fewer-tests | Shopify | "we run the full test suite every deploy" | full suite outside the PR gate
- code-test-selection-on-pr | https://shopify.engineering/spark-joy-by-running-fewer-tests | Shopify | "Pull requests can get merged before the full test suite completes." | full suite is not before merge
- code-test-selection-on-pr | https://shopify.engineering/spark-joy-by-running-fewer-tests | Shopify | "the percentage of pull requests with failing tests being merged to the main branch is about 0.06%" | Counterpoint (missed regressions)
- code-test-selection-on-pr | https://abseil.io/resources/swe-book/html/ch23.html | Google | "we typically limit presubmit tests to just those for the project where the change is happening" | subset on presubmit
- code-test-selection-on-pr | https://abseil.io/resources/swe-book/html/ch23.html | Google | "After a change has been submitted, we use TAP to asynchronously run all potentially affected tests, including larger and slower tests." | tests outside the PR gate
- code-test-selection-on-pr | https://nx.dev/ci/features/affected | Nx | "Most pull requests change a few files, so CI should only run the tasks those files affect." | affected tests on the PR
- code-test-selection-on-pr | https://docs.develocity.ai/current/using-develocity/predictive-test-selection/ | Gradle | "Relevant tests mode selects the most relevant subset for the current changeset. Use this for pre-merge CI jobs and local pre-commit checks to get fast feedback." | affected tests on the PR
- code-test-selection-on-pr | https://docs.develocity.ai/current/using-develocity/predictive-test-selection/ | Gradle | "Remaining tests mode selects the tests that were not run in a prior relevant-tests execution against the same changeset. Use this for post-merge or nightly builds to ensure complete coverage." | full suite outside the PR gate

## chg-no-per-user-ide-files (new)

- chg-no-per-user-ide-files | https://docs.github.com/en/get-started/git-basics/ignoring-files | GitHub | "You can create a .gitignore file in your repository's root directory to tell Git which files and directories to ignore when you make a commit." | list the paths in the repository
- chg-no-per-user-ide-files | https://docs.github.com/en/get-started/git-basics/ignoring-files | GitHub | "To share the ignore rules with other users who clone the repository, commit the .gitignore file into your repository." | list the paths in the repository
- chg-no-per-user-ide-files | https://docs.github.com/en/get-started/git-basics/ignoring-files | GitHub | "You can use this technique for locally-generated files that you don't expect other users to generate, such as files created by your editor." | machine-wide exclude for one developer's files
- chg-no-per-user-ide-files | https://git-scm.com/docs/gitignore | Git project | "Patterns which should be version-controlled and distributed to other repositories via clone (i.e., files that all developers will want to ignore) should go into a .gitignore file." | repository ignore file
- chg-no-per-user-ide-files | https://git-scm.com/docs/gitignore | Git project | "auxiliary files that live inside the repository but are specific to one user’s workflow) should go into the $GIT_COMMON_DIR/info/exclude file" | machine-wide exclude
- chg-no-per-user-ide-files | https://git-scm.com/docs/gitignore | Git project | "Patterns which a user wants Git to ignore in all situations (e.g., backup or temporary files generated by the user’s editor of choice) generally go into a file specified by core.excludesFile in the user’s ~/.gitconfig." | machine-wide exclude
- chg-no-per-user-ide-files | https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore | GitHub | "!.vscode/settings.json" (the file ignores ".vscode/*" and negates the shared files) | keep the shared settings, ignore the rest
- chg-no-per-user-ide-files | https://intellij-support.jetbrains.com/hc/en-us/articles/206544839 | JetBrains | "All files under the .idea directory in the project root except the items that store user-specific settings : workspace.xml usage.statistics.xml shelf directory" | do not commit per-user IDE state; keep shared settings
- chg-no-per-user-ide-files | https://intellij-support.jetbrains.com/hc/en-us/articles/206544839 | JetBrains | "Do not share the .iws file as it stores user specific settings." | do not commit per-user IDE state
- chg-no-per-user-ide-files | https://www.jetbrains.com/help/idea/configure-project-settings.html | JetBrains | "This folder contains both user-specific settings that should not be placed under version control and project settings that are normally shared among developers working in a team, for example, the code style configuration." | do not commit per-user state; keep shared settings
- chg-no-per-user-ide-files | https://www.jetbrains.com/help/idea/configure-project-settings.html | JetBrains | "IntelliJ IDEA automatically moves the workspace.xml file with your personal settings to the .gitignore list to avoid conflicts with other developers' settings." | list the paths in the repository
- chg-no-per-user-ide-files | https://code.visualstudio.com/docs/configure/settings | Microsoft | "User settings are your personal settings for customizing VS Code." | per-user state is personal
- chg-no-per-user-ide-files | https://code.visualstudio.com/docs/configure/settings | Microsoft | "When you add a Workspace Settings settings.json file to your project or source control, the settings for the project will be shared by all users of that project." | keep shared settings
- chg-no-per-user-ide-files | https://learn.microsoft.com/en-us/azure/devops/repos/git/ignore-files | Microsoft | "Examples of files that typically don't need tracking include temporary files from your development environment, test outputs, and logs." | do not commit per-user state
- chg-no-per-user-ide-files | https://learn.microsoft.com/en-us/azure/devops/repos/git/ignore-files | Microsoft | "Because Git doesn't commit or push the exclude file, you can safely use it to ignore files on your local system without affecting anyone else." | machine-wide exclude
- chg-no-per-user-ide-files | https://developer.apple.com/documentation/xcode/setting-up-your-project-to-use-xcode-cloud | Apple | "Use shared schemes." | keep shared settings (fetched as the page's documentation JSON; the HTML page renders client-side)

## Not used

- mod-no-repeated-switches | https://shopify.engineering/other-driven-developments | Shopify | (no quote) | the page is a "driven development" essay; it never states the Rule
- code-test-suite-time-budget | https://firefox-source-docs.mozilla.org/testing/xpcshell/index.html | Mozilla | "requesttimeoutfactor A multiplier applied to the default test timeout." | a timeout, not a written performance budget; dropped from the card
- code-test-suite-time-budget | https://abseil.io/resources/swe-book/html/ch11.html | Google | "Small tests, regardless of the scope, are almost always faster and more deterministic than tests that involve more infrastructure or consume more resources." | about test sizes, not a time budget; dropped from the card
- fn-no-pass-through-wrapper | https://refactoring.guru/inline-method | Refactoring.Guru | "In itself, this delegation is no problem." | left as draft; the page does not back a blanket deletion rule
- chg-no-per-user-ide-files | https://alint.org/docs/bundled-rulesets/hygiene-no-tracked-artifacts/ | alint project | (not fetched in this pass) | not cited: alint.org has no entry in tools/orgs.py; the card uses a git command as its gate instead

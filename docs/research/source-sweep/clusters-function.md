# Function-level clusters

## fn-complexity-cap | orgs: 4 | status: READY
Rule: Keep each function's cyclomatic complexity under the project's limit (reported at 10 or more by default), and split a function that passes it.
Concern tags: maintainability, testing
Severity guess: discuss
Rows: 194, 509, 496, 2426, 2427, 2464
Orgs: pmd, rubocop, microsoft, lockheed
Conflicts/duplicates: none. fn-length-budget explicitly says complexity is not what it measures and lists CognitiveComplexity and CA1505 only as non-length gates.
Notes: limits differ (PMD 10, Lockheed 20, Microsoft 25); Lockheed exempts a switch with many case labels. Linter-owned, so the card needs a judgement clause (split by job, keep flat dispatch).

## fn-early-return-no-else | orgs: 3 | status: READY
Rule: Return early on the error or edge case instead of nesting the main path in ifs or adding else after return, break or continue.
Concern tags: maintainability
Severity guess: discuss
Rows: 91, 729, 822
Orgs: google, apache, llvm
Conflicts/duplicates: none (go-wrap-errors-with-w is about wrapping, not layout)
Notes: google row is Go (success path runs down the page), apache says flip the condition and exit, llvm bans else after return.

## fn-nesting-depth-cap | orgs: 3 | status: READY
Rule: Keep control-flow nesting shallow (PMD flags more than 3 levels; Pylint defaults to 5) and flatten deeper code with early exits.
Concern tags: maintainability
Severity guess: discuss
Rows: 510, 2241, 729
Orgs: pmd, pylint, apache
Conflicts/duplicates: none
Notes: apache backs only the "flip and exit early" clause, not a number; numeric cap has pmd and pylint only (2). Could merge with fn-early-return-no-else.

## fn-password-min-length | orgs: 3 | status: READY
Rule: Enforce a minimum password length when the user sets one.
Concern tags: security
Severity guess: should-fix
Rows: 1096, 1466, 1795
Orgs: nist, owasp, microsoft
Conflicts/duplicates: none (fn-password-slow-hash covers hashing only)
Notes: numbers differ (NIST 15 as single factor, OWASP floor plus max of at least 64, Microsoft default 6). Max-length and no-truncation clause has owasp only.

## fn-error-summary | orgs: 2 | status: NEAR
Rule: After a failed submit, show an error summary at the top that lists every error and links each to its field.
Concern tags: accessibility, usability
Severity guess: should-fix
Rows: 1073, 1124, 1057
Orgs: govuk, a11yproject
Conflicts/duplicates: none (fn-error-says-what-and-how states per-field message only)
Notes: w3c row 1034 (focus the first invalid input) is a different clause; govuk shows the summary even for one error.

## py-raises-specific-exception | orgs: 2 | status: NEAR
Rule: In a test, assert on the specific exception type, not bare Exception.
Concern tags: testing
Severity guess: should-fix
Rows: 746, 1192
Orgs: pycqa, pytest
Conflicts/duplicates: none (fn-specific-exceptions-only covers catching in business code)
Notes: pmd 2217 (do not declare generic Exception) is the production-code version, one more org only if the clause is widened.

## fn-no-logic-in-tests | orgs: 2 | status: NEAR
Rule: Keep if, for, while and switch out of test bodies, and split table cases that need different assertions.
Concern tags: testing
Severity guess: discuss
Rows: 1051, 2239
Orgs: microsoft, uber
Conflicts/duplicates: none
Notes: uber is about conditional assertions in table tests; microsoft bans all branching in unit tests.

## fn-exec-full-path | orgs: 2 | status: NEAR
Rule: Run a child program by an explicit path (resolved once, e.g. shutil.which), never by a bare name looked up through PATH or the current directory.
Concern tags: security
Severity guess: should-fix
Rows: 706, 855
Orgs: psf, google
Conflicts/duplicates: none (fn-no-shell-with-input covers argv vs shell string)
Notes: google row is Go's "./prog" rule; psf says fully qualified path.

## fn-no-aria-hidden-on-focusable | orgs: 2 | status: NEAR
Rule: Never put aria-hidden="true", role="presentation" or CSS hiding on an element that can take focus.
Concern tags: accessibility
Severity guess: should-fix
Rows: 933, 936
Orgs: google, webaim
Conflicts/duplicates: none (fn-focus-indicator-visible is about the outline)
Notes: w3c 1002 is about content covering the focus indicator, not this clause.

## fn-return-error-not-panic | orgs: 2 | status: NEAR
Rule: Library and production code returns errors for expected failures; it does not panic.
Concern tags: reliability
Severity guess: should-fix
Rows: 493, 2206
Orgs: uber, google
Conflicts/duplicates: none
Notes: Go-specific.

## fn-freeze-object-prototype | orgs: 2 | status: NEAR
Rule: Freeze Object.prototype at startup so prototype pollution cannot alter shared defaults.
Concern tags: security
Severity guess: discuss
Rows: 820, 2476
Orgs: snyk, mitre
Conflicts/duplicates: none directly; fn-no-prototype-pollution is the key-handling rule and does not state freezing
Notes: portswigger 866 and owasp 568 say a blocklist or Object.seal is not enough (different clause).

## fn-flags-type-for-flag-sets | orgs: 2 | status: NEAR
Rule: Model a set of independent flags as a flags type, and keep simple enums out of flags.
Concern tags: maintainability
Severity guess: discuss
Rows: 812, 899
Orgs: microsoft, rust
Conflicts/duplicates: none (fn-no-stringly-typed-returns covers closed sets)
Notes: microsoft says FlagsAttribute only on flag enums; rust says bitflags rather than an enum.

## cpp-no-c-style-cast | orgs: 2 | status: NEAR
Rule: Use C++ named casts, never C-style casts.
Concern tags: correctness, maintainability
Severity guess: discuss
Rows: 823, 2288
Orgs: llvm, google
Conflicts/duplicates: none
Notes: clang-tidy owns it; C++ only. Pair row 821/2287 (no C++ exceptions) is project policy, also llvm+google, not reviewable by diff.

## ONE-org rows (most promising)

## fn-validate-on-blur | orgs: 1 | status: ONE
Rule: Validate a field when the user leaves it, not while typing, and clear the error as soon as the value is valid.
Concern tags: usability
Severity guess: discuss
Rows: 543, 544, 545
Orgs: baymard
Conflicts/duplicates: none with cards; contradicts govuk row 615 (validate on submit, not on leave)
Notes: source disagreement, do not draft until resolved.

## fn-confirmation-specific | orgs: 1 | status: ONE
Rule: Name the item and the consequence in a confirmation, never a bare "Are you sure?", and give it no default Yes.
Concern tags: usability
Severity guess: discuss
Rows: 957, 958
Orgs: nngroup
Conflicts/duplicates: none (fn-destructive-confirm-or-undo exists; check it does not already say this)
Notes: owasp 2106 asks human approval for high-impact agent actions.

## fn-e2e-step-asserts | orgs: 1 | status: ONE
Rule: Every E2E test action carries an assertion or refutation.
Concern tags: testing
Severity guess: should-fix
Rows: 429
Orgs: shopify
Conflicts/duplicates: none
Notes: nasa 905 (include negative tests) is a nearby but different clause.

## fn-open-enum-fallback | orgs: 1 | status: ONE
Rule: When reading an open enum, handle unknown values with a fallback branch.
Concern tags: compatibility, reliability
Severity guess: should-fix
Rows: 1690
Orgs: stripe
Conflicts/duplicates: none
Notes: mod-proto-enum-zero-unspecified is related but covers the zero value only.

## fn-test-failure-message | orgs: 1 | status: ONE
Rule: A test failure message reports the actual and the expected result.
Concern tags: testing
Severity guess: discuss
Rows: 763
Orgs: google
Conflicts/duplicates: none
Notes: vodafone 907 (readable parameterised case names) is adjacent.

## fn-env-for-untrusted-ci-input | orgs: 1 | status: ONE
Rule: Pass untrusted workflow context values (PR titles) to scripts through an environment variable, not inline in the script.
Concern tags: security
Severity guess: should-fix
Rows: 299
Orgs: github
Conflicts/duplicates: partly fn-no-eval-untrusted
Notes: vendor-specific (GitHub Actions); chg or code level may fit better.

## fn-no-self-modifying-code | orgs: 1 | status: ONE
Rule: Do not write code that modifies itself at run time.
Concern tags: maintainability, security
Severity guess: discuss
Rows: 2465
Orgs: lockheed
Conflicts/duplicates: overlaps fn-no-eval-untrusted only loosely
Notes: none

## fn-opaque-access-token | orgs: 1 | status: ONE
Rule: Clients treat access tokens as opaque strings and do not parse or validate them.
Concern tags: security, compatibility
Severity guess: discuss
Rows: 817
Orgs: microsoft
Conflicts/duplicates: CONFLICT risk with fn-jwt-verify-pinned (verify before reading claims); scope differs (client vs resource server) but check
Notes: none

## Dropped
- Template-building from user input (533, 585, 868, 869; google, github, portswigger): duplicate of fn-no-eval-untrusted ("template compiler").
- Redirect target rows (863, 2282, 2482): duplicate of fn-redirect-target-allowlist.
- Uber 2237 (return nil, not empty slice): CONFLICT with fn-empty-collection-not-none; no card proposed.
- Mutable default arguments (693 psf, 769 and 1228 google): 2 orgs, no card covers it, but listed as NEAR candidate below.

## fn-no-mutable-default-arg | orgs: 2 | status: NEAR
Rule: Do not use a mutable object as a default argument; default to None and create it inside the function.
Concern tags: correctness
Severity guess: should-fix
Rows: 693, 769, 1228
Orgs: psf, google
Conflicts/duplicates: none (fn-no-caller-mutation covers caller-owned parameters, not defaults)
Notes: Python; linters (B006) own detection.

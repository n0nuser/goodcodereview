# Module-level clusters (92 NEW rows; no group reaches 3 orgs)

## mod-fakes-over-mocks | orgs: 3 | status: READY (3+ orgs, but likely DUPLICATE; see Conflicts)
Rule: Prefer a fake or the real code path over a mock-heavy test; do not let a test depend on another service's correctness.
Concern tags: testing, maintainability
Severity guess: should-fix
Rows: 260, 516, 722
Orgs: google, nvidia, spotify
Conflicts/duplicates: mod-mock-at-boundaries-only (states the same direction; check it before drafting), typescript-mock-at-the-boundary
Notes: google = fakes over Mockito; nvidia = end-to-end over mock-heavy; spotify = no cross-service dependence. Clauses differ, so the shared clause per org is thin; rows 260 and 516 back "fake or real over mock" (2 orgs); 722 backs only the second clause.

## mod-call-parent-setup-teardown | orgs: 2 | status: NEAR
Rule: A test class that overrides setUp, tearDown, setUpClass or tearDownClass calls the parent's version.
Concern tags: testing, reliability
Severity guess: should-fix
Rows: 1231, 2314
Orgs: laravel, psf
Conflicts/duplicates: none (nearest cards py-pytest-expensive-fixture-scope, typescript-shared-test-setup do not state it)
Notes: laravel says parent::setUp/tearDown; psf says call up to setUpClass/tearDownClass.

## mod-no-protected-in-final | orgs: 1 | status: ONE
Rule: Do not declare protected members in a final class; use private or package access.
Concern tags: maintainability
Severity guess: discuss
Rows: 2243, 2319
Orgs: pmd
Conflicts/duplicates: none
Notes: PMD rule, close to a linter-only rule.

## mod-aggregate-boundaries | orgs: 1 | status: ONE
Rule: Change entities inside an aggregate only through its aggregate root, and reference other aggregates by foreign key, not navigation.
Concern tags: maintainability, correctness
Severity guess: should-fix
Rows: 1237, 1238
Orgs: microsoft
Conflicts/duplicates: none (mod-internals-unreachable is adjacent, not equal)
Notes: both rows Microsoft DDD pages.

## mod-declare-direct-deps | orgs: 1 | status: ONE
Rule: A file or rule declares each direct dependency it uses and does not rely on transitive ones.
Concern tags: maintainability, reliability
Severity guess: should-fix
Rows: 1046, 1159
Orgs: google
Conflicts/duplicates: none
Notes: C++ includes and Bazel deps; same org, two languages.

## mod-no-service-locator | orgs: 1 | status: ONE
Rule: Take dependencies by injection; do not call a service locator (GetService) for them.
Concern tags: maintainability, testing
Severity guess: should-fix
Rows: 1246
Orgs: microsoft
Conflicts/duplicates: none (mod-inject-boundary-collaborators adjacent)
Notes: spring row 1200 (plain `new`, no container) is a neighbouring practice, not the same clause.

## mod-no-virtual-in-ctor | orgs: 1 | status: ONE
Rule: Do not call virtual members from inside a constructor.
Concern tags: correctness
Severity guess: should-fix
Rows: 1255
Orgs: microsoft
Conflicts/duplicates: none (mod-no-logic-in-constructors adjacent)
Notes: checkable in review at class level.

## mod-config-mutually-exclusive | orgs: 1 | status: ONE
Rule: Reject a config that sets none or several of a set of mutually exclusive fields, or two entries claiming the same unique key.
Concern tags: correctness, reliability
Severity guess: should-fix
Rows: 2177, 2178, 2179
Orgs: envoy
Conflicts/duplicates: none (mod-validate-at-boundary-once adjacent)
Notes: Envoy proto validation rules.

## mod-validate-before-use | orgs: 1 | status: ONE
Rule: Call the validation step (is_valid) before reading validated data or saving.
Concern tags: correctness
Severity guess: should-fix
Rows: 952
Orgs: drf
Conflicts/duplicates: none
Notes: framework-specific; row 953 (partial update reads self.instance) is a separate clause.

## mod-subtype-exceptions | orgs: 1 | status: ONE
Rule: A subtype method signals only the exceptions its supertype method signals.
Concern tags: correctness, compatibility
Severity guess: should-fix
Rows: 2518
Orgs: liskov-wing
Conflicts/duplicates: mod-subtype-passes-parent-tests (partly covered by "accept/promise"); likely DUPLICATE, check
Notes: Liskov-Wing paper, an academic source.

## mod-no-public-collection-or-setters | orgs: 1 | status: ONE
Rule: Do not expose a domain object's collection or setters publicly; change state through methods.
Concern tags: maintainability
Severity guess: discuss
Rows: 1178, 1179
Orgs: nimblepros
Conflicts/duplicates: CONFLICT risk with row 2324 (google: make a trivial getter/setter attribute public); no card id
Notes: gnome 628 (do not export global variables) is a different clause.

## Dropped
- Duplicate of py-imports: 2321 (aisi, absolute imports), 2323 (google, imports at top).
- Same org only, divergent or product-specific: 2254/2257 (psf from-import), 92 (google dot-import), 1329/2514 (vitest), 830-833 (nodejs crypto API order), 2579/2580 (pgbouncer), tool-only or vendor-behaviour rows.

# Module audit index

One line per stable module card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `module.md`: read them with offset `<first>` and limit `<count>`.

- `mod-behaviour-lives-with-state` [discuss] {maintainability} L3+25: Put the invariants and calculations that read only one object's fields on that object.
- `mod-bounded-fan-out` [discuss] {maintainability} L29+26: Set a limit on how many other types or modules one unit depends on, and split a unit that passes it.
- `mod-class-size-budget` [discuss] {maintainability} L56+31: Split a class that passes the project's size limit for fields, public methods or lines, unless it is a data record.
- `mod-colour-tokens-meet-contrast` [should-fix] {accessibility, usability} <ui> L88+38: Make every text and background token pair meet 4.5:1 (3:1 for large text), and every border, icon, and focus colour meet 3:1 against its neighbour.
- `mod-deep-modules` [discuss] {maintainability} L127+26: Prefer a small interface that hides its implementation, and add a member only when callers need it.
- `mod-derive-dont-duplicate` [should-fix] {compatibility, maintainability} L154+26: Derive a type, list or enum from the schema or list that owns it, or add a build check that fails when the two disagree.
- `mod-fowler-smells` [discuss] {maintainability} L181+24: Name the smell, point to the line, and suggest the refactoring; do not file smells as taste.
- `mod-inject-boundary-collaborators` [should-fix] {testing, maintainability} L206+26: Inject boundary collaborators through the constructor; do not construct them inside or reach for a global.
- `mod-internals-unreachable` [should-fix] {maintainability} L233+27: Keep a module's internals unimportable and untouched from outside it. A caller uses the public surface, not a private file or member.
- `mod-law-of-demeter` [discuss] {maintainability} L261+25: Call methods on your direct collaborators, and do not call a method on an object that another call returned (a chain of two or more getters).
- `mod-layers-point-inward` [should-fix] {maintainability} L287+27: Make dependencies point inward: surface, then logic, then boundary.
- `mod-no-import-cycles` [should-fix] {maintainability} L315+28: Keep the dependency graph between modules or packages acyclic, and break a cycle by moving the shared part into a third module that both depend on.
- `mod-no-import-side-effects` [should-fix] {testing, maintainability} L344+26: Keep I/O at the edges: importing a package must not touch the network, read files, or read the environment.
- `mod-no-logic-in-constructors` [should-fix] {correctness, testing} L371+29: Assign only in constructors, and put I/O, parsing, and heavy computation in a named factory.
- `mod-no-module-mutable-state` [should-fix] {correctness, testing} L401+36: Keep no mutable state at module level; hold it on an instance.
- `mod-no-shotgun-surgery` [discuss] {maintainability} L438+25: Keep one decision in one module, and when a single change needs edits in many classes, move the scattered parts together.
- `mod-no-utils-grab-bag` [should-fix] {maintainability} L464+24: Put a helper in the module that owns the concept, or in a new module named after the concept.
- `mod-no-wrong-abstraction` [should-fix] {maintainability} L489+25: Inline an abstraction that has grown flags for its callers.
- `mod-one-name-per-concept` [should-fix] {maintainability} L515+28: Use one name for one concept across the codebase.
- `mod-pooled-clients-built-once` [should-fix] {performance} L544+29: Build pooled clients once at startup and reuse them.
- `mod-proto-enum-zero-unspecified` [should-fix] {compatibility} L574+32: Give every protobuf enum a zero value named `<ENUM>_UNSPECIFIED` with no real meaning.
- `mod-single-writer-per-state` [should-fix] {correctness} L607+25: Let only one writer change a piece of state at a time, through a single owner, a queue that serialises the writes, or compare-and-swap, never by convention.
- `mod-vetted-crypto-only` [block] {security} L633+27: Encrypt with an authenticated mode such as AES-GCM, and never reuse a nonce under one key.
- `mod-yagni` [should-fix] {maintainability, process} L661+25: Do not build an abstraction or capability for a need that does not exist yet; add it when the need or a second use appears.
- `py-class-earns-its-instance` [discuss] {maintainability} L687+32: Give a class real state or a collaborator; otherwise write a module function.
- `py-field-only-when-adds` [discuss] {correctness} L720+25: Use `Field()` only when it adds something (a constraint, an alias, or API docs), and set plain defaults directly.
- `py-httpx-client-lifespan` [should-fix] {performance} L746+30: Pass an explicit `httpx.Timeout` to every `httpx` client.
- `py-imports` [should-fix] {maintainability} L777+26: Put imports at module top, absolute only.
- `py-no-init-or-model-tests` [should-fix] {testing} L804+24: Cover `__init__` and plain models through the behaviour that uses them.
- `py-pytest-expensive-fixture-scope` [should-fix] {testing, performance} L829+49: Give an expensive pytest fixture `scope="session"` or `"module"` and isolate each test with a rollback, never a schema build or a seed load inside a function-scoped fixture.
- `py-test-hygiene` [discuss] {testing, reliability} L879+33: Keep unit tests off external I/O (the network, the shared filesystem and the database) and off the real clock, and run tests that need them in a separate, slower tier.
- `py-xdist-worker-isolated-state` [should-fix] {testing, reliability} L913+32: Under pytest-xdist, give each worker its own database or other mutable resource, keyed by `worker_id`, and build an expensive shared one once with a lock file.

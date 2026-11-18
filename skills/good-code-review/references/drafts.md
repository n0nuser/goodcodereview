# Draft cards

A draft card is not vetted. Report a `FAIL` of one under Draft findings, at `should-fix` at most, never in the ledger or the verdict. A draft `change`, `incident`, or `production` card applies only to a diff, an incident, or a release.

# change drafts

## chg-agent-mock-asserting-tests

level: change  
severity: should-fix  
concerns: testing, process  
applies_when: Tests were generated or edited alongside the code under test, especially by an agent.  
lacks: orgs, Google and cursor/plugins back it; Go backs a side remark and Feathers points the other way

Write tests that fail when the behaviour breaks, and reject tests that mostly assert on mocks, copy the implementation, or were edited to match new output without explanation.

## chg-api-spec-in-same-change

level: change  
severity: should-fix  
concerns: compatibility  
applies_when: The diff adds, removes or changes an HTTP route, a request or response field, a status code or a header.  
context: server  
lacks: orgs, OpenAPI and Zalando back it; needs a third org

Update the API spec in the same change that alters the routes, fields, status codes or headers it describes.

## chg-bot-approval-not-human

level: change  
severity: should-fix  
concerns: process, security  
applies_when: Branch protection or policy requires a human approval and a bot or agent can also approve.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that bar bot or agent approvals from a required human review

Do not let a bot or agent approval satisfy a required human approval.

## chg-changelog-entry

level: change  
severity: discuss  
concerns: maintainability, process  
applies_when: The project keeps a changelog, and the change adds, removes or changes a feature.  
lacks: orgs, a changelog entry per feature change has USGS and Rails; needs a third org

Add a changelog entry to each change that adds, removes or changes a feature.

## chg-fix-root-cause-not-symptom

level: change  
severity: should-fix  
concerns: correctness, testing  
applies_when: A change fixes a bug, a failing test, or an incident.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

In a bug fix, state the cause you saw in evidence, and reject a guard, retry, sleep, longer timeout, swallowed error, cast, skipped or weakened test, or special case for the failing input that the cause does not justify.

## chg-flag-owner-retirement

level: change  
severity: should-fix  
concerns: reliability  
applies_when: The change adds a feature flag, kill switch or config toggle.  
lacks: orgs, owner has Dropbox and Statsig; removal ticket has Statsig; default has GitLab; each needs another org

Give every new flag an owner, a default, and a removal condition or date, and ticket the removal.

## chg-link-tracked-issue

level: change  
severity: discuss  
concerns: process, maintainability  
applies_when: The project tracks work in an issue tracker.  
lacks: orgs, "link each PR to its issue" has Apache and WordPress; needs a third org

Link each pull request to the issue it addresses, with a keyword such as `Closes` or `See`.

## chg-matches-spec

level: change  
severity: should-fix  
concerns: process  
applies_when: The change links a ticket, spec or issue.  
lacks: orgs, checking the change against the spec has Google, plus Dropbox for security only; needs a third org

Trace every behaviour change in the diff to the stated requirement, and flag missing requirements and any change nobody asked for.

## chg-new-api-has-usage

level: change  
severity: should-fix  
concerns: maintainability  
applies_when: The change adds a public function, endpoint, option, interface or extension point.  
context: server  
lacks: duplicate, its FAIL shapes, an unused option and a one-implementation Protocol, are the stable mod-yagni Rule

Ship new API with at least one real caller in the same change, and fail speculative interfaces and options that nothing uses.

## chg-new-query-has-plan

level: change  
severity: should-fix  
concerns: performance  
applies_when: The change adds or rewrites a SQL query against a table that grows with users or time.  
context: data  
lacks: failable, without "attach the plan" a change review has nothing to mark FAIL; attaching has GitLab only

Attach the query plan for each new or rewritten query on a growing table, taken on production-sized data.

## chg-review-comment-format

level: change  
severity: discuss  
concerns: process  
applies_when: A reviewer writes feedback on a change.  
lacks: evidence, Google and Orosz recommend labels; Cloudflare and Dropbox describe their own tool output, not a rule for reviewers

Label each review comment with its severity: block, should-fix, or discuss.

## chg-review-rigour-by-risk

level: change  
severity: should-fix  
concerns: process  
applies_when: A repository sets how many approvals or how deep a review a change needs.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that set review depth by what the change touches

Set the review tier from what the change touches, such as auth, billing, CI or release workflows, and not from who wrote it.

## chg-review-rounds-capped

level: change  
severity: discuss  
concerns: process  
applies_when: A change goes through repeated review rounds, especially with an automated author or reviewer.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that cap review rounds or limit re-review to the new diff

Cap the number of review rounds; after the cap, re-review only the new diff and ask the author to rethink the approach if findings keep coming.

## chg-review-threads-resolved

level: change  
severity: should-fix  
concerns: process  
applies_when: A change has review comments and is about to merge.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that block merge on open review threads

Do not merge while any review thread is open; each one ends as a fix or as a resolution with a stated reason.

## chg-sensitive-paths-human-owner

level: change  
severity: should-fix  
concerns: security, process  
applies_when: The change touches code or config for auth, billing, CI or release workflows.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that name human owners for auth, billing, CI and release paths

Name a human owner in CODEOWNERS for auth, billing, CI and release paths, and require that owner's approval.

# function drafts

## fn-atomic-related-updates

level: function  
severity: should-fix  
concerns: correctness  
applies_when: One operation writes to two or more places that must agree (rows, tables, stores, files).  
lacks: orgs, only one vendor's review skill backs it; the all-or-nothing principle has no cited org

Make related writes succeed or fail together.

## fn-empty-collection-not-none

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A function returns a list, set or map.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Return an empty collection for "nothing found"; return `None` only when absent differs from empty.

## fn-error-summary

level: function  
severity: should-fix  
concerns: accessibility, usability  
applies_when: Code renders a form again after validation fails.  
context: ui  
lacks: orgs, "links each error to its field" has GOV.UK only; needs two more orgs that show a linked summary

After a failed submit, show a summary at the top of the page that lists every error and links each one to its field.

## fn-flags-type-for-flag-sets

level: function  
severity: should-fix  
concerns: maintainability, correctness  
applies_when: A type holds a set of independent options that can be combined, such as permissions or render options.  
lacks: orgs, Microsoft and the Rust API guidelines state it; a third independent organisation is missing

Model a set of independent flags with the language's or ecosystem's flags type (a `[Flags]` enum in C#, the `bitflags` crate in Rust), and do not use a plain enum for it.

## fn-known-keys-get-a-type

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A function takes or returns a dictionary whose keys are fixed and known.  
lacks: orgs, "record type for fixed keys" has PSF and attrs; mypy and PEP 589 share an author; needs one more org

Give a fixed key set a record type: a model, a dataclass or a typed dict.

## fn-no-anonymous-tuples

level: function  
severity: should-fix  
concerns: maintainability  
applies_when: A function returns or passes a tuple whose positions mean different things.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Return a small named record, not a positional tuple, once the fields differ in meaning.

## fn-no-aria-hidden-on-focusable

level: function  
severity: should-fix  
concerns: accessibility  
applies_when: Markup or CSS hides an element that can take keyboard focus.  
context: ui  
lacks: orgs, Google and WebAIM state it; a third independent organisation is missing

Never put `aria-hidden="true"` on an element that can take focus, or leave an element visually hidden while it has focus.

## fn-no-logic-in-tests

level: function  
severity: discuss  
concerns: testing, maintainability  
applies_when: A test body contains if, for, while or switch, or a table test branches on its case.  
lacks: orgs, "no branching in test bodies" has Microsoft and Uber only; needs one more org

Keep `if`, `for`, `while` and `switch` out of test bodies, and split table cases that need different assertions into separate tests.

## fn-no-pass-through-wrapper

level: function  
severity: should-fix  
concerns: maintainability  
applies_when: A method's whole body calls a collaborator's method of the same name with the same arguments.  
lacks: orgs, Ousterhout is the only backer, through two links to one author; needs two more orgs

Delete a method that only forwards, and keep wrappers that validate, adapt, or narrow.

## fn-no-stringly-typed-returns

level: function  
severity: should-fix  
concerns: correctness, compatibility  
applies_when: A function returns a status, kind or outcome as a string, and callers branch on it.  
lacks: orgs, "closed type for a returned status" has Microsoft and Apple; Rust covers arguments and Kotlin is a feature page; needs one more org

Return a closed type (an enum, a tagged union or a sealed hierarchy) for a closed set of values, not a bare string. For a boolean flag, see [[fn-bool-arg-at-callsite]].

## fn-propagate-dont-swallow

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A handler catches an error and either drops it or raises a different one.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Chain the original cause when you translate an exception.

## fn-resource-lifetime

level: function  
severity: should-fix  
concerns: correctness  
applies_when: Code starts a task, thread, goroutine, or subprocess, or opens a handle (file, socket, connection).  
lacks: orgs, a structured-concurrency blog (one person) and Google (cancel path) back it; needs two more orgs for the owner rule

Give every task and handle an owner that waits for it or closes it, on the error path too.

# module drafts

## mod-call-parent-setup-teardown

level: module  
severity: should-fix  
concerns: testing, reliability  
applies_when: A test class overrides setUp, tearDown, setUpClass or tearDownClass in an xUnit-style framework.  
lacks: orgs, "call the parent's setUp and tearDown" has Laravel and PSF; needs a third org

A test class that overrides `setUp`, `tearDown`, `setUpClass` or `tearDownClass` calls the parent's version.

## mod-central-config

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: Business code reads environment variables or holds configuration values.  
lacks: orgs, "one settings module" has no org; Uber and Cabify back only keeping knobs out of code

Read configuration in one settings module and pass it in; business code must not read the environment or hold knobs.

## mod-cohesive-unit

level: module  
severity: discuss  
concerns: maintainability  
applies_when: A module or package is large, mixes concepts, or holds a very large literal.  
lacks: failable, "one cohesive concept" is hard to mark FAIL; the Ousterhout backer is a secondary summary

Keep one cohesive concept per module.

## mod-mock-at-boundaries-only

level: module  
severity: should-fix  
concerns: testing  
applies_when: A test uses mocks, patches or fakes.  
lacks: evidence, Airbnb mocks services in load tests and Cabify runs a real gRPC server; neither states the Rule

Mock only at the process boundary (HTTP, DB, cloud, clock, I/O).

## mod-no-repeated-switches

level: module  
severity: discuss  
concerns: maintainability  
applies_when: The same switch or if-chain on one type, status or kind appears in more than one place.  
lacks: orgs, "repeated condition to polymorphism" has Refactoring.Guru and Google; needs one more org (the Shopify post does not mention switches)

When the same switch or if-chain on one type appears in more than one place, replace the copies with polymorphism, unless each copy is an exhaustive switch over a closed type that fails the build when a case is missing.

## mod-no-wire-types-in-public-api

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: A module exposes a public function, class or re-export.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

Expose domain types in a module's public interface, and keep transport, storage and framework types behind it.

## mod-prefer-sync-api

level: module  
severity: discuss  
concerns: correctness  
applies_when: A module wraps protocol, parsing or business logic and offers it to callers that may be sync or async.  
lacks: evidence, the sans-io and async-pressure posts are opinion and neither states this as a rule; the card combines them

Keep logic in plain synchronous functions with no I/O, and add async wrappers at the edge only.

## mod-shim-fails-loudly

level: module  
severity: should-fix  
concerns: correctness, reliability, testing  
applies_when: The code replaces, wraps or stubs another library, symbol or service, such as a compatibility shim, a global monkeypatch or a stub with a default return.  
lacks: evidence, the sources define how an unimplemented operation signals itself; none states a practice about shims or monkeypatches in production

A shim or stub must raise for every operation it does not implement; it must not return a success value such as 0, `None` or an empty result for an unknown call.

## mod-subtype-passes-parent-tests

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: The code adds a subclass or an implementation of an interface.  
lacks: evidence, Liskov and Wing state the substitution rule; none says to run the parent's tests, which is the card's proxy

Make a subtype pass its parent's tests: accept every input the parent accepts, promise at least what it promises, and keep its invariants.

## mod-thin-entry-point

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: The application has a main module, an entry point, or a bootstrap file.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Keep the entry module to wiring (bootstrap, configuration, lifespan) and put no business logic in it.

## mod-validate-at-boundary-once

level: module  
severity: should-fix  
concerns: correctness, maintainability  
applies_when: Input checks appear in more than one layer, or hand-rolled checks appear on a dict.  
lacks: failable, nobody backs "once"; without it the FAIL, hand-rolled checks in the handler, would pass

Validate at the boundary, once, with a schema or model, so that inner layers receive typed, already-valid data.

# service drafts

## svc-401-sends-challenge

level: service  
severity: should-fix  
concerns: compatibility, correctness  
applies_when: A service answers a request that lacks valid credentials for a protected resource.  
context: server  
lacks: orgs, one org (IETF); the Siemens guideline restates RFC 9110, so it adds none; needs two more orgs that require the challenge

Send a `WWW-Authenticate` challenge with every 401 response.

## svc-api-safe-idempotent-methods

level: service  
severity: should-fix  
concerns: compatibility  
applies_when: A service exposes HTTP endpoints, or a handler changes which method it accepts.  
context: server  
lacks: duplicate, the GET half is already in stable svc-csrf-state-changing; PUT and DELETE have IETF only

Keep GET, HEAD and OPTIONS free of side effects, and make PUT and DELETE give the same end state when repeated.

## svc-api-spec-matches-impl

level: service  
severity: should-fix  
concerns: compatibility  
applies_when: A service publishes an OpenAPI (Swagger) description that callers, SDK generators or gateways read.  
context: server  
lacks: contradiction, the Rule makes the spec the source of truth, then allows generating it from code; pick one

Keep the OpenAPI document as the source of truth, and generate it from the code or test the running service against it in CI.

## svc-api-trace-context

level: service  
severity: should-fix  
concerns: observability  
applies_when: A service calls another service over HTTP while handling a request.  
context: server  
lacks: orgs, W3C is the only backer; needs two more orgs that forward trace headers on every call

Forward `traceparent` and `tracestate` on every outgoing call, keep the incoming trace id, and set a new parent id for each hop.

## svc-boolean-no-is-prefix

level: service  
severity: discuss  
concerns: maintainability  
applies_when: A new API defines a boolean field or query parameter.  
context: server  
lacks: orgs, Google and Microsoft only; needs one more org that drops the "is" prefix on boolean API fields

Name a new boolean field for its state (`enabled`, `required`), not with an `is` prefix.

## svc-debug-off-in-production

level: service  
severity: should-fix  
concerns: security  
applies_when: The service has a debug mode or serves API docs or a developer UI such as Swagger.  
context: server  
lacks: orgs, OWASP backs debug modes and Microsoft backs Swagger UI; needs one more org per clause that turns debug tooling off in production

Keep debug modes and developer tooling, such as Swagger UI, disabled in production.

## svc-logs-tamper-resistant

level: service  
severity: should-fix  
concerns: security, observability  
applies_when: The service writes security-relevant logs or an audit trail.  
context: server  
lacks: orgs, tamper resistance has Google and OWASP only; needs a third org that ships logs to a store the host cannot alter

Ship logs and audit trails to a store that the logged host cannot alter or delete.

## svc-page-title-per-route

level: service  
severity: should-fix  
concerns: accessibility, usability  
applies_when: An app serves several pages or client-side routes under one HTML shell.  
context: ui  
lacks: held, kept draft by Pablo's call; W3C, Mozilla and A11y Project back the Rule

Give every page and every client-side view its own `<title>` that says what it is.

## svc-paginate-by-server-links

level: service  
severity: should-fix  
concerns: correctness, compatibility  
applies_when: The code calls a paginated HTTP or RPC API and reads more than one page.  
context: server  
lacks: orgs, "follow the next link" has GitHub only and "do not parse the token" has Google only; needs two more orgs for each

Fetch the next page only from the link or token the server returned; do not build page numbers or open the token.

## svc-path-normalise-before-authz

level: service  
severity: should-fix  
concerns: security  
applies_when: A proxy, gateway or CDN sits in front of the service and a deny, allow or cache rule matches on the URL path.  
context: server  
lacks: orgs, Envoy backs escaped-slash rejection and PortSwigger backs path agreement; each clause has fewer than three orgs

Normalise the URL path once at the first hop, or reject escaped slashes there, so every hop resolves a path to the same resource before any routing or authorisation rule runs.

## svc-rate-limit-by-cost

level: service  
severity: should-fix  
concerns: performance, reliability  
applies_when: One API or store serves requests whose cost differs by orders of magnitude, such as GraphQL queries, scans next to point reads, or bulk endpoints.  
context: server  
lacks: evidence, only Microsoft recommends cost-based limits; Shopify, GitHub and Airbnb describe them, and Uber dropped a bytes-based quota

When request costs differ by orders of magnitude, charge each request its estimated cost against the quota instead of counting it as one.

## svc-request-id-logging

level: service  
severity: should-fix  
concerns: observability  
applies_when: A service handles requests and writes logs while doing so.  
context: server  
lacks: evidence, the W3C spec does not mention logs; only Honeycomb backs putting the id on every log line

Put the request or trace id on every log line written during a request.

## svc-security-event-logging

level: service  
severity: should-fix  
concerns: security, observability  
applies_when: The service authenticates users.  
context: server  
lacks: held, kept draft by Pablo's call

Log every failed authentication with the account name and a timestamp.

## svc-security-headers

level: service  
severity: should-fix  
concerns: security  
applies_when: The service serves HTML pages or sets cookies for browsers over HTTPS.  
context: server  
lacks: held, kept draft by Pablo's call

Send `Strict-Transport-Security` on every HTTPS response.

## svc-server-read-timeouts

level: service  
severity: should-fix  
concerns: security, reliability  
applies_when: The service runs its own HTTP server and untrusted clients or networks can reach it.  
context: server  
lacks: orgs, Cloudflare (Go) and Node.js only; needs one more org that sets server read and header timeouts for untrusted clients

Set a header-read timeout and a request-read timeout on a server that faces untrusted clients.

## svc-tenant-scope-in-data-layer

level: service  
severity: should-fix  
concerns: security, correctness  
applies_when: Several tenants share one table or database and the service reads tenant data.  
context: data  
lacks: orgs, Microsoft (EF Core query filter) and OWASP (row-level security) only; needs one more org that scopes tenants in the data layer by default

Enforce tenant scope in the data layer by default, with a query filter or row-level security, not by a predicate at each call site.

# system drafts

## sys-append-only-stores-have-retention

level: system  
severity: should-fix  
concerns: reliability, performance  
applies_when: The system keeps a table, file, index or in-memory map that gains an entry for each event, request or job and that no code removes entries from.  
lacks: evidence, each source is one product's retention setting for its own store; none states the practice for your own tables

Give every store that only grows (event, audit and history tables, log files, finished-job registries) a maximum age or count, and a job or setting that enforces it.

## sys-cache-cold-start

level: system  
severity: should-fix  
concerns: performance, reliability  
applies_when: Cache misses fall through to a database or downstream service.  
lacks: orgs, AWS is the only backer; needs two more orgs

Cap and coalesce the cache-miss path so an empty cache cannot overwhelm the origin.

## sys-cache-hit-rate-watched

level: system  
severity: should-fix  
concerns: observability, performance, reliability  
applies_when: The change adds a cache, or resizes one, in front of a database or downstream service.  
context: server  
lacks: orgs, both clauses have AWS and Google only; the third source shows a cache chart, not a hit-rate or memory metric; needs one more org

Emit a cache hit-rate or memory-use metric and alert on it, so an undersized cache is noticed before it hurts the origin.

## sys-constraint-not-valid

level: system  
severity: should-fix  
concerns: compatibility  
applies_when: A migration adds a CHECK, FOREIGN KEY, or NOT NULL constraint to a large existing table.  
context: data  
lacks: orgs, PostgreSQL docs are the only backer; needs two more orgs that add constraints in two steps

Add the constraint `NOT VALID`, then run `VALIDATE CONSTRAINT` in a separate step, and never leave the VALIDATE out.

## sys-hedge-budget

level: system  
severity: should-fix  
concerns: reliability, performance  
applies_when: The code sends a second copy of a request to another replica when the first is slow.  
context: server  
lacks: orgs, Google and Envoy back it; needs one more org that caps hedged requests or honours server pushback

Cap hedged requests with a retry budget or retry limit, and stop hedging when the server asks clients not to retry.

## sys-leader-two-leaders

level: system  
severity: should-fix  
concerns: reliability  
applies_when: A job runs only on an elected leader or lease holder.  
lacks: orgs, AWS is the only backer; needs two more orgs

Make leader work safe if two leaders overlap: make it idempotent, check the lease before acting, and stop when renewal fails.

## sys-shuffle-shard

level: system  
severity: should-fix  
concerns: reliability  
applies_when: Many tenants share a pool of workers or nodes, and one tenant's traffic or bug can take a worker down.  
context: server  
lacks: orgs, AWS and Airbnb back it; needs one more org that assigns tenants to shuffled worker subsets

Assign each tenant a shuffled subset of shared workers, so one tenant's fault reaches only a few other tenants.

# codebase drafts

## code-ci-job-pass-rate-threshold

level: codebase  
severity: discuss  
concerns: reliability, process  
applies_when: Auditing how a team keeps its main-branch pipeline and blocking CI jobs trustworthy.  
lacks: orgs, GitLab states a target and Kubernetes a gate; needs one more org that sets a numeric pass rate for the pipeline or a blocking job

Set a numeric pass-rate threshold for the pipeline or each blocking job, and act when it falls below it.

## code-documented-setup-runs

level: codebase  
severity: should-fix  
concerns: maintainability, process  
applies_when: Auditing a repo's README or contribution guide.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs that test the setup commands

Keep the setup, build and run commands in the README or contribution guide accurate: they work as written on a clean checkout, and any drift is fixed or reported.

## code-gate-new-violations-only

level: codebase  
severity: should-fix  
concerns: maintainability, process  
applies_when: Auditing a codebase that adopted a linter, a quality gate or an architecture rule after most of its code existed.  
lacks: orgs, SonarSource (a vendor) and ArchUnit back it; needs one more org that gates on new code and keeps old violations apart

Gate CI on new or modified code, and track pre-existing violations in a separate store without letting a build add to it.

## code-signed-commits-protected

level: codebase  
severity: should-fix  
concerns: security, process  
applies_when: Auditing the branch protection of a repository that ships code or holds release branches.  
lacks: orgs, "require signed commits" has OWASP and Node.js; GitHub documents the setting and AWS calls signing optional; needs one more org

Require signed commits on protected branches, so unsigned commits cannot merge or be pushed.

## code-test-suite-time-budget

level: codebase  
severity: should-fix  
concerns: testing, performance, process  
applies_when: Auditing how a codebase keeps its own test suite fast.  
lacks: orgs, "fail the build on a suite or per-test budget" has thoughtbot and SciPy; needs one more org

Record the suite's total time and its slowest tests on every CI run, and fail the build when the total or a single test passes a written budget.

## code-tests-order-independent

level: codebase  
severity: should-fix  
concerns: testing, reliability  
applies_when: Auditing a test suite for tests that pass alone and fail in a run, or the reverse.  
lacks: orgs, GitLab and Alloy back it; Kent Beck is a person and does not count; needs one more org that runs tests in random order or isolates state

Make each test pass in any order, sharing no mutable state with other tests.

# production drafts

## prod-wide-events-bounded-labels

level: production  
severity: should-fix  
concerns: observability  
applies_when: A request handler or job emits telemetry.  
lacks: orgs, Honeycomb is the only backer, and the Rule does not mention bounded labels; needs two more orgs

Emit one structured event per request carrying trace, tenant, build and flag state.

# incident drafts

## inc-perf-regression-guard

level: incident  
severity: should-fix  
concerns: performance, testing  
applies_when: A postmortem covers a performance regression or a resource-exhaustion incident.  
lacks: duplicate, the guard half is the stable code-perf-budget-in-ci Rule; the postmortem-action half has Google SRE and Cloudflare only

Add an automated check that would have caught the regression (a benchmark, a budget, a load-test threshold, or a resource guard) as one of the postmortem's actions.

## inc-postmortem-owned-actions

level: incident  
severity: should-fix  
concerns: reliability, process  
applies_when: A postmortem or incident review is written or audited.  
lacks: orgs, an owner and due date on each action has no org; Dropbox and Shopify mention action items without naming either

Give every postmortem action one named owner, a due date, and a tracker link.

## inc-review-asks-which-check

level: incident  
severity: should-fix  
concerns: reliability, process  
applies_when: An incident review or postmortem is written or audited.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs whose incident review asks which check or layer should have caught the fault

Every incident review names the check that should have caught the fault (a test, CI gate, review, canary or alert) and turns the gap into a new or fixed check.

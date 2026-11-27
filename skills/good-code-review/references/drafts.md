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
lacks: orgs, Kubernetes (spec in the same PR) and Zalando (spec first) back it; OpenAPI defines the format only; needs one more org

Update the API spec in the same change that alters the routes, fields, status codes or headers it describes.

## chg-bot-approval-not-human

level: change  
severity: should-fix  
concerns: process, security  
applies_when: Branch protection or policy requires a human approval and a bot or agent can also approve.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that bar bot or agent approvals from a required human review

Do not let a bot or agent approval satisfy a required human approval.

## chg-fix-root-cause-not-symptom

level: change  
severity: should-fix  
concerns: correctness, testing  
applies_when: A change fixes a bug, a failing test, or an incident.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

In a bug fix, state the cause you saw in evidence, and reject a guard, retry, sleep, longer timeout, swallowed error, cast, skipped or weakened test, or special case for the failing input that the cause does not justify.

## chg-link-tracked-issue

level: change  
severity: discuss  
concerns: process, maintainability  
applies_when: The project tracks work in an issue tracker.  
lacks: orgs, Apache requires an issue per PR; WordPress ships a Closes template; CPython puts the issue number in the news file name; needs a third org

Link each pull request to the issue it addresses, with a keyword such as `Closes` or `See`.

## chg-matches-spec

level: change  
severity: should-fix  
concerns: process  
applies_when: The change links a ticket, spec or issue.  
lacks: orgs, Google and Microsoft check the change against the task; none says to flag changes nobody asked for or missing requirements; needs a third org

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

## chg-review-threads-resolved

level: change  
severity: should-fix  
concerns: process  
applies_when: A change has review comments and is about to merge.  
lacks: orgs, GitHub and GitLab document the merge setting only; the Anthropic X post cannot be re-fetched; needs orgs that state it as a rule

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
lacks: orgs, PostgreSQL, Django and Rails describe what a transaction is, not a rule to wrap related writes; needs orgs that tell reviewers to do so

Make related writes succeed or fail together.

## fn-comments-stay-short

level: function  
severity: should-fix  
concerns: maintainability  
applies_when: A comment block runs past a few lines, such as a long explanation above a config value or env var.  
lacks: contradiction, only GitLab and Home Assistant set a length limit; Go says no fixed length and CockroachDB values long comments

Keep a comment to a few lines. Put a longer explanation in the docs, a README or an ADR, and leave a one-line link in the comment.

## fn-empty-collection-not-none

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A function returns a list, set or map.  
lacks: orgs, Microsoft states it; PMD's rule page is a tool description; SEI CERT MET55-J would not load; needs two more orgs

Return an empty collection for "nothing found"; return `None` only when absent differs from empty.

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
lacks: orgs, chaining has Microsoft; Python and Oracle describe the mechanism; Google Go and SEI CERT back no-swallow, which is in the Why; needs two more orgs

Chain the original cause when you translate an exception.

# module drafts

## mod-call-parent-setup-teardown

level: module  
severity: should-fix  
concerns: testing, reliability  
applies_when: A test class overrides setUp, tearDown, setUpClass or tearDownClass in an xUnit-style framework.  
lacks: orgs, Laravel and Django back it; the Python unittest page states no such rule; needs a third org

A test class that overrides `setUp`, `tearDown`, `setUpClass` or `tearDownClass` calls the parent's version.

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
lacks: orgs, Python (PSF) and the Rust Book back it; needs a third org that keeps the entry module to wiring

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
lacks: orgs, IETF is the only org; MDN and the Siemens guideline restate RFC 9110, so they add none; needs two more orgs that require the challenge

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
lacks: orgs, W3C is the only firm backer; Google Cloud Trace and OpenTelemetry only describe propagation; needs two more orgs

Forward `traceparent` and `tracestate` on every outgoing call, keep the incoming trace id, and set a new parent id for each hop.

## svc-boolean-no-is-prefix

level: service  
severity: discuss  
concerns: maintainability  
applies_when: A new API defines a boolean field or query parameter.  
context: server  
lacks: orgs, Google and Microsoft only; needs one more org that drops the "is" prefix on boolean API fields

Name a new boolean field for its state (`enabled`, `required`), not with an `is` prefix.

## svc-logs-tamper-resistant

level: service  
severity: should-fix  
concerns: security, observability  
applies_when: The service writes security-relevant logs or an audit trail.  
context: server  
lacks: orgs, Google and OWASP back it; AWS CloudTrail validation detects tampering but does not say to ship logs off-host; needs a third org that does

Ship logs and audit trails to a store that the logged host cannot alter or delete.

## svc-page-title-per-route

level: service  
severity: should-fix  
concerns: accessibility, usability  
applies_when: An app serves several pages or client-side routes under one HTML shell.  
context: ui  
lacks: held, kept draft by the maintainer; W3C, Mozilla and A11y Project back the Rule

Give every page and every client-side view its own `<title>` that says what it is.

## svc-paginate-by-server-links

level: service  
severity: should-fix  
concerns: correctness, compatibility  
applies_when: The code calls a paginated HTTP or RPC API and reads more than one page.  
context: server  
lacks: orgs, next link has GitHub firm; Microsoft and Zalando state server-side rules only; opaque token has Google and Zalando (cursor opacity); needs more client-side orgs

Fetch the next page only from the link or token the server returned; do not build page numbers or open the token.

## svc-path-normalise-before-authz

level: service  
severity: should-fix  
concerns: security  
applies_when: A proxy, gateway or CDN sits in front of the service and a deny, allow or cache rule matches on the URL path.  
context: server  
lacks: orgs, Envoy and Istio each state the normalise clause; escaped-slash rejection has Envoy only; PortSwigger and Cloudflare describe attacks or features

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
lacks: evidence, Microsoft, Datadog and Google recommend correlation ids in logs; none says every line; needs a source that does

Put the request or trace id on every log line written during a request.

## svc-security-event-logging

level: service  
severity: should-fix  
concerns: security, observability  
applies_when: The service authenticates users.  
context: server  
lacks: held, kept draft by the maintainer

Log every failed authentication with the account name and a timestamp.

## svc-security-headers

level: service  
severity: should-fix  
concerns: security  
applies_when: The service serves HTML pages or sets cookies for browsers over HTTPS.  
context: server  
lacks: held, kept draft by the maintainer

Send `Strict-Transport-Security` on every HTTPS response.

## svc-server-read-timeouts

level: service  
severity: should-fix  
concerns: security, reliability  
applies_when: The service runs its own HTTP server and untrusted clients or networks can reach it.  
context: server  
lacks: orgs, request-read timeout has Cloudflare and Envoy firm; header-read timeout has no firm org; Node, Kestrel, nginx and Apache pages only describe options

Set a header-read timeout and a request-read timeout on a server that faces untrusted clients.

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
lacks: orgs, AWS is the only firm backer; Microsoft covers cache-down fallback only; Fastly and Go singleflight describe coalescing features; needs two more orgs

Cap and coalesce the cache-miss path so an empty cache cannot overwhelm the origin.

## sys-cache-hit-rate-watched

level: system  
severity: should-fix  
concerns: observability, performance, reliability  
applies_when: The change adds a cache, or resizes one, in front of a database or downstream service.  
context: server  
lacks: orgs, both clauses have AWS and Google; Microsoft lists a Cache Hits metric but gives no advice to alert on it; needs one more org that says to alert

Emit a cache hit-rate or memory-use metric and alert on it, so an undersized cache is noticed before it hurts the origin.

## sys-constraint-not-valid

level: system  
severity: should-fix  
concerns: compatibility  
applies_when: A migration adds a CHECK, FOREIGN KEY, or NOT NULL constraint to a large existing table.  
context: data  
lacks: orgs, PostgreSQL is the only firm backer; Django documents the NOT VALID operation and strong_migrations (one author) shows the pattern; needs two more orgs

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
lacks: orgs, AWS and Microsoft state it firm; Kubernetes client-go only states that its election does not fence; needs a third org that says to guard leader work

Make leader work safe if two leaders overlap: make it idempotent, check the lease before acting, and stop when renewal fails.

# codebase drafts

## code-ci-job-pass-rate-threshold

level: codebase  
severity: discuss  
concerns: reliability, process  
applies_when: Auditing how a team keeps its main-branch pipeline and blocking CI jobs trustworthy.  
lacks: orgs, GitLab and Kubernetes back it; Slack's 95% main-branch target is one project's metric (soft); needs one more org that sets a threshold

Set a numeric pass-rate threshold for the pipeline or each blocking job, and act when it falls below it.

## code-documented-setup-runs

level: codebase  
severity: should-fix  
concerns: maintainability, process  
applies_when: Auditing a repo's README or contribution guide.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs that test the setup commands

Keep the setup, build and run commands in the README or contribution guide accurate: they work as written on a clean checkout, and any drift is fixed or reported.

## code-signed-commits-protected

level: codebase  
severity: should-fix  
concerns: security, process  
applies_when: Auditing the branch protection of a repository that ships code or holds release branches.  
lacks: orgs, OWASP requires it; Node.js signs release commits only; GitHub and GitLab document the setting; needs two more orgs that state it as a rule

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
lacks: orgs, Go and RSpec document shuffle flags only; the GitLab and Alloy pages state no order rule on re-fetch; needs orgs that state the rule

Make each test pass in any order, sharing no mutable state with other tests.

# production drafts

## prod-alert-links-runbook

level: production  
severity: should-fix  
concerns: observability, process  
applies_when: A service ships alert rules that page a person.  
lacks: orgs, "link a runbook" has Google and Grafana Labs; Prometheus links consoles only and shares an author with Google; needs one more org

Link each paging alert to a runbook or dashboard that says what to check and do.

## prod-wide-events-bounded-labels

level: production  
severity: should-fix  
concerns: observability  
applies_when: A request handler or job emits telemetry.  
lacks: orgs, one event per request has Honeycomb firm and Stripe soft; the label clause has Prometheus; needs two more orgs for each

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
lacks: orgs, Atlassian is the only firm backer; the Google SRE workbook shows an owner column in an example table only; needs two more orgs

Give every postmortem action one named owner, a due date, and a tracker link.

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
lacks: orgs, the owner clause has Dropbox only; default, removal date and ticket have no company source

Give every new flag an owner, a default, and a removal condition or date, and ticket the removal.

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

## chg-no-special-case-branches

level: change  
severity: should-fix  
concerns: maintainability  
applies_when: The change adds a conditional, flag or nullable mode to code that serves more than one feature.  
lacks: orgs, one vendor's review skill backs it, with no data; needs two more orgs

Put a new case behind its own function or type; do not add a one-off branch to a shared flow.

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

## fn-bounded-read-fails-at-cap

level: function  
severity: should-fix  
concerns: correctness, reliability, security  
applies_when: A function reads a file, a response or a request body through a reader that has a byte limit.  
lacks: evidence, the sources are API, setting and status-code definitions; only OWASP states the practice

When a size cap is reached, return an error; never hand back the first N bytes as if they were the whole input.

## fn-empty-collection-not-none

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A function returns a list, set or map.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Return an empty collection for "nothing found"; return `None` only when absent differs from empty.

## fn-english-identifiers

level: function  
severity: discuss  
concerns: maintainability  
applies_when: The project has a written language policy, or its code may be read by people outside one language group.  
lacks: orgs, PEP 8 and LLVM give the rule and PEP 3131 argues the other way; needs a third org that mandates English

Write identifiers and comments in English, unless the project policy names another language.

## fn-known-keys-get-a-type

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A function takes or returns a dictionary whose keys are fixed and known.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Give a fixed key set a record type (model, dataclass, or typed dict), and use a generic map only for open keys.

## fn-name-intermediate-conditions

level: function  
severity: discuss  
concerns: maintainability  
applies_when: An `if` or `while` joins three or more terms in one expression.  
lacks: evidence, the only backer is a dev.to summary of Ousterhout; needs two orgs that say to name sub-conditions

Name each compound condition by assigning its sub-conditions to booleans that say what they mean.

## fn-no-anonymous-tuples

level: function  
severity: should-fix  
concerns: maintainability  
applies_when: A function returns or passes a tuple whose positions mean different things.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Return a small named record, not a positional tuple, once the fields differ in meaning.

## fn-no-check-then-act-across-await

level: function  
severity: should-fix  
concerns: correctness  
applies_when: Code reads shared state, yields (await, I/O, a lock release), then writes based on the earlier read.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Make check-and-write one atomic operation where the state lives, and never split it across a suspension point.

## fn-no-getattr-for-known-names

level: function  
severity: discuss  
concerns: maintainability  
applies_when: Code reads or writes an attribute or field by a dynamic key when the name is known at write time.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Use plain field access, and reserve dynamic access for genuinely dynamic names.

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
applies_when: A function returns a status, kind or outcome, and callers branch on it.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Return an enum or a tagged type, never a bare string that the caller must compare.

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
lacks: orgs, one blog post on structured concurrency backs it; needs two more orgs

Give every task and handle an owner that waits for it or closes it, on the error path too.

## fn-test-oracle-independent

level: function  
severity: should-fix  
concerns: correctness, testing  
applies_when: A test asserts on a computed value.  
lacks: orgs, Google states "from the requirement"; Microsoft backs "no logic in tests"; one source is person-authored

Take a test's expected value from the requirement, not from the code under test.

# module drafts

## mod-behaviour-lives-with-state

level: module  
severity: discuss  
concerns: maintainability  
applies_when: A service function computes something only from one object's own fields.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Put invariants and calculations over one object on that object, and move logic to a service only when it spans objects or needs an injected collaborator.

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

## mod-deep-modules

level: module  
severity: discuss  
concerns: maintainability  
applies_when: A new class or module is introduced, or an existing interface grows.  
lacks: orgs, Ousterhout is the only backer, and Martin disagrees; needs two more orgs

Prefer a small interface that hides real work, and flag modules whose interface is nearly as complex as their implementation.

## mod-fowler-smells

level: module  
severity: discuss  
concerns: maintainability  
applies_when: A reviewer sees long methods, feature envy, data clumps, primitive obsession, speculative generality, or divergent change.  
lacks: evidence, no Fowler or Beck source; backers are an Ousterhout summary and Google's review guide, mapped by hand

Name the smell, point to the line, and suggest the refactoring; do not file smells as taste.

## mod-mock-at-boundaries-only

level: module  
severity: should-fix  
concerns: testing  
applies_when: A test uses mocks, patches or fakes.  
lacks: evidence, Airbnb mocks services in load tests and Cabify runs a real gRPC server; neither states the Rule

Mock only at the process boundary (HTTP, DB, cloud, clock, I/O).

## mod-no-wire-types-in-public-api

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: A module exposes a public function, class or re-export.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

Expose domain types in a module's public interface, and keep transport, storage and framework types behind it.

## mod-no-wrong-abstraction

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: A shared helper or base class has gained flags or conditionals so different callers can bend it.  
lacks: orgs, Metz and Dodds back inlining; the re-split remedy has no third org, and the Counterpoint still cites an unsourced count

Inline an abstraction that has grown flags for its callers, then re-split it.

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

## svc-page-title-per-route

level: service  
severity: should-fix  
concerns: accessibility, usability  
applies_when: An app serves several pages or client-side routes under one HTML shell.  
context: ui  
lacks: held, kept draft by Pablo's call; W3C, Mozilla and A11y Project back the Rule

Give every page and every client-side view its own `<title>` that says what it is.

## svc-rate-limit-by-cost

level: service  
severity: should-fix  
concerns: performance, reliability  
applies_when: One API or store serves requests whose cost differs by orders of magnitude, such as GraphQL queries, scans next to point reads, or bulk endpoints.  
context: server  
lacks: evidence, Shopify, GitHub and Airbnb describe cost-based limits; none recommends it, and Uber dropped a bytes-based quota

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

## sys-constraint-not-valid

level: system  
severity: should-fix  
concerns: compatibility  
applies_when: A migration adds a CHECK, FOREIGN KEY, or NOT NULL constraint to a large existing table.  
context: data  
lacks: orgs, PostgreSQL docs are the only backer; needs two more orgs that add constraints in two steps

Add the constraint `NOT VALID`, then run `VALIDATE CONSTRAINT` in a separate step, and never leave the VALIDATE out.

## sys-leader-two-leaders

level: system  
severity: should-fix  
concerns: reliability  
applies_when: A job runs only on an elected leader or lease holder.  
lacks: orgs, AWS is the only backer; needs two more orgs

Make leader work safe if two leaders overlap: make it idempotent, check the lease before acting, and stop when renewal fails.

# codebase drafts

## code-ai-pr-disclosure

level: codebase  
severity: should-fix  
concerns: process  
applies_when: A pull request was written in whole or part by an AI tool.  
lacks: orgs, disclosure has the Linux kernel and Ghostty; needs a third org that asks for it and for an author who can explain the code

Disclose AI assistance in the PR, and have a human author who can explain and defend every changed line without the tool.

## code-documented-setup-runs

level: codebase  
severity: should-fix  
concerns: maintainability, process  
applies_when: Auditing a repo's README or contribution guide.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs that test the setup commands

Keep the setup, build and run commands in the README or contribution guide accurate: they work as written on a clean checkout, and any drift is fixed or reported.

## code-file-lines-ceiling

level: codebase  
severity: discuss  
concerns: maintainability, process  
applies_when: Auditing a repo for files that have grown past comprehension.  
lacks: evidence, backers are a dev.to summary and a blog post; no org states a file-length ceiling or the 1,000-line figure

Keep every hand-written source file under about 1,000 lines unless it has a listed exception, and split larger files by knowledge owned, not by execution order.

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

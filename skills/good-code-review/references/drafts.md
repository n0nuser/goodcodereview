# Draft cards

A draft card is not vetted. Report a `FAIL` of one under Draft findings, at `should-fix` at most, never in the ledger or the verdict. A draft `change`, `incident`, or `production` card applies only to a diff, an incident, or a release.

# change drafts

## chg-agent-grounded-code

level: change  
severity: should-fix  
concerns: maintainability, process  
applies_when: The change was written fully or partly by an AI agent.  
lacks: orgs, only an arXiv package-hallucination study backs checking every import and call; needs two more orgs

Verify that every import and external call the agent wrote exists with that signature.

## chg-agent-independent-review

level: change  
severity: should-fix  
concerns: process  
applies_when: An agent wrote the change, and an agent or the same session is asked to review it.  
lacks: orgs, a person's sign-off has Stripe and Dropbox; the fresh-context reviewer option has 0 orgs; needs one more firm org or that option cut

Get sign-off from a person or a fresh-context reviewer who has the spec but not the author's reasoning; self-review by the writing session does not count.

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

## chg-approval-tied-to-patch

level: change  
severity: should-fix  
concerns: process  
applies_when: A review approval or verification result exists and the branch has been pushed or rebased since.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

Treat an approval or verification verdict as current only if the patch is unchanged: compare `git patch-id` at the verdict commit with the current head. If the patches differ only in tests, docs, or lint config, the verdict can stand when the built output is the same; any other difference needs a fresh check.

## chg-bot-approval-not-human

level: change  
severity: should-fix  
concerns: process, security  
applies_when: Branch protection or policy requires a human approval and a bot or agent can also approve.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that bar bot or agent approvals from a required human review

Do not let a bot or agent approval satisfy a required human approval.

## chg-chestertons-fence

level: change  
severity: should-fix  
concerns: maintainability, process  
applies_when: The change removes, rewrites or "simplifies" odd-looking existing code, or rewrites a module.  
lacks: orgs, only Feathers backs a characterization test before a rewrite; Spolsky backs not rewriting from scratch

Add a characterization test before rewriting code you do not understand.

## chg-delete-legacy-after-migration

level: change  
severity: should-fix  
concerns: compatibility, maintainability  
applies_when: The change adds a new API, path or config and every caller lives in this repo.  
context: data  
lacks: orgs, "in the same change" has cursor/plugins and Stripe; Dropbox, GitHub, Shopify and Slack delete in a later step

When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.

## chg-devex-breaking-config

level: change  
severity: should-fix  
concerns: compatibility, process  
applies_when: The change renames an environment variable, remaps a port, moves a secret source, or adds a step needed to run or build the project.  
lacks: orgs, one vendor's review skill (cursor/plugins) backs it; needs two more orgs

Flag a change that renames or removes an environment variable, moves a secret, or remaps a port as breaking for developers and operators, and update every place that documents or sets it.

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

## chg-migration-add-column-rewrite

level: change  
severity: should-fix  
concerns: compatibility  
applies_when: A migration adds a column to a large PostgreSQL table.  
context: data  
lacks: orgs, PostgreSQL docs are the only backer; needs two more orgs

Add the column nullable or with a constant default, then fill volatile, computed, or identity values in batches.

## chg-name-attack-surface

level: change  
severity: should-fix  
concerns: security, process  
applies_when: The change adds an endpoint, input parser, file upload, dependency, permission, secret or outbound call.  
lacks: orgs, no source says to list the attack surface in the description; OWASP and Mozilla back only a threat-model trigger

List any new attack surface in the description.

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

## chg-no-silenced-diagnostics

level: change  
severity: should-fix  
concerns: correctness, maintainability, process  
applies_when: The diff adds a suppression (lint ignore, type ignore, skipped test, swallowed error) or deletes a failing check.  
lacks: orgs, reason and ticket on each suppression has cursor/plugins only; Stripe tracked suppressions as a group

Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.

## chg-no-special-case-branches

level: change  
severity: should-fix  
concerns: maintainability  
applies_when: The change adds a conditional, flag or nullable mode to code that serves more than one feature.  
lacks: orgs, one vendor's review skill backs it, with no data; needs two more orgs

Put a new case behind its own function or type; do not add a one-off branch to a shared flow.

## chg-proto-no-field-type-change

level: change  
severity: should-fix  
concerns: compatibility  
applies_when: The diff changes an existing field's type, default, label or name in a `.proto` file.  
lacks: orgs, "no field type change" has Google only; Uber and Cabify back renumbering and the buf breaking gate instead

Never change the type of a protobuf field, switch it between repeated and scalar, or rename it while any consumer reads JSON or text format; add a new field instead.

## chg-proto-reserve-removed-fields

level: change  
severity: should-fix  
concerns: compatibility  
applies_when: The diff deletes a field or enum value from a `.proto` message or enum.  
lacks: orgs, protobuf.dev is the only backer; needs two more orgs that require reserved on removal

When you delete a protobuf field or enum value, add `reserved` for its number and name in the same change, and never reuse a number.

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

## chg-rollback-path

level: change  
severity: should-fix  
concerns: reliability  
applies_when: The change deploys schema, data, config or behaviour that is costly to undo.  
lacks: orgs, only Anthropic (a vendor) says to state the undo in the change description; Google SRE backs canary rollback, not the statement

State in the description how to undo the change.

## chg-sensitive-paths-human-owner

level: change  
severity: should-fix  
concerns: security, process  
applies_when: The change touches code or config for auth, billing, CI or release workflows.  
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that name human owners for auth, billing, CI and release paths

Name a human owner in CODEOWNERS for auth, billing, CI and release paths, and require that owner's approval.

## chg-ui-change-screenshots-and-keyboard-pass

level: change  
severity: should-fix  
concerns: accessibility, usability, process  
applies_when: The change alters markup, styles, or behaviour a user sees or operates.  
context: ui  
lacks: orgs, reporting the keyboard pass has two PR templates; the 200% zoom clause has W3C only

A UI change shows before-and-after screenshots and says what a keyboard-only pass and a 200% zoom check found on the changed screens.

# function drafts

## fn-atomic-related-updates

level: function  
severity: should-fix  
concerns: correctness  
applies_when: One operation writes to two or more places that must agree (rows, tables, stores, files).  
lacks: orgs, only one vendor's review skill backs it; the all-or-nothing principle has no cited org

Make related writes succeed or fail together.

## fn-bool-arg-at-callsite

level: function  
severity: discuss  
concerns: maintainability  
applies_when: A call passes a literal `True` or `False` for a parameter.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Replace a boolean flag argument with an enum, keyword-only argument or two functions.

## fn-bounded-read-fails-at-cap

level: function  
severity: should-fix  
concerns: correctness, reliability, security  
applies_when: A function reads a file, a response or a request body through a reader that has a byte limit.  
lacks: evidence, the sources are API, setting and status-code definitions; only OWASP states the practice

When a size cap is reached, return an error; never hand back the first N bytes as if they were the whole input.

## fn-comments-survive-context

level: function  
severity: should-fix  
concerns: maintainability  
applies_when: A comment or TODO says "currently", "for now", "not yet", "see the PR" or promises future work.  
lacks: orgs, Google's three style guides back a dated or event-based TODO; no second org found that bans "currently" or "for now" comments

Write comments that remain true without outside context: no "currently", "for now" or "see the PR", and give a TODO the date or event that ends it.

## fn-distinct-types-for-ids

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A function takes two or more arguments of one primitive type that mean different things (ids, amounts, units).  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

Give arguments with different meanings distinct types, so a call that swaps them fails to type-check.

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

## fn-guard-uri-decoding

level: function  
severity: should-fix  
concerns: reliability, correctness  
applies_when: Code calls `decodeURIComponent` or `decodeURI` on a query parameter, a hash, a path segment or other input a user controls.  
context: ui, server  
lacks: orgs, Mozilla (MDN) and the Node.js docs back it; needs one more org that guards or avoids a throwing decode on user input

Wrap `decodeURIComponent` on user input in a `try`/`catch`, or parse with `URLSearchParams`, so that a malformed `%` sequence cannot throw.

## fn-known-keys-get-a-type

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A function takes or returns a dictionary whose keys are fixed and known.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Give a fixed key set a record type (model, dataclass, or typed dict), and use a generic map only for open keys.

## fn-link-url-scheme-allowlist

level: function  
severity: should-fix  
concerns: security  
applies_when: A URL taken from remote JSON, a query parameter or stored data is written to `href`, `src`, `location` or `window.open`.  
context: ui  
lacks: orgs, OWASP and Angular (Google) back it; needs one more org that checks the scheme before data reaches href or src

Parse a URL that comes from data and allow only `https:` (and `http:` or `mailto:` where needed) before you set it as a link target.

## fn-mask-credentials-in-output

level: function  
severity: should-fix  
concerns: security, usability  
applies_when: A CLI command, admin page or debug view prints stored configuration that can include tokens, API keys, or URLs with embedded secrets.  
context: cli  
lacks: orgs, GitHub and Django state masking for display; GitLab covers CI logs and OWASP covers logs, so the list/show clause has two organisations

Mask credentials in list, show and debug output (keep only the last four characters), and print a full value only behind an explicit flag.

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

## fn-no-magic-values

level: function  
severity: should-fix  
concerns: maintainability  
applies_when: A literal string or number carries meaning the reader must guess (status codes, mode names, limits).  
lacks: orgs, Google's review guide is the only backer; needs two more orgs

Give every meaningful literal a name: an enum member or a constant.

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

## fn-specific-exceptions-only

level: function  
severity: should-fix  
concerns: correctness  
applies_when: Code catches exceptions in business logic.  
lacks: orgs, the Go wiki and an Ousterhout summary back it; needs a third independent org

Catch only the specific exception you can handle in business code.

## fn-test-oracle-independent

level: function  
severity: should-fix  
concerns: correctness, testing  
applies_when: A test asserts on a computed value.  
lacks: orgs, Google states "from the requirement"; Microsoft backs "no logic in tests"; one source is person-authored

Take a test's expected value from the requirement, not from the code under test.

## fn-variants-as-tagged-union

level: function  
severity: should-fix  
concerns: maintainability  
applies_when: A type or function models a value that is one of several variants or states.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

Model variants as a tagged union, and make every switch over it fail the build when a variant is unhandled.

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

## mod-inject-boundary-collaborators

level: module  
severity: should-fix  
concerns: testing, maintainability  
applies_when: A class uses a database, HTTP, cloud or clock collaborator.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Inject boundary collaborators through the constructor; do not construct them inside or reach for a global.

## mod-internals-unreachable

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: A module has an intended public surface and internal files or symbols.  
lacks: orgs, one vendor's guidance (cursor/plugins) backs it; needs two more orgs

Make a module's internals unimportable from outside it, and have a check fail the build when a caller reaches in.

## mod-layers-point-inward

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: The codebase has separable transport, logic, and outbound-boundary code.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Make dependencies point inward: surface, then logic, then boundary.

## mod-mock-at-boundaries-only

level: module  
severity: should-fix  
concerns: testing  
applies_when: A test uses mocks, patches or fakes.  
lacks: evidence, Airbnb mocks services in load tests and Cabify runs a real gRPC server; neither states the Rule

Mock only at the process boundary (HTTP, DB, cloud, clock, I/O).

## mod-no-import-side-effects

level: module  
severity: should-fix  
concerns: testing, maintainability  
applies_when: A module does anything at import or load time other than defining names.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Keep I/O at the edges: importing a package must not touch the network, read files, or read the environment.

## mod-no-logic-in-constructors

level: module  
severity: should-fix  
concerns: correctness, testing  
applies_when: A constructor does work beyond assigning its arguments.  
lacks: orgs, only the author's own Python review guide backs it; no independent org

Assign only in constructors, and put I/O, parsing, and heavy computation in a named factory.

## mod-no-utils-grab-bag

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: The diff adds or grows a module named `utils`, `helpers`, `common`, or `misc`.  
lacks: evidence, the only backer is a dev.to summary of Ousterhout; needs two orgs that say to name helpers after a concept

Put a helper in the module that owns the concept, or in a new module named after the concept.

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

## mod-one-name-per-concept

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: The change introduces or reuses names for domain concepts.  
lacks: evidence, Netflix backs the converse, one concept per name; Slack's aliases are narrow; no org states the Rule

Use one name for one concept across the codebase.

## mod-prefer-sync-api

level: module  
severity: discuss  
concerns: correctness  
applies_when: A module wraps protocol, parsing or business logic and offers it to callers that may be sync or async.  
lacks: evidence, the sans-io and async-pressure posts are opinion and neither states this as a rule; the card combines them

Keep logic in plain synchronous functions with no I/O, and add async wrappers at the edge only.

## mod-proto-enum-zero-unspecified

level: module  
severity: should-fix  
concerns: compatibility  
applies_when: A `.proto` file defines an enum.  
lacks: orgs, the _UNSPECIFIED name has Google only; a zero value with no meaning has Google and Dropbox

Give every protobuf enum a zero value named `<ENUM>_UNSPECIFIED` with no real meaning.

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

## svc-api-cache-control

level: service  
severity: should-fix  
concerns: performance  
applies_when: A service returns responses that a browser, CDN, gateway or client library may cache.  
context: server  
lacks: orgs, IETF and Zalando back it; needs a third org

Set an explicit `Cache-Control` on every response a cache may store, use `private` or `no-store` for user-specific data, and add `Vary` for any request header that changes the body.

## svc-api-contract-tests

level: service  
severity: should-fix  
concerns: compatibility, testing  
applies_when: A service calls, or is called by, another service owned by a different team or deployed on its own schedule.  
context: server  
lacks: orgs, Pact is the only backer; OpenAPI does not back contract tests and provider verification is not asserted

Run a contract test for each cross-service call, derived from the consumer's real requests, and fail the provider's build when it breaks one.

## svc-api-documented-errors

level: service  
severity: should-fix  
concerns: correctness, compatibility  
applies_when: A service has an OpenAPI description, or callers depend on its error responses.  
context: server  
lacks: orgs, OpenAPI requires one response per operation; the stricter rule is Zalando's alone

Document every error status each operation can return, with a schema and one example.

## svc-api-naming-consistent

level: service  
severity: discuss  
concerns: maintainability  
applies_when: A service defines JSON fields, query parameters, headers or path segments for an HTTP API.  
context: server  
lacks: orgs, Zalando and Microsoft back it, and they disagree on casing; needs a third org that asks for consistency

Use one casing convention per location (fields, query parameters, headers, paths) across the whole API, and state it in the API guide.

## svc-api-problem-json

level: service  
severity: should-fix  
concerns: compatibility  
applies_when: A service returns errors from an HTTP API to other services or to clients.  
context: server  
lacks: orgs, IETF and Zalando back it; needs a third org

Return errors as `application/problem+json` with a `status` that equals the HTTP status, and leave stack traces and internal detail out.

## svc-api-retry-after

level: service  
severity: should-fix  
concerns: reliability  
applies_when: A service answers 429 or 503 to HTTP callers.  
context: server  
lacks: orgs, IETF and Zalando back it; needs a third org

Send `Retry-After` on every 429 and 503, and set it no earlier than the time capacity returns.

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

## svc-api-specific-status-codes

level: service  
severity: should-fix  
concerns: compatibility  
applies_when: A service returns HTTP responses that callers or intermediaries interpret by status code.  
context: server  
lacks: orgs, IETF and Zalando back it; needs a third org

Return the most specific status code that fits: 201 with `Location` for a create, 405 with `Allow` for a wrong method, and a 4xx or 5xx for any failure.

## svc-api-trace-context

level: service  
severity: should-fix  
concerns: observability  
applies_when: A service calls another service over HTTP while handling a request.  
context: server  
lacks: orgs, W3C is the only backer; needs two more orgs that forward trace headers on every call

Forward `traceparent` and `tracestate` on every outgoing call, keep the incoming trace id, and set a new parent id for each hop.

## svc-async-content-reserves-space

level: service  
severity: should-fix  
concerns: usability, performance  
applies_when: A page loads images, embeds, fonts, ads, or fetched content after the first paint.  
context: ui  
lacks: orgs, injected content and ads have Google only; the image-dimensions part has Google and Mozilla

Reserve the space for late-loading content with set dimensions or an aspect ratio, so nothing already on screen moves.

## svc-authn-by-default

level: service  
severity: should-fix  
concerns: security  
applies_when: The service has routes that need a signed-in user next to routes that are public.  
context: server  
lacks: evidence, only Microsoft and Spring say why auth by default; Django, Rails and NestJS describe the default without a reason

Require authentication on every route by default, and mark each public route by name.

## svc-best-effort-optional-deps

level: service  
severity: should-fix  
concerns: reliability, observability  
applies_when: The critical path of a request or a job calls a dependency whose data the product can do without, such as enrichment, recommendations, analytics, or a rate-limit control plane.  
lacks: orgs, best-effort calls have Netflix, Uber and Cabify; counting every fallback has Cabify only

Give each call to a non-critical dependency a short budget and a default, so its failure degrades the result instead of failing the critical path, and count every fallback.

## svc-circuit-breaker-bulkhead

level: service  
severity: should-fix  
concerns: reliability  
applies_when: A service calls several dependencies from shared pools, or retries a dependency that may be down.  
lacks: orgs, "per dependency" has Microsoft only; needs two more orgs that limit concurrency per downstream

Give each critical dependency its own concurrency limit.

## svc-dlq

level: service  
severity: should-fix  
concerns: reliability  
applies_when: The code consumes from a queue or stream.  
context: server  
lacks: evidence, Dropbox's dead-letter queue is a proposal, not a practice; needs a third org that runs it

Give every consumer queue a dead-letter queue and a way to replay its messages after the fix.

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

## svc-saga-steps

level: service  
severity: should-fix  
concerns: reliability, correctness  
applies_when: A business operation spans services, each with its own database, coordinated as a saga.  
context: server  
lacks: orgs, Azure is the only backer; needs two more orgs that require idempotent steps and compensations

Make steps after the pivot idempotent and retryable, and make every compensation idempotent with a failure path.

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

## svc-stream-dont-materialise

level: service  
severity: should-fix  
concerns: performance  
applies_when: A handler reads, transforms, or returns a result whose size depends on the data (files, query results, response bodies).  
lacks: orgs, the Node.js backpressure guide is the only backer, and its claim is Node-specific

Process large results as a stream with backpressure; do not load them whole into memory.

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

## sys-cells-limit-blast-radius

level: system  
severity: discuss  
concerns: reliability  
applies_when: Many tenants, regions, or product surfaces share one cluster, control plane, or data store.  
lacks: evidence, Netflix and Slack run cells; Airbnb's multi-cluster store and Cloudflare's postmortem describe failure domains, not cells

Split shared infrastructure into independent cells, each with its own control plane and storage, and route each tenant or request to one cell, so one failure stops only that cell.

## sys-constraint-not-valid

level: system  
severity: should-fix  
concerns: compatibility  
applies_when: A migration adds a CHECK, FOREIGN KEY, or NOT NULL constraint to a large existing table.  
context: data  
lacks: orgs, PostgreSQL docs are the only backer; needs two more orgs that add constraints in two steps

Add the constraint `NOT VALID`, then run `VALIDATE CONSTRAINT` in a separate step, and never leave the VALIDATE out.

## sys-health-liveness-readiness

level: system  
severity: should-fix  
concerns: reliability  
applies_when: A service exposes a health endpoint used by a load balancer, an orchestrator, or auto-replacement.  
lacks: orgs, AWS is the only backer; needs two more orgs

Wire load balancers and restarters to liveness and local checks only, never to shared-dependency checks.

## sys-index-concurrently

level: system  
severity: should-fix  
concerns: compatibility  
applies_when: A migration creates an index on an existing large or busy table.  
context: data  
lacks: orgs, PostgreSQL and GitLab back it; needs a third org

Create indexes with `CONCURRENTLY`, outside a transaction block, and handle a failed build that leaves an INVALID index.

## sys-leader-two-leaders

level: system  
severity: should-fix  
concerns: reliability  
applies_when: A job runs only on an elected leader or lease holder.  
lacks: orgs, AWS is the only backer; needs two more orgs

Make leader work safe if two leaders overlap: make it idempotent, check the lease before acting, and stop when renewal fails.

## sys-migration-lock-timeout

level: system  
severity: should-fix  
concerns: compatibility  
applies_when: A migration runs ALTER TABLE on a busy PostgreSQL table.  
context: data  
lacks: orgs, PostgreSQL and GitLab back it; the lock-queue reason is inferred; needs a third org

Set `lock_timeout` for the migration session and retry on timeout.

# codebase drafts

## code-a11y-check-in-ci

level: codebase  
severity: should-fix  
concerns: accessibility, testing  
applies_when: The repo builds a web UI and has an automated test suite.  
context: ui  
lacks: held, kept draft by Pablo's call; no org backs failing the build on a violation

Run an automated accessibility check, such as axe on rendered pages, in the automated tests, and fail the test on a violation.

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

## code-flaky-test-quarantine

level: codebase  
severity: should-fix  
concerns: testing, process  
applies_when: Auditing how the codebase handles tests that pass and fail on the same code.  
lacks: orgs, quarantine with owner and ticket has Dropbox and Shopify; rerun-verified return to the gate has Dropbox only

Report every test that passes only on retry, move it to a quarantine with a named owner and a ticket, and return it to the merge gate only after it passes many reruns.

## code-release-gated-on-ci

level: codebase  
severity: should-fix  
concerns: reliability, process  
applies_when: Auditing a workflow or pipeline that publishes a release when a tag is pushed.  
lacks: evidence, GitHub and GitLab pages describe the feature; only Kubernetes states the practice (red jobs, no release); needs two more orgs that gate releases on CI

Make a release or publish job depend on the checks passing for the tagged commit, never on the tag alone.

## code-scoped-validation-loop

level: codebase  
severity: discuss  
concerns: testing, process  
applies_when: Auditing how a contributor checks a small change.  
lacks: orgs, one vendor's local-loop review backs it; needs two more orgs that document a scoped local command

Document a command that checks one package or path, with readable output, so a small change does not need the full-repo run.

# production drafts

## prod-a11y-audit-before-launch

level: production  
severity: should-fix  
concerns: accessibility, usability  
applies_when: A new UI service or a major redesign is about to open to the public.  
context: ui  
lacks: orgs, "before a public launch" has GOV.UK only; the audit content has GOV.UK, W3C and Deque

Before a public launch, run an accessibility audit against WCAG 2.2 AA that includes assistive technology, and link the report in the launch checklist.

## prod-shadow-compare-before-cutover

level: production  
severity: should-fix  
concerns: correctness, reliability  
applies_when: Reads, writes, or a pipeline's traffic move from an old system to a new one, such as a new data store, a database upgrade, or a rewritten service.  
context: data  
lacks: evidence, Netflix, Stripe, Airbnb and GitHub describe doing it; none recommends it as a practice for others

Before you move traffic to a new system, run it beside the old one on live or captured production traffic, diff the results, and cut over only when every mismatch is fixed or explained.

## prod-slo-error-budget

level: production  
severity: discuss  
concerns: reliability, observability  
applies_when: A service has users or dependents who rely on its availability.  
lacks: orgs, gating releases on the error budget has no backing row

Define an SLO with an indicator and window, and use its remaining error budget to gate risky releases.

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

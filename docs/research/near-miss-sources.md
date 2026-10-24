# Near-miss sources: a third independent source for nine cards

Fetched 2026-10-24 through WebFetch (a small model summarises the page), so every row is paraphrase. Each row gives the URL, what it says, and the card whose Rule it backs. Pages from one org count once. A source counts only if it backs the Rule line, not just the Why. The "Findings" section at the end lists where a source shows a Rule is overstated.

## 1. svc-timeouts

1. https://grpc.io/docs/guides/deadlines/. Set an explicit, realistic deadline on every client call. gRPC sets none by default, so a call can wait forever. Pick the value from expected network latency and server processing time, ideally checked under load. A server that calls another server can pass the caller's deadline down. gRPC sends the remaining time, not an absolute timestamp, so unsynchronised clocks do not matter. Java and Go propagate by default; C++ needs it turned on. Backs both halves of `svc-timeouts` (explicit bound, derived from the caller's deadline). Strong primary.
2. https://sre.google/sre-book/addressing-cascading-failures/ (section "Latency and Deadlines"). Always set a deadline. With none, or a very long one, stale work holds resources after the client gave up. Servers should check the remaining time before each stage and skip work the client has abandoned. Deadline propagation hands the remaining time down the call tree, so each hop shares one cutoff instead of a fresh hardcoded timeout; leave a small margin for transit. Backs `svc-timeouts`. Strong primary.

Count: 2 before (asyncio docs, Azure) -> 4 after (+ gRPC, + Google SRE).

## 2. svc-retry-policy

3. https://sre.google/sre-book/addressing-cascading-failures/ (section "Retries"). Cap retries per request and never retry forever. Use randomised exponential backoff with jitter so clients do not synchronise. Set a server-wide retry budget and fail the request once it runs out. Retry at one layer only, because stacked layers multiply attempts onto the database. Do not retry permanent errors or malformed requests. Backs every clause of the `svc-retry-policy` Rule and its "one layer" line in the Why. Strong primary.
4. https://sre.google/sre-book/handling-overload/. Allow retries only while they stay under about 10% of a client's requests, which bounds retry-driven growth near 1.1x. A request gets at most three attempts, then the failure goes back to the caller. Retry only at the layer directly above the rejecting one, and use an "overloaded, don't retry" error to stop retry explosions. Backs the budget in the `svc-retry-policy` Counterpoint, which the card calls a team convention. Same org as item 3, so it counts once.

Count: 2 before (Azure, AWS) -> 3 after (+ Google SRE).

## 3. chg-reuse-before-write

5. https://www.kernel.org/doc/html/latest/process/coding-style.html (section 18, "Don't re-invent the kernel macros"). `include/linux/` already holds helpers such as `ARRAY_SIZE()`, `sizeof_field()`, and type-checked `min()` and `max()`. Use them instead of writing a variant, and look in the headers for others. Backs `chg-reuse-before-write` (look for an existing helper before adding one). Primary, from a project that enforces it in review. It names a few helpers; it does not describe a search procedure.
6. https://refactoring.com/catalog/replaceInlineCodeWithFunctionCall.html. Fowler's catalog entry for swapping hand-written code for a call to a function that already exists. The fetch returned only the title and a before/after example, not the motivation text. Weak. Not added to `borrowed_from`.

Count: 2 before (Orosz, Ousterhout secondary) -> 3 after (+ Linux kernel docs).

## 4. chg-match-codebase-pattern

7. https://peps.python.org/pep-0008/ (section "A Foolish Consistency is the Hobgoblin of Little Minds"). Consistency with the guide matters, consistency within a project matters more, and consistency within one module or function matters most. Valid reasons to depart: following the rule would hurt readability; matching nearby code that already breaks the rule is acceptable; old code needs no change unless you touch it for another reason; do not break compatibility just to comply. Backs both the Rule (follow the nearby pattern) and the Counterpoint (consistency does not freeze a bad pattern). Strong primary, independent of Google.
8. https://google.github.io/styleguide/cppguide.html (Goals, "Consistency"). One style across the codebase lets tools and engineers focus on more important things. It applies most strongly within a file or a closely related set of interfaces, and it is a tie-breaker, not a reason to keep an old style without weighing the newer one. Same org as Google eng-practices, so it counts once with that source. Consistent with the card's Counterpoint. Not added to `borrowed_from`.

Count: 2 before (Google, Orosz) -> 3 after (+ PEP 8).

## 5. chg-abstraction-needs-two-callers (card deleted in ce768ba)

9. https://sandimetz.com/blog/2016/1/20/the-wrong-abstraction. (now backs `mod-no-wrong-abstraction`) Duplication is far cheaper than the wrong abstraction. When a new need almost fits a shared abstraction, people add a parameter and a conditional, and each variant makes the shared code harder to read and easier to break. The remedy: inline the code back into each caller, keep only what each caller uses, drop the parameters, and extract again from what the code now shows. Backs the Why and the FAIL/PASS pair of `chg-abstraction-needs-two-callers`, including "inline it and re-split". Strong primary.
10. Rule of Three (Don Roberts, in Fowler's *Refactoring*): tolerate the second copy and extract at the third. The search found the book's wording only through Wikipedia and PDF mirrors, no public primary page. Not read and not added.

Count: 2 before (AHA/Dodds, Tef) -> 3 after (+ Metz). See Findings: Dodds's post builds on Metz, and no source states the number "two".

## 6. svc-idempotency-key

11. https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/ (draft 08 at fetch time, an Internet-Draft, not a standard). A client may send an `Idempotency-Key` on any request to ask for once-only effect, with a unique key per request. Reusing a key with a different payload should get HTTP 422. The draft sets no retention period; a server that purges keys should publish its expiry policy. Backs the key mechanism and the Counterpoint's retention remark. It does not require storing and replaying the first response (see Findings).
12. https://docs.stripe.com/api/idempotent_requests. The client generates a unique key (a V4 UUID is suggested, up to 255 characters). For API v1, Stripe saves the status code and body of the first request after execution begins and returns the saved response on retries, including 500 errors. It compares parameters and errors if they differ. Keys can be pruned after at least 24 hours. Requests that fail validation or hit a concurrent in-flight request are not saved and can be retried. `POST` takes keys; `GET` and `DELETE` do not need them. Backs the full Rule, including "stores and replays the first result". Strong primary. The v2 API works differently: it finishes failed work instead of replaying.
13. Brandur on idempotency keys (candidate in the brief). Not searched: items 11 and 12 already take the card past three orgs.

Count: 1 org before (two Azure pages) -> 3 orgs after (+ IETF draft, + Stripe).

## 7. sys-load-shedding-bounded-queues

14. https://sre.google/sre-book/addressing-cascading-failures/ (sections "Queue Management", "Load Shedding and Graceful Degradation"). Queues add memory use and latency. For steady traffic, keep the queue small relative to the thread pool (around half or less) so the server rejects excess early; bursty traffic may need sizing from burst size and frequency. Shed load by rejecting early, for example HTTP 503 above an in-flight limit. FIFO to LIFO, or CoDel, drops requests the user probably abandoned. Backs the Rule (bound the queue, reject excess cheaply) and the "old items are served after callers gave up" Why. Strong primary.
15. https://sre.google/sre-book/handling-overload/. Accept only what can be processed and reject the rest. Rejecting should cost less than serving, but for some services it costs nearly as much, and adaptive client-side throttling then rejects locally once requests reach about twice accepts. The chapter does not discuss bounded queues. Same org as item 14. Backs the "shedding must be cheap" line in the Counterpoint.
16. https://github.com/Netflix/concurrency-limits. The limiter finds how many concurrent requests a service handles before a queue builds and latency rises. The simple strategy tracks in-flight requests and rejects new ones at once when the limit is reached; a gRPC server rejects with `UNAVAILABLE` to keep latency low. The README does not talk about unbounded queues by name. Backs "reject excess cheaply" and the queue-latency link. Medium: it supports the limit-and-reject half of the Rule through a concurrency limiter, not a queue constructor.

Count: 1 org before (two AWS pages) -> 3 orgs after (+ Google SRE, + Netflix). The Netflix row backs only half the Rule.

## 8. sys-secrets-and-errors

17. https://cwe.mitre.org/data/definitions/636.html (CWE-636, "Not Failing Securely"). Describes a product that, on an error, falls back to a less secure state such as the most permissive access settings, often to "fail functional" and cut administration. It says safe defaults should govern how a product reacts to failure. It does not write out a deny-by-default rule. Backs the Rule's fail-closed line. Medium.
18. https://cwe.mitre.org/data/definitions/209.html (CWE-209). Error messages can reveal file paths, SQL structure, and private data. Mitigations: show the minimum detail useful to the audience, log detail but protect the logs and keep passwords out of them, handle exceptions internally, remove debug output from production, use default error pages that leak nothing. Backs the error-leak half of the Why. Same org as item 17, so both count once.
19. https://12factor.net/config. Credentials are config. Config must be strictly separate from code, and hardcoding it in source is a violation. Store it in environment variables, which are easy to change per deploy and unlikely to be committed by accident. Test: could the codebase be open-sourced now without leaking credentials. Backs the secrets-in-source half of the Why and the `API_KEY = env["API_KEY"]` PASS line. This is the only public source for that half; it does not back the Rule line.
20. https://web.mit.edu/Saltzer/www/publications/protection/Basic.html (the principle "fail-safe defaults", credited on the page to Glaser, 1965; the document is Saltzer and Schroeder, 1975). Base access decisions on granted permission, so the default is no access. A mistake then usually refuses access, which is safe and quickly noticed, while a mistake in an exclusion-based design more often grants access unnoticed. Backs the Rule's fail-closed line. Strong, primary, academic, independent of OWASP and MITRE. The fetch gave no author line; the attribution to Saltzer and Schroeder comes from the document's known title, not from the fetched text.

Count: 1 org before (OWASP Top 10 and ASVS) -> 3 orgs after for the fail-closed Rule line (+ MITRE CWE, + Saltzer and Schroeder). 12factor adds a fourth org for the secrets half, which the Rule line does not state.

## 9. sys-migration-expand-contract

21. https://stripe.com/blog/online-migrations. Four phases for changing a data model online: dual write, switch reads, switch writes, remove old data. The team created the new table and began dual writing first, then ran the backfill as its own step. The backfill identified records offline (a Hadoop job) to spare the production database, copied them with a multi-threaded process, and re-ran the identification job to confirm nothing was missed. Backs the Rule (backfill separate from the schema change) and the staged PASS. Strong primary (vendor engineering blog).
22. https://github.com/ankane/strong_migrations. A backfill in the same transaction as a table-altering change can hold the table lock for the whole backfill. Batch the updates, throttle between batches, and run the backfill outside a transaction, in a separate migration or console. Dropping a column: add it to `ignored_columns`, deploy, drop in a migration, deploy, then remove the `ignored_columns` line. Renaming: create a new column, write to both, backfill, move reads, stop writing the old column, then drop it. Backs the Rule and the N / N+1 / N+2 PASS directly. Strong primary (widely used Rails tool, single maintainer).

Count: 1 org before (two GitLab pages) -> 3 orgs after (+ Stripe, + strong_migrations). Rails Guides and Postgres docs were in the brief; neither was needed.

## Findings

- `svc-idempotency-key` Rule overstated against the IETF draft. The Rule says the server "stores and replays the first result". The draft (item 11) says a retry should get a response consistent with the request having completed, and does not require caching the original response. Stripe v1 (item 12) and the card's own PASS do replay. The Rule is backed by Stripe alone for the replay clause; Azure backs retry safety in general. If the Rule must be backed three times on the replay clause, soften it to "respond as the first attempt did".
- `chg-abstraction-needs-two-callers` (card since deleted) has no source for the number two. Metz (item 9) argues for inlining a wrong abstraction and never names a count. Dodds's post builds on her argument, so AHA and Metz are close to one line of thought; they count separately only because they are different authors and sites. The Rule of Three (item 10) says three, not two. The Rule's "two or more" is the card's own choice.
- `sys-secrets-and-errors` Rule and Why do not match. The Rule line says only "fail closed". Secrets in source and log leaks sit in the Why. The third-source count above is for the fail-closed Rule line. If the Rule is meant to cover secrets, it needs its own line, and then it is backed by 12factor and OWASP only.
- `sys-load-shedding-bounded-queues`: Google's overload chapter (item 15) does not discuss bounded queues, and the Netflix README (item 16) does not mention unbounded queues. Only the cascading-failures chapter (item 14) backs "bound the queue" directly. Google SRE's advice on queue length is steady-state ("around half the thread pool") and bursty traffic is the stated exception; the card's `maxsize=1000` PASS example is illustrative, not sourced.
- `svc-retry-policy`: Google's cascading-failures chapter says to retry at one layer; the card's PASS comment "the client's own retries are off" matches. The 10% retry budget (item 4) is a Google number, not a general constant; the card correctly leaves the budget as a team convention.
- `chg-reuse-before-write`: the weakest of the nine. The kernel source (item 5) backs the habit, and nothing found describes how to search. No Google, Chromium, or Mozilla page tells reviewers to check for an existing helper; Google's looking-for page does not mention it.
- `chg-match-codebase-pattern`: no Rule problem. PEP 8 agrees with the Counterpoint.

## Not found or not read

- Rule of Three primary page (Fowler's book is the primary).
- Fowler's motivation text for "Replace Inline Code with Function Call" (page returned the example only).
- Brandur's idempotency-key post (not needed).
- Envoy and Istio retry docs, AWS Builders' Library timeouts post (same org as existing AWS sources), Rails Guides, Postgres docs for migrations (not needed).
- A Google, Chromium, or Mozilla reviewer page on reusing existing helpers: none found.

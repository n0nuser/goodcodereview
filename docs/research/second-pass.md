# Second research pass: review skills, gap sources, not-yet-covered list

Fetched 2026-10-24. Pages read through WebFetch (a small model summarises the page) unless marked "raw": raw means the file text was read directly (GitHub API for repo files, pdftotext for the Bacchelli-Bird PDF). Everything below is paraphrase. Each row gives the URL, what it says, and the card or gap id it supports.

## 1. Cursor thermo-nuclear skills

Public source: the cursor/plugins repo, folder `thermos` (the same skill also sits in `cursor-team-kit`). Three skills. Both review skills are manual-invoke only. Read raw via the GitHub contents API.

1. https://github.com/cursor/plugins/blob/main/thermos/skills/thermo-nuclear-code-quality-review/SKILL.md. Strict maintainability review of a branch diff. OPINION (house style of one vendor, no data). Points, numbered as in the file:
   - P0 Ambition: look for a restructuring that deletes whole branches, helpers or layers ("code judo") instead of tidying locally. Reviewer posture, not checkable. -> dropped in COVERAGE.
   - P1 File size: a change that takes a file from under 1000 lines to over it is a presumptive blocker unless justified. -> `code-file-lines-ceiling`.
   - P2 Spaghetti: new ad-hoc conditionals, scattered special cases and one-off flags or nullable modes in unrelated flows are a design problem. Move the logic behind its own abstraction. -> gap `chg-no-special-case-branches`.
   - P3 Design over "it works": do not approve a working change that leaves the structure messier. Prefer deleting moving parts over spreading them. -> dropped (posture; see `chg-review-signal`).
   - P4 Boring code: distrust magic, generic mechanisms that hide simple data shapes, thin wrappers and identity helpers. -> `fn-no-pass-through-wrapper`.
   - P5 Types and boundaries: question needless optionality, `any`/`unknown`, casts, and loosely shaped objects; silent fallback over an unclear invariant should become an explicit boundary. -> `py-no-cast`, `fn-known-keys-get-a-type`.
   - P6 Canonical layer: feature logic leaking into shared paths, bespoke helpers where a canonical one exists, logic in the wrong package. -> `mod-layers-point-inward`, `chg-reuse-before-write`.
   - P7a Independent async work run one after another without reason. -> gap `fn-independent-work-concurrent`.
   - P7b Related updates that can leave state half applied. -> gap `fn-atomic-related-updates`.
   - Flag list extras: copy-pasted logic (-> `chg-reuse-before-write`); temporary branching likely to become permanent (-> `chg-flag-owner-retirement`); refactors that move code without reducing concepts (-> `chg-refactor-separate` only partly; mostly P0).
   - Tone and bar: direct, not rude; few high-conviction comments; do not flood with nits; approval needs no structural regression (-> `chg-review-signal`, `chg-review-comment-format`).
2. https://github.com/cursor/plugins/blob/main/thermos/skills/thermo-nuclear-review/SKILL.md. Bug, break and security audit of a branch diff. OPINION. Points:
   - Report only issues in added or modified lines. -> `chg-review-signal`.
   - Trace side effects across packages before claiming breakage. -> `chg-verify-before-claim`.
   - Developer-experience breaks count: changed secret sources, renamed env vars, remapped ports, new scripts needed to run or build. -> gap `chg-devex-breaking-config`.
   - Feature-gated code must not leak past its gate. -> `chg-flag-owner-retirement`.
   - Do not report a risk the branch is clearly meant to introduce, unless the author may not see the full effect. -> dropped (posture).
   - Do not over-report priority; trace end to end before reporting. -> `chg-review-signal`.
   - Read PR bot comments only after finishing the audit, so the review stays independent. -> `chg-agent-independent-review`.
   - Never present unfinished research ("fine if the backend handles it") when the backend is readable. -> `chg-verify-before-claim`.
3. https://github.com/cursor/plugins/blob/main/thermos/skills/thermos/SKILL.md. Orchestrator: run the two reviews as parallel background subagents on the same scoped diff, merge, dedupe, weight overlap. Workflow, not a rule. -> dropped (mechanics; fresh-context idea is `chg-agent-independent-review`).
4. https://cursor.com/marketplace/skills/thermo-nuclear-review. Marketplace listing; confirms the public home. Search results only; page not read.
5. Third-party hands-on write-up (daily.dev, "Can Cursor's HARDCORE Review Skill Stop The Slop?") was seen in search results only, not read; it is a claim of about 5 of 7 suggestions useful and more false positives. Not used.

## 2. Pocock code-review skill and Fowler

6. https://github.com/mattpocock/skills/blob/main/skills/engineering/code-review/SKILL.md (raw). Reviews `git diff <fixed-point>...HEAD`. Two axes run in parallel subagents and are never merged or reranked: Standards (repo's documented standards plus a fixed smell baseline) and Spec (missing or partial requirements, unrequested behaviour, requirements implemented wrongly, each quoting the spec line). No spec found: skip Spec and say so. Rules for the baseline: the repo's own standard overrides it; each smell is a labelled judgement call; skip what tooling already enforces. Final line gives the worst finding per axis, no overall winner. Supports `chg-match-codebase-pattern` (Standards), `chg-matches-spec` (Spec).
7. https://github.com/mattpocock/skills/blob/main/docs/engineering/code-review.md (raw). Explains why two axes: code can obey every convention and build the wrong thing, or build the right thing against the conventions. Confirms the fixed point must be given and the diff checked non-empty before spawning. Supports `chg-matches-spec`, `chg-match-codebase-pattern`.
8. Same SKILL.md, smell baseline. Twelve smells, each "what it is -> fix":
   - Mysterious Name: name hides purpose; rename, or the design is murky. -> `mod-one-name-per-concept`.
   - Duplicated Code: same shape in more than one hunk; extract. -> `chg-reuse-before-write`.
   - Feature Envy: method uses another object's data more than its own; move it. -> `mod-behaviour-lives-with-state`.
   - Data Clumps: the same few fields travel together; give them a type. -> `fn-no-anonymous-tuples`, `fn-known-keys-get-a-type`.
   - Primitive Obsession: string or primitive stands in for a domain concept. -> `fn-no-stringly-typed-returns`.
   - Repeated Switches: same if-cascade on one type recurs; polymorphism or one shared map. -> `mod-fowler-smells`.
   - Shotgun Surgery: one logical change touches many files; gather what changes together. -> `mod-fowler-smells`.
   - Divergent Change: one module edited for unrelated reasons; split. -> `mod-cohesive-unit`.
   - Speculative Generality: hooks and parameters for needs the spec lacks; delete. -> `mod-yagni`.
   - Message Chains: long a.b().c().d() navigation; hide behind one method. -> `mod-fowler-smells`.
   - Middle Man: class mostly delegates; call the target. -> `fn-no-pass-through-wrapper`.
   - Refused Bequest: subclass ignores most of what it inherits; compose instead. -> gap `mod-subtype-passes-parent-tests`.
9. https://martinfowler.com/bliki/CodeSmell.html. Fowler: a smell is a surface hint of a deeper problem; Kent Beck coined the term while helping with the Refactoring book. A smell is a prompt to investigate, not proof; a long method can be fine. Supports `mod-fowler-smells` and Pocock's "judgement call" rule.
10. https://refactoring.com/catalog/. Lists refactorings only, no smell definitions. The smell chapter (ch.3, Refactoring 2nd ed.) is the book; no public primary page for the catalogue was found. The definitions in item 8 come from Pocock's wording, not Fowler's.

## 3. Sources for the gap ids

11. `chg-migration-add-column-rewrite`. https://www.postgresql.org/docs/current/sql-altertable.html. A non-volatile default needs no rewrite and a NULL default needs none; a volatile default, a stored generated column, an identity column, or a constrained domain type forces a table and index rewrite. ALTER COLUMN TYPE usually rewrites, and can need double disk space. Default lock is ACCESS EXCLUSIVE. Strong primary.
12. `code-ai-pr-disclosure`. https://docs.kernel.org/process/generated-content.html and https://docs.kernel.org/process/coding-assistants.html. Kernel: tool-written content is disclosed (tool, inputs, affected parts, testing); the human submitter must understand and defend the whole change; agents never add Signed-off-by; use an Assisted-by tag. Also https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md: disclose AI use, contributor must be able to explain the code without AI. Both primary project policies. Good enough.
13. `code-build-hermetic`. https://bazel.build/basics/hermeticity. Same sources and config give same output; tools come as managed copies, not host binaries; inputs identified by hash; pin tool and dependency versions; timestamps and absolute paths break it. And https://reproducible-builds.org/docs/definition/: reproducible means same source revision, instructions and environment give byte-identical outputs; list the environment inputs and keep it short. Strong primary. The "release tied to one revision" half is covered by the reproducible-builds source.
14. `code-secret-scan`. https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning. Scans full history and branches plus issues and PRs; on a leak, rotate first, history rewrite is slow and often unnecessary. https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html: keep secrets out of code and CI config, scan early (pre-commit), revoke then replace after exposure. Both primary enough. Vendor docs plus OWASP.
15. `fn-english-identifiers`. https://peps.python.org/pep-0008/. Standard library identifiers are ASCII and use English words where feasible; non-native authors should write comments in English unless the code will never leave their language group. Weak: it is a stdlib convention, not a general rule. Card should say "project policy".
16. `fn-resource-lifetime`. https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/ (Nathaniel Smith). A fire-and-forget task escapes its caller, so cleanup, error propagation and reasoning about control flow break. The fix is a scope every child task must finish inside, where child errors cancel siblings and reach the parent. OPINION, well argued, primary. Existing `py-task-reference` and `py-cancellation` cite asyncio docs instead.
17. `mod-prefer-sync-api`. https://sans-io.readthedocs.io/how-to-sans-io.html. Keep protocol logic as synchronous functions with no I/O so one tested core serves sync and async callers. And https://lucumr.pocoo.org/2020/1/1/async-pressure/ (Armin Ronacher): async makes accepting too much work cheap and hides overload; expose readiness. OPINION. The two together support "do not make an API async-only"; neither says it as a rule.
18. `mod-subtype-passes-parent-tests`. Already have https://www.hillelwayne.com/post/lsp/ (secondary restatement). Primary is Liskov and Wing, "A behavioral notion of subtyping" (1994) at https://www.cs.cmu.edu/~wing/publications/LiskovWing94.pdf. The fetch returned a scanned image PDF with no text layer, so it was not read. Status: primary located, not read.
19. `svc-saga-steps`. https://learn.microsoft.com/en-us/azure/architecture/patterns/saga (raw). Compensable steps can be undone; the pivot is the point of no return; steps after it are retryable and idempotent; compensations can fail and leave inconsistency; sagas lack isolation (lost updates, dirty reads) and need countermeasures such as semantic locks and rereading values. Strong primary. The original Garcia-Molina and Salem paper: two fetch attempts failed (certificate error, 404). Not read.
20. `svc-request-id-logging`. https://www.w3.org/TR/trace-context/. A shared trace-id travels across services; the spec does not mention logs, but recording the id in log lines is what lets them be matched to each other and the trace. Inference, not stated. Honeycomb's wide-event page (item 25) is the stronger support. Weak to medium.
21. `svc-stream-dont-materialise`. https://nodejs.org/en/learn/modules/backpressuring-in-streams. Without backpressure a fast source piles data into memory (the page's test went from about 88 MB to about 1.5 GB); write() returning false pauses the source until drain. Medium: Node-specific, but the claim is general. The "bound background tasks" half has no source; `lucumr` (item 17) covers unbounded accepted work.

## 4. Not-yet-covered list

22. Beck "Tidy First". https://newsletter.kentbeck.com/p/tidy-first returned 404; no public page of that name found. Existing notes already hold three Beck newsletter pages (batch-sizes, getting-untangled, management-separate-tidying), all partly paywalled. Nothing new. Supports `chg-refactor-separate`.
23. Ousterhout red flags. Only the book (paid) lists them; his book page (https://web.stanford.edu/~ouster/cgi-bin/book.php) has no list, only second-edition notes. Existing secondary source stays: the dev.to summary already in docs/research/authors-principles-2.md. None found as primary.
24. Bacchelli and Bird, ICSE 2013. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ICSE202013-codereview.pdf (raw via pdftotext; the abstract page was read before). Defect finding is the top expected outcome, yet defect comments are 14% (78 of 570) and mostly small logic slips; code-improvement comments are 29% (165 of 570); knowledge transfer and team awareness matter. Understanding the change and its reason is the main reviewer challenge; reviewers who own the files need less description, others lean on "what changed and why". Single-company study, 570 hand-classified comments. EMPIRICAL. Supports `chg-author-hygiene`, `chg-review-signal`.
25. Honeycomb on wide events. https://honeycomb.io/blog/structured-events-basis-observability. One record per request with many fields, emitted at the end; keep raw so questions need not be chosen in advance; pre-aggregated metrics lose context; cardinality (user or request ids) is what isolates a problem; add trace and span ids to form traces. Vendor blog, OPINION. Supports `prod-wide-events-bounded-labels` (a mild tension: that card bounds labels on metrics, this page wants high cardinality on events) and `svc-request-id-logging`. The Honeycomb "observability 2.0" page already in notes says similar.
26. Postgres locking. https://www.postgresql.org/docs/current/explicit-locking.html. ACCESS EXCLUSIVE conflicts with every table mode; CREATE INDEX takes SHARE, which blocks writes but not reads; CONCURRENTLY takes SHARE UPDATE EXCLUSIVE. The page says waiting for a lock has no timeout unless a deadlock is detected. Queue behaviour (a waiting ALTER blocks later reads) is general PG behaviour but the page does not state it, so it is not sourced here. Supports `sys-migration-lock-timeout`.
27. Postgres CREATE INDEX CONCURRENTLY. https://www.postgresql.org/docs/current/sql-createindex.html. Two table scans with waits for older transactions; cannot run in a transaction block; a failure leaves an INVALID index that still costs on writes (drop or REINDEX); one concurrent build per table; not supported on partitioned parents directly. Strong primary. Supports `sys-index-concurrently`.
28. Dan Luu. Already read (tests-v-reason, bug-blind). The review post is a 404 (recorded earlier). None new.
29. Julia Evans. Search found debugging posts (jvns.ca) and no code-review writing. None found for review. Not read.
30. Hillel Wayne. Already read hoc and lsp. https://www.hillelwayne.com/post/cleverness/ gist only: clever code that exploits problem knowledge can be faster and simpler but is fragile and hard to hand over. OPINION. Weak support for `fn-name-intermediate-conditions`; not used.
31. Stripe, Netflix, Uber. Search returned no primary engineering page on their code review. Only a paywalled Pragmatic Engineer deep dive on Stripe (API change review), secondary, not read. None found as primary.

## Not found or not read

- Fowler's own definitions of the 12 smells (book only).
- Liskov and Wing 1994 (scanned PDF), Garcia-Molina and Salem 1987 (fetch failed).
- Beck "Tidy First" public page; Ousterhout's own red-flag list.
- Primary Netflix, Uber, Stripe, Julia Evans review posts.
- No source for the unbounded background-task half of `svc-stream-dont-materialise`.

# Older cards: extra sources

Fetched 2026-10-24 through WebFetch (a small model summarises the page), so every row is paraphrase. Each row gives the URL, what it says, and the card whose Rule it backs.

1. https://refactoring.guru/smells/duplicate-code. Duplicate code often appears because a programmer did not know a colleague had already written the reusable piece. Merging duplicates shortens code and eases upkeep. Backs `chg-reuse-before-write`. Secondary (a teaching site, not a project guide).
2. https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/. Reviewers check that the change fits the architecture and coding patterns already in use. Backs `chg-match-codebase-pattern`. It says nothing on reuse.
3. https://google.github.io/eng-practices/review/reviewer/looking-for.html. Watch for over-engineering: code more generic than needed, or built for a problem that has not arrived. Solve the future problem when it comes. Backs the "real call sites today" clause of `chg-abstraction-needs-two-callers`. Same org as the Google source on `chg-match-codebase-pattern`, but a different card.
4. https://martinfowler.com/bliki/Yagni.html. Abstractions built for anticipated needs usually cost more than they return; treat ones that make current code harder to read with suspicion. Backs the same clause. Does not name a call-site count.

Count after: `chg-reuse-before-write` 3 -> 4 orgs (Orosz, kernel, Ousterhout via a secondary summary, refactoring.guru). `chg-match-codebase-pattern` 3 -> 4 (Google, Orosz, PEP 8, Microsoft). `chg-abstraction-needs-two-callers` 4 -> 6 authors/orgs (Dodds, Tef, Ousterhout, Metz, Google, Fowler).

Not useful (read, no claim): Fowler's Beck Design Rules page (no-duplication rule only, no reuse or wait-to-abstract); Go Code Review Comments (nothing on consistency or reuse); refactoring.com catalog (index only). Go proverbs list "a little copying is better than a little dependency", not read as a rule source for a call-site count.

Findings: no source states the number "two" in `chg-abstraction-needs-two-callers`; the Rule's count is the card's own choice (see near-miss-sources.md). No source describes how to search for an existing helper.

Dedupe: `mod-bounded-caches` (draft, no sources) deleted. Its Rule (bound per-key caches by LRU or TTL) is covered by `sys-cache-bounds-invalidation` (size plus expiry). Its owner-end eviction line was Why-level only.

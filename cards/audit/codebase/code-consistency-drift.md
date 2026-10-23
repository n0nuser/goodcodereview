---
id: code-consistency-drift
level: codebase
tags: [consistency, architecture]
severity: discuss
status: draft
lang: core
applies_when: Auditing whether one concern is solved in several incompatible ways across the repo.
tool_gate: Lint rules that ban the deprecated pattern once a standard is chosen.
borrowed_from:
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
---

**Rule.** For each recurring concern (errors, config, HTTP clients, logging), one pattern is the standard and older variants are tracked for migration, not left as equal peers.

**Why.** Each extra variant is another thing to learn, test and secure, and drift accumulates through changes that each looked locally fine.

**FAIL**

```text
Three HTTP clients (requests, urllib3, httpx) with three timeout conventions;
no document says which is current.
```

**PASS**

```text
docs: "use httpx via net/client.py". Lint bans direct requests imports;
legacy sites listed in MIGRATION.md.
```

**Counterpoint.** Forcing one way can block a better tool. Answer: allow change through a proposal that updates the standard and migration list, not by a quiet second pattern. Leaning on Google: consistency is a tie-breaker, not a trump card.

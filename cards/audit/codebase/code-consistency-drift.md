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

**Rule.** For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard and track older variants for migration instead of leaving them as equal peers.

**Why.** Each extra variant is another thing to learn, test, and secure, and drift accumulates through changes that each looked locally fine.

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

**Counterpoint.** Forcing one way can block a better tool. Allow change through a proposal that updates the standard and the migration list, not through a quiet second pattern. Following Google, consistency is a tie-breaker, not a trump card.

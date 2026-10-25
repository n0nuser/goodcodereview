---
id: code-consistency-drift
level: codebase
tags: [correctness, maintainability, consistency, architecture]
severity: discuss
status: stable
lang: core
applies_when: Auditing whether one concern is solved in several incompatible ways across the repo.
tool_gate: Lint rules that ban the deprecated pattern once a standard is chosen.
note: Spotify, Uber, Cabify and Stripe back one standard per concern; tracking old variants has 2 (Stripe, Spotify), so it is in Why
borrowed_from:
  - https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/
  - https://google.github.io/eng-practices/review/reviewer/standard.html
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://engineering.atspotify.com/2026/6/code-with-claude-coding-is-no-longer-the-constraint
  - https://www.uber.com/blog/ubers-rate-limiting-system/
  - https://tech.cabify.com/blog/engineering/cabify-container-certification
  - https://stripe.dev/blog/sorbet-stripes-type-checker-for-ruby
---

**Rule.** For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.

**Why.** Each extra variant is another thing to learn, test, and secure, and drift accumulates through changes that each looked locally fine. Two limiters built two ways enforce the same quota differently. List the older variants and count them, so the migration shows progress and a new one shows up in review.

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

**Counterpoint.** "Forcing one way can block a better tool." Allow change through a proposal that updates the standard and the migration list, not through a quiet second pattern. Consistency breaks ties. It does not outrank a measured reason to switch.

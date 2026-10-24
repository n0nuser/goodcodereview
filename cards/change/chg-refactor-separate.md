---
id: chg-refactor-separate
level: change
tags: [refactoring, scope]
severity: should-fix
status: stable
lang: core
applies_when: The change both restructures or reformats code and changes behaviour, or moves code between files.
tool_gate: A formatter check in CI removes the reformatting case.
borrowed_from:
  - https://docs.kernel.org/process/submitting-patches.html
  - https://henrikwarne.com/2024/01/10/tidy-first/
  - https://newsletter.kentbeck.com/p/getting-untangled
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
---

**Rule.** Put refactors, renames, and reformatting in their own commit or PR, apart from behaviour changes.

**Why.** A reviewer can verify a pure refactor by "tests unchanged" and a pure move by diff. Mixed in with logic, neither check works and a real bug hides in noise. Never edit moved code in the same patch as the move.

**FAIL**

```text
commit: "Move parser to parsing/ and fix off-by-one"
diff shows whole file as new, the fix is line 212 of 400.
```

**PASS**

```text
commit 1: move parser (git detects rename, 0 content change)
commit 2: fix off-by-one + test
```

**Counterpoint.** Separate PRs cost review round trips, and untangling a mixed branch after the fact is work. Separate commits in one PR are an acceptable compromise, but separate PRs are ideal. A tidy that exists only to enable the behaviour change in hand may ship with it if the commits stay apart.

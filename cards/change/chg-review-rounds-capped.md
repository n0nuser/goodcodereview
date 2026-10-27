---
id: chg-review-rounds-capped
level: change
tags: [process, review, agents]
severity: discuss
status: draft
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that cap review rounds or limit re-review to the new diff
lang: core
applies_when: A change goes through repeated review rounds, especially with an automated author or reviewer.
tool_gate: Review bot configured with a maximum number of rounds and a diff-only re-review mode.
note: Anthropic only (a vendor, in a post about its own Claude Code team); "Limit the number of cycles" and "Limit re-review to just diff after the initial cycles"; the post says an agent author and an agent reviewer can cycle forever
borrowed_from:
  - https://x.com/addyosmani/status/2114604912520921136
---

**Rule.** Cap the number of review rounds; after the cap, re-review only the new diff and ask the author to rethink the approach if findings keep coming.

**Why.** A reviewer that reads the whole change again each round mostly re-reports old issues and adds a few more, and an agent author that answers each finding with a commit can loop without end. A cap forces the loop to converge.

**FAIL**

```text
Round 9: reviewer re-reads all 40 files and reports 2 new nits.
Round 10: author pushes fixes; reviewer re-reads all 40 files again.
```

**PASS**

```text
Rounds 1 to 3: full review.
After round 3: reviewer reads only commits since the last round, and the author is asked
whether the approach is right before another round starts.
```

**Counterpoint.** "Each pass can find a different bug." True, and a high-risk change can justify extra full passes, so the cap is a default that an owner can raise. A rule for every routine change is cheaper than a loop with no end.

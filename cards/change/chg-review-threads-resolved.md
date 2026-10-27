---
id: chg-review-threads-resolved
level: change
tags: [process, review]
severity: should-fix
status: draft
lacks: orgs, only Anthropic (a vendor) backs it; needs two more orgs that block merge on open review threads
lang: core
applies_when: A change has review comments and is about to merge.
tool_gate: Branch protection that requires conversations to be resolved before merge.
note: Anthropic only (a vendor, in a post about its own Claude Code team); "Require that all review threads be resolved before merging"
borrowed_from:
  - https://x.com/addyosmani/status/2114604912520921136
---

**Rule.** Do not merge while any review thread is open; each one ends as a fix or as a resolution with a stated reason.

**Why.** A comment that nobody answered gets lost at merge time, and the bug or question it raised ships with the change. A written reason for dismissing a thread also leaves a record for the next reader.

**FAIL**

```text
Thread on db.py:88: "this swallows the timeout error"
No reply, no commit. The PR merges on an earlier approval.
```

**PASS**

```text
Thread on db.py:88: "this swallows the timeout error"
Reply: "fixed in 9f2c1ab, the error now propagates." Thread resolved.
Another thread: "not a bug, the caller retries; see line 40." Resolved with that reason.
```

**Counterpoint.** "Nits will hold up the merge." The author may close a nit with a short reason, so the rule costs one line, not a code change. Reviewers should keep threads for points that matter.

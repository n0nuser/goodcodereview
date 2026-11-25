---
id: chg-review-threads-resolved
level: change
tags: [process, review]
severity: should-fix
status: draft
lacks: orgs, GitHub and GitLab document the merge setting only; the Anthropic X post cannot be re-fetched; needs orgs that state it as a rule
lang: core
applies_when: A change has review comments and is about to merge.
tool_gate: Branch protection that requires conversations to be resolved before merge.
note: GitHub: require conversation resolution before merging; GitLab: prevent merge while threads remain open; both are settings. Anthropic X post not re-fetchable (JS shell)
borrowed_from:
  - https://x.com/addyosmani/status/2114604912520921136
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches
  - https://docs.gitlab.com/user/project/merge_requests/
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

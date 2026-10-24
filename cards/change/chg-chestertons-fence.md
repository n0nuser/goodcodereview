---
id: chg-chestertons-fence
level: change
tags: [legacy, history]
severity: should-fix
status: draft
lang: core
applies_when: The change removes, rewrites or "simplifies" odd-looking existing code, or rewrites a module.
tool_gate: none
borrowed_from:
  - https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/
  - https://michaelfeathers.silvrback.com/characterization-testing
  - https://github.com/cursor/plugins/blob/main/pstack/skills/why/SKILL.md
  - https://github.com/cursor/plugins/blob/main/dyl-stack/skills/dyl-review/SKILL.md
---

**Rule.** Add a characterization test before rewriting code you do not understand.

**Why.** Strange code often carries a fix for a bug that is no longer visible. Removing it re-ships the bug. Check the history first (blame, the PR that added it, tickets, postmortems); defensive code such as null checks, retries and timeouts usually answers a real incident. For a rewrite, name the defect that justifies it.

**FAIL**

```text
PR "simplify retry loop": removes sleep(0.2) and a dedup check.
No blame/history cited; no test. Rewrite justified by "this is a mess".
```

**PASS**

```text
git blame shows sleep added for rate-limit incident INC-17.
PR keeps it with a comment, adds a characterization test first.
```

**Counterpoint.** Joel Spolsky's anti-rewrite case rests on anecdotes (Netscape, Borland), and Hickey argues for restating the problem, which may mean a new design. Rethinking is allowed. A big-bang rewrite needs small shippable steps, the old path working meanwhile, and a named defect.

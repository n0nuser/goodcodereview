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
---

**Rule.** Before deleting or rewriting code you do not understand, read its history and add a test recording what it does today; the description names the defect that justifies a rewrite.

**Why.** Strange code often carries a fix for a bug that is no longer visible. Removing it re-ships the bug.

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

**Counterpoint.** Joel's anti-rewrite case rests on anecdotes (Netscape, Borland) and Hickey argues for restating the problem, which may mean a new design. Answer: rethinking is allowed; a big-bang rewrite needs small shippable steps, the old path working meanwhile, and a named defect.

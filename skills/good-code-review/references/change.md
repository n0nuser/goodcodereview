# change

## chg-author-hygiene

severity: should-fix  
applies_when: Every change submitted for review.

**Rule.** Self-review the diff and write the description before requesting review.

**Why.** Reviewer time spent on stray debug lines, red builds, or a missing "why" is wasted and teaches reviewers to skim. The description gives the reason, the impact, and how the author verified the change. CI is green, or a failing job is shown to fail on the base branch too.

**FAIL**

```text
Title: "fixes". Body empty. CI red on lint. Diff has a leftover print() and
a commented-out block.
```

**PASS**

```text
Body: why (bug link), what changed, test plan, risk. CI green.
Author left inline notes on the two non-obvious hunks.
```

**Counterpoint.** Templates breed boilerplate that no one reads. The check is for substance, not headings: a one-line change needs one line of reason. Performance claims need numbers.

## chg-breaking-change-taxonomy

severity: block  
applies_when: The change alters anything a caller can observe, documented or not.

**Rule.** Treat any observable difference in signature, return shape, error type, ordering, timing, defaults, or side effects as breaking until a consumer check says otherwise.

**Why.** With enough users, every observable behaviour is depended on, so "undocumented" does not mean "safe to change".

**FAIL**

```text
list_orders() now returns newest-first (was insertion order).
PR says "no API change"; docs never promised an order.
```

**PASS**

```text
PR states: "ordering changes, known consumers A and B checked,
flag orders_newest_first defaults off for one release".
```

**Counterpoint.** Treating everything as breaking freezes the code. Weigh each change by known consumers and blast radius, and use a staged rollout instead of a ban. Optional parameters with defaults are the safe way to add.

## chg-expand-contract

severity: block  
applies_when: The change renames, removes or reshapes a column, API field, message, config key or exported symbol that other code reads.

**Rule.** Evolve shared contracts in steps: add the new form beside the old (expand), migrate every consumer, then remove the old form (contract) in a later change.

**Why.** Producers and consumers deploy at different times. A one-step rename breaks whichever side is still on the old version.

**FAIL**

```sql
ALTER TABLE users RENAME COLUMN name TO full_name;  -- app v1 still reads name
```

**PASS**

```sql
-- change 1: add full_name, dual-write, backfill
-- change 2: readers switch to full_name
-- change 3 (later): drop name
```

**Counterpoint.** Three steps are slow for internal code. Exception: when producer and consumers deploy atomically from one repo, or the table is small enough to alter in one safe step, a one-step change is fine. Say so in the description. [[sys-migration-expand-contract]] covers batching and release steps for databases.

## chg-one-concern

severity: should-fix  
applies_when: Every change.

**Rule.** Make each change do one logical thing; if the description needs "and" between unrelated outcomes, split it.

**Why.** Reviewers can only judge intent and risk of a single concern. Mixed changes hide the risky part, cannot be reverted alone, and break bisect.

**FAIL**

```text
PR "Add export button": new endpoint, renamed 40 files, bumped a dependency,
fixed an unrelated typo in the auth module.
```

**PASS**

```text
PR 1: dependency bump.  PR 2: rename (no logic change).  PR 3: export button.
```

**Counterpoint.** Splitting adds overhead, and stacked diffs need tooling and cost rebasing pain. The rule is one concern, not a line count: as small as possible, but no smaller. A single concern that is legitimately large (a generated migration) is fine if the description says so.

## chg-refactor-separate

severity: should-fix  
applies_when: The change both restructures or reformats code and changes behaviour, or moves code between files.

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

## chg-review-signal

severity: discuss  
applies_when: A reviewer is deciding what to comment on.

**Rule.** Do not comment on what a tool enforces or on taste with no written rule; spend comments on a few high-conviction findings, and if there are many, talk to the author.

**Why.** Noise buries the real defects and trains authors to dismiss review. A rubber-stamp approval is just as harmful: an approval must reflect real reading.

**FAIL**

```text
27 comments: 18 whitespace and import-order, 6 "I'd write it differently",
the null dereference on line 90 never mentioned.
```

**PASS**

```text
3 comments: the null dereference, a missing test for the empty case,
one nit. Formatting left to the formatter, which CI enforces.
```

**Counterpoint.** Limiting comments risks missing issues. The cap applies to opinion, not to defects, so every real defect is still raised. The written style guide or the formatter settles style, and repeated nits mean a missing gate.

## chg-size-ceiling

severity: discuss  
applies_when: The diff exceeds roughly 400 changed lines or about 20 files and is not generated or a pure move.

**Rule.** Split a change past about 400 changed lines or about 20 files, or say in the description why not; aim for about 200.

**Why.** Review usefulness falls as changes grow, so big diffs get skimmed and approved on trust.

**FAIL**

```text
1,800-line PR, 55 files, one approval after 10 minutes, no split plan.
```

**PASS**

```text
Stack of 6 changes of 150-300 lines, each builds and passes tests alone.
```

**Counterpoint.** "Line counts are arbitrary." The exact numbers are rough, but the direction is not: larger changes get fewer useful comments per file and are approved on trust. Treat 400 as a prompt to split or explain, not a hard gate, and exclude generated code and pure moves.

## chg-tests-ship-with-change

severity: block  
applies_when: The change alters behaviour of non-trivial code.

**Rule.** Ship new or changed behaviour in the same change as a test that fails if the behaviour breaks; a code-only change needs a stated reason.

**Why.** "Tests later" mostly means never, and the reviewer cannot tell from reading whether the code does what the author intended.

**FAIL**

```text
PR touches billing/discount.py (+90 lines). No file under tests/ changed.
Description: "will add tests in a follow-up".
```

**PASS**

```text
PR adds discount.py change and test_discount.py with the edge cases
(zero quantity, stacked coupons); the test was seen failing before the fix.
```

**Counterpoint.** "Holding a good change for tests blocks progress." Approve changes that improve the code even when imperfect, but the test is part of the change, not polish. Untestable cases exist (config, pure docs, emergency fixes), and the rule allows them with a written reason and a ticket for the test.

## chg-verify-before-claim

severity: block  
applies_when: The author or reviewer asserts the change works or a finding is real.

**Rule.** Back every "works" or "bug" claim with something run: a repro, a test or command output.

**Why.** Reasoning that "looks correct" misses stateful and corner cases, and a reviewer's false finding wastes the author's time. For a bug fix, reproduce the bug first and rerun the repro after the change.

**FAIL**

```text
Author: "Fixed the race, trust me." Reviewer: "LGTM, reads fine."
Nobody ran the failing case.
```

**PASS**

```text
Author: "repro: script X failed 3/10 runs; after fix 0/200. Test added."
Reviewer checked out the branch and reran it.
```

**Counterpoint.** Running everything is slow. Scale with risk: a rename needs no repro, but a race, a bug fix, or a UI change does. See it run, do not only read it.

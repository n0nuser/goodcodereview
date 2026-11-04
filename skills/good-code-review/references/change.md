# change

## chg-approval-tied-to-patch

severity: should-fix  
concerns: process  
applies_when: A review approval or verification result exists and the branch has been pushed or rebased since.  
Backed by: Cursor, Anthropic, GitLab, Kubernetes, Gerrit Code Review.

**Rule.** Treat an approval or verification verdict as current only if the patch is unchanged: compare `git patch-id` at the verdict commit with the current head. If the patches differ only in tests, docs, or lint config, the verdict can stand when the built output is the same; any other difference needs a fresh check.

**Why.** A verdict covers one patch. After a push or rebase the reviewer approved code that no longer exists.

**FAIL**

```text
Approved at abc123. Two later pushes change src/auth.py. Merged on the old approval.
```

**PASS**

```text
Approved at abc123. Rebase onto main: `git patch-id` of the diff at abc123 equals the one at the new head, so the approval stands.
Push that edits src/auth.py: patch ids differ, approval dismissed, re-requested.
Push that only edits a README: approval stands once the build output is shown to be the same.
```

**Counterpoint.** "Re-approving after every push is noisy." A rebase that keeps the patch id does not void the verdict, and neither does a change to tests, docs, or lint config that leaves the built output the same. Branch protection can enforce this without human effort.

## chg-author-hygiene

severity: should-fix  
concerns: process  
applies_when: Every change submitted for review.  
Backed by: Linux kernel, Phacility, Palantir, Kubernetes, GitLab.

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
concerns: compatibility  
applies_when: The change alters anything a caller can observe, documented or not.  
Backed by: Python Software Foundation, Google, Microsoft, Kubernetes, OpenJDK, AWS, Pact, Spring. People cited: Hyrum Wright, Michael Feathers.

**Rule.** Treat any change that callers can observe in a signature, return values, error types, defaults, or side effects as breaking until a consumer check says otherwise.

**Why.** With enough users, every observable behaviour is depended on, so "undocumented" does not mean "safe to change". Result ordering and timing can break callers too, but no published guide treats them as breaking, so weigh them case by case.

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

## chg-delete-legacy-after-migration

severity: should-fix  
concerns: compatibility, maintainability  
applies_when: The change adds a new API, path or config and every caller lives in this repo.  
context: data  
Backed by: Cursor, Stripe, Google, LLVM.

**Rule.** When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.

**Why.** Two supported ways to do one task both keep gaining callers. The old path becomes the one nobody dares remove.

**FAIL**

```text
+ def fetch_user_v2(id): ...
  def fetch_user(id): ...        # kept "for now"; 14 callers still use it
```

**PASS**

```text
- def fetch_user(id): ...        # old API deleted
+ def fetch_user_v2(id): ...     # new API
- user = fetch_user(uid)         # x14, every caller moved to fetch_user_v2 in this diff
+ user = fetch_user_v2(uid)
```

**Counterpoint.** This rule applies only when no consumer sits outside the repo: a published library, a public API, a client on an older release, or data written by older code. For those, follow [chg-expand-contract](change.md#chg-expand-contract) and remove the old form later. Check the consumer claim before you mark `FAIL`. Even with all callers in the repo, a team may keep the old path on purpose: Stripe kept Flow support for part of its codebase while it moved the rest to TypeScript. A stated, scoped exception is not a FAIL.

## chg-devex-breaking-config

severity: should-fix  
concerns: compatibility, process  
applies_when: The change renames an environment variable, remaps a port, moves a secret source, or adds a step needed to run or build the project.  
Backed by: Cursor, GitLab, Spring.

**Rule.** Flag a change that renames or removes an environment variable, moves a secret, or remaps a port as breaking for developers and operators, and update every place that documents or sets it.

**Why.** A renamed variable or moved secret fails on the next machine that pulls, often with a vague error far from the cause. The diff looks harmless because nothing in the code breaks. A short migration note with the old name, the new name, and what to do saves each person from finding that out alone.

**FAIL**

```text
- DATABASE_URL=...
+ DB_DSN=...            # no note, no fallback, .env.example untouched
```

**PASS**

```text
+ DB_DSN=...            # reads DATABASE_URL with a deprecation warning for one release
+ PR text flags the break: "DATABASE_URL renamed to DB_DSN; update .env and CI secrets"
+ .env.example updated
```

**Counterpoint.** "It is an internal repo; people will ask." Each person who asks costs more than the note, and CI and deploy environments cannot ask. For published configuration, [chg-breaking-change-taxonomy](change.md#chg-breaking-change-taxonomy) has the wider rules.

## chg-expand-contract

severity: block  
concerns: compatibility  
applies_when: The change renames, removes or reshapes a column, API field, message, config key or exported symbol that other code reads.  
context: data  
Backed by: Python Software Foundation, GitLab, Stripe, Kubernetes, Microsoft. People cited: Hyrum Wright.

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

**Counterpoint.** Three steps are slow for internal code. Exception: when producer and consumers deploy atomically from one repo, or the table is small enough to alter in one safe step, a one-step change is fine. Say so in the description. [sys-migration-expand-contract](system.md#sys-migration-expand-contract) covers batching the backfill.

## chg-match-codebase-pattern

severity: should-fix  
concerns: correctness, maintainability  
applies_when: The change adds code that solves a problem the codebase already solves somewhere.  
Backed by: Google, The Pragmatic Engineer, Python Software Foundation, Microsoft.

**Rule.** Follow the established pattern nearby.

**Why.** A silent second way to do the same thing doubles what every later reader must learn. Equally, copying a bad pattern forever freezes it in place.

**FAIL**

```text
Repo uses Result-returning repository classes everywhere.
New PR adds a module that raises raw DB exceptions and builds SQL inline,
description: "cleaner this way". No ticket, no mention of the old pattern.
```

**PASS**

```text
New module uses the repository pattern like its neighbours.
PR notes: "pattern X leaks DB errors, see TICKET-123 proposing a standard".
Code the PR touches anyway is improved in passing.
```

**Counterpoint.** "Consistency preserves bugs." Consistency is a tie-breaker, not a reason to copy something that breaks a rule or hurts code health, so a reviewer must not demand matching code that makes things worse. When the nearby pattern is bad, keep to the local style in this change, file a ticket, and propose the new standard in its own change, improving what you touch. A second pattern slipped into a feature change without a word is the failure.

## chg-no-silenced-diagnostics

severity: should-fix  
concerns: correctness, maintainability, process  
applies_when: The diff adds a suppression (lint ignore, type ignore, skipped test, swallowed error) or deletes a failing check.  
Backed by: Google, Palantir, Cursor, ESLint, Rust project.

**Rule.** Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.

**Why.** Silencing a diagnostic hides the problem it reports and removes the safety net for the next author.

**FAIL**

```python
x = load(cfg)  # type: ignore
try: sync()
except Exception: pass
@pytest.mark.skip   # flaky
```

**PASS**

```python
x = load(cfg)  # type: ignore[arg-type]  # lib stub wrong, TICKET-42
try: sync()
@pytest.mark.skip(reason="flaky on CI clock skew, TICKET-43, remove by 2026-12-01")
```

**Counterpoint.** Sometimes a warning is a false positive. Then suppress narrowly with a reason and an expiry date, which keeps the gate useful. A suppression of a rule that guards correctness or safety should be removed, not documented. Palantir's list covers TODOs without issue references and merging with checks red. The Go list covers discarded errors. This card extends both to suppressions.

## chg-one-concern

severity: should-fix  
concerns: process  
applies_when: Every change.  
Backed by: Linux kernel, Python Software Foundation, Phacility, Palantir.

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

## chg-perf-claim-evidence

severity: should-fix  
concerns: performance, testing  
applies_when: The change or its description claims a speed, throughput, memory or cost improvement.  
Backed by: Cursor, Linux kernel, GitLab, Phacility.

**Rule.** Back a performance claim with measured before-and-after numbers.

**Why.** A single fast run can measure noise, a cached result, an error path that returns early, or a step that is a tenth of the total. A piece that is 10% of the run caps the gain near 11% however well it is tuned. So a useful number comes with the run count, the spread, the resource that limits further gain, and a check that errors were counted and the work ran inside the timed region.

**FAIL**

```text
"Parse is much faster now." (no numbers; 4% of requests now return 500 early)
```

**PASS**

```text
Median of 7 alternating runs: 412 ms -> 301 ms, range 398-421 vs 295-310.
0 errors in both. Parse is 35% of the request, so the cap is 1.5x; limiter: DB round trip.
```

**Counterpoint.** "A micro-optimisation needs no benchmark ceremony." A claim in prose does. If the description makes no performance claim, mark `N/A`.

## chg-proto-no-field-type-change

severity: should-fix  
concerns: compatibility  
applies_when: The diff changes an existing field's type, default, label or name in a `.proto` file.  
Backed by: Google, Buf, Istio.

**Rule.** Never change the type of a protobuf field, switch it between repeated and scalar, or rename it while any consumer reads JSON or text format; add a new field instead.

**Why.** The wire format carries numbers and types, not names, so a type change is read as garbage by anything not yet redeployed. The JSON and text formats carry names, so a rename breaks those readers.

**FAIL**

```proto
message Invoice {
-  int32 amount = 2;
+  string amount = 2;
}
```

**PASS**

```proto
message Invoice {
  int32 amount = 2 [deprecated = true];
  string amount_decimal = 3;
}
```

**Counterpoint.** "Both ends deploy together." A rolling deploy runs both versions at once, and stored data does not redeploy. If the message never leaves one binary, mark the card N/A.

## chg-refactor-has-behaviour-pin

severity: should-fix  
concerns: testing, maintainability  
applies_when: The change restructures code and claims to keep its behaviour.  
Backed by: Cursor, GitHub, Stripe, SonarSource, JetBrains, Apache Software Foundation.

**Rule.** Pin current behaviour with a characterization test, snapshot or equivalence check before the refactor moves any structure.

**Why.** A type check and a linter pass on code that now does something else. Without a pin, "no behaviour change" is a claim nobody ran.

**FAIL**

```text
PR "split billing.py into three modules": 900 lines moved, no test touched or added.
```

**PASS**

```text
Commit 1: golden-file test of invoice output for 12 fixtures (passes on old code).
Commit 2: the split. The same test passes unchanged.
```

**Counterpoint.** "The code is already well tested." Then name the test that covers the moved paths. If you cannot, the pin is missing. See [chg-refactor-separate](change.md#chg-refactor-separate) for keeping the refactor apart from behaviour changes.

## chg-refactor-separate

severity: should-fix  
concerns: maintainability, process  
applies_when: The change both restructures or reformats code and changes behaviour, or moves code between files.  
Backed by: Linux kernel, Google, Apache Software Foundation, Python Software Foundation, LLVM. People cited: Henrik Warne, Kent Beck.

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

## chg-reuse-before-write

severity: should-fix  
concerns: maintainability  
applies_when: The change adds a helper, util, type or constant.  
Backed by: GitHub, Cursor, Google, Linux kernel, Refactoring.Guru. People cited: Sébastien Portebois.

**Rule.** Do not add a helper that duplicates one already in the repo; search for it first.

**Why.** Reviewers see only the diff, so a reimplementation of a helper a few files away looks fine in isolation. Two copies then drift and get fixed once.

**FAIL**

```python
# utils/dates.py already has parse_iso(s)
def _parse_date(s):  # new, in billing/invoice.py
    return datetime.strptime(s, "%Y-%m-%d")   # drops timezone handling
```

**PASS**

```python
from utils.dates import parse_iso
```

**Counterpoint.** "Searching costs more than writing ten lines." For tiny code that is true. Then the duplicate is tolerable and `mod-yagni` governs extraction. The cost flips once the logic holds a rule (parsing, money, auth) that must stay in one place.

## chg-review-signal

severity: discuss  
concerns: process  
applies_when: A reviewer is deciding what to comment on.  
Backed by: Google, Slack, The Pragmatic Engineer, Microsoft, Meta, Anthropic.

**Rule.** Do not spend review comments on what a tool enforces or on minor style points; spend them on the findings that matter.

**Why.** Noise buries the real defects and trains authors to dismiss review. Prefer a few high-conviction comments, and when a first pass turns up many, talk to the author instead of posting a long list; both are common advice but have fewer than three organisations behind them, and a style point outside the written guide is the reviewer's taste. A rubber-stamp approval is just as harmful: an approval must reflect real reading.

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

## chg-rollback-path

severity: should-fix  
concerns: reliability  
applies_when: The change deploys schema, data, config or behaviour that is costly to undo.  
Backed by: Anthropic, Google, GitLab, Microsoft, AWS. People cited: tef (programmingisterrible).

**Rule.** State in the description how to undo the change.

**Why.** When a release goes wrong, the time to find the way back is before shipping. Irreversible steps (dropped data, sent messages) need an explicit decision. The author has checked that the route is possible. See [inc-rollback-path-tested](incident.md#inc-rollback-path-tested) for drilling it and [prod-canary-staged-rollout](production.md#prod-canary-staged-rollout) for abort rules.

**FAIL**

```text
Migration drops column legacy_id and deletes backing rows.
Description: no rollback section. Code and migration deploy together.
```

**PASS**

```text
Rollback: revert PR; column kept for one release, dropped in a later PR.
Behaviour behind a flag; canary at 5% with an abort rule.
```

**Counterpoint.** "We can always roll forward." Fine for stateless code, but not after data is destroyed or a client has cached the new contract. The check is cheap for reversible changes (one line) and bites only on irreversible ones.

## chg-size-ceiling

severity: discuss  
concerns: process  
applies_when: The diff exceeds roughly 400 changed lines or about 20 files and is not generated or a pure move.  
Backed by: Google, Microsoft, SmartBear, The Pragmatic Engineer, US Department of Veterans Affairs, USGS, Apache Software Foundation, Godot Engine, Ethereum Foundation.

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
concerns: testing  
applies_when: The change alters behaviour of non-trivial code.  
Backed by: Kubernetes, Python Software Foundation, Google, Rust project, Ruby on Rails, Microsoft, Mozilla.

**Rule.** Ship new or changed behaviour in the same change as a test that fails if the behaviour breaks.

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

**Counterpoint.** "Holding a good change for tests blocks progress." Approve changes that improve the code even when imperfect, but the test is part of the change, not polish. Untestable cases exist (config, pure docs, emergency fixes), and a written reason plus a ticket for the test is the usual way to ship without one.

## chg-verify-before-claim

severity: block  
concerns: testing, process  
applies_when: The author or reviewer asserts the change works or a finding is real.  
Backed by: Python Software Foundation, Phacility, Google, Anthropic, GitLab. People cited: Dan Luu.

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

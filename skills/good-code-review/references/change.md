# change

## chg-agent-grounded-code

severity: should-fix  
concerns: maintainability, process  
applies_when: The change was written fully or partly by an AI agent.  
tool gate: Compiler, type checker and dependency-resolution in CI catch non-existent imports and calls.  
Backed by: Kubernetes (unjudged), Google (unjudged), University of Texas at San Antonio (unjudged), Cloud Security Alliance (supports). Backing: mixed.

**Rule.** Verify that every import and external call the agent wrote exists with that signature.

**Why.** Agents invent plausible APIs and rewrite nearby utilities without searching. A study of 16 code models found that at least about 5% of the packages they suggested (about 22% for open-source models) did not exist, and an attacker can publish a malicious package under a name that models keep inventing. A green build proves only what the compiler sees. [chg-reuse-before-write](change.md#chg-reuse-before-write) covers re-implemented helpers. The author must also be able to explain each hunk; see [chg-agent-independent-review](change.md#chg-agent-independent-review).

**FAIL**

```python
import requests_cache_pro                # package does not exist, or exists only because an attacker registered it
total = sum_cents(items)                 # new helper; money.sum_cents() already exists
resp = client.fetch_json(url, retries=3) # fetch_json has no retries param
```

**PASS**

```python
from money import sum_cents
resp = client.fetch_json(url)   # signature checked against source
```

**Counterpoint.** "Humans make the same mistakes." True, but agents make them fluently and at volume, and disclosure alone does not catch them. Kubernetes requires disclosure and an author who can explain the change. A compiler and a dependency check catch the mechanical part, so use this card for calls that resolve but behave differently than assumed.

## chg-agent-independent-review

severity: should-fix  
concerns: process  
applies_when: An agent wrote the change, and an agent or the same session is asked to review it.  
Backed by: Kubernetes (unjudged), Meta (unjudged), Stripe (unjudged), Uber (unjudged), Dropbox (unjudged), Anthropic (supports), GitLab (unjudged). Backing: mixed.

**Rule.** Get sign-off from a person or a fresh-context reviewer who has the spec but not the author's reasoning; self-review by the writing session does not count.

**Why.** The same context repeats the same blind spots and assumptions. An approval without real reading is a rubber stamp. The person who submits the change must also be able to explain each hunk. A human author's own approval does not count either: most review tools can bar it.

**FAIL**

```text
Session writes the diff, then "reviews" it: "no issues found". Merged.
```

**PASS**

```text
Fresh reviewer given spec + diff + test output, runs the branch, files findings.
A human who can explain the change approves.
```

**Counterpoint.** A same-session pass still catches typos and leftovers. Keep it as the author's self-review step, not as the gate. Meta tracks "eyeball time" as a guardrail against rubber-stamping, the failure this card targets.

## chg-applied-migration-not-edited

severity: should-fix  
concerns: correctness, process  
applies_when: The diff changes or deletes a migration file that is already on the main branch.  
context: data  
tool gate: Flyway `validate` or a Liquibase checksum check in CI; a CI step that fails when a file under the migrations directory that exists on main is modified or removed.  
Backed by: Redgate (unjudged), Ruby on Rails (unjudged), Prisma (unjudged). Backing: unjudged.

**Rule.** Do not edit or delete a migration that has already run in a shared environment; add a new migration that makes the change.

**Why.** A database records which migrations it has applied. If you change one afterwards, environments that ran the old version never run the new one, so staging, production and each developer's copy drift apart with no error. Migration tools that store a checksum fail on the edited file instead. A new migration reaches every environment the same way. A migration that has run only on your own machine can still be edited.

**FAIL**

```diff
# db/migrate/20260301120000_add_status_to_orders.rb  (merged and deployed last week)
 class AddStatusToOrders < ActiveRecord::Migration[7.1]
   def change
-    add_column :orders, :status, :string
+    add_column :orders, :status, :string, default: "new", null: false
   end
 end
```

**PASS**

```ruby
# db/migrate/20260310090000_default_orders_status.rb  (new file)
class DefaultOrdersStatus < ActiveRecord::Migration[7.1]
  def change
    change_column_default :orders, :status, from: nil, to: "new"
    change_column_null :orders, :status, false, "new"
  end
end
```

**Counterpoint.** "The migration is broken, and fixing it in place is cheaper." That holds while only your machine has run it. Once any shared environment has, the fix goes in a new migration, because the old file has already done its work there and will not run again.

## chg-approval-tied-to-patch

severity: should-fix  
concerns: process  
applies_when: A review approval or verification result exists and the branch has been pushed or rebased since.  
tool gate: Branch protection that dismisses stale approvals on new commits.  
Backed by: Cursor (unjudged), Anthropic (unjudged), GitLab (supports), Kubernetes (supports), Gerrit Code Review (supports). Backing: strong.

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

**Counterpoint.** "Re-approving after every push is noisy." A rebase that keeps the patch id does not void the verdict, and neither does a change to tests, docs, or lint config that leaves the built output the same. Branch protection can enforce this without human effort. Many review tools drop approvals on any new commit by default, so the exemptions above are the tuned case, not the baseline.

## chg-author-hygiene

severity: should-fix  
concerns: process  
applies_when: Every change submitted for review.  
tool gate: PR template with required sections; branch protection requiring green CI.  
Backed by: Linux kernel (unjudged), Phacility (unjudged), Palantir (unjudged), Kubernetes (unjudged), GitLab (unjudged). Backing: unjudged.

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
tool gate: Contract tests and API-diff tooling.  
Backed by: Python Software Foundation (unjudged), Google (unjudged), Microsoft (unjudged), Kubernetes (unjudged), OpenJDK (unjudged), AWS (unjudged), Pact (unjudged), Spring (unjudged). Backing: unjudged. People cited: Hyrum Wright (unjudged), Michael Feathers (unjudged).

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

## chg-changelog-entry

severity: discuss  
concerns: maintainability, process  
applies_when: The project keeps a changelog, and the change adds, removes or changes a feature.  
Backed by: USGS (unjudged), Ruby on Rails (unjudged), Django Software Foundation (unjudged), Python Software Foundation (unjudged), GitLab (unjudged), Kubernetes (unjudged), Apache Software Foundation (unjudged), Red Hat (unjudged), Grafana Labs (unjudged). Backing: unjudged.

**Rule.** Add a changelog entry to each change that adds, removes or changes a feature.

**Why.** Users and release managers read the changelog, not the diff. A feature change with no entry reaches the release notes late or never, and a removal with no entry surprises whoever depended on it.

**FAIL**

```text
Diff: removes the --legacy flag from the CLI and renames --out to --output.
CHANGELOG.md is untouched.
```

**PASS**

```text
Diff: same change, plus in CHANGELOG.md under "Unreleased":
  - Removed: the --legacy flag.
  - Changed: --out is now --output.
```

**Counterpoint.** "Every fix needs an entry too, or the log is incomplete." Bug fixes, refactors and test changes carry no user-visible feature change, and entries for them bury the ones that matter. Add an entry for a fix only when users must act on it.

## chg-chestertons-fence

severity: should-fix  
concerns: maintainability, process  
applies_when: The change removes, rewrites or "simplifies" odd-looking existing code, or rewrites a module.  
Backed by: Cursor (unjudged), GetYourGuide (supports), Red Hat (supports). Backing: mixed. People cited: Joel Spolsky (unjudged), Michael Feathers (unjudged).

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

## chg-commit-body-says-why

severity: discuss  
concerns: process, maintainability  
applies_when: A change is not trivial enough for its subject line to say everything.  
Backed by: Django Software Foundation (unjudged), Spring (unjudged), Linux kernel (unjudged), Ruby on Rails (unjudged), GNOME (unjudged). Backing: unjudged.

**Rule.** Use the commit body to say why the change was made, not to repeat what the diff shows.

**Why.** The diff already shows what changed. The reason lives only in the author's head, and `git blame` is where the next maintainer looks for it.

**FAIL**

```text
Change timeout from 5 to 30

Changed the timeout constant to 30 seconds.
```

**PASS**

```text
Raise the export timeout to 30 seconds

Large accounts take up to 20 seconds to export, and the 5 second limit
cut them off halfway and left partial files.
```

**Counterpoint.** "The PR description has the reason." Squash merges and mirrors drop it. Keep a line in the commit, and link the PR for the rest.

## chg-commit-subject-imperative

severity: discuss  
concerns: process, maintainability  
applies_when: A change carries a commit message or squash-merge title.  
tool gate: commitlint `subject-max-length` and `subject-case`, or a `commit-msg` hook.  
Backed by: Linux kernel (unjudged), Kubernetes (unjudged), Spring (unjudged), OpenJS Foundation (unjudged), GNOME (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Write the commit subject as a short command in the imperative, about 50 characters and at most 72, with no trailing period.

**Why.** The subject is what `git log --oneline`, blame views and release tooling show. An imperative line reads as what applying the change does, and a short one is not cut off.

**FAIL**

```text
Fixed the bug where the importer sometimes crashed when a row was empty.
```

**PASS**

```text
Skip empty rows in the importer
```

**Counterpoint.** "Our project uses past tense, or conventional-commit types." The rule is consistency and a short line. Follow the project's convention where one is written down, and check it in a hook.

## chg-commit-title-area-prefix

severity: discuss  
concerns: process, maintainability  
applies_when: The project has several subsystems or packages and writes commit or PR titles as `area: summary`.  
tool gate: commitlint `scope-empty` or a PR-title check in CI.  
Backed by: Linux kernel (unjudged), OpenJS Foundation (unjudged), Prometheus (unjudged). Backing: unjudged.

**Rule.** Start the commit or PR title with the area it changes, such as `net: summary` or `importer: summary`, where the project uses area prefixes.

**Why.** A one-line log shows which part of the system each change touched, so a reader can scan for their area and a bisect lands on the right owner.

**FAIL**

```text
Skip empty rows
```

**PASS**

```text
importer: skip empty rows
```

**Counterpoint.** "Prefixes eat the 50 characters." They replace words the subject would spend on context anyway. A small repo with one area gains nothing, so the rule applies only where a prefix convention exists.

## chg-delete-legacy-after-migration

severity: should-fix  
concerns: compatibility, maintainability  
applies_when: The change adds a new API, path or config and every caller lives in this repo.  
context: data  
tool gate: Dead-code and unused-export checks.  
Backed by: Cursor (unjudged), Stripe (unjudged), Google (supports), LLVM (supports). Backing: mixed.

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
tool gate: Startup check that fails fast on missing or unknown config keys.  
Backed by: Cursor (unjudged), GitLab (supports), Spring (supports). Backing: mixed.

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

## chg-doc-marks-version-added

severity: discuss  
concerns: compatibility  
applies_when: A diff adds a public feature, option or API that is documented, or changes how a documented one behaves.  
tool gate: Sphinx `versionadded` and `versionchanged` directives with a docs check, or a front-matter lint for a version field.  
Backed by: Django Software Foundation (unjudged), Python Software Foundation (unjudged), OpenJS Foundation (unjudged), Elastic (unjudged). Backing: unjudged.

**Rule.** When a diff adds or changes a documented feature, mark in the docs the version that added or changed it.

**Why.** Readers run many versions. Without a version marker they cannot tell if the option exists in theirs, and the docs cannot be trimmed later without guessing.

**FAIL**

```text
The `--dry-run` flag prints what would change.     (flag added in this diff, no version)
```

**PASS**

```text
The `--dry-run` flag prints what would change.
.. versionadded:: 3.2
```

**Counterpoint.** "Release notes already say it." Release notes are read once at upgrade time. The marker stays on the page where the reader looks it up.

## chg-docs-updated-with-code

severity: should-fix  
concerns: maintainability, process  
applies_when: The diff changes behaviour, an argument, a return value or an error that a comment, docstring, README or doc page describes.  
Backed by: Google (unjudged), Zephyr Project (unjudged), Python Software Foundation (unjudged), Django Software Foundation (unjudged), Apache Software Foundation (unjudged), OpenJS Foundation (unjudged). Backing: unjudged.

**Rule.** Change the comments, docstrings and docs that describe the code in the same diff as the code, or delete them.

**Why.** A doc fixed "later" is a doc that stays wrong. The reviewer sees the old text and the new behaviour side by side only in this diff, so this is the cheapest place to catch the mismatch.

**FAIL**

```text
- def fetch(url, retries=3):   # retries up to 3 times
+ def fetch(url, retries=0):   # retries up to 3 times
```

**PASS**

```text
- def fetch(url, retries=3):   # retries up to 3 times
+ def fetch(url, retries=0):   # no retries unless the caller asks
```

**Counterpoint.** "Doc fixes bloat the diff and slow the change." Fixing the text is a line or two, and a separate doc PR is rarely sent. If the text cannot be fixed now, delete it.

## chg-each-commit-builds

severity: discuss  
concerns: process, testing, maintainability  
applies_when: A change is submitted as several commits that are kept, not squashed.  
tool gate: A CI job that checks out each commit and runs the build and tests (`git rebase --exec`, `git bisect run`).  
Backed by: Linux kernel (unjudged), Prometheus (unjudged), Django Software Foundation (unjudged). Backing: unjudged.

**Rule.** Make each commit in a series build and pass the tests on its own.

**Why.** `git bisect` can land on any commit. A broken one in the middle of a series sends the person bisecting after a bug that the next commit already fixes.

**FAIL**

```text
commit 1: Rename Config.timeout to Config.deadline   (callers still use timeout; build fails)
commit 2: Update callers to deadline
```

**PASS**

```text
commit 1: Add Config.deadline, keep Config.timeout as an alias
commit 2: Move callers to deadline
commit 3: Remove Config.timeout
```

**Counterpoint.** "We squash on merge." Then the squashed commit is the unit and the rule is met by CI on the PR. The rule matters where the series is kept.

## chg-expand-contract

severity: block  
concerns: compatibility  
applies_when: The change renames, removes or reshapes a column, API field, message, config key or exported symbol that other code reads.  
context: data  
tool gate: Schema or API diff tools (breaking-change detectors) in CI.  
Backed by: Python Software Foundation (unjudged), GitLab (unjudged), Stripe (unjudged), Kubernetes (unjudged), Microsoft (unjudged). Backing: unjudged. People cited: Hyrum Wright (unjudged).

**Rule.** Evolve shared contracts in steps: add the new form beside the old (expand), migrate every consumer, then remove the old form (contract) in a later change.

**Why.** Producers and consumers deploy at different times. A one-step rename breaks whichever side is still on the old version. Start writing both forms before any reader moves to the new one, and backfill old rows, or a reader sees stale or empty values.

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

## chg-flag-both-states-tested

severity: should-fix  
concerns: testing  
applies_when: The change adds or edits code behind a feature flag.  
tool gate: Test helper that runs the flagged suite once per flag state, or a CI job that fails when a flag has tests for one state only.  
Backed by: GitLab (unjudged), GrowthBook (unjudged), Unleash (unjudged). Backing: unjudged.

**Rule.** Test the flagged behaviour with the flag on and with the flag off for as long as the flag exists.

**Why.** The off path is the one production runs until rollout, and the one it falls back to when the flag is turned off in an incident. A suite that sets the flag on leaves that path unchecked, and it breaks unseen. See [chg-tests-ship-with-change](change.md#chg-tests-ship-with-change) for the general rule.

**FAIL**

```python
def test_checkout_total(monkeypatch):
    monkeypatch.setattr(flags, "is_on", lambda name: True)
    assert checkout(cart).total == 90   # only the new path is tested
```

**PASS**

```python
@pytest.mark.parametrize("enabled,total", [(True, 90), (False, 100)])
def test_checkout_total(monkeypatch, enabled, total):
    monkeypatch.setattr(flags, "is_on", lambda name: enabled)
    assert checkout(cart).total == total
```

**Counterpoint.** "Two states double the test cost, and many flags multiply it." Test each flag in both states on its own, with the others at their defaults, rather than every combination. Remove the flag soon after rollout and the second state goes with it.

## chg-flag-fallback-chosen

severity: should-fix  
concerns: reliability  
applies_when: The change evaluates a feature flag or kill switch in code.  
Backed by: ConfigCat (unjudged), GrowthBook (unjudged), PostHog (unjudged), LaunchDarkly (unjudged). Backing: unjudged.

**Rule.** Pass each flag evaluation a fallback chosen for the outcome if the flag service fails, and do not assume `false`.

**Why.** When the flag service is down, the SDK returns the fallback. For a switch that disables a payment path or a safeguard, `false` turns off the thing you need most. A fallback that nobody chose is a decision made by the default argument. For tests of the fallback path, see [prod-kill-switch-fallback](production.md#prod-kill-switch-fallback).

**FAIL**

```python
# "payments-enabled" is true in production. A flag outage returns False.
enabled = client.variation("payments-enabled", context, False)
```

**PASS**

```python
# Fallback True: during a flag outage keep taking payments.
enabled = client.variation("payments-enabled", context, True)
```

**Counterpoint.** "Ship new features off." That holds for a release flag, where the fallback is the old behaviour. It is a choice made per flag, and it is wrong for a flag whose off state removes a safeguard or a required path.

## chg-flag-naming-convention

severity: discuss  
concerns: maintainability, process  
applies_when: The change adds a feature flag or renames one.  
tool gate: Flag registry linter that checks each key against the documented pattern and rejects a key that was deleted before.  
Backed by: Unleash (unjudged), LaunchDarkly (unjudged), ConfigCat (unjudged), Flagsmith (unjudged), GrowthBook (unjudged). Backing: unjudged.

**Rule.** Name each new flag by the team's written convention, and never give a deleted flag's key to different behaviour.

**Why.** Names such as `test2` or `new_thing` hide what a flag does and who owns it, so nobody dares to remove it. A key that comes back with a new meaning can match old code, caches or telemetry that still refer to the earlier flag and switch on behaviour nobody meant to enable.

**FAIL**

```yaml
# flags.yaml
flags:
  - key: newThing          # no area, type or purpose
  - key: test2
  - key: checkout.release.one-page-flow   # deleted last quarter, reused for a pricing experiment
```

**PASS**

```yaml
# flags.yaml  (convention in docs/flags.md: <area>.<type>.<behaviour>)
flags:
  - key: checkout.release.one-page-flow
  - key: search.experiment.semantic-ranking
  - key: pricing.experiment.annual-discount-banner   # new key, the old one stays retired
```

**Counterpoint.** "The pattern is bikeshedding." The exact pattern does matter little; sources disagree on it. What is checked is that one written pattern exists, the new key follows it, and retired keys are not reused. A lint over the registry makes that cheap.

## chg-flag-owner-retirement

severity: should-fix  
concerns: reliability  
applies_when: The change adds a feature flag, kill switch or config toggle.  
tool gate: Flag registry linter that requires owner and expiry fields.  
Backed by: Dropbox (unjudged), Statsig (unjudged), GitLab (unjudged), Google (unjudged), Unleash (unjudged), LaunchDarkly (unjudged), Harness (unjudged), GrowthBook (unjudged), ConfigCat (unjudged), FeatBit (unjudged), Flagsmith (unjudged), Optimizely (unjudged). Backing: unjudged. People cited: tef (programmingisterrible) (unjudged).

**Rule.** Give every new flag an owner, a removal condition or date and a removal ticket, mark flags meant to stay as permanent, and remove the others and their dead branches once rollout ends.

**Why.** A flag without an owner becomes a permanent fork of behaviour that nobody dares delete and that multiplies test paths. Opening the removal ticket with the flag, while the context is fresh, schedules the removal before the rollout starts. The off state of a flag is not always the safe one when evaluation fails; see [chg-flag-fallback-chosen](change.md#chg-flag-fallback-chosen).

**FAIL**

```python
if flags.get("new_checkout"):   # who owns it? when does it go?
    ...
```

**PASS**

```python
# flag: new_checkout  owner: payments
# remove when 100% for 2 weeks (ticket PAY-88), temporary
if flags.get("new_checkout"): ...
```

**Counterpoint.** Some flags are permanent, such as kill switches and entitlements. Label them as permanent, with an owner, and skip the removal condition. The check is that the intent is explicit.

## chg-match-codebase-pattern

severity: should-fix  
concerns: correctness, maintainability  
applies_when: The change adds code that solves a problem the codebase already solves somewhere.  
tool gate: Repeated style nits mean a missing linter or formatter rule; add the gate instead of commenting.  
Backed by: Google (unjudged), The Pragmatic Engineer (unjudged), Python Software Foundation (unjudged), Microsoft (unjudged). Backing: unjudged.

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

## chg-migration-add-column-rewrite

severity: should-fix  
concerns: compatibility  
applies_when: A migration adds a column to a large PostgreSQL table.  
context: data  
tool gate: Migration linter that flags volatile defaults, stored generated columns and identity columns on ADD COLUMN.  
Backed by: PostgreSQL (unjudged), PayPal (supports), Retool (supports). Backing: mixed.

**Rule.** Add the column nullable or with a constant default, then fill volatile, computed, or identity values in batches.

**Why.** A constant or NULL default is a metadata change. A volatile default, a stored generated column, or an identity column rewrites the whole table, and the default lock (ACCESS EXCLUSIVE) blocks every query on it for the duration.

**FAIL**

```sql
ALTER TABLE events ADD COLUMN token uuid DEFAULT gen_random_uuid();   -- volatile: rewrites 400M rows
```

**PASS**

```sql
ALTER TABLE events ADD COLUMN token uuid;                 -- no rewrite
-- backfill in batches, then SET DEFAULT for new rows only
```

**Counterpoint.** "The table is small." Then the rewrite is cheap and the one-step form is fine. State the row count in the description. [sys-migration-lock-timeout](system.md#sys-migration-lock-timeout) covers locking and timeouts.

## chg-name-attack-surface

severity: should-fix  
concerns: security, process  
applies_when: The change adds an endpoint, input parser, file upload, dependency, permission, secret or outbound call.  
tool gate: SAST and dependency scanning in CI catch the mechanical part.  
Backed by: Google (unjudged), OWASP (unjudged), Mozilla (unjudged), Python Software Foundation (supports). Backing: mixed.

**Rule.** List any new attack surface in the description.

**Why.** A generalist reviewing a diff will not spot an exposed route the author never mentioned. A new input, trust boundary, credential, or dependency counts, and security-relevant changes go to a qualified reviewer.

**FAIL**

```text
PR "add debug endpoint /admin/dump". Description: "helper for support".
Auth not mentioned, merged by one general reviewer.
```

**PASS**

```text
Description: "new endpoint, admin-only via role X, rate limited, no PII".
Security reviewer tagged. Randomness uses a crypto source.
```

**Counterpoint.** Naming threats on every PR is theatre. Only changes that add one of the listed surfaces need the section, and most PRs write "none".

## chg-new-dependency-justified

severity: should-fix  
concerns: maintainability  
applies_when: The change adds a third-party package, library or vendored source tree.  
tool gate: A PR template or CI check that asks for the reason when a manifest gains a dependency.  
Backed by: Google (unjudged), Kubernetes (unjudged), OpenSSF (unjudged). Backing: unjudged.

**Rule.** When a change adds a dependency, say why it is needed and which existing dependency or own code was considered instead.

**Why.** Every dependency is code the team did not write and must keep updating, a licence to satisfy and a new route for a supply-chain attack. A package added for one helper function keeps costing for years. A reviewer can only weigh the cost if the change names the need, and it also helps to name the licence and who maintains the package. See [chg-reuse-before-write](change.md#chg-reuse-before-write) for reuse inside the codebase and [code-dependency-licence-sbom](codebase.md#code-dependency-licence-sbom) for the licence check.

**FAIL**

```text
PR: "add left-pad"
diff: package.json  + "left-pad": "^1.3.0"
```

**PASS**

```text
PR: "Add dateutil for recurring-event expansion"
Needed: RRULE parsing; 400 lines to write and test ourselves.
Considered: stdlib datetime (no RRULE), the existing icalendar dependency (parses but does not expand).
Licence: BSD-3. Maintained: active, last release 2 months ago.
```

**Counterpoint.** "A one-line justification for a small utility is review friction." Scale it by risk: a dev-only tool needs a sentence, a runtime or security-sensitive package needs the full note. The check is that a reason exists, not that every package gets an essay.

## chg-no-per-user-ide-files

severity: should-fix  
concerns: process, maintainability  
applies_when: A change adds a tracked file under an editor or IDE project directory.  
tool gate: A CI step that fails when `git ls-files | rg '(^|/)(\.idea/workspace\.xml|\.idea/shelf/|xcuserdata/)|\.xcuserstate$'` prints a path. `git ls-files -ci --exclude-standard` lists only tracked files that already match an ignore entry, so it misses a repository with no entry.  
Backed by: GitHub (unjudged), Git (unjudged), JetBrains (unjudged), Microsoft (unjudged), Apple (unjudged). Backing: unjudged.

**Rule.** Do not commit a file that holds one developer's editor or IDE state; ignore those paths in the repository or a machine-wide exclude file. An ignore entry does not untrack a file already committed: remove it from the index with `git rm --cached`.

**Why.** Per-user state changes on every IDE session and every machine, so it adds diff noise and merge conflicts. The shared files are the ones a teammate or CI needs. JetBrains says `.idea` holds both user-specific settings that "should not be placed under version control" and project settings "normally shared among developers". Microsoft says workspace settings in `.vscode` are "shared by all users of that project". Git and GitHub offer the repository `.gitignore` for paths everyone hits and a machine-wide exclude for a path only one developer has.

**FAIL**

```text
git diff --cached --name-only
.idea/workspace.xml
xcuserdata/alice.xcuserdatad/xcschemes/App.xcscheme
.gitignore            # no entry for either path
```

**PASS**

```text
# .gitignore
.idea/workspace.xml
.idea/shelf/
xcuserdata/
*.xcuserstate

# committed
.idea/codeStyles/Project.xml
.vscode/settings.json
App.xcodeproj/xcshareddata/xcschemes/App.xcscheme
```

**Counterpoint.** "A blanket ignore throws away the run configurations and schemes the team shares." Those live in shared locations: `.idea/runConfigurations/`, `.vscode/launch.json`, `xcshareddata/xcschemes/`. Commit those and ignore `workspace.xml` and `xcuserdata`. In a one-developer repository, put the path in the machine-wide exclude instead of the shared ignore file.

## chg-no-silenced-diagnostics

severity: should-fix  
concerns: correctness, maintainability, process  
applies_when: The diff adds a suppression (lint ignore, type ignore, skipped test, swallowed error) or deletes a failing check.  
tool gate: Linter rule that requires a reason and ticket on each suppression.  
Backed by: Google (unjudged), Palantir (unjudged), Cursor (unjudged), thoughtbot (unjudged), ESLint (supports), Rust project (supports). Backing: mixed.

**Rule.** Name the rule, the reason, and a ticket on every suppression; a swallowed error, skipped test, or disabled check is a FAIL unless justified.

**Why.** Silencing a diagnostic hides the problem it reports and removes the safety net for the next author. An exception with an expiry date fails the check again when it lapses, so it cannot stay forever.

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

## chg-no-special-case-branches

severity: should-fix  
concerns: maintainability  
applies_when: The change adds a conditional, flag or nullable mode to code that serves more than one feature.  
tool gate: Microsoft CA1502 (cyclomatic complexity, default 25) or PMD CognitiveComplexity (default 15) on the shared function.  
Backed by: Linux kernel (unjudged), Google (unjudged), Microsoft (unjudged), PMD (unjudged), Shopify (unjudged), Cursor (unjudged). Backing: unjudged.

**Rule.** Put a new case behind its own function or type; do not add a one-off branch to a shared flow.

**Why.** Each special case in a shared path is a condition that every later reader and every other feature must reason about. The cases accumulate until nobody can say what the path does.

**FAIL**

```text
def checkout(cart, user):
    ...
    if user.org == "acme":            # added for one customer
        total = total * 0.9
```

**PASS**

```text
def checkout(cart, user, pricing=standard_pricing):
    total = pricing(cart, user)       # acme's rule lives in its own pricing function
```

**Counterpoint.** "It is one line; an abstraction is overkill." One is fine. The second and third special case are the signal. See [mod-yagni](module.md#mod-yagni) for when not to extract yet..

## chg-one-concern

severity: should-fix  
concerns: process  
applies_when: Every change.  
tool gate: A CI check can label or warn on file count and diff size.  
Backed by: Linux kernel (unjudged), Python Software Foundation (unjudged), Phacility (unjudged), Palantir (unjudged). Backing: unjudged.

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
Backed by: Cursor (unjudged), Linux kernel (unjudged), GitLab (unjudged), Phacility (unjudged). Backing: unjudged.

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
tool gate: `buf breaking` with the wire and JSON rule sets.  
Backed by: Google (unjudged), Buf (supports), Istio (supports). Backing: mixed.

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

## chg-proto-reserve-removed-fields

severity: should-fix  
concerns: compatibility  
applies_when: The diff deletes a field or enum value from a `.proto` message or enum.  
tool gate: `buf breaking` or an equivalent descriptor diff in CI.  
Backed by: Google (unjudged), Microsoft (supports), Deliveroo (supports). Backing: mixed.

**Rule.** When you delete a protobuf field or enum value, add `reserved` for its number and name in the same change, and never reuse a number.

**Why.** Old data and old clients still carry the number. A new field that takes it is read as the old type, and the failure is silent corruption, not an error. Renumbering a live field breaks old data the same way.

**FAIL**

```proto
message Order {
-  string coupon = 4;
+  int32 loyalty_points = 4;   // number 4 reused
}
```

**PASS**

```proto
message Order {
  reserved 4;
  reserved "coupon";
  int32 loyalty_points = 5;
}
```

**Counterpoint.** "Nobody sends field 4 any more." Stored messages, queued messages and a client on last month's build do. Reserving costs one line and cannot be undone by accident.

## chg-refactor-has-behaviour-pin

severity: should-fix  
concerns: testing, maintainability  
applies_when: The change restructures code and claims to keep its behaviour.  
tool gate: Snapshot or golden-file tests in CI.  
Backed by: Cursor (unjudged), GitHub (unjudged), Stripe (unjudged), SonarSource (unjudged), JetBrains (unjudged), Apache Software Foundation (unjudged). Backing: unjudged.

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
tool gate: A formatter check in CI removes the reformatting case.  
Backed by: Linux kernel (unjudged), Google (unjudged), Apache Software Foundation (unjudged), Python Software Foundation (unjudged), LLVM (unjudged). Backing: unjudged. People cited: Henrik Warne (unjudged), Kent Beck (unjudged).

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
tool gate: Clone-detection in CI (jscpd, PMD CPD, or similar) can flag near-duplicate blocks.  
Backed by: GitHub (unjudged), Cursor (unjudged), Google (unjudged), Linux kernel (unjudged), Refactoring.Guru (unjudged). Backing: unjudged. People cited: Sébastien Portebois (unjudged).

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
tool gate: Formatter, linter and type checker own style and mechanical rules.  
Backed by: Google (unjudged), Slack (unjudged), The Pragmatic Engineer (unjudged), Microsoft (unjudged), Meta (unjudged), Anthropic (unjudged). Backing: unjudged.

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
tool gate: Migration linter requiring a down step; deploy pipeline with automatic abort.  
Backed by: Anthropic (unjudged), Google (unjudged), GitLab (supports), Microsoft (supports), AWS (supports). Backing: strong. People cited: tef (programmingisterrible) (unjudged).

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
tool gate: Size labels or a diff-size warning in CI.  
Backed by: Google (unjudged), Microsoft (unjudged), SmartBear (unjudged), The Pragmatic Engineer (unjudged), US Department of Veterans Affairs (unjudged), USGS (unjudged), Apache Software Foundation (unjudged), Godot Engine (unjudged), Ethereum Foundation (unjudged). Backing: unjudged.

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
tool gate: Coverage-delta or "changed source without changed tests" check in CI.  
Backed by: Kubernetes (unjudged), Python Software Foundation (unjudged), Google (unjudged), Rust project (unjudged), Ruby on Rails (unjudged), Microsoft (unjudged), Mozilla (unjudged), Django Software Foundation (unjudged). Backing: unjudged.

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

## chg-ui-change-screenshots-and-keyboard-pass

severity: should-fix  
concerns: accessibility, usability, process  
applies_when: The change alters markup, styles, or behaviour a user sees or operates.  
context: ui  
tool gate: A pull request template with a UI checklist; the screenshots and the keyboard result are the evidence.  
Backed by: W3C (unjudged), WebAIM (unjudged), GOV.UK (unjudged), WordPress (unjudged), Elastic (unjudged), Mozilla (unjudged). Backing: unjudged.

**Rule.** A UI change shows before-and-after screenshots and says what a keyboard-only pass and a 200% zoom check found on the changed screens.

**Why.** A reviewer reading a diff cannot see focus, order, or overflow. A screenshot shows the visual change, and the keyboard pass shows what the diff hides: a lost focus ring, a trap, a control that cannot be reached.

**FAIL**

```text
PR: "Redesign the settings dialog"
Files: Settings.tsx, settings.css
(no screenshots, no mention of keyboard or zoom)
```

**PASS**

```text
PR: "Redesign the settings dialog"
Before / after: screenshots attached (default and 200% zoom).
Keyboard: Tab reaches every control in order, Esc closes, focus returns to the gear button.
Not covered: screen reader, not tested.
```

**Counterpoint.** "Automated checks run in CI." They find a minority of problems. They cannot tell that Tab order is wrong or that focus vanished. Say what you did not test, as the last line shows.

## chg-verify-before-claim

severity: block  
concerns: testing, process  
applies_when: The author or reviewer asserts the change works or a finding is real.  
Backed by: Python Software Foundation (unjudged), Phacility (unjudged), Google (unjudged), Anthropic (unjudged), GitLab (unjudged). Backing: unjudged. People cited: Dan Luu (unjudged).

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

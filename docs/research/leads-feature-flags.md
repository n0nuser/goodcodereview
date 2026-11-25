# Feature-flag lifecycle leads

Method: pages fetched with `curl -sL`, tags stripped with `python3 -I`, sentence found with `rg` in the stripped text. Fetch date 2026-11-24, about 45 fetches. Quotes are short; the rest is paraphrase. Search-engine summaries were used only to find URLs, never as evidence. Org grouping follows docs/PROMOTION.md; Split and Harness are one org (the Split "dos and don'ts" post now lives on harness.io). Martin Fowler and Pete Hodgson are persons, reference only, not counted. Not fetchable as text (JS shells or 404): Flagsmith docs site, FeatBit docs root, ConfigCat docs, Optimizely support, Harness FME docs; blog or alternate pages were used instead. Flipt v2 has no best-practice page of its own; the Git-native post found is by a third party (bex.co), not counted.

## PROMOTION rule 3 and vendor docs

Rule 3 says a source counts when it "states a practice" (a recommendation, a standard, or a team's description of what it does and why). Excluded: plans, definition pages, secondary summaries, and "a vendor page that restates another organisation's guidance". So a vendor page counts when the sentence is advice to the reader or the vendor's own practice ("Give them owners", "remove the flag"). It does not count when it only describes a product feature ("GrowthBook can automatically detect stale flags", "Statsig auto-assigns an owner", an SDK API signature). I applied that line below. Vendor pages that mostly cite Fowler's categories (Unleash, LD, Harness) are borderline under the "restates" exclusion, but each adds its own prescriptions, so I counted them. Conflict of interest (they sell the tool) is not an exclusion in rule 3; the existing card already treats vendors as counting.

## Count per clause

| Clause | Firm orgs | Orgs | Verdict |
|---|---|---|---|
| Remove flag and dead branch after rollout | 11 | Chromium, GitLab, Unleash, LaunchDarkly, Statsig, Flagsmith, Split/Harness, Optimizely, PostHog, FeatBit, GrowthBook | clears (already in card) |
| Owner | 7 | Unleash, LaunchDarkly, Split/Harness, GrowthBook, ConfigCat, Optimizely, FeatBit (long-lived flags); plus Dropbox already in card | clears |
| Expiry date or removal condition | 7 | Chromium, Unleash, Optimizely, FeatBit, ConfigCat, GrowthBook, Split/Harness | clears |
| Removal ticket or task made at creation | 3 + 1 partial | Statsig, Unleash, GrowthBook; GitLab partial | clears 3, thin |
| New flag defaults off | 1 firm | GitLab; Chromium soft (code sample only); LaunchDarkly soft | short |
| Explicit fallback when evaluation fails (new lead) | 4 | ConfigCat, GrowthBook, LaunchDarkly, PostHog; OpenFeature API soft | clears |
| Short-lived release flags vs long-lived ops and permission flags, labelled | 7 | GitLab, Unleash, LaunchDarkly, Flagsmith, Split/Harness, FeatBit, ConfigCat, GrowthBook | clears |
| Kill switch kept deliberately, owned, still works | 4 | FeatBit, GrowthBook, Split/Harness, Unleash/LD (exception only) | clears 3 for "owned and exercised" |
| Flag naming convention | 7 | Unleash, LaunchDarkly, ConfigCat, Flagsmith, Split/Harness, GrowthBook, FeatBit | clears |
| Tests cover both flag states | 3 | GitLab, GrowthBook, Unleash | clears 3 |

## Which clauses of `chg-flag-owner-retirement` reach 3

- Removal: yes (11). Already in the Rule.
- Owner: yes (7). Already in the Rule; evidence is much stronger than the card's note shows.
- Expiry date or removal condition: yes (7).
- Removal ticket: yes at exactly 3 firm (Statsig, Unleash, GrowthBook) plus GitLab's roll-out issue. It can move from Why into the Rule, with Why still carrying the PR link detail.
- Default off: no. Only GitLab states it as a rule. Worse, GrowthBook says "False is not universally safe" for a failure default, so "ship off" and "fallback is chosen per flag" pull apart. Keep it in the Why, or replace with the fallback lead (below).

## Leads

### 1. Every flag has a named owner (team) that outlives the author
Rule candidate: flag registry entry or code comment names an owner team. FAIL: `flags.get("x")` with no owner field. Nearest card: `chg-flag-owner-retirement` (clause already in it, now well sourced). Not a new card.
1. Unleash, https://docs.getunleash.io/topics/feature-flags/feature-flag-best-practices : "Give them owners, set expiration dates, and add cleanup tasks". Its FAQ: "Set an expiration date and assign an owner when you create the flag."
2. LaunchDarkly, https://launchdarkly.com/docs/guides/flags/technical-debt : each view "has a maintainer", "a good way to record who is responsible for cleaning up a given set of flags".
3. Split/Harness, https://www.harness.io/blog/dos-and-donts-of-feature-flags : "Each feature flag should be owned by a single team".
4. GrowthBook, https://www.growthbook.io/insights/feature-flag-best-practices : "Every flag needs a team, not just the person who created it."
5. ConfigCat, https://configcat.com/blog/feature-flag-best-practices/ : "every flag should have a named owner (a team, a squad, or a specific person)".
6. Optimizely, https://www.optimizely.com/insights/blog/manage-outdated-feature-flags/ : Removal Day is used to "assign owners"; says ownership "isn't always clear".
7. FeatBit, https://docs.featbit.co/feature-flags/flag-lifecycle-management/set-cleanup-expectations : long-lived kill switches "need an owner and runbook"; unclear ownership means `needs-owner-decision`.
Soft: Statsig (a product feature, auto-assigns the creator; the blog also asks "Who's responsible for removing it?").
Caveat: ownership in a tool UI cannot be seen in a diff; the checkable form is an owner comment or registry field. Counterpoint: tiny repos with one team.

### 2. Flag has an expiry date or a stated removal condition
Rule candidate: flag declaration carries expiry or exit criteria. Nearest card: `chg-flag-owner-retirement`. Clause, not a new card.
1. Chromium, https://chromium.googlesource.com/chromium/src/+/main/docs/how_to_add_your_feature_flag.md : the test `AboutFlagsTest.EveryFlagHasMetadata` "will ask you to update the flag expiry metadata in flag-metadata.json".
2. Unleash (above): "Assign expiration dates to feature flags".
3. Optimizely: "You can set expiration dates for your feature flags"; Removal Day checks "that the exit criteria has been met".
4. FeatBit set-cleanup-expectations: "Review after 30 stable days, then remove the temporary branch."
5. ConfigCat (page above): a flag description should say "when it can be deleted".
6. GrowthBook insights: plan "When should it be reviewed or removed?"; cleanup issue lists "expected decision date".
7. Split/Harness: "you should know the criteria for the flag to meet its definition of done"; sunset timelines differ by purpose.
Caveat: Chromium's is the only one machine-enforced. Counterpoint: a date makes a flag expire while the rollout is late; a condition (100% for N days) is the better form.

### 3. A removal ticket exists from the start (clears 3, thin)
Rule candidate: PR that adds a flag links a removal ticket.
1. Statsig, https://www.statsig.com/blog/feature-flag-code-cleanup : "Create a cleanup ticket alongside your rollout"; the PR template links `ENG-1234` with a target date.
2. Unleash: "add cleanup tasks to your backlog".
3. GrowthBook insights: "Open a cleanup issue when the flag is introduced. Include the owner, expected decision date..."
Partial: GitLab requires a rollout issue from the Roll Out template for beta and `gitlab_com_derisk` flags; that issue's steps include the removal MR. Also Flipt-on-Git third-party post (not counted). Counterpoint: ticket debt; tickets "for later" languish (Statsig admits it).

### 4. Fallback value for failed evaluation is chosen and documented (new clause or card)
Rule candidate: every flag evaluation call passes a deliberate fallback, and it is not assumed to be `false`. FAIL: `flags.get("kill_provider")` where fallback `False` leaves a broken provider on; PASS: fallback named for the outcome. Nearest card: `chg-flag-owner-retirement` (its Why says "off by default") and `prod-kill-switch-fallback` (fallback path exercised). New clause; could be a card `chg-flag-fallback-chosen` if a fourth source is wanted beyond these.
1. ConfigCat: flag description should include "what the safe default value is if the flag evaluation fails".
2. GrowthBook insights: "Every evaluation needs an explicit fallback. 'False' is not universally safe." Test it "without the flag service".
3. LaunchDarkly: "Test the fallback values of permanent flags periodically"; a bad fallback "risk[s] falling back to the undesired old UI".
4. PostHog, https://posthog.com/docs/feature-flags/best-practices : "Add per-flag safe defaults and even a cold start during an outage returns usable values."
Soft: OpenFeature spec requires a `default value` argument on every evaluation (an API shape, not advice); Unleash says SDKs should use "last known configuration or defaults" (product behaviour).
Counterpoint: this contradicts a flat "default off". Kill switches may need default-on fallback.

### 5. Short-lived release flags are separated from long-lived ops and permission flags, and labelled
Rule candidate: a flag is marked temporary or permanent when created. Nearest card: `chg-flag-owner-retirement` (counterpoint says "label them as permanent"). Clause; strong enough to move the counterpoint into the Rule.
1. GitLab https://docs.gitlab.com/development/feature_flags/ : each type has a "Maximum Lifespan" (2, 4 or 6 months); "ops feature flags are long-lived".
2. Unleash: "While most feature flags should be short-lived, there are valid exceptions for long-lived flags".
3. LaunchDarkly: "Flags are either temporary or permanent." Toggle "Mark flags as temporary"; archiving a permanent flag warns.
4. Flagsmith, https://www.flagsmith.com/blog/feature-flags-best-practices : release flags "should be deleted once they've served their purpose".
5. Split/Harness: "Some are meant to be permanent"; owners differ by type.
6. FeatBit: cleanup rule per type (release, experiment, migration, operational, permission).
7. ConfigCat: "short-term flags...medium or long-term...permanent flags used as kill switches".
Reference only: Fowler's toggle categories (release, experiment, ops, permissioning).

### 6. Long-lived kill switches are kept on purpose, owned, and the old path still works
Rule candidate: a kill switch flag has an owner and runbook, and its off-path is exercised. Nearest card: `prod-kill-switch-fallback` (stable; exercise the fallback, switch off without deploy). Clause on that card, not new. Count of NEW orgs with a distinct statement on ownership/exercising:
1. FeatBit: "Long-lived kill switches need an owner and runbook."
2. GrowthBook: "A kill switch is useful only if the old path still works"; document "what it disables, expected fallback, propagation time, and owner. Test it in a game day."
3. Split/Harness: "If you're using a flag as a kill switch, your Ops team should manage it."
Soft: Unleash and LaunchDarkly name kill switches or circuit breakers as the valid long-lived flag, with no owner or test rule; Statsig says a kill switch is fine to leave "forever".

### 7. Flags follow a naming convention
Rule candidate: flag key matches a team-agreed pattern (lint). Nearest card: none. New card candidate (change level), tool gate: regex on flag key in the registry.
1. Unleash: "Ensure that all flags...have unique names"; unique naming "prevents the reuse of old flag names".
2. LaunchDarkly: "Create organization-wide naming conventions".
3. ConfigCat, https://configcat.com/blog/feature-flag-naming-conventions/ : pattern `teamname_flagtype_flagfunction`; "Include the Feature Flag Type".
4. Flagsmith: "Introduce consistent feature flag naming conventions".
5. Split/Harness: "implement a naming convention that you follow for all flags"; names should be unique; Policy Engine can enforce.
6. GrowthBook: "Choose a naming convention that communicates domain and purpose"; "do not reuse a deleted key for unrelated behavior".
7. FeatBit: "unique naming conventions across all applications".
Counterpoint: the exact format varies (ConfigCat says format "matters less than consistency"), so the card must demand "a documented convention" and the check is the lint, not a specific pattern. Nearly all sources also add never reuse a deleted key.

### 8. Tests cover both flag states while the flag exists
Rule candidate: a PR adding a flag has tests for on and off. FAIL: tests only the on path. Nearest card: `chg-tests-ship-with-change` (generic). New card or clause; three firm.
1. GitLab: "As long as the feature flag exists in the codebase, both states should be fully functional (when the feature is on and off)."
2. GrowthBook: "CI should exercise enabled and disabled behavior for release flags."
3. Unleash FAQ: "Test both code paths while the flag is active".
Reference: Fowler: automated tests exercise "the system both with the feature off and with it on". Soft: Chromium suggests a virtual test for flags. Counterpoint: doubles test cost for tiny flags; combinatorial explosion with many flags.

### 9. Not enough
- Default off (see table): 1 firm (GitLab).
- Flag created in the same PR as the code, removal as its own change: GitLab only ("removal should be the only change in an MR"); Flipt-on-Git post third party.
- Flags as config separate: Unleash only, descriptive.
- Single flag per purpose: ConfigCat ("a flag is tied to one purpose only"), GrowthBook ("accumulating several unrelated jobs"), Flagsmith ("flag will cover too much"). Three, but about flag design not lifecycle; possible later card.

## Summary for the parent
Clauses of `chg-flag-owner-retirement` that reach 3: removal, owner, expiry/removal condition, removal ticket (exactly 3). Default off does not. New cards that clear: flag naming (7), both-states tests (3), explicit fallback (4); kill-switch ownership folds into `prod-kill-switch-fallback` (3). Temporary vs permanent labelling (7) moves the card's Counterpoint into its Rule.

---
id: chg-flag-owner-retirement
level: change
tags: [reliability, feature-flags, release]
severity: should-fix
status: stable
lang: core
applies_when: The change adds a feature flag, kill switch or config toggle.
tool_gate: Flag registry linter that requires owner and expiry fields.
note: Removal after rollout - Chromium, GitLab, Unleash, LaunchDarkly, Statsig, Flagsmith, Harness, Optimizely, FeatBit and GrowthBook. Owner - Dropbox (every experiment and feature gate has a clear owner), Unleash, LaunchDarkly (a named maintainer per set of flags), Harness (one owning team), GrowthBook (a team, not just the author), ConfigCat, Optimizely and FeatBit. Expiry date or removal condition - Chromium (flag expiry metadata), Unleash, Optimizely, FeatBit, ConfigCat, GrowthBook and Harness. Removal ticket at creation - Statsig, Unleash and GrowthBook. Permanent flags marked as such - LaunchDarkly (temporary or permanent), GitLab (a type with a maximum lifespan) and ConfigCat (flag type and longevity). The vendors state advice to the reader, so they count under docs/PROMOTION.md rule 3. A default of off has GitLab only, and GrowthBook says false is not universally safe as a fallback, so it left the card; the fallback sits in chg-flag-fallback-chosen
borrowed_from:
  - https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to
  - https://dropbox.tech/infrastructure/lessons-learned-in-incident-management
  - https://statsig.com/blog/feature-flag-code-cleanup
  - https://docs.gitlab.com/ee/development/feature_flags/
  - https://chromium.googlesource.com/chromium/src/+/main/docs/how_to_add_your_feature_flag.md
  - https://docs.getunleash.io/topics/feature-flags/feature-flag-best-practices
  - https://launchdarkly.com/docs/guides/flags/technical-debt
  - https://www.harness.io/blog/dos-and-donts-of-feature-flags
  - https://www.growthbook.io/insights/feature-flag-best-practices
  - https://configcat.com/blog/feature-flag-best-practices/
  - https://docs.featbit.co/feature-flags/flag-lifecycle-management/set-cleanup-expectations
  - https://www.flagsmith.com/blog/feature-flags-best-practices
  - https://www.optimizely.com/insights/blog/manage-outdated-feature-flags/
---

**Rule.** Give every new flag an owner, a removal condition or date and a removal ticket, mark flags meant to stay as permanent, and remove the others and their dead branches once rollout ends.

**Why.** A flag without an owner becomes a permanent fork of behaviour that nobody dares delete and that multiplies test paths. Opening the removal ticket with the flag, while the context is fresh, schedules the removal before the rollout starts. The off state of a flag is not always the safe one when evaluation fails; see [[chg-flag-fallback-chosen]].

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

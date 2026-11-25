---
id: chg-flag-naming-convention
level: change
tags: [maintainability, feature-flags, process]
severity: discuss
status: stable
lang: core
applies_when: The change adds a feature flag or renames one.
tool_gate: Flag registry linter that checks each key against the documented pattern and rejects a key that was deleted before.
note: Documented convention - Unleash (enforce unique naming conventions), LaunchDarkly (organisation-wide naming conventions), ConfigCat (a pattern with team, type and function), Flagsmith (create a naming convention upfront) and GrowthBook (a convention that shows domain and purpose). No reuse of a deleted key - Unleash (unique names prevent reuse of old names), GrowthBook (do not reuse a deleted key for unrelated behaviour), ConfigCat (one purpose per flag, a new purpose gets a new flag) and LaunchDarkly (a new flag with a deleted flag's key can be picked up by old code). The vendors state advice to the reader, so they count under docs/PROMOTION.md rule 3. The exact pattern differs by source and the card does not pick one
borrowed_from:
  - https://docs.getunleash.io/topics/feature-flags/feature-flag-best-practices
  - https://launchdarkly.com/docs/guides/flags/technical-debt
  - https://configcat.com/blog/feature-flag-naming-conventions/
  - https://configcat.com/blog/feature-flag-best-practices/
  - https://www.flagsmith.com/blog/feature-flags-best-practices
  - https://www.growthbook.io/insights/feature-flag-best-practices
---

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

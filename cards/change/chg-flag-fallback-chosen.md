---
id: chg-flag-fallback-chosen
level: change
tags: [reliability, feature-flags]
severity: should-fix
status: stable
lang: core
applies_when: The change evaluates a feature flag or kill switch in code.
tool_gate: none
note: ConfigCat (the flag description says what the safe default is if evaluation fails), GrowthBook (every evaluation needs an explicit fallback and false is not universally safe), PostHog (per-flag safe defaults so a cold start in an outage returns usable values) and LaunchDarkly (test the fallback values of permanent flags periodically). The vendors state advice to the reader, so they count under docs/PROMOTION.md rule 3. The OpenFeature default-value argument is an API shape, not counted
borrowed_from:
  - https://configcat.com/blog/feature-flag-best-practices/
  - https://www.growthbook.io/insights/feature-flag-best-practices
  - https://posthog.com/docs/feature-flags/best-practices
  - https://launchdarkly.com/docs/guides/flags/technical-debt
---

**Rule.** Pass each flag evaluation a fallback chosen for the outcome if the flag service fails, and do not assume `false`.

**Why.** When the flag service is down, the SDK returns the fallback. For a switch that disables a payment path or a safeguard, `false` turns off the thing you need most. A fallback that nobody chose is a decision made by the default argument. For tests of the fallback path, see [[prod-kill-switch-fallback]].

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

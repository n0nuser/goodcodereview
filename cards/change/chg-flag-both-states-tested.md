---
id: chg-flag-both-states-tested
level: change
tags: [testing, feature-flags]
severity: should-fix
status: stable
lang: core
applies_when: The change adds or edits code behind a feature flag.
tool_gate: Test helper that runs the flagged suite once per flag state, or a CI job that fails when a flag has tests for one state only.
note: GitLab (both states should be fully functional while the flag exists), GrowthBook (CI exercises the enabled and disabled behaviour of release flags) and Unleash (test both code paths while the flag is active). The vendors state advice to the reader, so they count under docs/PROMOTION.md rule 3. Martin Fowler's toggles article is a person's reference and not counted
borrowed_from:
  - https://docs.gitlab.com/development/feature_flags/
  - https://www.growthbook.io/insights/feature-flag-best-practices
  - https://docs.getunleash.io/topics/feature-flags/feature-flag-best-practices
---

**Rule.** Test the flagged behaviour with the flag on and with the flag off for as long as the flag exists.

**Why.** The off path is the one production runs until rollout, and the one it falls back to when the flag is turned off in an incident. A suite that sets the flag on leaves that path unchecked, and it breaks unseen. See [[chg-tests-ship-with-change]] for the general rule.

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

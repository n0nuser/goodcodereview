---
id: code-flaky-test-quarantine
level: codebase
tags: [testing, process, ci, flaky-tests]
severity: should-fix
status: draft
lacks: orgs, quarantine with owner and ticket has Dropbox and Shopify; rerun-verified return to the gate has Dropbox only
note: report and route flaky tests - Dropbox (Quarantine Keeper removes tests that fail too often and files a bug against the owner), Shopify (retries a failed test up to three times and notifies developers of every pass after a retry); rerun-verified fix - Dropbox only (100 or more CI runs); causes - Shopify (fixed pauses instead of waits), Cabify (state kept between tests), Dropbox (short timeouts, leftover state); only 2 orgs back the Rule
lang: core
applies_when: Auditing how the codebase handles tests that pass and fail on the same code.
tool_gate: none
borrowed_from:
  - https://dropbox.tech/application/accelerating-iteration-velocity-on-dropboxs-desktop-client-part-1
  - https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents
  - https://shopify.engineering/unreasonable-effectiveness-test-retries-android-monorepo-case-study
  - https://shopify.engineering/mobile-e2e-testing
  - https://tech.cabify.com/blog/engineering/acceptance-testing-go-services-using-aceptadora
---

**Rule.** Report every test that passes only on retry, move it to a quarantine with a named owner and a ticket, and return it to the merge gate only after it passes many reruns.

**Why.** A test that fails at random on unchanged code teaches people to rerun until green, and then a real regression looks like noise. Dropbox removes tests that fail too often from the main pool and files a bug against the owner. Its fix workflow then runs the test 100 or more times in CI before the fix lands. Shopify retries a failed test but tells developers about every pass after a retry. The usual causes are a fixed pause where the test should wait for an element (Shopify) and state left behind by an earlier test (Cabify, Dropbox).

**FAIL**

```yaml
# .github/workflows/test.yml
- run: pytest --reruns 3          # a pass on retry counts as a pass, and nobody hears about it
```

**PASS**

```yaml
# .github/workflows/test.yml
- run: pytest --reruns 3 -m "not quarantine" --junitxml=report.xml
- run: python tools/flaky_report.py report.xml   # opens a ticket per pass after retry, owner from CODEOWNERS
# nightly.yml: a quarantined test rejoins the gate after 100 clean runs
- run: pytest -m quarantine --count 100
```

**Counterpoint.** "Retries keep the build green, and quarantine hides coverage." Shopify's data backs retries: a slightly slower build beats an engineer rerunning it by hand. Retries are fine when each pass after a retry reaches someone. A quarantined test still runs outside the gate, and its owner and ticket stop it from staying there for good. Skipping or deleting a flaky test in a diff is a separate FAIL. See [[chg-no-silenced-diagnostics]]. For the merge gate itself, see [[code-ci-gates]].

---
id: code-vuln-remediation-window
level: codebase
tags: [security, supply-chain, process]
severity: should-fix
status: stable
lang: core
applies_when: The repo has open dependency alerts, update pull requests, or scan reports; with none open, mark it N/A.
tool_gate: Dependabot or Renovate alerts with a severity SLA; OSV-Scanner or Scorecard `Vulnerabilities` in CI.
note: Windows from OpenSSF (60 days for medium and above), CISA (two weeks for exploited CVEs) and GitHub (an SLA per severity). Risk acceptance is OWASP and GitHub only, so it sits in the Why
borrowed_from:
  - https://www.bestpractices.dev/en/criteria/0
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://www.cisa.gov/news-events/directives/bod-22-01-reducing-significant-risk-known-exploited-vulnerabilities
  - https://docs.github.com/en/code-security/securing-your-organization/understanding-your-organizations-exposure-to-vulnerabilities/prioritizing-dependabot-alerts-using-metrics
  - https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html
---

**Rule.** Write down how long a known-vulnerable dependency may stay unfixed and fix or upgrade it inside that window.

**Why.** A scan that finds a vulnerability and then sits unread protects nobody. An alert left open past its window is the failure, whatever the tool says. If a fix is not possible, record the accepted risk with an owner and a review date, so the open alert is a decision and not an oversight. [[code-dependency-licence-sbom]] covers running the scan, and this card covers acting on the result.

**FAIL**

```text
Dependabot: 14 open alerts, 3 critical, oldest opened 210 days ago.
Open update PRs for those alerts: unreviewed. No stated window, no dismissal reason.
```

**PASS**

```text
SECURITY.md: critical and exploited: 7 days; high: 30 days; medium: 60 days.
Open alerts: all younger than their window.
```

**Counterpoint.** "Most alerts are not reachable in our code, so the window is busywork." Then triage the alert inside the window and dismiss it with the reason. Reachability is a finding to record, not a reason to skip the clock.

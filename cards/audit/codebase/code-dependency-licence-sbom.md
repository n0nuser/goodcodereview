---
id: code-dependency-licence-sbom
level: codebase
tags: [security, supply-chain, licences, sbom]
severity: should-fix
status: draft
lang: core
applies_when: Auditing what third-party code the repo ships and under which terms.
tool_gate: Licence checker and vulnerability scan in CI; SBOM generated at release.
note: SBOM and scan from OWASP A03:2025; the licence allowlist is team policy, unsourced
borrowed_from:
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://www.cisa.gov/sbom
  - https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph
---

**Rule.** Generate an SBOM and scan dependencies for known vulnerabilities in CI.

**Why.** Without an inventory, a team cannot answer a disclosed vulnerability quickly. Team policy: also fail the build on a dependency whose licence is not on the approved list.

**FAIL**

```text
No SBOM step, no scanner in CI, GPL-3.0 package pulled into a proprietary build
unnoticed.
```

**PASS**

```text
CI: generate SBOM, run scanner, run licence check against allowlist;
release artifacts attach the SBOM.
```

**Counterpoint.** SBOMs and scanners create noise that nobody triages. Tune severity thresholds and assign an owner, since an ignored report is worse than none. The licence list is team policy, not a universal rule. Drop it if your team has no licence constraints.

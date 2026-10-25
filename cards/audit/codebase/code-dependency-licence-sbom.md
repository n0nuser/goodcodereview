---
id: code-dependency-licence-sbom
level: codebase
tags: [security, supply-chain, licences, sbom]
severity: should-fix
status: stable
lang: core
applies_when: Auditing what third-party code the repo ships and under which terms.
tool_gate: A vulnerability scanner such as OSV-Scanner or Dependabot alerts; an SBOM generator such as Syft.
note: SBOM backed by OWASP, NIST and GitHub; scan by OWASP, OpenSSF, GitHub and Cabify (Trivy at build, running images rescanned every 6 hours); the licence allowlist is team policy, unsourced
borrowed_from:
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
  - https://www.cisa.gov/sbom
  - https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-security-supply-chains-software-1
  - https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/about-the-dependency-graph
  - https://tech.cabify.com/blog/engineering/cabify-container-certification
---

**Rule.** Generate an SBOM, and scan dependencies for known vulnerabilities on every change or on a schedule.

**Why.** Without an inventory, a team cannot answer a disclosed vulnerability quickly. CI is the usual place for both steps: the SBOM then matches what was built, and the scan runs without anyone remembering it. Team policy: also fail the build on a dependency whose licence is not on the approved list.

**FAIL**

```text
No SBOM anywhere, no scanner in CI, and dependency alerts turned off.
```

**PASS**

```text
CI: generate SBOM, run vulnerability scanner, fail on high severity;
release artifacts attach the SBOM.
```

**Counterpoint.** SBOMs and scanners create noise that nobody triages. Tune severity thresholds and assign an owner, since an ignored report is worse than none. The licence list is team policy, not a universal rule. Drop it if your team has no licence constraints.

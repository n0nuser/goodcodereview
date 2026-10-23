---
id: code-dependency-licence-sbom
level: codebase
tags: [supply-chain, licences, sbom]
severity: should-fix
status: draft
lang: core
applies_when: Auditing what third-party code the repo ships and under which terms.
tool_gate: Licence checker and vulnerability scan in CI; SBOM generated at release.
borrowed_from:
  - https://owasp.org/Top10/2025/A03_2025-Software_Supply_Chain_Failures/
  - https://github.com/ossf/scorecard/blob/main/docs/checks.md
---

**Rule.** The repo can produce an SBOM, runs a dependency-vulnerability scan in CI, and fails on dependencies whose licence is not on the approved list.

**Why.** Without an inventory, a disclosed vulnerability or a licence conflict cannot be answered quickly.

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

**Counterpoint.** SBOMs and scanners create noise that nobody triages. Answer: tune severity thresholds and assign an owner, since an ignored report is worse than none. OWASP A03:2025 lists the missing-SBOM and missing-scan checks; the licence part comes from our judgement and has no source in the notes.

---
id: chg-new-dependency-justified
level: change
tags: [maintainability, supply-chain, dependencies]
severity: should-fix
status: stable
lang: core
applies_when: The change adds a third-party package, library or vendored source tree.
tool_gate: A PR template or CI check that asks for the reason when a manifest gains a dependency.
note: Chromium and the Google SWE book (motivation, alternatives considered, who keeps it up to date; one organisation), the Kubernetes dependency checklist (is a similar dependency already present, is the licence compatible) and the OpenSSF evaluation guide (every new dependency is a possible supply-chain or support problem, so eliminate unnecessary ones)
borrowed_from:
  - https://chromium.googlesource.com/chromium/src/+/main/docs/adding_to_third_party.md
  - https://abseil.io/resources/swe-book/html/ch21.html
  - https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-architecture/vendor.md
  - https://best.openssf.org/Concise-Guide-for-Evaluating-Open-Source-Software
---

**Rule.** When a change adds a dependency, say why it is needed and which existing dependency or own code was considered instead.

**Why.** Every dependency is code the team did not write and must keep updating, a licence to satisfy and a new route for a supply-chain attack. A package added for one helper function keeps costing for years. A reviewer can only weigh the cost if the change names the need, and it also helps to name the licence and who maintains the package. See [[chg-reuse-before-write]] for reuse inside the codebase and [[code-dependency-licence-sbom]] for the licence check.

**FAIL**

```text
PR: "add left-pad"
diff: package.json  + "left-pad": "^1.3.0"
```

**PASS**

```text
PR: "Add dateutil for recurring-event expansion"
Needed: RRULE parsing; 400 lines to write and test ourselves.
Considered: stdlib datetime (no RRULE), the existing icalendar dependency (parses but does not expand).
Licence: BSD-3. Maintained: active, last release 2 months ago.
```

**Counterpoint.** "A one-line justification for a small utility is review friction." Scale it by risk: a dev-only tool needs a sentence, a runtime or security-sensitive package needs the full note. The check is that a reason exists, not that every package gets an essay.

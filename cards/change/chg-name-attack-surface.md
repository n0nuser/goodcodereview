---
id: chg-name-attack-surface
level: change
tags: [security, process, review]
severity: block
status: draft
lang: core
applies_when: The change adds an endpoint, input parser, file upload, dependency, permission, secret or outbound call.
tool_gate: SAST and dependency scanning in CI catch the mechanical part.
note: thin sourcing: routing to a qualified reviewer and crypto randomness only; the rest is synthesis
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://go.dev/wiki/CodeReviewComments
  - https://cheatsheetseries.owasp.org/cheatsheets/Attack_Surface_Analysis_Cheat_Sheet.html
  - https://wiki.mozilla.org/Security/Reviews
---

**Rule.** List any new attack surface in the description.

**Why.** A generalist reviewing a diff will not spot an exposed route the author never mentioned. A new input, trust boundary, credential, or dependency counts, and security-relevant changes go to a qualified reviewer.

**FAIL**

```text
PR "add debug endpoint /admin/dump". Description: "helper for support".
Auth not mentioned, merged by one general reviewer.
```

**PASS**

```text
Description: "new endpoint, admin-only via role X, rate limited, no PII".
Security reviewer tagged. Randomness uses a crypto source.
```

**Counterpoint.** Naming threats on every PR is theatre. Only changes that add one of the listed surfaces need the section, and most PRs write "none".

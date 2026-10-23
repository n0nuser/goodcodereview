---
id: chg-name-attack-surface
level: change
tags: [security, review]
severity: block
status: draft
lang: core
applies_when: The change adds an endpoint, input parser, file upload, dependency, permission, secret or outbound call.
tool_gate: SAST and dependency scanning in CI catch the mechanical part.
borrowed_from:
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://go.dev/wiki/CodeReviewComments
---

**Rule.** The description lists any new attack surface (new input, trust boundary, credential, dependency) and security-relevant changes are routed to a qualified reviewer.

**Why.** A generalist reviewing a diff will not spot an exposed route that the author never mentioned.

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

**Counterpoint.** Naming threats on every PR is theatre. Answer: only changes that add one of the listed surfaces need the section; most PRs write "none". The notes give only the routing and crypto-randomness checks; the rest is our synthesis, so the card stays draft.

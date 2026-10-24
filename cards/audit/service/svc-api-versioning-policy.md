---
id: svc-api-versioning-policy
level: service
tags: [compatibility, api, versioning]
severity: should-fix
status: stable
note: the three sources pick three different mechanisms; the card requires only that one is chosen and documented
lang: core
applies_when: A service offers an HTTP API to callers you do not deploy together with it.
tool_gate: Spec diff in CI that fails on a breaking change inside a published version.
borrowed_from:
  - https://opensource.zalando.com/restful-api-guidelines/
  - https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md
  - https://docs.stripe.com/api/versioning
---

**Rule.** Write down one versioning scheme for the API, and ship no breaking change inside a version it has published.

**Why.** Callers upgrade on their own schedule. With no stated scheme, each breaking change is a surprise, and each team invents its own v2.

**FAIL**

```text
GET /orders   # renamed total -> amount_total
no version marker anywhere; README says "we try not to break things"
```

**PASS**

```text
docs/api-versioning.md: dated api-version query parameter, previews last 6 months, 90 days' notice
GET /orders?api-version=2026-03-01 keeps returning "total"
the rename ships under api-version=2026-09-01
```

**Counterpoint.** "We will cross that bridge later." Later arrives with a customer on the old shape. The scheme can be minimal. A media type, a dated query parameter and a pinned header all work. Pick one and write it down. What counts as breaking is in [[chg-breaking-change-taxonomy]].

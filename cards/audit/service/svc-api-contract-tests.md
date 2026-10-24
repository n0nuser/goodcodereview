---
id: svc-api-contract-tests
level: service
tags: [compatibility, testing, api, contracts]
severity: should-fix
status: draft
note: the Pact page read does not describe provider verification or the broker; those steps are not asserted here
lang: core
applies_when: A service calls, or is called by, another service owned by a different team or deployed on its own schedule.
tool_gate: Contract test run in CI for both sides, and a gate that blocks deploy when a consumer's contract fails against the provider.
borrowed_from:
  - https://docs.pact.io/
  - https://spec.openapis.org/oas/v3.1.0.html
---

**Rule.** Run a contract test for each cross-service call, derived from the consumer's real requests, and fail the provider's build when it breaks one.

**Why.** A provider's own tests check what the provider thinks callers need. A spec check says what could happen, not what the consumer relies on. Only a check built from the consumer's usage catches the removed field before deploy, without a full-system end-to-end run.

**FAIL**

```text
billing calls GET /customers/{id} and reads "vat_id"
customers team removes "vat_id"; its tests pass; billing breaks in production
```

**PASS**

```text
billing CI publishes a contract: GET /customers/{id} -> body has "vat_id"
customers CI verifies every published contract and fails on the removal
```

**Counterpoint.** "End-to-end tests cover it." They are slow, need every service running, and run late. Contract tests run per service in minutes. Pact is one way; a consumer-written example set replayed against the provider also passes. For services deployed together from one repo, mark the card N/A.

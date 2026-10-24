---
id: sys-pii-minimise-retention
level: system
tags: [security, privacy, data]
severity: should-fix
status: draft
lang: core
applies_when: The system stores, copies or logs personal or otherwise sensitive data.
tool_gate: Retention jobs with a TTL on tables and buckets; a data inventory checked in CI.
note: the legal retention periods differ by jurisdiction; the source gives only the engineering principle
borrowed_from:
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/
  - https://gdpr-info.eu/art-5-gdpr/
---

**Rule.** Store sensitive data only as long and as fully as the feature needs, and give every store a delete or expiry rule.

**Why.** Data you do not keep cannot leak. Full card numbers, national IDs and raw request bodies pile up in logs, analytics tables and backups, and nobody owns their deletion. Tokenise or truncate when the full value is not needed, and encrypt what you keep. This is a technical check, not a legal opinion.

**FAIL**

```text
analytics.events: full email, DOB and phone, no TTL
logs: raw request body with the national ID field, kept forever
```

**PASS**

```text
analytics.events: hashed user id, TTL 90 days
logs: id field masked; table has a retention policy and an owner
```

**Counterpoint.** "We might need it later." A guess is not a purpose. Keep it when a named feature or legal duty needs it, and write that reason next to the retention rule.

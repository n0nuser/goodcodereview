---
id: mod-derive-dont-duplicate
level: module
tags: [compatibility, maintainability, duplication, schemas]
severity: should-fix
status: stable
lang: core
applies_when: A schema, spec, enum or list owns a shape that other code restates by hand.
tool_gate: Codegen from the schema, or a test that diffs the two lists.
note: Uber, Stripe and Spotify back the Rule without cursor/plugins
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-type-system-discipline/SKILL.md
  - https://github.com/cursor/plugins/blob/main/pstack/skills/architect/references/design-red-flags.md
  - https://www.uber.com/blog/designing-mcp-gateway/
  - https://www.uber.com/blog/high-performance-grpc/
  - https://stripe.dev/blog/how-api-changes-flow-into-stripes-developer-products
  - https://stripe.dev/blog/shepherd-how-stripe-adapted-chronon-to-scale-ml-feature-development
  - https://engineering.atspotify.com/2026/5/spotify-ads-api-claude-plugins
---

**Rule.** Derive a type, list or enum from the schema or list that owns it, or add a build check that fails when the two disagree.

**Why.** A hand-kept copy drifts. The next field added to the schema is missing from the copy, and nothing fails until a user hits it.

**FAIL**

```text
openapi.yaml defines Status: [open, closed, void]
status.py:   class Status(Enum): OPEN, CLOSED     # void missing
```

**PASS**

```text
status.py is generated from openapi.yaml in the build, or a test asserts the two sets are equal
```

**Counterpoint.** "Generated code is awkward to read." A parity test gives the same safety with hand-written types. The rule fails only when neither derivation nor a check exists.

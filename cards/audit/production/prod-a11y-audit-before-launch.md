---
id: prod-a11y-audit-before-launch
level: production
tags: [accessibility, usability, frontend, release]
severity: should-fix
status: draft
lang: core
applies_when: A new UI service or a major redesign is about to open to the public.
tool_gate: none; a launch checklist item that links the audit report.
note: 3 orgs (GOV.UK, W3C, Section508.gov weak); the GOV.UK duty is a UK legal duty, so this card names WCAG 2.2 AA as the standard and claims no law elsewhere
borrowed_from:
  - https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
  - https://www.w3.org/WAI/test-evaluate/preliminary/
  - https://alphagov.github.io/accessibility-tool-audit/
  - https://www.section508.gov/test/
---

**Rule.** Before a public launch, run an accessibility audit against WCAG 2.2 AA that includes assistive technology, and link the report in the launch checklist.

**Why.** Quick checks and automated tools are a first pass, not an evaluation. A page can pass both and still block a screen-reader user from finishing the task. Finding that after launch means fixing it under load and in public.

**FAIL**

```text
Launch checklist
[x] Load test      [x] Rollback plan      [x] Monitoring
(no accessibility line)
```

**PASS**

```text
Launch checklist
[x] Accessibility audit vs WCAG 2.2 AA, with screen reader, magnifier, and voice input.
    Report: docs/audit-2026-10.pdf. Open issues: 2, both minor, owner and date set.
```

**Counterpoint.** "We have no budget for an external audit." GOV.UK accepts a department auditor. Cut scope instead of the audit: audit the main task flows first, and say in the report which parts are not covered.

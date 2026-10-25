---
id: prod-a11y-audit-before-launch
level: production
tags: [accessibility, usability, frontend, release]
severity: should-fix
status: draft
lacks: orgs, "before a public launch" has GOV.UK only; the audit content has GOV.UK, W3C and Deque
lang: core
applies_when: A new UI service or a major redesign is about to open to the public.
tool_gate: none; a launch checklist item that links the audit report.
note: draft after stable pass 5 - 3 orgs for an audit with assistive technology (GOV.UK, W3C, Deque), but only GOV.UK ties it to before a public launch, which is the card's point; Section508.gov weak; the GOV.UK duty is a UK legal duty, so this card names WCAG 2.2 AA as the standard and claims no law elsewhere
borrowed_from:
  - https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
  - https://www.w3.org/WAI/test-evaluate/preliminary/
  - https://alphagov.github.io/accessibility-tool-audit/
  - https://www.section508.gov/test/
  - https://www.w3.org/WAI/test-evaluate/
  - https://www.deque.com/web-accessibility-beginners-guide/
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

**Counterpoint.** "We have no budget for an external audit." The auditor can be in-house, if they are trained and did not build the service. Cut scope instead of the audit: audit the main task flows first, and say in the report which parts are not covered.

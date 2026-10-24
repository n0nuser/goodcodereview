---
id: chg-ui-change-screenshots-and-keyboard-pass
level: change
tags: [accessibility, usability, frontend, process]
severity: should-fix
status: draft
lang: core
applies_when: The change alters markup, styles, or behaviour a user sees or operates.
tool_gate: A pull request template with a UI checklist; the screenshots and the keyboard result are the evidence.
note: draft after stable pass 5 - running a keyboard pass is backed by W3C, WebAIM, GOV.UK, but reporting it in the change only by the WordPress and Elastic PR templates (2); 200% zoom is W3C only; screenshots rest on three PR templates (WordPress, Elastic, Mozilla), and WordPress's section is optional
borrowed_from:
  - https://www.w3.org/WAI/test-evaluate/preliminary/
  - https://webaim.org/techniques/keyboard/
  - https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction
  - https://raw.githubusercontent.com/WordPress/gutenberg/trunk/.github/PULL_REQUEST_TEMPLATE.md
  - https://raw.githubusercontent.com/elastic/eui/main/.github/pull_request_template.md
  - https://raw.githubusercontent.com/mozilla/addons-frontend/master/.github/PULL_REQUEST_TEMPLATE.md
---

**Rule.** A UI change shows before-and-after screenshots and says what a keyboard-only pass and a 200% zoom check found on the changed screens.

**Why.** A reviewer reading a diff cannot see focus, order, or overflow. A screenshot shows the visual change, and the keyboard pass shows what the diff hides: a lost focus ring, a trap, a control that cannot be reached.

**FAIL**

```text
PR: "Redesign the settings dialog"
Files: Settings.tsx, settings.css
(no screenshots, no mention of keyboard or zoom)
```

**PASS**

```text
PR: "Redesign the settings dialog"
Before / after: screenshots attached (default and 200% zoom).
Keyboard: Tab reaches every control in order, Esc closes, focus returns to the gear button.
Not covered: screen reader, not tested.
```

**Counterpoint.** "Automated checks run in CI." They find a minority of problems. They cannot tell that Tab order is wrong or that focus vanished. Say what you did not test, as the last line shows.

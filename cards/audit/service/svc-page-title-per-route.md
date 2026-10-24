---
id: svc-page-title-per-route
level: service
tags: [accessibility, usability, frontend, routing]
severity: should-fix
status: draft
lang: core
applies_when: An app serves several pages or client-side routes under one HTML shell.
tool_gate: none; a test that navigates each route and asserts `document.title` changes.
note: 2 orgs for the core rule (W3C, A11y Project); the "Error:" prefix is GOV.UK and USWDS guidance and is shown as the PASS example
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html
  - https://www.a11yproject.com/checklist/
  - https://design-system.service.gov.uk/components/error-summary/
  - https://designsystem.digital.gov/components/form/
---

**Rule.** Give every page and every client-side route its own `<title>` that describes it, and update the title when the route changes.

**Why.** The title labels the browser tab, the history, search results, and bookmarks, and it helps users find where they are. If every route says "My App", a user cannot tell the pages apart. A single-page app that never updates the title leaves it describing the first view only.

**FAIL**

```html
<title>My App</title>
<!-- the same title on /billing, /settings, and /billing/error -->
```

**PASS**

```js
useEffect(() => {
  document.title = hasErrors ? "Error: Billing details - My App" : "Billing details - My App";
}, [hasErrors]);
```

**Counterpoint.** "The router library sets it." Then test that it does for each route. A router that changes the URL and the view but not the title is the common failure.

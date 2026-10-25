---
id: svc-page-title-per-route
level: service
tags: [accessibility, usability, frontend, routing]
severity: should-fix
status: draft
lacks: held, kept draft by Pablo's call; W3C, Mozilla and A11y Project back the Rule
lang: core
applies_when: An app serves several pages or client-side routes under one HTML shell.
tool_gate: axe `document-title` catches a missing or empty title only; a test that navigates each route and asserts its `document.title`.
note: 3 orgs for the Rule (W3C 2.4.2, including the single-page-app view; Mozilla, unique and descriptive; A11y Project, a unique title for each page or view); Deque backs only that a non-empty title exists; the "Error:" prefix is GOV.UK and USWDS guidance and is shown in the PASS example
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html
  - https://www.a11yproject.com/checklist/
  - https://design-system.service.gov.uk/components/error-summary/
  - https://designsystem.digital.gov/components/form/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/title
  - https://dequeuniversity.com/rules/axe/html/4.10/document-title
---

**Rule.** Give every page and every client-side view its own `<title>` that says what it is.

**Why.** The title labels the browser tab, the history, search results, and bookmarks, and it helps users find where they are. If every route says "My App", a user cannot tell the pages apart. In a single-page app the shell's title stays put unless the code changes it, so it goes on describing the first view.

**FAIL**

```html
<title>My App</title>
<!-- the same title on /billing, /settings, and /billing/error -->
```

**PASS**

```jsx
function usePageTitle(title) {
  useEffect(() => { document.title = `${title} - My App`; }, [title]);
}

function Settings() { usePageTitle("Settings"); /* ... */ }
function Billing({ hasErrors }) {
  usePageTitle(hasErrors ? "Error: Billing details" : "Billing details");
  /* ... */
}
```

**Counterpoint.** "The router library sets it." Then test that it does for each route. A router that changes the URL and the view but not the title is the common failure.

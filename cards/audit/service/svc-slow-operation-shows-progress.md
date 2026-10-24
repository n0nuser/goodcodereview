---
id: svc-slow-operation-shows-progress
level: service
tags: [usability, accessibility, frontend]
severity: should-fix
status: draft
lang: core
applies_when: A page action, such as a save, an upload, a search, or a page load, can take more than about a second.
tool_gate: none; throttle the network and run the action.
note: 4 orgs; Norman's feedback principle is topic only
borrowed_from:
  - https://www.nngroup.com/articles/response-times-3-important-limits/
  - https://www.nngroup.com/articles/skeleton-screens/
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/progress-indicators.json
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/feedback.json
  - https://www.cs.umd.edu/users/ben/goldenrules.html
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
---

**Rule.** Show that work is under way within about a second, and show progress with a way to cancel past about ten.

**Why.** With no feedback, users click again, reload, or leave, and a double click can run the action twice. A bar tells them whether to wait. A message that says what is happening is better than "Loading".

**FAIL**

```jsx
<button onClick={upload}>Upload</button>   // 40 s, nothing changes
```

**PASS**

```jsx
<button onClick={upload} disabled={busy} aria-busy={busy}>Upload</button>
{busy && <progress value={sent} max={total} aria-label="Uploading report.pdf" />}
{busy && <button onClick={cancel}>Cancel</button>}
<div role="status" aria-live="polite">{busy ? `Uploading, ${pct}%` : ""}</div>
```

**Counterpoint.** "A spinner on a 200 ms call flickers." Right: below about a second, show nothing, or the placeholder just flashes. Skeleton screens suit page loads, and progress bars suit uploads and other long jobs.

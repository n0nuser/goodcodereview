---
id: svc-slow-operation-shows-progress
level: service
tags: [usability, accessibility, frontend]
severity: should-fix
status: stable
lang: core
applies_when: A page action, such as a save, an upload, a search, or a page load, can take more than about a second.
tool_gate: none; throttle the network and run the action.
note: Showing that a slow action is under way is backed by NN/g, Apple, Microsoft and Atlassian. Showing progress when it runs long is backed by NN/g, Apple and Microsoft, and Microsoft gives the determinate and indeterminate split the PASS example uses. The 1 s and 10 s limits and the Cancel button come from NN/g, and Cancel also from Apple, so they are in Why. Norman's feedback principle is topic only, and Shneiderman's golden rules are a person's list, not an organisation
borrowed_from:
  - https://www.nngroup.com/articles/response-times-3-important-limits/
  - https://www.nngroup.com/articles/skeleton-screens/
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/progress-indicators.json
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/feedback.json
  - https://www.cs.umd.edu/users/ben/goldenrules.html
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
  - https://learn.microsoft.com/en-us/windows/apps/design/controls/progress-controls
  - https://atlassian.design/components/spinner/usage
---

**Rule.** Show that a slow action is under way, and show its progress when it runs long.

**Why.** With no feedback, users click again, reload, or leave, and a double click can run the action twice. A bar tells them whether to wait. A message that says what is happening is better than "Loading". As a guide, show feedback after about one second. Past about ten seconds, show how much is done and offer Cancel where stopping is safe.

**FAIL**

```jsx
<button onClick={upload}>Upload</button>   // 40 s, nothing changes
```

**PASS**

```jsx
<button onClick={busy ? undefined : upload} aria-disabled={busy}>Upload</button>
{busy && <progress value={sent} max={total} aria-label="Uploading report.pdf" />}
{busy && <button onClick={cancel}>Cancel</button>}
<div role="status">{message}</div>   // "Uploading report.pdf", then "Upload complete"
// aria-disabled keeps keyboard focus on the button; disabled would drop it
```

**Counterpoint.** "A spinner on a 200 ms call flickers." Right: below about a second, show nothing, or the placeholder just flashes. Skeleton screens suit page loads, and progress bars suit uploads and other long jobs.

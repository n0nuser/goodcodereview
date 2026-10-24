---
id: fn-status-announced-live-region
level: function
tags: [accessibility, usability, frontend, aria]
severity: should-fix
status: draft
lang: core
applies_when: Script shows a message after an async action without moving focus, such as "Saved", a result count, or an error.
tool_gate: none; a screen-reader pass, or a test that the region exists with a role before the text changes.
note: 3 orgs; USWDS reports that VoiceOver on macOS does not support `role="alert"`, so test the target reader
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
  - https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions
  - https://inclusive-components.design/notifications/
  - https://www.w3.org/WAI/tutorials/forms/notifications/
---

**Rule.** Announce an async status message through a live region (`role="status"` or `role="alert"`) that is already in the markup before its text changes.

**Why.** A sighted user sees "Saved" appear. A screen-reader user hears nothing, because focus did not move. Most readers announce a change only in a region that existed first, so a region created together with its message is often skipped.

**FAIL**

```js
const note = document.createElement("div");
note.textContent = "Changes saved";
document.body.append(note);
```

**PASS**

```html
<div id="status" role="status" aria-live="polite"></div>
<script>
  document.getElementById("status").textContent = "Changes saved";
</script>
```

**Counterpoint.** "Move focus to the message instead." Use that for a blocking error after submit, where the user must act. For a passive result, moving focus steals the user's place. Keep `assertive` and `role="alert"` for errors, because they interrupt speech.

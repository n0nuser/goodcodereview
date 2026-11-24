---
id: fn-error-message-actionable
level: function
tags: [usability, observability]
severity: discuss
status: stable
lang: core
applies_when: A diff writes a message for a person or an API caller that reports a failure, outside form validation.
tool_gate: none
note: GCC, Google (AIP-193), Atlassian and Apple state it; GitLab Pajamas says the same for forms. `fn-error-says-what-and-how` covers form validation
borrowed_from:
  - https://gcc.gnu.org/onlinedocs/gccint/Guidelines-for-Diagnostics.html
  - https://google.aip.dev/193
  - https://atlassian.design/foundations/content/designing-messages/error-messages
  - https://developer.apple.com/design/human-interface-guidelines/writing.md
---

**Rule.** Say in an error message what went wrong and what the reader can do about it.

**Why.** A message that stops at "failed" leaves the reader to guess the cause and the fix, and sends them to a search engine or a support ticket.

**FAIL**

```text
Error: request failed (code 4021)
```

**PASS**

```text
The export was cut off because the file is over 100 MB. Choose a shorter date range and try again.
```

**Counterpoint.** "Some causes are unknown." Then say what is known and where to look, such as a log id. Keep the cause and fix in the message and put internals in a details field.

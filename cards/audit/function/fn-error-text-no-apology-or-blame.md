---
id: fn-error-text-no-apology-or-blame
level: function
tags: [usability, content]
severity: discuss
status: stable
lang: core
applies_when: A diff writes or edits a message shown to a person when something fails.
tool_gate: A regex or Vale rule for "please", "sorry", "oops" and "you forgot" in message strings.
note: GOV.UK, Atlassian, Apple and Microsoft state it. Microsoft and Google allow narrow exceptions: a serious product fault, or asking permission
borrowed_from:
  - https://design-system.service.gov.uk/components/error-message/
  - https://atlassian.design/foundations/content/designing-messages/error-messages
  - https://developer.apple.com/design/human-interface-guidelines/writing.md
  - https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/sorry
  - https://developers.google.com/style/word-list
---

**Rule.** Do not blame the user, and do not pad error text with "please", "sorry" or "oops".

**Why.** The padding does not help the reader fix anything, and blame makes them stop reading. Say what happened and what to do, in neutral words.

**FAIL**

```text
Oops! You forgot to enter your email. Please try again, sorry for the trouble.
```

**PASS**

```text
Enter your email address.
```

**Counterpoint.** "A sorry shows empathy." For a serious fault that is ours, say so once and plainly. For input the user got wrong, the shortest fix reads as the kindest.

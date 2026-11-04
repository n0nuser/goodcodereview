---
id: fn-comments-survive-context
level: function
tags: [maintainability, docs]
severity: should-fix
status: stable
lang: core
applies_when: A comment or TODO says "currently", "for now", "not yet", "see the PR" or promises future work.
tool_gate: none
note: Google C++, Python and Java guides say a future-dated TODO needs a specific date or event. They also want a bug link in the TODO, so the card allows ticket ids; the Ousterhout summary stays as a reference
borrowed_from:
  - https://google.github.io/styleguide/cppguide.html
  - https://google.github.io/styleguide/pyguide.html
  - https://google.github.io/styleguide/javaguide.html
  - https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2
  - https://docs.webkit.org/Deep%20Dive/Web%20Inspector/Compatibility.html
  - https://github.com/PostHog/posthog/blob/master/.agents/skills/writing-code-comments/SKILL.md
---

**Rule.** Write comments that remain true without outside context: no "currently", "for now" or "see the PR", and give a TODO the date or event that ends it.

**Why.** The PR vanishes from memory and the "currently" never gets updated. A comment whose context has expired is a lie by the next release. A TODO with a removal condition tells the next reader when to act. A bug link in the TODO is welcome, as long as the comment says what to do and when.

**FAIL**

```text
# TODO: handle the legacy case for now
retry = False  # see the PR, currently disabled
```

**PASS**

```text
# TODO(JIRA-4412): drop this branch once every client sends v2 payloads
```

**Counterpoint.** "Ticket links help traceability." They do, and the PASS keeps one. The ticket alone is not enough, since trackers get migrated and closed. Name the condition in the comment too.

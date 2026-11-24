---
id: code-docs-no-minimising-words
level: codebase
tags: [docs, usability]
severity: discuss
status: stable
lang: core
applies_when: A diff adds documentation text that describes a task or a step.
tool_gate: A Vale rule (GitLab `SubstitutionWarning`, Google `WordList`) or a regex for "simply", "just", "easily" and "obviously".
note: Django, GitLab, Google, Docker and Elastic state it
borrowed_from:
  - https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/
  - https://docs.gitlab.com/development/documentation/styleguide/word_list/
  - https://developers.google.com/style/word-list
  - https://raw.githubusercontent.com/docker/docs/main/STYLE.md
  - https://www.elastic.co/docs/contribute-docs/style-guide/
---

**Rule.** Do not call a step "simple", "easy", "just" or "simply" in docs.

**Why.** What is easy for the author is not easy for a newcomer. A reader who fails at an "easy" step blames themselves, and the word adds nothing to the instruction.

**FAIL**

```text
Simply run the migration, then just restart the worker.
```

**PASS**

```text
Run the migration, then restart the worker.
```

**Counterpoint.** "'Just' softens the tone." Cut the word and keep the instruction. If a step really is optional, say so.

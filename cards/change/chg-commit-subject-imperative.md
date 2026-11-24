---
id: chg-commit-subject-imperative
level: change
tags: [process, maintainability]
severity: discuss
status: stable
lang: core
applies_when: A change carries a commit message or squash-merge title.
tool_gate: commitlint `subject-max-length` and `subject-case`, or a `commit-msg` hook.
note: Imperative mood is stated by the Linux kernel, Kubernetes, Spring, Node.js, GNOME and Google. Length (50 to 72) by Kubernetes, Spring, Node.js, GNOME, GitLab and Rails. Django asks for past tense, and Spring bans `fix:` type prefixes
borrowed_from:
  - https://docs.kernel.org/process/submitting-patches.html
  - https://www.kubernetes.dev/docs/guide/pull-requests/
  - https://raw.githubusercontent.com/spring-projects/spring-framework/main/CONTRIBUTING.md
  - https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md
  - https://handbook.gnome.org/development/commit-messages.html
  - https://google.github.io/eng-practices/review/developer/cl-descriptions.html
---

**Rule.** Write the commit subject as a short command in the imperative, about 50 characters and at most 72, with no trailing period.

**Why.** The subject is what `git log --oneline`, blame views and release tooling show. An imperative line reads as what applying the change does, and a short one is not cut off.

**FAIL**

```text
Fixed the bug where the importer sometimes crashed when a row was empty.
```

**PASS**

```text
Skip empty rows in the importer
```

**Counterpoint.** "Our project uses past tense, or conventional-commit types." The rule is consistency and a short line. Follow the project's convention where one is written down, and check it in a hook.

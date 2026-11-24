---
id: chg-commit-body-says-why
level: change
tags: [process, maintainability]
severity: discuss
status: stable
lang: core
applies_when: A change is not trivial enough for its subject line to say everything.
tool_gate: none
note: Django, Spring, the Linux kernel, Rails and GNOME state it. Node.js and Google say to include what changed as well, so the Rule asks for the why and leaves the what optional
borrowed_from:
  - https://docs.djangoproject.com/en/dev/internals/contributing/committing-code/
  - https://raw.githubusercontent.com/spring-projects/spring-framework/main/CONTRIBUTING.md
  - https://docs.kernel.org/process/submitting-patches.html
  - https://guides.rubyonrails.org/contributing_to_ruby_on_rails.html
  - https://handbook.gnome.org/development/commit-messages.html
---

**Rule.** Use the commit body to say why the change was made, not to repeat what the diff shows.

**Why.** The diff already shows what changed. The reason lives only in the author's head, and `git blame` is where the next maintainer looks for it.

**FAIL**

```text
Change timeout from 5 to 30

Changed the timeout constant to 30 seconds.
```

**PASS**

```text
Raise the export timeout to 30 seconds

Large accounts take up to 20 seconds to export, and the 5 second limit
cut them off halfway and left partial files.
```

**Counterpoint.** "The PR description has the reason." Squash merges and mirrors drop it. Keep a line in the commit, and link the PR for the rest.

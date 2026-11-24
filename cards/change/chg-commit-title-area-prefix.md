---
id: chg-commit-title-area-prefix
level: change
tags: [process, maintainability]
severity: discuss
status: stable
lang: core
applies_when: The project has several subsystems or packages and writes commit or PR titles as `area: summary`.
tool_gate: commitlint `scope-empty` or a PR-title check in CI.
note: The Linux kernel, Node.js and Prometheus state it. Spring bans type prefixes such as `fix:`, and several projects use none, so the Rule applies where the project uses area prefixes
borrowed_from:
  - https://docs.kernel.org/process/submitting-patches.html
  - https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md
  - https://raw.githubusercontent.com/prometheus/prometheus/main/CONTRIBUTING.md
---

**Rule.** Start the commit or PR title with the area it changes, such as `net: summary` or `importer: summary`, where the project uses area prefixes.

**Why.** A one-line log shows which part of the system each change touched, so a reader can scan for their area and a bisect lands on the right owner.

**FAIL**

```text
Skip empty rows
```

**PASS**

```text
importer: skip empty rows
```

**Counterpoint.** "Prefixes eat the 50 characters." They replace words the subject would spend on context anyway. A small repo with one area gains nothing, so the rule applies only where a prefix convention exists.

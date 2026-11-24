---
id: chg-doc-marks-version-added
level: change
tags: [compatibility, docs]
severity: discuss
status: stable
lang: core
applies_when: A diff adds a public feature, option or API that is documented, or changes how a documented one behaves.
tool_gate: Sphinx `versionadded` and `versionchanged` directives with a docs check, or a front-matter lint for a version field.
note: Django, Python, Node.js and Elastic state it. Docker only describes keeping such notes
borrowed_from:
  - https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/
  - https://devguide.python.org/documentation/markup/
  - https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md
  - https://www.elastic.co/docs/contribute-docs/how-to/cumulative-docs/
---

**Rule.** When a diff adds or changes a documented feature, mark in the docs the version that added or changed it.

**Why.** Readers run many versions. Without a version marker they cannot tell if the option exists in theirs, and the docs cannot be trimmed later without guessing.

**FAIL**

```text
The `--dry-run` flag prints what would change.     (flag added in this diff, no version)
```

**PASS**

```text
The `--dry-run` flag prints what would change.
.. versionadded:: 3.2
```

**Counterpoint.** "Release notes already say it." Release notes are read once at upgrade time. The marker stays on the page where the reader looks it up.

---
id: chg-docs-updated-with-code
level: change
tags: [maintainability, docs, process]
severity: should-fix
status: stable
note: Google, Zephyr, Python, Django and Apache Airflow state it for docs; Node.js only for API changes. Chromium is Google. Google's review guide also says to consider deleting docs when code is deleted
lang: core
applies_when: The diff changes behaviour, an argument, a return value or an error that a comment, docstring, README or doc page describes.
tool_gate: none
borrowed_from:
  - https://google.github.io/styleguide/docguide/best_practices
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md
  - https://docs.zephyrproject.org/latest/contribute/contributor_expectations.html
  - https://devguide.python.org/getting-started/pull-request-lifecycle/
  - https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/
  - https://github.com/apache/airflow/blob/main/contributing-docs/05_pull_requests.rst
  - https://github.com/nodejs/node/blob/main/doc/contributing/pull-requests.md
---

**Rule.** Change the comments, docstrings and docs that describe the code in the same diff as the code, or delete them.

**Why.** A doc fixed "later" is a doc that stays wrong. The reviewer sees the old text and the new behaviour side by side only in this diff, so this is the cheapest place to catch the mismatch.

**FAIL**

```text
- def fetch(url, retries=3):   # retries up to 3 times
+ def fetch(url, retries=0):   # retries up to 3 times
```

**PASS**

```text
- def fetch(url, retries=3):   # retries up to 3 times
+ def fetch(url, retries=0):   # no retries unless the caller asks
```

**Counterpoint.** "Doc fixes bloat the diff and slow the change." Fixing the text is a line or two, and a separate doc PR is rarely sent. If the text cannot be fixed now, delete it.

---
id: fn-todo-has-owner-or-issue
level: function
tags: [maintainability, process]
severity: discuss
status: stable
lang: core
applies_when: A diff adds a TODO, FIXME or similar marker.
tool_gate: ESLint `no-warning-comments` with a pattern, Ruff `TD002`/`TD003`, or a regex check in CI.
note: GitLab and CockroachDB require an issue link; Envoy and OpenStack require an owner name. A TODO with a date or event is `fn-comments-survive-context`
borrowed_from:
  - https://docs.gitlab.com/development/code_review/
  - https://raw.githubusercontent.com/cockroachdb/cockroach/master/docs/style.md
  - https://raw.githubusercontent.com/envoyproxy/envoy/main/STYLE.md
  - https://docs.openstack.org/hacking/latest/user/hacking.html
---

**Rule.** Give each TODO an owner or a tracking issue, such as `TODO(alice)` or `TODO(#1234)`.

**Why.** An anonymous TODO has nobody to ask and nothing to close, so it stays for years. An owner or a ticket tells the next reader who knows the context and where the work is tracked.

**FAIL**

```text
# TODO: handle the empty case
```

**PASS**

```text
# TODO(#1234): handle the empty case once the importer sends batches
```

**Counterpoint.** "People leave and tickets get closed." Then the marker still points somewhere to ask. Pair it with `fn-comments-survive-context` so the comment also says when it ends.

---
id: chg-changelog-entry
level: change
tags: [maintainability, process]
severity: discuss
status: draft
lacks: orgs, a changelog entry per feature change has USGS and Rails; needs a third org
lang: core
applies_when: The project keeps a changelog, and the change adds, removes or changes a feature.
tool_gate: none
borrowed_from:
  - https://astrogeology.usgs.gov/docs/how-to-guides/software-management/guidelines-for-pull-requests/
  - https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html
---

**Rule.** Add a changelog entry to each change that adds, removes or changes a feature.

**Why.** Users and release managers read the changelog, not the diff. A feature change with no entry reaches the release notes late or never, and a removal with no entry surprises whoever depended on it.

**FAIL**

```text
Diff: removes the --legacy flag from the CLI and renames --out to --output.
CHANGELOG.md is untouched.
```

**PASS**

```text
Diff: same change, plus in CHANGELOG.md under "Unreleased":
  - Removed: the --legacy flag.
  - Changed: --out is now --output.
```

**Counterpoint.** "Every fix needs an entry too, or the log is incomplete." Bug fixes, refactors and test changes carry no user-visible feature change, and entries for them bury the ones that matter. Add an entry for a fix only when users must act on it.

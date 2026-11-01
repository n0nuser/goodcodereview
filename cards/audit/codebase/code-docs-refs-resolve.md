---
id: code-docs-refs-resolve
level: codebase
tags: [maintainability, docs, ci]
severity: should-fix
status: stable
lang: core
applies_when: Auditing a repo whose README, guides or AGENTS.md cite file paths, anchors or other pages.
tool_gate: A link checker in CI, such as lychee (`lychee --offline --include-fragments docs README.md`) or mdBook linkcheck.
note: GitHub docs, GitLab docs and the Rust dev guide each run a link check on every change. Whether the documented commands run is a different rule
borrowed_from:
  - https://github.com/github/docs/blob/main/src/links/README.md
  - https://docs.gitlab.com/development/documentation/testing/links/
  - https://github.com/rust-lang/rustc-dev-guide/blob/master/.github/workflows/ci.yml
---

**Rule.** Run a link check in CI over the docs, so that every relative link and anchor they cite resolves.

**Why.** A rename or a deleted file leaves docs that point at nothing. Readers and agents then follow a dead path, and nobody notices until someone trips on it. A machine finds a dangling reference on the pull request that causes it.

**FAIL**

```text
README.md:  See [the deploy guide](docs/deploy.md).      <- docs/deploy.md was renamed to docs/ops/deploy.md
AGENTS.md:  See [Setup](docs/dev.md#setup).             <- the heading was renamed
CI:         no link check, no job reads the docs
```

**PASS**

```yaml
docs-links:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@<40-char-sha>
    - run: lychee --offline --include-fragments README.md AGENTS.md docs
```

**Counterpoint.** "External links flake, so the job will be red half the time." Check local paths and anchors on every change, where the result is stable. Run the external links on a schedule, so a dead site never blocks a merge.

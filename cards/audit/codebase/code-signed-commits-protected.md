---
id: code-signed-commits-protected
level: codebase
tags: [security, process, supply-chain, git]
severity: should-fix
status: draft
lacks: orgs, "require signed commits" has OWASP and Node.js; GitHub documents the setting and AWS calls signing optional; needs one more org
lang: core
applies_when: Auditing the branch protection of a repository that ships code or holds release branches.
tool_gate: Branch protection or ruleset "Require signed commits" on every protected branch.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/CI_CD_Security_Cheat_Sheet.html
  - https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-rulesets/available-rules-for-rulesets
  - https://github.com/nodejs/node/blob/main/doc/contributing/releases.md
---

**Rule.** Require signed commits on protected branches, so unsigned commits cannot merge or be pushed.

**Why.** An author name and email in a commit are plain text that anyone can set. Without a verified signature, a stolen token or a forged identity can put code in the release branch under a maintainer's name, and the history gives no way to tell.

**FAIL**

```text
Branch protection for main:
  Require a pull request before merging: on
  Require signed commits: off
```

**PASS**

```text
Branch protection for main:
  Require a pull request before merging: on
  Require signed commits: on
```

**Counterpoint.** "Signing adds setup for every contributor, and squash merges made in the web UI are signed by the host, not the author." Both are true. The host's signature still proves the commit came through the reviewed merge path, and an unsigned push straight to the branch is the case the rule blocks. Scope the rule to protected branches, not to every branch.

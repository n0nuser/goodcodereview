---
id: chg-no-per-user-ide-files
level: change
tags: [process, maintainability, git]
severity: should-fix
status: draft
lacks: unreviewed, sources and examples are in place; no stable pass has checked rules 1 to 10
lang: core
applies_when: A change adds a tracked file under an editor or IDE project directory.
tool_gate: A CI step that fails when `git ls-files | rg '(^|/)(\.idea/workspace\.xml|\.idea/shelf/|xcuserdata/)|\.xcuserstate$'` prints a path. `git ls-files -ci --exclude-standard` lists only tracked files that already match an ignore entry, so it misses a repository with no entry.
note: GitHub and Git describe the repository ignore file and the machine-wide excludes; JetBrains and Microsoft separate shared project settings from per-user state; Apple requires shared Xcode schemes for CI
borrowed_from:
  - https://docs.github.com/en/get-started/git-basics/ignoring-files
  - https://git-scm.com/docs/gitignore
  - https://github.com/github/gitignore/blob/main/Global/VisualStudioCode.gitignore
  - https://intellij-support.jetbrains.com/hc/en-us/articles/206544839
  - https://www.jetbrains.com/help/idea/configure-project-settings.html
  - https://code.visualstudio.com/docs/configure/settings
  - https://learn.microsoft.com/en-us/azure/devops/repos/git/ignore-files
  - https://developer.apple.com/documentation/xcode/setting-up-your-project-to-use-xcode-cloud
---

**Rule.** Do not commit a file that holds one developer's editor or IDE state; ignore those paths in the repository or a machine-wide exclude file, and keep the settings the team shares in the repository.

**Why.** Per-user state changes on every IDE session and every machine, so it adds diff noise and merge conflicts. The shared files are the ones a teammate or CI needs. JetBrains says `.idea` holds both user-specific settings that "should not be placed under version control" and project settings "normally shared among developers". Microsoft says workspace settings in `.vscode` are "shared by all users of that project". Git and GitHub offer the repository `.gitignore` for paths everyone hits and a machine-wide exclude for a path only one developer has.

**FAIL**

```text
git diff --cached --name-only
.idea/workspace.xml
xcuserdata/alice.xcuserdatad/xcschemes/App.xcscheme
.gitignore            # no entry for either path
```

**PASS**

```text
# .gitignore
.idea/workspace.xml
.idea/shelf/
xcuserdata/
*.xcuserstate

# committed
.idea/codeStyles/Project.xml
.vscode/settings.json
App.xcodeproj/xcshareddata/xcschemes/App.xcscheme
```

**Counterpoint.** "A blanket ignore throws away the run configurations and schemes the team shares." Those live in shared locations: `.idea/runConfigurations/`, `.vscode/launch.json`, `xcshareddata/xcschemes/`. Commit those and ignore `workspace.xml` and `xcuserdata`. In a one-developer repository, put the path in the machine-wide exclude instead of the shared ignore file.

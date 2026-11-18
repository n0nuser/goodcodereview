# Promotion pass C

- chg-no-per-user-ide-files: TRIMMED+PROMOTED, severity should-fix.
  - Clause "do not commit per-user IDE state": jetbrains, git, github.
  - Clause "ignore in repo or machine-wide exclude": git, github, microsoft.
  - Clause "git rm --cached": git, github, microsoft.
  - Clause "keep shared settings in the repository": verified only jetbrains and microsoft (Apple page and the GitHub VS Code gitignore are not in the cache). Moved to the Why.
  - Rule edit: dropped ", and keep the settings the team shares in the repository". Rest unchanged.
  - Weak point: git and github back the first clause through editor-generated files, not IDE state by name.
- mod-temporary-field: PROMOTED, severity discuss (sources are lint warnings). Rule unchanged. Orgs: jetbrains, sonarsource, pmd (refactoring-guru does not count). tool_gate rules FieldCanBeLocal, S1450, SingularField exist.
- code-ai-pr-disclosure: PROMOTED, severity should-fix. Rule unchanged. Disclosure: kernel, ghostty, godot. Human can explain and defend: kernel, ghostty, godot. tool_gate is a PR template and trailer check, not a linter rule.

`python3 tools/validate.py` exits 0.

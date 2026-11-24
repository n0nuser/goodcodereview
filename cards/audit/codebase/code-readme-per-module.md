---
id: code-readme-per-module
level: codebase
tags: [maintainability, docs]
severity: discuss
status: stable
lang: core
applies_when: Auditing a repo with several packages, modules or self-contained components.
tool_gate: A CI check that every package root holds a README (a glob test, or a docs linter).
note: Google (with Chromium), Microsoft (Azure SDK) and HashiCorp (Terraform) state it. None says every subdirectory, so the Rule stops at the package, module or component root
borrowed_from:
  - https://google.github.io/styleguide/docguide/READMEs.html
  - https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_guidelines.md
  - https://azure.github.io/azure-sdk/general_documentation.html
  - https://developer.hashicorp.com/terraform/language/modules/develop/structure
  - https://raw.githubusercontent.com/github/docs/main/content/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes.md
---

**Rule.** Give each package, module or self-contained component a README at its root that says what it holds and how to use it.

**Why.** A reader landing in a directory from search or a stack trace has no other place to learn what the code is for. The README is the one file everyone opens first.

**FAIL**

```text
services/billing/    (12 files, no README)
```

**PASS**

```text
services/billing/README.md   What billing owns, how to run its tests, who to ask.
```

**Counterpoint.** "A README per folder is clutter." The rule stops at the unit that has its own purpose. Leave plain subfolders without one.

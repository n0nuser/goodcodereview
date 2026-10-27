---
id: mod-yagni
level: module
tags: [maintainability, process, design, scope]
severity: should-fix
status: stable
lang: core
applies_when: The change adds an abstraction, parameter, hook or option.
tool_gate: none
note: The MediaWiki architecture page labels itself a draft. The Microsoft playbook checklist may echo Google's wording and the extensibility guideline is indirect. Shopify backs the second-use clause.
borrowed_from:
  - https://kentcdodds.com/blog/aha-programming
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  - https://www.mediawiki.org/wiki/Architecture_guidelines
  - https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/designing-for-extensibility
  - https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/
  - https://shopify.engineering/other-driven-developments
  - https://martinfowler.com/bliki/Yagni.html
  - https://henrikwarne.com/2024/01/10/tidy-first/
  - https://github.com/NVIDIA/Model-Optimizer/blob/main/CONTRIBUTING.md
---

**Rule.** Do not build an abstraction or capability for a need that does not exist yet; add it when the need or a second use appears.

**Why.** Speculative flexibility costs reading time every day and is usually the wrong shape when the need arrives. Reviewers cannot verify a use that does not exist.

**FAIL**

```text
class NotifierFactory: ...   # one product, one caller
def send(msg, retries=3, backoff=None, hook=None): ...   # nobody passes these
```

**PASS**

```text
def send_welcome_email(user): ...
```

**Counterpoint.** "But we will surely need it." Then add it when you do, in a change that has the real second caller to shape it. Optimising for easy change means simple code, not built-in flexibility. The cost of waiting is low, and the cost of the wrong guess is not. When the need is certain and a retrofit would be costly, as for a public API that cannot change later, weigh that cost before waiting.

# Dead code and YAGNI: sources for two promotions

Two cards go back to stable after a second organisation pass: `code-dead-code` and `mod-yagni`. Each quote below came back from a fetch of the page named. People never count toward the three organisations. Vendors count and are flagged.

## code-dead-code

The Rule is narrowed to two clauses that each reach three organisations. Commented-out code and orphaned files moved to the Why.

Unreferenced functions and variables: Google, Meta, Carnegie Mellon SEI, with the Linux kernel and NVIDIA as extra sources.

- Google, https://abseil.io/resources/swe-book/html/ch09.html: "Getting rid of dead or obsolete code is one of the best ways to improve the overall code health of a codebase."
- Google, https://abseil.io/resources/swe-book/html/ch15.html: "if a system is obsolete, it has a net cost on the organization and should be removed." The same chapter says "Even code that has been removed can be found again."
- Meta, https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/: SCARF "operates at a symbol level as opposed to a file level", aims at "minimizing developer costs", and has deleted "more than 100 million lines of code".
- Carnegie Mellon SEI, https://cmu-sei.github.io/secure-coding-standards/sei-cert-c-coding-standard/recommendations/miscellaneous-msc/msc12-c: CERT MSC12-C says dead or unreachable code "should be identified, understood, and eliminated."
- Linux kernel, https://docs.kernel.org/process/coding-style.html: "if a function or variable always goes unused, delete it."
- NVIDIA, https://github.com/NVIDIA/Model-Optimizer/blob/main/CONTRIBUTING.md: "Remove dead code". A contributing guide, so a weaker source.

Expired feature-flag branches: Microsoft, GitLab, Uber, with Statsig as a vendor extra.

- Microsoft, https://learn.microsoft.com/en-us/devops/operate/progressive-experimentation-feature-flags: "Most feature flags can be retired once a feature has been rolled out to everyone. At that point, the team can delete all references to the flag in code and configuration."
- GitLab, https://docs.gitlab.com/ee/development/feature_flags/: "Feature flags should remain in the codebase for as short a period as possible" and "After all mentions of the feature flag have been removed, legacy code can be removed."
- Uber, https://www.uber.com/blog/piranha/: "all code artifacts related to the flag need to be removed from the source code"; leftovers "might still be made executable in unexpected cases".
- Statsig (vendor), https://statsig.com/blog/feature-flag-code-cleanup: the cleanup ticket says "Remove all if/else conditions using ff_new_checkout"; stale flags make code "harder to read, reason about, and refactor".

Why-only sources, with fewer than three organisations:

- Commented-out code. Lockheed Martin's JSF C++ standard, https://www.stroustrup.com/JSF-AV-rules.pdf (Doc. 2RDU00001 Rev C): "AV Rule 127: Code that is not used (commented out) shall be deleted." JetBrains (vendor), https://www.jetbrains.com/help/inspectopedia/CommentedOutCode.html: "it is better to delete commented out code completely and use the VCS history instead." MISRA Dir 4.4 is only quoted second-hand, and SonarSource's rule page was not reached, so neither is cited.
- Orphaned files. Nothing verified. Google's Sensenmann post reportedly deletes libraries not linked into any binary, but the fetch returned only a title.
- Palantir, https://blog.palantir.com/code-review-best-practices-19e02780015f: returned 403, so its stance is unverified.

## mod-yagni

The Rule is narrowed to one claim: do not build for a need that does not exist yet, and add it when the need or a second use appears. "Non-trivial" and "clutters the main flow" had no source and are dropped.

- Google, https://google.github.io/eng-practices/review/reviewer/looking-for.html: over-engineering is "making the code more generic than it needs to be". "Encourage developers to solve the problem they know needs to be solved now, not the problem that the developer speculates might need to be solved in the future."
- Wikimedia (MediaWiki), https://www.mediawiki.org/wiki/Architecture_guidelines: under "You aren't gonna need it", "Do not introduce abstraction in advance of need." The page calls itself a draft and a work in progress, and does not state its publisher.
- Microsoft, https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/designing-for-extensibility: "choose the least costly extensibility mechanism that meets the requirements." and "it's usually possible to add more extensibility later, but you can never take it away". Indirect.
- Microsoft, https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/: "Does the code add functionality that isn't needed?" The wording may echo Google's.
- Shopify, https://shopify.engineering/other-driven-developments (John DeWyze, 2021): "don't go looking for an abstraction until you have three instances of similar code." Backs the second-use clause. The rule of three comes from Fowler.

People cited, not counted: Martin Fowler, https://martinfowler.com/bliki/Yagni.html ("any abstraction that makes it harder to understand the code for current requirements is presumed guilty."). Sandi Metz's line on the wrong abstraction was only seen quoted in a vendor page, so it is not cited.

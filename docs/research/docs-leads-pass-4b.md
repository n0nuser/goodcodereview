# Docs and comments leads: pass 4b (practices J, H, P, S1, S2)

Fetched 2026-11-22. Each page was downloaded raw with `curl -sL`, tags stripped with `python3 -I`, and the sentence found with `rg` in the stripped text. No WebFetch summary is evidence. Paraphrases are mine; no quote runs over 10 words. Google (pyguide, Java guide, Go, Chromium) counts as one org; Microsoft Learn and Azure SDK count as one.

Card check: `rg` over `cards/` found no card for J, H or P. `fn-comments-stay-short` (draft) covers S1 and S2. `fn-comments-explain-why` is the nearest card for H (it says not to restate what the next line does, not about doc comments on signatures).

## J. Doc parameter lists match the signature (no card)

1. https://project.pages.drupalcode.org/coding_standards/php/documentation/. Drupal. Every function parameter gets a `@param` tag, and its type equals the type in the signature. Found: "Each parameter of a function must be documented" and "identical to the parameter type".
2. https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags. Microsoft. The documented parameter names must match the API signature, and the compiler warns on a missing or wrong one. Found: "names for parameters must match the API signature".
3. https://peps.python.org/pep-0257/. Python (PSF). Docstrings must carry the correct argument names, since names can be used as keywords; a function docstring documents its arguments. Found: "docstring should document the correct argument names" and "document its arguments, return value(s)".

Count: 3 orgs (Drupal, Microsoft, Python). Python is the new third; it is a docstring convention, not a compiler or lint check, so it is the weakest. Extra, coverage only: Google pyguide (https://google.github.io/styleguide/pyguide.html) says to list each parameter by name under Args; it also lets the section drop when the signature suffices. Not counted: Kotlin (https://kotlinlang.org/docs/coding-conventions.html) says to avoid `@param`; Home Assistant says to leave types out. Existing card: none.

## H. No doc comment that only restates the name or signature (no card)

1. https://flink.apache.org/how-to-contribute/code-style-and-quality-common/. Apache Flink. Javadoc must not carry meaningless text added to please checkstyle. Found: "JavaDocs should not state meaningless information".
2. https://google.github.io/styleguide/pyguide.html. Google. A docstring that only repeats the class or method name should be left out. Found: "A docstring that only repeats class or method name".
3. https://www.kernel.org/doc/html/latest/process/coding-style.html. Linux kernel. Do not add boilerplate kernel-doc that reiterates what the function signature already shows. Found: "Do not add boilerplate kernel-doc which simply reiterates".
4. https://peps.python.org/pep-0257/. Python (PSF). A one-line docstring must not be a signature that reiterates the parameters, since introspection gives those. Found: "should NOT be a “signature” reiterating the function/method parameters".

Count: 4 orgs (Flink, Google, Linux kernel, Python). Linux kernel is the strongest new one (same wording as the practice). NumPy (https://numpydoc.readthedocs.io/en/latest/format.html, from 3b) is a weak fifth and is not counted here. Existing card: none (nearest `fn-comments-explain-why`).

## P. Names built at runtime get a comment listing the possible values (no card)

1. https://www.mediawiki.org/wiki/Manual:Coding_conventions. Wikimedia. Avoid building message keys, CSS class names or file names dynamically; if you must, leave a nearby comment with the possible or most common values. Found: section "Dynamic identifiers", "you must leave a comment nearby".

Count: 1 org (Wikimedia). Searched the 40-odd raw pages from this pass for grep, git-grep and searchable wording. Adjacent, not the practice: Linux kernel coding style says never to split user-visible strings, so they stay greppable; Ansible docs (variable-name indirection kept grep-able, not a comment); Airbnb (long strings stay searchable); Google C++ guide (long literals keep searchability). None says to list the possible runtime values in a comment. Does not clear the bar. Existing card: none.

## S1. Keep a code comment to a few lines (draft card fn-comments-stay-short)

1. https://docs.gitlab.com/development/code_comments/. GitLab. A comment is limited to three lines of prose, and a RuboCop cop enforces it. Found: "Limit a comment to three lines of prose".
2. https://developers.home-assistant.io/docs/development_guidelines/. Home Assistant. Comments are short and explain why, never what. Found: "Keep them short, and use them to explain".

Count: 2 orgs (GitLab, Home Assistant). No third found. Checked and not a length rule: Google Go decisions ("no fixed line length for comments"), Google pyguide/Java/C++, PEP 8, Linux kernel (warns against over-commenting and avoiding comments inside functions, no length limit; the closest, but a style warning, not a "keep short" rule), Kotlin, Swift, Chromium, Django, Rust compiler guide, Spark, Flink, Kafka, Elastic (says comments need not all be Javadoc), Angular, Envoy, Uber, Beam. CockroachDB points readers to its large code comments as a feature, so it argues the other way. Existing card: fn-comments-stay-short.

## S2. Long explanation goes to docs, an ADR, or the commit/PR with a link (draft card fn-comments-stay-short)

1. https://docs.gitlab.com/development/code_comments/. GitLab. Longer rationale goes to the MR description or issue, found via git blame. Found: "Put longer rationale in the merge request description".
2. https://www.mediawiki.org/wiki/Manual:Coding_conventions/Documentation. Wikimedia. Detailed architecture and design notes belong in a `/docs` directory or component README kept in Git beside the code. Found: "well-suited for detailed documentation about a project's code architecture". This says where detail lives; it does not say to move it out of a code comment.
3. https://google.github.io/styleguide/docguide/best_practices.html. Google. Documentation is a spectrum from terse comments to detailed prose; inline comments give the why, and the larger layers hold the rest. Found: "terse comments to detailed prose". This too states layering, not a move-out rule.

Count: 1 firm org (GitLab); Google and Wikimedia are layering statements, not a "move it out and link" rule. No third org found. Not found: Python devguide, Django, Rust, Linux Documentation/ (kernel coding style says use kernel-doc, no such rule), Chromium (design docs become archives, README holds detail; no code-comment rule), Spark, Flink, Kafka, Angular, Elastic. Existing card: fn-comments-stay-short.

## Unreachable or unverified

- https://azure.github.io/azure-sdk/java_documentation.html returned 404.
- https://wiki.crdb.io/... returned 202 with an empty body. https://kafka.apache.org/community/coding-guide/ returned 404 (and the Kafka coding page is not used).
- https://github.com/spring-projects/spring-framework/wiki/Code-Style returned 404; Spring unverified for all five practices.
- https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html and https://docs.oracle.com/en/java/javase/21/javadoc/doc-comment-specification.html returned small pages with no `@param` rule text; Java doc rules unverified.
- https://www.swift.org/documentation/docc/... returned 213-byte shells (JS-rendered); Swift DocC unverified. The Swift API guidelines page had no J, H or S text.
- https://raw.githubusercontent.com/JetBrains/intellij-community/master/CONTRIBUTING.md, https://raw.githubusercontent.com/hashicorp/terraform/main/.github/CONTRIBUTING.md and the Swift compiler StyleGuide path returned 404 or tiny bodies; JetBrains, HashiCorp unverified.
- Android code-style page, Mozilla C++ style, Node.js docs, Envoy STYLE.md, Uber guide and Airbnb README loaded but held no sentence for J, H, P, S1 or S2. Not searched: Rust API-guideline pages beyond `documentation.html`, Kubernetes API conventions (client-rendered).

## Summary

- J: 3 orgs (Drupal, Microsoft, Python). Clears the bar, Python weakest.
- H: 4 orgs (Flink, Google, Linux kernel, Python). Clears the bar.
- P: 1 org. Lead only.
- S1: 2 orgs. No third found.
- S2: 1 firm org plus two layering statements. No third found.

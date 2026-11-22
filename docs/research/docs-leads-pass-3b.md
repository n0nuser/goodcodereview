# Docs and comments leads: pass 3b (practices F to K)

Fetched 2026-11-22. Every page was downloaded raw with `curl -sL`, tags stripped with `python3 -I`, and the sentence found by `rg` in the stripped text. Nothing here comes from a WebFetch summary. Paraphrases are mine; no quote runs over 10 words. Google (pyguide, Java guide) counts as one org; Microsoft (Learn, Azure SDK) counts as one org.

## F. A doc comment starts with one short summary sentence (no existing card)

1. https://peps.python.org/pep-0257/. Python (PSF). A multi-line docstring opens with a summary line that fits on one line, then a blank line. Found: "Multi-line Docstrings" paragraph.
2. https://www.swift.org/documentation/api-design-guidelines/. Swift. Begin with a summary of the declared entity; use one sentence fragment ending in a period. Found: "Focus on the summary" paragraph.
3. https://rust-lang.github.io/rfcs/0505-api-comment-conventions.html. Rust. The first line of any doc comment is a single short summary sentence, third person. Found: "Formatting" section.
4. https://google.github.io/styleguide/pyguide.html and https://google.github.io/styleguide/javaguide.html. Google. Python docstrings start with a one-line summary ending in punctuation; Javadoc starts with a brief summary fragment. Found: "3.8" docstring text and "7.2 The summary fragment".
5. https://project.pages.drupalcode.org/coding_standards/php/documentation/. Drupal. Docblock summary is one line, under 80 characters, ending in a period. Found: "All summaries (the first line of a docblock)".
6. https://developer.wordpress.org/coding-standards/inline-documentation-standards/php/. WordPress. The summary is a brief one-sentence purpose statement ending in a period. Found: "Summary : A brief, one sentence explanation".
7. https://docs.openstack.org/hacking/latest/user/hacking.html. OpenStack. Multi-line docstrings start with a one-line summary under 80 characters (check H405). Found: Docstrings section.
8. https://numpydoc.readthedocs.io/en/latest/format.html. NumPy. Docstring section 1 is a one-line short summary. Found: "Short summary" heading text.

Count: 8 orgs (Python, Swift, Rust, Google, Drupal, WordPress, OpenStack, NumPy). Existing card: none.
Seen but not counted: Kotlin KDoc says by convention the first paragraph is the summary (https://kotlinlang.org/docs/kotlin-doc.html), which is a paragraph rule, not a sentence rule. Go doc comments (https://go.dev/doc/comment) require complete sentences and a name-first opening, with no summary rule. Microsoft XML docs require a `<summary>` tag but no length or sentence rule.

## G. Fallible, panicking or unsafe functions document Errors, Panics, Safety (no exact card; svc-api-documented-errors covers HTTP API errors only)

1. https://rust-lang.github.io/api-guidelines/documentation.html. Rust. Errors, panics and safety each get their own section in function docs. Found: heading "Function docs include error, panic, and safety considerations".
2. https://google.github.io/styleguide/pyguide.html. Google. The Raises section lists every exception relevant to the interface. Found: "Raises: List all exceptions that are relevant".
3. https://learn.microsoft.com/en-us/dotnet/standard/design-guidelines/exception-throwing. Microsoft (.NET). Document all exceptions thrown by publicly callable members for contract violations. Found: "DO document all exceptions thrown".

Count: 3 orgs (Rust, Google, Microsoft). Existing card: none.
Not counted: Home Assistant shows a Raises section in its example (https://developers.home-assistant.io/docs/development_guidelines/) but states no rule. numpydoc calls Raises optional, to be used judiciously. Kotlin says there is no expectation to document all exceptions. Swift lists Throws as a recognised markup keyword only. Java `@throws` (Oracle javadoc page): the fetched page held no `@throws` text, so not verified.

## H. No doc comment that only restates the name or signature (no existing card; fn-comments-explain-why is the nearest)

1. https://flink.apache.org/how-to-contribute/code-style-and-quality-common/. Apache Flink. Javadoc must not state meaningless information added to satisfy checkstyle. Found: "JavaDocs should not state meaningless information".
2. https://google.github.io/styleguide/pyguide.html. Google. A docstring that only repeats the class or method name should be omitted; a class docstring should not state that it is a class. Found: "A docstring that only repeats class or method name". The first sentence sits in the test-method paragraph.
3. https://numpydoc.readthedocs.io/en/latest/format.html. NumPy. The one-line summary must not use variable names or the function name. Found: "does not use variable names or the function name".

Count: 3 orgs (Flink, Google, NumPy). NumPy is a documentation-format rule, so it is the weakest of the three. Existing card: none.
Weak extra: Django says test docstrings should skip preambles like "Tests that" (https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/). Not counted.

## I. Every public module, class, function has a docstring, linter-enforced (no existing card)

1. https://developers.home-assistant.io/docs/development_guidelines/. Home Assistant. Every module, class and function has a docstring, and Ruff checks docstrings in pre-commit and CI. Found: "Every module, class, and function has a docstring" and "which Ruff checks too". This is the only lint-enforced statement I verified.
2. https://peps.python.org/pep-0257/. Python. Modules, exported functions and classes, and public methods should have docstrings. Found: "should normally have docstrings". No linter claim.
3. https://google.github.io/styleguide/pyguide.html. Google. A docstring is mandatory for public-API, non-trivial or non-obvious functions. Found: "A docstring is mandatory". The guide also tells readers to run pylint; the link to docstring rules is implied, not stated.
4. https://azure.github.io/azure-sdk/python_documentation.html. Microsoft (Azure SDK). Provide docstrings for all public modules, types and methods. Found: "DO provide docstrings for all public modules". No linter claim in the page.
5. https://kafka.apache.org/community/developer/. Apache Kafka. All public APIs must have Javadocs. Found: "All public APIs must have JavaDocs". The page also mentions checkstyle, but not tied to this rule.
6. https://go.dev/doc/comment. Go (Google). Every exported name should have a doc comment. Found: "Every exported (capitalized) name". Same org as Google.
7. https://project.pages.drupalcode.org/coding_standards/php/documentation/. Drupal. Every function, constant, class, member and file must be documented, even private ones. Found: "Every function, constant, class, interface".
8. https://doc.rust-lang.org/rustc/lints/listing/allowed-by-default.html. Rust. A `missing_docs` lint flags undocumented public items; it is allow-by-default because it is noisy. Found: "missing_docs lint detects missing documentation". This is a tool, not a stated practice.

Count: 6 distinct orgs state the docstring rule (Home Assistant, Python, Google incl. Go, Microsoft, Kafka, Drupal). Only Home Assistant states that a linter enforces it. Rust ships the lint but does not call it a practice. Existing card: none.

## J. Doc parameter lists match the signature (no existing card)

1. https://project.pages.drupalcode.org/coding_standards/php/documentation/. Drupal. Each parameter needs a `@param` tag, and its type must equal the signature type. Found: "Each parameter of a function must be documented" and "identical to the parameter type".
2. https://learn.microsoft.com/en-us/dotnet/csharp/language-reference/xmldoc/recommended-tags. Microsoft (.NET). Param names must match the API signature, and the compiler warns when one is missing or unknown. Found: "names for parameters must match the API signature".
3. https://google.github.io/styleguide/pyguide.html. Google. The Args section lists each parameter by name; it can be dropped when name and signature already suffice. Found: "Args: List each parameter by name". Coverage only; no "must match" wording.
4. https://developers.home-assistant.io/docs/development_guidelines/. Home Assistant. Docstring parameters leave types out because the signature has them. Found: "leave the types out". This is a no-duplicate rule, not a match rule; the parent's earlier lead is not confirmed beyond this.

Count: 2 firm (Drupal, Microsoft) plus Google as coverage-only. Existing card: none.

## K. Delete orphan example or doc files nobody references (card: code-dead-docs-deleted)

1. https://kubernetes.io/docs/contribute/style/style-guide/. Kubernetes. A standalone YAML example no topic references should be deleted, not updated. Found: "not referenced from any topics, consider deleting".

Count: 1 org (Kubernetes). I checked the GitLab docs style guide and docs landing page, and the Django writing-documentation page, for orphan, unreferenced, unused or remove-image wording and found none. Existing card: code-dead-docs-deleted (check its sources against this).

## Pages not reached or not verified

- https://www.oracle.com/technical-resources/articles/java/javadoc-tool.html returned 200 but had no `@param`, `@throws` or "restate" text, so Java `@throws` and `@param` rules are unverified.
- https://learn.microsoft.com/en-us/contribute/content/how-to-write-images returned 404.
- https://docs.gitlab.com/development/documentation/styleguide/images/ returned 404.
- https://raw.githubusercontent.com/mdn/content/main/docs/MDN_CONTRIBUTOR_DOC.md returned 404.
- The Azure SDK page has no lint claim for I; the pydocstyle error-codes page returned 200 but the D103 text did not match my search.
- Go and Microsoft were searched for F and found only weaker rules (see F).

## Parent verification and outcome (2026-11-22)

Re-fetched raw and matched the sentence for F (Python, Swift, Rust, WordPress, OpenStack), G (Rust, Google, Microsoft) and I (Home Assistant, Python, Microsoft). New stable cards: `fn-doc-summary-sentence`, `fn-doc-documents-errors`, `fn-public-api-has-docstring`. Not carded: H (no restating doc comment; Flink, Google and a weak NumPy rule, close to `fn-comments-explain-why`), J (parameters match the signature; Drupal and Microsoft only), K (orphan examples; Kubernetes only).

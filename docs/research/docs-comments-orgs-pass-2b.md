# Docs and comments practices: org sources, pass 2b

Fetched 2026-11-22 with WebFetch (a small model summarises each page, so paraphrases are second-hand; nothing was read raw). Same format as docs-comments-orgs-pass.md. Practices: (1) docs and comments change in the same change as the code; (2) delete wrong or obsolete docs, archive design docs after implementation; (3) short code comments, long explanation in docs with a link; (4) minimum viable docs, README per directory, link instead of duplicating.

## Rows

1. https://kafka.apache.org/community/developer/. Apache Kafka. Docs ship in the same PR as the code (Streams requires it), and a changer should check existing JavaDocs are still accurate. Backs 1.
2. https://kafka.apache.org/community/developer/. Apache Kafka. Do not commit commented-out code, since version control keeps history; avoid leftover TODO/FIXME. Backs 2 (code comments only, not docs).
3. https://kafka.apache.org/community/developer/. Apache Kafka. Clear names are preferred over comments; a needed comment is written for a human reader. Backs 3 weakly (no length rule, no link rule).
4. https://github.com/apache/airflow/blob/main/contributing-docs/05_pull_requests.rst. Apache Airflow. A PR that adds functionality updates the docs in that PR; a docstring is often enough. Backs 1.
5. https://spark.apache.org/contributing.html. Apache Spark. When preparing a PR, consider whether docs need adding or updating and do it in the same PR; user-visible behaviour changes also go in the migration guide. Backs 1.
6. https://contributors.home-assistant.io/core/development/style/. Home Assistant. Keep comments short and explain why; delete commented-out code; keep docs close to the code and remove them when outdated. Backs 2, 3 (short only, no link rule).
7. https://contributors.home-assistant.io/core/development/style/. Home Assistant. Point to the authoritative style guide or quality scale instead of repeating it. Backs 4.
8. https://project.pages.drupalcode.org/coding_standards/php/documentation/. Drupal. Docs describe the current code, not past differences or future plans; every function, class, constant, member and file is documented. Backs 1 (state-of-code, not same-change).
9. https://project.pages.drupalcode.org/coding_standards/php/documentation/. Drupal. Use @see and {@inheritdoc} to point at related docs instead of restating them. Backs 4.
10. https://www.drupal.org/docs/develop/standards/php/api-documentation-and-comment-standards. Drupal. Obsolete items are marked @deprecated with removal version and replacement; outdated doc pages are marked deprecated and pointed to the replacement, not deleted. Backs 2 weakly (deprecate-then-remove).
11. https://developer.wordpress.org/coding-standards/inline-documentation-standards/php/. WordPress. Document an argument array once in its originating function and cross-reference it with @see elsewhere; duplicate hook docs become a one-line pointer. Backs 4.
12. https://developer.wordpress.org/coding-standards/inline-documentation-standards/php/. WordPress. Summaries are one brief sentence and inline comments are single lines. Backs 3 weakly (length only).
13. https://developer.wordpress.org/coding-standards/inline-documentation-standards/php/. WordPress. A significant change (new argument, changed default) adds a new @since entry in the docblock. Backs 1 weakly.
14. https://www.mediawiki.org/wiki/Manual:Coding_conventions. Wikimedia (MediaWiki). Concepts, subsystems and data flows belong in the /docs folder, not scattered through code comments; language rules are linked to subpages, not repeated. Backs 3 and 4.
15. https://kubernetes.io/docs/contribute/style/content-guide/. Kubernetes. Link to the canonical source rather than hosting a copy, because duplicates cost effort and go stale. Backs 4.
16. https://kubernetes.io/docs/contribute/style/style-guide/. Kubernetes. A standalone YAML example not referenced by any topic is deleted, not updated. Backs 2 (narrow: orphan examples). Full page read this time (offsets 0-100000 and 100000-end).
17. https://azure.github.io/azure-sdk/general_documentation.html. Azure SDK. Each library has a README.md in its root directory covering install and basic usage. Backs 4 (README per package).

## Not counted (read, state none of the four)

- Rust API guidelines (https://rust-lang.github.io/api-guidelines/documentation.html): only says a link to an example may suffice when an item is used once; no rule on the four.
- Rust RFC 505 (https://rust-lang.github.io/rfcs/0505-api-comment-conventions.html), rust-lang/rfcs README: comment-format rules. The README says accepted RFCs stay in the repo and need a new RFC for substantial change; nothing on archiving after implementation.
- Flink code-style-and-quality-common and -java: comments explain why, avoid redundant comments, no meaningless JavaDoc; no length, delete, or link rule.
- Apache Spark documentation.html, Mozilla contributing/index and coding-style index: navigation only. Firefox contributing_code: docs not required with a patch.
- GitHub docs best-practices and about-contributing: audience, one-or-two tasks per article, self-review before PR; none of the four. Style guide: link only when readers need it, no repeated link in one article.
- Debian Policy ch. 12 (https://www.debian.org/doc/debian-policy/ch-docs.html): packaging rules; a program without a man page is a bug. Not a code-comment practice.
- Microsoft Learn contributor guide: how to contribute, no practice.
- Home Assistant docs writing guide (https://contributors.home-assistant.io/writing/): no same-PR or delete rule stated.
- Red Hat modular docs (https://redhat-documentation.github.io/modular-docs/): reuse via snippets and cross-references, cover only what users need. This is user-documentation structure, not code docs; counted only as a lead. Supplementary style guide: fetch read only 100k of 560k chars and the summary's claim about a "final section" on removing obsolete content was not confirmed.
- Grafana writers-toolkit pages: summariser first claimed the landing page lists "remove obsolete docs, link instead of duplicating, keep docs minimal", then two re-fetches said none of it is stated. Treated as not stated. The toolkit links to "Deprecate or remove" and "Reuse" guides that were not fetched.

## Not reached

- Microsoft Learn code review / engineering docs: https://learn.microsoft.com/en-us/contribute/content/ read, but no page on deleting or linking found; Microsoft style on code docs not located.
- Mozilla documentation_best_practices (404), Mozilla Managing Documentation (moztreedocs) not fetched.
- Rust std-dev-guide pages best-practices, policy/doc-comments (404); doc-comments page fetch returned the API guidelines answer only, rustc stabilization guide returned a redirect stub.
- Grafana contribute/style-guides/documentation-style-guide.md (404).
- Fedora docs (contributing, contributing-docs) and Ubuntu governance page: blocked by Anubis or 404. Canonical documentation site: login redirect.
- Eclipse project handbook: read 100k of 975k chars, nothing on docs found; remainder unread.
- Spark: first fetch of contributing.html failed once then succeeded. Kafka contributing page redirected to /community/developer/, which was read.
- Apache Flink: no separate docs-with-code page found; Airflow 09_testing mention only.

## Counts (orgs added by this pass)

- Practice 1 (docs change with code): Kafka, Airflow, Spark; weakly Drupal, WordPress. Combined with pass 1: Google, Chromium, Zephyr, Python, Django, Node.js, Kafka, Airflow, Spark = 9.
- Practice 2 (delete obsolete): Home Assistant (comments and docs, delete outright), Kubernetes (orphan examples only), Kafka (commented-out code only); Drupal deprecates rather than deletes. No page found on archiving design docs after implementation.
- Practice 3 (short comments, long explanation to linked docs): Wikimedia (concepts go in /docs, not comments) is the only new org; Home Assistant and WordPress state short comments with no link rule.
- Practice 4 (minimum viable, README per dir, link not duplicate): Kubernetes, Drupal, WordPress, Home Assistant, Wikimedia (link/single-source); Azure SDK (README per library). Minimum viable docs: none new.

## New-card leads (checkable practices no row covers)

- Doc comment first line is one short sentence, third-person present, ends with a period (Rust RFC 505, Drupal, WordPress).
- Fallible functions have an Errors section, panicking ones a Panics section, unsafe ones a Safety section (Rust API guidelines).
- Every public item has a runnable example; snippets are built and tested in CI (Rust API guidelines, Azure SDK).
- Deprecation carries version, removal version, and replacement pointer (Drupal, WordPress).
- Every TODO links to a tracking issue (Drupal @todo; Kafka says avoid TODO/FIXME).
- No commented-out code (Kafka, Home Assistant).
- No meaningless doc comment that only restates the name (Flink).
- Every module, class and function has a docstring, enforced by linter in CI (Home Assistant).
- Comments avoid time-relative words ("currently", "new") and version-hedging comments inside examples (Kubernetes style guide).
- Dynamic identifiers (message keys, CSS classes built at runtime) get a nearby comment listing every possible value (MediaWiki).
- User-visible behaviour change adds a migration-guide entry and a release-note field (Spark).
- Each library root has a TROUBLESHOOTING.md (Azure SDK).
- Document params and return match the signature, types omitted from prose when the signature has them (Drupal, Home Assistant).
- Orphan example files are deleted (Kubernetes).

## Parent verification (2026-11-22, raw page text)

Confirmed against the raw pages: Airflow (docs in the same PR), Kubernetes content guide (a duplicate grows stale), Home Assistant (short comments, why not what, no commented-out code), Kafka (no commented-out code), MediaWiki (concepts and data flows go in /docs). Not confirmed in raw text, so not used as sources: Kafka docs-in-same-PR, Spark docs-in-same-PR, Shopify comment-update rule. Home Assistant's "delete outdated docs" claim is not on its style page.

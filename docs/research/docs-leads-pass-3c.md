# Docs leads, pass 3c

Fetched 2026-11-22 with `curl -sL`, tags stripped with `python3 -I`, sentence located with `rg` in the raw text. Paraphrases only. "Found" gives the section or phrase matched in the stripped text.

## L. User-visible change adds a changelog, NEWS or release-note entry

Existing card: `chg-changelog-entry` (draft, lacks a third org; cites USGS and Rails). Everything below is new to it.

1. https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/ . Django. The PR checklist asks for a release note when a change is backwards incompatible, and for new features and backported fixes. Found: "is there a note in the release notes ... docs/releases/A.B.txt" and "New Features ... Is there a release note".
2. https://devguide.python.org/getting-started/pull-request-lifecycle/ . Python. Most changes get a NEWS entry; the exceptions are docs, tests, internal-only changes and reverts. User-interesting changes also go in "What's New". Found: "Changes that require NEWS entries" section.
3. https://docs.gitlab.com/development/changelog/ . GitLab. Any user-facing change, API change or database migration needs a changelog entry. Found: "Any user-facing change must have a changelog entry."
4. https://github.com/kubernetes/community/blob/master/contributors/guide/release-notes.md . Kubernetes. A user-visible or operator-visible change qualifies for a release note. Found: "Any user-visible or operator-visible change qualifies".
5. https://spark.apache.org/contributing.html . Apache Spark. A behaviour change that may need user action goes in the migration guide, and reviewers may ask for it. Found: "highlighted in the migration guide".

Not counted: Node.js (pull-requests.md) only asks for a breakdown of semver-major changes in the commit message, no changelog file entry. Rust relnotes is a triagebot label process run by the team, not an author duty (forge.rust-lang.org/release/release-notes.html).

Count: 5 orgs verified (Django, Python, GitLab, Kubernetes, Spark). Existing card: chg-changelog-entry. New: the card cites only USGS and Rails; these five clear the 3-org bar, and Django/Python/Spark add the migration-guide and "What's New" variants for breaking changes.

## M. Each package or directory has a README (what it holds, who owns it)

Existing card: none found by `rg` (code-docs-link-dont-duplicate touches linking only).

1. https://google.github.io/styleguide/docguide/READMEs.html . Google. A README is a short summary of the directory's contents. Found: "A README is a short summary of the contents of a directory."
2. https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_best_practices.md . Chromium (Google, same org). README.md should say what the directory is meant to hold. Found: "What is this directory intended to hold?"
3. https://azure.github.io/azure-sdk/general_documentation.html . Azure SDK (Microsoft). README.md sits in each library's root with install and usage. Found: "README.md - Resides in the root of your library's directory".
4. https://docs.unity.com/en-us/engine/6000.0/manual/packages-list/cus-pkg-development/cus-layout . Unity. Recommended package layout has README.md at the package root, but it is developer documentation, not a "what this holds" summary. Weak.
5. https://www.kubernetes.dev/docs/guide/owners/ . Kubernetes. OWNERS files designate who is responsible for each part of the code. This covers the "who owns it" half only, in a separate file, not a README.

Count: 2 orgs verified for "README per directory/package" (Google incl. Chromium, Microsoft Azure SDK). Unity is partial. "Owner named in the README" is not stated by any page found. Not reached: Rust, Node.js, Go (go.dev/doc/contribute only says the repo-root README has testing info; Go package comments are a different practice). Does not clear the bar.

## N. Each library has a TROUBLESHOOTING or FAQ doc

Existing card: none.

1. https://azure.github.io/azure-sdk/general_documentation.html . Azure SDK (Microsoft). Each library root holds a TROUBLESHOOTING.md used by customers and support. Found: "TROUBLESHOOTING.md - Resides in the root of your library's directory".
2. https://docs.gitlab.com/development/documentation/topic_types/troubleshooting/ . GitLab. Troubleshooting topics belong at the end of a feature page, and rare cases are included too. This is per page, not per library. Weak.

Count: 1 org verified (Azure). A web search for SDK guides requiring an FAQ file found none. Does not clear the bar.

## O. Docs and comments avoid time-relative words

Existing card: `fn-comments-survive-context` (stable; cites Google C++/Python/Java guides on dated TODOs, WebKit, PostHog). It covers comments and TODOs. New: a docs-level rule on the words "currently", "new", "now" in prose, from orgs not in the card.

1. https://developers.google.com/style/timeless-documentation . Google. Avoid "currently", "new", "latest" for product features. Found: "avoid phrases like "currently," "new," or "latest"".
2. https://kubernetes.io/docs/contribute/style/style-guide/ . Kubernetes. Avoid words like "currently" and "new", since new today is old in months. Found under "Avoid statements that will soon be out of date".
3. https://docs.gitlab.com/development/documentation/styleguide/word_list/ . GitLab. Do not use "currently" for product features, and "new" is usually avoidable. Found: "Do not use currently when talking about the product".
4. https://www.mariadb.com/docs/general-resources/about/readme/documentation-style-guide . MariaDB. Its style guide lists "Timeless documentation" and says to avoid currently, existing, in the future, now, soon. Found: "avoid words and terms like currently".

Related, not counted: Django writing-documentation says to avoid naming a Django version outside versionadded blocks because it goes stale (about versions, not these words). Splunk present-tense page flags "will now process" (tense, not time words). Red Hat supplementary guide says avoid predicting future releases (different). Microsoft Learn word-list pages for "currently"/"new" returned 404; Apple HIG and Unity style guide pages not reachable (empty or 403). So Microsoft and Apple are unverified.

Count: 4 orgs verified (Google, Kubernetes, GitLab, MariaDB). Existing card: fn-comments-survive-context. New: three non-Google orgs state the docs-prose rule. Caveat: all four are docs style guides, not code-comment rules; the card's applies_when is comments/TODOs, so either widen it to docs prose or add a docs card.

## P. Dynamic identifiers get a comment listing every possible value

Existing card: none.

1. https://www.mediawiki.org/wiki/Manual:Coding_conventions . Wikimedia/MediaWiki. Prefer writing identifiers out; if concatenating, leave a nearby comment with the possible or most common values. Found under "Dynamic identifiers": "you must leave a comment nearby with the possible (or most common) values". Note MediaWiki says "possible (or most common)", not "every".

Count: 1 org verified (Wikimedia). BiggerPockets "Write Greppable Code" (Search result) now returns GitHub Pages 404; unverified. Greppability blog posts are individuals, not orgs. Does not clear the bar.

## Q1. Delete wrong or obsolete docs

Existing card: `code-dead-docs-deleted`.

1. https://google.github.io/styleguide/docguide/best_practices.html . Google. Cut out-of-date, incorrect or redundant information; section "Delete Dead Documentation". Found in raw text.
2. https://docs.gitlab.com/development/documentation/workflow/ . GitLab. Delete unfinished docs instead of hiding them in HTML comments, because hidden docs go stale. Found: "Delete instead of hiding documentation".
3. https://www.kernel.org/doc/html/latest/doc-guide/contributing.html . Linux kernel. Remove obsolete documentation; if it cannot be updated, add an outdated warning. Found: "There is surprising resistance to removing obsolete documentation, but we should do that anyway."

Count: 3 orgs verified (Google, GitLab, Linux kernel). Linux kernel is the new third org. Checked, nothing found: Kubernetes reviewing-prs/style guide, MDN writing style guide, Python devguide documentation, Django writing-documentation, Rust contributing/about-this-guide (no obsolete-docs rule seen). Microsoft Learn contribute page and MDN Remove_or_deprecate did not load. Note GitLab row 2 is about unreleased hidden docs; a strict reader may say it fits less than the kernel page. Existing card: code-dead-docs-deleted.

## Q2. Long explanation goes to docs/ADR with a link, not a code comment

Existing card: `code-docs-link-dont-duplicate` and `code-adr` are near; no card for this exact rule found.

1. https://docs.gitlab.com/development/code_comments/ . GitLab. Limit a comment to three lines; longer rationale goes in the MR description or issue, found through git blame. Found: "Put longer rationale in the merge request description or the issue". Destination is the MR or issue, not docs/ADR, so this is adjacent.

Count: 0 verified new orgs for the docs/ADR-with-link form (GitLab is adjacent). Google and Wikimedia stay from earlier passes. Not found: Python devguide, Django, Rust, Linux Documentation/ (kernel coding-style says to see Documentation/ files for API but states no such comment rule). GitHub, Red Hat, AWS, 18F ADR posts: no code-comment sentence found (18F page returned empty, Red Hat and AWS had no match, GitHub blog had no match).

## Unreached or unverified pages

- learn.microsoft.com style-guide word pages (404), contribute/content (no match).
- developer.apple.com HIG writing (stub, JS).
- docs-style-guide.unity.com (403).
- docs.redhat.com (access denied); Red Hat supplementary guide was reachable but had no relevant rule.
- developer.mozilla.org Remove_or_deprecate, drupal.org API standards, pantsbuild style guide, neovim dev_style (tiny or empty responses).
- 18f.gsa.gov ADR post, wiki.simpler.grants.gov, biggerpockets.github.io (empty or 404).
- github.com/kubernetes/community api-conventions.md (client-rendered, no usable text).

## Parent verification and outcome (2026-11-22)

Re-fetched raw and matched the sentence for: GitLab (three-line limit), Home Assistant (short, why not what), Python NEWS, Kubernetes release notes, Spark migration guide, Django release notes, GitLab changelog, Google/Kubernetes/GitLab/MariaDB time-relative words, Linux kernel (remove obsolete docs). Applied: `chg-changelog-entry` promoted to stable; the four time-relative sources added to `fn-comments-survive-context`; kernel added to `code-dead-docs-deleted` (still draft: GitLab's page is about unfinished docs); GitLab added to `fn-comments-stay-short` (still draft, each clause has two organisations). README per directory (Google, Azure SDK), troubleshooting doc per library (Azure SDK) and runtime-built identifiers (MediaWiki) stay leads.

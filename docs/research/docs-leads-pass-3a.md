# Docs leads, pass 3a

Method: each page was fetched with `curl -sL`, tags stripped with `python3 -I`, and the sentence found with `rg` in the stripped text. Raw copies were kept in the session scratchpad only. "Known" orgs from earlier passes (Drupal, WordPress, Cloudflare, Spotify, Google, Azure SDK) were not re-fetched here and are listed as known, not verified in this pass. Quotes are kept under 10 words.

## A. Every TODO/FIXME links to an issue or names an owner/date

Existing card: `fn-comments-survive-context` (TODO needs a date or event; its note cites Google guides). No card on "TODO links an issue/owner". Related: `chg-no-silenced-diagnostics` cites Palantir.

1. https://docs.gitlab.com/development/code_review/ . GitLab. A TODO is added only if a reviewer requires it, and then it must link the issue. Raw: code review page, sentence "If you add a TODO, include a link to the relevant issue".
2. https://raw.githubusercontent.com/cockroachdb/cockroach/master/docs/style.md . CockroachDB. Incomplete code paths get a tracking issue and a `// TODO(#NNNNN)` comment at the call site. Raw: "Incomplete implementations" section, "Track each gap with a GitHub issue".
3. https://raw.githubusercontent.com/envoyproxy/envoy/main/STYLE.md . Envoy. TODO comments carry the author's GitHub name, `TODO(foobar)`. Raw: style bullet list, "Use your GitHub name in TODO comments".
4. https://docs.openstack.org/hacking/latest/user/hacking.html . OpenStack. Rule H101: include your name with TODOs so the author is findable. Raw: rule H101, "Include your name with TODOs".
5. https://github.com/kubernetes/community coding-conventions: fetched, no TODO rule found. Does not count.
6. Known, not re-verified: Google (C++/Python/Java guides, date or event; Android code style page fetched and also says "include a specific date" for future-dated TODOs, but is Google), Drupal `@todo`.

Count: 4 distinct non-Google orgs verified (GitLab, CockroachDB, Envoy, OpenStack), plus known Google and Drupal. Mixed forms: issue link (GitLab, CockroachDB), owner name (Envoy, OpenStack). A card worded "a TODO names an owner or a tracking issue" has 4 verified. Caveat: Envoy is a project, OpenStack a foundation; both are orgs by the repo's rule. Not found in LLVM, Linux kernel, Rust compiler guide (it bans landing a TODO outright), Mozilla, Uber, Go CodeReviewComments, Kafka (known: avoids TODO).

## B. A deprecation carries the removal version and a replacement pointer

Existing cards: `chg-expand-contract`, `svc-api-deprecation-sunset` (service-level Sunset header), `chg-breaking-change-taxonomy`. Nothing on code-level deprecation markers.

1. https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/submitting-patches/ . Django. The deprecation warning class names the removal version; the docs get a `deprecated` directive with the upgrade path; release notes and a deprecation timeline are updated. Raw: "Deprecating a feature" section, "RemovedInDjangoXXXXWarning (where XXXX is the Django version where the feature will be removed)" and "note about the upgrade path".
2. https://docs.oracle.com/en/java/javase/21/docs/specs/javadoc/doc-comment-spec.html . Oracle (Java). The first sentence of the deprecation text should say when it was deprecated and what replaces it, with a link. Raw: `@deprecated` tag section, "should tell the user when the API was deprecated".
3. https://angular.dev/reference/releases . Angular (Google, so shares org with Google if Google is counted elsewhere). Deprecations ship with a recommended update path and an `@deprecated` annotation; removal waits for a later major. Raw: "Deprecation policy" table, "we also announce a recommended update path". Also https://raw.githubusercontent.com/angular/angular/main/contributing-docs/commit-message-guidelines.md : the DEPRECATED footer must mention the recommended update path.
4. https://peps.python.org/pep-0387/ . Python. A warning message should include the release and an issue link; soft deprecations should propose a replacement; removal is scheduled. Raw: "The warning message should include the release". Caveat: that sentence sits in the default-change part; "propose a replacement" is about soft deprecation only. Treat as partial. It is an adopted policy PEP, not a plan.
5. https://doc.rust-lang.org/reference/attributes/diagnostics.html . Rust. `#[deprecated]` takes `since` and `note`; rustdoc shows them. Raw: "including the since version and note". This is a language reference, so it describes the mechanism, not a rule that every deprecation must carry both. Weak. RFC 1270 (rust-lang.github.io/rfcs/1270-deprecation.html) likewise is a proposal, does not count.
6. https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md . Node.js. Adding or deprecating an API means updating the YAML doc entry with the version (`REPLACEME`). Raw: "If you are adding to or deprecating an API". collaborator-guide.md adds: communicate pending deprecations and mitigations early. Version yes, replacement only implied. Partial.
7. https://kubernetes.io/docs/reference/using-api/deprecation-policy/ . Kubernetes. Fetched; states minimum lifetimes (e.g. 9 months or 3 releases) before removal. I did not find a sentence requiring a replacement pointer in each deprecation notice. Not counted.
8. Known, not re-verified: Drupal `@deprecated` with removal version and replacement, WordPress.

Count: strong on both halves: Django, Oracle Java (2 verified), plus known Drupal and WordPress = 4. Partial: Angular, Python, Node.js, Rust. A card could claim three on strong evidence (Django, Oracle, Drupal) without relying on the partials.

## C. A deleted or moved doc page gets a redirect in the same change

Existing cards: `code-dead-docs-deleted` (draft, deleting wrong docs; not this). No card on redirects.

1. https://docs.gitlab.com/development/documentation/redirects/ . GitLab. Moving, renaming or deleting a page requires a redirect; a technical writer is assigned to such merge requests. Raw: first paragraph, "you must add a redirect".
2. https://docs.github.com/en/contributing/writing-for-github-docs/configuring-redirects . GitHub. When a title or location changes, a redirect from the old URL is created. Raw: "About redirects" section, "we create a redirect". Does not say "same PR".
3. https://raw.githubusercontent.com/mdn/content/main/CONTRIBUTING.md . MDN (Mozilla). The `content move` command fixes redirects automatically; `content delete --redirect` adds one; forgotten redirects can be added afterwards. Raw: "Moving documents", "fixes up redirects automatically"; "Deleting a document". Partial: tooling, and allows later fix.
4. Known, not re-verified: Cloudflare (redirect in same PR, bot reminder).

Count: 3 verified (GitLab, GitHub, MDN partial) plus known Cloudflare = 4; GitLab is the only one with an explicit "you must". Not found: Kubernetes (style guide, content-organization, pr-wranglers: no redirect rule). Microsoft Learn: contribute redirect pages returned 404 at every URL I tried; not verified.

## D. Doc code examples are embedded from source or tested, not pasted

Existing cards: none exact. `code-docs-link-dont-duplicate` is related (link, do not duplicate prose).

1. https://doc.rust-lang.org/rustdoc/write-documentation/documentation-tests.html . Rust. Doc examples run as tests so they stay current. Raw: intro, "makes sure that examples within your documentation are up to date". Also https://rust-lang.github.io/api-guidelines/documentation.html: every public item has an example (C-EXAMPLE), compiled by `cargo test`.
2. https://go.dev/blog/examples . Go (Google). Example functions are compiled and run as part of the test suite. Raw: "Examples are compiled (and optionally executed)". Counts as Google.
3. https://kubernetes.io/docs/contribute/style/hugo-shortcodes/ . Kubernetes. The `code_sample` shortcode embeds a file from `examples/` into the page. Raw: "Source code files", "embed the contents of file". Mechanism description inside a contributor guide; embed is stated as the way to include samples, with a "generic sample" condition. Partial.
4. https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide . MDN (Mozilla). Authors must run and test every example before submitting. Raw: "Run and test every code example". Manual test, not CI. Partial.
5. https://devguide.python.org/documentation/markup/ . Python. Larger examples live in external files pulled in by `literalinclude`. Raw: "may be included by storing the example text in an external file". Permissive wording, partial. The doctest module page (docs.python.org) describes a tool; it does not state a rule. Not counted.
6. https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md . Node.js. Code samples in API docs are checked by `make lint`. Raw: "Code samples included in the API docs will also be checked". Lint, not run; partial.
7. Known, not re-verified: Spotify TechDocs, Azure SDK (the Azure general_documentation page fetched here says snippets live in README and docstrings but I found no CI/embed sentence; left as known only).

Count: tested or embedded, clear: Rust, Go (Google), Kubernetes (embed) = 3 orgs, plus known Spotify. MDN and Node.js are partial. Distinct orgs for a "tested in CI or embedded" card: Rust, Google (Go), Kubernetes, Spotify = 4; Kubernetes is the weakest.

## E. Docs have a declared owner and a last-updated/review date

Existing cards: `code-dead-docs-deleted` (its `lacks` line asks for a third org; its tool_gate mentions a last-reviewed date or owner per page). `chg-sensitive-paths-human-owner` is about code paths.

1. https://learn.microsoft.com/en-us/contribute/content/metadata . Microsoft. Every article carries `ms.author`, which identifies the owner, and `ms.date`, shown on the page as last substantially edited or guaranteed fresh. Raw: field table, "Identifies the article's owner" and "Displayed on the published page". Both halves.
2. https://docs.gitlab.com/development/documentation/metadata/ . GitLab. Each page declares its stage and group in front matter, and a CODEOWNERS file maps docs files to technical writers who must approve. Raw: "Stage and group metadata", and "Batch updates for TW metadata", "The CODEOWNERS file contains a list of files". Owner only; no date found (searched for last updated, reviewed, freshness).
3. https://raw.githubusercontent.com/kubernetes/website/main/OWNERS . Kubernetes. The docs repo has an OWNERS file naming approvers and reviewers; pages show a last-modified date in the theme. The contributor guides describe OWNERS_ALIASES roles (kubernetes.io/docs/contribute/participate/roles-and-responsibilities/). This is configuration evidence, not a sentence stating a docs-ownership practice. Not counted.
4. Known, not re-verified: Spotify (owner and last-updated date, CODEOWNERS in TechDocs announcement).

Count: 2 verified (Microsoft both halves, GitLab owner only) plus known Spotify = 3 for "docs have a declared owner"; only Microsoft and Spotify cover the date half. Kubernetes does not count.

## Pages not reached or not verified

- Microsoft Learn redirect guidance: `/contribute/content/redirection`, `/redirects`, `/redirects-how-to`, `/redirection-guidance` all 404; MicrosoftDocs/contributor-guide GitHub API 404.
- MDN `Writing_guidelines/Howto/Move_a_page` and `Page_structures/Redirect`: 404.
- Node.js `doc/contributing/deprecations.md`: 404 (the deprecations doc at nodejs.org/api/deprecations.html was reachable but describes deprecation kinds, not a per-deprecation rule).
- Rust std-dev-guide deprecation page: 404.
- Swift StyleGuide.md, Godot code style, Vue docs contributing, Docker docs file-conventions and CONTRIBUTING redirect pages, Spring: 404 or no hit.
- Kubernetes redirect rule: not found in style-guide, content-organization, pr-wranglers or open-a-pr.
- Not checked for the known ones: Drupal, WordPress, Cloudflare, Spotify, Azure SDK, Google.

## Parent verification and outcome (2026-11-22)

Re-fetched raw and matched the sentence for A (GitLab, CockroachDB, Envoy, OpenStack), B (Django, Oracle, WordPress) and D (Rust, Go, Kubernetes). New stable cards: `fn-todo-has-owner-or-issue`, `fn-deprecation-names-version-and-replacement`. Drafts: `code-doc-examples-stay-true` (each clause has two organisations), `code-docs-redirect-on-move` (GitLab, Cloudflare, GitHub; exact sentences not read by a stable pass). Owner and last-updated date (E): Microsoft and GitLab, owner half only for GitLab; stays a lead.

# Docs leads, pass 5b

Method: every page was fetched with `curl -sL` into a fresh `mktemp -d` directory, tags stripped with `python3 -I`, whitespace collapsed, and the sentence found with `rg` in the stripped text. No summaries are used as evidence. Quotes are under 10 words; the rest is paraphrase. Fetch date: 2026-11-22. Org grouping follows docs/PROMOTION.md and `tools/orgs.py` (Google covers Go and eng-practices; Microsoft covers Learn; Red Hat covers Ansible and its docs; a person's blog does not count).

Sources read for every practice (not only the ones below): Django (writing-documentation, coding-style, submitting-patches, committing-code), rustc-dev-guide (conventions, git, contributing), Node.js (pull-requests.md, api-documentation.md, collaborator-guide.md, cpp-style-guide.md), Go (go.dev/doc/contribute), Spring (CONTRIBUTING.md), Elastic (contribute-docs, cumulative docs, style guide), Docker (docs repo STYLE.md, AGENTS.md, CONTRIBUTING.md), HashiCorp (web-unified-docs CONTRIBUTING.md), Ansible (documentation style guide, changelog fragments), Prometheus (CONTRIBUTING.md), Grafana (CONTRIBUTING.md, merge-pull-request.md), Red Hat (supplementary style guide, modular docs).

Existing-card check: `rg` over `cards/` and `docs/research/` before each lead. No card covers commit messages (`rg -il "commit message|subject line" cards` finds no commit-message rule), directional words, minimizing words, Latin abbreviations, or version annotations in docs. Pass 3c already mined time-relative words, so they are not repeated here.

Org count in each `Count:` line uses organisations, not pages. "Verified" means the sentence is in the raw text I downloaded.

## A. Commit subject: imperative mood and short (no card)

Rule candidate: "Write the commit subject as an imperative summary of 72 characters or fewer."
Nearest card: `chg-author-hygiene` (self-review and write the description; it does not say how the subject reads). Not covered.

1. https://docs.kernel.org/process/submitting-patches.html . Linux kernel. Describe changes in imperative mood, as an order to the codebase. Found: "Describe your changes" section, imperative paragraph. Subject form is `subsystem: summary phrase`.
2. https://www.kubernetes.dev/docs/guide/pull-requests/ . Kubernetes. Subject 50 characters or fewer, never over 72; use imperative mood; no trailing period. Found: "Commit Message Guidelines" list.
3. https://raw.githubusercontent.com/spring-projects/spring-framework/main/CONTRIBUTING.md . Spring. Subject at most 55 characters, imperative verb, no period. Found: "Commit Messages" bullets.
4. https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md . Node.js (OpenJS). First line 50 characters or fewer preferably, 72 at most, starts with an imperative verb. Found: "Commit message guidelines", item 1.
5. https://handbook.gnome.org/development/commit-messages.html . GNOME. Summary at most 72 characters, imperative present tense ("Add", not "Added"). Found: "Summary line" section.
6. https://google.github.io/eng-practices/review/developer/cl-descriptions.html . Google. First line is a short summary, written as though it was an order. Found: "First Line". Go (https://go.dev/doc/contribute) is the same org; its rule completes "This change modifies Go to ...", lowercase, no full sentence. Found: "First line" under "Good commit messages".
7. https://docs.gitlab.com/development/contributing/merge_request_workflow/ . GitLab. Subject at most 72 characters, no trailing period, starts with a capital. Found: "Commit messages guidelines". Length and period only; no imperative rule.
8. https://guides.rubyonrails.org/contributing_to_ruby_on_rails.html . Rails. Ideal summary 50 characters or fewer, body wrapped at 72. Found: sample message after "A good commit message looks like this". Length only.
9. Counter-evidence: Django (https://docs.djangoproject.com/en/dev/internals/contributing/committing-code/) says write the subject in the past tense and end with a period, with "Fixed" correct and "Fixes" incorrect. Found: "Write detailed commit messages in the past tense". The mood half is contested; the length half is not.

Count, short subject (about 50 to 72 characters): Kubernetes, Spring, Node.js, GNOME, GitLab, Rails, Linux kernel (75 on the body, summary phrase) = 7 organisations.
Count, imperative mood: Linux kernel, Kubernetes, Spring, Node.js, GNOME, Google = 6 organisations. Django disagrees (past tense). Suggested rule: "Write the commit subject as a short summary of 72 characters or fewer, in one mood the project uses." Mood as a rule needs the Django counterpoint in the card.
Verdict: clears three on length and on imperative mood. Draft card candidate: `chg-commit-subject-summary`.

## B. Commit body explains why (no card)

Rule candidate: "Give a commit that changes behaviour a body that says why it was made."
Nearest card: `chg-author-hygiene` (self-review and write the description before review; its Why says the description gives the reason). It is stable and broad, so a "why in the commit" clause is a new card or a clause on it; `chg-link-tracked-issue` covers the issue link only.

1. https://docs.djangoproject.com/en/dev/internals/contributing/committing-code/ . Django. The body explains why the change was made, not what or how. Found: "should explain why the change was made, not what was changed".
2. https://raw.githubusercontent.com/spring-projects/spring-framework/main/CONTRIBUTING.md . Spring. The description explains the motivation, for example "Prior to this commit". Found: "Commit Messages" bullets.
3. https://docs.kernel.org/process/submitting-patches.html . Linux kernel. Start by describing the problem that motivated the work and convince the reviewer it is worth fixing. Found: "Describe your changes", first paragraph ("Describe your problem").
4. https://guides.rubyonrails.org/contributing_to_ruby_on_rails.html . Rails. A descriptive message helps others understand why the change was made; include what the linked issue says. Found: text before the sample message.
5. https://handbook.gnome.org/development/commit-messages.html . GNOME. Treat the message as an email to a future reader about why you changed it; no need for the how. Found: "no need to specify the how".
6. https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md . Node.js. A good message describes what changed and why. Found: first sentence of "Commit message guidelines". Includes "what", so it backs the clause loosely.
7. https://google.github.io/eng-practices/review/developer/cl-descriptions.html . Google. Body gives the problem being solved and why this approach. Found: "Body is Informative". Same org as Go, whose guide says to give context and explain what the change does.

Count: Django, Spring, Linux kernel, Rails, GNOME = 5 firm; Node.js and Google loose. Existing card: `chg-author-hygiene` (stable).
Verdict: clears three. Draft card candidate: `chg-commit-body-says-why`. A diff-level FAIL is a subject-only commit that changes behaviour with no reason in the body or description.

## C. Area prefix on the commit or PR title (no card)

Rule candidate: "Prefix the commit or pull request title with the area it changes."
Nearest card: none (`chg-link-tracked-issue` covers the link, not the title).

1. https://docs.kernel.org/process/submitting-patches.html . Linux kernel. Canonical subject is `subsystem: summary phrase`. Found: "Subject Line" section.
2. https://go.dev/doc/contribute . Google (Go). First line prefixed by the primary affected package. Found: "First line" under "Good commit messages".
3. https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md . Node.js. First line prefixed with the changed subsystem; `git log --oneline` shows which. Found: "Commit message guidelines", item 1.
4. https://raw.githubusercontent.com/prometheus/prometheus/main/CONTRIBUTING.md . Prometheus. Title formatted `area: short description`. Found: "PR triage dashboard" bullets.
5. https://raw.githubusercontent.com/grafana/grafana/main/contribute/merge-pull-request.md . Grafana Labs. PR title is `Area: Summary`; it becomes the squash subject and the changelog line. Found: "Format the pull request title".
6. https://handbook.gnome.org/development/commit-messages.html . GNOME. May prefix the first line with one tag naming the part of the module. Found: "Uses imperative present tense" paragraph. Optional ("can").
7. Counter-evidence: Spring bans `fix:` or `feat:` type prefixes in the subject (CONTRIBUTING.md, "Commit Messages"). It bans type words, not area. GitLab allows `fix:` or `[API]` but does not require one.

Count: Linux kernel, Google (Go), Node.js, Prometheus, Grafana Labs = 5 firm; GNOME optional. Verdict: clears three. Draft card candidate: `chg-commit-title-names-area`. Weakness: Kubernetes, Rails, Django, Spring do not use it, so the card should say "where the project uses area prefixes".

## D. Each commit builds and passes tests (bisectable) (no card)

Nearest card: `chg-one-concern` (one logical thing per change; says nothing on each commit in a series).

1. https://docs.kernel.org/process/submitting-patches.html . Linux kernel. In a patch series the kernel must build and run after each patch, since `git bisect` can split anywhere. Found: "Separate your changes" ("take special care").
2. https://raw.githubusercontent.com/prometheus/prometheus/main/CONTRIBUTING.md . Prometheus. Each commit should compile and pass tests independently. Found: "Pull Request Checklist", second bullet.
3. https://docs.djangoproject.com/en/dev/internals/contributing/committing-code/ . Django. Tests should pass and docs should build after each commit. Found: "Tests should pass and docs should build after each commit".
4. https://rustc-dev-guide.rust-lang.org/git.html . Rust. Linear history (no merge commits) simplifies bisecting; a merge commit in a PR is not allowed. Found: "no-merge" policy paragraph. Backs the linear-history half, not "each commit builds".
5. Not found: Python devguide, Kubernetes pull-request guide and Chromium contributing page have no "each commit builds" sentence in the raw text.

Count: Linux kernel, Prometheus, Django = 3 firm on "each commit builds and passes"; Rust partial. Verdict: reaches three. A diff reviewer can only mark FAIL by reading per-commit CI, so tool_gate would be a per-commit CI run. Draft card candidate: `chg-each-commit-builds`.

## E. Docs state the version that added or changed a feature (no card)

Rule candidate: "Mark a new or changed feature in docs with the version that introduced it."
Nearest cards: `fn-deprecation-names-version-and-replacement` (deprecations only), `chg-changelog-entry`, `chg-docs-updated-with-code`.

1. https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/ . Django. Significant changes are marked with `versionadded` and `versionchanged`, and also noted in the release notes. Found: "Documenting new features".
2. https://devguide.python.org/documentation/markup/ . Python (PSF). `versionadded` records the version that added a feature; use `next` until release. Found: "versionadded" paragraph.
3. https://raw.githubusercontent.com/nodejs/node/main/doc/contributing/pull-requests.md . Node.js. Adding or deprecating an API means adding the YAML version metadata, using a placeholder until release. Found: just before the C++ style note. Also `introduced_in` and `added` in api-documentation.md ("Writing Documentation").
4. https://www.elastic.co/docs/contribute-docs/how-to/cumulative-docs/ . Elastic. Tag content when functionality is added or changes state, with `applies_to`; page-level tag mandatory. Found: "When to tag content".
5. https://raw.githubusercontent.com/docker/docs/main/AGENTS.md . Docker. Version-introduction notes ("Starting with ...") mark when a feature arrived; keep recent ones. Found: "Version-introduction notes". Describes keeping the notes; it does not say authors must add them.

Count: Django, Python, Node.js, Elastic = 4 firm; Docker partial. Verdict: clears three. Draft card candidate: `code-docs-mark-version-added`. Not checked: Kubernetes feature-state shortcode (pages 200 but sentence not isolated), GitLab history notes (not found in the pages fetched).

## F. Docs avoid directional words (above, below, left, right) (no card)

Rule candidate: "Refer to docs by link or 'previous'/'following', not 'above' or 'below'."
Nearest cards: `code-docs-link-text-descriptive` (link wording), `fn-img-alt-text` (images). Neither covers position words.

1. https://developers.google.com/style/word-list . Google. Do not use above or below for a position in a document or UI; use earlier or following. Found: entries "above" and "below". Also https://developers.google.com/style/accessibility ("directional language" paragraph).
2. https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/b/below . Microsoft. Do not use as an adjective ("the code below"); use a link, "later" or "the following". Found: opening lines. Same for `/a/above`.
3. https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Writing_style_guide . Mozilla. Avoid spatial and directional words such as above, below, left, right, here. Found: "Use accessible language".
4. https://docs.gitlab.com/development/documentation/styleguide/word_list/ . GitLab. Avoid "above" for an example or table; say "previous". Found: entry "above".
5. https://www.elastic.co/docs/contribute-docs/style-guide/ . Elastic. Avoid directional language, and use device-agnostic verbs. Found: "Accessibility and inclusivity" paragraph.
6. https://redhat-documentation.github.io/supplementary-style-guide/ . Red Hat. Avoid left, right, above and below, since a screen reader gives them no meaning. Found: "Colors and other visual information" and "Images" sections. Ansible (https://docs.ansible.com/ansible/latest/dev_guide/style_guide/index.html) is Red Hat; its "Colors and other visual information" says not to rely only on sensory characteristics.
7. https://raw.githubusercontent.com/docker/docs/main/STYLE.md . Docker. Word list maps "below" to "following" and "above" to "previous". Found: "Recommended terms" table. Weak: a table row, no reasoning.

Count: Google, Microsoft, Mozilla, GitLab, Elastic, Red Hat = 6 firm; Docker weak. Verdict: strongest lead in the pass. Draft card candidate: `code-docs-no-directional-words`. Counterpoint to carry: a reference inside a short section is harmless; Google allows "below" in non-spatial phrases ("below zero").

## G. Docs avoid words that minimise effort (simply, easily, just) (no card)

Nearest card: none (`code-docs-no-future-promises` is about promises).

1. https://docs.djangoproject.com/en/dev/internals/contributing/writing-documentation/ . Django. Avoid words that minimise difficulty: easily, simply, just, merely, straightforward. Found: "Voice" section.
2. https://docs.gitlab.com/development/documentation/styleguide/word_list/ . GitLab. Do not use simply or simple; also easily. Found: entries "simply, simple" and "easily". A Vale rule enforces it.
3. https://developers.google.com/style/word-list . Google. Try removing easy and easily; it may not be easy for others. Found: entry "easy, easily".
4. https://raw.githubusercontent.com/docker/docs/main/STYLE.md . Docker. Avoid hedge words: simply, just, easily, seamlessly. Found: "Avoiding marketing language". AGENTS.md says Vale enforces it.
5. https://www.elastic.co/docs/contribute-docs/style-guide/ . Elastic. Word choice list marks easy, simple and please as words to avoid. Found: "Word choice" paragraph.
6. Not counted: Kubernetes ("simple and direct language" is about plain wording); MDN, Rails and Python use "simple" as a plain-language ask, not a ban.

Count: Django, GitLab, Google, Docker, Elastic = 5 organisations. Verdict: clears three. Draft card candidate: `code-docs-no-minimising-words`. Counterpoint: a grep list produces false hits ("just in time").

## H. Docs use English words, not Latin abbreviations (e.g., i.e.) (no card)

Nearest card: none.

1. https://kubernetes.io/docs/contribute/style/style-guide/ . Kubernetes. Prefer English terms over Latin abbreviations; "for example", not "e.g."; "etc." is the exception. Found: "Avoid Latin phrases".
2. https://devguide.python.org/documentation/style-guide/ . Python. Do not use "e.g." or "i.e." where English words will do. Found: "Use simple language".
3. https://developers.google.com/style/word-list . Google. Do not use e.g. or i.e.; write "for example" or "that is". Found: entries "e.g." and "i.e.".
4. https://docs.gitlab.com/development/documentation/styleguide/word_list/ . GitLab. Do not use Latin abbreviations; a Vale rule `LatinTerms` checks it. Found: entry "e.g.".
5. https://raw.githubusercontent.com/docker/docs/main/STYLE.md . Docker. Word list maps "e.g." to "for example, such as". Found: "Recommended terms" table. Weak.
6. https://docs.ansible.com/ansible/latest/dev_guide/style_guide/index.html . Red Hat (Ansible). A heading, "Avoid using Latin phrases", says non-native readers may find them harder. Found: the section under that heading.

Count: Kubernetes, Python, Google, GitLab, Red Hat = 5 firm; Docker weak. Verdict: clears three; low value, so a draft at `nit` severity. Draft card candidate: `code-docs-no-latin-abbreviations`.

## Leads with fewer than three organisations, or already covered

- Doc image alt text and no screenshots of CLI output: Ansible (use a code block) and Red Hat (avoid screenshots, alt text unique), Elastic (alt text for all images). Red Hat and Ansible are one org. 2 organisations (Red Hat, Elastic); not searched further. Nearest `fn-img-alt-text` (UI); check whether it applies to docs before drafting.
- Move or rename pages in a separate PR from rewriting them: HashiCorp (web-unified-docs CONTRIBUTING.md, "Keep changes reviewable"), Google eng-practices small CLs (moving and renaming a class goes in a different CL from a fix). Google and HashiCorp = 2. Better as a clause on `chg-refactor-separate`; add both URLs to its `borrowed_from` (step 5).
- Test docstrings state the behaviour, no "Tests that" preamble: Django coding-style only. 1 org.
- Docs page opens with what it covers and why it matters: Docker STYLE.md only in this pass. 1 org.
- Docs build with spelling and style checks in CI: Django (must pass before merge), Docker (Vale), GitLab (Vale), Elastic (Vale mentioned). A repo-level practice, hard to FAIL in a diff; skipped.
- No merge commits in a PR (linear history): Rust (no-merge policy), Django ("Beware of merges of upstream branches"). 2. Pass 4 source-sweep row lists a Rust rule; not extended.
- Comment deprecated-code hooks with the removal marker (Django `RemovedInDjangoXXXWarning`): 1 org; nearest `fn-deprecation-names-version-and-replacement`.
- Rust "TODO comments for things to fix before landing" (rustc conventions) conflicts in direction with `fn-todo-has-owner-or-issue`; 1 org; skip.
- Feed to existing cards (step 5): `chg-changelog-entry` gains Ansible changelog fragments (docs.ansible.com development_process page: "you must add a changelog fragment" to PRs that change functionality) and Grafana (merge-pull-request.md asks whether a PR needs a changelog entry), and Django (backwards-incompatible changes need a release-notes note: submitting-patches "contribution checklist"). Those need a borrowed_from edit, not done here (this pass edits no other file).
- `chg-link-tracked-issue` gains Go, Spring, Django ("Fixed #xxxxx") for the reference form; Go and Spring already state `Fixes`/`Closes` syntax.

## Unreachable or unverified

- Docker docs site pages (docs.docker.com/contribute/...) return the 404 page; the docker/docs repo raw files were used instead (STYLE.md, AGENTS.md, CONTRIBUTING.md are fetched and verified).
- Rust std-dev-guide: `documentation/doc-comments.html`, `policy/deprecating.html`, `documentation/doc-examples.html` and `documentation/summary.html` returned 404. Only the root, `policy/doc-alias.html` and `development/feature-lifecycle.html` loaded; nothing relevant was found in them. rustc-dev-guide `contributing.html` is a short index page.
- Node.js `deprecations.md` (doc/contributing) is 404 at that path.
- Spring `CODE_STYLE.md` is 404; the code-style rules sit in CONTRIBUTING.md. Not read for comment rules beyond the Javadoc first-sentence note (imperative first sentence, "Return" not "Returns"); one org, not searched.
- HashiCorp: `terraform-provider-aws` documentation page 404; the versioning best-practices page loaded but holds no docs or comment rule. Terraform `.changes/README.md` is only 339 bytes.
- Prometheus `docs/README.md` 404; `prometheus.io` writing-exporters not read for docs rules.
- Grafana documentation style guide URLs on GitHub raw return 404, and the Writers' Toolkit style page is JavaScript-rendered with little text; Grafana appears only through CONTRIBUTING.md and merge-pull-request.md.
- Atlassian Design System (atlassian.design) and the Atlassian developer pages are JavaScript-rendered or 404 for raw fetch: unverified, not counted.
- Twilio and Stripe: only product and marketing pages were reachable (Twilio glossary, Stripe building-with-llms); no contributor or style guidance found. Not counted.
- Python devguide `core-developers/commit-bit` is 404; the pull-request lifecycle page was used (it gives a sample message structure, no rule found beyond that).
- Microsoft Learn word-list URLs for "simple", "easy" returned the 404 page, so Microsoft does not count for lead G. Learn's "above"/"below" entries loaded and count for F.
- Microsoft and Google rows for F were found in the word list pages; Google's separate `directional-language` URL is 404 and is not used.
- Kubernetes feature-state, GitLab version-history notes: pages loaded but I did not isolate a clean sentence; not counted for lead E.
- WordPress commit-message handbook (make.wordpress.org/core/handbook/best-practices/commit-messages/): loaded, summary line is about 50 characters and 70 at most; only that one sentence checked, so WordPress is not counted in A or B beyond the length point.
- Mozilla (firefox-source-docs contributing_code): no commit-message rule found in the stripped text, so Mozilla does not count for A to D.

## Summary

Seven leads reach three organisations on raw text and have no card: A (commit subject short and imperative), B (commit body says why), C (area prefix, with the caveat that several projects skip it), D (each commit builds), E (version added or changed in docs), F (no directional words in docs), G (no minimising words), H (no Latin abbreviations). Strongest by count and clarity: F (6), A (7 on length, 6 on mood), B (5), G (5), H (5), E (4). Commit-message cards are the largest gap: `chg-author-hygiene` is the only card that touches them. Pablo's call: whether commit rules sit at change level as new `chg-` cards or as one card with the subject and body rules split into separate clauses. Existing-card feeds: `chg-changelog-entry`, `chg-refactor-separate`, `chg-link-tracked-issue`.

## Parent verification and outcome (2026-11-22)

Re-fetched raw and matched the sentence for A, B, D, E, F and G (and C for the kernel, Node.js and Prometheus; the Grafana and Go rows did not match in my fetch, so C counts three). New stable cards: `chg-commit-subject-imperative`, `chg-commit-body-says-why`, `chg-commit-title-area-prefix`, `chg-each-commit-builds` (kernel, Prometheus, Django), `chg-doc-marks-version-added`, `code-docs-no-directional-words`, `code-docs-no-minimising-words`. Not carded although they clear the bar: Latin abbreviations in docs (H: Kubernetes, Python, Google, GitLab, Red Hat) and no links in headings (Google, GitLab, Python), as style-only rules a Vale config already covers. Step-5 feeds the agent suggested (Ansible, Grafana, Django release notes into `chg-changelog-entry`; HashiCorp and Google small-CLs into `chg-refactor-separate`) were not verified and are not applied.

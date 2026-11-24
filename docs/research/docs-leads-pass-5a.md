# Docs leads, pass 5a

Fetched 2026-11-22 with `curl -sL`, tags stripped with `python3 -I`, each sentence found with `rg` in the stripped text (fresh scratch dir). Paraphrases only. WebSearch was used for discovery only; no search snippet counts. Existing-card check: `rg` over `cards/audit/codebase` and `cards/audit/function` found no card for N, P, K, E or the two F2 practices. Nearby: `code-dead-docs-deleted` (K, E), `code-docs-link-text-descriptive`, `code-docs-link-dont-duplicate` (F2), `fn-heading-structure` (HTML heading levels, not links).

## N. A library or SDK has a troubleshooting doc (no card)

1. https://azure.github.io/azure-sdk/general_documentation.html . Microsoft (Azure SDK). Each library root holds a TROUBLESHOOTING.md for customers and support. Raw: "TROUBLESHOOTING.md - Resides in the root of your library".
2. https://posthog.com/handbook/engineering/sdks/guidelines . PostHog. Every SDK should have a troubleshooting page covering install, build, config, network and runtime errors. Raw: "Each SDK should have a troubleshooting page".
3. https://docs.sentry.io/contributing/approach/sdk-docs/ . Sentry. The standard SDK docs layout includes a Troubleshooting section for known corner and edge cases (kept at SDK level). Raw: "Troubleshooting Covers corner and edge cases we know of". It is a listed section of the structure, not worded "must"; the Migration Guide beside it is the one marked optional.
4. https://www.elastic.co/docs/contribute-docs/content-types/troubleshooting . Elastic. Defines the format of a troubleshooting page (Symptoms, Resolution). Not a duty to have one per library. Not counted.
5. https://redhat-documentation.github.io/supplementary-style-guide/ . Red Hat. Procedures should include troubleshooting, recovery and verification steps. Raw: "Be sure to include troubleshooting, error recovery". Per procedure, not per library. Not counted.
6. https://docs.gitlab.com/development/documentation/topic_types/troubleshooting/ . GitLab. Per feature page, rare cases included. Raw: "All troubleshooting information is included". Not counted (per page).

Count: 3 orgs (Microsoft, PostHog, Sentry). Meets the bar, with Sentry the softest (layout list, not a "should"). Wording that fits all three: "a library or SDK has its own troubleshooting page". Kubernetes and Django have troubleshooting/FAQ pages as site content but no rule found. Existing card: none.

## P. Names built at runtime: avoid, or list the values in a comment (no card)

1. https://www.mediawiki.org/wiki/Manual:Coding_conventions . Wikimedia. Avoid building message keys, CSS class names or file names dynamically; if you must, leave a nearby comment with the possible values for search. Raw: "you must leave a comment nearby with the possible".
2. https://tailwindcss.com/docs/detecting-classes-in-source-files . Tailwind Labs. Class names built by concatenation or props are not found in the source, so write complete class names. Raw: "Don't construct class names dynamically". Reason is a scanner limit, not grep; adjacent.
3. https://docs.djangoproject.com/en/stable/topics/i18n/translation/ . Django. Translation strings held in variables are not found by `makemessages`. Raw: "won't be able to find". Tool limit; adjacent, and it states a caveat rather than a rule.
4. https://unpkg.com/kibana-123@5.2.1/style_guides/css_style_guide.md (same text at raw.githubusercontent.com/elastic/kibana/5.2/style_guides/css_style_guide.md; removed from `main`). Elastic (Kibana). Do not build concatenated SCSS selector names, they are hard to grep. Raw: "really difficult to grep for". Build-time nesting, not runtime; adjacent.
5. https://docs.gitlab.com/development/fe_guide/style/scss/ . GitLab. Avoid compound class names made with SCSS `&`; it makes searching for usages harder. Raw: "It makes searching for usages harder". Build-time; adjacent.
6. https://google.github.io/styleguide/pyguide.html . Google. Log and error messages keep interpolated pieces identifiable so they can be grepped. Raw: "allow simple automated processing (e.g. grepping)". Messages, not identifiers; adjacent.
7. https://www.kernel.org/doc/html/latest/process/coding-style.html . Linux kernel. Never break user-visible strings across lines so they stay greppable. Raw: "breaks the ability to grep for them". Strings; adjacent. Airbnb (README, "make code less searchable") and the Google C++ guide ("searchability") say the same about long literals.
8. https://docs.ansible.com/ansible/latest/tips_tricks/ansible_tips_tricks.html . Ansible. A variable-name layer keeps secret-variable names greppable. Raw: "keep the names of your variables accessible (by grep". Different practice; not counted.

Count, exact practice (runtime-built identifiers get a values comment or are avoided): 1 org (Wikimedia). Count, looser practice ("write names and strings in full so they can be searched"): Wikimedia, Elastic, GitLab, Google, Linux kernel, Airbnb = 6, but only Wikimedia covers runtime construction, and none of the others covers identifiers built at runtime in a way a reviewer would call the same rule. Recommendation: a card is feasible only on the looser wording ("don't assemble or split a name or message so grep cannot find it"), with MediaWiki's comment as the fallback clause; ask Pablo whether he accepts that merge. Not reachable: biggerpockets.github.io greppable-code (blog-grade, a company handbook, not re-fetched); drupal.org/node/1887918 (returned 307 bytes). Existing card: none.

## K. Unreferenced doc, image or example files are deleted (draft nearby: code-dead-docs-deleted)

1. https://developers.cloudflare.com/style-guide/how-we-docs/image-maintenance . Cloudflare. Remove images no longer referenced; a GitHub Action flags unused images and opens an issue. Raw: "remove images that are no longer referenced". Includes the CI check.
2. https://kubernetes.io/docs/contribute/style/style-guide/ . Kubernetes. A standalone YAML example that no topic references should be deleted rather than updated. Raw: "not referenced from any topics, consider deleting". Soft ("consider").
3. https://raw.githubusercontent.com/Qiskit/documentation/main/scripts/js/commands/checkStaleImages.ts . IBM (Qiskit). A CI script fails the build when an image is unused and says it should usually be deleted. Raw: "They should usually be deleted". This is a script message, not a guide sentence; partial.
4. https://www.jetbrains.com/help/writerside/maintenance-and-cleanup.html.md . JetBrains. Without cleanup after removals you end up with unused topics and images; the tool reports unreferenced images and suggests removal. Raw: "unused topics, images, and pieces of content". Tool documentation; partial.
5. https://docs.gitlab.com/development/documentation/workflow/ . GitLab. Dropped features leave orphaned content, so delete prematurely added docs. Raw: "Dropped features leave orphaned content". Also a merge request (gitlab.com/gitlab-org/technical-writing/docs-gitlab-com/-/merge_requests/428) adds a monthly find-unused-images task with an exit-code flag. Partial; the MR page is a change record, not a rule.
6. https://www.sphinx-doc.org/en/master/usage/restructuredtext/field-lists.html . Sphinx. A page not in any toctree raises a warning (the `orphan` field suppresses it). Raw: "not being included in any toctree". Tool behaviour; not counted.

Count: firm stated practice, 2 (Cloudflare with CI, Kubernetes soft). With the partials (IBM Qiskit script, JetBrains, GitLab) the loose count is 5, but none of the partials is a style-guide statement. Fetched, no match: Microsoft contribute pages (404), Docker, Django, MDN, Python devguide, Node.js, Mattermost README, Cloudflare style-guide index. Existing card: `code-dead-docs-deleted` (does not name orphans).

## E. Each doc page shows an owner and a last-updated or review date (no card; clause of code-dead-docs-deleted)

1. https://learn.microsoft.com/en-us/contribute/content/metadata . Microsoft. `ms.author` identifies the owner; `ms.date` is shown on the page as last substantially edited or guaranteed fresh. Raw: "Displayed on the published page". Both halves.
2. https://docs.gitlab.com/development/documentation/metadata/ . GitLab. Each page carries stage and group metadata with a Technical Writer pointer. Raw: "Stage and group metadata", "Unassigned pages Documents with no clear group owner". Owner half. The handbook page https://handbook.gitlab.com/docs/frontmatter/ recommends a `date:` for the last meaningful change ("recommended that you add a date"). Date half, handbook not docs.
3. https://grafana.com/docs/writers-toolkit/write/front-matter/ . Grafana. `review_date` records when a page was last reviewed for correctness. Raw: "set the date you last reviewed a page". Date half.
4. https://developers.cloudflare.com/style-guide/how-we-docs/metadata/index.md . Cloudflare. Tracks last-modified for every page and last-reviewed for important content types only. Raw: "Last reviewed (optional)". Date half; also .../component-attributes/last-updated/index.md says the page footer shows the Git-based date. Raw: "A date displayed at the bottom of each page".
5. https://docs.optimism.io/op-stack/contribute/curation-policy.md . Optimism. Every curated page carries a `last-reviewed:` front-matter stamp that is checked on sweeps. Raw: "Every curated artifact carries a review stamp". Date half, curated pages only, a foundation docs site.
6. Not counted: Google, Red Hat and Kubernetes render "Last updated" or "Last modified" in the page footer (seen in raw text), which is site behaviour, not a stated practice. Angular reviewing-content page (reported as "no Last reviewed date means never reviewed") could not be read: the angular.dev page is a client-rendered shell and the raw markdown paths returned nothing; it would also be Google. Backstage/Spotify ownership: no raw sentence found.

Count: date half, 5 orgs (Microsoft, GitLab recommended, Grafana, Cloudflare partly optional, Optimism curated only). Owner half, 2 (Microsoft, GitLab). Owner plus date together: Microsoft only. A card worded "each page records when it was last reviewed" clears the bar on the date half, with Grafana and Microsoft the cleanest. Existing card: none; `code-dead-docs-deleted` names it only in a tool_gate.

## F2a. No links in headings (no card)

1. https://developers.google.com/style/headings . Google. Do not put links in headings; a link can be mistaken for heading style. Raw: "Don't put links in headings."
2. https://docs.gitlab.com/development/documentation/styleguide/links/ . GitLab. Do not use links in headings; they cause errors. Raw: "Headings that contain links cause errors."
3. https://devguide.python.org/documentation/style-guide/ . Python. Do not use links in section headers; they distract and the term can be linked in the paragraph. Raw: "Do not use links in section headers."
4. Searched and not found in Microsoft, Kubernetes, MDN, Red Hat, GitHub Docs, Chef (linking page), Docker, Django, Elastic: no sentence. Splunk style guide linkformatting page returned 29 bytes (unreachable).

Count: 3 orgs (Google, GitLab, Python), unchanged from pass 4c. Meets the bar. Existing card: none (`fn-heading-structure` is HTML levels).

## F2b. Examples use documentation-reserved domains and addresses (no card)

1. https://developers.google.com/style/examples . Google. Use example.com, example.org or example.net, which IANA reserves for documentation, and no real domain names. Raw: "Don't use real domain names, email addresses".
2. https://docs.digitalocean.com/style/digitalocean/language/domains-and-ip-ranges/ . DigitalOcean. Examples and tutorials use only domains and IP ranges reserved for documentation (RFC 2606, RFC 5737, RFC 3849). Raw: "use only domains and IP address ranges that are explicitly reserved".
3. https://www.rfc-editor.org/rfc/rfc2606.txt . IETF (BCP 32). Reserves TLDs and second-level names for examples in documentation. Raw: "examples in documentation, DNS related experimentation". A standard, counted as an org in pass 4c.
4. https://redhat-documentation.github.io/supplementary-style-guide/ . Red Hat. Use the IP and MAC ranges reserved for documentation. Raw: "ranges that are reserved for documentation purposes". Addresses only, not domains; adjacent.
5. Microsoft style-guide pages on placeholders and fictitious names returned the 690-byte stub (404 for this path set); `urls-web-addresses` fetched and shows only an example.com sample in a URL, no rule. Kubernetes, GitLab, MDN, Django, GitHub Docs fetched, no rule sentence.

Count: Google, DigitalOcean, IETF = 3 for domains; Red Hat adds a 4th only if the card widens to "documentation-reserved IP and domain ranges". Meets the bar if the IETF standard is accepted as an organisation (it is a definition of the reservation, close to a "definition page" the rule excludes). Decision for Pablo: with IETF excluded the count is Google, DigitalOcean (2) plus Red Hat on the wider wording (3). Existing card: none.

## Unreachable or unverified in this pass

- Google Cloud Java TROUBLESHOOTING.md (14-byte raw response), Angular reviewing-content (empty shell), Splunk linking page (29 bytes), drupal.org node 1887918 and standards page (307 bytes), Microsoft style-guide placeholder and fictitious-name pages (stub), Grafana `style-guide/structure` and troubleshooting topic-type paths (404), Docker contribute pages (site shell, no match), New Relic useful-scripts (stub), Blender manual check_images.py (404), GitLab `docs.gitlab.com` handbook date page read (counted as GitLab).
- Fetched, no match for any lead: Django, Rust API guidelines, Node.js, Mozilla coding style (Firefox source docs), WordPress PHP standards, Home Assistant docs, Docker, GitHub Docs, MDN writing guide, Kubernetes content guide (beyond row K2).
- Search-snippet only, not read raw, not counted: Scayle translation guide (dynamic i18n keys; page returned 489 bytes), i18next best practices (no match), BiggerPockets greppable code, Apertis and New Relic unused-image scripts.

## Parent outcome (2026-11-22)

No card from this pass. Troubleshooting doc per library has PostHog and Azure SDK firmly and Sentry as a layout list, so it stays a lead. Runtime-built names stays a lead (MediaWiki only; a looser "keep names greppable" wording is a maintainer call). Orphan doc files, owner-and-date per page and reserved example domains stay below the bar or depend on whether a definition page counts.

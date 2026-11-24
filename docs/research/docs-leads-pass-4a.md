# Docs leads, pass 4a

Fetched 2026-11-22 with `curl -sL`, tags stripped with `python3 -I`, sentence found with `rg` in the stripped text. Paraphrases only. Raw copies stayed in the session scratchpad. Existing-card check: `rg` over `cards/` found no card for M, N or K. For E, `code-dead-docs-deleted` (draft) names "last-reviewed date or owner per page" only in its `tool_gate`; `code-docs-link-dont-duplicate` mentions README-per-directory in its note as Google-only.

## M. Each package or component directory has a README saying what it holds

Existing card: none.

1. https://google.github.io/styleguide/docguide/READMEs.html . Google. A README is a short summary of a directory's contents, and every top-level package directory should have an up-to-date one. Found: "A README is a short summary of the contents of a directory." and "All top-level directories for a code package should have an up-to-date README.md".
2. https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_guidelines.md . Chromium (Google). Any self-contained unit of code with its own directory should have a README describing what it is and how it is used. Found: "Any self contained unit of code that merits a container directory should have a README.md". Same org as row 1.
3. https://azure.github.io/azure-sdk/general_documentation.html . Azure SDK (Microsoft). Each client library ships a README.md in its root with install and usage info. Found: "README.md - Resides in the root of your library".
4. https://developer.hashicorp.com/terraform/language/modules/develop/structure . HashiCorp (Terraform). The root module and every nested module should have a README describing the module and its purpose; a nested module without one is treated as internal only. Found: "The root module and any nested modules should have README files."

Weak, not counted: GitHub Docs about-READMEs (README is optional, repo level: "You can add a README"); Open Source Guides (GitHub, project-level, "every project should include"); Ansible Galaxy dev guide (`role init` skeleton creates README.md, a tool behaviour, no rule); Python Packaging guide (PyPI-friendly README, about rendering); MediaWiki coding conventions (only file-name case for readmes).

Count: 3 distinct verified orgs: Google (Google plus Chromium), Microsoft (Azure SDK), HashiCorp. Wording must be "package, module or component root", not "every directory": no page says every subdirectory. Existing card: none (new card possible; note that Chromium and Azure add no second org).

## N. Each library or product area has a troubleshooting or FAQ doc

Existing card: none.

1. https://azure.github.io/azure-sdk/general_documentation.html . Azure SDK (Microsoft). Each library root holds a TROUBLESHOOTING.md with guidance used by customers and support. Found: "TROUBLESHOOTING.md - Resides in the root of your library".
2. https://docs.gitlab.com/development/documentation/topic_types/troubleshooting/ . GitLab. Troubleshooting topics belong with the feature page, and every troubleshooting item is included, however rare. Found: "All troubleshooting information is included". Per page, not per library. Weak.
3. https://www.elastic.co/docs/contribute-docs/content-types/troubleshooting . Elastic. Prefers dedicated troubleshooting pages with required Symptoms and Resolution sections. Found: "dedicated troubleshooting page (preferred)". It sets the format of such pages, not a duty to have one per library. Weak.

Google Cloud client libraries (google-cloud-java) ship a TROUBLESHOOTING.md, seen only in search results; the raw GitHub fetch returned empty text, and it would be Google and a file, not a stated rule. Not counted.

Count: 1 distinct verified org stating a per-library rule (Microsoft). GitLab and Elastic are per-page and format only. Does not clear the bar. A web search for a requirement in other SDK guides found none.

## E. Docs have a declared owner and a last-updated or review date

Existing card: none exact (`code-dead-docs-deleted` mentions it in `tool_gate` only).

1. https://learn.microsoft.com/en-us/contribute/content/metadata . Microsoft. `ms.author` identifies the article's owner and `ms.date` shows when it was last substantially edited or guaranteed fresh. Found: "Identifies the article's owner." and "Displayed on the published page". Both halves.
2. https://docs.gitlab.com/development/documentation/metadata/ . GitLab. Owner half only: stage and group per page, plus CODEOWNERS (from pass 3a; not re-read here). Separately https://handbook.gitlab.com/docs/frontmatter/ (re-read): a `date:` field is recommended to show the last meaningful update, and controlled documents list their code owners in CODEOWNERS. Found: "It's recommended that you add a date".
3. https://grafana.com/docs/writers-toolkit/write/front-matter/ . Grafana Labs. A `review_date` front matter field records when the page was last reviewed for correctness and is shown at the foot of the page. Found: "Use the review_date front matter to set the date you last reviewed a page". Date half only; no owner field found.
4. https://developers.cloudflare.com/style-guide/how-we-docs/metadata/ . Cloudflare. Each page shows a last-updated date taken from Git history, and an optional "last reviewed" is tracked only for important content types. Found: "Last reviewed (optional)". Date half only, optional.

Count: owner plus date together: Microsoft only. Owner: Microsoft, GitLab (2). Date: Microsoft, GitLab (recommended), Grafana, Cloudflare (optional review) = 4. A card worded "docs show a last-updated or reviewed date" has Microsoft, Grafana, Cloudflare, GitLab verified; the owner clause has two. Existing card: none for this; could become a clause on `code-dead-docs-deleted` (freshness check) rather than a new card.

## K. Orphan docs or example files that nothing references are deleted

Existing card: `code-dead-docs-deleted` is nearby (draft; wrong or obsolete docs) but does not name orphans.

1. https://kubernetes.io/docs/contribute/style/style-guide/ . Kubernetes. A standalone YAML example that no topic references should be deleted rather than updated. Found: "If a stand-alone YAML file is not referenced from any topics, consider deleting it". Soft wording ("consider").
2. https://developers.cloudflare.com/style-guide/how-we-docs/image-maintenance/ . Cloudflare. A GitHub Action opens an issue for image files no MDX references, and a build check makes it safe for a writer to delete them in a pull request. Found: "Flag unused images". Images, not pages.
3. https://docs.gitlab.com/development/documentation/workflow/ . GitLab. Docs for dropped features leave orphaned content, so delete prematurely added docs instead of hiding them. Found: "Dropped features leave orphaned content". Also https://docs.gitlab.com/development/documentation/testing/ : the `docs-i18n-lint paths` job fails when a translated file has no English source. Found: "fails if translated files". Adjacent, not the same practice.

Count: 3 distinct orgs only on a loose reading of "unreferenced doc files are found and deleted": Kubernetes (YAML examples), Cloudflare (images, automated), GitLab (orphaned translations by CI, orphaned content of dropped features). Strict count for "orphan pages or example files": Kubernetes only, with Cloudflare for images. Treat as a lead.

## Not found or unverified

- Fetch failed or returned nothing usable: DigitalOcean docs front-matter (404), New Relic content types (404), Grafana contribute style guide on GitHub (404), Google Cloud Java TROUBLESHOOTING.md (empty), Docker docs CONTRIBUTING (no relevant match), Elastic docs README (no relevant match).
- Fetched, no match for the practices: Ansible tips page, Red Hat modular docs, Django writing-documentation, MDN CONTRIBUTING, Rust CONTRIBUTING, rustc-dev-guide, Kubernetes content guide and reviewing-prs, Node.js pull-requests, Python devguide, GitHub docs best practices (all no README, owner or orphan rule).
- Not tried: Mozilla in-tree docs, Debian, Eclipse, Apache, Atlassian, Stripe, Docker beyond one page.

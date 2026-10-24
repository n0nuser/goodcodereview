# Agent readiness: gap audit of the built site

Audit of `site/` (built with `python3 tools/build.py` from commit `04b6a26`) against the checklist in [agent-readiness.md](agent-readiness.md). It covers every item marked "static-site applicable: yes", plus items 10, 21, and 22 (`_headers` may satisfy them). Items marked "no" are not listed, except where noted at the end.

State is PASS, PARTIAL, or FAIL as of the audit, before any change. "Plan" names the change in `tools/build.py`, or the reason to skip. After the change, `python3 tools/agent_ready_check.py` checks each implemented item.

Facts the repo states, and the only ones the site may use: the author Pablo González, https://pablogonzalez.me, https://github.com/n0nuser/goodcodereview, the licences (content CC BY 4.0, code MIT), and the host (Cloudflare Pages, `docs/deploy.md`).

Cloudflare Pages redirects `/x.html` to `/x` and `/index.html` to `/` ([Serving Pages](https://developers.cloudflare.com/pages/configuration/serving-pages/)). The final URL of a page is therefore the extensionless one, so canonical URLs and sitemap entries use it. Internal links keep `.html`, which still resolves.

| # | State | Evidence | Plan |
|---|---|---|---|
| 1 | PASS | `index.html` is plain HTML with one `<h1>` and about 3,000 characters of text. Filters and copy buttons need JS, but the content does not. | None. |
| 2 | PASS | `robots.txt` is `User-agent: *` and `Allow: /`. No `X-Robots-Tag`, no meta `noindex`. Cloudflare Pages adds no bot challenge to static assets. | None. Checked again in the check script. |
| 3 | PASS | One wildcard group, no named crawler. | Keep one wildcard group. Training crawlers stay allowed. |
| 4 | FAIL | `robots.txt` has no `Sitemap:` line. | Add `Sitemap: https://goodcodereview.com/sitemap.xml`. |
| 5 | FAIL | `site/sitemap.xml` does not exist. | Write `sitemap.xml` with every HTML page except `404.html`. |
| 6 | FAIL | No sitemap, so no `lastmod`. | `lastmod` is the date of the HEAD commit (`git log -1 --format=%cs`), one value for all pages. Outside a git checkout it falls back to the build date. |
| 7 | PASS (host) | `site/404.html` exists, so Cloudflare Pages answers missing paths with status 404 and does not fall back to a single-page app. Python's `http.server` cannot show this. | None. |
| 8 | PASS | The site needs no redirect of its own. The `.html` to extensionless redirects are real 308 responses from the host. | No `_redirects` file. |
| 9 | PARTIAL | `404.html` is a heading and one link, "Back to the start". | Rewrite the body as plain text: what happened, then a list of links with one-line descriptions (home, llms.txt, sitemap, each level). |
| 10 | SKIP | `_headers` cannot produce a 429. Cloudflare answers throttled requests at the edge. | None. The site sets no rate limit and serves no challenge page. |
| 12 | PASS | Home has real anchors to every level page, the Concerns page, and the packs. No pricing: the content is free, and the About page says so. | None. |
| 13 | PASS | Home opens with "Choose a review" and has "Start a review with an agent". | None. |
| 14 | PARTIAL | One page per answer, but no `<link rel="canonical">`. | Add canonical to every page (extensionless URL). |
| 15 | PARTIAL | Source fences in `cards/` carry a language tag, but the rendered `<pre><code>` has no `language-*` class. Fences are balanced (the build fails otherwise). | Render the fence tag as `class="language-x"`. |
| 16 | PARTIAL | `llms.txt` is 17,017 characters, under 30K, with an H1. It has no blockquote summary, and the links are bare `Full text: URL` lines. | Blockquote summary. Links in `- [Title](URL): description` form. |
| 17 | PARTIAL | All links point to files the build writes, but nothing checks it. | `agent_ready_check.py` resolves every own-domain link in `llms.txt` against `site/`. |
| 18 | PARTIAL | `llms.txt` links one `.md` file per level, but no index of them as such. | Keep `llms.txt` as the index and group the per-level `.md` links under one "Full text by level" section with a description each. |
| 19 | FAIL | No "when to use this site" text in `llms.txt`. | Add a "When to use this site" paragraph. |
| 20 | FAIL | The footer links only the author, source, and good-css.com. The head has no discovery links. | Footer links: About, Privacy, Contact (GitHub Issues), llms.txt, sitemap, AGENTS.md, skill folder. Head links: `rel="alternate"` for the Markdown twin and `llms.txt`, plus `rel="sitemap"`. |
| 21 | FAIL | No `_headers` file. | Write `_headers`: a `Link` header for the sitemap and `llms.txt` on every path, and a `Link` header for the Markdown twin on each page. Syntax checked against [Cloudflare Pages headers](https://developers.cloudflare.com/pages/configuration/headers/). |
| 22 | PARTIAL | Eight level `.md` files exist. No twin for home, Concerns, glossary, or the pack. No alternate link anywhere. | Add `index.md`, `concerns.md`, `glossary.md`, `pack-python.md`, `about.md`, `privacy.md`, and the alternate link on each HTML page. |
| 23 | FAIL | Level `.md` files start with `# <level>`, no frontmatter. | Frontmatter on every served `.md`: `title`, `description`, `canonical`, `updated`. The copies in `skills/` stay unchanged. |
| 25 | FAIL | No JSON-LD. | JSON-LD on the home page: `WebSite` plus a `CreativeWork` for the checklist. Name, description, URL, author, and licence only, all stated in the repo and shown in the page text. |
| 26 | SKIP | Needs `contactPoint` and `PostalAddress`. The repo states neither, and the project is not an organisation. | None. |
| 27 | SKIP | Needs `sameAs` profiles. The repo names no official profiles beyond the author's site, which `author.url` already carries. | None. No profile is invented. |
| 28 | PARTIAL | Covered by item 25: two types that match the page. | `WebSite` and `CreativeWork` only. |
| 29 | FAIL | `lang` and `<title>` exist. No canonical, no `description`, no Open Graph. | `description`, canonical, `og:title`, `og:description`, `og:type`, `og:url`, `og:site_name` on every page. No `og:image`: the site has no image, and a made-up one would be false. |
| 30 | PASS | `header`, `nav`, `main`, `footer`, a skip link, and no skipped heading levels on any page. | None. Checked again in the check script. |
| 31 | PASS | Controls are native `<button>` elements with text labels. There are no form fields. | None. |
| 32 | PASS | No hidden instruction text. The only `hidden` nodes are copy buttons that JS reveals. | None. |
| 33 | PASS | No `noindex` in the HTML. No `X-Robots-Tag`. | The new `_headers` sets none. Checked in the check script. |
| 34 | FAIL | No `/about`, `/contact`, or `/privacy`. | Add `about.html` and `privacy.html`, each over 500 characters, linked from the footer. No `/contact` page: the only contact channel is GitHub Issues, so the footer and About link to it. Writing 500 characters about one link would be filler. |
| 35 | PASS | No login, no paywall. | None. |
| 36 | FAIL | `concerns.html` has 147,159 characters of extracted text (320,830 bytes). The next largest, `function.html`, has 63,127. | Concerns page lists every stable and draft card as a row that links to the full card. Report sizes after the change. |
| 37 | PARTIAL | Titles are the bare page name, such as "Change review". | `<title>` becomes "Change review | Good Code Review" on every page but home. |
| 38 | PASS | `AGENTS.md` is in the repo root. | Link it from the footer and from `llms.txt`. |
| 39 | FAIL | No `/.well-known/agent-skills/index.json`. | Write the index with the Agent Skills discovery schema 0.2.0, a `sha256` digest of `skills/good-code-review/SKILL.md`, recomputed at each build. Serve the skill files at the URL the index names. |
| 40 | SKIP | `ai-catalog.json`: the research gives the shape of one entry (an MCP server card) and `AR-FIND-04` says entries are "typed by media type". No source gives the media types for `llms.txt`, a skill, or docs. Writing them would be a guess. | None. Revisit when a source lists the types. |
| 42 | FAIL | No site-type meta tag. | `<meta name="is-agentic-site-type" content="content">` on every page. |
| 43 | PASS | `.claude-plugin/` holds the plugin manifest. | Link the skill folder from the footer. |

## Items not listed above

Items 11, 24, 41, and 44 to 55 are marked "static-site applicable: no" in the checklist. The reasons stand: they need a server, an API, MCP, auth, payments, or an off-site presence, or (item 24) request-time content negotiation that Cloudflare Pages does not do. Item 44 (pricing) is covered by one sentence on the About page: the content is free.

Item 10 appears in the table because the task listed it; it is skipped for the reason given there.

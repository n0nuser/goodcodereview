# Scaling pages: how big reference sites manage volume, and what goodcodereview.com should do

Date: 2026-11-24. Question: how do documentation and reference sites with thousands of rules or entries handle that volume for human readers and for AI agents, and what should this site do as cards grow.

Method. Primary sources only, fetched raw with `curl -sL` and stripped with `python3 -I`. A page that needs JavaScript to show its content does not count (Sonar's rules site is one, see section 3). Text sizes for third-party pages are characters left after stripping tags, so they include navigation chrome; read them as upper bounds. Repo numbers are from `cards/` front matter and the `site/` snapshot in the working tree (not rebuilt; `build.py` was not run). Nothing in `cards/`, `tools/` or `site/` was edited.

## Short answer

1. Keep level as the primary split and context as the second. Do not split by concern or by topic tag. Serve concerns and topics as generated index views, which the site already does for concerns.
2. Set one budget and enforce it for both formats: a part's `.md` twin at or under 50,000 characters (about 26 to 30 stable cards), never over 100,000; its HTML at or under 100,000 characters by `Page.chars()`. Today the HTML limit is 150,000 and `service-server.html` is 133,534.
3. When a (level, context) part is over budget, split it with a build-time planner that picks a meaningful group (concern first, then topic), names each child, and never splits by character count. Mintlify and afdocs both say this.
4. Keep the whole-level files as downloads with the truncation warning, as `docs/research/context-splitting.md` decided.

## 1. What the repo already knows

- `docs/research/agent-readiness.md` item 36: "Pages under about 100K chars of extracted text (`page-token-budget`). Sources: 4. Static-site applicable: yes". `docs/research/agent-readiness-4.md` row for `page-token-budget`: "Extracted text under about 100K chars per page. Fix: split large pages."
- `tools/config.py`: `PAGE_MAX = 150_000  # characters of text in one human page (agents read the .md twins); past it a level page splits by context`. Also `LLMS_BUDGET = 12_000`, `INDEX_BUDGET = 12_000`, `SKILL_BODY_BUDGET = 16_000`.
- `tools/agent_ready_check.py`: item 36 fails a page at `PAGE_MAX` (150,000), while item 53 fails an `.md` over `MD_MAX = 100_000` except `service.md` and `function.md` (`MD_OVER`). Item 54 checks that every part says "part n of N" and that `llms.txt` links all parts and the whole file.
- `tools/site_pages.py` `split_levels`: a level whose one-page HTML reaches `PAGE_MAX` splits into a hub plus one page per `context`. If a part is still over, the build raises `BuildError("... add a context or split the level further")`. That is a manual step today.
- `docs/research/context-splitting.md` (2026-11-11 and 2026-11-12): keep the whole file and add parts; parts say "part N of M"; in a small run (3 runs per layout, Sonnet 5.5, Read tool) whole file, five parts and both reached 59 of 59 card ids. Its own limits: truncating fetch tools, other models and harnesses, larger repos, N = 3. The AgentReady trace data it analysed: median 2 docs pages per run, 40% of runs fetched 3 or more, 14% fetched 6 or more.
- Gap found here: the checklist says about 100K for a page, the config allows 150K for HTML. afdocs fails HTML over 100,000 characters after conversion (section 2), so `service-server.html` would fail `page-size-html` while passing item 36.

## 2. Size limits and splitting guidance from the agent-readiness sources

### afdocs (https://afdocs.dev/checks/page-size)

- "Agent platforms have diverse truncation limits, from 5K characters on some platforms to over 100K on others. Pages that exceed these limits are silently truncated: the agent sees the beginning of the page and loses the rest."
- `page-size-markdown`: "Pass Under 50,000 characters. Warn 50,000-100,000 characters (fits within some platforms but may exceed others). Fail Over 100,000 characters (truncated by all major agent platforms)". `page-size-html` uses the same bands on "post-conversion character count". The "all major platforms" claim names no platform; I could not verify it.
- Fix text: "If pages are too large, break them into smaller pages", and "Large pages: Break long reference pages into smaller sections."
- `single-fetch-completeness`: "Split by meaning, don't window by size." and "Complete content that fits under the 50,000-character pass threshold should be served in one response". A continuation note "declared at the top of the content" and with an absolute URL is the pass condition.
- `page-size-transfer` (bytes, separate): pass under 1MB, "Claude Code stops at about 10MB". Our largest HTML is 360,716 bytes (service-server.html), so this one is fine.
- `content-start-position`: pass when content starts "within the first 10%". Not measured here.

### afdocs llms.txt rules (https://afdocs.dev/checks/content-discoverability.md)

- `llms-txt-size`: "Pass Under 50,000 characters. Warn 50,000-100,000. Fail Over 100,000 characters (likely truncated by major agent platforms)". Fix: "split into a root `llms.txt` that links to section-level files, each under 50,000 characters. For example, a root index might link to `/api/llms.txt`, `/guides/llms.txt`, and `/reference/llms.txt`."
- `llms-txt-links-markdown`: "Agents don't discover `.md` URL variants on their own; they follow whatever link `llms.txt` gives them." This is why `llms.txt` here links the `.md` twins (item 52).
- `llms-txt-directive-md`: a blockquote near the top of each `.md` pointing to `llms.txt` (item 49).

### afdocs at scale (https://afdocs.dev/documentation-at-scale.md)

- For sites of "roughly 500 or more documentation pages": "Use a separate config for each product, locale, or supported version that needs its own results and owner." Not a split rule for content, but it shows scope by product, locale and version, not by topic, as the unit large sites use.

### AgentReady (https://www.agentready.org/, spec https://raw.githubusercontent.com/agentready-org/standard/main/spec/spec.md)

- AR-READ-07: "The site **SHOULD** ship an `llms.txt`: a lean, described index of its key pages." No character or token limit. I searched the spec for "token", "characters", "truncat", "page size", "split": no page-size requirement. Markdown mirror is AR-READ-09, MAY; the repo's `agent-readiness.md` records that task success did not change with it.

### Ora scanner (https://ora.ai/api/checks, the data behind agentready.org's scanner)

- `page-token-budget`: "Keep each page's extracted text under ~100K characters (~25K tokens) so it fits an agent's context window without truncation. Split oversized reference pages into focused per-topic documents and link them from an index."
- `llms-txt-formatting`: "keep it under 30,000 characters. Agents truncate an llms.txt past 100,000 characters". `modular-llms-txt`: "Per-section llms.txt files (like /docs/llms.txt) so an agent working in one area gets a focused index instead of your whole site."

### Chrome Lighthouse (https://developer.chrome.com/docs/lighthouse/agentic-browsing/llms-txt)

- No size guidance. It audits existence only: "If the file is not provided by the server (resulting in a 404), the audit is marked as Not Applicable (N/A), as providing the file is optional at the moment." And the file "should follow the llms.txt specification and provide a concise Markdown summary of your site's purpose and key links."

### llms.txt spec (https://llmstxt.org/)

- "The file itself stays small enough to fit in context. The detail lives behind the links, and is fetched only when needed."
- "The file can be placed at the site root, or at any path within it, covering the pages under that path." So nested `llms.txt` files are in the spec, not an invention.
- "The 'Optional' section is used, by convention, for secondary information: links an agent can skip when a shorter context is needed."

### Mintlify (https://www.mintlify.com/blog/scaling-llms-txt, vendor blog)

- "Splitting by character count would prevent truncation, but it would create ambiguous files: llms-2.txt and llms-3.txt give no indication of their contents."
- "Each product, version, language, group, or API reference section therefore becomes a candidate for its own child file. When an index grows too large, the generator chooses among those candidates by how much space each would save."
- Result they report: "On 200 tasks across ten docs sites ... agents complete tasks 52.1% faster ... with 44.8% less tokens". These are lookup tasks on ten sites, and Mintlify sells the product, so treat the size of the effect as unconfirmed.

## 3. How real reference sites handle volume

Sizes are my measurements of the fetched page (tags stripped, chrome included) on 2026-11-24.

| Site | Unit and size | Facets and index | Evidence |
|---|---|---|---|
| Rust clippy lints, https://rust-lang.github.io/rust-clippy/master/index.html | One page, 842 lints, 621,802 chars of text | Filters by lint level, group, version, applicability, plus text filter | "Clippy Lints Total number: 842 Lint levels ... Lint groups 9 ... Version ... Applicability" |
| ESLint rules, https://eslint.org/docs/latest/rules/ | Index page 45,003 chars; one page per rule (no-unused-vars 18,452) | Grouped by type, per-rule flags | "Rules in ESLint are grouped by type to help you understand their purpose. Each rule has emojis denoting: Recommended, Fixable, hasSuggestions, Frozen." Groups: Possible Problems, Suggestions, Layout & Formatting, Deprecated, Removed |
| Kubernetes feature gates, https://kubernetes.io/docs/reference/command-line-tools-reference/feature-gates/ | One page, 258 gates, 114,715 chars of text, 778,116 bytes HTML | Split by lifecycle: alpha/beta table, graduated table, separate removed page | "For a reference to old feature gates that are removed, please refer to feature gates removed." |
| OWASP Cheat Sheets, https://cheatsheetseries.owasp.org/ | One page per topic, about 150 sheets (Authentication 43,440 chars, Input Validation 13,126) | Alphabetical index plus indexes by outside taxonomy: ASVS, MASVS, Proactive Controls, Top 10 | "created to provide a concise collection of high value information on specific application security topics." Nav lists "Index Alphabetical / Index ASVS / Index MASVS / Index Proactive Controls / Index Top 10" |
| Google style guides, https://google.github.io/styleguide/ | One guide per language (C++ 212,701 chars, Python 92,735, Java 43,479), each one page with an in-page table of contents | Index page of 24 language links | "This project (google/styleguide) links to the style guidelines we use for Google code." |
| MDN, https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Page_structures/Page_types | One page per entry; landing pages for navigation | Three page categories | "Reference pages describe the details of something, and are organized according to the structure of the thing described. Guide pages describe how to do something ... Navigation pages exist primarily to provide links to other pages." An API landing page is "primarily a navigation page, but also functions as an at-a-glance reference page", and "does not link directly to specific methods or properties" |
| Microsoft Learn contributor guide, https://learn.microsoft.com/en-us/contribute/content/style-quick-start | Article length rule of thumb | n/a | "Use sections to chunk long procedures into more manageable groups of steps. (Procedures with more than 12 steps are probably too long.)" A step limit for people, no character limit |
| SonarSource rules | Retired public rule site; docs `llms.txt` is one file | n/a | https://rules.sonarsource.com/: "The standalone rules website is no longer available. You can now browse rules within SonarQube." https://docs.sonarsource.com/llms.txt is 2,244,777 bytes with 5,191 list links in one file, 22 times afdocs's 100,000 fail line |
| Awesome lists, https://raw.githubusercontent.com/sindresorhus/awesome/main/awesome.md and `pull_request_template.md` | One README per list; Awesome Python README is 84,858 chars with about 646 entries | A `Contents` section is required; outside search for big lists | "Make sure your list covers a certain scope and nothing else. Link to other awesome lists if you think they already cover a certain subject well enough." Items that are unmaintained or deprecated "should be in a separate Markdown file." Awesome Python: "Visit the website to search and filter projects more easily." |

What the table shows, and what it does not:

- The big human-facing catalogs scale by one page per entry plus an index grouped by a small fixed set (ESLint type, clippy group, OWASP outside taxonomy), and by a JavaScript filter where there is one page (clippy). Agents cannot use the filter; AgentReady AR-READ-01 wants the answer in the initial HTML.
- Where volume is in one page, nothing keeps it small: clippy (621K) and the Google C++ guide (212K) are far over the 100,000 fail line. They rely on an in-page table of contents and browser search, which suits people.
- Splitting by lifecycle status (Kubernetes removed gates, awesome lists' separate file for unmaintained items) is a repeated pattern. Here that is `status: draft` vs `stable`, already served by `llms-drafts.txt` and `cards-drafts.json`.
- Root `llms.txt` check on 2026-11-24: MDN, Kubernetes, ESLint, Microsoft Learn, OWASP, clippy and the Google style guides returned 404. Sonar docs (2,244,777 bytes) and Anthropic's docs (108,297 bytes, over 100K) returned 200. So I found no large catalog that both publishes an `llms.txt` and meets afdocs's size band, apart from Mintlify's own architecture post. I cannot cite a precedent for a rule catalog with thousands of entries splitting for agents.

## 4. Our own measurements

Counts come from `cards/` front matter (355 card files, excluding `_template.md`; a lenient line parser, because some `tool_gate:` lines are not valid YAML). Source chars are the card file length.

### Cards

| Item | Count |
|---|---|
| Cards | 355 |
| Stable / draft | 293 / 62 |
| Lang | all 355 are `core` (language packs live in `packs/`, 40 md files) |
| Severity | should-fix 239, discuss 63, block 53 |
| Concerns listed | maintainability 92, security 81, process 60, reliability 58, correctness 48, performance 35, testing 33, usability 33, compatibility 30, accessibility 28, observability 18 |
| Cards with 1 / 2 / 3 concerns | 202 / 145 / 8 |
| Topic tags | 168 distinct, 77 used once, 9 used 10 or more times (api 35, frontend 31, docs 21, ci 20, design 17, http 16, authn 13, readability 12, resilience 11); about 3.1 tags per card |
| Context | any 223, server 77, ui 31, data 17, cli 4, ui+server 2, server+data 1 |
| Stable card size | median 1,940 chars, p90 2,839, max 3,997, mean 2,026 |

Topic tags are not a controlled vocabulary: `config` and `configuration` both appear, and 46% of tags are singletons.

### By level (source chars)

| Level | Cards | Stable | Draft | Source chars |
|---|---|---|---|---|
| function | 94 | 86 | 8 | 173,396 |
| service | 84 | 70 | 14 | 189,945 |
| change | 54 | 41 | 13 | 102,241 |
| codebase | 42 | 37 | 5 | 85,349 |
| module | 36 | 25 | 11 | 65,123 |
| system | 24 | 18 | 6 | 47,993 |
| production | 14 | 12 | 2 | 29,519 |
| incident | 7 | 4 | 3 | 13,271 |

### By level and context (all cards: count, source chars)

- service: server 64 / 145,602; any 9 / 19,526; ui 5 / 11,474; data 4 / 7,984; cli 3 / 6,783.
- function: any 60 / 105,852; ui 23 / 45,413; server 10 / 18,012; data 2 / 5,376; cli 1 / 2,249.
- change: any 46 / 86,957; data 5 / 9,880; server 2 / 3,266; ui 1 / 2,138.
- codebase: any 41 / 82,367; ui 1 / 2,982. module: any 35 / 63,031; ui 1 / 2,092.
- system: any 13 / 27,308; data 6 / 11,452; server 4 / 6,957; ui 1 / 2,276.
- production: any 12 / 23,779; data 1; ui 1. incident: any 7 / 13,271.
- Cards with two contexts appear in both rows, so rows sum to 358 against 355 cards.

### Concerns by stable cards, selected parts

- service-server (51 stable, 118,748 source chars): security 32 (80,032), reliability 8 (19,643), compatibility 8 (14,215), performance 5, correctness 5, observability 2, maintainability 2, testing 1. Counted by every concern, so the sum is above 51.
- Within service-server security: authn 9 cards (26,787), http 4 (11,502), then 14 groups of 1 or 2 cards.
- Severity in service-server: block 14 (36,172), should-fix 36 (80,663), discuss 1.
- function-any (52 stable): maintainability 24, correctness 16, security 10, reliability 6, testing 5.

### Site pages (`site/`, 37 non-card HTML pages; 94 `.md` files; sitemap 36 URLs)

HTML text is `Page.chars()` from `tools/agent_ready_check.py`; the `.md` column is characters of the twin.

| Page | HTML text chars | `.md` chars |
|---|---|---|
| service-server | 133,534 | 96,306 |
| function-any | 99,851 | 73,628 |
| change | 91,879 | 56,580 |
| codebase | 78,719 | 57,517 |
| concerns | 70,103 | 101,213 |
| module | 60,045 | 46,195 |
| system | 43,949 | 26,213 |
| function-ui | 43,606 | 36,529 |
| pack-python | 37,442 | 32,757 |
| production | 27,802 | 18,778 |
| service (whole level) | n/a | 129,775 |
| function (whole level) | n/a | 130,201 |

- The ratio HTML text to `.md` is about 1.4 for level and part pages (service-server 1.39, function-any 1.36, change 1.62, codebase 1.37). The HTML text includes controls and labels the twin drops. So a 50,000-character `.md` is about 70,000 of HTML text.
- Over 100,000 HTML text: `service-server` only. In the afdocs warn band (50,000 to 100,000): function-any, change, codebase, concerns, module (60,045). That is six pages.
- Over 50,000 in `.md`, excluding the two allowed whole-level files: concerns.md 101,213 (over the 100,000 fail line), service-server 96,306, function-any 73,628, codebase 57,517, change 56,580. Item 53 only exempts `service.md` and `function.md`, so on this snapshot `concerns.md` would fail it. Either the `site/` snapshot is stale against the working tree or the check was not run; I did not run it.
- `llms.txt` 7,329 chars (budget 12,000); `llms-drafts.txt` 34,153; `llms-full.txt` 508,898 (no afdocs size check read it). Each "part n of N" line in `llms.txt` is about 405 chars.
- Card HTML pages do not exist: `site/cards/` holds JSON only (27 files). A card is reachable only inside a level or part page, by anchor. That limits how finely a reader or agent can fetch one rule and is part of why page size matters here.

## 5. Splitting options and their costs

Per-card md size is about 1,888 chars on service-server (96,306 over 51 cards). At 50,000 characters that is 26 cards; I use 26 to 30 as the rule of thumb. Page counts below are estimates, not builds.

| Axis | What it buys | What it costs here |
|---|---|---|
| Level (today, primary) | Matches the input a reviewer has ("one file is a file"); verdict is per level; llms.txt already routes by it | Levels are uneven: service has 70 stable cards, incident 4 |
| Context (today, second) | Applicability: UI cards skipped for server code; function-ui 23 cards is clean | `any` is the residual: 223 of 355 cards, so the biggest parts (function-any 52 stable, change, codebase, module) are not helped. A reader must read `any` plus their context. Only 4 values; adding one means re-judging `any` cards |
| New context value (for example `infra`) | Could shrink `any` | Authors must re-tag a large `any` set; no evidence yet which values cut it evenly. Cards with a context are only 37% of the set |
| Concern | Matches "security only" reviews (the concerns page) | 153 of 355 cards (43%) carry two or three concerns: either the rule text sits on two pages (against one canonical page per answer, AR-FIND-02) or one concern must be named primary and every author must order tags. Per level it is lopsided (service-server security 67% of source chars, so the biggest part is still 65K md). A review that must report "each card of the level" then spans up to 11 parts instead of 5, which is the completeness risk `context-splitting.md` flags |
| Topic tag | Finest grain; maps to how people think ("authn") | 168 tags, 77 singletons, synonyms exist, 9 tags with 10 or more cards. About 20 groups in service-server alone, 11 of them one card. URLs would change when tags are renamed |
| Severity | Matches `quick` (block only), `default` (block plus should-fix), `deep` | `default` needs two parts and should-fix is 80,663 source chars in service-server (about 65K md), so the part is still over 50K. Not tested beyond that count |
| Size only (part 1, part 2) | Simple | Unnamed parts. Mintlify and afdocs both warn against it |

Effects on the artifacts:

- Page counts. Getting every `.md` under 50,000 means service-server into 2, function-any into 2, codebase into 2, change into 2, and `concerns.md` turned into a hub over the existing 19 `concerns/*.md` views. About 4 new content parts, each with an HTML page and an `.md`, so the sitemap goes from 36 URLs to about 40 and the `.md` files by 4.
- `llms.txt`. Each part line is about 405 chars, so 4 more parts add about 1,600 chars (7,329 to about 8,900 of the 12,000 budget). Growth past that needs nested `llms.txt` per level, which the llms.txt spec allows and afdocs recommends.
- Indexes. `<level>-index.md` already splits by context past 12,000 chars. More parts means more lines; it must keep one line per card with a link to its part, so a skipped part is visible.
- `.md` twins. Each new part needs the same header: "part n of N", the card range at the top, absolute links to the others (afdocs: a continuation at the top, absolute URL; `context-splitting.md`: the headers that failed only because the links did not resolve locally).
- Growth. 62 drafts waiting. If all promoted, stable cards go from 293 to 355 (+21%). service-server alone has 14 service drafts across contexts, so it would reach about 60 cards and about 113K md. Any manual "add a context" step will keep recurring.

## 6. Recommendation

1. Budget (both formats, enforced in `tools/config.py` and `agent_ready_check.py`).
   - Part `.md` twin: target 50,000 chars, hard 100,000 (afdocs pass and fail lines; Ora says about 100K).
   - Part HTML text: hard 100,000 by `Page.chars()` (lower `PAGE_MAX` from 150,000), target about 70,000, because HTML text is about 1.4 times the `.md`.
   - Rule of thumb: 26 to 30 stable cards per part.
   - `llms.txt` stays at 12,000. Nested per-level `llms.txt` files only if the root passes about 10,000.
   - Whole-level and `llms-full.txt` stay as labelled downloads, exempt, as today.
2. Primary scheme: level, then context, as now. Keep `any` first in the route.
3. Overflow rule: when a (level, context) part is over target, split it by the largest meaningful group, concern first, then topic, and merge groups under about 8 cards into an "other" part. Name every child by its group (`service-server-security`, not `service-server-2`). Make this a planner in `split_levels` rather than a `BuildError` telling a person to add a context. Needs a stated rule on which concern is primary (the first listed), and a lint that the first tag is a concern.
4. Concern and topic stay views. Concern pages exist (19 `concerns/*.md`). Add static topic index pages only for tags with 10 or more cards (9 today), one line per card, not full text. Keep the JavaScript filter on `concerns.html` for people, since agents use `cards-index.json` and the `.md` views.
5. Add a lint for tag vocabulary (synonyms such as `config` and `configuration`) before any topic-based split depends on it.
6. Check item 36 to use the same limit as its own checklist text, and decide whether `concerns.md` (101,213) should become a hub.

## 7. What the evidence does not settle

- Whether any of 50,000, 100,000 or 25,000 tokens matches a real truncation point for the agents that will use this site. afdocs gives a range of "5K characters on some platforms to over 100K on others" and does not name platforms. Ora's "about 25K tokens" is a character-to-token ratio of four, not measured.
- Whether more parts lose cards. The repo's own run covers five parts, 3 runs, one model and the Read tool. No run covers 8 to 10 parts, a fetch tool that summarises, or a "report every card id" verdict.
- Whether a concern split would serve reviewers better than a context split. No source tests rule catalogs; clippy, ESLint and OWASP show practice, not measured outcomes. I found no usability data for any of these sites.
- Mintlify's 52.1% and 44.8% figures come from the vendor, on lookup tasks, not on "check all items" reviews.
- Whether the site/ snapshot matches the working tree: `cards/` shows many modified files in `git status`, and the `concerns.md` size looks stale against item 53. A rebuild is needed before acting on the page numbers.
- Estimates of the number of new parts and `llms.txt` growth assume today's cards and a 1.4 HTML-to-md ratio.
- Large catalogs publishing a size-compliant `llms.txt`: none found; the closest precedent is Mintlify's description of its own generator.

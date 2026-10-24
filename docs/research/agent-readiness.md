# Agent readiness: what five sources check

Research for goodcodereview.com, a static documentation site (built by `tools/build.py` into `site/`, with `llms.txt`, `llms-drafts.txt`, per-level `.md` files and `robots.txt`). The goal is to turn each criterion below into a site change without re-reading the sources. Nothing here was submitted to any scanner. Fetched in October 2026.

Files:

- This file: all five sources, overlap, conflicts, scanner notes, irrelevant items, and the merged checklist.
- [agent-readiness-4.md](agent-readiness-4.md): the full Ora ranker catalog (132 checks) behind source 4, one row per check with layer, points, tier, essentials tier, test and fix.

Source numbers used everywhere:

1. https://is-agentic.com/
2. https://is-agentic.com/methodology
3. https://ora.ai/blog/ax-is-the-new-aeo
4. https://ora.ai/methodology
5. https://www.agentready.org/

## 0. Fetch log and gaps

Pages fetched (WebFetch converts to markdown and a small model summarizes against my prompt, so wording below is a paraphrase and some detail may be lost):

- Sources 1 to 5, then, within the same site and up to two levels: https://is-agentic.com/docs, https://is-agentic.com/llms.txt, https://is-agentic.com/openapi.json, https://is-agentic.com/.well-known/ai-catalog.json, https://is-agentic.com/mcp/server-card, https://ora.ai/llms.txt, https://ora.ai/docs, https://ora.ai/docs/essentials, https://ora.ai/docs/discovery, https://ora.ai/docs/cli, https://ora.ai/docs/api/scores, https://ora.ai/api/checks, https://ora.ai/api/checks?include=essentials, https://ora.ai/api/openapi.json, https://ora.ai/bot, https://ora.ai/blog/is-agentic-with-vercel, https://www.agentready.org/ and its spec at https://github.com/agentready-org/standard/blob/main/spec/spec.md plus the repo page https://github.com/agentready-org/standard.
- Partial or missing:
  - Source 1 (https://is-agentic.com/) and source 2 (https://is-agentic.com/methodology) name no individual checks, weights or score bands. They give only the pool structure (80/20/5) and topic areas. The only per-check data that maps to Is Agentic's Essential, Recommended and Bonus split is the `include=essentials` field of the Ora catalog (see section 4 and the caveat there). The check list on the Is Agentic report pages (`/scan/<host>`) was not fetched because that would need a scanned site; no example report URL is linked from the pages.
  - Source 3 (https://ora.ai/blog/ax-is-the-new-aeo) is a research article. It has no check list.
  - Source 4 (https://ora.ai/methodology) fetched as a summary: four layers, weights, 126-check total, grade bands. The per-check detail came from the catalog endpoint, not from the methodology page.
  - https://ora.ai/api/openapi.json was read for the first 100,000 of 218,326 characters only. The check ids, request body of `/api/scan/checks`, and later schemas were not read.
  - https://ora.ai/api/checks?include=essentials: one row (`ax-native-controls`) was cut at a chunk boundary, so its essentials values are not read.
  - The agentready.org front page lists "AR-READ-10" as absent; the spec says it was retired in 2.0.
  - Not followed (different sites or beyond depth): Mintlify Agent Score, Netlify AXIS, Tavily, the arXiv paper 2609.34951, https://ora.ai/blog/what-agents-actually-reach and https://ora.ai/blog/state-of-agent-readiness-2026.

## 1. Source 1: https://is-agentic.com/

- What it is: a free tool that scores how ready a public website is for AI agents, with evidence and fixes. Submit a public HTTP or HTTPS URL; the report lives at `/scan/<host-or-url-path>`.
- Who runs it: Is Agentic is a Vercel x Ora product (agentready.org calls it "essentials, Vercel x Ora"); the github skill sits under vercel-labs. Every technical scan is run and scored by Ora. The page itself says nothing more about the operator.
- Related pages read: https://is-agentic.com/docs, https://is-agentic.com/llms.txt, https://is-agentic.com/openapi.json, https://is-agentic.com/.well-known/ai-catalog.json, https://is-agentic.com/mcp/server-card.

### Score structure (page states these, no check ids)

| Item | Detail |
|---|---|
| Essential checks | Carry most of the score. Topics: server-rendered content; correct HTTP behavior; clear document structure; recoverable errors; usable controls; identity metadata (canonical URL, declared language, Open Graph tags). Check ids and individual weights are not on the page. |
| Recommended checks | Switch on only when the scan sees an API, OAuth flow, GraphQL endpoint, MCP server, developer portal or commerce surface. Inapplicable ones are excluded, not failed. |
| Bonus | Emerging formats earn limited credit. Absence never lowers a score. |
| Findings | Each has observed evidence and, where available, a recommendation. |
| Observed agent journey | One agent's navigation run and its friction. Supporting evidence, not part of the numeric score. |
| Rescan | Replaces the latest report; the report URL stays stable. |
| Score bands | Not given on the page. The API returns a `score_label` string; its values are not listed. |
| Limits | Private pages, authenticated flows, geography, bot defenses, outages, user state are not observable. Not a security, accessibility, privacy or legal audit. |

### Site-type declaration (a thing the site can add)

- Markup: `<meta name="is-agentic-site-type" content="...">` in `<head>`, exactly one tag, exactly one value.
- Allowed values: `content` (documentation, editorial, reference), `business`, `app`, `store` (commerce).
- Effect: overrides inferred type; selects which checks are shown first. Adds no points and does not change the score.
- Relevance: for goodcodereview.com the value is `content`. Static-site applicable: yes.

### Interfaces Is Agentic itself publishes (they show what it considers good practice)

- Public report API: `GET https://is-agentic.com/api/v1/report?url=<encoded url>` returns the latest completed report; never starts a scan. Errors use RFC 9457 `application/problem+json`; codes 400, 404, 405, 429, 503. Limit: 120 requests per client IP per 60 s, with `RateLimit-Policy`, `RateLimit` and `Retry-After`. Versioned under `/api/v1`; deprecations signalled with RFC 9745 headers; `/api/report` is a deprecated alias.
- CLI: `npx is-agentic <domain>` (and `--json`). Starts a scan if no report exists.
- MCP server: Streamable HTTP at `/mcp`, three read-only tools (`is_agentic_get_report`, `is_agentic_get_methodology`, `is_agentic_get_developer_docs`), no auth. Server card at `/mcp/server-card` and `/.well-known/mcp/server-card.json`; registry manifest `/server.json`. Supported protocol versions listed in the card: 2026-07-28, 2025-11-25, 2025-06-18.
- Discovery: `/.well-known/api-catalog` (RFC 9727), `/.well-known/ai-catalog.json` (specVersion 1.0, one entry pointing at the MCP server card), `/.well-known/agent-skills/index.json` (lists skill file with SHA-256), `/openapi.json`, `/llms.txt`, `/sitemap.xml`, `/pricing.md`.
- Report pages: server-rendered HTML; `Accept: text/markdown` returns compact markdown at the same URL, `Content-Type: text/markdown; charset=utf-8`, `Vary: Accept`; unsupported `Accept` gives 406.
- Skill: `npx skills add vercel-labs/is-agentic`.
- Its own `llms.txt` (https://is-agentic.com/llms.txt) is the example: one-line description, bullet links with descriptions, a "Scan reports" paragraph, usage rules.

## 2. Source 2: https://is-agentic.com/methodology

- What it is: the scoring explainer for Is Agentic. Run by Ora scoring, shown by Is Agentic.
- Pools: Essential 80 points; Recommended 20 points; Emerging signals (Bonus) up to +5. So the maximum score is 100 plus a 5-point bonus ceiling (the page does not say whether the total is capped at 100; the API schema constrains `score` to 0 to 100).
- Partial results earn proportional credit. Not-applicable checks are excluded. Duplicate check ids across several MCP surfaces are averaged.
- Weighting within a tier: even (stated by https://ora.ai/blog/is-agentic-with-vercel as "weighted evenly", unlike the ranker).
- Site-type views: documentation and content, business, app, commerce. A valid `is-agentic-site-type` meta sets the default; otherwise inferred. Switching views changes which checks are highlighted, not the score or stored evidence.
- Outputs: a prioritized implementation prompt, observed agent journeys, share pages, caching, history.
- Caveats: reports are cached and can change when the target, the Ora methodology or time-sensitive evidence changes; automated checks can be partial or wrong.
- Not on the page: check ids, per-category weights beyond 80/20/5, score bands, measurement details, pass conditions, fixes.
- Check data available elsewhere: the JSON schema at https://is-agentic.com/openapi.json defines `PublicScanReport` (`score` 0 to 100 or null, `score_label`, `eligible_checks`, `score_breakdown.essential|recommended` as `{earned, available, passing, total}`, `score_breakdown.bonus` as `{points, positive_signals}`, `issues[]` with `id`, `name`, `tier` of essential, recommended or bonus, `result` of failed or partial, `details`, `recommendation`). Check ids are free-form strings; no list.

## 3. Source 3: https://ora.ai/blog/ax-is-the-new-aeo

- What it is: a research article by Ido Finder, Assaf Elovic, Gad Shalev and Liad Yosef (ora research), tied to arXiv 2609.34951 (https://arxiv.org/abs/2609.34951), dated Oct 8 2026; copyright era labs. It argues agent experience (AX) now matters more than answer-engine optimization (AEO).
- Defines no checks, signals or weights. It points readers to https://ora.ai and https://agentready.org to assess readiness.
- Classification rule: "agent-ready" vs "not agent-ready" by the Ora accessibility score; the ambiguous band 0.50 to 0.65 (a 0 to 1 scale, not the 0 to 100 scale of source 4) was dropped. Each agent-ready business was paired with a not-agent-ready one in the same industry, matched on brand fame, model familiarity and third-party citation frequency.
- Design: 1,056 live business sites; 37,927 agent journeys across four agent setups; 140,000+ page fetches; 31,127 asked facts graded against ground truth from 131 sampled businesses.
- Measured outcomes (agent-ready vs not): clear endorsement 20% vs 11% (1.9x); web search share of the answer 12% vs 25%; own-page share of the answer 78% vs 58%; runs ending in a grounded answer 78% vs 56%; turns per run 5.5 vs 6.8; block rate 2.1x for not-ready sites; cost per grounded answer +64% on average (up to +93%); answers with none of the asked facts 7% when read from the site vs 25% off-site; accuracy 56% at highest own-site share vs 41% at lowest. Training knowledge supplies 7 to 10% of answers; pricing accuracy 60% from the site vs 37% from the web; web searches 2.6x higher on least readable sites.
- Recommended fix (general only): make the site accessible, readable and usable for agents.
- Why it matters for us: it is the evidence that the readiness checks matter. Static-site applicable: the findings, yes; no checks to apply.

## 4. Source 4: https://ora.ai/methodology

- What it is: the methodology of the Ora ranker, the "agent experience score". Run by Ora (ora research, era labs).
- Fetched page content (summary level): four scored layers and a grade scale. The page says 126 checks in total.

### Layers and weights (100 points)

| Layer | Weight | Checks stated | Question |
|---|---|---|---|
| Discovery | 20 | 16 | Can an agent find and recommend you? |
| Access | 30 | 42 | Can it access your data and understand you? |
| Usability | 40 | 62 | Can it use you: operate, authenticate, integrate? |
| Payments | 10 | 6 | Can it pay you? |

Each layer is scored by how many of its checks pass, then combined to 0 to 100. Points within a layer follow each check's own max score (see the catalog). The API enum for layers is `discovery | accessibility | usability | payments`.

### Grade bands

| Grade | Score | Label |
|---|---|---|
| A+ | 95 to 100 | Leading |
| A | 86 to 94 | Agent-Ready |
| B | 70 to 85 | Competitive |
| C | 48 to 69 | Needs Work |
| D | 28 to 47 | At Risk |
| F | 0 to 27 | Unusable |

### Check catalog

132 checks recorded in [agent-readiness-4.md](agent-readiness-4.md): 16 Discovery, 43 Access, 67 Usability, 6 Payments. Each row has id, name, scope, maturity, points, tier, Is Agentic essentials tier, static-site relevance, test and fix. The catalog's own fields: `id`, `name`, `status` (pass, fail, warning, error, pending, na), `score`, `maxScore`, `estScoreGain`, `bonus`, `maturity` (verified or emerging), `tier` (required, recommended, emerging), `specUrl`, `mcpKind`, `mcpUrl`, `details`, `recommendation`, `naReason`, plus `beta` (a beta check runs but cannot change a score).

Applicability rule: checks with a precondition (MCP, REST API, GraphQL, MCP App) read N/A when the surface is absent. Payments: any one protocol satisfies the set, the others read N/A.

### Is Agentic essentials mapping (from `include=essentials`)

Is Agentic's 80/20/5 split is the same check results re-bucketed: "essentials tier" is one of required, recommended, emerging, plus a bonus-only flag and an excluded flag. The two robots.txt policy checks (`robots-ai-policy-quality`, `robots-agent-user-policy`) are excluded from essentials (since catalog 1.19.1). The mapping is in the "Ess" column of the catalog file. It is the nearest published list of what Is Agentic scores, but no page says that the Is Agentic Essential list equals the "R" rows exactly; treat as probable.

### Other things on or around the page

- Agent-facing material the Ora site itself ships, useful as worked examples: https://ora.ai/llms.txt, `/agents.md`, `/skill.md`, `/auth.md`, `/.well-known/agent-skills/index.json`, `/.well-known/mcp.json`, `/.well-known/agent-card.json`, `/.well-known/ard.json` (legacy alias `/.well-known/ai-catalog.json`), MCP at `/api/mcp`, docs MCP at `/api/docs/mcp`, NLWeb `/ask` (v0.55), `/pap/catalog.json`.
- Scanner identity: `OraBot/1.0 (+https://ora.ai/bot)`; Web Bot Auth keys published at `/.well-known/http-message-signatures-directory` but signing not yet live; during a scan it also sends a few homepage requests using GPTBot, ClaudeBot and PerplexityBot user-agent strings, unsigned. No IP list published. Active probes (tier 1) are limited to one round of 7 requests per domain every 6 hours.
- Observed agent journeys (https://journey.ora.ai) are separate from the score.
- Not on the methodology page: per-check pass conditions (derived from catalog descriptions), numeric weights per check (in the catalog `maxScore`).

## 5. Source 5: https://www.agentready.org/

- What it is: AgentReady v2.0 (October 2026), an open standard (MIT) for what a product should implement so AI agents can use it, with stable `AR-*` requirement ids. Written by ora.ai and Vercel; research by the Ora lab; named collaborators: Ora, Vercel, Stripe, Auth0, Mintlify, Tavily by Nebius, Google, Elementor, Netlify. Repo: https://github.com/agentready-org/standard (spec at `spec/spec.md`, data in `data/`, `CHANGELOG.md`). The site takes precedence over the repo where they differ.
- Strength levels: MUST (agents fail without it), SHOULD (measurably affects outcomes or reliability), MAY (emerging conventions). Conformance: every applicable MUST (including MUST NOT) is met; stages are Find, Read, Act in order; Read applies to reachable pages; Act applies only to products agents are expected to act on. Prerequisite for all: the agent can reach the page and find the answer in the returned HTML.
- Weights, pass thresholds and score bands: none published. The page says scanner checks and weights may change independently of the spec.
- Version history: 2.0 (Oct 2026) added AR-ACT-10 (MUST), raised AR-ACT-07 to SHOULD, added AR-FIND-04, AR-READ-11, AR-ACT-08, AR-ACT-09, retired AR-READ-10; 1.0 (Aug 2026) restructured into Find/Read/Act; 1.0.0 (Apr 2026) used retired ids AR-DISC/CONT/CAPA/IDEN/COMM.
- Count: 24 live requirements (FIND 4, READ 10, ACT 10) plus 1 retired id.

### FIND: be reachable and citable

| Id | Level | Requirement | Measure / pass | Fix |
|---|---|---|---|---|
| AR-FIND-01 | MUST | Do not block agents or crawlers from public content, in robots.txt or at the network layer. | `curl -iL -A 'Claude-User/1.0' <page>` ends in 200 (301/308 hops fine) with the answer in the HTML; server logs are the dependable test. A WAF returning 403 or a challenge to agents fails. Scanner data: 88% of ~50,000 sites ship robots.txt, 80% reachable to every major AI crawler, about 1 in 10 block them all. | One wildcard `User-agent: *` policy, not a named-crawler allowlist; disallow only low-value paths (example `/search/`); reference the sitemap. Training crawlers (GPTBot, ClaudeBot) MAY be blocked while staying open to OAI-SearchBot, Claude-SearchBot, ChatGPT-User, Claude-User. Admit verified agents by provider IP ranges or Web Bot Auth signatures; throttle with 429 and `Retry-After`, not challenges. Note: specific groups override `*`; user-initiated fetchers may ignore robots.txt. |
| AR-FIND-02 | SHOULD | Publish citable answers on one canonical, current, first-party docs page. | 82% of answers traced to a fetched page; docs pages were 47% of those. | Make the canonical page the single source. |
| AR-FIND-03 | SHOULD | List pages in `sitemap.xml`, referenced from `robots.txt`. | Fetched directly in 4% of runs. | Publish the sitemap and add a `Sitemap:` line. |
| AR-FIND-04 | MAY | Publish an AI Catalog at `/.well-known/ai-catalog.json` listing agent-facing resources (MCP server card, llms.txt, OpenAPI, A2A card, docs, skills) typed by media type. | Not measured. | Link it with `<link rel="ai-catalog">` in the head and an HTTP `Link` header. |

### READ: put the answer where agents read

| Id | Level | Requirement | Evidence | Fix |
|---|---|---|---|---|
| AR-READ-01 | MUST | The answer is in the initial HTML (SSR or prerender), not injected by a SPA. | JS-hidden answers broke the non-JS client. | Server-render or prerender. |
| AR-READ-02 | MUST | Accurate status codes: 404 or a valid redirect for missing paths; 429 with `Retry-After` for throttling. Never 200 for a missing page; never a challenge page in place of 429. | An SPA returning 200 on every path looked valid to agents. | Fix host/router 404 handling. |
| AR-READ-03 | SHOULD | Homepage is raw HTML with real links to docs, product and pricing. | Reached in 69% of runs, first fetch in 92% of those, next hop docs in 59%. | Add real anchor links on the homepage. |
| AR-READ-04 | SHOULD | Docs pages answer the tasks users bring to agents; setup/quickstart linked from the homepage. | Reached in 83% of runs, about 3.4 pages per run. | Write task-shaped pages. |
| AR-READ-05 | SHOULD | Code snippets are fenced and language-tagged. | 61% of answers with code reused lines verbatim. | Tag every fence. |
| AR-READ-06 | SHOULD | Discovery files (`llms.txt`, `.well-known/*`, `openapi.json`, `AGENTS.md`) are linked from pages agents already visit (footer, `<link rel="alternate">`, resources section). | `.well-known/*` reached in ~23% of runs; 86 to 100% of visits arrived via links. | Add footer/head links to each. |
| AR-READ-07 | SHOULD | Ship an `llms.txt`: a lean, described index of key pages. Shape: H1 site name, blockquote summary, H2 sections of `- [Title](URL): description`, including a link to `openapi.json` where one exists. | About 1 in 3 readers fetched a listed page; 36% drew the final answer from it. | Keep it short and described. |
| AR-READ-08 | SHOULD | JSON-LD on key pages, homepage first; repeat critical facts in visible text. | Agents parse facts from the block; converters may drop script blocks. | Add JSON-LD plus visible text. |
| AR-READ-09 | MAY | Advertise a markdown mirror: `<link rel="alternate" type="text/markdown" href="/docs/quickstart.md">` or an HTTP `Link` header. | Markdown requested in ~65% of fetches, chosen 96% when a format was specified, but task success did not change. | Make HTML work first. |
| AR-READ-11 | SHOULD | Publish pricing as HTML text on a first-party page (plans, free tier, limits), not an image, calculator or sales form. | 60% accurate from first-party pages vs 37% elsewhere. | Add the page. |
| AR-READ-10 | retired | Formerly AGENTS.md / SKILLS.md. Removed in 2.0; id not reused. | n/a | n/a |

### ACT: let agents complete tasks (only for products agents act on)

| Id | Level | Requirement | Notes |
|---|---|---|---|
| AR-ACT-01 | SHOULD | Auth an agent can finish: self-serve keys with documented scopes; OAuth 2.0 with discoverable metadata under `/.well-known` for user-delegated access (RFC 8414, RFC 9728). | OAuth metadata and PKCE pass on about 1% of sites. |
| AR-ACT-02 | SHOULD | Public API with an OpenAPI contract: operation ids, typed responses and errors, `/v1/` versioning, documented rate limits. | `openapi.json` used in 21% of runs where shipped. |
| AR-ACT-03 | SHOULD | MCP server over Streamable HTTP at `/mcp`; docs MCP public; product MCP behind OAuth with `/.well-known/oauth-protected-resource` (RFC 9728) and PKCE; `server.json` in the MCP Registry. | About 3% of sites ship a spec-grade MCP server. |
| AR-ACT-04 | MAY | MCP server card for pre-connection discovery. | SEP-2127 working-group draft; path may change (open question in the spec). |
| AR-ACT-05 | MAY | MCP Apps view as a `ui://` resource. | No evidence cited. |
| AR-ACT-06 | SHOULD | SDKs (npm, PyPI) and a CLI; show install and first call in docs. | |
| AR-ACT-07 | SHOULD | If there is a web UI, register WebMCP tools on `document.modelContext`; feature-detect; only real actions. | W3C Community Group draft; raised from MAY in 2.0. |
| AR-ACT-08 | MAY | Agent payments if the product charges: x402 or MPP for per-call pricing, UCP or ACP for checkout; with Stripe enable Link and accept Shared Payment Tokens; no CAPTCHA in front of verified agents. | Agents got 92.3% of test checkouts right through Link; 18 of 26 agents scored 90% or more. |
| AR-ACT-09 | MAY | Content-heavy sites may serve NLWeb `/ask` (natural-language question in, schema.org-shaped results out) and expose the same `ask` tool over MCP. | |
| AR-ACT-10 | MUST | Expose at least one agent-operable interface: an MCP server (ACT-03) or a CLI (ACT-06). Do not ship an empty surface to satisfy it. | Added in 2.0. MUST applies only where agents should complete tasks. |

### Other facts on the page

- Scanner reach: Ora scanner across about 127,000 sites; average score 43; grade split D or F 59%, C 35%, B or better 6%.
- Tools listed: is-agentic (`npx is-agentic example.com`), ora.ai full ranker with `ax` CLI (`npx ax audit https://example.com`), Mintlify Agent Score (docs, 29 checks, `npx mint score docs.example.com`), Netlify AXIS (runs 20+ coding agents, four scoring dimensions, CI gating; `npx @netlify/axis init`, `npx @netlify/axis run`), Tavily visibility report (https://avr.tavily.com, free, needs a Tavily API key).
- Dataset: `data/traces.csv` (1,033 runs, 25 sites, four models, two harnesses, June to August 2026) and `data/fetchability.csv` (one docs site, 19 configurations, 190 probes).
- Open questions in the spec: the MCP server card path; whether user-initiated fetchers that ignore robots.txt need separate crawl guidance.

## 6. Overlap table

| Criterion | S1/S2 (Is Agentic) | S4 (Ora catalog ids) | S5 (AgentReady) |
|---|---|---|---|
| Content present without JavaScript | "Server-rendered content" (essential) | `content-no-js` | AR-READ-01 |
| Do not block agents | "Correct HTTP behavior" | `bot-detection`, `agent-crawler-reachability`, `robots-ai-policy-quality`, `robots-agent-user-policy` | AR-FIND-01 |
| Correct status codes, recoverable errors | "Correct HTTP behavior", "Recoverable errors" | `agent-friendly-404`, `redirect-hygiene`, `json-error-responses`, `rate-limit-headers` | AR-READ-02 |
| Document structure | "Clear document structure" | `ax-document-structure` | none |
| Usable controls, labels | "Usable controls" | `ax-native-controls`, `ax-accessible-names`, `ax-form-labeling`, `ax-tree-injection-safe` | none |
| Identity metadata | canonical URL, language, Open Graph | `metadata-completeness` (canonical, lang, og:image, og:type), `json-ld`, `org-schema-completeness`, `json-ld-entity-linking`, `schema-type-breadth` | AR-READ-08 (JSON-LD only) |
| llms.txt | bonus-only (essentials mapping) | `llms-txt-exists`, `llms-txt-formatting`, `llms-txt-links-resolve`, `modular-llms-txt` | AR-READ-07 |
| Sitemap | recommended (essentials mapping) | `sitemap`, `sitemap-lastmod` | AR-FIND-03 |
| Markdown mirror / negotiation | bonus (S1 implements `Accept: text/markdown`) | `markdown-url-fallback`, `markdown-link-alternate`, `markdown-frontmatter`, `markdown-negotiation`, `markdown-negotiation-vary`, `agent-ua-markdown` | AR-READ-09 |
| AI catalog / ARD | bonus | `ai-catalog-published`, `ard-catalog`, `ard-entries-valid`, `ard-trust-manifest` | AR-FIND-04 |
| Discovery files linked from pages | n/a | `link-headers-discovery`, `agent-discovery-file`, `mcp-well-known-discovery` | AR-READ-06 |
| Agent instruction files | n/a | `agent-instruction`, `agent-rules-repo` (AGENTS.md) | AR-READ-10 (retired), AR-READ-06 mention |
| Docs and API docs | n/a | `public-api-docs`, `developer-portal`, `agentic-search-specific` | AR-FIND-02, AR-READ-03, AR-READ-04 |
| Code blocks | n/a | `code-fence-validity` | AR-READ-05 |
| Pricing | n/a | `pricing-info`, `pricing-md` | AR-READ-11 |
| OpenAPI | recommended if API | `openapi-spec`, `api-schema-analysis`, `function-calling-compat` | AR-ACT-02 |
| Auth / OAuth metadata | recommended if OAuth | `oauth-support`, `scoped-permissions`, `oauth-protected-resource`, `mcp-oauth-metadata`, `mcp-pkce-s256`, `onboarding-friction` | AR-ACT-01 |
| MCP server | recommended if MCP | `mcp-server` and ~20 `mcp-*` checks | AR-ACT-03, AR-ACT-10 |
| MCP server card | recommended if MCP | `mcp-server-card`, `registry-branding` | AR-ACT-04 |
| MCP Apps | n/a | `mcp-app-registry`, `mcp-apps-ui-quality`, `mcp-view-domain`, `mcp-view-csp` | AR-ACT-05 |
| WebMCP | n/a | `webmcp` | AR-ACT-07 |
| CLI / SDKs | recommended if developer portal | `cli-tool`, `rest-sdk-packages`, `npm-sdk-package` | AR-ACT-06 |
| NLWeb | n/a | `nlweb-ask`, `nlweb-streaming`, `nlweb-schema-feeds` | AR-ACT-09 |
| Agent payments | recommended if commerce | `x402-support`, `mpp-support`, `ucp-support`, `acp-support`, `acp-delegate-payment`, `ap2-support` | AR-ACT-08 |
| Web Bot Auth | n/a | `web-bot-auth-directory` | AR-FIND-01 (mentions signatures) |
| API catalog (RFC 9727) | listed on S1's own site | `api-catalog-rfc9727` | none |
| A2A agent card | n/a | `a2a-agent-card` | listed as an AI Catalog entry type only |
| Trust pages | n/a | `trust-anchors` (/about, /contact, /privacy) | none |
| Noindex | n/a | `noindex-directives` | none |
| Page size | n/a | `page-token-budget` | none |
| Auth-gated content | not observable | `docs-auth-gate` | AR-READ-01 prerequisite |
| Brand/search presence | n/a | `brand-search-accuracy`, `agentic-search-usecase`, `wikipedia-presence` | AR-FIND-02 (indirect) |

## 7. Conflicts and disagreements

- llms.txt. S5 rates it SHOULD (AR-READ-07) and notes only 36% of readers drew an answer from it. S4's catalog lists `llms-txt-exists` as tier "required" in the ranker, but the essentials mapping makes llms.txt checks emerging and bonus-only, so S1/S2 never penalize a missing one. Both agree on shape (markdown index with descriptions). S4 adds a 30K-char ceiling, at least 100 chars of text, all links must resolve, and a modular per-section variant; S5 asks for a link to `openapi.json`.
- robots.txt for AI crawlers. S5: one wildcard rule, no named-crawler allowlist; blocking training crawlers (GPTBot, ClaudeBot) is allowed while search and user fetchers stay open. S4: `robots-ai-policy-quality` wants AI search crawlers allowed, `robots-agent-user-policy` wants ChatGPT-User, Claude-User, Perplexity-User allowed, and both are scored in the ranker but excluded from Is Agentic's essentials. Our site: no named allowlist in either; a simple `User-agent: *` with a `Sitemap:` line satisfies both.
- Structured data. S5 has JSON-LD as one SHOULD on key pages and warns converters may drop script blocks, so repeat facts in text. S4 scores JSON-LD at 4 points plus Organization (contactPoint, PostalAddress), `sameAs` and extra schema types: much more than S5 asks. S1/S2 name only canonical, language and Open Graph for identity metadata.
- Markdown negotiation. S5: MAY, and format did not change task success. S4: six markdown checks (negotiation with `Vary: Accept`, `.md` twins, frontmatter, bot-UA serving, alternate link). S1 does `Accept: text/markdown` with `Vary: Accept` and 406 on its own pages. A static host cannot negotiate content; `.md` twins plus `rel="alternate"` are the static-friendly route.
- Content signals. None of the five sources defines or scores a `Content-Signal` robots directive or similar. Not covered.
- MCP. S5: MCP SHOULD (AR-ACT-03) and MUST-have-MCP-or-CLI (AR-ACT-10) only for products agents act on. S4: `mcp-server` 6 points, tier required, but essentials-recommended. S1: MCP checks apply only if the scan finds an MCP server. Net: not applicable to a docs-only site, but S5's wording of ACT-10 could be read as a MUST for any site; the spec limits Act to products agents are expected to act on.
- NLWeb. S5: MAY (AR-ACT-09) for content-heavy sites. S4: three emerging checks (`nlweb-ask`, `nlweb-streaming`, `nlweb-schema-feeds` needing a `schemamap` directive in robots.txt). S5 does not mention the schemamap directive.
- Agent cards and catalogs. S5's AI Catalog is `/.well-known/ai-catalog.json` linked by `rel="ai-catalog"`. S4 lists both `ai-catalog-published` (specVersion 1.0) and ARD at `/.well-known/ard.json` (ARD v0.91) and says ard.json is the current Ora manifest with ai-catalog.json the legacy alias; the same check family treats them as separate. MCP server card path: S5 says the path is unsettled (SEP-2127); S4 accepts `/server-card` or an ai-catalog entry; S1 serves both `/mcp/server-card` and `/.well-known/mcp/server-card.json`. A2A card: only S4 scores it (`/.well-known/agent-card.json`).
- Sitemaps. S5: reference from robots.txt, SHOULD. S4: file at `/sitemap.xml`, 2 points, plus `lastmod` freshness; the sitemap check is tier required but essentials-recommended.
- AGENTS.md. S5 retired its AGENTS.md/SKILLS.md requirement (READ-10) in 2.0, yet still lists AGENTS.md among discovery files to link (READ-06). S4 still scores an AGENTS.md-style rules repo (`agent-rules-repo`, emerging) and a required-tier `agent-instruction` (when to use you).
- schema.org types. S4 wants Organization with contactPoint and PostalAddress, `sameAs`, extra types and an `Offer` for pricing; S5 names no type. Neither source names a type for documentation (for example `TechArticle`, `WebSite`, `Article`).
- Scoring scales. S1/S2: 80 essential, 20 recommended, up to +5 bonus, even weights inside a tier. S4: 20/30/40/10 layers with per-check points of 1 to 7, grades A+ to F. S3: a 0 to 1 scale with an excluded 0.50 to 0.65 band. S5: no weights. A site's score will differ between S1 and S4.
- Check counts. S4 page: 126 checks. S3 and S5: "100+". Catalog read: 132 rows. No source reconciles these.
- Bot verification. S5 asks sites to admit verified agents by Web Bot Auth signatures or IP ranges. S4's own scanner does not yet sign requests, publishes no IP list, and sends some requests with GPTBot, ClaudeBot and PerplexityBot user agents unsigned. A site that blocks unverified agents would block the scanner.
- Required vs recommended meaning. Several S4 checks marked "required" in the ranker (for example `llms-txt-exists`, `webmcp`, payment protocols) are bonus-only in Is Agentic's essentials mapping.
- Soft-404. S5 asks only for a real 404 or redirect; S4's `agent-friendly-404` additionally wants a markdown error body of at least 20 chars.

## 8. Scanner and tool notes

| Tool | Input | Cost / access | Unpublished or localhost? |
|---|---|---|---|
| Is Agentic web (S1) | public HTTP/HTTPS URL at https://is-agentic.com/ | Free, no key; bulk scanning and rate-limit bypass disallowed | No. Public URLs only; the docs say it cannot see private pages. Report API only returns completed reports and never starts a scan. |
| `npx is-agentic <domain>` | domain | Free; returns stored report or starts a scan and waits | Public domains only (no tunnel option documented). |
| Is Agentic report API / MCP | `GET /api/v1/report?url=` or MCP tool `is_agentic_get_report` | Free, 120 requests/min/IP | Read-only; needs an existing public report. |
| Ora scan (S4) `POST /api/scan` | `url` (domain, MCP URL or MCP App URL); options `force`, `ephemeral`, `maxAgeSeconds`, `siteType`, `activeProbes`; query `include=essentials` | Reads keyless; 10 requests/min/IP, 30 scans per 24 h per IP, 6 forced; scan API key lifts limits | `ephemeral` is "intended for a local site exposed through a tunnel"; results are not stored on the leaderboard and expire after a few days. Public tunnel hosts (trycloudflare.com, ngrok) are treated as ephemeral automatically. Whether a bare `localhost` URL works in `/api/scan` was not stated. |
| `npx ax audit <url>` | URL or `localhost:3000` with `--tunnel-cmd 'ngrok http 3000 --log stdout'` | No account; `--min-score <n>` for CI; `--json`; `--force`; `--api-key` | Yes, via a tunnel you run. This is the only documented path for a not-yet-published site. A tunnel makes the site public to the scanner for the scan duration, and still contacts Ora's servers. |
| `POST /api/scan/checks` | selected check ids | Re-verifies a fix; no aggregate score | Same as scan. |
| `GET /api/checks` | none | Static catalog, 60 requests/min/IP | n/a. Free way to read every check without scanning. |
| Ora agent journey | intents; custom tasks need a partner key | Separate from the score | Rejects localhost (per the OpenAPI excerpt). |
| Mintlify Agent Score, Netlify AXIS, Tavily (S5) | domain / project | See S5; not read | Not checked. AXIS is built for CI, which suggests local runs, but this was not confirmed. |

For this project: do not submit goodcodereview.com anywhere until it is live. The pre-launch route that stays inside the sources is to read the catalog (`agent-readiness-4.md`) and test locally with `curl` against `site/` served on localhost, using the checks listed in S5's verification note (`curl -iL -A 'Claude-User/1.0' <page>`). If a scan is wanted before launch, `ax audit` with a tunnel is the one documented option and needs the owner's decision.

## 9. Items a source says are irrelevant or not applicable to a docs-only static site

Marked N in the catalog file. In summary:

- All Payments-layer checks and AR-ACT-08 (nothing is sold). Ora treats them as N/A when the site has no commerce.
- API and auth surface: OpenAPI, OAuth, scoped permissions, RFC 9728 metadata, `auth.md` family, `agent_auth` metadata, PAP family, rate-limit headers, idempotency keys, REST and GraphQL design checks, sandbox, batch endpoints, async jobs, pagination, JSON error responses for an API, SDKs, CLI, developer portal, API catalog (RFC 9727). S1 and S5 say these only apply when an API exists; the site has none.
- MCP family (about 20 checks), MCP Apps, MCP registry listings, server card, `mcp-well-known-discovery`, AR-ACT-03, 04, 05, 10. Not applicable without an MCP server. AR-ACT-10 is MUST only where agents act.
- WebMCP (AR-ACT-07, `webmcp`): applies to sites with a web UI offering actions; a read-only docs site has none, so registering tools would invent actions (the spec says to expose only real actions).
- NLWeb `/ask` and streaming, `nlweb-schema-feeds`: need a server; content-heavy sites "may" add it.
- Server-side content negotiation (`markdown-negotiation-vary`, `agent-ua-markdown`, `agent-mode-view`): need request-time logic a static host does not give. Static alternatives exist (`.md` twins).
- Pricing (`pricing-info`, `pricing-md`, AR-READ-11): the site is free; at most a one-line "free, open content" statement.
- Off-site presence: Wikipedia/Wikidata, ChatGPT app listing, skills.sh listing, MCP registry, category share of voice, ARD trust manifest, A2A card. Not site changes.
- HTTP response headers (`Link` headers, `Vary`) depend on the host; GitHub Pages-style hosting may not allow custom headers. Check `docs/deploy.md` before planning.

## Agent-readiness checklist

One line per distinct criterion after merging duplicates. Tags: sources that require or score it (1 to 5; 1 and 2 are tagged where the Is Agentic pages name the topic, or where the Ora essentials mapping puts the check in their buckets), then static-site applicable. Detail for the Ora ids is in agent-readiness-4.md; for AR ids in section 5.

1. Answer content present in raw HTML without JavaScript, with a single H1 and at least 500 chars on the homepage (`content-no-js`, AR-READ-01). Sources: 1, 2, 4, 5. Static-site applicable: yes
2. Do not block agents or search crawlers in robots.txt or at the network layer; test with `curl -A 'Claude-User/1.0'` (`bot-detection`, `agent-crawler-reachability`, AR-FIND-01). Sources: 1, 2, 4, 5. Static-site applicable: yes
3. robots.txt uses one wildcard policy, no named-crawler allowlist, allows AI search crawlers and user-fetchers (ChatGPT-User, Claude-User, Perplexity-User), may block training crawlers (`robots-ai-policy-quality`, `robots-agent-user-policy`, AR-FIND-01). Sources: 4, 5. Static-site applicable: yes
4. robots.txt references the sitemap (AR-FIND-03). Sources: 5. Static-site applicable: yes
5. `/sitemap.xml` exists, is valid and complete (`sitemap`, AR-FIND-03). Sources: 2, 4, 5. Static-site applicable: yes
6. Sitemap `lastmod` dates present and recent (`sitemap-lastmod`). Sources: 4. Static-site applicable: yes
7. Missing paths return 404 or a valid redirect, never 200 for a missing page (AR-READ-02, Is Agentic "correct HTTP behavior"). Sources: 1, 2, 5. Static-site applicable: yes
8. Redirects are real HTTP 301/302/308, not meta-refresh or JS stubs (`redirect-hygiene`). Sources: 1, 2, 4. Static-site applicable: yes
9. 404 page is useful to agents, with a markdown or plain-text error body of at least 20 chars (`agent-friendly-404`; Is Agentic "recoverable errors"). Sources: 1, 2, 4. Static-site applicable: yes (depends on host 404 file)
10. Throttling uses 429 with `Retry-After`, never a challenge page (AR-READ-02, AR-FIND-01, `rate-limit-headers`). Sources: 4, 5. Static-site applicable: no (host or CDN setting)
11. Verified agents admitted by IP range or Web Bot Auth, no CAPTCHA in front of them (AR-FIND-01, `web-bot-auth-directory`). Sources: 4, 5. Static-site applicable: no
12. Homepage is raw HTML with real links to docs, product and pricing (AR-READ-03). Sources: 5. Static-site applicable: yes
13. Docs pages answer the tasks users bring to agents; setup or quickstart linked from the homepage (AR-READ-04, AR-FIND-02, `public-api-docs`). Sources: 4, 5. Static-site applicable: yes
14. One canonical, current first-party page per answer (AR-FIND-02). Sources: 5. Static-site applicable: yes
15. Code blocks are fenced, language-tagged and balanced (AR-READ-05, `code-fence-validity`). Sources: 4, 5. Static-site applicable: yes
16. `/llms.txt` exists, at least 100 chars, markdown H1 plus blockquote summary plus H2 link lists with descriptions, under 30K chars (`llms-txt-exists`, `llms-txt-formatting`, AR-READ-07). Sources: 4, 5. Static-site applicable: yes
17. Every link in `llms.txt` resolves to real content (`llms-txt-links-resolve`). Sources: 4. Static-site applicable: yes
18. Modular `llms.txt`: per-section indexes linked from the root (`modular-llms-txt`). Sources: 4. Static-site applicable: yes
19. `llms.txt` includes agent instructions on when to use the site (`agent-instruction`). Sources: 4. Static-site applicable: yes
20. Discovery files (`llms.txt`, `.well-known/*`, AGENTS.md, markdown mirrors) linked from pages agents visit: footer, head `<link rel="alternate">` (AR-READ-06). Sources: 5. Static-site applicable: yes
21. HTTP `Link` headers for sitemap, markdown and docs (`link-headers-discovery`, AR-FIND-04, AR-READ-09). Sources: 4, 5. Static-site applicable: no (host headers)
22. Markdown twins for pages (`/index.md` and per-page `.md`), advertised with `<link rel="alternate" type="text/markdown">` (`markdown-url-fallback`, `markdown-link-alternate`, AR-READ-09). Sources: 4, 5. Static-site applicable: yes
23. Served markdown starts with frontmatter: title plus description, canonical or last-updated (`markdown-frontmatter`). Sources: 4. Static-site applicable: yes
24. Server-side markdown negotiation: `Accept: text/markdown` with `Vary: Accept`; markdown for bot user agents; `?mode=agent` view (`markdown-negotiation`, `markdown-negotiation-vary`, `agent-ua-markdown`, `agent-mode-view`). Sources: 4 (S1 does it itself). Static-site applicable: no
25. JSON-LD on the homepage and key pages with name, description, url and type; critical facts repeated in visible text (`json-ld`, AR-READ-08). Sources: 4, 5. Static-site applicable: yes
26. Organization (or equivalent) JSON-LD with contactPoint and PostalAddress (`org-schema-completeness`). Sources: 4. Static-site applicable: yes (the postal address may not fit a project)
27. `sameAs` links to official profiles in JSON-LD (`json-ld-entity-linking`). Sources: 4. Static-site applicable: yes
28. Additional schema.org types that match visible content (`schema-type-breadth`). Sources: 4. Static-site applicable: yes
29. Homepage metadata: canonical URL, declared `lang`, `og:image`, `og:type` and the other Open Graph tags (`metadata-completeness`; Is Agentic "identity metadata"). Sources: 1, 2, 4. Static-site applicable: yes
30. Semantic document structure: landmarks, `main`, `nav`, sequential heading order (`ax-document-structure`; Is Agentic "clear document structure"). Sources: 1, 2, 4. Static-site applicable: yes
31. Native interactive controls, accessible names and labelled form fields (`ax-native-controls`, `ax-accessible-names`, `ax-form-labeling`; Is Agentic "usable controls"). Sources: 1, 2, 4. Static-site applicable: yes
32. No hidden instructions in the accessibility tree (`ax-tree-injection-safe`). Sources: 4. Static-site applicable: yes
33. No `noindex` meta tag or `X-Robots-Tag` on the homepage (`noindex-directives`). Sources: 4. Static-site applicable: yes
34. Trust pages `/about`, `/contact`, `/privacy`, at least 500 chars each (`trust-anchors`). Sources: 4. Static-site applicable: yes
35. Content publicly readable, no login wall (`docs-auth-gate`). Sources: 1, 4, 5. Static-site applicable: yes
36. Pages under about 100K chars of extracted text (`page-token-budget`). Sources: 4. Static-site applicable: yes
37. Brand-name search lands on the domain: clear titles and headings (`brand-search-accuracy`, `agentic-search-specific`). Sources: 4. Static-site applicable: yes (titles); the ranking itself is off-site
38. AGENTS.md or rules file in a public repo, linked from entry pages (`agent-rules-repo`; S5 retired READ-10 but still lists it in READ-06). Sources: 4, 5. Static-site applicable: yes
39. Agent Skills index at `/.well-known/agent-skills/index.json` with sha256 digests (`agent-discovery-file`, `agent-skills-index-v2`). Sources: 4. Static-site applicable: yes (the repo ships a skill)
40. AI Catalog at `/.well-known/ai-catalog.json` linked by `rel="ai-catalog"` and a Link header; ARD catalog `/.well-known/ard.json` (`ai-catalog-published`, `ard-catalog`, `ard-entries-valid`, AR-FIND-04). Sources: 4, 5. Static-site applicable: yes (the file; headers no)
41. ARD trust manifest on catalog entries (`ard-trust-manifest`). Sources: 4. Static-site applicable: no
42. `site-type` declaration `<meta name="is-agentic-site-type" content="content">`. Sources: 1, 2. Static-site applicable: yes
43. Plugin manifest (`plugin.json`) in a public repo (`agent-plugins-repo`). Sources: 4. Static-site applicable: yes (the repo has `.claude-plugin/`)
44. Pricing or "free" statement as HTML text, `/pricing.md` (AR-READ-11, `pricing-info`, `pricing-md`). Sources: 4, 5. Static-site applicable: no (free content; one line at most)
45. Public API with OpenAPI spec, typed errors, versioning, pagination, idempotency, async jobs, batch, sandbox, SDKs, CLI, developer portal (AR-ACT-02, AR-ACT-06, about 25 Ora checks). Sources: 1, 2, 4, 5. Static-site applicable: no
46. OAuth 2.0 with RFC 8414/9728 metadata, scoped permissions, PKCE, `auth.md`, agent-auth metadata, WWW-Authenticate hint, self-serve keys (AR-ACT-01, about 12 Ora checks). Sources: 1, 2, 4, 5. Static-site applicable: no
47. RFC 9727 API catalog at `/.well-known/api-catalog` (`api-catalog-rfc9727`). Sources: 4. Static-site applicable: no
48. MCP server over Streamable HTTP, with tool descriptions, schemas, annotations, error handling, identity, docs MCP, server card, registry listing (AR-ACT-03, AR-ACT-04, AR-ACT-10, about 20 Ora checks). Sources: 1, 2, 4, 5. Static-site applicable: no
49. MCP Apps views with CSP and public reachability (AR-ACT-05, `mcp-app-registry` family, A2UI). Sources: 4, 5. Static-site applicable: no
50. WebMCP tools registered on `document.modelContext` (AR-ACT-07, `webmcp`). Sources: 4, 5. Static-site applicable: no (no actions to expose)
51. NLWeb `/ask` endpoint, streaming, `schemamap` in robots.txt (AR-ACT-09, `nlweb-*`). Sources: 4, 5. Static-site applicable: no
52. A2A agent card at `/.well-known/agent-card.json` (`a2a-agent-card`). Sources: 4. Static-site applicable: no
53. PAP discovery family (`pap-*`, six checks). Sources: 4. Static-site applicable: no
54. Agent payments: x402, MPP, UCP, ACP, AP2 (AR-ACT-08, six Ora checks). Sources: 1, 2, 4, 5. Static-site applicable: no
55. Off-site presence: Wikipedia/Wikidata, ChatGPT app directory, skills.sh, category share of voice (`wikipedia-presence`, `chatgpt-app-listed`, `skills-sh-*`, `agentic-search-usecase`). Sources: 4. Static-site applicable: no (not a site change)

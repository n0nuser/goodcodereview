# Agent readiness, source 4 detail: the Ora ranker check catalog

Part of [agent-readiness.md](agent-readiness.md). This file holds the full per-check table behind https://ora.ai/methodology.

## Where the data came from

- https://ora.ai/methodology is a summary page. It lists layers, weights and grades but no checks (see the main file).
- The check list below was read from the catalog endpoint https://ora.ai/api/checks (contract version 1.36.0, described at https://ora.ai/docs/api/scores as the complete catalog, CDN-cached 1 hour, CORS open, 60 requests per minute per IP). It carries each check's description and fix. It does not carry separate "how measured" or "pass condition" fields, so the "What it tests" cell serves as the pass condition.
- Essentials tier, bonus-only and excluded flags came from https://ora.ai/api/checks?include=essentials (fetched in two chunks; one entry, `ax-native-controls`, was cut at the chunk boundary, so its essentials values are not read and are marked "not read").
- The catalog page at https://ora.ai/docs/api/scores does not show the schema; https://ora.ai/api/openapi.json gives the check fields (main file, section 4).

## How to read the columns

- Layer: D = Discovery (20 pts of the 100), A = Access (30; API id `accessibility`), U = Usability (40), P = Payments (10).
- Applies: `all` = any scan target, `domain` = a website scan, `mcp` / `mcp-app` / `api` / `api (REST)` / `api (GraphQL)` = only when that surface is found (otherwise N/A, not a failure).
- Mat: V = verified, E = emerging.
- Pts: the check's `maxScore`. Suffix B = bonus in the ranker (upside only), D = draft or beta (cannot change a score), beta marker as listed.
- Tier: the ranker `tier` field (required, recommended, emerging).
- Ess: the Is Agentic "essentials" mapping from `include=essentials`. R = required (counts in the 80-point Essential pool), Rc = recommended (20-point pool), E = emerging; `+b` = bonus-only (adds up to 5 pts, never subtracts); `x` = excluded from essentials. This is the nearest thing to the is-agentic Essential/Recommended/Bonus split that is published (see main file for the caveat).
- "Test and fix" is paraphrased from the catalog description and recommendation.

Static-site relevance (S) is tagged on each row: Y = relevant to a docs-only static site, N = needs a server, API, MCP, auth or payments the site does not have, ? = partly or optional.

## Discovery layer (20 pts)

| id | name | Applies | Mat | Pts | Tier | Ess | S | Test and fix |
|---|---|---|---|---|---|---|---|---|
| ard-catalog | ARD discovery | all | V | 1 | req | E+b | ? | Catalog at `/.well-known/ard.json` or a `rel="ard"` link. Fix: publish an ARD v0.91 catalog with entries for your resources. |
| ai-catalog-published | AI Catalog discovery | all | V | 1 B | rec | E+b | ? | Valid catalog at `/.well-known/ai-catalog.json` with specVersion 1.0. Fix: serve that file. |
| ard-entries-valid | ARD entry validity | all | V | 2 B | rec | E+b | ? | Each entry has a `urn:air` id, name, media type and one of url/data. Fix: complete every entry. |
| ard-trust-manifest | ARD trust manifest | all | V | 2 B | rec | E+b | N | Entries carry trust signals (identity, attestations, signatures). Fix: add a trustManifest. |
| agentic-search-usecase | Category share of voice | domain | V, beta | 6 | rec | E+b | ? | Whether AI answers surface you for your problem category. Fix: publish use-case content. Off-site measurement. |
| agentic-search-specific | Developer resource discoverability | domain | V | 3 | rec | Rc | ? | Dev resources (API docs, OpenAPI, MCP, auth, SDK docs) appear in name searches. Fix: predictable URLs, llms.txt links, clear titles. |
| brand-search-accuracy | Brand name discoverability | domain | V | 3 | req | Rc | Y | Your domain ranks for brand + main product searches. Fix: clarify titles and headings. |
| wikipedia-presence | Wikipedia/Wikidata entity | domain | V | 4 B | rec | Rc+b | N | Article and Wikidata entry linking your domain. Fix: earn press, then create cited entries. |
| robots-ai-policy-quality | robots.txt AI crawler policy | domain | V | 2 | req | Rc x | Y | AI search crawlers may read public pages. Fix: allow them; keep private paths blocked. |
| mcp-registry-listed | Listed in MCP registries | all | V | 1 | rec | Rc+b | N | Entry on Smithery or mcp.so verified to your domain. Fix: register and link back. |
| npm-sdk-package | NPM/PyPI SDK package | domain | V | 1 | rec | Rc+b | N | Official SDK published with repository/homepage fields. Fix: publish SDK; set both fields. |
| agent-rules-repo | Agent platform configs | domain | E | 1 | emg | E+b | Y | Public AGENTS.md or similar rules file, linked from entry pages. Fix: add and link it. |
| agent-plugins-repo | Agent Plugins manifest | domain | E | 1 B D | emg | E+b | ? | `plugin.json` in a public repo. Fix: add a plugin.json manifest. |
| registry-branding | Registry branding | all | E | 2 | emg | E+b | N | Server card has name, icon and description. Fix: complete all three. |
| chatgpt-app-listed | ChatGPT app listed | all | V | 2 B | rec | Rc+b | N | Listed in the ChatGPT apps directory. Fix: submit the app. |
| noindex-directives | Homepage not hidden from search | domain | V | 1 | rec | Rc | Y | No noindex meta tag or `X-Robots-Tag` on the homepage. Fix: remove the noindex directive. |

## Access layer (30 pts)

| id | name | Applies | Mat | Pts | Tier | Ess | S | Test and fix |
|---|---|---|---|---|---|---|---|---|
| sitemap | Sitemap exists | domain | V | 2 | req | Rc | Y | Valid XML sitemap at `/sitemap.xml`. Fix: publish a complete sitemap. |
| content-no-js | Content without JavaScript | domain | V | 3 | req | R | Y | Homepage has at least 500 chars of raw-HTML content, one H1, sequential headings. Fix: server-render content. |
| bot-detection | Not blocked by bot detection | domain | V | 2 | req | R | Y | Agent user agents are not blocked by a WAF. Fix: allow verified bots. |
| agent-discovery-file | Agent discovery file | domain | V | 2 | req | E+b | ? | Agent Skills index at `/.well-known/agent-skills/index.json`. Fix: publish it with name and description per skill. |
| agent-skills-index-v2 | Agent Skills index v0.2.0 | domain | E | 2 B | emg | E+b | ? | Schema v0.2.0, typed entries, verified digest. Fix: upgrade the index and add sha256 digests. |
| a2a-agent-card | A2A agent card | domain | V | 2 B | rec | Rc+b | N | Card at `/.well-known/agent-card.json`. Fix: publish capabilities and contact info. |
| skills-sh-listed | Listed on skills.sh | all | E | 1 | emg | E+b | ? | Skills published on skills.sh. Fix: add SKILL.md and register it. |
| pricing-md | pricing.md exists | domain | E | 2 | emg | E+b | N | `/pricing.md` with plain-markdown pricing. Fix: create it. (No pricing on our site.) |
| nlweb-schema-feeds | NLWeb Schema Feeds | domain | E | 1 | emg | E+b | N | `schemamap` directive in robots.txt. Fix: add it and a Schema Map XML. |
| mcp-well-known-discovery | MCP well-known discovery | domain | V | 2 B | rec | E+b | N | MCP server announced via well-known or llms.txt. Fix: list servers in ai-catalog.json or llms.txt. |
| agent-mode-view | Agent mode view | domain | E | 2 B | emg | E+b | N | `?mode=agent` returns a structured machine view. Fix: add it. Needs server logic. |
| link-headers-discovery | HTTP Link headers | domain | V | 1 B | req | Rc+b | ? | Link headers for sitemap, markdown, API docs. Fix: add RFC 8288 Link headers. Needs host header control. |
| markdown-url-fallback | Markdown URL fallback | domain | E | 2 B | emg | E+b | Y | `/index.md` served; `.md` twins for content pages. Fix: add a markdown homepage and twins. |
| modular-llms-txt | Modular llms.txt | domain | E | 1 B | emg | E+b | Y | Per-section llms.txt linked from root. Fix: add section indexes. |
| sitemap-lastmod | Sitemap freshness | domain | V | 1 B | rec | Rc+b | Y | `lastmod` dates parse; newest is recent. Fix: add and maintain lastmod. |
| robots-agent-user-policy | robots.txt agent-user policy | domain | V | 2 | req | Rc x | Y | Homepage allowed for ChatGPT-User, Claude-User, Perplexity-User. Fix: remove restrictions; keep private paths blocked. |
| llms-txt-exists | llms.txt exists | domain | V | 1 | req | E+b | Y | `/llms.txt` with at least 100 chars of real text. Fix: write and serve it as raw text. |
| llms-txt-formatting | llms.txt formatting | domain | V | 2 | rec | E+b | Y | Markdown heading, links, under 30K chars. Fix: format as a navigation index. |
| json-ld | JSON-LD structured data | domain | V | 4 | req | Rc | Y | Homepage JSON-LD completeness (name, description, url, type fields). Fix: add identity-type markup. |
| pricing-info | Pricing info accessible | domain | V | 3 | req | Rc | N | Pricing on a page or as schema.org Offer. Fix: add /pricing or Offer data. (Free content site: likely N/A or a "free" statement.) |
| public-api-docs | Public API docs linked | domain | V | 3 | req | Rc | N | Owned API docs linked from homepage. Fix: publish docs at /docs, /api or /developers. |
| agent-instruction | Agent instruction / when-to-use | domain | V | 3 | req | Rc | Y | Specific guidance on when to use you. Fix: add it to llms.txt or an agent file. |
| skills-sh-quality | Skills.sh skill quality | all | E | 2 | emg | E+b | ? | Multiple skills with descriptive names. Fix: expand skill repos. |
| json-ld-entity-linking | sameAs linking | domain | V | 2 | rec | Rc+b | Y | `sameAs` links to official profiles. Fix: add them to JSON-LD. |
| metadata-completeness | Metadata completeness | domain | V | 2 | req | Rc | Y | canonical, lang, og:image, og:type on homepage. Fix: add all four. |
| org-schema-completeness | Organization schema | domain | V | 2 | rec | Rc | Y | Organization JSON-LD with contactPoint and PostalAddress. Fix: add both. |
| schema-type-breadth | Schema type breadth | domain | V | 2 | rec | Rc+b | Y | Extra schema.org types matching visible content. Fix: add types that match the page. |
| trust-anchors | Trust anchor pages | domain | V | 2 | req | Rc | Y | `/about`, `/contact`, `/privacy` with at least 500 chars each. Fix: publish real pages. |
| llms-txt-links-resolve | llms.txt links resolve | domain | V | 2 | rec | E+b | Y | Every llms.txt link returns real content. Fix: fix or remove dead links. |
| markdown-link-alternate | Markdown alternate link | domain | E | 1 B | emg | E+b | Y | `rel=alternate` to markdown that really serves markdown. Fix: add the link and verify the target. |
| markdown-frontmatter | Markdown frontmatter | domain | E | 1 | emg | E+b | Y | Served markdown opens with title plus description/canonical/last-updated. Fix: add frontmatter. |
| redirect-hygiene | Redirect hygiene | domain | V | 1 | rec | R | Y | Real HTTP redirects, no meta/JS stubs. Fix: replace with 301/302. |
| page-token-budget | Page token budget | domain | V | 1 | rec | Rc | Y | Extracted text under about 100K chars per page. Fix: split large pages. |
| code-fence-validity | Code fence validity | domain | E | 1 | emg | Rc | Y | Fenced code blocks are balanced. Fix: close every fence. |
| docs-auth-gate | Content behind auth | domain | V | 2 | rec | R | Y | Sampled content pages are publicly readable. Fix: remove login walls; publish summaries. |
| openapi-spec | OpenAPI spec published | domain | V | 7 | req | R | N | Spec at `/openapi.json` or `/api/openapi.yaml`. Fix: publish it. |
| developer-portal | Developer portal | domain | V | 6 | rec | Rc | N | Self-serve signup, keys, docs, sandbox. Fix: build /developers. |
| api-catalog-rfc9727 | API catalog | domain | V | 2 B | req | Rc | N | RFC 9727 linkset at `/.well-known/api-catalog`. Fix: publish it. |
| markdown-negotiation | Markdown agent docs | domain | E | 1 | emg | E+b | ? | Markdown via `Accept` negotiation or a static .md file. Fix: serve one of them. |
| markdown-negotiation-vary | Markdown negotiation on homepage | domain | V | 1 B | rec | R | N | Homepage returns markdown for `Accept: text/markdown` with `Vary: Accept`. Fix: enable it and verify with curl. Needs server logic; a static host cannot negotiate. |
| agent-ua-markdown | Bot-UA markdown serving | domain | E | 1 B | emg | E+b | N | AI bots receive markdown. Fix: optionally serve markdown to bot user agents. Needs server logic. |
| agent-friendly-404 | Agent-friendly 404s | domain | V | 2 | rec | R | ? | Real 404/410 plus a Markdown error body of at least 20 chars. Fix: add the markdown body. Depends on host 404 handling. |
| agent-crawler-reachability | Agent crawler reachability | domain | V | 2 | rec | R | Y | Homepage reachable by user-facing agent crawlers. Fix: allow them through WAF and robots. |

## Usability layer (40 pts)

| id | name | Applies | Mat | Pts | Tier | Ess | S | Test and fix |
|---|---|---|---|---|---|---|---|---|
| mcp-tool-descriptions | MCP tool descriptions | mcp | V | 3 B | rec | Rc | N | Each tool has a description of at least 20 chars. Fix: write detailed descriptions. |
| mcp-param-schemas | MCP parameter schemas | mcp | V | 2 B | rec | Rc | N | Typed `inputSchema` with `required` arrays. Fix: define schemas. |
| mcp-server-identity | MCP server identity | mcp | V | 1 B | rec | R | N | Name, version, instructions in `initialize`. Fix: set them. |
| mcp-tool-listing | MCP tool listing | mcp | V | 3 B | rec | Rc | N | `tools/list` returns breadth (product) or focus (docs); valid outputSchemas. Fix: expose tools; avoid external $ref. |
| mcp-tool-naming | MCP tool naming | mcp | V | 2 B | rec | Rc | N | Consistent, descriptive, non-generic names. Fix: standardize naming. |
| public-api | Public API reachable | domain (API) | V | 7 | req | R | N | Docs plus at least one responding endpoint. Fix: expose a public REST/GraphQL API. |
| oauth-support | OAuth 2.0 support | domain | V | 5 | req | R | N | OAuth 2.0 or an open API with no keys. Fix: implement OAuth and publish AS metadata. |
| scoped-permissions | Scoped permissions | domain | V | 5 | rec | R | N | Machine-readable OAuth scopes. Fix: declare scopes in OpenAPI or RFC 9728. |
| mcp-auth-mechanism | MCP auth mechanism | mcp | V | 2 B | rec | R | N | Auth matches server type. Fix: OAuth for product servers. |
| mcp-oauth-metadata | MCP OAuth metadata | mcp | V | 2 B | rec | R | N | RFC 8414 metadata with endpoints and CIMD flag. Fix: publish it. |
| mcp-pkce-s256 | MCP PKCE S256 | mcp | V | 2 B | rec | R | N | `S256` in `code_challenge_methods_supported`. Fix: add it. |
| onboarding-friction | Agent onboarding friction | domain | V | 2 | rec | Rc | N | Discovery to first API call without humans. Fix: free tier, self-serve keys, sandbox. |
| web-bot-auth-directory | Web Bot Auth directory | domain | E | 2 B | emg | E+b | N | Ed25519 JWKS at `/.well-known/http-message-signatures-directory`. Fix: publish keys. |
| oauth-protected-resource | RFC 9728 metadata | domain | V | 2 B | req | R | N | Protected-resource metadata with resource and auth details. Fix: publish at `/.well-known/oauth-protected-resource`. |
| auth-md-exists | auth.md exists | domain | V | 2 B D | req | E+b | N | `/auth.md` with at least 200 chars markdown. Fix: publish a credential walkthrough. |
| auth-md-structure | auth.md structure | domain | V | 2 B D | rec | E+b | N | Standard sections graded for content. Fix: follow the WorkOS structure. |
| auth-md-walkthrough-simulation | auth.md walkthrough | domain | V | 2 B D | rec | E+b | N | Auth chain traversable end to end. Fix: test and fix dead links. |
| agent-auth-discovery-metadata | Agent auth discovery metadata | domain | V | 3 B D | rec | E+b | N | RFC 9728/8414 metadata with an `agent_auth` block. Fix: publish and cross-link. |
| agent-auth-www-authenticate | WWW-Authenticate hint | domain | V | 1 B D | rec | Rc | N | 401 includes `resource_metadata`. Fix: add the header. |
| agent-auth-endpoints-reachable | agent_auth endpoints reachable | domain | V | 2 B D | rec | E+b | N | Advertised endpoints respond to OPTIONS. Fix: remove stale URIs or stand up endpoints. |
| pap-discovery | PAP discovery file | domain | E | 2 B D | emg | E+b | N | Valid `/.well-known/poppy.json` over HTTPS. Fix: publish it. |
| pap-issuer-binding | PAP issuer binding | domain | E | 2 B D | emg | E+b | N | Issuer metadata matches and lists this domain. Fix: align issuer metadata. |
| pap-auth-config | PAP sign-in config | domain | E | 2 B D | emg | E+b | N | Defined scopes and well-formed sign-in. Fix: use only PAP scopes. |
| pap-interfaces | PAP interface entries | domain | E | 2 B D | emg | E+b | N | Complete agent and API entries. Fix: fill required fields. |
| pap-endpoint-enforcement | PAP endpoint enforcement | domain | E | 2 B D | emg | E+b | N | Unauthenticated requests rejected correctly. Fix: return the specified error codes and challenges. |
| pap-cross-protocol | PAP cross-protocol consistency | domain | E | 2 B D | emg | E+b | N | Matches ARD, auth.md and issuers. Fix: align all surfaces. |
| mcp-server | MCP server/manifest | all | V | 6 | req | Rc | N | A Model Context Protocol server or manifest. Fix: build a Streamable HTTP MCP server. |
| mcp-error-handling | MCP error handling | mcp | V | 2 B | rec | R | N | Structured JSON-RPC errors. Fix: return code and message. |
| mcp-transport-modern | MCP modern transport | mcp | V | 1 B | rec | R | N | Streamable HTTP supported. Fix: move off legacy SSE. |
| webmcp | WebMCP support | domain | V | 5 | req | E+b | ? | In-page tools via `navigator`/`document` `modelContext.registerTool()`. Fix: register tools with registerTool(). Static JS could do it; no actions exist on a docs site. |
| rate-limit-headers | Rate limit headers | api | V | 2 | rec | Rc | N | RFC RateLimit headers and `Retry-After` on 429. Fix: add them. |
| idempotency-key-support | Idempotency-Key support | api | V | 3 | rec | Rc+b | N | Write operations accept the key. Fix: declare it in the spec. |
| json-error-responses | JSON error responses | domain | V | 4 | req | R | N | Structured JSON errors, not HTML. Fix: return JSON errors with codes and hints. Applies to API endpoints. |
| api-error-model | REST typed error model | api (REST) | V | 3 | rec | Rc | N | Typed error schema or RFC 9457. Fix: document errors in OpenAPI. |
| api-versioning-policy | REST versioning policy | api (REST) | V | 3 | rec | Rc | N | Versioning and deprecation signals. Fix: publish the policy and use Sunset headers. |
| pagination-shape | REST pagination | api (REST) | V | 2 | rec | Rc+b | N | Consistent, documented pagination. Fix: use cursors and define in spec. |
| async-job-pattern | REST async jobs | api (REST) | V | 2 | rec | Rc+b | N | 202 with a polling reference. Fix: document the polling pattern. |
| cli-tool | CLI tool | domain | V | 3 | rec | Rc | N | Official CLI on npm, PyPI or Homebrew. Fix: publish one. |
| rest-sdk-packages | Multi-language SDKs | domain | V | 3 | rec | Rc+b | N | Official SDKs with homepage links. Fix: generate and publish SDKs. |
| nlweb-ask | NLWeb /ask | domain | E | 1 | emg | E+b | N | `POST /ask` with the specified JSON shape. Fix: implement it. Needs a server. |
| nlweb-streaming | NLWeb streaming | domain | E | 1 | emg | E+b | N | SSE streaming on /ask. Fix: add event streaming. |
| response-schema-coverage | REST response schemas | api (REST) | V | 2 | rec | Rc | N | Typed response schemas per operation. Fix: define them. |
| mcp-tool-annotations | MCP tool annotations | mcp | V | 2 B | rec | Rc+b | N | `readOnlyHint` and `destructiveHint` set. Fix: annotate tools. |
| mcp-server-card | MCP server card | mcp | V | 2 B | rec | E+b | N | Card at `/server-card` or listed in ai-catalog.json. Fix: publish with `$schema` and a remotes URL. |
| mcp-multi-surface-coverage | Product + docs MCP | domain | V | 2 B | rec | E+b | N | Separate action and docs MCP servers. Fix: add a docs MCP surface. |
| sandbox-environment | Sandbox environment | domain | V | 2 B | rec | Rc+b | N | Test mode without production data. Fix: provide and document one. |
| batch-endpoints | REST batch endpoint | api (REST) | V | 2 B | rec | Rc+b | N | Batch or array-body operations. Fix: add batch support. |
| mcp-resource-listing | MCP resources exposed | mcp | V | 3 | rec | R | N | `resources/list` returns items if the capability is advertised. Fix: list resources or drop the capability. |
| graphql-error-type-definition | GraphQL typed errors | api (GraphQL) | V | 3 | rec | Rc | N | Error types in mutation payloads. Fix: model errors in schema. |
| graphql-versioning-policy | GraphQL deprecation | api (GraphQL) | V | 2 | rec | Rc | N | `@deprecated` with reasons. Fix: adopt the policy. |
| graphql-pagination-pattern | GraphQL pagination | api (GraphQL) | V | 2 | rec | Rc | N | Relay Connection/PageInfo. Fix: adopt Relay pagination. |
| graphql-async-job-pattern | GraphQL async jobs | api (GraphQL) | V | 2 | rec | Rc | N | Job types or subscriptions. Fix: model async work. |
| graphql-schema-completeness | GraphQL descriptions | api (GraphQL) | V | 3 B | rec | Rc | N | At least 80% of types/fields described. Fix: add descriptions. |
| graphql-batch-mutations | GraphQL batch mutations | api (GraphQL) | V | 2 B | rec | Rc | N | createMany/updateMany style fields. Fix: add them. |
| ax-document-structure | Accessible document structure | domain | V | 3 B | rec | R | Y | Landmarks, `main`, `nav`, heading order. Fix: use semantic HTML. |
| ax-native-controls | Native interactive controls | domain | V | 3 B | not read | not read | Y | Buttons are real buttons. Fix: replace clickable divs. (Tier and essentials values were cut off in the fetch.) |
| ax-accessible-names | Accessible names | domain | V | 2 B | rec | R | Y | Every control has a computable name. Fix: add labels or aria-label. |
| ax-form-labeling | Form labeling | domain | V | 2 B | rec | R | Y | Real labels on fields (N/A without forms). Fix: add labels. |
| ax-tree-injection-safe | Injection safety | domain | V | 2 B | rec | Rc+b | Y | Scans for hidden instructions in the accessibility tree. Fix: remove hidden instructions. |
| mcp-app-registry | MCP Apps support | mcp-app | V | 4 | rec | E+b | N | `ui://` resources and tool UI metadata. Fix: add MCP Apps via ext-apps. |
| a2ui-support | A2UI / generative UI | domain | E | 2 | emg | E+b | N | UI rendered in agent conversations. Fix: support MCP Apps or similar. |
| mcp-apps-ui-quality | MCP Apps UI quality | mcp-app | V | 4 B | rec | E+b | N | Correct MIME type, valid HTML, dark mode, no secrets. Fix: meet the listed requirements. |
| mcp-view-domain | MCP App view reachable | mcp-app | V | 4 | rec | R | N | View loads publicly with no auth wall. Fix: make it public. |
| mcp-view-csp | MCP App view CSP | mcp-app | V | 4 | rec | R | N | Specific origins declared in `_meta.ui.csp`, or omitted. Fix: declare narrow origins. |
| api-schema-analysis | API schema complexity | api | V | 2 | rec | Rc | N | Self-describing spec with operationIds and descriptions. Fix: simplify and document. |
| function-calling-compat | Function calling compatibility | domain | V | 2 | rec | Rc | N | Spec converts cleanly to LLM function formats. Fix: unique operationIds and typed schemas. |
| mcp-resource-quality | MCP resource quality | mcp | V | 3 | rec | Rc | N | Resources have valid mimeType and non-empty content. Fix: fix or remove broken resources. |

## Payments layer (10 pts)

Any one protocol satisfies the set; the others read N/A. All are N for a docs-only site that charges nothing.

| id | name | Applies | Mat | Pts | Tier | Ess | S | Test and fix |
|---|---|---|---|---|---|---|---|---|
| mpp-support | MPP | domain | V | 2 B | req | E+b | N | HTTP 402 with a full Payment challenge and `x-payment-info`. Fix: implement MPP. |
| x402-support | x402 | domain | V | 2 B | req | E+b | N | `PAYMENT-REQUIRED`/`PAYMENT-SIGNATURE`/`PAYMENT-RESPONSE` headers and `/discovery/resources`. Fix: implement x402. |
| ucp-support | UCP | domain | V | 3 B | req | E+b | N | `/.well-known/ucp` profile and checkout REST surface. Fix: publish profile and endpoints. |
| acp-support | ACP | domain | V | 3 B | req | E+b | N | `/checkout_sessions` with required headers and negotiation. Fix: implement the checkout API. |
| acp-delegate-payment | ACP delegate payment | domain | V | 3 B | rec | E+b | N | Delegate payment endpoint returning vault tokens. Fix: expose the endpoint. |
| ap2-support | AP2 | domain | V | 3 B | rec | E+b | N | Signed mandate verification and UCP capability. Fix: adopt AP2 only if no other protocol is covered. |

## Counts and discrepancies

- Rows recorded here: 132 (Discovery 16, Access 43, Usability 67, Payments 6). The https://ora.ai/methodology page states 126 checks (16, 42, 62, 6). Discovery and Payments match; Access is off by one and Usability by five. Likely cause: the catalog fetch includes draft/beta and PAP/auth.md rows the page total leaves out, but no source says so. Treat the catalog as the list and the page numbers as the headline.
- https://ora.ai/blog/ax-is-the-new-aeo and https://www.agentready.org/ both say "100+ checks" for the ranker.
- The essentials fetch showed 119 rows plus a 13-row tail (one row cut); that is 132 as well.
- The `ax-*` accessibility checks sit under Usability in the catalog. Is Agentic's essentials mapping rates `ax-document-structure`, `ax-accessible-names` and `ax-form-labeling` as required.

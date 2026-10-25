# Distribution surfaces and Cloudflare quota

Checked 2026-10-25. Cloudflare figures come from the Workers documentation pages named below. Ora and Is Agentic results come from scans that Pablo ran after the site went live.

## Why this note exists

The first Ora scan scored the site 58 out of 100 and Is Agentic scored it 81. After the Markdown negotiation Worker, the Markdown 404, `og:image`, and the author metadata, Is Agentic scored 100 and Ora scored 62. The remaining Ora gaps fall into two groups.

- Gaps that ask for a surface the site does not have: OAuth metadata, `auth.md`, Web Bot Auth, a sandbox, a developer portal, an A2A card, NLWeb `/ask`, and payments. This site has no account, no API, and nothing to protect. Building these only to score would mislead an agent that tries to use them.
- Gaps that a real deliverable would close: a machine-readable index, a CLI, an MCP server, more than one skill, and an API catalog that points to something.

## Decision

Build the deliverables in this order. Each one reads a single generated file, `cards.json`, so a card edit reaches every surface after one `python3 tools/build.py`.

1. `cards.json` and its JSON Schema. Static files.
2. A CLI that reads `cards.json`. Published to npm from Pablo's account.
3. Cloudflare rules that serve `index.md` for `Accept: text/markdown` on `/`, so the homepage does not invoke the Worker.
4. Later, and only after Pablo decides on the Workers Paid plan: a read-only MCP server with `cards.json` bundled into the Worker, a server card, and concern-scoped skills.

Not planned: OAuth metadata, `auth.md`, Web Bot Auth, sandbox, developer portal, A2A, NLWeb, WebMCP, and payments.

## Cloudflare quota

Source: https://developers.cloudflare.com/workers/static-assets/billing-and-limitations/ and https://developers.cloudflare.com/workers/platform/limits/.

| Fact | Detail |
|---|---|
| Static asset requests | Free and unlimited. Storage is free. This covers every `.md`, `llms.txt`, and `cards.json`. |
| Worker invocations | Counted. A request that matches `run_worker_first`, or no static file when a Worker is configured, invokes the Worker. |
| Workers Free daily limit | 100,000 requests a day, resetting at midnight UTC. CPU time is 10 ms per request. |
| Over the free limit | A `run_worker_first` request gets a 429 response and does not fall back to the static file. Other overages return Cloudflare error 1027 unless the Worker fails open. |
| Workers Paid | No request limit is listed on the pages above. The price and the included requests are on the Workers pricing page and were not checked. |

The first Worker version used `run_worker_first: ["/"]`. On a day above the free limit, human visitors would get a 429 on the homepage. That is the reason to move `/` off the Worker.

## Homepage without a Worker

Two Cloudflare rules replace the Worker branch for `/`. They live in the dashboard, not in the repo, so `docs/deploy.md` records them.

- A URL Rewrite rule. When the path is `/` and the `Accept` header contains `text/markdown`, rewrite the path to `/index.md`.
- A Modify Response Header rule. On `/`, set `Vary: Accept`.

These rules are untested. Verify with `curl -sS -i -H 'Accept: text/markdown' https://goodcodereview.com/` and the same request with `Accept: text/html` after creating them.

After that, the Worker answers only for paths that match no file. Bots that probe unknown paths still reach it, so a Cloudflare rate limiting rule on unknown paths is a cheap guard.

## Design rules for new surfaces

- Put heavy use on static files. A CLI call fetches `/cards.json` and is free.
- Bundle `cards.json` into any Worker at build time. A Worker call then costs one invocation and no subrequests.
- Add a billing notification before shipping anything that invokes the Worker per use.
- Keep one source. The cards are the only input, and `tools/build.py` generates every surface from them.

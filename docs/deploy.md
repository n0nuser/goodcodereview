# Deploy

`tools/build.py` builds the site as plain static files. Cloudflare Workers serves them as static assets.

## Workers project settings

Cloudflare points new static sites at Workers with static assets. `wrangler.jsonc` in the repo root sets the output directory (`site`) and `auto-trailing-slash` handling for `.html` files. `src/worker.js` runs for paths that match no file, and for `/concerns.md` and `/cards.json` (`run_worker_first`). For those two it answers `?concern=`, `?topic=`, `?level=`, and `?group=` filters with a filtered Markdown or JSON list, and with no filter it passes the request to the static file. For unmatched paths it returns the `404.html` page, or a short Markdown 404 for a Markdown request, with status 404. `site/_headers` applies to every static response. Test the Worker with `node --test test/worker.test.mjs`.

Static files cost nothing and have no request limit, so the homepage, `cards.json`, and every `.md` file stay off the Worker. The free Workers plan allows 100,000 Worker requests a day. Past that, a Worker request gets a 429 instead of the static file, so only unknown paths and the two filter paths may reach the Worker; the HTML pages, including `/concerns`, never do (the page filters in the browser). If the quota becomes a problem, drop `run_worker_first` and the filters on `.md` and JSON stop working; the page filters still work. Research: `docs/research/distribution-and-quota.md`.

### Which requests reach the Worker

`run_worker_first` lists `/concerns.md` and `/cards.json`, so every request to those two paths starts the Worker, with or without a query string, and counts against the 100,000 a day. A route cannot see the query string, so the Worker has to look at it. Besides those two paths, the Worker runs only for paths that match no file (the 404 page).

Everything else is a static asset and never starts the Worker: the HTML pages, every other `.md` file, `llms.txt`, `cards-drafts.json`, `cards-index.json`, `cards/<level>.json`, `cards/drafts-<level>.json`, `cards/concern-<concern>.json`, `concerns/<concern>.md`, and `concerns/level-<level>.md`. Point agents at those paths (`llms.txt` lists them) instead of at a query on `/cards.json` or `/concerns.md`.

Inside the Worker, a single `concern` or `level` is answered by fetching the static file, with no parse. Any other filter parses `cards-index.json` (Markdown, about 54 KB) or `cards.json` (JSON, about 437 KB), and the Worker keeps the answer in the Cache API under the request URL for 300 seconds. A cache hit still counts as a Worker request but skips the parse.

In the dashboard, choose Workers & Pages, Create, and connect `n0nuser/goodcodereview` on `main`. Set:

- Build command: `python3 tools/build.py`
- Deploy command: `npx wrangler deploy` (the default)
- Preview command: the default

The Pages build image has Python 3, and the build uses only the standard library. To use the legacy Pages workflow instead, choose Pages, Connect to Git, framework preset None, build command `python3 tools/build.py`, output directory `site`, and no deploy command.

## Staged rollout

A push to `main` builds and deploys the whole site at once, so a bad build reaches every visitor. To roll out in stages, use Workers gradual deployments:

1. Upload without deploying: `npx wrangler versions upload`. This creates a version that receives no traffic.
2. Send a small share of traffic to it: `npx wrangler versions deploy <new-version-id>@10% <current-version-id>@90%`. Wait 30 minutes.
3. Compare the new version to the current one on error rate (Workers metrics, 5xx) and on `/llms.txt`, `/cards.json`, and `/index.html` returning 200 with the expected `Content-Type`. Run `curl -sS -o /dev/null -w '%{http_code}' https://goodcodereview.com/llms.txt` against the split.
4. Abort rule: if the error rate of the new version is above the current version's, or any of those three URLs fails, deploy the previous version at 100% with `npx wrangler versions deploy <current-version-id>@100%`. Do not decide by judgment.
5. Otherwise raise to 50%, then 100%.

Owner action: today the Cloudflare dashboard (or its Git integration) deploys `main` at 100% in one step. Switching it to `wrangler versions upload` plus a staged `versions deploy` step is a change to the Cloudflare project or its CI, and it is the owner's to make. Nothing in this repository changes those settings. Check Cloudflare's gradual-deployment notes on version affinity before the first split: a visitor may get the HTML from one version and a later request from the other.

## Cloudflare rules

Two rules serve `index.md` for `Accept: text/markdown` on the homepage without a Worker. They live in the dashboard (Rules, then Transform Rules) and not in the repo, so recreate them if the zone changes.

1. Rewrite URL rule, named "Markdown for agents".
   - When: `(http.host in {"goodcodereview.com" "www.goodcodereview.com"} and http.request.uri.path eq "/" and any(http.request.headers["accept"][*] contains "text/markdown"))`
   - Then: rewrite the path to the static value `/index.md`.
2. Modify Response Header rule, named "Vary on Accept".
   - When: `(http.host in {"goodcodereview.com" "www.goodcodereview.com"} and http.request.uri.path in {"/" "/index.md"})`
   - Then: set the static header `Vary` to `Accept`.

Verify both:

```
curl -sS -i -H 'Accept: text/markdown' https://goodcodereview.com/
curl -sS -i -H 'Accept: text/html' https://goodcodereview.com/
```

The first must return Markdown with `Content-Type: text/markdown` and `Vary: Accept`. The second must return HTML with `Vary: Accept`.

## Custom domain

An apex domain (`goodcodereview.com`, no `www`) on Pages needs its DNS zone on Cloudflare. The registrar can stay where it is, and only the nameservers move. The Cloudflare free plan covers the DNS.

1. In the Cloudflare dashboard, choose Add a domain, enter `goodcodereview.com`, and choose the Free plan. Note the two nameservers that Cloudflare gives you.
2. At the registrar, set the domain's nameservers to those two. In Namecheap: Domain List, Manage, Nameservers, Custom DNS. Wait until Cloudflare shows the zone as Active.
3. In the project, open Settings, Domains & Routes, then add a custom domain. (In the legacy Pages workflow: Custom domains, then Set up a custom domain.) Add `goodcodereview.com`, then `www.goodcodereview.com`. Cloudflare creates the DNS records.
4. Wait until the certificate shows Active. Then open `https://goodcodereview.com/llms.txt`.

Cost: the Pages free plan (static requests and bandwidth are not metered, and it allows 500 builds a month) and the free DNS plan. Only the domain renewal costs money.

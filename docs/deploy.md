# Deploy

`tools/build.py` builds the site as plain static files. Cloudflare Workers serves them as static assets.

## Workers project settings

Cloudflare points new static sites at Workers with static assets. `wrangler.jsonc` in the repo root sets the output directory (`site`) and `auto-trailing-slash` handling for `.html` files. `src/worker.js` runs for paths that match no file, and for `/concerns`, `/concerns.md`, and `/cards.json` (`run_worker_first`). For those three it answers `?concern=`, `?topic=`, `?level=`, and `?group=` filters with a filtered Markdown or JSON list, and with no filter it passes the request to the static file. For unmatched paths it returns the `404.html` page, or a short Markdown 404 for a Markdown request, with status 404. `site/_headers` applies to every static response. Test the Worker with `node --test test/worker.test.mjs`.

Static files cost nothing and have no request limit, so the homepage, `cards.json`, and every `.md` file stay off the Worker. The free Workers plan allows 100,000 Worker requests a day. Past that, a Worker request gets a 429 instead of the static file, so only unknown paths and the three filter paths may reach the Worker. If the quota becomes a problem, drop `run_worker_first` and the filters on `.md` and JSON stop working; the page filters still work. Research: `docs/research/distribution-and-quota.md`.

In the dashboard, choose Workers & Pages, Create, and connect `n0nuser/goodcodereview` on `main`. Set:

- Build command: `python3 tools/build.py`
- Deploy command: `npx wrangler deploy` (the default)
- Preview command: the default

The Pages build image has Python 3, and the build uses only the standard library. To use the legacy Pages workflow instead, choose Pages, Connect to Git, framework preset None, build command `python3 tools/build.py`, output directory `site`, and no deploy command.

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

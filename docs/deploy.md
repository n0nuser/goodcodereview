# Deploy

`tools/build.py` builds the site as plain static files. Cloudflare Pages hosts them.

## Workers project settings

Cloudflare points new static sites at Workers with static assets. `wrangler.jsonc` in the repo root sets the output directory (`site`), a custom `404.html` for unknown paths, and `auto-trailing-slash` handling for `.html` files. `site/_headers` is applied to the static responses.

In the dashboard, choose Workers & Pages, Create, and connect `n0nuser/goodcodereview` on `main`. Set:

- Build command: `python3 tools/build.py`
- Deploy command: `npx wrangler deploy` (the default)
- Preview command: the default

The Pages build image has Python 3, and the build uses only the standard library. To use the legacy Pages workflow instead, choose Pages, Connect to Git, framework preset None, build command `python3 tools/build.py`, output directory `site`, and no deploy command.

## Custom domain

An apex domain (`goodcodereview.com`, no `www`) on Pages needs its DNS zone on Cloudflare. The registrar can stay where it is, and only the nameservers move. The Cloudflare free plan covers the DNS.

1. In the Cloudflare dashboard, choose Add a domain, enter `goodcodereview.com`, and choose the Free plan. Note the two nameservers that Cloudflare gives you.
2. At the registrar, set the domain's nameservers to those two. In Namecheap: Domain List, Manage, Nameservers, Custom DNS. Wait until Cloudflare shows the zone as Active.
3. In the project, open Settings, Domains & Routes, then add a custom domain. (In the legacy Pages workflow: Custom domains, then Set up a custom domain.) Add `goodcodereview.com`, then `www.goodcodereview.com`. Cloudflare creates the DNS records.
4. Wait until the certificate shows Active. Then open `https://goodcodereview.com/llms.txt`.

Cost: the Pages free plan (static requests and bandwidth are not metered, and it allows 500 builds a month) and the free DNS plan. Only the domain renewal costs money.

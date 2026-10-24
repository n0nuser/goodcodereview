# Deploy

`tools/build.py` builds the site as plain static files. Cloudflare Pages hosts them.

## Pages project settings

- Framework preset: None
- Build command: `python3 tools/build.py`
- Build output directory: `site`
- Python: no pin needed. The Pages build image ships Python 3.11 (v2) or 3.13 (v3), and the build uses only the standard library. To pin a version, set the `PYTHON_VERSION` environment variable or add a `.python-version` file. See [Cloudflare language support](https://developers.cloudflare.com/pages/configuration/language-support-and-tools/).

## Custom domain

An apex domain (`goodcodereview.com`, no `www`) on Pages needs its DNS zone on Cloudflare. The registrar can stay where it is, and only the nameservers move. The Cloudflare free plan covers the DNS.

1. In the Cloudflare dashboard, choose Add a domain, enter `goodcodereview.com`, and choose the Free plan. Note the two nameservers that Cloudflare gives you.
2. At the registrar, set the domain's nameservers to those two. In Namecheap: Domain List, Manage, Nameservers, Custom DNS. Wait until Cloudflare shows the zone as Active.
3. In the Pages project, choose Custom domains, then Set up a custom domain. Add `goodcodereview.com`, then `www.goodcodereview.com`. Cloudflare creates the DNS records.
4. Wait until the certificate shows Active. Then open `https://goodcodereview.com/llms.txt`.

Cost: the Pages free plan (static requests and bandwidth are not metered, and it allows 500 builds a month) and the free DNS plan. Only the domain renewal costs money.

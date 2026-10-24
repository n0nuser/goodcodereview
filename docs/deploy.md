# Deploy

The site is plain static files built by `tools/build.py`. Hosted on Cloudflare Pages.

## Pages project settings

- Framework preset: None
- Build command: `python3 tools/build.py`
- Build output directory: `site`
- Python: no pin needed. Pages' build image already ships Python 3.11 (v2) or 3.13 (v3), and the build uses only the standard library. To pin, set the `PYTHON_VERSION` environment variable or add a `.python-version` file ([Cloudflare language support](https://developers.cloudflare.com/pages/configuration/language-support-and-tools/)).

## Custom domain

An apex domain (`goodcodereview.com`, no `www`) on Pages needs its DNS zone on Cloudflare. The registrar can stay where it is; only the nameservers move. Cloudflare's free plan covers the DNS.

1. Cloudflare dashboard, Add a domain, `goodcodereview.com`, Free plan. Note the two nameservers it gives.
2. At the registrar, set the domain's nameservers to those two (Namecheap: Domain List, Manage, Nameservers, Custom DNS). Wait for Cloudflare to show the zone Active.
3. Pages project, Custom domains, Set up a custom domain: add `goodcodereview.com`, then `www.goodcodereview.com`. Cloudflare creates the DNS records.
4. Wait for the certificate to show Active, then check `https://goodcodereview.com/llms.txt`.

Cost: Pages free plan (static requests and bandwidth are not metered; 500 builds a month) and the free DNS plan. Only the domain renewal is paid.

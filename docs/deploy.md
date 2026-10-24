# Deploy

The site is plain static files built by `tools/build.py`. Hosted on Cloudflare Pages.

## Pages project settings

- Framework preset: None
- Build command: `python3 tools/build.py`
- Build output directory: `site`
- Python: no pin needed. Pages' build image already ships Python 3.11 (v2) or 3.13 (v3), and the build uses only the standard library. To pin, set the `PYTHON_VERSION` environment variable or add a `.python-version` file ([Cloudflare language support](https://developers.cloudflare.com/pages/configuration/language-support-and-tools/)).

## Custom domain

1. Pages project, Custom domains, Set up a custom domain, enter `goodcodereview.com`.
2. If the domain's DNS is on Cloudflare, accept the CNAME it proposes. Otherwise add a CNAME to `<project>.pages.dev` at your DNS host.
3. Wait for the certificate to show Active, then check `https://goodcodereview.com/llms.txt`.

# goodcodereview

Command line for [goodcodereview.com](https://goodcodereview.com). It reads the site's public static files, needs no account or key, and has no dependencies.

```sh
uvx goodcodereview levels
uvx goodcodereview cards --concern security --level function
uvx goodcodereview card svc-sqli-authn
uvx goodcodereview prompt
```

A single level or concern is one static file. A combination is filtered on your machine, so the site runs no code for it. `--base file:///path/to/site` reads a local build.

Content is CC BY 4.0, code is MIT. Source: [cli/](https://github.com/n0nuser/goodcodereview/tree/main/cli).

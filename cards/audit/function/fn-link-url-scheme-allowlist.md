---
id: fn-link-url-scheme-allowlist
level: function
tags: [security, xss, javascript]
severity: should-fix
status: stable
lang: core
applies_when: A URL taken from remote JSON, a query parameter or stored data is written to `href`, `src`, `location` or `window.open`.
context: [ui]
tool_gate: none
note: OWASP says URL properties need URL validation even where React blocks javascript: URLs; Angular sanitizes URL bindings. fn-no-raw-html-sink covers HTML sinks, and fn-redirect-target-allowlist covers server redirects
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
  - https://angular.dev/best-practices/security
  - https://developer.wordpress.org/reference/functions/esc_url/
---

**Rule.** Parse a URL that comes from data and allow only `https:` (and `http:` or `mailto:` where needed) before you set it as a link target.

**Why.** A `javascript:` URL in an `href` runs script in your origin when clicked, and a data feed or an API you do not fully control can supply one. Some frameworks block it, but the check belongs to the app, because the next sink may not be covered.

**FAIL**

```javascript
const item = await (await fetch("/feed.json")).json();
link.href = item.url;
```

**PASS**

```javascript
const item = await (await fetch("/feed.json")).json();
const u = new URL(item.url, location.origin);
link.href = ["https:", "http:"].includes(u.protocol) ? u.href : "#";
```

**Counterpoint.** "The feed is ours, so it is trusted." It is trusted until a third party writes into it or someone breaches it. The check is two lines and does not depend on who owns the source.

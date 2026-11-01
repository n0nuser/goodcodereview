---
id: fn-guard-uri-decoding
level: function
tags: [reliability, correctness, javascript]
severity: should-fix
status: draft
lacks: orgs, Mozilla (MDN) and the Node.js docs back it; needs one more org that guards or avoids a throwing decode on user input
lang: core
applies_when: Code calls `decodeURIComponent` or `decodeURI` on a query parameter, a hash, a path segment or other input a user controls.
context: [ui, server]
tool_gate: none
note: MDN lists the URIError and shows a try/catch; Node's querystring.unescape falls back to a decoder that does not throw
borrowed_from:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/decodeURIComponent
  - https://nodejs.org/api/querystring.html
---

**Rule.** Wrap `decodeURIComponent` on user input in a `try`/`catch`, or parse with `URLSearchParams`, so that a malformed `%` sequence cannot throw.

**Why.** `decodeURIComponent("%E0%A4%A")` throws a `URIError`. A link with a stray `%` in its query then breaks the page script for that visitor, and anyone can craft such a link.

**FAIL**

```javascript
const q = decodeURIComponent(location.hash.slice(1));
render(q);
```

**PASS**

```javascript
let q;
try {
  q = decodeURIComponent(location.hash.slice(1));
} catch {
  q = "";
}
render(q);
```

**Counterpoint.** "Only our own links reach this code." The address bar accepts anything, and other sites, chat apps and crawlers produce broken links. A guard costs three lines.

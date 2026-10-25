---
id: fn-no-prototype-pollution
level: function
tags: [security, javascript, injection]
severity: block
status: draft
lacks: unreviewed, OWASP, PortSwigger, GitHub and Snyk listed; check each recommends the practice rather than defining it
lang: core
applies_when: JavaScript or TypeScript code merges, clones, or assigns properties whose key names come from JSON, a query string, or other untrusted input.
tool_gate: CodeQL `js/prototype-pollution-utility` and `js/prototype-polluting-assignment`.
note: ASVS 15.3.6; fn-no-mass-assignment covers the same input setting fields on a model instead of the prototype
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x24-V15-Secure-Coding-and-Architecture.md
  - https://cheatsheetseries.owasp.org/cheatsheets/Prototype_Pollution_Prevention_Cheat_Sheet.html
  - https://cwe.mitre.org/data/definitions/1321.html
  - https://portswigger.net/web-security/prototype-pollution/preventing
  - https://codeql.github.com/codeql-query-help/javascript/js-prototype-pollution-utility/
  - https://learn.snyk.io/lesson/prototype-pollution/
---

**Rule.** Never write an untrusted key into a plain object. Use a `Map`, an object from `Object.create(null)`, or an allowlist of keys, and block `__proto__`, `constructor`, and `prototype` in any deep merge.

**Why.** `obj[key] = value` with `key` set to `__proto__` writes to `Object.prototype`, so every object in the process gains that property. An attacker who sets `isAdmin` or a template option there can skip checks or reach code execution. The bug sits in generic helpers such as deep merge and path setters, so one bad helper exposes every caller.

**FAIL**

```javascript
function merge(dst, src) {
  for (const k in src) {
    if (typeof src[k] === "object") merge(dst[k] ??= {}, src[k]);
    else dst[k] = src[k];
  }
}
merge(settings, JSON.parse(body));   // body: {"__proto__": {"isAdmin": true}}
```

**PASS**

```javascript
const ALLOWED = new Set(["theme", "lang"]);
const prefs = new Map();
for (const [k, v] of Object.entries(JSON.parse(body))) {
  if (ALLOWED.has(k)) prefs.set(k, v);
}
```

**Counterpoint.** "Just freeze `Object.prototype` at startup." That helps, and the sources list it, but it can break libraries that patch prototypes, and it leaves `constructor.prototype` paths in class instances open. Fix the merge, and add the freeze on top if your dependencies allow it.

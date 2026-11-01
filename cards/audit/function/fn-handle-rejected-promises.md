---
id: fn-handle-rejected-promises
level: function
tags: [reliability, correctness, javascript]
severity: should-fix
status: stable
lang: core
applies_when: Code starts a promise that can reject, such as `fetch`, `navigator.clipboard.writeText` or an async function, and does not return it.
tool_gate: typescript-eslint `no-floating-promises`.
note: MDN (Mozilla), web.dev (Google), typescript-eslint and Node.js each state the practice or its effect. Node.js ends the process by default on an unhandled rejection
borrowed_from:
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Using_promises
  - https://developer.mozilla.org/en-US/docs/Web/API/Clipboard/writeText
  - https://web.dev/articles/async-clipboard
  - https://typescript-eslint.io/rules/no-floating-promises/
  - https://nodejs.org/api/cli.html
---

**Rule.** Handle the rejection of every promise you start: `await` it inside `try`/`catch`, end the chain with `.catch()`, or return it to a caller that does.

**Why.** A browser API such as `writeText` rejects when the page lacks permission. With no handler the failure surfaces only as an `unhandledrejection` event, the user sees nothing, and the next step runs as if the call worked. In Node.js 15 and later the same rejection ends the process by default.

**FAIL**

```javascript
button.addEventListener("click", () => {
  navigator.clipboard.writeText(url);
  showToast("Copied");
});
```

**PASS**

```javascript
button.addEventListener("click", async () => {
  try {
    await navigator.clipboard.writeText(url);
    showToast("Copied");
  } catch (err) {
    showToast("Could not copy. Select the text and copy it by hand.");
  }
});
```

**Counterpoint.** "A global `unhandledrejection` handler already logs everything." It logs after the fact and cannot tell the user what to do. Only the call site knows which message and which fallback fit. Keep the global handler as a net, not as the handling.

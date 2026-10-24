---
id: fn-no-raw-html-sink
level: function
tags: [security, xss, frontend]
severity: block
status: draft
lang: core
applies_when: Code writes a string into a page, a template or a rendered model-output view.
tool_gate: ESLint (`no-unsanitized/property`, `no-unsanitized/method`, `react/no-danger`) and template-engine autoescape checks.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html
  - https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
  - https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML
  - https://web.dev/articles/trusted-types
  - https://react.dev/reference/react-dom/components/common
  - https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-cross-site-scripting-vulnerabilities
---

**Rule.** Write untrusted text through an encoding sink (`textContent`, auto-escaped template), never through a raw HTML sink.

**Why.** One `innerHTML` of a username or of model output runs the attacker's script with the victim's session. Encoding must match the context: body, attribute, script string and URL each differ. Framework escape hatches such as `dangerouslySetInnerHTML` have the same effect.

**FAIL**

```text
el.innerHTML = comment.body;
<div dangerouslySetInnerHTML={{ __html: reply }} />
```

**PASS**

```text
el.textContent = comment.body;
<div>{reply}</div>                       // escaped by the framework
// user-authored HTML: DOMPurify.sanitize(html), nothing edited afterwards
```

**Counterpoint.** "We need to render rich text." Then sanitise with a maintained library such as DOMPurify at render time and add a CSP as a second layer. A CSP alone is not a fix, because it is defence in depth.

---
id: fn-colour-not-sole-cue
level: function
tags: [accessibility, usability, frontend, css]
severity: should-fix
status: stable
lang: core
applies_when: Styles or markup show an error, a required field, a status, or a link using colour.
tool_gate: none; view the page in greyscale, or run a browser colour-vision emulation.
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
  - https://www.nngroup.com/articles/error-message-guidelines/
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json
  - https://inclusive-components.design/notifications/
---

**Rule.** Pair every colour that carries meaning with a second cue: text, an icon, a shape, or an underline.

**Why.** Colour-blind users, glare, greyscale mode, and a screen reader all remove colour. A red border on a bad field, or a link that differs from body text only by hue, tells those users nothing.

**FAIL**

```css
.field.error { border-color: red; }
.status-ok   { color: green; }
a { color: #0a58ca; text-decoration: none; }
```

**PASS**

```html
<input aria-invalid="true" aria-describedby="e1" style="border: 2px solid #b42318">
<p id="e1" class="error"><svg aria-hidden="true">…</svg> Error: enter a date such as 27/03/2026</p>
<a href="/terms" style="text-decoration: underline">terms</a>
```

**Counterpoint.** "Colour is the quickest cue, and the icon clutters the design." Colour can stay as the fast cue. The rule asks for a second one, not for removing the first. A text prefix such as "Error:" costs a few characters. A link in body text can also pass with 3:1 contrast against the text around it plus a non-colour cue on hover and focus. The underline is the simpler fix.

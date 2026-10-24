---
id: mod-colour-tokens-meet-contrast
level: module
tags: [accessibility, usability, frontend, css, design-system]
severity: should-fix
status: stable
lang: core
applies_when: A design-system module or theme defines foreground and background colour tokens.
tool_gate: axe `color-contrast` on rendered components; a unit test that computes the ratio for each token pair. axe cannot see text on images or gradients.
note: 5 orgs; the 3:1 figure for non-text parts is cited through the A11y Project and web.dev pages, and SC 1.4.11 was not read as its own page
borrowed_from:
  - https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
  - https://dequeuniversity.com/rules/axe/html/4.10/color-contrast
  - https://www.a11yproject.com/checklist/
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json
  - https://web.dev/learn/accessibility/focus
  - https://www.w3.org/WAI/test-evaluate/preliminary/
---

**Rule.** Make every text and background token pair meet 4.5:1 (3:1 for large text), and every border, icon, and focus colour meet 3:1 against its neighbour.

**Why.** Low contrast is invisible to the author on a bright monitor. Fixing it once in the tokens fixes every component. Fixing it per component means hunting through each one, and each new component can reintroduce it.

**FAIL**

```css
:root {
  --text-muted: #9aa0a6;     /* 2.6:1 on white */
  --bg: #ffffff;
  --input-border: #e0e0e0;   /* 1.3:1 on white */
}
```

**PASS**

```css
:root {
  --text-muted: #5f6368;     /* 6.0:1 on white */
  --bg: #ffffff;
  --input-border: #767676;   /* 4.5:1 on white, above the 3:1 floor */
}
```

```js
test.each(pairs)("%s meets 4.5:1", (fg, bg) => expect(ratio(fg, bg)).toBeGreaterThanOrEqual(4.5));
```

**Counterpoint.** "The brand colour fails." A logo is exempt. A brand-coloured button label or link is not. Darken the shade used for text and keep the brand shade for fills. The ratio is exact: 4.499:1 fails.

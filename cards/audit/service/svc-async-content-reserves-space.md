---
id: svc-async-content-reserves-space
level: service
tags: [usability, performance, frontend, css]
severity: should-fix
status: draft
lacks: orgs, injected content and ads have Google only; the image-dimensions part has Google and Mozilla
lang: core
applies_when: A page loads images, embeds, fonts, ads, or fetched content after the first paint.
tool_gate: Lighthouse CI assertion on `cumulative-layout-shift`.
note: draft after stable pass 5 - injected content and ads are backed by Google only; cut to image dimensions the Rule has Google and Mozilla firm, while WHATWG advises width and height only on lazy-loaded images (checked 2026-10-24), so it is a partial third; Apple and NN/g on placeholders are indirect
borrowed_from:
  - https://web.dev/articles/cls
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/loading.json
  - https://www.nngroup.com/articles/skeleton-screens/
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img
  - https://developer.mozilla.org/en-US/docs/Glossary/CLS
  - https://html.spec.whatwg.org/multipage/embedded-content.html
---

**Rule.** Reserve the space for late-loading content with set dimensions or an aspect ratio, so nothing already on screen moves.

**Why.** A page that jumps while someone reads or taps makes them hit the wrong target. A cumulative layout shift of 0.1 or less is good, and over 0.25 is poor, measured on real users at the 75th percentile.

**FAIL**

```html
<img src="/hero.jpg">
<div id="promo"></div>   <!-- script inserts a banner above the article -->
```

**PASS**

```html
<img src="/hero.jpg" width="1200" height="630" style="max-width: 100%; height: auto">
<div id="promo" style="min-height: 90px"></div>
```

**Counterpoint.** "Ads vary in height." Reserve the common height, or the largest, and accept some blank space. A banner that pushes the article down is the worse trade.

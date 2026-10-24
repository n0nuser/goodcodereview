---
id: fn-reduced-motion-respected
level: function
tags: [accessibility, usability, frontend, css, motion]
severity: should-fix
status: draft
lang: core
applies_when: Styles or script add a transition, an animation, a parallax effect, or autoplay motion.
tool_gate: Stylelint `a11y/media-prefers-reduced-motion` (a plugin; name from author knowledge). A browser run with reduced motion emulated.
note: WCAG 2.3.3 is level AAA, so this is good practice and not an AA floor
borrowed_from:
  - https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
  - https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html
  - https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json
  - https://www.a11yproject.com/checklist/
  - https://web.dev/articles/cls
---

**Rule.** Switch off or replace large, repeating, or interaction-triggered motion when `prefers-reduced-motion: reduce` is set.

**Why.** Scaling, panning, and parallax can trigger nausea and dizziness for people with vestibular disorders. They have already told their device so. A page that ignores the setting makes them leave.

**FAIL**

```css
.hero   { animation: zoom-in 1.2s ease-out infinite alternate; }
.card   { transition: transform 0.6s; }
.card:hover { transform: scale(1.3) rotate(4deg); }
```

**PASS**

```css
.hero { animation: zoom-in 1.2s ease-out infinite alternate; }
@media (prefers-reduced-motion: reduce) {
  .hero { animation: none; }
  .card { transition: opacity 0.2s; }
  .card:hover { transform: none; opacity: 0.9; }
}
```

**Counterpoint.** "Motion carries meaning, such as a loading spinner." Keep what the user needs and make it gentler: swap movement for a fade. The rule is about decorative and large movement, not about every pixel that moves.

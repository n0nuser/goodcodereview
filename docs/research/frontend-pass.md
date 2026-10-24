# Frontend pass: sources for a usability and accessibility checklist

Fetched 2026-10-24. Pages were read through WebFetch (a small model summarises the page), so every row is paraphrase. Each row gives the URL, the organisation behind it, how much was read, the distilled point, whether a reviewer can mark `FAIL`, and the card id it supports. Quotes are 15 words or fewer. "Topic only" means the page covers the subject but does not back the rule's requirement, so it does not count. A row that cites an earlier row by number is a re-use of that page.

Org counting: one organisation counts once, whatever the number of pages. W3C covers every w3.org page, including WCAG Understanding documents, the WAI tutorials, and the ARIA Authoring Practices Guide (APG). NN/g covers Nielsen's heuristics and the NN/g articles. Google covers web.dev. Mozilla covers MDN. Apple is one. GOV.UK covers the Design System, the Service Manual, the design principles, and the GDS accessibility tool audit. USWDS (GSA) and Section508.gov are separate bodies of the US government. Deque is axe-core and its rule pages. The A11y Project, WebAIM (Utah State University), Heydon Pickering's Inclusive Components, Baymard, Ben Shneiderman (University of Maryland), Don Norman (jnd.org), and the `eslint-plugin-jsx-a11y` project are one organisation each. The notes at the end of each section give the count per rule.

Fetch problems, recorded as gaps. The Apple HIG HTML pages are rendered by script and returned only the page title, so Apple rows were read from `developer.apple.com/tutorials/data/design/human-interface-guidelines/<page>.json`. Material Design (`m3.material.io`) returned only a title for both pages tried, so it backs no rule. `nngroup.com/articles/principles-of-design-norman/`, `web.dev/articles/accessibility-testing`, and the MDN Cumulative Layout Shift glossary page returned 404. The USWDS `form-controls` URL redirects to `form`. The Section508.gov `develop` page states no WCAG requirement.

## 1. Function level

### fn-img-alt-text

1. https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html (org: W3C; read: full). Every image needs a text alternative that serves the same purpose. A decorative image gets `alt=""` or moves to CSS. Listed failures: no `alt`, a file name as `alt`, non-empty `alt` on a decorative image. FAIL: yes. -> `fn-img-alt-text`.
2. https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Accessibility/HTML (org: Mozilla; read: full). Meaningful images need short, context-specific alt text. Decorative images get an empty `alt`. File names tell the user nothing. The same page covers labels (row 7) and native elements (row 12). FAIL: yes. -> `fn-img-alt-text`, `fn-form-control-has-label`, `fn-native-button-or-link`.
3. https://dequeuniversity.com/rules/axe/html/4.10/image-alt (org: Deque; read: full). The axe rule `image-alt` has critical impact. A missing `alt` makes a screen reader fall back to the file name. Avoid "image" and "chart" as alt text. FAIL: yes. -> `fn-img-alt-text`.
4. https://www.a11yproject.com/checklist/ (org: The A11y Project; read: full). A checklist: every `img` has an `alt`, decorative images have an empty one, and charts and maps get a text alternative. The same page backs rows on labels, focus, contrast, motion, headings, titles, and links. FAIL: yes. -> `fn-img-alt-text` and most cards below.
5. https://github.com/jsx-eslint/eslint-plugin-jsx-a11y (org: jsx-eslint; read: README). A static JSX checker. `alt-text` flags images with no alternative text. The README says it catches only what static code shows and recommends testing the rendered DOM and with assistive technology. FAIL: yes, as a lint. -> `fn-img-alt-text`.

Notes: 5 orgs (W3C, Mozilla, Deque, A11y Project, jsx-eslint). The card keeps the alt text itself a judgment: a tool can see that `alt` exists but not that it is accurate. The Deque page and the GDS audit (row 76) both say so.

### fn-form-control-has-label

6. https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html (org: W3C; read: full). Each form control needs a label that software can connect to it, with `label for` as the first technique. Related controls go in a `fieldset` with a `legend`. FAIL: yes. -> `fn-form-control-has-label`.
7. Row 2 (Mozilla). A visible label near an input is not enough. It must be tied with `label for` and a matching `id`. The click target also grows. FAIL: yes.
8. https://dequeuniversity.com/rules/axe/html/4.10/label (org: Deque; read: full). The axe rule `label` has critical impact. Fixes in order: `label for`, a wrapping `label`, then `aria-label` or `aria-labelledby`. A placeholder alone fails because it disappears when the user types. FAIL: yes. -> `fn-form-control-has-label`.
9. Row 4 (A11y Project) and row 5 (jsx-eslint `label-has-associated-control`). Connect each input to a label, group related inputs with `fieldset`. FAIL: yes.
10. https://designsystem.digital.gov/components/form/ (org: USWDS; read: full). Group related controls with `fieldset` and `legend`. It says nothing on placeholders. Topic only for the label requirement.

Notes: 5 orgs (W3C, Mozilla, Deque, A11y Project, jsx-eslint). USWDS does not count.

### fn-native-button-or-link

11. https://www.w3.org/WAI/WCAG22/Understanding/name-role-value.html (org: W3C; read: full). Every control must expose a name and a role. The page lists scripted `div` and `span` controls without a role, without a name, and without reported focus as failures. A native HTML control meets the criterion when used as specified. FAIL: yes. -> `fn-native-button-or-link`, `fn-aria-role-has-state-and-keys`.
12. Row 2 (Mozilla). A `button` gets Tab and Space or Enter for free. A `div` needs a role, `tabindex`, and an Enter handler. An `a href="#"` used as a button breaks open-in-new-tab and signals the wrong role. FAIL: yes. -> `fn-native-button-or-link`, `fn-aria-role-has-state-and-keys`.
13. https://webaim.org/techniques/keyboard/ (org: WebAIM; read: full). Native links, buttons, and fields already work by keyboard. A custom widget needs `tabindex="0"`, ARIA, and handlers for keyboard and mouse. Also covers focus indicators (row 20), tab order (row 29), and traps (row 25). FAIL: yes. -> `fn-native-button-or-link`, `fn-focus-indicator-visible`, `fn-no-positive-tabindex`, `fn-dialog-focus-managed`.
14. https://www.w3.org/WAI/ARIA/apg/practices/read-me-first/ (org: W3C; read: the opening). No ARIA is better than bad ARIA. A role changes what assistive technology reports and adds no keyboard behaviour. FAIL: yes. -> `fn-native-button-or-link`, `fn-aria-role-has-state-and-keys`.
15. Row 5 (jsx-eslint). `click-events-have-key-events` and `no-static-element-interactions` flag a clickable `div`. FAIL: yes, as a lint.
16. https://jnd.org/affordances-and-design/ (org: Norman; read: full). Designers care about perceived affordance: what users believe they can do. Actionable elements should look actionable, with labels and outlines. Topic only for the markup rule. Supports the Why. -> `fn-native-button-or-link`.

Notes: 4 orgs (W3C, Mozilla, WebAIM, jsx-eslint). Row 16 is context.

### fn-focus-indicator-visible

17. https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html (org: W3C; read: full). SC 2.4.7 (AA): a keyboard focus indicator must be visible. Failures: script that removes focus (F55) and styles that remove or hide the outline (F78). The indicator also falls under the 3:1 non-text contrast rule. FAIL: yes, `outline: none` with no replacement. -> `fn-focus-indicator-visible`.
18. https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html (org: W3C; read: full). SC 2.4.11 (AA): author content must not completely hide the focused component. The typical failure is a sticky header or footer (F110). FAIL: yes, in a rendered page. -> `fn-focus-indicator-visible`.
19. https://web.dev/learn/accessibility/focus (org: Google; read: the focus-indicator and tabindex sections). Keep the browser outline unless a replacement is equally visible. A custom indicator should not rely on colour alone and should have 3:1 contrast. The page says the indicator should not be hidden behind other components. It does not cover dialog or route focus. FAIL: yes. -> `fn-focus-indicator-visible`, `fn-no-positive-tabindex`, `mod-colour-tokens-meet-contrast`.
20. Row 13 (WebAIM). `outline:0` and `outline:none` remove the browser indicator. A custom one needs strong contrast. FAIL: yes.
21. https://www.w3.org/WAI/WCAG22/Understanding/focus-appearance.html (org: W3C; read: full). SC 2.4.13 (AAA) sets a minimum size (a 2 CSS px thick perimeter) and a 3:1 change. It is informative only. Not used as a requirement.

Notes: 4 orgs (W3C, Google, WebAIM, A11y Project via row 4). Only SC 2.4.7 and 2.4.11 are required at AA. The card does not require 2.4.13.

### fn-dialog-focus-managed

22. https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ (org: W3C; read: the keyboard and ARIA sections). On open, focus moves into the dialog. Tab and Shift+Tab wrap inside it. Escape closes it. On close, focus returns to the opener. The dialog has the `dialog` role and an accessible name. FAIL: yes, in a rendered page. -> `fn-dialog-focus-managed`.
23. https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html (org: W3C; read: full). SC 2.1.2 (A): if focus can enter a part of the page, it must be able to leave by keyboard. Confining focus in a modal is fine when there is an exit. FAIL: yes. -> `fn-dialog-focus-managed`.
24. https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog (org: Mozilla; read: full). `showModal()` makes the rest of the page inert, moves focus in, and closes on Esc. Screen readers treat it as modal. The page does not say where focus goes on close, so the card calls it out as a step to check. A dialog built from generic elements must recreate all of it. FAIL: yes, a custom dialog with no trap or no Esc. -> `fn-dialog-focus-managed`.
25. Row 13 (WebAIM). Scripts and modals can lock focus. Esc should release it, and a harder exit must be explained. FAIL: yes.
26. Row 4 (A11y Project). Remove focus from hidden elements such as closed menus or inactive modals. Partial.

Notes: 3 orgs (W3C, Mozilla, WebAIM). A11y Project is partial. The return-focus step has one org (W3C APG).

### fn-no-positive-tabindex

27. https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html (org: W3C; read: full). SC 2.4.3 (A): focus order must keep meaning and operability. A positive `tabindex` used to build an order is failure F44. FAIL: yes. -> `fn-no-positive-tabindex`.
28. Row 19 (Google). Positive values are placed first in the order, and the page advises avoiding them. `0` adds an element in DOM order. `-1` removes it from the tab order. FAIL: yes.
29. Row 13 (WebAIM). Set the order in the source and adjust layout with CSS. Avoid `tabindex` of 1 or higher. FAIL: yes.
30. Row 4 (A11y Project). Focus order should match the visual layout. Partial.

Notes: 3 orgs (W3C, Google, WebAIM). The same rule appears as the `tabindex-no-positive` lint in `eslint-plugin-jsx-a11y` (author knowledge; the README page read names only four rules) and as the axe rule `tabindex` (not fetched). The card names them as tool gates without counting them.

### fn-aria-role-has-state-and-keys

31. Row 14 (W3C APG), row 11 (W3C), row 12 (Mozilla). A role is only a promise. The author adds the state, the name, and the key handling.
32. https://inclusive-components.design/toggle-button/ (org: Heydon Pickering; read: full). Build a toggle on a native `button`. Expose state with `aria-pressed` set to an explicit `true` or `false`. Do not change the label and the pressed state together. FAIL: yes. -> `fn-aria-role-has-state-and-keys`.

Notes: 3 orgs (W3C, Mozilla, Heydon Pickering). The card lists `role-has-required-aria-props` (jsx-a11y) and `aria-required-attr` (axe) as gates from author knowledge.

### fn-status-announced-live-region

33. https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html (org: W3C; read: full). SC 4.1.3 (AA): a status message that appears without moving focus must carry a role so assistive technology announces it. `role="status"` for results and success, `role="alert"` for errors, `role="log"` for sequential updates. FAIL: yes, in a rendered page. -> `fn-status-announced-live-region`.
34. https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions (org: Mozilla; read: full). Screen readers announce changes only in a region that already exists. Put the region in the initial HTML, or defer the update. `polite` for most updates, `assertive` sparingly. `role="alert"` plus `aria-live="assertive"` can double-speak in VoiceOver on iOS. FAIL: yes. -> `fn-status-announced-live-region`.
35. https://inclusive-components.design/notifications/ (org: Heydon Pickering; read: full). Use `role="status"` with `aria-live="polite"`. Create the region before the message. Start each message with a type label such as "Error:". FAIL: yes. -> `fn-status-announced-live-region`, `fn-colour-not-sole-cue`.
36. https://www.w3.org/WAI/tutorials/forms/notifications/ (org: W3C; read: full). Link each message to its control with `aria-describedby`. Use a live region for dynamic messages. Move focus to the first field with an error after a failed submit. -> `fn-status-announced-live-region`, `fn-error-says-what-and-how`, `fn-colour-not-sole-cue`.

Notes: 3 orgs (W3C, Mozilla, Heydon Pickering). The USWDS form page (row 10) says VoiceOver on macOS does not support `role="alert"`, which is the counterpoint in the card.

### fn-heading-structure

37. https://www.w3.org/WAI/tutorials/page-structure/headings/ (org: W3C; read: full). Headings mirror the content outline. Avoid skipping levels. Returning to a higher level is fine. The page does not state a one-`h1` rule. FAIL: yes. -> `fn-heading-structure`.
38. Row 6 (W3C, technique H42: real heading markup), row 2 (Mozilla: a `span` styled as a heading gives screen reader users nothing to navigate by), row 4 (A11y Project: no skipped levels, CSS for size). FAIL: yes.

Notes: 3 orgs (W3C, Mozilla, A11y Project). The A11y Project's "one `h1`" is not in the W3C page, so the card does not require it.

### fn-colour-not-sole-cue

39. https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html (org: W3C; read: full). SC 1.4.1 (A): colour alone cannot carry information. Links in text need an underline or a 3:1 contrast with the surrounding text. Required and error states need a second cue. FAIL: yes. -> `fn-colour-not-sole-cue`.
40. https://www.nngroup.com/articles/error-message-guidelines/ (org: NN/g; read: full). Errors need bold, contrast, and icons or borders. Never rely on colour alone. Other points on placement, wording, input, and tone are in `fn-error-says-what-and-how` and `fn-keep-input-on-error`. FAIL: yes. -> `fn-colour-not-sole-cue`, `fn-error-says-what-and-how`, `fn-keep-input-on-error`.
41. https://developer.apple.com/tutorials/data/design/human-interface-guidelines/accessibility.json (org: Apple; read: full, via the JSON). Pair colour with shape, icon, or label. Contrast: 4.5:1 up to 17 pt, 3:1 for larger and bold text. Hit targets: 44 by 44 pt default on iOS, 28 minimum. Respond to Reduce Motion with fades in place of movement. Native-app guidance, so it backs the principle and not the CSS values. -> `fn-colour-not-sole-cue`, `fn-target-size`, `fn-reduced-motion-respected`, `mod-colour-tokens-meet-contrast`.
42. Row 35 (Heydon Pickering) and row 36 (W3C). A type prefix such as "Error:" or "OK:" in text.

Notes: 4 orgs (W3C, NN/g, Apple, Heydon Pickering).

### fn-target-size

43. https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html (org: W3C; read: full). SC 2.5.8 (AA): a pointer target is at least 24 by 24 CSS px. Exceptions: enough spacing (a 24 px circle on each target must not overlap another target), an equivalent control that is big enough, and targets inside a sentence. FAIL: yes, in a rendered page or from the CSS. -> `fn-target-size`.
44. Row 41 (Apple). 44 by 44 pt default, 28 minimum, and 12 pt spacing around bezelled controls. Native app, so analogous only.
45. Row 4 (A11y Project). Make targets easy to activate and space them out. No numbers.

Notes: 2 orgs (W3C firm, Apple analogous). The Material page that sets 48 dp was not readable (gap). The card stays a draft with a `note:`.

### fn-reduced-motion-respected

46. https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion (org: Mozilla; read: the first 100000 characters). `reduce` signals a request for less motion. Large scaling and panning can cause discomfort for people with vestibular disorders. Replace the animation or switch it off inside the media query. FAIL: yes. -> `fn-reduced-motion-respected`.
47. https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html (org: W3C; read: full). SC 2.3.3 (AAA): motion triggered by interaction can be turned off unless essential. Technique C39 uses `prefers-reduced-motion`. AAA, so the card cites it as the technique and not as a conformance floor. -> `fn-reduced-motion-respected`.
48. Row 41 (Apple). Respond to Reduce Motion: cut repetitive animation, soften springs, swap movement for fades.
49. Row 4 (A11y Project). Respect `prefers-reduced-motion` for all animations. Provide a way to pause background video.
50. https://web.dev/articles/cls (org: Google; read: full). Among the fixes: respect `prefers-reduced-motion`. -> `fn-reduced-motion-respected`, `svc-async-content-reserves-space`.

Notes: 5 orgs (Mozilla, W3C, Apple, A11y Project, Google). The level is AAA in WCAG, which is why the severity is `should-fix` and the card says so.

### fn-error-says-what-and-how

51. https://www.nngroup.com/articles/ten-usability-heuristics/ (org: NN/g; read: full). Heuristic 9: plain language, no codes, state the problem precisely, suggest a fix. Heuristics 1, 3, 4, 5, and 6 are used in other cards. FAIL: yes. -> `fn-error-says-what-and-how` and the cards that cite it.
52. Row 40 (NN/g error guidelines). Show the error next to the element that caused it. Name the specific problem and a next step. Avoid jargon and codes.
53. https://design-system.service.gov.uk/components/error-message/ (org: GOV.UK; read: full). Put the message directly next to its field. Say what went wrong and how to fix it. Reuse the label's wording. Do not use "please" or "sorry". Prefix with a hidden "Error:". The page says nothing about colour alone. FAIL: yes. -> `fn-error-says-what-and-how`, `fn-keep-input-on-error`, `sys-consistent-ui-terms`.
54. https://design-system.service.gov.uk/components/error-summary/ (org: GOV.UK; read: full). Show a summary whenever validation fails, move focus to it, link to each field, and prefix the page title with "Error:". Context for the card's PASS code. -> `fn-error-says-what-and-how`, `svc-page-title-per-route`.
55. https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html (org: W3C; read: full). SC 3.3.3 (AA): when the system detects an error and knows the fix, it suggests it, unless that would weaken security. FAIL: yes. -> `fn-error-says-what-and-how`.
56. Row 10 (USWDS). Place errors next to their fields so magnifier users can find them. Name each incomplete required field. Write messages that help the user fix the problem.
57. https://www.cs.umd.edu/users/ben/goldenrules.html (org: Shneiderman, University of Maryland; read: full). Rule 5: make serious mistakes hard to make. When errors happen, give specific guidance for only the faulty part. -> `fn-error-says-what-and-how`.

Notes: 5 orgs (NN/g, GOV.UK, W3C, USWDS, Shneiderman).

### fn-keep-input-on-error

58. Row 40 (NN/g). Keep what users entered so they can fix it instead of retyping. FAIL: yes, a form that resets on a failed submit.
59. Row 53 (GOV.UK error message). Do not clear entries after an error. Keep correct and incorrect answers.
60. https://design-system.service.gov.uk/patterns/validation/ (org: GOV.UK; read: full). Show the form again with the values the user entered. Validate on submit, not on blur. This is the opposite of Baymard's advice (row 61), so the card does not require a validation time.
61. https://baymard.com/blog/inline-form-validation (org: Baymard; read: full). Errors found only at submit make users search and often re-enter data that some forms clear. Inline validation on blur helps, and early validation frustrates. 31% of benchmarked sites lack inline validation. -> `fn-keep-input-on-error`.
62. Row 57 (Shneiderman). Rule 8 is about memory load, such as re-entering data between screens. Related, not the same as clearing a field.

Notes: 3 orgs firm (NN/g, GOV.UK, Baymard) plus Shneiderman as a related principle. GOV.UK says validate on submit and Baymard says validate on blur. The card takes no side.

### fn-destructive-confirm-or-undo

63. https://www.nngroup.com/articles/confirmation-dialog/ (org: NN/g; read: full). Confirmation guards serious, hard-to-reverse actions. Overuse trains people to click through. Undo is often better. Name the outcome on the buttons ("Delete file"), and do not pre-select an answer. FAIL: yes. -> `fn-destructive-confirm-or-undo`.
64. Row 51 (NN/g). Heuristic 3: give an easy way out with undo, redo, and cancel. Heuristic 5: confirm before a risky action.
65. https://developer.apple.com/tutorials/data/design/human-interface-guidelines/alerts.json (org: Apple; read: full, via the JSON). Skip an alert for a common, undoable action such as deleting a file. Use alerts for uncommon, irreversible ones. Include Cancel on a destructive alert, title it "Cancel", and do not make it the default. FAIL: yes. -> `fn-destructive-confirm-or-undo`.
66. https://www.w3.org/WAI/WCAG22/Understanding/error-prevention-legal-financial-data.html (org: W3C; read: full). SC 3.3.4 (AA): a page that creates legal or financial commitments, deletes user data, or submits a test must be reversible, checked, or confirmed. FAIL: yes. -> `fn-destructive-confirm-or-undo`.
67. Row 57 (Shneiderman). Rule 6: make actions reversible, a single action or a group.
68. https://jnd.org/books/the-design-of-everyday-things-revised-and-expanded-edition/ (org: Norman; read: the table of contents). Chapter 5 covers slips and mistakes, designing for error, and undo. A table of contents only, so topic only.

Notes: 4 orgs (NN/g, Apple, W3C, Shneiderman). Norman is topic only.

## 2. Module level

### mod-colour-tokens-meet-contrast

69. https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html (org: W3C; read: full). SC 1.4.3 (AA): normal text 4.5:1, large text (18 pt, or 14 pt bold) 3:1. Measured on the specified colours, not rounded: 4.499:1 fails. Logos and inactive controls are exempt. FAIL: yes, computed from the token pair. -> `mod-colour-tokens-meet-contrast`.
70. https://dequeuniversity.com/rules/axe/html/4.10/color-contrast (org: Deque; read: full). The axe rule `color-contrast` checks the same thresholds. It cannot judge text on a background image, gradients, or overlapped elements, so those need a manual look. FAIL: yes, with that limit. -> `mod-colour-tokens-meet-contrast`.
71. Row 4 (A11y Project). 4.5:1 normal text, 3:1 large text, icons, and input borders.
72. Row 41 (Apple). Same ratios for text. Check both light and dark appearance, and offer a higher-contrast palette.
73. https://www.w3.org/WAI/test-evaluate/preliminary/ (org: W3C; read: full). A quick check that text stands out, with 4.5:1 for normal text. Also used in rows for keyboard, zoom, and the audit card.
74. Rows 19 and 71: a focus indicator needs 3:1, and so do icons and input borders.

Notes: 5 orgs (W3C, Deque, A11y Project, Apple, Google). The non-text 3:1 rule (SC 1.4.11) was not read as its own page. It is cited through rows 4, 17, and 19.

## 3. Service level

### svc-no-redundant-entry

75. https://www.w3.org/WAI/WCAG22/Understanding/redundant-entry.html (org: W3C; read: full). SC 3.3.7 (A): in one process, information the user already entered must be auto-populated or selectable. Exceptions: essential re-entry, security (retyping a new password), and data that is no longer valid. Browser autofill does not count. FAIL: yes, in a rendered flow. -> `svc-no-redundant-entry`.
75a. Row 51 (NN/g). Heuristic 6: make options and information visible so users need not carry details from one screen to another.
75b. Row 57 (Shneiderman). Rule 8 reduces memory load, with re-entering data as the example.

Notes: 3 orgs (W3C, NN/g, Shneiderman).

### svc-slow-operation-shows-progress

76. https://www.nngroup.com/articles/response-times-3-important-limits/ (org: NN/g; read: full). Past about 1 second, show that the system is working. Past about 10 seconds, show a percent-done indicator and a way to interrupt. If the total is unknown, show running progress. A spinner is the last resort. FAIL: yes, a long action with no indicator. -> `svc-slow-operation-shows-progress`.
77. https://www.nngroup.com/articles/skeleton-screens/ (org: NN/g; read: full). Skeleton screens suit full-page loads up to about 10 seconds. Spinners suit 2 to 10 seconds. Progress bars suit longer waits. None for pages under 1 second. The page does not discuss layout shift. -> `svc-slow-operation-shows-progress`, `svc-async-content-reserves-space`.
78. https://developer.apple.com/tutorials/data/design/human-interface-guidelines/progress-indicators.json (org: Apple; read: full, via the JSON). Use a determinate indicator when you can. Keep it moving. Say what is happening, not "loading". Offer Cancel when stopping is safe. FAIL: yes. -> `svc-slow-operation-shows-progress`.
79. Row 57 (Shneiderman). Rule 3: feedback for every action, modest for minor ones and substantial for major ones. Rule 4 asks for a clear end to a group of actions.
80. Row 33 (W3C 4.1.3). Progress needs a role so assistive technology announces it (`role="log"` or a progress bar with a live region).
81. https://developer.apple.com/tutorials/data/design/human-interface-guidelines/feedback.json (org: Apple; read: full, via the JSON). Show status near the item it describes. Explain why a command cannot run. Confirm significant tasks only. Use more than one channel. -> `svc-slow-operation-shows-progress`, `fn-colour-not-sole-cue`.

Notes: 4 orgs (NN/g, Apple, Shneiderman, W3C). Norman's feedback principle is topic only (row 68 table of contents and row 16).

### svc-async-content-reserves-space

82. Row 50 (web.dev CLS; org: Google; read: full). CLS of 0.1 or less is good, over 0.25 is poor, measured at the 75th percentile. Causes: media with no dimensions, late fonts, ads, and content inserted above existing content. For a user-triggered wait, reserve the space and show a loading indicator. Animate with `transform`. FAIL: yes, `<img>` with no dimensions, or a banner injected above content. -> `svc-async-content-reserves-space`.
83. https://developer.apple.com/tutorials/data/design/human-interface-guidelines/loading.json (org: Apple; read: full, via the JSON). Show placeholders at once and swap in real content as it arrives. Says nothing about layout jumps. Indirect. -> `svc-async-content-reserves-space`.
84. Row 77 (NN/g). A skeleton mirrors the final page structure, so users know where content will appear. Indirect.

Notes: 1 org firm (Google), 2 indirect. The MDN glossary page for CLS returned 404, so there is no second firm source. The card stays a draft with a `note:`.

### svc-reflow-and-zoom

85. https://www.w3.org/WAI/WCAG22/Understanding/reflow.html (org: W3C; read: full). SC 1.4.10 (AA): no two-way scroll and no lost content at 320 CSS px wide. Exceptions: maps, data tables, diagrams, toolbars that must stay visible. A table gets its own scroll container. FAIL: yes, in a rendered page at a 320 px viewport. -> `svc-reflow-and-zoom`.
86. https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html (org: W3C; read: full). SC 1.4.4 (AA): text enlarges to 200% with no clipping. Failures: clipped content (F69), non-resizing form controls (F80), misused viewport units (F94). FAIL: yes. -> `svc-reflow-and-zoom`.
87. https://dequeuniversity.com/rules/axe/html/4.10/meta-viewport (org: Deque; read: full). The axe rule `meta-viewport` flags `user-scalable=no` and a `maximum-scale` under 2. Critical impact for low-vision users. FAIL: yes, in markup. -> `svc-reflow-and-zoom`.
88. Row 73 (W3C quick checks). Enlarge text to 200% and check that nothing overlaps or gets cut off.

Notes: 2 orgs (W3C, Deque). The WebAIM and GOV.UK pages on zoom were not read.

### svc-page-title-per-route

89. https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html (org: W3C; read: full). SC 2.4.2 (A): every page has a title that describes its topic or purpose. A single-page app updates the title as the view changes. FAIL: yes. -> `svc-page-title-per-route`.
90. Row 4 (A11y Project). Give each page or view a unique `title`. Avoid the `title` attribute for important information.
91. Row 54 (GOV.UK). Prefix the page title with "Error:" when the page shows errors. A special case of the same rule.
92. Row 10 and 56 (USWDS). Add an error notice to the page title.

Notes: 2 orgs for the core rule (W3C, A11y Project), 4 for the error-prefix variant. The card requires the unique, current title, and cites the error prefix as the PASS example. The `lang` rule (SC 3.1.1, https://www.w3.org/WAI/WCAG22/Understanding/language-of-page.html, W3C: declare the page language with `lang` on `html`) was read but has one more org at most (A11y Project, row 4), so it has no card of its own.

## 4. System level

### sys-consistent-ui-terms

93. Row 51 (NN/g). Heuristic 4: users should not wonder whether different words or actions mean the same thing. Follow platform conventions. FAIL: yes, across screens. -> `sys-consistent-ui-terms`.
94. Row 57 (Shneiderman). Rule 1: consistent actions, terms, and design for similar situations, with a few clear exceptions.
95. https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html (org: W3C; read: full). SC 3.2.4 (AA): a component with the same function is identified the same way across related pages. Wording may shift slightly. FAIL: yes.
96. https://www.gov.uk/guidance/government-design-principles (org: GOV.UK; read: the consistency principle). Principle 9: be consistent, not uniform. Same language and patterns where you can, a coherent approach where you cannot. -> `sys-consistent-ui-terms`.
97. Row 53 (GOV.UK). Reuse the label's wording in the error message and use the same message in the field and the summary.

Notes: 4 orgs (NN/g, Shneiderman, W3C, GOV.UK). The code-name equivalent is `mod-one-name-per-concept`, and the API one is `svc-api-naming-consistent`. This card is about the words and controls a user sees.

## 5. Codebase level

### code-a11y-check-in-ci

98. Row 5 (jsx-eslint). The plugin lints JSX for accessibility problems. It has partial coverage by design. FAIL: yes, no lint or check configured. -> `code-a11y-check-in-ci`.
99. https://www.deque.com/axe/core-documentation/ (org: Deque; read: the hub page). Lists CI/CD as an integration. No percentage, and no statement about manual testing. Weak. -> `code-a11y-check-in-ci`.
100. https://alphagov.github.io/accessibility-tool-audit/ (org: GOV.UK; read: the summary). GDS planted 142 barriers on a page and ran 13 automated tools. The best found 40%, the worst 13%. Counting items that need a human judgment, the best reached 50%. -> `code-a11y-check-in-ci`, `chg-ui-change-screenshots-and-keyboard-pass`.
101. https://www.gov.uk/service-manual/helping-people-to-use-your-service/making-your-service-accessible-an-introduction (org: GOV.UK; read: full). WCAG 2.2 AA is the minimum. Combine automated and manual tests each time a feature is built. An audit before public beta is required. No automated-coverage figure. -> `code-a11y-check-in-ci`, `chg-ui-change-screenshots-and-keyboard-pass`, `prod-a11y-audit-before-launch`.
102. https://www.section508.gov/test/ (org: Section508.gov; read: full). Validation can be automated, manual, or hybrid. The page does not explain tool limits or mention keyboard testing. Topic only for the CI rule.

Notes: 3 orgs (jsx-eslint, Deque weak, GOV.UK). Because the best tool finds 40% of planted barriers, the card asks for the gate and says it does not replace the manual pass in `chg-ui-change-screenshots-and-keyboard-pass`.

## 6. Change level

### chg-ui-change-screenshots-and-keyboard-pass

103. Row 73 (W3C quick checks). Tab through every link, field, button, and media control. Check the focus highlight. Enlarge text to 200%. These are a rough first pass, not an evaluation. FAIL: yes, a UI change with no record of the pass. -> `chg-ui-change-screenshots-and-keyboard-pass`.
104. Row 13 (WebAIM). Keyboard behaviour in detail: focus indicators, tab order, custom controls, skip links, traps.
105. Row 101 (GOV.UK). Test with automated and manual checks each time a feature is built.
106. Row 102 (Section508.gov). Manual testing is one of three approaches. Topic only.
107. Before-and-after screenshots in a review: first-hand practice of this repo's authors. No primary source was read for it, so the card says so in `note:`.

Notes: 3 orgs for the keyboard and zoom pass (W3C, WebAIM, GOV.UK). 0 for the screenshots.

## 7. Production level

### prod-a11y-audit-before-launch

108. Row 101 (GOV.UK). The service must work with common assistive technology: screen magnifiers, screen readers, speech recognition. An accessibility audit must show that it does before public beta. A department auditor or an external specialist can do it. FAIL: yes, a launch with no audit report. -> `prod-a11y-audit-before-launch`.
109. Row 73 (W3C). The quick checks are not a full evaluation. A page can pass them and still have significant barriers. Professionals should assess.
110. Row 100 (GOV.UK audit). Automated tools alone miss most barriers.
111. Row 102 (Section508.gov). Conformance can be automated, manual, or hybrid. The ICT Testing Baseline aims for consistent results. Weak.

Notes: 3 orgs (GOV.UK, W3C, Section508 weak). The law cited by GOV.UK is a UK duty, so the card names WCAG 2.2 AA as the standard and does not claim a legal obligation elsewhere.

## 8. Which levels have a new card

- change: `chg-ui-change-screenshots-and-keyboard-pass`.
- function: `fn-img-alt-text`, `fn-form-control-has-label`, `fn-native-button-or-link`, `fn-focus-indicator-visible`, `fn-dialog-focus-managed`, `fn-no-positive-tabindex`, `fn-aria-role-has-state-and-keys`, `fn-status-announced-live-region`, `fn-heading-structure`, `fn-colour-not-sole-cue`, `fn-target-size`, `fn-reduced-motion-respected`, `fn-error-says-what-and-how`, `fn-keep-input-on-error`, `fn-destructive-confirm-or-undo`.
- module: `mod-colour-tokens-meet-contrast`. A "component requires an accessible name" card was left out, because `fn-form-control-has-label` and `fn-native-button-or-link` already fail the same call site.
- service: `svc-no-redundant-entry`, `svc-slow-operation-shows-progress`, `svc-async-content-reserves-space`, `svc-reflow-and-zoom`, `svc-page-title-per-route`.
- system: `sys-consistent-ui-terms`.
- codebase: `code-a11y-check-in-ci`.
- production: `prod-a11y-audit-before-launch`.
- incident: none. No source describes an accessibility-specific incident review.

## 9. Read, not used, or not read

- Dropped: an empty-state card. Only NN/g (https://www.nngroup.com/articles/empty-state-interface-design/, read: full) backs it: say what state the system is in, and offer a next action. One org, so it stays out of the cards and in `docs/COVERAGE.md`.
- Dropped: a page-language card (see the note under `svc-page-title-per-route`).
- Dropped: "no autoplaying media" and "captions". Not researched in this pass.
- Not read: Material Design, Refactoring UI, Steve Krug, the WAI-ARIA patterns other than the modal dialog, the WCAG 1.4.11 and 2.5.7 pages, and the USWDS accessibility pages.
- Weak points to fix before a stable pass: a second firm org for `svc-async-content-reserves-space`, a Material or Chrome source for `fn-target-size`, and a primary source for before-and-after screenshots.

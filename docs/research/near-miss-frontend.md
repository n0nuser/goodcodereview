# Near-miss sources: a third org for eight frontend cards

Fetched 2026-10-24 through WebFetch (a small model summarises the page), so every row is paraphrase. Pages from one org count once. A source counts only if it backs the Rule line. Style follows `second-pass.md`: URL, distilled point, the card whose Rule it backs.

## fn-target-size (2 orgs -> 4)
1. https://dequeuniversity.com/rules/axe/html/4.10/target-size (Deque). Targets are at least 24 by 24 CSS px, or a 24 px circle on each undersized target must touch no other target. Maps to WCAG 2.5.8 AA. Backs both halves of the Rule.
2. https://developer.mozilla.org/en-US/docs/Web/Accessibility/Guides/Understanding_WCAG/Operable (Mozilla). 2.5.8 lists the 24 px floor and the spacing exception, plus equivalent, inline, user-agent and essential exceptions. Backs the Rule and the Counterpoint.
3. https://web.dev/articles/accessible-tap-targets (Google). Recommends about 48 px with about 8 px spacing. Does not back 24 px; it is stricter. Not added to `borrowed_from`.

## svc-async-content-reserves-space (1 firm org -> 3)
4. https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/img (Mozilla). Set `width` and `height` so the browser reserves space and avoids layout shift; more important for lazy-loaded images. Backs the Rule.
5. https://developer.mozilla.org/en-US/docs/Glossary/CLS (Mozilla, same org). `img` and `video` without dimensions cause shift; set the attributes. Does not cover ads or injected content.
6. https://html.spec.whatwg.org/multipage/embedded-content.html (WHATWG). Advises `width` and `height` on lazy-loaded images so layout does not shift. Narrower than the Rule: images only, and only the lazy-loaded case was read.

Not enough: the MDN `Cumulative_layout_shift` guide URL returned 404; the MDN lazy-loading and `aspect-ratio` pages do not state the rule. Nothing found outside Google for ads and injected banners.

## svc-page-title-per-route (2 orgs -> 4)
7. https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/title (Mozilla). Titles should be unique and descriptive; its example updates the title on a state change ("2 errors - ..."). Says screen readers do not announce a title change by themselves. It does not name SPAs.
8. https://dequeuniversity.com/rules/axe/html/4.10/document-title (Deque). Every document needs a non-empty, descriptive `title` (WCAG 2.4.2). Backs only that a title exists, not per-route updates.
9. https://www.w3.org/WAI/WCAG22/Understanding/page-titled.html (W3C, re-read). In a single-page app the title changes with the view.

## code-a11y-check-in-ci (3 orgs, one weak -> 5)
10. https://designsystem.digital.gov/documentation/accessibility/ (USWDS). Runs pa11y and axe on every code change and blocks failing merges; also tests by hand. Strongest CI source.
11. https://www.gov.uk/service-manual/helping-people-to-use-your-service/testing-for-accessibility (GOV.UK). Automated alone misses issues; test regularly during development. Does not mention a CI pipeline.
12. https://playwright.dev/docs/accessibility-testing (Microsoft). Examples assert zero axe violations, so a violation fails the test. Says automation cannot detect all WCAG failures. No CI text.
13. https://github.com/dequelabs/axe-core (Deque). Claims about 57% of WCAG issues found; marks undecidable cases "incomplete"; fits existing functional tests. Better than the docs hub row for Deque.

Not enough: the Lighthouse scoring page (Google) does not say automation is partial. The W3C tool-selection page says no tool alone can decide conformance but never names CI.

## chg-ui-change-screenshots-and-keyboard-pass (keyboard 3 orgs; screenshots none -> 3 practice sources)
14. https://raw.githubusercontent.com/WordPress/gutenberg/trunk/.github/PULL_REQUEST_TEMPLATE.md (WordPress). Before/after screenshots section (optional); keyboard-only testing instructions required for UI changes.
15. https://raw.githubusercontent.com/elastic/eui/main/.github/pull_request_template.md (Elastic). Before/after table; checklist asks for keyboard-only, screen reader and forced-colors testing.
16. https://raw.githubusercontent.com/mozilla/addons-frontend/master/.github/PULL_REQUEST_TEMPLATE.md (Mozilla). Before/after screenshots for UI-affecting changes only.

Caveat: these are single-project PR templates, not standards guidance, and none mentions a 200% zoom check (only W3C's quick checks do). Checked with no match: GOV.UK frontend (404), Primer docs, MDN content, Fluent UI, VS Code, USWDS templates.

## prod-a11y-audit-before-launch (2 firm + 1 weak -> 3)
17. https://www.deque.com/web-accessibility-beginners-guide/ (Deque). Manual testing with assistive technology is central; automated scans are only a first check; recommends a full audit by experts. No timing, so no "before launch".
18. https://www.w3.org/WAI/test-evaluate/ (W3C). No tool alone decides conformance; WCAG-EM and a report tool for formal evaluation; involve users with disabilities.

Not enough: the Section508.gov test page makes no assistive-technology or pre-release requirement; the WebAIM services page describes an audit with a report but no assistive technology; Accessibility Insights targets WCAG 2.1, not 2.2; the Australian DTA pages timed out.

## fn-aria-role-has-state-and-keys (W3C + 2 each clause -> 3 or more each)
19. https://www.w3.org/WAI/ARIA/apg/patterns/switch/ (W3C). Switch toggles on Space (Enter optional); `aria-checked` reflects state.
20. https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Roles/switch_role (Mozilla). `aria-checked` required on `role="switch"`; must be focusable and keyboard accessible; author updates the state.
21. https://dequeuniversity.com/rules/axe/html/4.10/aria-required-attr (Deque). Widget roles need their required states (`aria-checked`, `aria-expanded`...); critical, WCAG 4.1.2. Does not map switch to `aria-checked` itself.
22. https://web.dev/learn/accessibility/aria-html (Google). ARIA changes no behaviour; you add the keyboard code. Silent on keeping state current.

Counts: state clause W3C, Mozilla, Deque (plus Heydon Pickering); keys clause W3C, Mozilla, Google.

## fn-no-raw-html-sink (OWASP only -> 4)
23. https://developer.mozilla.org/en-US/docs/Web/API/Element/innerHTML (Mozilla). `innerHTML` is an injection sink; use `textContent` for plain text; sanitize otherwise.
24. https://react.dev/reference/react-dom/components/common (Meta). `dangerouslySetInnerHTML` is XSS-prone with untrusted data; only trusted, sanitized HTML.
25. https://angular.dev/best-practices/security (Google). Values are escaped by default; `bypassSecurityTrust` skips that and risks XSS.
26. https://github.com/mozilla/eslint-plugin-no-unsanitized (Mozilla, same org). Rules `property` and `method` flag `innerHTML` and `insertAdjacentHTML` with non-literal values. Confirms the tool_gate names.

Not used: web.dev Trusted Types recommends sanitizing and Trusted Types, not `textContent`.

## Findings
- `svc-async-content-reserves-space`: the Rule covers ads and injected banners, but the Mozilla and WHATWG sources cover only media dimensions. Only Google backs the injected-content half.
- `prod-a11y-audit-before-launch`: "before a public launch" is stated only by GOV.UK. Deque and W3C back the audit content, not the timing.
- `chg-ui-change-screenshots-and-keyboard-pass`: the 200% zoom clause rests on W3C alone; the screenshot clause rests on three project templates.
- `fn-target-size`: no Rule problem; Apple and Google ask for more than 24 px.

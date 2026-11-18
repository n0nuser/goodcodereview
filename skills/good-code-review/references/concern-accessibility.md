# accessibility cards

Every stable card that lists the `accessibility` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-ui-change-screenshots-and-keyboard-pass` [should-fix] {accessibility, usability, process} <ui> change.md:L754+31: A UI change shows before-and-after screenshots and says what a keyboard-only pass and a 200% zoom check found on the changed screens.

## function

- `fn-aria-role-has-state-and-keys` [should-fix] {accessibility} <ui> function.md:L3+30: When a native element cannot do the job, give the custom widget the state attribute and the keys its role promises.
- `fn-colour-not-sole-cue` [should-fix] {accessibility, usability} <ui> function.md:L97+30: Pair every colour that carries meaning with a second cue: text, an icon, a shape, or an underline.
- `fn-dialog-focus-managed` [block] {accessibility, usability} <ui> function.md:L339+33: When a modal opens, move focus into it and keep Tab inside it. Make Escape close it. When it closes, return focus to the control that opened it or, if it is gone, to the next logical control.
- `fn-error-says-what-and-how` [should-fix] {usability, accessibility} <ui> function.md:L502+30: Show each validation error next to its field, in plain words that name what is wrong and how to fix it.
- `fn-focus-indicator-visible` [block] {accessibility, usability} <ui> function.md:L563+27: Keep a visible focus indicator on every focusable element. Never set `outline: none` without a replacement.
- `fn-form-control-has-label` [block] {accessibility, usability} <ui> function.md:L591+31: Tie every form control to a visible `<label>`, with `for` and a matching `id` or by wrapping it. A placeholder is not a label.
- `fn-heading-structure` [should-fix] {accessibility, usability} <ui> function.md:L724+31: Mark every heading with a real `<h1>` to `<h6>` element, not a styled `div`, `span`, or `p`.
- `fn-img-alt-text` [should-fix] {accessibility} <ui> function.md:L756+31: Give every `<img>` an `alt` attribute: text that serves the image's purpose, or `alt=""` when the image is decorative.
- `fn-label-above-field` [discuss] {usability, accessibility} <ui> function.md:L909+31: Put the visible label of a text input, select, or textarea directly above it.
- `fn-native-button-or-link` [block] {accessibility, usability} <ui> function.md:L1071+30: Use `<button>` for an action and `<a href>` for navigation. Do not attach a click handler to a `div`, `span`, or `a` with no `href`.
- `fn-no-positive-tabindex` [should-fix] {accessibility, usability} <ui> function.md:L1374+31: Write the DOM in reading order and never set `tabindex` above 0.
- `fn-reduced-motion-respected` [should-fix] {accessibility, usability} <ui> function.md:L1654+33: Switch off or replace large, repeating, or interaction-triggered motion when `prefers-reduced-motion: reduce` is set.
- `fn-related-controls-in-fieldset` [should-fix] {accessibility, usability} <ui> function.md:L1718+35: Wrap each radio group, checkbox group, and other set of related controls, such as day, month, and year, in a `<fieldset>` with a `<legend>` that names the group, often as the question.
- `fn-status-announced-live-region` [should-fix] {accessibility, usability} <ui> function.md:L1846+31: Announce an async status message through a live region (`role="status"` or `role="alert"`), and put a `role="status"` or `aria-live` region in the markup before its text changes.
- `fn-target-size` [should-fix] {accessibility, usability} <ui> function.md:L1878+30: Make each pointer target at least 24 by 24 CSS pixels, or space it so that a 24 px circle centred on it touches no other target and no other undersized target's circle.

## module

- `mod-colour-tokens-meet-contrast` [should-fix] {accessibility, usability} <ui> module.md:L88+38: Make every text and background token pair meet 4.5:1 (3:1 for large text, which is 18pt, or 14pt bold), and every border, icon, and focus colour meet 3:1 against its neighbour.

## service

- `svc-no-redundant-entry` [should-fix] {usability, accessibility} <ui> service.md:L1363+29: Do not ask for information the user already gave in the same flow. Fill it in, or let the user pick it.
- `svc-reflow-and-zoom` [should-fix] {accessibility, usability} <ui> service.md:L1526+37: Make the page usable at 320 CSS pixels wide and at 200% text zoom, with no sideways scrolling, no clipped content, and no blocked pinch-zoom.
- `svc-slow-operation-shows-progress` [should-fix] {usability, accessibility} <ui> service.md:L1738+30: Show that a slow action is under way, and show its progress when it runs long.

## system

- `sys-consistent-ui-terms` [discuss] {usability, accessibility} <ui> system.md:L90+29: Use one label and one icon for the same action and the same concept across all screens.

## codebase

- `code-a11y-check-in-ci` [should-fix] {accessibility, testing} <ui> codebase.md:L3+30: Run an automated accessibility check, such as axe on rendered pages, in the automated tests, and fail the test on a violation.

## production

- `prod-a11y-audit-before-launch` [should-fix] {accessibility, usability} <ui> production.md:L3+30: Before a public launch, run an accessibility audit against WCAG 2.2 AA that includes assistive technology, and link the report in the launch checklist.

---
id: fn-dialog-focus-managed
level: function
tags: [accessibility, usability, frontend, keyboard]
severity: block
status: stable
lang: core
applies_when: A component opens a modal dialog, drawer, or menu that covers the page.
tool_gate: none; a component test that opens the dialog, presses Tab and Escape, and asserts `document.activeElement`.
note: Focus into the modal, Tab kept inside: W3C APG, Mozilla, GitHub (Primer). Escape and return focus to the opener are in W3C APG and WebAIM; MDN does not state return focus, so that part is in Why
borrowed_from:
  - https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/
  - https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html
  - https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/dialog
  - https://webaim.org/techniques/keyboard/
  - https://primer.style/product/components/dialog/accessibility
---

**Rule.** When a modal opens, move focus into it and keep Tab inside it. Make Escape close it.

**Why.** Without it, a keyboard user keeps tabbing through the page behind the dialog, or gets stuck inside it with no exit. When it closes, return focus to the control that opened it. Focus that falls to the top of the page makes them start over.

**FAIL**

```jsx
{open && <div className="modal"><h2>Delete?</h2><button onClick={del}>Delete</button></div>}
```

**PASS**

```html
<button id="opener">Delete project</button>
<dialog id="dlg" aria-labelledby="t"><h2 id="t">Delete project?</h2>
  <button autofocus>Cancel</button> <button>Delete</button></dialog>
<script>
  const opener = document.getElementById("opener"), dlg = document.getElementById("dlg");
  opener.onclick = () => dlg.showModal();   // focus moves in, page behind is inert
  dlg.onclose = () => opener.focus();       // focus returns to the opener
</script>
```

**Counterpoint.** "Our library handles it." Check, because a library that traps focus but never restores it is common. Prefer the native `<dialog>` with `showModal()`, which makes the page inert and closes on Escape. A dialog built from generic elements must recreate each of those.

# UX laws pass: sources for three form and layout cards

Fetched 2026-10-25 with `curl`, tags stripped, then searched for each quote. The leads came from a social-media list of UX laws, so they are leads, not sources. Every row below is a page I opened. Quotes are 15 words or fewer. Org counting follows `docs/research/frontend-pass.md`: one organisation counts once, whatever the number of pages.

Fetch notes. The w3.org pages sometimes answered a browser User-Agent with a Cloudflare challenge, so they were fetched with plain `curl`. A later fetch with a browser User-Agent got the full pages. Apple HIG, Material, and IBM Carbon pages returned script shells or empty bodies and back nothing here.

## Label placement

| URL | Org | Year | Paraphrase | Backs |
|---|---|---|---|---|
| https://design-system.service.gov.uk/components/text-input/ | GOV.UK | not shown | Align labels above the text input they refer to. Do not use a placeholder as a label. | Rule, text fields |
| https://atlassian.design/components/textfield/usage | Atlassian | not shown | The label is left-aligned "directly above the input area". | Rule, text fields |
| https://www.nngroup.com/articles/web-form-design/ | NN/g | 2016 | Keep labels close to their fields: above for mobile and short desktop forms, beside for very long desktop forms. Avoid labels equidistant from two fields. | Rule, text fields; Counterpoint |
| https://www.w3.org/WAI/tutorials/forms/labels/ | W3C | 2024 | Convention puts labels right of radio buttons and checkboxes, and left of or above other fields. Above cuts sideways scrolling, but the choice "needs to be assessed individually". | Rule, text fields; Why (checkbox and radio order); Counterpoint |

Count: 4 orgs for "above a text field", with NN/g and W3C also allowing a side label. 1 org (W3C) for the checkbox and radio order. The checkbox and radio order sits in Why. Decision: draft `fn-label-above-field`, severity `discuss`, because W3C refuses a blanket rule.

Correction to the brief. The retrieval report and the brief said a checkbox or radio label goes "to its left". W3C says the label goes to the right of the control. The card puts the control to the left of its label.

## Grouping related fields

| URL | Org | Year | Paraphrase | Backs |
|---|---|---|---|---|
| https://design-system.service.gov.uk/components/fieldset/ | GOV.UK | not shown | Use a fieldset to show a relationship between several inputs. Its first element must be a legend. | Rule |
| https://design-system.service.gov.uk/components/date-input/ | GOV.UK | not shown | The date input example wraps day, month, and year in a fieldset with a legend. | Rule, multi-part values |
| https://www.w3.org/WAI/tutorials/forms/grouping/ | W3C | 2026 | Group "visually and in the code". Radio groups should always use a fieldset. The legend acts as the group's heading. | Rule; Why |
| https://designsystem.digital.gov/components/form/ | USWDS | not shown | Put each set of related controls in a fieldset, labelled by a legend. VoiceOver on iOS does not support them, so add `aria-labelledby`. | Rule; Counterpoint |
| https://www.a11yproject.com/checklist/ | The A11y Project | not shown | Use fieldset and legend where appropriate. | Rule |
| https://www.nngroup.com/articles/web-form-design/ | NN/g | 2016 | Section a form that asks about two topics into groups and tag the groups for screen readers. Does not name fieldset. | Topic only |
| https://www.nngroup.com/articles/gestalt-proximity/ | NN/g | 2020 | Close elements read as related. Groupings can shift in responsive layouts. | Topic only |
| https://lawsofux.com/law-of-proximity/ | Laws of UX | not shown | States the law of proximity. No instruction. | Topic only |

Count: 4 orgs (GOV.UK, W3C, USWDS, A11y Project). No page gives a spacing number or ratio, so spacing stays out of the Rule. Decision: draft `fn-related-controls-in-fieldset`.

Merge check. One Rule cannot state both label placement and fieldset grouping honestly. They have different org counts, different severities, and one is visual while the other is markup. They stay two cards.

Overlap check. `fn-form-control-has-label` cites W3C and USWDS on fieldset in its research rows but its Rule and examples cover single labels only. No card states either rule (`rg -il 'fieldset|legend|label.*above' cards glossary`).

## Progressive disclosure

| URL | Org | Year | Paraphrase | Backs |
|---|---|---|---|---|
| https://www.nngroup.com/articles/progressive-disclosure/ | NN/g | 2006 | Show up front everything users often need. Designs past two disclosure levels "typically have low usability". | Rule, both parts |
| https://design-system.service.gov.uk/components/details/ | GOV.UK | not shown | Use details for what only some users need. Do not hide what most users need. | Rule, first part |
| https://docs.appian.com/suite/help/26.9/sail/ux-progressive-disclosure.html | Appian | v26.9 | The interface must work if the user never reveals the hidden items. In a step-by-step flow, disable fields that are not ready instead of hiding them. | Rule, first part; Counterpoint |
| https://primer.style/product/ui-patterns/progressive-disclosure/ | GitHub Primer | not shown | Use disclosure "sparingly", only when truncation is necessary. | Topic only |
| https://learn.microsoft.com/en-us/windows/win32/uxguide/ctrl-progressive-disclosure-controls | Microsoft | Windows 7 era | Rules on disclosure controls (no links, arrow shapes). The page says it was written for Windows 7. | Topic only |

Count: 3 orgs (NN/g, GOV.UK, Appian) for "do not hide what most users need". 1 org (NN/g) for the two-level cap. The cap sits in Why, worded the way NN/g counts levels (the first view is level one). Decision: draft `fn-disclosure-hides-only-secondary`.

## Leads dropped after research

### Recognition over recall

| URL | Org | Year | Paraphrase |
|---|---|---|---|
| https://www.nngroup.com/articles/ten-usability-heuristics/ | NN/g | not shown | Heuristic 6: show information in the interface rather than make people remember it. |
| https://www.nngroup.com/videos/recognition-vs-recall/ | NN/g | not shown | Recognition is easier than recall because it has more cues. |
| https://www.w3.org/WAI/WCAG22/Understanding/consistent-identification.html | W3C | WCAG 2.2 | Name components with the same function the same way across pages. Covers label consistency, not showing options. |

Count: 2 orgs, and W3C covers only part. Decision: dropped, under 3 orgs.

### Feedback within a time budget

| URL | Org | Year | Paraphrase |
|---|---|---|---|
| https://www.nngroup.com/articles/progress-indicators/ | NN/g | not shown | Always give immediate feedback. Show a progress indicator for actions over about one second. |
| https://www.nngroup.com/articles/response-times-3-important-limits/ | NN/g | not shown | Limits at 0.1 s, 1 s, and 10 s. Past 10 s, tell users when the work will finish. |
| https://lawsofux.com/doherty-threshold/ | Laws of UX | not shown | Gives a 400 ms target for system feedback. |
| https://learn.microsoft.com/en-us/windows/apps/design/controls/progress-controls | Microsoft | not shown | Pick determinate or indeterminate progress by whether the duration is known. Some tasks need none. |
| https://newsletter.kentbeck.com/p/the-precious-eyeblink | Kent Beck | not shown | Says no research shows attention slipping at exactly 400 ms. |

Decision: dropped. Stable `svc-slow-operation-shows-progress` already covers waits. The 400 ms figure has no primary source behind it, and Kent Beck disputes it.

### Hick's law

| URL | Org | Year | Paraphrase |
|---|---|---|---|
| https://lawsofux.com/hicks-law/ | Laws of UX | not shown | Minimise choices when response time is critical. |
| https://design-system.service.gov.uk/components/select/ | GOV.UK | not shown | Treat select as a last resort. Ask questions that leave fewer options. |
| https://baymard.com/blog/drop-down-usability | Baymard | not shown | Avoid drop-downs with more than 10 or fewer than 5 options, in e-commerce checkout only. |
| https://www.interaction-design.org/literature/topics/hick-s-law | Interaction Design Foundation | not shown | Decision time grows with the log of the number of choices. Matters most for short lists. |
| https://www.smashingmagazine.com/2012/02/23/redefining-hicks-law/ | Smashing Magazine | 2012 | Calls the usual "fewer menu items" reading oversimplified. |

Decision: dropped. No source gives a count a reviewer can apply outside Baymard's checkout drop-down range.

### Fitts's law

| URL | Org | Year | Paraphrase |
|---|---|---|---|
| https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html | W3C | WCAG 2.2 | AAA level: targets at least 44 by 44 CSS px. |
| https://developer.apple.com/design/tips/ | Apple | not shown | Controls at least 44 by 44 pt. |
| https://support.google.com/accessibility/android/answer/7101858?hl=en | Google | not shown | Touch targets at least 48 by 48 dp, 8 dp apart. |
| https://learn.microsoft.com/en-us/windows/apps/design/input/touch-interactions | Microsoft | not shown | Touchable means at least 40 by 40 epx. |
| https://www.nngroup.com/articles/touch-target-size/ | NN/g | 2019 | Touch targets at least 1 cm by 1 cm. |

Decision: dropped. Stable `fn-target-size` already sets the 24 by 24 CSS px floor from WCAG 2.5.8 and its Counterpoint names the larger platform numbers. None of these pages backs the 24 px Rule, so none was added to its `borrowed_from`.

## Leads excluded before research

- Aesthetic-usability effect, peak-end rule, goal-gradient effect, serial position effect, Von Restorff effect, Tesler's law: not reviewable in code or config.
- Miller's law: weak. The "7 plus or minus 2" figure is overstated when applied to interface lists.
- Postel's law: contested. RFC 9413 argues against tolerant input handling in protocols.

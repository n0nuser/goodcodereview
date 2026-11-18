# Source pilot: function level

Pilot of 5 source pages against the function-level cards. Coverage checked with `rg` over `cards/`, `packs/` and `docs/COVERAGE.md`, then the nearest card read in full. Per the brief, no card files were created or edited. NEW marks are leads only: a new card needs three independent organisations.

Totals: 5 fetched, 0 blocked. Rules: 15 (6 covered, 3 partial, 6 NEW).

---

## 1. WCAG 2.2 Understanding: Non-text Content

URL: https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html
Fetch status: fetched

| # | Rule (quoted or tightly paraphrased) | Mark | Evidence |
|---|---|---|---|
| 1 | "All non-text content that is presented to the user has a text alternative that serves the equivalent purpose." | covered: `fn-img-alt-text` | Card rule: "Give every `<img>` an `alt` attribute: text that serves the image's purpose, or `alt=""` when the image is decorative." |
| 2 | Controls and input must have "a name that describes its purpose." | partial: `fn-img-alt-text` | Card covers `<img>` only, with one PASS example of `<button><img alt="Delete draft">`. Missing: `<area>` and `<input type="image">` (both named in the page's failure list), and icon-only controls drawn with SVG or CSS that have no `<img>`. |
| 3 | CAPTCHA: text must describe its purpose, and "alternative forms of CAPTCHA using output modes for different types of sensory perception are provided." | NEW candidate | `rg -il captcha cards packs docs/COVERAGE.md` returns nothing. Nearest checked: `fn-img-alt-text`, which does not address it. Lead only; needs two more independent orgs. |

Rules not listed (within the cap of three): decorative content hidden from assistive tech (covered by `fn-img-alt-text`'s `alt=""` rule); time-based media descriptions (not checked further).

---

## 2. GOV.UK Design System: Details component

URL: https://design-system.service.gov.uk/components/details/
Fetch status: fetched. The page is mostly usage guidance and navigation. The WebFetch summary was a model-written digest, so quotes below are not verbatim-checked against the page.

| # | Rule | Mark | Evidence |
|---|---|---|---|
| 1 | "Do not use the details component to hide information that the majority of your users will need." | covered: `fn-disclosure-hides-only-secondary` | Card rule: "Do not hide a required field or information most users need behind a disclosure that starts closed." The card cites this same URL. |
| 2 | "Use the details component instead of tabs or an accordion if you only have 1 section of content." | NEW candidate | `rg -il 'accordion\|tabs'` hits `fn-disclosure-hides-only-secondary` only in `applies_when`. Its body has no single-section rule. Lead only. |
| 3 | Markup conventions: wrapper `<details class="govuk-details">`, `<summary class="govuk-details__summary">`, content in `govuk-details__text`. | NEW candidate | No card covers this. It is design-system-specific, so it is a lint for GOV.UK users, not a general rule. Lead only; a single org (GOV.UK) is not enough for a general card. |

---

## 3. Go pkg.go.dev: crypto/rand

URL: https://pkg.go.dev/crypto/rand
Fetch status: fetched

| # | Rule (quoted) | Mark | Evidence |
|---|---|---|---|
| 1 | "Use crypto/rand ... when generating secrets": `Text()` "for use when a secret string, token, password, or other text is needed." | covered: `fn-csprng-for-secrets` | Card rule: "Draw every security-relevant random value from the platform CSPRNG." The card cites pkg.go.dev/crypto/rand, but its FAIL/PASS examples are Python and JS only. Go is thin. |
| 2 | "Check the errors returned by `Int` and `Prime`": `Int` "returns an error if rand.Read returns one." | partial: `chg-no-silenced-diagnostics` | That card covers swallowed errors in general and cites go.dev CodeReviewComments. Missing: nothing Go-specific about checking the error from crypto/rand return values. |
| 3 | "Validate inputs before calling `Int`": `Int` "panics if max <= 0." | NEW candidate | Nearest checked: `fn-csprng-for-secrets`, `chg-no-silenced-diagnostics`. Nothing on argument-validation panics in library calls. Lead only. |

---

## 4. CodeQL query help: py/path-injection

URL: https://codeql.github.com/codeql-query-help/python/py-path-injection/
Fetch status: fetched

| # | Rule (quoted) | Mark | Evidence |
|---|---|---|---|
| 1 | "Validate paths constructed from untrusted user input before using them to access files." | covered: `fn-confine-file-path` | Card rule: "Resolve the final path and check that it stays inside the intended base directory before using it." |
| 2 | "First, normalize the path using `os.path.normpath` or `os.path.realpath`." | covered: `fn-confine-file-path` | Card PASS uses `.resolve()` before the check, and its Why explains `../` bypasses. |
| 3 | "Then check that the normalized path starts with the root folder." | covered: `fn-confine-file-path` | Card PASS: `if not p.is_relative_to(UPLOADS.resolve()): abort(400)`. The card cites this URL. |

Note: all three rules on this page are covered. This page is already a source of the card.

---

## 5. TypeScript Handbook: Narrowing

URL: https://www.typescriptlang.org/docs/handbook/2/narrowing.html
Fetch status: fetched. The WebFetch summary was a model-written digest, so quotes are not verbatim-checked.

| # | Rule (quoted or paraphrased) | Mark | Evidence |
|---|---|---|---|
| 1 | `typeof x === "object"` does not exclude `null`: "`typeof null` is actually `"object"`!" | NEW candidate | Nearest checked: `typescript-strict-mode` (codebase level, draft, lacks orgs). It covers the strict flag, not the typeof-null guard. Lead only. |
| 2 | Truthiness checks on primitives can drop valid values: "truthiness checking on primitives can often be error prone." | NEW candidate | `rg -il 'truthy\|typeof'` finds no card on this. Lead only. |
| 3 | Discriminated unions use literal discriminants; avoid optional fields plus `!`. | partial: `fn-variants-as-tagged-union` | Card covers tagged unions and exhaustive `switch` with `never`, with a FAIL of boolean and optional-field bags. Missing: the non-null assertion (`shape.radius!`) on optional fields as a FAIL signal. |

---

## Summary

| Source | Covered | Partial | NEW |
|---|---|---|---|
| WCAG non-text | 1 | 1 | 1 |
| GOV.UK details | 1 | 0 | 2 |
| crypto/rand | 1 | 1 | 1 |
| CodeQL path-injection | 3 | 0 | 0 |
| TS narrowing | 0 | 1 | 2 |
| **Total** | **6** | **3** | **6** |

NEW leads and the other sources they would need for three independent orgs:
- CAPTCHA alternatives (WCAG): needs two more orgs beyond W3C.
- Single-section details vs accordion (GOV.UK): needs two more orgs beyond GOV.UK and the existing NN/g citation.
- Go `Int` panic on `max <= 0` (crypto/rand): needs two more orgs, such as Go vet/staticcheck docs or the Go spec.
- typeof-null narrowing and truthiness on primitives (TS): the TS handbook is one org. Needs two more, such as the TypeScript-ESLint `strict-boolean-expressions` docs or MDN on `typeof`.
- GOV.UK markup conventions: single-source and design-system-specific; not a general card.

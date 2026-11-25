# Pass: fn, change, codebase drafts

Fetch date 2026-11-24, raw text via curl with tags stripped, sentence matched. This note records the sources added to cards in the pass that followed `drafts-orgs-fn-change-codebase.md`.

## Promoted

- code-gate-new-violations-only: Sonar ("enforce quality standards on new and modified code while tracking legacy issues separately"), ArchUnit (freezing rules), Android lint baseline ("only new issues are reported").
- fn-no-logic-in-tests: Microsoft ("avoid ... if, while, for, switch" in unit tests), Uber ("Avoid Unnecessary Complexity in Table Tests"), Google Testing Blog (state inputs and outputs directly). The table-case clause had Uber only, so it moved out of the Rule into the Why.
- fn-error-summary: GOV.UK, NHS, Scottish Government and the A11y Project all say the summary sits at the top and links to each field.
- fn-flags-type-for-flag-sets: Microsoft (FlagsAttribute), Rust API guidelines (C-BITFLAG), Oracle (EnumSet as the typesafe alternative to int bit flags).
- fn-no-aria-hidden-on-focusable: web.dev, WebAIM, MDN, Deque for the aria-hidden clause; WebAIM skip links (https://webaim.org/techniques/skipnav/), W3C focus visible and web.dev focus for the visible-on-focus clause.
- fn-resource-lifetime: tasks: Google Go style, Uber, Python asyncio. Handles: ISO C++ R.1, Python tutorial (https://docs.python.org/3/tutorial/inputoutput.html, `with` closes the file even on an exception), Google (Effective Go `defer f.Close()`).

## Stayed draft

- fn-empty-collection-not-none: Microsoft collections guidelines; PMD rule page (https://pmd.github.io/pmd/pmd_rules_java_errorprone.html) is a tool description. SEI CERT MET55-J returned an empty body on four fetches.
- fn-propagate-dont-swallow: Microsoft exception best practices (https://learn.microsoft.com/en-us/dotnet/standard/exceptions/best-practices-for-exceptions) give the inner-exception form. Python (https://docs.python.org/3/tutorial/errors.html) and Oracle (https://docs.oracle.com/javase/tutorial/essential/exceptions/chained.html) describe chaining as a mechanism.
- Alloy (Cloudflare block) and the GitLab testing guide (no order rule) did not re-match for code-tests-order-independent. The OpenAPI 3.1 spec states no practice for chg-api-spec-in-same-change.

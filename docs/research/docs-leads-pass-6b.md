# Docs leads, pass 6b

Method: every page was fetched with `curl -sL` into a fresh `mktemp -d` scratch dir, tags stripped with `python3 -I`, and the sentence found with `rg` in the stripped text (raw GitHub files where a docs site is a JS shell). Fetch date 2026-11-22. No summaries used as evidence. Paraphrases only; quotes are 10 words or fewer. Org grouping follows docs/PROMOTION.md (Google covers Go, eng-practices, Chromium, AIP and the Go style guide; Microsoft covers Learn, Azure SDK and .NET; GitHub covers its docs and opensource.guide; a person's blog is not an org; a tool or library description is not a stated practice).

Area covered: PR descriptions and templates, README contents, error and log message wording, API reference docs. Existing-card check: `rg` over `cards/` first. No card covers error-string casing, apologetic or blaming error text, log-and-return, or log-call interpolation. `fn-error-says-what-and-how` (stable) covers form validation text only; `chg-commit-body-says-why`, `chg-commit-subject-imperative`, `chg-commit-title-area-prefix` (already made, pass 5b) cover commit messages; `chg-author-hygiene` covers "write the description"; `code-readme-per-module` covers a README existing per package.

## Ranking

| # | Lead | Orgs | Verdict |
|---|---|---|---|
| 1 | Error strings: lowercase start, no trailing period | 3 firm (+1 partial) | clears three, new card |
| 2 | Log an error or return it, not both | 3 | clears three, new card |
| 3 | Error text avoids "please", "sorry", "oops" and blame | 5 | clears three, new card (strongest) |
| 4 | Error text from code, CLI or API names the cause and the next step | 5 | clears three; overlaps `fn-error-says-what-and-how`, widen or split |
| 5 | Log calls pass variable data as fields or arguments, not interpolated into the message | 3 (one weak) | clears three with a caveat |
| 6 | Top-level README says what the project is and how to use it | 3 | clears three; near `code-readme-per-module` |
| - | PR description says why and how it was tested | why: 8; how tested: 2 | why is covered; how-tested under three |
| - | API reference documents every field | 1 to 2 | not enough; mostly covered |

## 1. Error strings: lowercase start, no trailing period

Rule candidate: "Start an error string in lowercase and do not end it with a period, since it is wrapped in other text." A diff that adds `errors.New("Failed to read config.")` is a FAIL. Nearest card: none (`fn-error-says-what-and-how` is UI validation).

1. https://go.dev/wiki/CodeReviewComments . Google (Go). Error strings are not capitalised and have no end punctuation, because they print after other context. Found: "Error Strings" section.
2. https://google.github.io/styleguide/go/decisions . Google (Go style guide, same org as 1). Same rule, with an exception for proper nouns and exported names. Found: "Error strings".
3. https://raw.githubusercontent.com/rust-lang/rustc-dev-guide/master/src/diagnostics.md . Rust. Error, warning, note and help messages start lowercase and end without punctuation. Found: "Diagnostic structure" bullet list.
4. https://rust-lang.github.io/api-guidelines/interoperability.html . Rust (same org as 3). The `Display` text of an error type is lowercase, no trailing punctuation, concise. Found: "Error types are meaningful and well-behaved (C-GOOD-ERR)".
5. https://llvm.org/docs/CodingStandards.html . LLVM. Start the first sentence in lowercase and drop the final period, to match other tools. Found: "Error and Warning Messages".
6. https://clang.llvm.org/docs/InternalsManual.html . LLVM (same org as 5). Diagnostics do not start capitalised or end with punctuation, except proper nouns and a question mark. Found: diagnostic wording suggestions.
7. https://raw.githubusercontent.com/swiftlang/swift/main/docs/Diagnostics.md . Apple (Swift). Diagnostic is one phrase or sentence with no period at the end. Found: "Grammar and Phrasing". Period only, no casing rule; partial.

Count: Google, Rust, LLVM = 3 firm; Swift partial. Not found: GCC internals page (checked "Guidelines for Diagnostics" and the GCC coding conventions page, no casing sentence); Uber Go guide (no casing rule). Counterpoint to carry: user-facing UI text and public API messages are sentence case with a period (Microsoft, Google, GOV.UK), so the card is scoped to developer-facing error strings that get wrapped or joined. Draft id: `fn-error-string-lowercase-no-period`.

## 2. Log an error or return it, not both

Rule candidate: "Handle an error once: log it or return it, not both." A diff that adds a log line and then returns the same error is a FAIL. Nearest card: none (`svc-request-id-logging` is about ids).

1. https://google.github.io/styleguide/go/best-practices . Google (Go). If you return an error, usually do not also log it; let the caller choose, to avoid log spam. Found: "Logging errors" section, "Avoid duplication".
2. https://raw.githubusercontent.com/uber-go/guide/master/style.md . Uber. The caller should not log the error and then return it, because callers above may handle it too. Found: "Handle Errors Once", with a Bad example.
3. https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-instrumentation/logging.md . Kubernetes. Do not emit an error log before returning, since the caller may handle it gracefully. Found: error-handling guidance after "How to log". It allows a V(4) info log for debugging.

Count: Google, Uber, Kubernetes = 3. Not found: Microsoft .NET best-practices page (the rethrow section is about stack traces, not logging); Azure SDK general implementation (logging rules are about what to log). Counterpoint: at a top-level handler where the error is not returned further, logging is correct (Kubernetes names this case). Draft id: `fn-log-or-return-not-both`.

## 3. Error text avoids "please", "sorry", "oops" and blame

Rule candidate: "Do not apologise with sorry or oops in error text, or word it to blame the reader." Checkable with grep on added message strings. Nearest card: none.

1. https://developer.apple.com/design/human-interface-guidelines/writing.md . Apple. Avoid blame in error messages; interjections like "oops" are usually unneeded. Found: "Write clear error messages". (The plain `/writing` URL is a JS shell; the `.md` variant loads.)
2. https://design-system.service.gov.uk/components/error-message/ . GOV.UK. Do not use "please", "sorry", "oops", or words like "you forgot". Found: the "Do not use" list.
3. https://atlassian.design/foundations/content/designing-messages/error-messages . Atlassian. Avoid "please" and "sorry"; sorry makes errors look more severe. Found: the Do/Don't table on that page.
4. https://learn.microsoft.com/en-us/style-guide/a-z-word-list-term-collections/s/sorry . Microsoft. Apologise only for serious product faults, never for outside causes such as the network. Found: the whole entry. Entry `/p/please` says avoid please unless the app is at fault.
5. https://developers.google.com/style/word-list . Google. Do not use please in ordinary instructions; allowed for permission or forgiveness. Found: entry "please".

Count: Apple, GOV.UK, Atlassian, Microsoft, Google = 5. Microsoft and Google allow narrow use, so the card says "avoid" and keeps the exception. Only Apple and GOV.UK name blame directly. Draft id: `fn-error-text-no-apology-or-blame`.

## 4. Error text names the cause and the next step (beyond form validation)

Rule candidate: "An error shown to a user, caller or operator says what failed and what to do next." Nearest card: `fn-error-says-what-and-how` (stable; applies only when code builds form-validation text). This lead extends the same idea to exceptions, CLI output and API error bodies. Better as a widened `applies_when` or a sibling card with `context: []`.

1. https://gcc.gnu.org/onlinedocs/gccint/Guidelines-for-Diagnostics.html . GNU (GCC). A diagnostic helps the user act; for an error they ask how to fix it. Found: "Diagnostics are actionable".
2. https://google.aip.dev/193 . Google. Message states the problem and offers an actionable resolution; keep it brief and actionable. Found: "Status.message" and the guidance text above it. https://cloud.google.com/apis/design/errors carries the same text.
3. https://atlassian.design/foundations/content/designing-messages/error-messages . Atlassian. An error message says what happened and what to do next. Found: opening paragraph.
4. https://design.gitlab.com/content/error-messages . GitLab. Error messages let users know of a problem and provide ways to resolve it. Found: the "Error messages" section of the forms page.
5. https://developer.apple.com/design/human-interface-guidelines/writing.md . Apple. Be clear about what someone can do to fix an error. Found: "Write clear error messages".
6. https://llvm.org/docs/CodingStandards.html . LLVM. Give the context needed to understand what went wrong. Found: "Error and Warning Messages". Names the cause only; partial.

Count: GNU, Google, Atlassian, GitLab, Apple = 5 firm; LLVM partial. Draft id: `fn-error-text-names-fix`. Decision for the parent: merge into `fn-error-says-what-and-how` (add GCC, AIP-193, Atlassian, GitLab to its `borrowed_from`) or split.

## 5. Log calls pass variable data as fields, not interpolated into the message

Rule candidate: "Pass variable data to a log call as arguments or key/value fields, not through string interpolation." Nearest card: none (`svc-tenant-id-in-telemetry` says which fields).

1. https://raw.githubusercontent.com/kubernetes/community/master/contributors/devel/sig-instrumentation/logging.md . Kubernetes. The non-structured klog methods such as Infof are no longer recommended; migrate to the key/value ones. Found: "How to log".
2. https://learn.microsoft.com/en-us/dotnet/core/extensions/logging-library-authors . Microsoft. Avoid string interpolation in logging; use the message template and an argument list. Found: heading "Avoid string interpolation in logging". The page https://learn.microsoft.com/en-us/dotnet/core/extensions/logging says the same, in a Tip near "Log message template".
3. https://docs.python.org/3/howto/logging.html . Python. To log variable data, use a format string and append the data as arguments. Found: "Logging variable data". An instruction by example; it does not say why or forbid f-strings. Weak.

Count: Kubernetes, Microsoft, Python (weak) = 3. Not counted: Uber zap, HashiCorp go-hclog, Go slog blog, Elastic ECS and Google Cloud Logging docs (tool or product descriptions, not a stated practice); Pylint W1203 (a linter). Counterpoint: the reasons differ (structure, performance, lazy evaluation), so the Rule should stay at "do not interpolate" and let `tool_gate` name the linter (CA2254, W1203). Draft id: `fn-log-no-interpolated-message`.

## 6. Top-level README says what the project is and how to use it

Rule candidate: "A README says what the project does and how to install and use it." Nearest card: `code-readme-per-module` (stable; one README per package). Different check: the README exists but is empty or only a title. Probably a clause on that card, not a new one.

1. https://google.github.io/styleguide/docguide/READMEs.html . Google. A package README says what the package is for, who to contact, its status, and how to use it. Found: "What to put in your README".
2. https://chromium.googlesource.com/chromium/src/+/main/docs/documentation_guidelines.md . Google (Chromium, same org as 1). Component README says what it does and how it is meant to be used. Found: "Guidelines" paragraph on README.md.
3. https://azure.github.io/azure-sdk/general_documentation.html . Microsoft (Azure SDK). The library README includes installation and usage information. Found: README.md bullet in the deliverables list.
4. https://raw.githubusercontent.com/github/docs/main/content/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes.md . GitHub. READMEs typically cover what it does, why useful, how to start, where to get help. Found: list after "About READMEs". Descriptive ("typically"), not a MUST.
5. https://opensource.guide/starting-a-project/ . GitHub (same org as 4). Answer what it does, why it is useful, how to get started, where to get help. Found: "Writing a README".

Count: Google, Microsoft, GitHub = 3 (Chromium and opensource.guide add no org). Not found: Microsoft Learn contributor README page (404), OpenSSF badge page (no README sentence), CNCF README template page (loaded, no usable sentence), Mozilla open-leadership book (404).

## PR description (checked, not a new card)

Rule candidate: "A PR description says why the change is made and how it was tested."

Why or motivation in the description:
1. https://google.github.io/eng-practices/review/developer/cl-descriptions.html . Google. A description says what changed and why; "Fix bug" is called inadequate. Found: "Writing good CL descriptions", "Bad CL Descriptions".
2. https://raw.githubusercontent.com/spring-projects/spring-framework/main/CONTRIBUTING.md . Spring. Use the PR description to give context and motivation. Found: "Submit a Pull Request" item 1.
3. https://raw.githubusercontent.com/rails/rails/main/.github/pull_request_template.md . Rails. Template asks the motivation and why the PR must be merged. Found: "Motivation / Background".
4. https://raw.githubusercontent.com/facebook/react/main/.github/PULL_REQUEST_TEMPLATE.md . Meta (React). Summary explains the motivation; three fields are mandatory. Found: "Summary" and the header comment.
5. https://raw.githubusercontent.com/kubernetes/kubernetes/master/.github/PULL_REQUEST_TEMPLATE.md . Kubernetes. Template asks what the PR does and why it is needed. Found: heading "What this PR does / why we need it".
6. https://raw.githubusercontent.com/django/django/main/.github/pull_request_template.md . Django. Branch description gives the rationale, minimum five words. Found: "Branch description".
7. https://raw.githubusercontent.com/numpy/numpy/main/.github/PULL_REQUEST_TEMPLATE.md . NumPy. Describe what problem the PR solves. Found: "PR summary" comment.
8. https://docs.gitlab.com/development/contributing/merge_request_workflow/ . GitLab. Clear title and description explaining relevance. Found: "Description of changes".

Count (why): 8 organisations. Existing: `chg-author-hygiene` (stable) already says write the description and that it gives the reason; `chg-commit-body-says-why` covers the commit body. Not a new card.

How it was tested, in the description:
1. React template, "How did you test this change?": commands run and output; an empty answer likely closes the PR. Meta.
2. https://raw.githubusercontent.com/microsoft/vscode/main/.github/pull_request_template.md . Microsoft (VS Code). Include a description of the changes and how to test them. Found: last checklist bullet.
3. GitLab MR workflow (URL as above): description includes steps for reviewers to view the change; the testing section covers tests, not the description. Partial.

Count (how tested in the description): Meta, Microsoft = 2, GitLab partial. Under the bar. Feed to `chg-author-hygiene` `borrowed_from`: React and VS Code templates. Other templates (Azure SDK Python, Angular, Flutter, Home Assistant) have a "tests added" tick box, which is a different check and is `chg-tests-ship-with-change`.

## PR template exists, API reference documents every field (checked, dropped)

- PR template exists: Kubernetes, Rails, Meta, Microsoft, Django, NumPy and Prometheus all ship one, and GitLab and GitHub document the feature, but a reviewer cannot FAIL a diff on it. Skipped. `chg-author-hygiene` already names a PR template as its `tool_gate`.
- Every API field documented: https://google.aip.dev/192 (Google) says public comments must sit over every service, method, message, field and enum value. https://learn.microsoft.com/en-us/style-guide/developer-content/reference-documentation (Microsoft) lists a description per parameter and per property value as sections of a reference page, a page layout more than a rule. Zalando, Kubernetes api-conventions, OpenAPI best practices and Azure REST guidelines were fetched and have no sentence requiring a description on every field. Count 1 to 2. `fn-public-api-has-docstring` (stable) already covers code-level public API; only schema and IDL fields are uncovered.

## Existing cards to feed (step 5, not edited here)

- `fn-error-says-what-and-how`: GCC, AIP-193, Atlassian, GitLab, Apple (lead 4).
- `chg-author-hygiene`: React and VS Code PR templates for the how-tested clause.
- `code-readme-per-module`: Azure SDK and GitHub README content lines (lead 6).

## Unreachable or unverified

- developers.google.com/style/error-messages, /style/messages, /style/ui-text: 404. Google appears only through the word list, AIP-193 and Go pages.
- learn.microsoft.com style-guide pages for error messages (several guessed paths) 404; the style-guide TOC has no error-messages page. Microsoft counted only through the `sorry` and `please` entries.
- mozilla/fluent `docs/error-messages.md` and mozilla/protocol error-messages: 404. design.firefox.com/photon page returned a 1.7 KB JS shell with no text. Mozilla not counted.
- Stripe docs/error-handling: fetched (Spanish, 2.3 MB) but no wording rule was read; not counted. Stripe canonical-log-lines is an engineering post describing one technique; not counted.
- Shopify Polaris actionable-language: loaded, no sentence on apology or blame found. Carbon design system fetch failed.
- Apple HIG `/alerts` and `/writing`: JS shell; the `.md` URLs loaded. `error-messages.md` has no text.
- clang InternalsManual `.rst` on raw GitHub 404; the HTML page was used. GCC "Guidelines for Diagnostics" and the GCC coding conventions: no casing sentence found.
- Zalando RESTful guidelines (status codes, models, meta): no error-text wording or per-field description rule found.
- Grafana and Elasticsearch pull_request_template.md, github/docs CONTRIBUTING.md, Atlassian atlaskit CONTRIBUTING.md, .NET runtime and OpenShift PR templates: 404 at the paths tried.
- Fuchsia contribute_changes and AOSP submit-patches: fetched, no "Test:" or how-tested sentence located; not counted.
- Python logging cookbook and library page returned about 500 bytes (blocked or redirect); only the HOWTO was used.
- Spring Boot logging docs: binary-match on the stripped text; not read.

## Parent verification and outcome (2026-11-22)

Re-fetched raw and matched the sentence for lowercase error strings (Google Go, Rust, LLVM), log-or-return (Google Go best practices, Uber, Kubernetes), no apology or blame (GOV.UK, Atlassian, Apple, Microsoft), and actionable errors (GCC, AIP-193, Atlassian, Apple). New stable cards: `fn-error-string-lowercase-no-period`, `fn-log-or-return-not-both`, `fn-error-text-no-apology-or-blame`, `fn-error-message-actionable`. GitHub about-readmes added to `code-readme-per-module`. Left as leads: log fields not interpolated (Kubernetes, Microsoft, Python weak), PR description says how it was tested (Meta, Microsoft only), README contents (a clause on `code-readme-per-module`).

# Size, branches, types (Task F) — organisation sources

Pass for four draft cards. Every page below was fetched and read; quotes are verbatim in quote marks, paraphrases are marked "(paraphrase)". Pages I could not fetch are marked UNFETCHED and excluded from the org counts. A tool/linter default is reported as the tool's documented threshold, as the brief asks.

Card drafts checked against `docs/PROMOTION.md` "The bar" (three independent organisations per Rule clause; a person never counts; a tool/linter rule page counts when it documents a rule with a threshold or rationale).

---

## F1 — a source file/module should stay under a documented line ceiling (≈1,000 lines)

The single most important result: **Pylint's `max-module-lines` default is exactly `1000`**, and **SonarSource rule S104 defaults to `1000`**. The draft's `lacks:` line ("no org states a file-length ceiling or the 1,000-line figure") is no longer true on the number.

1. https://pylint.readthedocs.io/en/stable/user_guide/configuration/all-options.html (org: Pylint / pylint-dev). `--max-module-lines` is documented as "Maximum number of lines in a module." with "**Default:** `1000`". The companion message page (https://pylint.readthedocs.io/en/stable/user_guide/messages/convention/too-many-lines.html) says the check fires when "a module has too many lines, reducing its readability", message "Too many lines in module (%s/%s)". **Backs F1.** Tool gate: `too-many-lines` (C0302) / `max-module-lines`.

2. https://eslint.org/docs/latest/rules/max-lines (org: ESLint / OpenJS Foundation). "`"max"` (default `300`) enforces a maximum number of lines in a file." And: "Some people consider large files a code smell. Large files tend to do a lot of things and can make it hard following what's going. While there is not an objective maximum number of lines considered acceptable in a file, most people would agree it should not be in the thousands. Recommendations usually range from 100 to 500 lines." **Backs F1** (a documented ceiling; its own recommendation is lower than 1,000 — see Counter-evidence). Tool gate: `max-lines`.

3. https://checkstyle.sourceforge.io/checks/sizes/filelength.html (org: Checkstyle). `FileLength` default `max` = `2000`. "Checks for long source files. Rationale: If a source file becomes very long it is hard to understand. Therefore, long classes should usually be refactored into several individual classes that focus on a specific task." **Backs F1.** Tool gate: `FileLength`.

4. https://docs.rubocop.org/rubocop/latest/cops_metrics.html (org: RuboCop). `Metrics/ClassLength` and `Metrics/ModuleLength`: "Checks if the length of a class exceeds some maximum value." Default `Max` = `100` for each. (Also `Metrics/MethodLength` Max `10`, `Metrics/BlockLength` Max `25`.) **Backs F1** (a documented ceiling, at class/module granularity rather than whole file). Tool gate: `Metrics/ClassLength`, `Metrics/ModuleLength`.

5. https://docs.pmd-code.org/latest/pmd_rules_java_design.html (org: PMD). `GodClass`: "God classes do too many things, are very big and overly complex. They should be split apart to be more object-oriented." `CyclomaticComplexity` (methodReportLevel `10`, classReportLevel `80`) and `CognitiveComplexity` (`reportLevel` `15`) set numeric size/complexity ceilings. Note: the `ExcessiveClassLength` and `NcssCount` rules the brief names are **not present in the PMD 7 Java design ruleset I fetched** (removed/renamed); `ExcessivePublicCount` (default `45`) is the surviving size cap. **Backs F1.** Tool gate: `CognitiveComplexity`, `CyclomaticComplexity`, `GodClass`, `ExcessivePublicCount`.

6. SonarSource rule S104 "Files should not have too many lines of code" — **corroborated, not directly fetched** (see UNFETCHED below). Across multiple public SonarQube rule pages the default parameter is "Maximum authorized lines of code in a file. Default Value: 1000" and the canonical violation message is "This file has N lines, which is greater than 1000 authorized. Split it into smaller files." I report this as corroboration of the 1,000 figure, not as a counted, quoted row, because I could not render a canonical rule page. Tool gate: `S104` (files-too-many-lines).

**F1 org count (directly fetched, quoted):** Pylint, ESLint, Checkstyle, RuboCop, PMD = **5 organisations** (plus SonarSource S104 = 1,000 as corroboration). Confidence: **high** on "a documented ceiling exists"; **high** on the exact 1,000 figure (Pylint default 1,000, SonarSource S104 default 1,000); **low** on "1,000 is the consensus number" — it is not (ESLint 300, RuboCop 100, Checkstyle 2,000).

---

## F2 — put a new case behind its own function or type; don't add a one-off branch to a shared flow

Two clauses. "Put the case behind its own function/type" has the strongest backing; "don't add a one-off branch" is backed by complexity-limit rules plus the Linux kernel's explicit "factor the conditional into a helper function".

1. https://www.kernel.org/doc/html/latest/process/coding-style.html (org: Linux kernel project). §21 Conditional Compilation: "Wherever possible, don't use preprocessor conditionals (#if, #ifdef) in .c files; doing so makes code harder to read and logic harder to follow." and "Prefer to compile out entire functions, rather than portions of functions or portions of expressions. Rather than putting an ifdef in an expression, factor out part or all of the expression into a separate helper function and apply the conditional to that function." §1: "if you need more than 3 levels of indentation, you're screwed anyway, and should fix your program." §6: "Functions should be short and sweet, and do just one thing." … "Use helper functions with descriptive names". **Backs F2 clause A (own function) and B (no one-off branch).**

2. https://go.dev/doc/effective_go (org: Go project). Switch: "It's therefore possible—and idiomatic—to write an `if`-`else`-`if`-`else` chain as a `switch`." Type switch: "A switch can also be used to discover the dynamic type of an interface variable. Such a *type switch* uses the syntax of a type assertion with the keyword `type` inside the parentheses." If: "when an `if` statement doesn't flow into the next statement—that is, the body ends in `break`, `continue`, `goto`, or `return`—the unnecessary `else` is omitted." **Backs F2 clause A (own type via type switch / dispatch) and B (flatten conditionals, omit unnecessary else).**

3. https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca1502 (org: Microsoft). "A method has an excessive cyclomatic complexity." "The rule reports a violation when the cyclomatic complexity of a method is more than 25." Cyclomatic complexity is "determined by the number and complexity of conditional branches." **Backs F2 clause B** (a documented cap on conditional branches). Tool gate: `CA1502` (default threshold 25).

4. https://docs.pmd-code.org/latest/pmd_rules_java_design.html (org: PMD). `CognitiveComplexity`: "Methods that are highly complex are difficult to read and more costly to maintain." "By default, this rule reports methods with a complexity of 15 or more. Reported methods should be broken down into less complex components." **Backs F2 clause B.** Tool gate: `CognitiveComplexity` (reportLevel 15).

5. https://shopify.engineering/other-driven-developments (org: Shopify). In "Stickler Driven Development", on a method with `or`/`elsif` branches: "it's unnecessary complexity and incorrect coupling we're really after. … the problem is solved if we pass the persistence logic on to our item. The item will implement a persist method however it sees fit". (paraphrase of the worked example) The fix shown replaces the branch with a polymorphic `item.persist`. **Backs F2 clause A** (replace conditional with a method on the type).

Corroborated, not directly fetched: SonarSource S3776 "Cognitive Complexity of functions should not be too high" (default threshold 15 for most languages, 25 for some). Secondary/person: Martin Fowler and Refactoring Guru "Replace Conditional with Polymorphism"; Google "Clean Code Talks" (Misko Hevery) — persons, listed apart, not counted.

**F2 org count:** Linux kernel, Go, Microsoft, PMD, Shopify = **5 organisations**. Clause A (own function/type): Linux kernel, Go, Shopify = 3. Clause B (no one-off branch): Linux kernel, Microsoft (CA1502), PMD, Go = 4. Confidence: **medium-high**.

---

## F3 — inline a wrong abstraction that has grown flags, then re-split (prefer duplication / Rule of Three)

1. https://go-proverbs.github.io/ (org: Go community — from Rob Pike's 2015 Gopherfest talk). "A little copying is better than a little dependency." **Backs F3 clause A (prefer duplication/inlining).** Flag: the proverb is person-attributed (Rob Pike) on a community site, so treat it as a borderline org; it is the canonical Go statement of the practice.

2. https://shopify.engineering/other-driven-developments (org: Shopify). "If we're in a position where we're duplicating code, Martin Fowler shared a helpful rule of thumb, the 'rule of three.' In other words, don't go looking for an abstraction until you have three instances of similar code. Refactoring after one duplication inevitably produces a premature, and thus likely incorrect, abstraction". And on flag-riddled front-end abstractions: "If you constantly abstract all similar behavior between pages, with the use of flags and conditionals, you've gained less duplication at the cost of your bundle size." **Backs F3 clause A (a flags+conditionals abstraction is a bad trade) and B (re-split only at the third instance).**

3. https://thoughtbot.com/blog/the-case-for-wet-tests (org: Thoughtbot). Quotes and endorses Sandi Metz: "Duplication is far cheaper than the wrong abstraction". Own practice: "I find it helpful to always view a new abstraction as a trade-off between de-duplication and added complexity." and "DRY test code should be a means to achieving the goals of your test suite, rather than a goal in and of itself." and "over-abstracting in tests tends to be more expensive than in business code." **Backs F3 clause A and B.**

4. https://docs.astral.sh/ruff/rules/boolean-type-hint-positional-argument/ (org: Astral / Ruff). `FBT001` (boolean-type-hint-positional-argument): "The use of a boolean will also limit the function to only two possible behaviors, which makes the function difficult to extend in the future. Instead, consider refactoring into separate implementations for the `True` and `False` cases, using an `Enum`, or making the argument a keyword-only argument, to force callers to be explicit when providing the argument." **Backs F3 clause A (a boolean flag is a wrong abstraction) and B (re-split into separate implementations).** Tool gate: `FBT001` / `FBT002` (Ruff, from flake8-boolean-trap).

People/secondary (not counted): Sandi Metz "The Wrong Abstraction" ("duplication is far cheaper than the wrong abstraction"); Martin Fowler "Refactoring" / the Rule of Three; Kent C. Dodds "AHA Programming".

**F3 org count:** Shopify, Thoughtbot, Astral (Ruff), plus Go (proverb, borderline) = **3–4 organisations**. Clause A (inline/prefer duplication): Shopify, Thoughtbot, Ruff, Go = 4 (3 solid). Clause B (re-split at the right time): Shopify (Rule of Three), Thoughtbot, Ruff (refactor into separate implementations) = 3. Confidence: **medium** — clause B only just reaches three, and one of the three (Ruff) is a linter rule rather than a prose "prefer duplication" source.

---

## F4 — name the smell, point to the line, suggest the refactoring; don't file smells as taste

1. https://google.github.io/eng-practices/review/reviewer/standard.html and .../looking-for.html (org: Google — one org, two pages). Standard: "Aspects of software design are almost never a pure style issue or just a personal preference. They are based on underlying principles and should be weighed on those principles, not simply by personal opinion." and "Reviewers should *always* feel free to leave comments expressing that something could be better, but if it's not very important, prefix it with something like 'Nit: ' to let the author know that it's just a point of polish that they could choose to ignore." Looking-for: "Usually comments are useful when they **explain why** some code exists, and should not be explaining *what* some code is doing." and "Don't block CLs from being submitted based only on personal style preferences." **Backs F4 clause A (point to the issue, give the reason) and B (not taste — Nit: for taste, design is not opinion).**

2. https://docs.gitlab.com/ee/development/code_review/ (org: GitLab). Reviewer guidance: "Identify ways to simplify the code while still solving the problem." "Offer alternative implementations, but assume the author already considered them." "Be explicit. People don't always understand your intentions online." And on taste: "Accept that many programming decisions are opinions. Discuss trade-offs and resolve quickly." and "Enforce code style through automation rather than review comments." **Backs F4 clause A and B.**

3. https://blog.palantir.com/code-review-best-practices-19e02780015f (org: Palantir). "Comments: concise, friendly, actionable": "Reviews should be concise and written in neutral language. Critique the code, not the author." and "Try to differentiate between suggestions (e.g., 'Suggestion: extract method to improve legibility'), required changes (e.g., 'Add @Override'), and points that need discussion or clarification." and "Avoid absolute judgements: 'this can *never* work', 'the result is *always* wrong'." Its "Personal taste" example marks a taste comment with `//R: nit:` ("up to you"). **Backs F4 clause A (specific, actionable suggestion with a named refactor) and B (label taste as nit, separate from real smells).**

Note: Microsoft's Engineering Playbook code-review page (https://github.com/microsoft/code-with-engineering-playbook/blob/main/docs/code-reviews/README.md) only states goals and links out to "Google's Engineering Practices documentation" — it restates Google and does not independently state the practice, so it is **not counted**. SonarSource's "code smell" issue taxonomy and per-rule "Why is this an issue? / How to fix it" structure support the "name the smell + suggest the fix" mechanic, but I could not fetch a clean rule page, so it is listed under UNFETCHED below rather than counted.

**F4 org count:** Google, GitLab, Palantir = **3 organisations**. Clause A (name + line + refactor): Google, GitLab, Palantir = 3. Clause B (not taste): Google, GitLab, Palantir = 3. Confidence: **high**.

---

## Counter-evidence

- **F1:** ESLint's own recommendation ("Recommendations usually range from 100 to 500 lines") and default (300) are *below* 1,000; Checkstyle's default is *above* it (2,000). So "about 1,000" is a specific tool default (Pylint, SonarSource S104), not a cross-tool consensus. The Linux kernel coding style sets a function-length / indentation-depth guidance but no whole-file line count. Ousterhout's "deep modules" already listed in the card's counterpoint: a long file can be coherent.
- **F2:** Over-extracting one special case is itself a smell — Google eng-practices "Complexity" warns against over-engineering: "Encourage developers to solve the problem they know needs to be solved *now*, not the problem that the developer speculates *might* need to be solved in the future." The card's own counterpoint (one line is fine; [[mod-yagni]]) is consistent with this.
- **F3:** The dominant counter-principle is DRY: duplication has its own cost (the card already notes Ousterhout lists repetition as a red flag). Shopify's post is careful to say copying is "a tool to be wielded", not a default: "we should treat copying and pasting as a skill".
- **F4:** GitLab says style should be enforced "through automation rather than review comments" — a reviewer who files every smell as a comment is off-target; the practice is to name substantive design smells, not to relitigate style.

---

## Also read, no rule / UNFETCHED

- UNFETCHED (excluded from counts): SonarSource rule S104 and S3776 canonical pages (rules.sonarsource.com returns 404 for `/java/RSPEC-104/`; `next.sonarqube.com` rule pages are JS SPAs that render no rule text to a fetch; `sonarsource.github.io/rspec` returns a GitHub sign-in). The S104 default (1000) and S3776 default (15) were confirmed only via search snippets of public SonarQube instances and the canonical violation strings, so they are reported as corroboration, not as quoted rows.
- https://www.sonarsource.com/resources/cognitive-complexity/ — fetched, but it is a marketing landing page with no whitepaper body text (the paper is a gated PDF). No usable quote; the metric's substance is instead documented via the PMD `CognitiveComplexity` rule page (which cites `https://www.sonarsource.com/docs/CognitiveComplexity.pdf`).
- Google "Clean Code Talks" (Misko Hevery, "Inheritance, Polymorphism, & Testing") and Martin Fowler / Refactoring Guru "Replace Conditional with Polymorphism" — persons/secondary for F2, listed apart.
- Google SWE book "Rule of Three" — I could not pin a verbatim passage on abseil.io in this pass; the Rule of Three is instead sourced through Shopify's post and Wikipedia's definition. Listed as a possible fourth org for F3 if a future pass quotes the book directly.
- JetBrains inspections (e.g. "Replace conditional with polymorphism") — not fetched this pass; a candidate tool gate for F2 if a page is opened.
- SonarSource "code smells" taxonomy page (https://www.sonarsource.com/learn/code-smells/) — a candidate F4 source (names the smell, per-rule "how to fix"), not fetched this pass.

---

## Per-claim summary

| Claim | Distinct orgs (fetched, quoted) | Clauses at ≥3 orgs | Confidence |
|---|---|---|---|
| F1 line ceiling | 5 (Pylint, ESLint, Checkstyle, RuboCop, PMD) + SonarSource S104 (corroborated) | single Rule line | high (number = 1,000 exactly in Pylint & S104) |
| F2 no special-case branch | 5 (Linux kernel, Go, Microsoft, PMD, Shopify) | A=3, B=4 | medium-high |
| F3 inline wrong abstraction | 3 solid + 1 borderline (Shopify, Thoughtbot, Ruff; Go proverb) | A=4, B=3 (B just reaches 3) | medium |
| F4 name the smell, not taste | 3 (Google, GitLab, Palantir) | A=3, B=3 | high |

## Doubts / notes for the maintainer

1. **SonarSource rows are corroboration, not counted.** I could not render a canonical S104/S3776 rule page (JS SPA / 404). If you want SonarSource as a hard third org anywhere, fetch `docs.sonarsource.com` or a live SonarQube rule page and quote the default parameter directly.
2. **Go proverb is person-attributed.** "A little copying is better than a little dependency" is Rob Pike's, on a community site — a reviewer may refuse to count it as an independent org. Without it, F3 clause A still has Shopify + Thoughtbot + Ruff (3), so the floor holds.
3. **F3 clause B ("re-split") is the thinnest.** It reaches three only by counting Ruff's "refactor into separate implementations" as backing the re-split remedy. The card's `lacks:` line already flags this; my pass does not add a clean fourth prose org for the re-split side.
4. **Microsoft's Engineering Playbook does not independently back F4** (it links to Google's eng-practices), so F4 rests on Google + GitLab + Palantir.
5. **PMD's `ExcessiveClassLength`/`NcssCount` are gone in PMD 7.** The brief names them, but the current PMD 7 Java design ruleset uses `CognitiveComplexity`, `CyclomaticComplexity`, `GodClass`, `ExcessivePublicCount` instead.

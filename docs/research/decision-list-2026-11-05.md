# Decision list, 2026-11-05

For Pablo to decide. Nothing below is written as a card yet except where marked. Counts are distinct organisations from the three research passes (`design-depth-orgs-D.md`, `coupling-orgs-E.md`, `size-branches-types-orgs-F.md`). I re-fetched 8 of the pages cited in these three passes (Pylint source, CA1506, the Microsoft abstractions page, Go review comments, AWS hexagonal, PMD, ESLint max-lines, Shopify) and every quote I checked matched; rows I did not re-fetch are marked. Source of the three skills: Matt Pocock's `improve-codebase-architecture` and `codebase-design`, Cursor's `thermo-nuclear-code-quality-review` (already mapped in `second-pass.md`), and the community `untangle` skill (Law of Demeter, fan-out, cycles; its page names no author).

## A. Promote an existing draft to stable

| # | Card | Result of the search | Recommendation |
|---|---|---|---|
| A1 | `code-file-lines-ceiling` | Pylint `max-module-lines` default 1000 (checked in its source), SonarSource S104 default 1000 (page not fetched, corroboration only), ESLint 300, Checkstyle 2000, RuboCop 100 per class, PMD size/complexity caps. 5 orgs state a ceiling, but the number differs. | Promote, but reword the Rule to "set a file-length limit in the linter and split files that pass it" and keep 1,000 as the Pylint/Sonar default in the Why. The bare "1,000" backs on one verified org. |
| A2 | `chg-no-special-case-branches` | Linux kernel style (helper function over `#ifdef`), Effective Go, Microsoft CA1502 (cyclomatic 25), PMD CognitiveComplexity (15, checked), Shopify (checked). Clause "own function or type" 3 orgs, clause "no one-off branch" 4. | Promote after I re-fetch the Linux, Go and CA1502 quotes. |
| A3 | `mod-no-wrong-abstraction` | Shopify (rule of three, checked), Thoughtbot, Ruff FBT001 flag-argument rule. "Re-split" clause only just reaches 3 and leans on a lint rule. | Promote with the "inline" clause as the Rule and move "re-split" to the Why. |
| A4 | `mod-deep-modules` | Microsoft design guidelines (checked, but a 2008 reprint that says it may be out of date), Rust API guidelines, Go review comments (indirect). Ousterhout and Martin still disagree. | Promote only with the Rule narrowed to "small interface: no more members than callers need". Otherwise leave as draft. |
| A5 | `fn-no-pass-through-wrapper` | ESLint `no-useless-constructor`, Pylint `useless-parent-delegation` (both are inheritance-only), Refactoring.Guru (single author). | Keep draft. These sources are narrower than the Rule. |
| A6 | `mod-fowler-smells` | Google, GitLab, Palantir all say: explain the issue, label taste as a nit. | Merge into `chg-review-comment-format` (stable) or delete. It repeats a stable card (rule 8). |

## B. New cards the three skills expose

| # | Card | Orgs | Tool gate | Recommendation |
|---|---|---|---|---|
| B1 | No import cycles between modules or packages (`untangle`) | 6: Go spec, Bazel (both Google), Cargo, import-js, Nx, ArchUnit, Pylint | `import/no-cycle`, Pylint `R0401`, `@nx/enforce-module-boundaries`, ArchUnit `beFreeOfCycles()` | Write as stable. Scope it to the package or module boundary (Python and Rust allow module-level cycles). |
| B2 | Cap the number of things a unit depends on (fan-out) (`untangle`) | 4: Microsoft CA1506 (95 types / 40 members, checked), Checkstyle `ClassFanOutComplexity` (20), import-js `max-dependencies` (10), PMD `CouplingBetweenObjects` (20) and `ExcessiveImports` (30, both checked) | those rules | Write as stable. Defaults differ, so the Rule should say "set a limit" and not a number. |
| B3 | Do not reach through objects (Law of Demeter) (`untangle`) | 2: PMD (`trustRadius` 1, checked), Google Testing Blog. No third found. | PMD `LawOfDemeter` | Write as draft. A third org needs another search. |
| B4 | Do not add an interface or adapter until a second implementation exists (`improve-codebase-architecture`) | 3: Microsoft ("DO NOT provide abstractions unless …", checked), Go review comments (checked), AWS hexagonal page (checked, a caveat) | none | Do not make a card. Add these three to `mod-yagni` (stable) as extra sources. |
| B5 | Record alternatives before committing (design it twice) | Rust RFC, PEP 12, Kubernetes KEP, Oxide RFD add to `code-adr`'s six | none | Add to `code-adr`'s `borrowed_from`. Needs an `oxide` entry and a `pylint.readthedocs.io` prefix in `tools/orgs.py`. |
| B6 | Test through the public interface | Rust book adds one org to `fn-test-behaviour-not-implementation` | none | Add to its sources. |
| B7 | The deletion test, locality, leverage (Pocock's vocabulary) | Pocock only | none | Skip. It is one author's vocabulary and `mod-deep-modules` covers the idea. |

## C. From Cloudflare's security-audit-skill (`cloudflare-security-audit-skill.md`)

| # | Item | Recommendation |
|---|---|---|
| C1 | Add to the review procedure: a missing best practice with no affected principal is not a FAIL; an audit states plainly when it is partial; a finding may be refuted by a fresh reader | Yes, as three short lines in `references/audit.md` through `AUDIT_STEPS` in `tools/build.py`. Not in `SKILL.md` (budget). |
| C2 | A `rejected` record so a disproved claim is not re-raised | Maybe. Only useful for repeated audits; costs a new output section. |
| C3 | About 17 attack classes with no card (cache poisoning, request smuggling, Host/forwarded-header trust, OAuth/OIDC binding, SAML, MFA/passkey, account linking, password reset, soft-delete bypass, derived-copy ACL drift, export/backup scope, quota reset, decompression bombs, poison messages, stale or reordered messages, workload identity, build-input pinning) | Yes, as a research batch: one worker per five classes, OWASP / PortSwigger / RFC sources, drafts first. A big job, so say how many you want. |
| C4 | Machine-readable verdict file plus a validator | No for now. Our reviewers read the text and the lint tool already exists. |

## D. Review lenses (your next task)

Recommendation: do not add a lens as a new axis next to level, concern and depth. Add two optional **modes** beside depth, written in `references/audit.md`:

1. **Adversarial.** After the ledger, a fresh reader gets only the FAILs and tries to refute each one from the code; unrefuted findings stay, refuted ones are dropped and counted. Evidence: Cloudflare ("the agent that checks a finding is never the agent that found it"; validation rejected 40% of raw candidates early, 11% later) and the Adversarial Review paper (arXiv 2608.18167): the plain version scored lowest on review F1 (0.457), and the version with evidence-grounded verdicts scored highest (0.533) at about 4.5 times the tokens. So it needs the rule that a disagreement must cite code, which our `proven` tag already demands.
2. **Empirical.** For every FAIL or PASS whose card has a `tool_gate` or a runnable check, run it and report the output. This is what `pstack`'s "prove it works" principle asks for and what our `proven` tag already means; the mode just makes the run mandatory.

Not recommended: more named lenses (security-minded, performance-minded). That is what the `concern` filter already does. I could not find the poteto tweet; if you paste it I will check these two against it.

## E. From Fran's two reviews

| # | Item | Recommendation |
|---|---|---|
| E1 | Output opened with prose, so `Verdict:` was line 3 and line 7 | Add an eval case for "first line is the Verdict" and tighten the sentence in `SKILL.md`. Cheap. |
| E2 | Committed IDE and user-state files (`xcuserdata/`, `.idea/workspace.xml`) | New change-level card. Needs sources (GitHub gitignore docs, Apple, JetBrains). |
| E3 | No Swift pack | Not now; wait for more Swift reviews. |

## F. Earlier test-speed work, still open

`code-test-suite-time-budget` (draft, needs one more org), `py-test-collection-and-imports` (draft, needs one more org), and three language-neutral practices researched but not carded: unit tests off the network and disk (Google, Microsoft, Spring), per-worker databases when parallel (Django, Rails), affected-tests-only runs (Meta, Microsoft, Shopify).

## Notes

- The repo asks for one card per pull request. A1 to A6 and B1 to B3 are nine cards, so they need splitting or an exception.
- opencode's default model in your other sessions is probably now DeepSeek V4.1 Flash (Go).

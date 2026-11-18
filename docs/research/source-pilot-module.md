# Source pilot, module level

Five source pages, three candidate rules each. Each rule is checked against `cards/`, `packs/` and `docs/COVERAGE.md`.

Fetch caveat: the WebFetch tool passes page text through a small model. Quotes below are tight paraphrases from that output, not verified verbatim against the live page. Check the live page before quoting any of them in a card.

Coverage marks: **covered** (a card states the rule), **partial** (a card covers part of it; the gap is named), **NEW candidate** (no card; nearest ids listed). A NEW candidate is only a lead. A new card needs three independent orgs behind it, so each entry names the other sources it would still need.

Totals: 15 rules. Covered 6, partial 5, NEW candidate 4.

---

## 1. Uber Go style guide, "Avoid Mutable Globals"

URL: https://github.com/uber-go/guide/blob/master/style.md#avoid-mutable-globals
Fetch status: ok (summarized; the tool declined to return the section verbatim).

| # | Rule (paraphrase) | Coverage | Evidence |
|---|---|---|---|
| 1 | Do not mutate global variables; use dependency injection. Quote: "Avoid mutating global variables, instead opting for dependency injection." | **covered**: `mod-no-module-mutable-state` (stable) | Card Rule: "Keep no mutable state at module level; hold it on an instance." The card already cites this URL. |
| 2 | The rule also applies to global function pointers. | **partial**: `mod-no-module-mutable-state` | `applies_when` lists "a module-level variable, a list, dict, counter, cache, client or singleton". Function pointers and hooks are not named. Gap: an explicit example of a swapped function-pointer global. |
| 3 | Tests configure an instance, not a saved and restored global. | **covered**: `mod-no-module-mutable-state` | Card Why: "Hidden global state leaks between tests"; PASS example uses a class instance. |

## 2. Buf lint rules

URL: https://buf.build/docs/lint/rules/
Fetch status: ok (summarized). Rule names below come from the summary; confirm them on the live page before any citation.

| # | Rule | Coverage | Evidence |
|---|---|---|---|
| 1 | `ENUM_ZERO_VALUE_SUFFIX`: the zero value of every enum ends in `_UNSPECIFIED`. | **covered**: `mod-proto-enum-zero-unspecified` (draft) | Card `tool_gate`: "Protobuf linter (`buf lint`, ENUM_ZERO_VALUE_SUFFIX)." Card already cites buf.build/docs/lint/rules/. |
| 2 | `IMPORT_USED`: every declared import is referenced. | **NEW candidate** | Nearest checked: `mod-no-import-cycles` (cycles only), `mod-no-import-side-effects`. No card covers an unused import. Needs three orgs. Possible sources not yet checked: Go spec (the compiler rejects unused imports), Pylint W0611, ESLint `no-unused-vars`. |
| 3 | `FIELD_NOT_REQUIRED`: no `required` fields in proto2 or Editions. | **NEW candidate** (previously dropped) | `docs/COVERAGE.md` line 515: "protobuf.dev: No required fields \| dropped: narrow, no card yet". Buf is a second source for the same rule. Needs a third org, for example Google's protobuf style guide or another lint tool. |

## 3. AWS Prescriptive Guidance, hexagonal architecture

URL: https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html
Fetch status: ok. The page is long; the summary was taken from the Intent, Issues and considerations, and Implementation sections.

| # | Rule (paraphrase) | Coverage | Evidence |
|---|---|---|---|
| 1 | Business logic talks to the outside only through ports; adapters translate. Quote: "Ports connect to the application, and adapters serve as a connection to the outside world." | **covered**: `mod-layers-point-inward` (stable) | Card Rule: "Make dependencies point inward"; PASS: "service takes plain domain types". The card already cites this URL. |
| 2 | An adapter is justified only with several inputs or outputs, or when the store has to change. Quote: "The additional adapter code ... is justified only if the application component requires several input sources and output destinations." | **partial**: `mod-layers-point-inward`, `mod-yagni` | `mod-layers-point-inward` counterpoint says three layers is ceremony for a CRUD app. Gap: the adapter-count test itself, meaning when an adapter layer pays off. Not checked by any card. |
| 3 | Domain logic is unit-tested without infrastructure. Quote: "You can test components independently without any dependencies on the infrastructure code." | **covered**: `mod-layers-point-inward` | Card Why: "you cannot reuse or test the logic without the transport". |

## 4. Refactoring.guru, Temporary Field

URL: https://refactoring.guru/smells/temporary-field
Fetch status: ok (summarized).

| # | Rule (paraphrase) | Coverage | Evidence |
|---|---|---|---|
| 1 | Flag a field used only inside one method's algorithm. Quote: "These fields are used only in the algorithm and go unused the rest of the time." | **partial**: `mod-temporary-field` (draft) | The card covers a field assigned and read in one method. Its note says Refactoring.guru "is a different smell" and "backs the name and not the trigger". The trigger here is the JetBrains/Sonar/PMD one. |
| 2 | Flag an object field that is almost always empty. Quote: "You expect to see data in object fields but for some reason they're almost always empty." | **NEW candidate** | Nearest checked: `mod-temporary-field` (the note excludes this trigger), `mod-behaviour-lives-with-state`. Needs three orgs. Refactoring.guru is one; Fowler's book and one tool with a conditional-field check would be the next candidates. |
| 3 | Move a cluster of temporary fields and their code into its own class. Quote: "Temporary fields and all code operating on them can be put in a separate class." | **partial**: `mod-temporary-field` | Card note names Extract Class as the fix, but no card states the cluster-to-class rule. |

## 5. Refactoring.guru, Inappropriate Intimacy

URL: https://refactoring.guru/smells/inappropriate-intimacy
Fetch status: ok (summarized).

| # | Rule (paraphrase) | Coverage | Evidence |
|---|---|---|---|
| 1 | A class reads or writes another class's internals. Quote: "Good classes should know as little about each other as possible." | **covered**: `mod-internals-unreachable` (stable) | The card's member half cites Refactoring.guru's intimacy page. |
| 2 | Pairs of classes that work together constantly should be checked for a misplaced method or field. Quote: "Keep a close eye on classes that spend too much time together." | **NEW candidate** | Nearest checked: `mod-fowler-smells` (names feature envy, one object's own fields used elsewhere), `mod-behaviour-lives-with-state`. The pair-chatter trigger is not stated by any card. Needs three orgs. Fowler's book and a second source on feature envy or coupling would be the next candidates. |
| 3 | Mutual references between two classes should be cut to one direction. Quote: "If the classes are mutually interdependent." | **partial**: `mod-no-import-cycles` | Card covers cycles between modules and packages ("break a cycle"). It does not cover class-level mutual references. |

---

## Summary

| Source | Rules | Covered | Partial | NEW |
|---|---|---|---|---|
| Uber mutable globals | 3 | 2 | 1 | 0 |
| Buf lint | 3 | 1 | 0 | 2 |
| AWS hexagonal | 3 | 2 | 1 | 0 |
| Refactoring.guru temporary field | 3 | 0 | 2 | 1 |
| Refactoring.guru inappropriate intimacy | 3 | 1 | 1 | 1 |
| **Total** | **15** | **6** | **5** | **4** |

Lead list (NEW candidates, none to be carded yet):
- Unused import (Buf `IMPORT_USED`). Needs three orgs. Go spec, Pylint or ESLint are candidates.
- Proto `required` fields (Buf `FIELD_NOT_REQUIRED`). Second source; needs a third.
- Almost-always-empty object field (temporary field, rule 2). Needs Fowler plus one more.
- Class pairs that constantly work together (intimacy, rule 2). Needs Fowler plus one more.

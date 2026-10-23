# Browser pass: code review sources (2026-10-23)

Raw extracted text lives outside the repo at `/tmp/claude-1000/-home-pablo-dev/adeab644-096d-471c-8405-57866ddb64b4/scratchpad/raw/`. Quotes below are kept to 15 words or fewer; everything else is paraphrased.

Status summary: 4 of 8 items read in full (Tef, Palantir, McIntosh, Fagan), 1 read secondhand (Ousterhout red flags), 1 partially (Sapling), 2 not reachable (Beller, Mäntylä), 1 not obtainable in usable form (McConnell ch.21), 1 not located (Block).

---

## 1. Tef — "Write code that is easy to delete, not easy to extend"

- **URL read:** https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to (dated 2016-02-13)
  - A guessed slug returned a 403 "Checking your browser" page and then a 404. The correct URL came from a search result.
- **Author/org:** Tef (blog "programming is terrible"), individual author.
- **Summary:** The post argues for treating lines of code as recurring cost and for designing so parts can be deleted or replaced without rewriting others. Its 7 steps move from copy-paste, through utils, boilerplate and layering, to feature flags and piecemeal deletion.
- **Reviewable CHECKS**
  - FAIL if a shared helper is extracted after its first use, before at least two real callers exist (Step 1: copy-paste a couple of times first).
  - FAIL if new logic goes into a single catch-all `util` file (Step 2 aside).
  - FAIL if a public API leaks a third-party library's types, instead of wrapping them (Step 4).
  - FAIL if a module holds two independent hard decisions and changing one requires editing the other (Step 6).
  - FAIL if a long-lived feature branch has no runtime or flag-based way to switch it off (Step 7).
- **Empirical vs opinion:** Opinion/essay. It cites Parnas, Brooks, Perlis and similar, but reports no measurements. Empirical claims are anecdotal (e.g., Chrome release cycle, Erlang supervision).
- **Exact numbers:** None of substance. The only numbers are illustrative line counts ("50, 500, 5,000, 10,000, 25,000") and "18 smaller interleaved mistakes".
- **Caveat on the raw file:** The reading list at the end is condensed to titles, not verbatim (noted in the raw file header).

---

## 2. McConnell — Code Complete ch.21 "Collaborative Construction"

- **URL read:** Not usable. The chapter body is not in any source I could reach legitimately:
  - O'Reilly and Eyrolles: not opened (paywalled book listings).
  - Cisco Press sample PDF (https://www.ciscopress.com/content/images/9780735619678/samplepages/9780735619678a.pdf): 113 pages, read with `pdftotext`. It is front matter. Chapter 21 appears only in the table of contents (book p. 479) and in cross-references from other chapters. The chapter text is absent.
  - A GitHub-hosted text file of the book came up in search. I did not use it, because it is probably an unlicensed copy.
- **Author/org:** Steve McConnell, Microsoft Press / Code Complete 2nd ed.
- **Summary:** Not read. The TOC lists 21.1 overview, 21.2 pair programming, 21.3 formal inspections, 21.4 other practices.
- **Reviewable CHECKS:** None extracted.
- **Empirical vs opinion:** Not determined.
- **Numbers:** None extracted.
- **Raw file:** `02-mcconnell-cisco-sample.txt` (sample front matter only).

---

## 3. Palantir — "Code Review Best Practices"

- **URL read:** https://blog.palantir.com/code-review-best-practices-19e02780015f (Medium-hosted, Mar 4 2018, 12 min read). Full article was readable without login.
- **Author/org:** Palantir (engineering blog). Copied from the best-practice guide of their Java tool chain, Baseline.
- **Summary:** A practice guide covering when to review, how to prepare a change, what reviewers should check, and how to write review comments. It is an internal-policy style document, not research.
- **Reviewable CHECKS**
  - FAIL if a CR touches more than about 5 files, takes more than 1–2 days to write, or takes more than 20 minutes to review, and is not split.
  - FAIL if a CR mixes a refactor with a behavior change.
  - FAIL if commit summary exceeds 80 characters, is not in imperative mood, or has no blank line before the body.
  - FAIL if the diff contains commented-out code, or a TODO without an issue reference.
  - FAIL if new logic has no test, or the CR lowers test coverage.
  - FAIL if a CR is merged without automated checks passing first.
  - FAIL if fixes made during review are squashed into the earlier commit, instead of added as a separate commit.
  - FAIL if a review comment uses absolute judgments ("this can never work") or possessive blame ("your method has a bug").
  - FLAG a CR with more than three reviewers, which the guide says is often counter-productive.
- **Empirical vs opinion:** Opinion and practice. One claim is attributed to unnamed studies ("Studies have found that even short and informal code reviews have significant impact on code quality"). No citation given.
- **Exact numbers:** "more than ~5 files", "1–2 days", "20 minutes to review", "hours, not days" (review turnaround), "more than three parties". These are policy thresholds, not measurements.

---

## 4. McIntosh, Kamei, Adams, Hassan — "The Impact of Code Review Coverage and Code Review Participation on Software Quality" (MSR 2014)

- **URL read:** https://rebels.cs.uwaterloo.ca/papers/msr2014_mcintosh.pdf (downloaded with curl, text extracted with `pdftotext -layout`). The browser's PDF viewer gave no text.
- **Author/org:** Queen's University, Kyushu University, Polytechnique Montréal. DOI 10.1145/2597073.2597076.
- **Summary:** Mines Gerrit review data for Qt, VTK and ITK and builds regression models on post-release defects. Finds that both low review coverage and low participation are associated with more post-release defects. Associations only, not causation.
- **Reviewable CHECKS**
  - Coverage: FLAG a component whose share of reviewed changes is below 0.29 (VTK) or 0.6 (Qt). The paper says such components are expected to contain at least one post-release defect.
  - Participation: FLAG a component where more than 0.71 of changes have no discussion. The paper estimates at least two post-release defects in both Qt releases studied.
  - Abstract: "up to two" additional defects for low coverage and "up to five" for lax participation.
- **Empirical vs opinion:** Empirical. Observational mining of three projects. Models are multiple linear regression with VIF filtering. Adjusted R² around 0.19–0.44 across models. Authors note limits (for example, only 2–14% of some projects' changes could be linked to reviews).
- **Exact numbers and where they appear**
  - Abstract: "up to two" (coverage) and "up to five" (participation) additional post-release defects per component.
  - Results (RQ1): coverage thresholds 0.29 (VTK) and 0.6 (Qt).
  - Participation: the 0.71 "without discussion" threshold, and the 0.1 / 0.13 proportions that the Qt 5.1.0 model expects to produce defects.
  - Filtering: 90% (1,201/1,339) of Qt 5.0.0 components survived filtering. Only 5% (8/170) of VTK components did.

---

## 5. Fagan — "Design and code inspections to reduce errors in program development" (IBM Systems Journal, 1976)

- **URL read:** https://www.ida.liu.se/~TDDC90/labs/lab-papers/fagan76.pdf. This is a Linköping course copy, not IBM's archive. Downloaded with curl and extracted with `pdftotext`. It is a 30-page scan with OCR errors ("eficient", "verijicution", "andof"). Figures are read from the OCR and checked against context where possible.
- **Author/org:** M. E. Fagan, IBM. IEEE record: IBM Systems Journal vol. 15, no. 3, pp. 182–211.
- **Summary:** Describes formal design and code inspections with defined roles, exit criteria and data collection. Reports large error-detection efficiency and productivity gains in a few industrial projects, with a feedback loop on error rates.
- **Reviewable CHECKS**
  - FAIL if an inspection session runs longer than two hours, or more than two sessions per day (paper's recommendation).
  - FAIL if more than 5% of inspected material is reworked and no full reinspection is scheduled.
  - FAIL if inspection roles (moderator, author, reader, recorder) and entry/exit criteria are undefined.
  - FLAG if defect data is not categorized, so process improvement cannot be measured.
- **Empirical vs opinion:** Empirical but thin. Small projects, industrial anecdotes, a few tables. The paper is the original, so it is primary.
- **Exact numbers and where they appear**
  - Table 1: inspection error-detection efficiency **82%** (38 of 46 errors per KNCSS found by design and code inspections).
  - Application case: a 4,439-line COBOL module finished in 46.5 programmer-days vs 62 predicted, a **25%** resource saving.
  - Inspection sample vs walkthrough sample: **38% fewer** errors per KLOC during test (figure caption).
  - Session length: efficiency "tends to dwindle after two hours" (section on scheduling).
  - Reinspection trigger: **5%** reworked material.
  - Claim not found: the "60–90% of defects" figure that secondary sources attribute to this paper does not appear in the extracted text. Do not cite it from this source.

---

## 6. Ousterhout — red flags (A Philosophy of Software Design)

- **URL read:** Not the book or a talk transcript. Only a secondhand transcription: https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2 (Sébastien Portebois, Apr 2021, notes.portebois.net). The author states it is a partial list of the flags "scattered throughout the book".
- **Author/org:** John Ousterhout (Stanford). The summary is by a third party.
- **Summary:** The book flags design smells, each with a chapter reference. Several are listed below, with the chapter references as given in the secondary summary.
- **Reviewable CHECKS** (from the secondary list; verify against the book)
  - FAIL: shallow module, interface nearly as complex as the functionality it hides (4.6).
  - FAIL: information leakage, same format knowledge in two classes (5.2).
  - FAIL: temporal decomposition, code split by execution order instead of by knowledge (5.3).
  - FAIL: pass-through method that only forwards its arguments (7.1).
  - FAIL: repetition of near-identical code, meaning missing abstraction (9.4).
  - FAIL: special-general mixture, specialized code inside a general mechanism (9.5).
  - FAIL: conjoined methods, one cannot be understood without reading the other (9.8).
  - FAIL: comment repeats the code's words (13.2).
  - FAIL: vague name that could refer to many things (14.3).
  - FAIL: nonobvious code with no explanatory comment (18.2).
- **Empirical vs opinion:** Opinion and design heuristics. No measurements.
- **Numbers:** None.
- **Not done:** Ousterhout's own talk or a full book read. Flagged as unfinished.

---

## 7. Square/Block and Sapling docs (stacked diffs, code review)

- **URLs read**
  - Sapling docs: https://sapling-scm.com/docs/introduction/ and https://sapling-scm.com/docs/overview/stacks. Sapling is Meta's source control system.
  - Block: https://engineering.block.xyz/blog/. The page loaded, but the link list showed no code-review or stacked-diff posts.
- **Author/org:** Meta (Sapling). Block (engineering blog).
- **Summary:** Sapling's stacks page documents amend, fold, split, absorb and amend `--to` on commit stacks. It covers the tool's mechanics, not review policy. Block: no relevant post found.
- **Reviewable CHECKS:** None on review policy. The stacks page is tool documentation. A review-related check that follows from it: a stack should keep each commit independently reviewable. This is my inference, not from the page.
- **Empirical vs opinion:** Documentation. No evaluation.
- **Numbers:** None relevant.
- **Not found:** Review-specific Sapling content (Phabricator / submit workflow) was not on the pages read. Block's stacked-diff or review post was not found.

---

## 8. Mäntylä & Lassenius (2009) and Beller et al. (2014) — defect/maintainability percentages

### Beller et al., "Modern Code Reviews in Open-source Projects: Which Problems Do They Fix?" (MSR 2014, pp. 202–211, DOI 10.1145/2597073.2597082)

- **Status: not read.** The TU Delft repository PDF timed out with both curl and the browser. The Zenodo record (`https://zenodo.org/records/268478`) holds the dataset only, not the paper.
- **Numbers from search snippets only (unverified against the PDF):** more than 1,400 changes classified; roughly 75:25 maintainability vs functional; 7–35% of review comments discarded; 10–22% of changes not triggered by a review comment. Do not cite these until the paper is read.

### Mäntylä & Lassenius, "What Types of Defects Are Really Discovered in Code Reviews?" (IEEE TSE 35(3), 2009, pp. 430–448, DOI 10.1109/TSE.2008.71)

- **Status: not read.** The paper URL in the search results (lib.tkk.fi, Aalto) redirected to an unrelated repository search page.
- **Conflicting secondary numbers, do not cite:** 77% evolvability / 23% functional (arXiv 2024 paper); 71% maintainability / 21% functional / 7% false positives (slide deck); 60–75% evolvability (2011 Java Code Geeks post); "up to 75%" (Wikipedia).

---

## Not obtained: summary

| Item | Why |
|---|---|
| McConnell Code Complete ch.21 | Chapter not in the legitimate sample; O'Reilly paywalled; unofficial text not used |
| Beller et al. 2014 | TU Delft PDF timed out (curl + browser); no other legitimate copy found |
| Mäntylä & Lassenius 2009 | Repository link redirected to an unrelated page; no other copy found |
| Block engineering code-review post | Not located on the blog listing or by search |
| Ousterhout primary text | Only a third-party red-flags summary was read |

## Notes on method

- Browser text extraction failed for PDFs (Chromium's PDF viewer exposes no text). PDFs were downloaded with `curl` into separate empty directories under the scratchpad and extracted with `pdftotext`. The downloaded PDFs are in `.../scratchpad/pdf-*/`, outside the repo.
- Browser sessions were used for HTML pages. No login or CAPTCHA was bypassed. The Tef interstitial was a plain "checking your browser" page and cleared on its own.
- The Palantir raw file flattens the code-example blocks. The Tef raw file condenses the reading list. Both are noted in their headers.

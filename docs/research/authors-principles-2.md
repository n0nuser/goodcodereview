# Authors' principles, batch 2 (research notes for goodcodereview.com)

Method note: pages were fetched with WebFetch, which returns a model-written digest of the page, not raw text. Each digest was read in full, but wording below is paraphrase of digests, so spot-check anything before quoting. "Opinion" = author's judgment or anecdote. "Evidence" = data, benchmark or checkable example.

## Pages read

Tier A: primary page fetched and digest read (12).

1. https://github.com/johnousterhout/aposd-vs-clean-code/blob/main/README.md
   Ousterhout and Robert Martin. First ~100k of 123k chars read, so the TDD section is truncated. Debate on function length, comments, TDD. Mostly opinion; one reproducible benchmark (splitting a hot loop into methods was reported 3-4x slower; Martin's later version reported faster) and one verifiable wrong comment.
2. https://www.hyrumslaw.com/ (Hyrum Wright; naming credited to Titus Winters). With enough users, every observable behavior gets depended on. Observation from large-scale change work at Google; not a measured result.
3. https://www.joelonsoftware.com/2000/04/06/things-you-should-never-do-part-i/ (Joel Spolsky). Do not rewrite working code from scratch. Evidence is anecdotal case studies (Netscape 6, Borland); causation asserted, not shown. Opinion.
4. https://kentcdodds.com/blog/aha-programming (Kent C. Dodds). Avoid Hasty Abstractions: duplicate until the pattern is clear, prefer duplication to the wrong abstraction (credits Sandi Metz). Opinion with two personal anecdotes.
5. https://blog.pragmaticengineer.com/good-code-reviews-better-code-reviews/ (Gergely Orosz). "Good vs better" reviewer behaviour, from industry experience. Opinion/experience, no data.
6. https://github.com/matthiasn/talk-transcripts/blob/master/Hickey_Rich/HammockDrivenDev.md (Rich Hickey, Clojure/Conj 2010 transcript). Most serious defects are misunderstood problems; state the problem, list alternatives. Self-described experience report; opinion. Not about code review directly; checks below are derived.
7. https://michaelfeathers.silvrback.com/characterization-testing (Michael Feathers). Write tests that record what legacy code does now, before changing it. Practice/opinion; no formal checklist in the page.
8. https://google.github.io/eng-practices/review/reviewer/standard.html (Google). Approve once a change definitely improves code health; style guide is authority; data over preference; consistency as a tie-breaker. Institutional policy; opinion backed by experience, no data.
9. https://danluu.com/tests-v-reason/ (Dan Luu). Testing vs informal reasoning (reply to "Out of the Tar Pit"). Mix of examples (Intel bug, Euclid error) and personal anecdote. Not about code review; review implications are inference.
10. https://danluu.com/bug-blind/ (Dan Luu). People stop noticing bugs they work around. Anecdotal, self-selected examples, author says so. Not about code review.
11. https://www.hillelwayne.com/post/hoc/ (Hillel Wayne). Hierarchy of controls from safety engineering applied to software (eliminate, substitute, engineer out, administer). Ranking is from OSHA/NIOSH; software application is his reasoning.
12. https://www.hillelwayne.com/post/lsp/ (Hillel Wayne). Subclass should pass the parent's black-box tests; restates the Liskov rules (preconditions, postconditions, invariants, history). Rules are standard; the teaching claim rests on informal testimony.

Tier B: page fetched, but content limited, secondary, or paywalled (6). Do not cite as the author's argument.

13. https://newsletter.kentbeck.com/p/management-separate-tidying (Kent Beck). Only the free opening visible: tidyings in the same PR make reviewers complain it is too long. Paywalled rest.
14. https://newsletter.kentbeck.com/p/getting-untangled (Kent Beck). Free part: three options for a tangled change (ship as is, untangle into separate PRs/commits, discard and redo tidying first); first is called impolite to reviewers. Paywalled rest.
15. https://newsletter.kentbeck.com/p/batch-sizes (Kent Beck). Free part: tidying is structural change supporting the next behavior change; rest paywalled.
16. https://henrikwarne.com/2024/01/10/tidy-first/ (Henrik Warne, review of Beck's book). SECONDARY. Source for the tidying list, the S/B separation rule, and "tidy first / after / later / never".
17. https://dev.to/sportebois/software-design-red-flags-wisdom-nuggets-from-john-ousterhout-43i2 (Sylvain Porteboeuf). SECONDARY list of Ousterhout's 14 red flags, not the book.
18. https://blog.ploeh.dk/2023/04/24/are-pull-requests-bad-because-they-originate-from-open-source-development/ (Mark Seemann). SECONDARY on Dave Farley's pull-request position; quote's original source is unverified.

## Checks by theme

Each check is phrased as a question a reviewer can ask. Source number in brackets.

### 1. Consistency with the codebase vs improving it
- Does this change leave the codebase healthier, even if not perfect? If yes, lean to approve rather than hold for polish. [8]
- Is each comment either blocking or marked non-blocking ("nit")? Educational or taste comments should say they are optional. [8, 5]
- Is a style objection backed by the written style guide? If not, treat it as preference. [8]
- Where no rule applies, is the request "match nearby code" only made when it does not make the code worse? [8] Consistency is a tie-breaker, not a trump card.
- Is the objection about design based on principle or data, rather than taste? If the author shows two approaches are equally valid, accept theirs. [8]
- Are repeated nitpicks pointing to a missing linter or agreed convention? Automate instead of commenting. [5]
- Does the new code look like it was written for this system (follows existing architecture), or does it add a new pattern for one use? [5 "better" reviews check new abstractions against existing architecture]
- If it does depart from the existing pattern, is the reason stated and is the old pattern marked for migration, not left as a silent second way? (Inferred from [8],[5]; neither says this outright.)
- Does the PR keep style-only edits (rename, reformat) apart from logic edits so each can be checked? [3 as review check, 16, 13/14]

### 2. Reusability and where code lives
- Is this the second copy or the third? One duplicate is tolerable; ask about abstraction at the third. [4, weak heuristic]
- If an abstraction is introduced, do the call sites share structure that has stayed stable? Or is the shape guessed from one or two uses? [4]
- Does an existing abstraction now carry growing flags/conditionals so callers can bend it? Treat as a wrong-abstraction sign; consider inlining and re-duplicating. [4]
- Is knowledge (a file format, a rule, a constant) held in one place, or leaked into several modules that must change together? [17, 1]
- Is the module deep (small interface hiding real work), or shallow (interface about as complex as the code)? Flag pass-through methods, pass-through variables, wrappers that add nothing. [17, 1]
- Is the code split by when things happen (read, then parse, then write) instead of by what knowledge each piece owns? [17]
- Does a general-purpose mechanism contain code for one special caller? Move the special case out. [17]
- Can each new function/class be understood without opening its neighbours? If two methods only make sense together, consider merging them. [17, 1]
- Is a split into many small functions making the reader jump around? Is a split inside a hot loop measured? [1] Ousterhout and Martin disagree here (see Disagreements).
- Does a new base/derived relationship pass the parent's tests: no stricter inputs, no weaker outputs, no broken invariants, no state change the parent forbids? [12]
- Where does a fix sit? Check blame/history before moving or "simplifying" an odd-looking piece of code; it may hold a fix for a real bug. [3]

### 3. Characterization and legacy handling
- Before behavior in untested legacy code changes, is there a test that records what it does today? [7]
- Does the new test assert observed behavior (not what we wish it did)? [7]
- If a test failed after the change, was the behavior change intended, and is it stated in the PR? [7]
- Was surprising behavior kept (and recorded in a test) when nobody could say whether it is a bug? [7] Callers may rely on it.
- Are test names updated to say what the code is now understood to do? [7]
- Does the change alter any observable behavior (ordering, timing, error shape, defaults), not only the documented contract? Assume somebody depends on it; ask about staged rollout, flags, notice to known consumers. [2]
- For a rewrite or "cleanup": can it be split into small shippable steps? Does the old path keep working during it? Is there a stated problem (architecture, performance with a profile, style) that a rewrite is the only fix for? [3]
- Is the claim "the old code is a mess" backed by a named defect? Reading code is harder than writing it, so dislike alone is weak evidence. [3, opinion]
- Do existing tests pass unchanged for a pure refactor? If tests had to change, is that explained? (Derived from [3],[7].)
- Is reasoning ("I checked, it's correct") backed by a test for the tricky or stateful part? [9, inference]

### 4. Deletability
Note: Tef's article could not be fetched (see Not found). These checks come from other sources only.
- Does the PR delete what it makes dead (unused functions, flags, commented-out code, old paths)? [16 "delete dead code"]
- Is a speculative extension point being added for a need that does not exist yet? [4 "optimize for change" is about easy change, not built-in flexibility; 16 tidy only for the next change in hand]
- Would removing this feature later require touching many modules? Check for tangled coupling: cost of change tracks coupling. [16, citing Beck's theory; opinion]
- Does a duplicate-first choice keep each copy easy to remove or alter independently? [4]
- For any new safeguard, is it at the strongest level possible: remove the hazard, or make the mistake impossible in code, before relying on a written rule or a human check? [11]

### 5. Structure of the change itself
- Is tidying separate from behavior change, at least in separate commits, ideally separate PRs? [16, 13, 14]
- Is the PR too large to review? Ask to split. [5, 13]
- Does the tidying serve the behavior change in hand, not a distant hope? [15]
- If the change is tangled, was it untangled (rebase/split) or redone tidy-first? Shipping it tangled is the worst option for the reviewer. [14]
- Is the problem stated in the description (what, why, constraints, open questions)? [6, 5]
- Were at least two approaches considered, and does the text say what the chosen one costs? Listing only the chosen design's flaws is not a trade-off. [6, opinion]
- Does the change fix the cause or work around the symptom? [6]

### 6. Readability and comments (Ousterhout's flags as questions)
- Does each comment add information the code lacks (why, units, what callers may rely on)? Delete restatements. [17, 16]
- Does interface documentation leak implementation detail? [17]
- Is a name vague (could mean many things) or hard to pick? Treat as a design smell. [17]
- Can the behavior be understood on a quick read? If not, fix code or comment. [17]
- Is each comment still true? A wrong comment is checkable; both sides in [1] agree comments need checking against code.

### 7. Reviewer conduct and process
- Ask questions and offer alternatives instead of verdicts; assume missing context. [5]
- Do not approve with open questions; label non-blocking items. [5]
- Many comments after a first pass: talk to the author; likely a misunderstanding. [5]
- Do not let a disagreement stall the change: agree on principle, then call, then escalate. [8]
- Test as a new user would; do not count a habitual workaround as acceptable. [10]
- Bring in a reviewer who has not adapted to the project's quirks. [10, opinion from anecdotes]

## Disagreements

- Function length and decomposition: Martin prefers many very short functions and says he would err toward decomposition; Ousterhout says that creates shallow, entangled methods and slows hot paths. Evidence is thin (one benchmark, disputed in follow-ups). Treat the check "does splitting help a reader here?" as local judgment, not a rule. [1]
- Comments: Martin treats comments as a necessary evil and prefers names; Ousterhout says missing comments cost much more than wrong ones (his 10-100x figure is anecdotal). [1]
- TDD vs writing tests after a small unit: unresolved in the part I read; Ousterhout concedes his book mis-described TDD. [1]
- DRY vs duplicate-first: Dodds (AHA) and Metz prefer duplication over a wrong abstraction; Ousterhout lists repetition as a red flag. They can be reconciled: Ousterhout's flag asks "is this one piece of knowledge in many places?", AHA asks "is the abstraction proven?". No data either side. [4, 17]
- Rewrite vs incremental: Spolsky argues against rewrites; Hickey's talk argues for stepping back to restate the problem, which can lead to a different design. They conflict only if "rethink" means "rewrite"; neither provides measured outcomes. [3, 6]
- Consistency vs improvement: Google asks to favour improvement over perfection and uses consistency as a tie-breaker; a reviewer insisting on matching surrounding code at the cost of readability goes against that. [8]
- Pull-request review vs alternatives: Farley (as reported by Seemann, quote unverified) says PRs are gatekeeping suited to untrusted contributors and prefers pairing; Seemann replies that review also finds defects and spreads understanding. Neither side gives data. [18]
- Tests vs reasoning: Luu argues informal reasoning cannot cover complex systems, so tests are needed. Relevant to reviewers who sign off on "looks correct". Based on examples, not studies. [9]
- Tidying in the same PR or not: Beck says it irritates reviewers; the book's guidance is to separate, though the free posts show he found it costly in PR-based workflows. [13, 14, 16]

## Not found

- Tef, "Write code that is easy to delete, not easy to extend": every fetch of programmingisterrible.com returned 403, including a mirror redirect. I did not read the article; only a search summary exists (reusable code creates dependencies, isolate what changes, write less). Deletability checks above rely on other sources. Retry from a browser.
- Dan Luu on code review: danluu.com/code-review/ returned 404; the site index lists no code-review post. The two Luu pages read are about testing and bug noticing.
- Julia Evans (jvns.ca): no post on code review or giving feedback found; /blog/ and /blog/2025/ gave 404. Search only hinted at a git-review-commits tool she wrote about.
- Jessica Kerr: searched; found profiles only, no code-review post.
- Hillel Wayne: no post on code review or legacy code on his post list. Read two related posts (hoc, lsp).
- Michael Fagan 1976 inspection paper: PDF is scanned images; text not extractable (saved at /home/pablo/.claude/projects/-home-pablo-dev/adeab644-096d-471c-8405-57866ddb64b4/tool-results/webfetch-1792787522769-67ws53.pdf; OCR needed). Search results only confirmed publication details (IBM Systems Journal 15(3), 1976) and that it recommends classifying errors by type to build checklists. Claims like "inspections remove 60-90% of defects" are from secondary sites and unverified.
- McConnell, Code Complete ch. 21: O'Reilly page returned 403; only the chapter outline (pair programming, formal inspections, other practices, comparison) and secondary slide figures were seen (55-60% defects found by inspection vs about 35% in low-volume beta testing; 20-80% error reduction). Unverified; do not cite.
- Ousterhout's own red-flags summary: his book page has only the second-edition notice; the YouTube talk could not be fetched. The red flags come from a secondary summary (#17). The book's own summary list is the authority.
- Dave Farley / Jez Humble primary text: davefarley.net post found did not discuss review; Farley's PR claim only seen second-hand (#18). Humble not covered.
- Kent Beck's own PR-separation argument is behind a paywall; rules come from the Warne review (#16).
- Kent C. Dodds: only AHA read. Tef, Fagan, McConnell, Farley, Beck paid text: all need a second pass.

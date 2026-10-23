# Code review culture and evidence: research notes

Fetched 2026-10-23. "Read" = page or PDF fetched and summarised via WebFetch (a small model summarises the page; it is not a verbatim read). Evidence label per page: EMPIRICAL (data), OPINION (practitioner judgment), MIXED.

## Pages read

1. https://google.github.io/eng-practices/review/reviewer/looking-for.html. Google, "What to look for in a code review". Checklist of review dimensions. OPINION (cites no data).
2. https://google.github.io/eng-practices/review/reviewer/standard.html. Google, "The Standard of Code Review". Approve once a change clearly improves code health, even if imperfect; facts beat preferences. OPINION.
3. https://sback.it/publications/icse2018seip.pdf. Sadowski, Söderberg, Church, Sipko, Bacchelli, "Modern Code Review: A Case Study at Google", ICSE-SEIP 2018. Interviews, a survey, and logs of about 9M reviewed changes with 13M comments. EMPIRICAL. Read from the PDF text with pdftotext. Numbers below come from that text.
4. https://www.microsoft.com/en-us/research/publication/expectations-outcomes-and-challenges-of-modern-code-review/. Bacchelli and Bird, ICSE 2013, Microsoft. Only the abstract page was read, not the full paper. EMPIRICAL (observation, interviews, survey, hand classification of hundreds of comments). Finding: reviews are less about defects than expected. Knowledge transfer, team awareness and alternative solutions matter. Understanding the change is the main challenge.
5. https://www.microsoft.com/en-us/research/publication/characteristics-of-useful-code-reviews-an-empirical-study-at-microsoft/. Bosu, Greiler, Bird, MSR 2015. 1.5M comments from 5 Microsoft projects. EMPIRICAL. Larger changes (more files) have a lower share of useful comments. Reviewer usefulness rises sharply in the first year.
6. Local PDF of Czerwonka, Greiler, Tilford, "Code Reviews Do Not Find Bugs" (Microsoft, ICSE-SEIP 2015 talk abstract). It was reached through the URL microsoft.com/en-us/research/wp-content/uploads/2015/05/PID3556473.pdf, which carries the PDF title "IEEE Paper Template". EMPIRICAL, but a short talk abstract with no methods. About 15% of comments indicate a possible defect and at least 50% concern long-term maintainability. Reviewer usefulness is about 33% on a first review of an area, about 67% on the third, then the long-run average. Usefulness drops from about 20 changed files. Median time to sign-off is about 24 hours, and developers spend about 6 hours a week reviewing.
7. https://smartbear.com/learn/code-review/best-practices-for-peer-code-review/. SmartBear, Cisco study write-up. MIXED. The page ties 200-400 LOC per review and the drop-off past 400 to the Cisco study, and it ties lightweight review taking under 20% of formal-inspection time with equal bugs found to that study too. The 500 LOC/hour rate is attributed to "SmartBear research", and the checklist claim has no cited data. The commercial source is a caveat. The original Cisco report was not read.
8. https://engineering.fb.com/2022/11/16/culture/meta-code-review-time-improving/. Meta Engineering, "Time In Review". MIXED. Goal metric is P75 Time In Review. Guardrail is "eyeball time", to catch rubber-stamping. Nudgebot is reported at -7% average Time In Review and -12% of diffs waiting over 3 days, from an experiment with no variance or significance reported. The reviewer-recommender gain is +1.5% of diffs reviewed within 24h. "Next Reviewable Diff" is reported at +17% review actions, a correlational result.
9. https://newsletter.pragmaticengineer.com/p/stacked-diffs. Gergely Orosz, "Stacked diffs". Secondary source, OPINION and reporting. Meta, Google (chained CLs) and Uber use stacking. Claimed benefits are small, independently reviewable and revertable changes. Downsides are tooling cost and rebasing pain. About 200 changed lines per PR is a rule of thumb.
10. https://go.dev/wiki/CodeReviewComments. Go project, 31 check items. OPINION and project convention.
11. https://docs.kernel.org/process/submitting-patches.html. Linux kernel. Convention, OPINION. It sets the meaning of Reviewed-by, Acked-by and Tested-by tags.
12. https://devguide.python.org/getting-started/pull-request-lifecycle/. CPython devguide. Reviewer and contributor checks. Convention.
13. https://www.kubernetes.dev/docs/guide/pull-requests/. Kubernetes, PR and reviewer guidance. Convention. The size/S..XXL labels exist but the thresholds are not defined on the page.
14. https://rustc-dev-guide.rust-lang.org/pr-lifecycle.html. Rust compiler dev guide. Process only: r+, bors, status labels, incremental commits during review. It has no reviewer checklist and no size guidance. The sibling page contributing.html has no review content.
15. https://secure.phabricator.com/book/phabflavor/article/writing_reviewable_code/. Phabricator docs (the review tool Meta's Differential came from). OPINION, with one data point: median Phabricator change is about 35 lines.
16. https://slack.engineering/how-about-code-reviews/. Slack Engineering. OPINION. The review is about people and communication.
17. https://www.linkedin.com/blog/engineering/developer-experience-productivity/scaling-collective-code-ownership-with-code-reviews. LinkedIn Engineering, Nikolai Avteniev, 2018. MIXED. It mostly relays Cisco and Microsoft findings and publishes no LinkedIn numbers of its own.
18. https://tidyverse.org/blog/2023/06/code-review-principles/. Posit/tidyverse announcement, adapted from Google's guide. Thin, since the fetched page only links to the full guide at code-review.tidyverse.org. That guide was not read.
19. https://dropbox.tech/culture/beyond-code-generation-rethinking-engineering-productivity-in-the-age-of-ai-agents. Dropbox. It names code review turnaround as a quality signal and gives no numbers. Little review content.

## Checks by theme

Each check is tagged with the page number(s) above.

### Design and fit
- Does the change belong in this codebase and fit the system, and is now the right time for it? [1]
- Judge design on engineering principles, not taste. If the author shows several options are equally valid, accept theirs. [2]
- Look at the surrounding file and system, not only the diff. Small degradations accumulate. [1]
- Interfaces: declare them where they are consumed, return concrete types, and avoid speculative interfaces. [10]
- Prefer synchronous APIs, because callers can add concurrency more easily than remove it. [10]
- Raise design problems early. Google interviewees reported friction when reviewers and authors disagreed on whether review is the place for design. [3]

### Functionality and correctness
- Does it do what the author intended, and is that good for users? Check edge cases, concurrency, and anything visible from reading. [1]
- UI changes: see them running, not only read the code. [1]
- For a bug fix, reproduce the bug first, apply the PR locally, rerun the repro, and probe corner cases. [12]
- Ask for a test plan that says how the change was verified. [15]
- Error handling: no discarded errors, errors-first control flow, no sentinel return values (-1, ""). [10]
- Check goroutine/thread lifetimes (leaks, races), context passing, and copies of types that hold slices or pointers. [10]
- Randomness for security uses a crypto source, and security or privacy review goes to a qualified reviewer. [1][10]

### Complexity and scope
- Flag any line, function or class that is harder than it needs to be, and any over-engineering or speculative feature. [1]
- One logical change per PR or commit, and keep it as small as possible without losing meaning. [11][12][15]
- Reformatting or cosmetic cleanup goes in a separate change from functional work. [1][12][15]
- When code moves between files, do not edit it in the same patch. [11]
- Every patch in a series should build and run, so that bisect works. [11]
- Reject lint-only or large automated edits unless the author explains how they were generated and maintainers agreed. [13]
- Size: about 200 lines is a guideline, with a ceiling around 400. [7][9][17]. The Microsoft data show usefulness falling from about 20 files. [5][6]

### Tests
- Are tests present, and would they fail if the code broke? Are assertions simple and useful? [1]
- A PR that touches code without touching tests needs a reason. [13][12]
- Run the full suite, and name the platform you tested on. [12]
- Test failure messages should show input, actual and expected values. [10]
- Look into CI failures, and check whether they already fail on the base branch before blaming the PR. [12]

### Readability, naming, comments, docs
- Names are descriptive without being unwieldy. [1]
- Comments explain why, not what. Remove stale TODOs and comments. [1]
- Commit and PR descriptions explain the reason for the change and its impact. Optimisation claims come with numbers. [11][15]
- Update docs, READMEs and release notes when build, usage or behaviour changes. [1][12]
- User-visible changes get an entry with a plain description, not implementation details. [12]

### Compatibility and API
- Do not break existing behaviour. New optional parameters with defaults are the safe form. [12]
- Public API and userspace-visible changes go to the matching maintainers and lists. [11]

### Process hygiene
- Read every human-written line, and ask for clarification where it is unclear. [1]
- Mark optional preferences as "Nit:". [1][2]
- Do not squash or force-push during review. Use new commits so reviewers can see the delta. [12][13][14]
- Say what you tested, and say where your confidence ends. Approve only what you understand. [12][16]
- AI-assisted PRs: disclosure is required, and the author must be able to explain the change. [13]

### Social and tone
- Praise good work as well as flagging problems. [1][12]
- Ask rather than assert, and use "we" language. Move long threads to a call. [16]
- Do not drag out reviews or withhold approval as leverage ("power" breakdown). [3]
- Disagreements need an escalation path so changes do not stall. [2]

## Empirical findings

Labelled by strength. All figures are as reported in the sources, not independently reproduced.

### Google (observational, large; [3])
- The median change is 24 lines. Over 35% touch a single file. Over 10% touch a single line.
- Median latency is under 4 hours for the whole review. First feedback takes under 1 hour for small changes and about 5 hours for very large ones.
- Over 80% of changes need at most one round of resolving comments.
- Fewer than 25% of changes have more than one reviewer. The median is 1. Comments per change grow with change size and peak around 12.5 comments at about 1250 lines.
- Interview themes: education, maintaining norms, gatekeeping and accident prevention. The original motive for review was code understandability and maintainability, with defect finding welcome but not the focus.
- Google's own comparison shows it differs from the two-reviewer convergence reported by Rigby and Bird for other projects. This is a comparison against earlier papers, not a controlled test.

### Microsoft
- About 15% of comments flag a possible defect, and at least 50% concern maintainability [6]. This is a talk abstract with little method detail.
- Larger changes get proportionally fewer useful comments [5][6]. A reviewer's first pass in an unfamiliar area gets about a third of comments judged useful, rising to about two thirds by the third pass [6].
- Review is mainly about understanding the change, and tooling for that is weak [4].
- Median time to sign-off is about 24 hours [6].

### Review size and defect density
- The 200-400 LOC, under-500 LOC/hour and 60-90 minute guidance traces to the Cisco/SmartBear study [7][17]. The popular quote "70-90% of defects" is not clearly attributed to the study on the page. I did not read the original report.
- Google data shows more comments on larger changes, but comment count is not defect yield [3].
- Net: the direction (smaller is better) is well supported across [3][5][6][7]. The precise thresholds are weakly sourced. Treat 200/400 as heuristics.

### Maintainability share of comments
- Mäntylä and Lassenius (IEEE TSE 2009): I could not fetch the paper (the host certificate failed). Secondary sources give different shares of evolvability defects, from about 60% to 77%, so I do not quote one figure here. Needs verification against the paper.
- Beller, Bacchelli, Zaidman, Juergens (MSR 2014): reported through a search summary only, not read directly (the TU Delft mirror refused the connection). Roughly 75% maintainability to 25% functional across 1,400+ changes in two open-source projects, with 7-35% of comments discarded. Needs verification.
- Both are consistent with the Microsoft findings in [4][6] and Google's stated motive in [3].

### Review latency (Meta)
- Meta ties long wait (P75 Time In Review) to engineer dissatisfaction via a survey. That is a correlation, not causation. Nudgebot results come from an experiment with no stats reported [8].

### Weak spots in the evidence
- Little of this measures defects escaping after review. McIntosh et al. (MSR 2014, review coverage and participation vs post-release defects) was not fetched (HTTP 403), so it is not used here.
- Most data comes from three large companies and a few open-source projects, and may not generalise to small teams.

## Disagreements

- Reviewers per change: two reviewers was reported as optimal by Rigby and Bird (as cited in [3]). Google finds one is usually enough and its comment counts rise with reviewers [3]. Microsoft invites up to 4.
- Style: Google says the style guide wins and prefers tooling or nits [1][2]. Slack says leave formatting to tooling and focus on design [16]. Go's list nonetheless includes many mechanical style items [10].
- Perfection vs progress: Google says approve when the change improves code health, even if imperfect [2]. Kubernetes and CPython are stricter on tests and the full suite before merge [12][13].
- Bug finding: reviewers and managers expect defect finding, but data in [4][6] say most comments are about maintainability. This argues for tests and analysis to catch defects and review for understanding. That is an inference from the data, not a claim the sources make about each other.
- Where to discuss: Slack advises taking long threads offline [16]. The Linux kernel and Google want the decision recorded in the thread [2][11].
- Squashing: CPython, Rust and Kubernetes say keep review history and squash at merge or on request [12][13][14]. Some Kubernetes reviewers ask for a squash at /lgtm [13].
- Commit and PR size: Phabricator says "as small as possible, but no smaller" and rejects line-count rules [15]. Others give 200-400 LOC [7][9][17].
- Stacked diffs: Orosz argues they speed up teams; GitHub-style flows lack native support, and the tooling cost is high [9]. Rust and Kubernetes review plain PRs [13][14].

## Not found

- Stripe: no primary page on code review. A Pragmatic Engineer article (paywalled, summary only) says API changes go through a stricter review than normal. Not read.
- Netflix, Uber, Airbnb, Spotify, Etsy, Twitter/X: no primary code-review page found. Uber appears only inside [9]. An Etsy post mentions SOX-driven extra approvals, seen only as a search snippet.
- Square/Block: the blog tag URL guessed (developer.squareup.com/blog/tag/code-review/) returned 404. No article found.
- Dropbox: only [19], which has little review content.
- Basecamp/37signals: no official page. Search returned unofficial third-party "skills" built from the open-source Fizzy repo. These are secondary and were not used.
- Meta: only [8] was read. I did not retrieve a primary Meta post on Phabricator or Differential, or any Sapling page (https://sapling-scm.com/docs/overview/ returned 404). The stacked-diff material comes from [9] and [15].
- Palantir "Code Review Best Practices" (blog.palantir.com): HTTP 403, not read.
- McIntosh et al. (ACM DL): HTTP 403, not read.
- Mäntylä & Lassenius and Beller et al. full papers: not read (see Empirical findings).
- Cisco study original report and Rigby & Bird: not read.
- Rust: no reviewer checklist exists in the pages read. The reviewer guide on forge.rust-lang.org was not fetched.
- Tidyverse full guide (code-review.tidyverse.org) not read.

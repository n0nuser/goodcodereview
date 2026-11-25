# 0002. Split an oversize part by concern, then by topic

Status: accepted, 2026-11-24. Owner: Pablo González.

## Context

A level page that reaches `PAGE_MAX` characters of text splits into a hub plus one page per `context` (`ui`, `server`, `data`, `cli`, or `any`). The cards that apply to any input all sit in one context, so a part can still be too big. When `service-server` passed the limit, the build stopped with "add a context or split the level further", and the only ways out were a new context, which changes a closed schema, or a higher limit.

The research in `docs/research/scaling-pages.md` measured the alternatives:

- 153 of 355 cards (43%) carry two or three concerns, so a physical split by concern alone would repeat cards or need a rule for each card's primary concern.
- 77 of 168 topic tags are used on one card, so topic alone is too uneven to split on.
- afdocs fails a page past 100,000 characters, and `docs/research/agent-readiness.md` records the same line for the HTML page. The 150,000 limit set earlier in this change stayed above it.

## Decision

`split_levels` in `tools/site_pages.py` plans the split. A level over `PAGE_MAX` splits by context. A context part still over `PAGE_MAX` splits by the first concern tag of each card. A concern part still over splits by the first topic tag. A group with fewer than `MIN_PART` cards (4) joins an `other` part of its context. If a part is still over after that, the build fails and names it.

`PAGE_MAX` is 100,000 characters of text, which matches the afdocs line.

Each card lives on exactly one page. Its home is the first concern tag, because authors list the main concern first. The page names are `<level>-<context>-<concern>` and, one step further, `<level>-<context>-<concern>-<topic>`. The hub, `llms.txt`, the sitemap, the Markdown twins and every card link read the same plan, so they cannot disagree about where a card is.

`concerns.md` joins `service.md` and `function.md` in `MD_OVER` in `tools/agent_ready_check.py`. It holds every card grouped by concern in one fetch, and one file per concern under `concerns/` is its split form.

Duplicate tags were merged first so the concern and topic keys are stable: `configuration` became `config`, `rate-limiting` and `rate-limits` became `rate-limit`, `multitenancy` became `multi-tenant`, and `tests` became `testing`.

## Options ruled out

- **Raise `PAGE_MAX` again.** One line, but each batch of cards uses up the room and the limit ends up above what the scanners accept.
- **Add an `ops` context.** It moves about a dozen cards and keeps one split rule, but it changes the closed context set, its schema and its docs, and the next overflow needs another context.
- **Split by character count.** A rule can be cut across two pages, and afdocs and Mintlify both advise against it.
- **List a card on every concern page.** It repeats text and makes the page sizes depend on how many concerns a card lists.

## Consequences

- The service level is nine parts and the function level is five. With the limit at 150,000 the sitemap held 36 URLs, and it now holds 40. `llms.txt` grew from 7.3K to 7.7K of its 12K budget.
- A card has one home page, so a reader scoped to one concern can miss a card whose first concern is another. The `concerns/<concern>.md` views and `cards.json` list a card under every concern it names, and the index lists every card with a link to its part.
- The first concern tag now decides a card's page. Reordering the tags in a card moves it.
- Eval, 2026-11-25 (Sonnet, `tools/eval_layout.py`, service level, 70 card ids, 9 parts). At first the `parts` layout, where the agent starts at one part and must open the others, reported every id in 1 of 3 runs and 7 of 70 in the other two: the agent read the first part, said "only this checklist part was given", and stopped. The `llms` layout (llms.txt plus every file) reported all 70 in 2 of 2 runs. Each part's header now carries a numbered list of every part with its card count and says to open all of them. After that change the `parts` layout reported all 70 in 3 of 3 runs. The earlier 5-part check was also 3 of 3. Three runs is a small sample, so read it as fixed, not proven. Forced `audit_repo` passed substance and missed the format line (`Verdict:` first), a miss the README already records for that case.
- Revisit `MIN_PART` and the concern-first choice when a part named `other` grows past about a fifth of its context, or when a new concern tag appears on many cards.

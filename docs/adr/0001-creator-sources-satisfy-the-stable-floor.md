# 0001. A source by the creator satisfies the stable floor

Status: accepted, 2026-11-02. Owner: Pablo González.

## Context

A stable card needs three independent organisations behind its rule (`docs/PROMOTION.md`, rule 1). A person's blog or talk is a reference and never counts. The Python pack comes from the maintainer's own review guide (https://pablogonzalez.me/posts/python-code-review-guide/). Few other organisations publish the same rules, so under the three-organisation bar the pack stayed draft and could not take part in a verdict.

## Decision

A stable card passes the organisation floor when one of its sources is by the creator of this repository. `CREATORS` in `tools/orgs.py` lists the creator, and `tools/validate.py` skips the three-organisation check for a card that cites one. The creator stays a person in `PERSONS`, shown under "People cited". Every other card still needs three organisations.

## Options ruled out

- **Keep the three-organisation bar for every card.** Honest about independence, but the whole Python pack stays draft and never decides a verdict.
- **Count the creator as a fourth-party organisation.** It would hide that one author backs the card. The creator is a person, so the card shows that.
- **Per-card waivers.** More precise, but each waiver needs its own review and the list drifts. One named exception is easier to audit.

## Consequences

- 13 Python cards became stable on 2026-11-02. Nine of them cite no organisation, and four cite one.
- "Stable means three independent organisations" is no longer true for every card. The README, About page and `CONTRIBUTING.md` say so.
- The creator's guide backs rules that this repo then uses to judge itself. A reviewer who wants only independently backed rules can scope to cards that list three or more organisations in `cards.json` (`orgs`).
- To drop the exception, empty `CREATORS`. The affected cards then fail validation until they gain organisations or go back to draft.
- Revisit when a second maintainer joins, or when an independent organisation publishes the same practice.

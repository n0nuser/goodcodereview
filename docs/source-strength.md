# Source strength

The organisation count says who backs a card. Source strength says how well. A card can list three organisations and still rest on pages that only touch its Rule.

## Verdicts

Each source is judged against the card's Rule, one row per card and URL, in `docs/research/source-strength.tsv`:

| Verdict | Meaning |
|---|---|
| `supports` | The source shows the organisation practises or documents this Rule: a recommendation, a published standard, or a team describing what it does and why. |
| `partial` | Related, but covers only part of the Rule or is generic. |
| `weak` | Tangential, a plan or proposal, a definition page, a summary of someone else's guidance, a vendor restating another organisation's guidance, or a tool's default setting. |
| `off` | Does not support the Rule. |
| `unjudged` | No row. Nobody has compared the source with the Rule yet. |

An organisation is as strong as its best source for that card. A card's backing is `strong` when at least three organisations support the Rule, `unjudged` when none of its sources has a row, and `mixed` otherwise.

## Where it shows

- The "Backed by" list on each card page and in the Markdown and text outputs, after each organisation name: `Google (supports)`.
- `cards.json` and the level and concern files: `Card.backing`, and `Org.strength` on every organisation and person (schema version 5).

## How rows are added

A judge reads the Rule, the source's URL and its quoted sentence, which a script has already confirmed is on the page. It does not fetch the page. Rows from 2026-11-04 come from the source pass in `docs/research/source-pass-2026-11-04.md` and its round 2. Sources that predate that pass have no row, so most cards show `unjudged`. Judge them, and add rows, before you promote a card or when you review one.

Strength does not change the promotion bar in `docs/PROMOTION.md`. It makes the weak spots visible.

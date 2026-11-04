# cards.json

`cards.json` lists every stable card in one file. `cards-drafts.json` lists the draft cards in the same shape. The shape is `cards.schema.json`, and [api-versioning.md](api-versioning.md) says how it changes.

## One file per level

The build also writes one file for each level that has cards, from the same list of cards as the merged file:

| File | Cards |
|---|---|
| `cards/<level>.json` | the stable cards of that level, for example `cards/function.json` |
| `cards/drafts-<level>.json` | the draft cards of that level |

Each file has the same top-level keys as `cards.json` (`levels` and `concerns` stay whole), with `cards` limited to one level, in the same order. A pack card goes in the file of its own `level`. Every card is in exactly one level file, and the build fails if the level files and the merged file hold different ids. All of them validate against `cards.schema.json`.

## Bounded files

None of the files is paginated. They are static files that the build writes, so they cannot grow past what the cards hold, and no query can return an unbounded result. `cards.json` is about 614,000 bytes (about 600 KB) and the largest level file, `cards/function.json`, is about 190,000 bytes. The build used to fail past 600,000 bytes; the maintainer removed that limit on 2026-11-04. An agent that wants a smaller response fetches a level or concern file instead.

## One file per concern, and a slim index

| File | Holds |
|---|---|
| `cards/concern-<concern>.json` | the stable cards that list the concern, in `cards.json` shape; a card with two concerns is in both files |
| `concerns/<concern>.md` | the same cards as a Markdown list, the text of `/concerns.md?concern=<concern>` |
| `concerns/level-<level>.md` | the stable cards of one level as a Markdown list, the text of `/concerns.md?level=<level>` |
| `cards-index.json` | every stable card in slim form: `id`, `level`, `severity`, `concerns`, `topics`, `rule`, `url`, plus `schema_version`, `concerns`, and the level ids. About 54 KB. The shape is `cards-index.schema.json` |

The build fails if a concern file does not hold exactly the merged cards that list the concern, in the merged order, or if `cards-index.json` differs from `cards.json` in its ids or slim fields. A concern with no stable card has no file. The Markdown files are rendered twice, once by the build and once by the Worker, and `test/worker.test.mjs` asserts that each file equals the Worker's output.

## Get a smaller response

Fetch the file that matches your question. These are static files, so the request never reaches the Worker:

| You want | Fetch |
|---|---|
| one level, JSON | `/cards/function.json` |
| one concern, JSON | `/cards/concern-security.json` |
| one concern, Markdown | `/concerns/security.md` |
| one level, Markdown | `/concerns/level-function.md` |
| a lookup table of every card | `/cards-index.json` |
| every card, full | `/cards.json` |

The query forms `https://goodcodereview.com/cards.json?level=function` and `https://goodcodereview.com/concerns.md?concern=security` return the same files, but they do reach the Worker, because a Worker route cannot see the query string. With one `concern` or one `level` and no other filter, the Worker serves the static file as is, without parsing it. A concern or level with no file falls back to filtering, and returns an empty list.

For any other filter, ask the Worker for a filtered list. It answers Markdown from `cards-index.json` and JSON from `cards.json`, and keeps each answer in the Cache API for the `max-age=300` that the response sets. These filters work on `cards.json` and on `concerns.md`:

- `concern`, `topic`, and `level` take comma-separated values, or repeat the parameter. A card matches when it has any value given for each filter. A filter whose values are all unknown returns no cards.
- `group=concern|level|topic` groups the Markdown list.

```
https://goodcodereview.com/cards.json?concern=security,performance&level=service
https://goodcodereview.com/concerns.md?topic=forms&group=concern
```

The filtered JSON response keeps every top-level key of the file and replaces `cards` with the matching cards. With no filter, the Worker passes the request to the static file. Draft cards have no filter: use `cards-drafts.json` or `cards/drafts-<level>.json`. `src/worker.js` has the rules, and `docs/deploy.md` says when the Worker runs.

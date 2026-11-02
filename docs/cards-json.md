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

None of the files is paginated. They are static files that the build writes, so they cannot grow past what the cards hold, and no query can return an unbounded result. Today `cards.json` is about 437,000 bytes (about 436 KB) and the largest level file, `cards/function.json`, is about 145,000 bytes. The build fails if any emitted file passes `CARDS_JSON_BUDGET`, 600,000 bytes (`tools/config.py`). If it does, split further before you raise the number; see [AGENTS.md](../AGENTS.md) on budgets.

## Get a smaller response

For one level, fetch its file: `https://goodcodereview.com/cards/function.json`. The address `https://goodcodereview.com/cards.json?level=function` returns the same file: when `level` is the only filter and has one value, the Worker serves `cards/<level>.json` as it is, without parsing or filtering. A level with no cards has no file, and the Worker then filters `cards.json` and returns an empty list.

For any other filter, ask the Worker for a filtered list. These filters work on `cards.json` and on `concerns.md`:

- `concern`, `topic`, and `level` take comma-separated values, or repeat the parameter. A card matches when it has any value given for each filter. A filter whose values are all unknown returns no cards.
- `group=concern|level|topic` groups the Markdown list.

```
https://goodcodereview.com/cards.json?level=function
https://goodcodereview.com/cards.json?concern=security,performance&level=service
```

The filtered response keeps every top-level key of the file and replaces `cards` with the matching cards. With no filter, the Worker passes the request to the static file. Draft cards have no filter: use `cards-drafts.json` or `cards/drafts-<level>.json`. `src/worker.js` has the rules, and `docs/deploy.md` says when the Worker runs.

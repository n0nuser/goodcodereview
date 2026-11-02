# cards.json

`cards.json` lists every stable card in one file. `cards-drafts.json` lists the draft cards in the same shape. The shape is `cards.schema.json`, and [api-versioning.md](api-versioning.md) says how it changes.

## One bounded file

The file is not paginated. It is a static file that the build writes, so it cannot grow past what the cards hold, and it has no query that could return an unbounded result. Today `cards.json` is about 437,000 bytes (about 436 KB). The build fails if either cards file passes `CARDS_JSON_BUDGET`, 600,000 bytes (`tools/config.py`). If it does, add a way to fetch part of the corpus before you raise the number; see [AGENTS.md](../AGENTS.md) on budgets.

## Get a smaller response

Ask the Worker for a filtered list. These filters work on `cards.json` and on `concerns.md`:

- `concern`, `topic`, and `level` take comma-separated values, or repeat the parameter. A card matches when it has any value given for each filter. A filter whose values are all unknown returns no cards.
- `group=concern|level|topic` groups the Markdown list.

```
https://goodcodereview.com/cards.json?level=function
https://goodcodereview.com/cards.json?concern=security,performance&level=service
```

The filtered response keeps every top-level key of the file and replaces `cards` with the matching cards. With no filter, the Worker passes the request to the static file. `src/worker.js` has the rules, and `docs/deploy.md` says when the Worker runs.

# goodcodereview-lint

Run the lint rules that [Good Code Review](https://goodcodereview.com) cards name as gates, and report each finding as a card: its id, its severity and how well the card is backed.

```sh
pipx install goodcodereview-lint      # or: uvx --from goodcodereview-lint gcr-lint check .
gcr-lint check src/                   # run the rules, one finding per card
gcr-lint coverage                     # which cards these rules cover, and how many they leave out
gcr-lint config                       # a ruff config that selects the same rules
```

## What it is, and what it is not

It adds no detection of its own. It selects ruff rules that cards already name in `tool_gate`, runs ruff, and maps each code back to the card. The point is the map: a finding says which review rule it enforces, how severe the card is, and how strong its sources are.

It covers a small part of the card set. Every run ends with the count:

```
ruff rules here cover 10 of 202 stable cards (4 in full, 6 in part). The other 192 need a reviewer or another tool. A clean run is not a review.
```

A clean run does not mean the code passed review. Most cards are judgement that no linter can own; for those, use the [Good Code Review skill](https://goodcodereview.com).

## Cards and rules

`src/goodcodereview_lint/data/gates.tsv` maps `tool`, `code`, `card` and `scope`. `scope` is `full` when the rule is the card's whole check and `partial` when it catches part of it. `data/cards.json` is a snapshot of the cards this release was built from; rebuild it with `python3 lint/scripts/snapshot.py` after `python3 tools/build.py`. A repository test fails when the snapshot or the map drifts from the cards.

## Exit code

`--fail-on` sets the lowest severity that makes the exit code 1 (`should-fix` by default; `never` always exits 0).

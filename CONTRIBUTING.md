# Contributing

One card per pull request. Copy `cards/_template.md` into `cards/change/` or `cards/audit/<level>/`.

A card is accepted when it has:
- a rule a reviewer can mark `FAIL` in code or config (a topic with nothing to fail goes in `glossary/`)
- a `FAIL` and a `PASS` example
- a `why` and the best counterpoint, answered
- a source in `borrowed_from`, or a note of first-hand experience
- exactly one `level`
- your own words: distil sources, never paste their text

New cards start as `status: draft`. Only `stable` cards ship in `SKILL.md`.

# cards.json versioning

`cards.json`, `cards-drafts.json`, and the per-level files in `cards/` ([cards-json.md](cards-json.md)) are the only machine-readable API of this site. Each file carries `schema_version`, an integer, and `cards.schema.json` is the JSON Schema for the current version. The number lives in `SCHEMA_VERSION` in `tools/schema.py`.

## One scheme: an integer in the file

There is one URL for each file, and it serves the current version only. The site does not serve older versions side by side. A consumer reads `schema_version` and refuses a number it does not know.

## What bumps `SCHEMA_VERSION`

Any change to the shape in `tools/schema.py`, because the published schema sets `additionalProperties: false` and a strict consumer fails on a key it has not seen:

| Change | Kind |
|---|---|
| Add a key | additive, still bumps the number |
| Add a value to an enum such as `severity` | additive, still bumps the number |
| Remove or rename a key | breaking |
| Change a key's type, or make a nullable key required | breaking |
| Remove a value from an enum | breaking |
| Change what a key means, for example the order or the set that a list holds | breaking |

Each bump has a line in [CHANGELOG.md](../CHANGELOG.md) that names the change and says whether it is breaking. The comment on `SCHEMA_VERSION` keeps the same history in short form.

## What does not bump it

- Adding or removing a file that has the same shape, such as `cards/<level>.json` when a level gains its first card or loses its last. Every file validates against the same `cards.schema.json`, so no consumer of the shape breaks. A consumer should list the level files it needs from `llms.txt` or `cards.json` (`levels`), not assume all eight exist.

- Card text, severities, and tags change, and cards are added.
- A card id is a stable key for consumers. Removing or renaming one is a breaking change for anyone who stores ids, so it gets a CHANGELOG line, but it does not change the shape.

## Notice

The site serves one version, so the notice is a CHANGELOG entry in the release that bumps the number. A consumer that needs a longer notice should pin a commit of this repository and read `site/cards.json` from its own build.

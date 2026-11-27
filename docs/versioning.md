# Versioning

Good Code Review follows [Semantic Versioning 2.0.0](https://semver.org/). One number, `VERSION` in `tools/config.py`, covers the cards, the site, and the skill. The `lint/` package versions itself.

## What the version promises

- Stable card ids.
- The shape of `cards.json` and the other JSON files ([api-versioning.md](api-versioning.md)).
- Published page URLs, their `.md` twins, and `llms.txt`.
- The verdict format and the skill name `good-code-review`.

Draft cards carry no promise.

## Which number to raise

| Change | After 1.0.0 | While the version starts with 0 |
|---|---|---|
| Remove, rename, or demote a stable card; remove a published URL; change `SCHEMA_VERSION`; change the verdict format | MAJOR | MINOR |
| Add or promote a stable card; change a severity; add a page or a file | MINOR | MINOR |
| Reword a card, add a source, fix a bug that changes no verdict format, id, or shape | PATCH | PATCH |

`tools/release.py` refuses a number that is too small for the change in card ids, severities, and `SCHEMA_VERSION`. The other rows are the reviewer's job.

## Pin a release

Each release is frozen at `https://goodcodereview.com/v/<version>/`: `cards.json`, `cards.schema.json`, and `badge.svg`. The files never change; `test/test_release.py` fails if one does. The other URLs serve the current version.

## Cut a release

1. Raise `VERSION`. Set the same number in `pyproject.toml` and `CITATION.cff`.
2. In `CHANGELOG.md`, move the `Unreleased` entries under `## [<version>] - <date>`.
3. Run `python3 tools/build.py && python3 tools/release.py && python3 tools/build.py`.
4. Merge the pull request. Then tag the merge commit `v<version>` and push the tag. The `release` workflow checks the tag against `VERSION` and publishes the release with the frozen files.

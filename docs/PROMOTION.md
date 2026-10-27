# How a draft card becomes stable

Only stable cards ship in `SKILL.md` and `llms.txt`, and only stable cards give a verdict. A card starts as `status: draft`. It moves to `status: stable` when it meets every rule below. Each draft records in its `lacks:` line the rule it fails today.

## The bar

A draft becomes stable when all of these hold:

1. **Three independent organisations back the Rule line.** Count organisations, not pages. One organisation counts once, whatever the number of its pages. Every clause of the Rule needs its own three. A source that backs only the Why, or only one clause, does not count for the rest of the Rule.
2. **A clause with fewer than three organisations moves to the Why or out of the card.** The card is then judged on what remains, and every Rule edit is listed in the pull request.
3. **Each source states a practice.** A recommendation, a published standard, or a team's description of what it does and why counts. A plan or proposal, a definition page, a secondary summary of another source, and a vendor page that restates another organisation's guidance do not.
4. **A reviewer can mark the Rule `FAIL` at the card's level.** For a change card, the diff or its description must show the failure.
5. **The `FAIL` and `PASS` examples are correct.** The code or config parses and uses real APIs. The `FAIL` breaks the Rule and the `PASS` meets it.
6. **The counterpoint is a real objection, and the card answers it.**
7. **Reader text carries no sourcing chatter.** The Rule, examples, and counterpoint do not say "Google suggests" or "following AWS". Sources go in `borrowed_from` and `note`.
8. **The card does not repeat or contradict a stable card.** Merge the two or delete the weaker one.
9. **The card names only stable cards and glossary entries.** `tools/validate.py` fails if a stable card names a draft id.
10. **`tool_gate` names a rule that exists.** Open the linter's rule page to confirm it.

## Count organisations

These groups count as one organisation each:

- OWASP: ASVS, the Cheat Sheets, the Top 10, and the GenAI project.
- W3C: every page on w3.org.
- Google: web.dev, Chrome, the SRE books, and the Go blog.
- Microsoft: Learn and the engineering playbook.

GitLab and GitHub are separate organisations. NIST, CISA, and NCSC are separate organisations.

A person is not an organisation. A blog, a talk, or a book by one author is a reference: the card lists the author under "People cited" and never counts it toward the three. `PERSONS` in `tools/orgs.py` lists the people. A person who speaks for a company counts only through the company's own page.

`tools/orgs.py` maps every source URL to the organisation that publishes it, and follows these groups. On a code host such as GitHub, the organisation is the repository owner, not the host. `tools/validate.py` fails on a URL that the map does not cover. It warns about a stable card with fewer than three organisations in `borrowed_from`, and people do not count; set `ORG_FLOOR_STRICT = True` in that file to make the warning an error. That check is a floor: rule 1 counts per Rule clause, so a card can pass the check and still fail rule 1. The map also counts publishers, not independence. Prometheus has its own entry, though the worked example below counts its alerting page as no new organisation. A reviewer still judges whether two publishers draw on the same source.

## What `lacks:` says

Every draft has one line, `lacks: <reason>, <note>`. The reason is the first rule the card fails, in the order of this table. A draft that no stable pass has checked yet gets `unreviewed`.

| Reason | Meaning | Rule |
|---|---|---|
| `held` | The maintainer keeps the card as a draft. | none |
| `contradiction` | The card argues against itself. | 5, 6 |
| `duplicate` | The card repeats or conflicts with a stable card. | 8 |
| `failable` | No reviewer could mark the Rule `FAIL` at its level. | 4 |
| `evidence` | A source is a plan, a definition, or a summary. | 3 |
| `orgs` | A Rule clause has fewer than three organisations. | 1 |
| `unreviewed` | The sources are listed, but no stable pass has checked them against rules 1 to 10. | all |

The note says what is missing in one sentence of at most 160 characters. For example: `lacks: orgs, "per dependency" has Microsoft only; needs two more orgs that limit concurrency per downstream`. `tools/validate.py` checks the format and the reason. It rejects the line on a stable card, so remove it when you promote.

## A worked example

`prod-alerts-symptoms-golden-signals` was a draft with this Rule: "Page on user-visible symptoms, such as error rate and latency, not on causes."

The Google SRE book backed it. A research pass in `docs/research/alerting-pass.md` found three more pages:

- Prometheus's alerting practices say to alert on symptoms. The page comes from the same Google author, so it adds a source but no organisation.
- Grafana Labs says alerts should detect user-facing failures. It adds an organisation.
- Datadog says to build pages around symptoms rather than causes. It adds an organisation.

That gave Google, Grafana Labs, and Datadog: three independent organisations behind the whole Rule line. The examples parsed, the counterpoint answered the objection that cause alerts help diagnosis, and no stable card covered the same rule. The card moved to stable.

## Propose a promotion

Open a "Promote a draft" issue with the three organisations and a link to each source. Then send a pull request that sets `status: stable`, removes the `lacks:` line, adds the sources to `borrowed_from` and to a note under `docs/research/`, and runs `python3 tools/validate.py && python3 tools/build.py`. Commit the regenerated `skills/` directory.

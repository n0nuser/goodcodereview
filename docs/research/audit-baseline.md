# Audit baseline: what real repo-level runs showed

Evidence: one 26-repo run (28 Oct 2026, test-suite scope, from the author's pasted vendor feedback) and seven whole-repo `codebase` runs (31 Oct 2026). The seven reports and feedback files were in the session scratchpad and are not kept in the repo; the counts below come from them. Findings tagged as inferred are the reviewers' own inference.

## Runs

| Run | Findings | vetted | pack | draft | no-card | Dropped / not read |
|---|---|---|---|---|---|---|
| 26 repos, test suites (28 Oct) | 389 | 67 | ~61 | 142 | 118 | 139 dropped |
| decathlon-cli (Go) | 7 | 6 | 0 | 0 (6 notes) | 1 | not stated |
| LocalRAG (Python) | 17 | 10 | 3 | 3 | 1 | 8 dropped, 4 could not check |
| n0nuser.github.io (Hugo/JS) | 20 | 9 | 1 | 2 | 8 | 5 inferred |
| deadchannel (Python/React) | 32 | 14 | 3 | 11 | 4 | ~12 drafts never read (truncated fetch) |
| leroymerlin-cli (Go) | 9 | 6 | 0 | 1 | 2 | none stated |
| obramat-cli (Go) | 18 | 11 | 0 | 0 (4 notes) | 7 | several files not read |
| radiotui (Python TUI) | 8 | 5 | 1 | 1 | 1 | none stated |
| **Seven whole-repo runs** | **111** | **61 (55%)** | **8 (7%)** | **18 (16%)** | **24 (22%)** | |

The seven runs told workers to treat drafts and packs as notes, so their draft share is lower than the 26-repo run, where drafts counted as findings (37%). Both runs show 22% to 30% of findings with no card behind them.

## Problems, by how many runs hit them

Counts are out of 8 runs (the 26-repo run plus seven), unless stated.

1. **Fetch tools summarise the rules (8/8).** WebFetch returned paraphrases of `llms.txt`, `llms-drafts.txt` and the pack page. One run read a truncated page and skipped ~12 drafts; one run got an empty pack body. Every worker fell back to `curl`. Rules arrive lossy unless the agent notices.
2. **No applicability filter (8/8).** 70 to 165 of ~200 cards were N/A per repo. Workers read every `applies_when` or title to decide. `cards.json` has `applies_when`; `llms.txt` does not show it.
3. **Codebase scope is undefined (7/8).** The `codebase` level has 11 cards, all CI, dependency and process. Real defects sat under function, module and service cards. Nothing says whether to run lower levels, how much code to read, or what to sample.
4. **No report shape (8/8).** Every run invented counts by severity and source, a ledger with N/A collapsed, proposed changes with size, product bugs, dropped candidates and "could not check". The verdict example fits one level only, and has no slot for the "decision to write down" line.
5. **Overlapping cards, no owner (5/8).** One defect filed under two or three cards, such as `code-dead-code`, `code-consistency-drift` and `chg-reuse-before-write`. Workers applied "file under the best card" by instinct.
6. **Draft handling (5/8).** Draft `block` severity leaks into counts or flattens real exposure. The draft list carries backer gaps but not the Rule text. Python-only drafts are unmarked. Pack pages link to a placeholder host.
7. **No proof recipe (5/8).** Cards say "cite file:line" but not what counts as proof. Several `block` cards could only be `inferred`. Platform evidence such as `gh api` was unclear.
8. **Severity ignores context (3/8).** A single weak `block`, often process-only (`code-secret-scan` with no scanner), flips the whole verdict to request changes.
9. **Absent control is ambiguous (4/8).** "No scanner / no branch protection / no CI": is that a FAIL of the card, N/A, or no-card?
10. **Card wording (6/8).** `code-dependency-pinning` has pip-only examples (4 runs). `code-dependency-licence-sbom` bundles inventory, scan and licence (3 runs). `code-rule-has-enforcer` and `code-dead-code` mix two checks each. `svc-cors-allowlist` lacks a condition.

## Missing cards that more than one run asked for

- Fail-open default: auth or allow-list that is off unless configured, and a default secret that lets the app boot (LocalRAG, deadchannel, radiotui).
- Self-update or installer trusts a checksum from the same origin as the archive (decathlon-cli, obramat-cli).
- Credentials shown in tool output (decathlon-cli).
- Input-domain validation and silent truncation: negative quotas, bounded reads that cut instead of failing (deadchannel, obramat-cli).
- Stale or false comments and docs references (deadchannel, n0nuser.github.io, obramat-cli, plus the 26-repo run).
- Aged vulnerability alerts left unmerged (leroymerlin-cli).
- CLI cards exist only as drafts under `service`, unreachable from a CLI repo (radiotui, obramat-cli).
- Language packs: no Go pack (3 runs); no TypeScript/Vitest pack (26-repo run).
- Front-end JavaScript correctness (n0nuser.github.io: unhandled rejections, unguarded `decodeURIComponent`).
- Test-suite entry point and test-code reduction (26-repo run only).

## What the data says about the earlier plan

- **Report template, granularity map, evidence field: confirmed as top priority.** Every run rebuilt them.
- **Exceptions record: low demand.** No run asked for it.
- **Org level: still no.** Missing cards are code-level (fail-open, updater provenance, validation), not governance.
- **`detect:` scanning: still no.** Dropped candidates (139 of 389) show the cost is verification, not finding.
- **New and bigger than expected:** applicability tagging, publishing raw cards (so reviews do not depend on a fetch tool), and the draft policy.
- **Sampling:** workers read 10 of 61 files, or skipped half the repo, with no stated rule. The granularity map must include one.

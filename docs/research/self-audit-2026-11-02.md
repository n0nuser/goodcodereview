# Self-audit: goodcodereview against its own cards, 2026-11-02

Verdict: request changes - codebase (entry), function, module, service, system, production; Python pack; drafts - all concerns - card set good-code-review 1.0 at 0c3b898 - 2 block, 16 should-fix, 1 discuss FAIL, 40 PASS, 82 N/A. Neither block FAIL is a missing process control.

Input: the whole repo at HEAD `0c3b898`, plus GitHub settings read with `gh api`. "Source" tags follow `references/audit.md`. I tagged the 14 stable Python-pack cards `pack (stable)` and counted them in the ledger, because they are stable (see Wrong W2).

## Ledger

FAILs first (block, then should-fix, then discuss), then PASS.

| Card | Verdict | Severity | Evidence | Tag | Note |
|---|---|---|---|---|---|
| code-dependency-pinning | FAIL | block | `.github/workflows/eval.yml:25` | proven, vetted | `npm install -g @anthropic-ai/claude-code` has no version and no lockfile, in a job that holds `ANTHROPIC_API_KEY` (`:27-28`). impact: low, because the job only runs on manual dispatch. Also breaks code-workflow-supply-chain (Why). |
| prod-canary-staged-rollout | FAIL | block | `docs/deploy.md:11-15`, `wrangler.jsonc:1-11` | inferred, vetted | Every push to `main` deploys to 100% of traffic through Workers Builds, with no staged rollout and no abort rule. I could not see the Cloudflare dashboard. impact: low, because it is a static docs site. Scope choice explained in Method. |
| code-ci-gates | FAIL | should-fix | `gh api repos/n0nuser/goodcodereview/branches/main/protection` returns `404 Branch not protected`, and `.../rulesets` returns `[]` | proven, vetted | No check is required before merge. The `skills/` gate (`check.yml:13-15`) is advisory, and direct pushes to `main` skip it (`134617c`, `6112ec4`, and `53d59bd` have no PR number). |
| code-rule-has-enforcer | FAIL | should-fix | `CONTRIBUTING.md:25`, `AGENTS.md:19`, `AGENTS.md:46`, `CONTRIBUTING.md:3` | proven, vetted | AGENTS.md names `agent_ready_check.py` as the check for a mandatory spec, but CONTRIBUTING says "CI does not run it". "Send one card per pull request" has no check: commit `134617c` promoted 13 cards in one direct push. |
| code-docs-refs-resolve | FAIL | should-fix | absent in `.github/workflows/*.yml` (no link-check step) | proven, vetted | A missing control. A one-off scan of the relative links in `*.md`, `docs/`, and `.github/` found 0 broken relative paths (4 hits were `(url)` placeholders); anchors were not checked. |
| code-dead-code | FAIL | should-fix | `tools/build.py:23`, `:121`, `:495-500`; `tools/validate.py:21-22`, `:129`; `src/worker.js:7` | proven, vetted | `AUDIT = LEVELS[1:]` is rebound at `:121` to a list of prose lines, so the Audits nav menu in `page()` never renders: 0 matches for `summary>Audits<` in the built `site/*.html`. `ORG_FLOOR_STRICT` is a flag that is always `True`, so its other branch is dead. `GROUPS = KEYS` is an alias. Also breaks mod-one-name-per-concept (draft). |
| code-dependency-licence-sbom | FAIL | should-fix | absent in `.github/workflows/check.yml` | proven, vetted | The SBOM part fails: there is no SBOM anywhere. The site ships third-party content, the Simple Icons paths in `tools/org_icons.json`. impact: low, because the repo has no package manifests. |
| svc-api-versioning-policy | FAIL | should-fix | `tools/schema.py:12`; `CHANGELOG.md:23` | proven, vetted | `cards.json` is advertised to outside callers (`README.md:37-45`). v3 changed what `orgs` means at the same URL, and no versioning scheme is written down. |
| svc-cli-exit-codes-and-streams | FAIL | should-fix | `tools/eval.py:308-328`, `:324-326`; `tools/validate.py:164` | proven, vetted | `eval.py run` exits 0 even when substance checks fail, and it prints harness errors to stdout, so `eval.yml` can never go red. `validate.py` prints its errors to stdout. Also breaks fn-propagate-dont-swallow (draft). |
| svc-csp-strict-script-src | FAIL | should-fix | `tools/build.py:717-718` | proven, vetted | The CSP is `frame-ancestors 'none'` only. The comment says a `script-src` policy would block the inline script, but that script is a build-time constant (`:374-415`), so a `sha256-` hash would work. |
| svc-invalid-input-is-4xx | FAIL | should-fix | `src/worker.js:17-18`, `:64` | proven, vetted | Unknown `concern`, `topic`, and `level` values get a 200. The Markdown response names them, but the JSON response drops them without a trace. This is deliberate (`worker.js:11`), so it is a candidate for `accepted by <owner> until <date>`. |
| svc-list-endpoint-paginates | FAIL | should-fix | `site/cards.json` (436,562 bytes, all 141 stable cards); `src/worker.js:55-57` | proven, vetted | No page size and no documented limit. The Worker parses the whole file on every filtered request. impact: low today. Also breaks svc-stream-dont-materialise (draft). |
| svc-cli-destructive-dry-run | FAIL | should-fix | `tools/build.py:749`, `:826-827` | proven, vetted | `build.py` runs `rmtree(site/)` and unlinks `references/*.md` with no preview flag. impact: low, because the output is generated and `skills/` is tracked in git. See Noisy N3. |
| mod-no-module-mutable-state | FAIL | should-fix | `tools/validate.py:23`, `:70`, `:128`; `tools/eval.py:142-153` | proven, vetted | `below` is a module list that `validate()` clears and fills. `_tags` is an unbounded module cache. |
| mod-yagni | FAIL | should-fix | `tools/eval.py:115-117`, `:232-237`; `tools/validate.py:21-22` | proven, vetted | The opencode adapter "has not been run against a real opencode install". The `ORG_FLOOR_STRICT` option never changes. The card's applies_when says "The change adds", and I applied it to existing options (see Method A5). |
| py-imports | FAIL | should-fix | `test/test_skill.py:65-67`; `tools/eval.py:148-149` | proven, pack (stable) | `sys.path.insert` followed by an import inside a test method and inside a function. |
| py-modern-typing | FAIL | should-fix | `tools/schema.py:8`, `:23`, `:53-55`; absent in `check.yml` (no type gate) | proven, pack (stable) | Uses `Optional` and `Union`. The fix must also teach `_schema_of` (`:121`) about `types.UnionType`, because `str \| None` is not `typing.Union`. |
| fn-regex-compiled-once | FAIL | should-fix | `tools/validate.py:150-152`, `:155-156` | proven, vetted | Builds one regex per (stable card × draft id) pair inside nested loops. That is about 141 × 136 patterns, past `re`'s 512-entry cache. impact: low: `validate.py` runs in 1.0 s. |
| code-adr | FAIL | discuss | `tools/validate.py:127`; `docs/PROMOTION.md` ("One exception"); commit `134617c` | proven, vetted | The `CREATORS` exception made 13 cards stable on the maintainer's own guide. It is recorded only as one line and a commit message, with no context, no options weighed, and no consequences. |
| code-build-hermetic | PASS | | `check.yml:8-10`; `build.py:694-700` | vetted | Python 3.12 is pinned, the build uses only the standard library, and the date comes from the HEAD commit. |
| code-secret-scan | PASS | | `gh api repos/...` → `secret_scanning: enabled`, `secret_scanning_push_protection: enabled` | vetted | A regex scan of `git log --all -p` for AKIA, `sk-ant-`, `ghp_`, and PEM keys found 0 hits. |
| code-workflow-supply-chain | PASS | | `check.yml:7-8`, `eval.yml:20-21`, `sync-skills.yml:13-14` | vetted | Every `uses:` is pinned to a 40-character SHA. The Why-only items fail; see Wrong W9. |
| code-perf-budget-in-ci | PASS | | `build.py:879-880`, `:890-894`, `:942-943`; `check.yml:12` | vetted | The context budgets fail the CI build. |
| code-consistency-drift | PASS | | `tools/` | vetted | One renderer, one front-matter parser, and one URL-to-org map. |
| mod-derive-dont-duplicate | PASS | | `schema.py:13-17` restates `validate.py:11,14-15`; `build.py:997-998` | vetted | `schema.check` fails the build when a card's level, severity, or status leaves the schema enums, which is the parity check the card accepts. |
| mod-single-writer-per-state | PASS | | `AGENTS.md:45`; `sync-skills.yml:17-25` | vetted | Only `build.py` writes `skills/`, whether a contributor or the bot runs it. See the race in Product bugs B6. |
| mod-colour-tokens-meet-contrast | PASS | | `build.py:263-267` | inferred, vetted | Converted from OKLCH to sRGB: text tokens are at least 6.67:1 in light mode and 8.76:1 in dark mode, and `--edge` is 4.10:1 and 4.39:1 (non-text, needs 3:1). |
| fn-comments-explain-why | PASS | | `build.py:717`, `:831`, `:946`; `worker.js:20` | vetted | |
| fn-handle-rejected-promises | PASS | | `build.py:413` (clipboard `.then(ok, fail)`) | vetted | |
| fn-heading-structure | PASS | | `build.py:506` h1, `:634` h2, `:580` h3, `:461` md headings shifted down one level | vetted | |
| fn-img-alt-text | PASS | | `build.py:534`, `:543` | vetted | Icons are `aria-hidden`, with the org name as adjacent text. |
| fn-native-button-or-link | PASS | | `build.py:594`, `:496` | vetted | |
| fn-no-positive-tabindex | PASS | | `build.py:506` (`tabindex=-1` on `main` only) | vetted | |
| fn-focus-indicator-visible | PASS | | `build.py:299`, `:309` | vetted | The outline is removed only on `main`, the skip-link target. |
| fn-form-control-has-label | PASS | | `build.py:614` | vetted | |
| fn-colour-not-sole-cue | PASS | | `build.py:578`, `:451` | vetted | Severity and FAIL/PASS are shown as text. |
| fn-target-size | PASS | | `build.py:301`, `:327-328`, `:333` | vetted | |
| fn-reduced-motion-respected | PASS | | `build.py:371-373` | vetted | |
| fn-status-announced-live-region | PASS | | `build.py:634`, `:507` | vetted | |
| fn-disclosure-hides-only-secondary | PASS | | `build.py:47`, `:624`, `:628` | vetted | |
| fn-aria-role-has-state-and-keys | PASS | | `build.py:593-594` | vetted | Native buttons with `aria-pressed`. |
| fn-related-controls-in-fieldset | PASS | | `build.py:593` (`role="group"` with `aria-label`) | vetted | |
| fn-no-raw-html-sink | PASS | | `build.py:430-438` escapes before marking up; `:503` escapes JSON-LD | vetted | `copy_pre` (`:597-598`) takes raw HTML, but only from constants today. |
| fn-no-shell-with-input | PASS | | `eval.py:214`, `:240`; `build.py:697` | vetted | Argument lists, never a shell. |
| fn-no-native-deserialise-untrusted | PASS | | `json.loads` only | vetted | |
| fn-no-prototype-pollution | PASS | | `worker.js:15`, `:30` (fixed keys, `Object.hasOwn`) | vetted | |
| fn-no-blocking-call-in-async-code | PASS | | `worker.js:48-79` | vetted | |
| fn-test-behaviour-not-implementation | PASS | | `test/test_eval.py:27-40`; `test/worker.test.mjs` | vetted | |
| fn-rerun-safe-after-crash | PASS | | `build.py:749` | vetted | The build regenerates from scratch. |
| fn-join-dont-concat-in-loop | PASS | | `build.py:467`, `:724` | vetted | |
| py-paths-from-file | PASS | | `eval.py:134`, `test/test_skill.py:6` | pack (stable) | |
| py-docstrings-google | PASS | | `build.py:470-471`, `:519` | pack (stable) | The docstrings carry information the signature does not. |
| svc-timeouts | PASS | | `eval.py:218`, `:255` (`timeout=600`) | vetted | `build.py:697` runs `git log` with no timeout. That is a process boundary under applies_when but not a "remote call" under the Rule (W9). |
| svc-cli-non-interactive | PASS | | `tools/*.py` | vetted | No prompts. |
| svc-reflow-and-zoom | PASS | | `build.py:261-292` | inferred, vetted | Fluid type, `min-width:0`, and `overflow-wrap`. There are 390 px screenshots in the untracked `.playwright-mcp/`. |
| sys-agent-tool-least-privilege | PASS | | `eval.py:214`, `:240` (`--allowedTools Read,Grep,Glob,Skill`) | vetted | |
| sys-prompt-injection | PASS | | `eval.py:156-184` | vetted | Model output is only matched with regexes, and the tools are read-only. |
| sys-secrets-and-errors | PASS | | `eval.yml:27-28`; `eval.py:224` | vetted | |
| sys-cache-bounds-invalidation | PASS | | `worker.js:58` (`max-age=300`) | vetted | |

N/A: 82 cards. applies_when does not hold, or the scope skips them:
- change: 13, skipped because there is no diff. This includes the stable `py-ruff-gate`; see W7.
- incident: 2, because there is no postmortem.
- production: 5. No alerts, SLOs, profiling, kill switch, or launch.
- `<data>`: every card, because the repo has no database.
- Auth, session, upload, crypto, JWT, password, CORS, CSRF, SSRF, retry, queue, and lock cards: the repo has none of these.
- `code-vuln-remediation-window`: `gh api .../dependabot/alerts` returned `[]`.
- `py-pytest-parametrize`: the tests use `unittest`.
- `py-no-init-or-model-tests`: its applies_when needs a diff.

Counts by source: vetted 17 FAIL and 38 PASS. pack (stable) 2 FAIL and 2 PASS. draft and pack-draft: 19 FAIL, listed below. no-card: 7 product bugs.

Could not check, apart from the ledger:
- prod-canary-staged-rollout: the Cloudflare dashboard (versions, gradual deployments).
- svc-tls-modern-only: the Cloudflare TLS settings.
- Whether `_headers` applies to Worker responses built from `env.ASSETS.fetch` (`worker.js:69-70`).

Dropped candidates: 4. These were a broken-links hit on `(url)` placeholders, a duplicated-budget finding withdrawn because the test is a deliberate tripwire, a `fn-join-dont-concat-in-loop` lead, and an svc-security-headers lead on the Worker 404, which copies the asset headers.

Decision I would most want written down: the `CREATORS` exception (`tools/validate.py:127`, `tools/orgs.py` `CREATORS`). The alternative costs 13 Python cards going back to draft, and the Python pack losing its say in the verdict.

## Draft findings

Not vetted. None of these changes the verdict.

| Card | Source | Evidence | Tag | Note |
|---|---|---|---|---|
| mod-one-name-per-concept | draft | `build.py:23` vs `:121`; `:744` `none` vs `:829` `empty`; the local `section` (`:858`), `row` (`:674`), and `md` (`:711`) shadow the functions at `:645`, `:584`, and `:441` | proven | Reusing the `AUDIT` name is what killed the nav menu (B1). |
| mod-cohesive-unit | draft | `tools/build.py` (1,025 lines): CSS `:261-373`, JS `:374-415`, About and Privacy prose `:159-202`, the md renderer `:421-467`, budgets, and file output | proven | Also breaks code-file-lines-ceiling (draft, around 1,000 lines). |
| mod-fowler-smells | draft | `build.py:727-1021` | proven | `main()` is 295 lines. Also breaks mod-thin-entry-point. |
| mod-no-import-side-effects | draft | `tools/orgs.py:122` reads JSON on import; `build.py:14` and `eval.py:148` mutate `sys.path` | proven | |
| mod-central-config | draft | `build.py:53` `REPO`, restated literally at `:163`, `:171`, `:795` | proven | |
| fn-bool-arg-at-callsite | draft | `build.py:627`, `:630`, `:637`, `:767`, `:821` | proven | `page(..., True, ...)` and `listing(..., f[:-5] in none, f == "concerns.html")`. |
| fn-no-anonymous-tuples | draft | `build.py:751`, `:757` (`pages[inc][2]`), `:860`, `:602` (`c[1]["status"]`) | proven | Also breaks py-frozen-dataclass-over-tuple (pack draft). |
| fn-known-keys-get-a-type | draft | `validate.py:10` (fixed keys), with `fm` passed as a dict through about 30 functions in `build.py` | proven | |
| fn-no-magic-values | draft | `build.py:627` (`cur[:-5]`), `:559` (`[0, 12, 10, 8, 6.5][len(m)]`) | proven | |
| fn-name-intermediate-conditions | draft | `build.py:389` | proven | A three-term `\|\|` decides `hidden`. |
| fn-propagate-dont-swallow | draft | `eval.py:324-326` | proven | Named on the svc-cli-exit-codes line. |
| fn-comments-survive-context | draft | `build.py:115` ("today every pack card is a draft", now false); `eval.py:117`; `test/test_schema.py:47` ("validate.py warns", but it errors) | proven | |
| fn-atomic-related-updates | draft | `build.py:878-880`, `:888-891`, `:826-827` | proven | Writes the file, then checks the budget. A failed build leaves `skills/` half regenerated. |
| py-strenum-not-strings | pack draft | `build.py:602`, `:823-824`; `validate.py:78`, `:127`, `:132` | proven | `"stable"` and `"draft"` are compared as strings. |
| py-pydantic-validation | pack draft | `validate.py:31-54`, `:68-158` | proven | Front matter is validated by hand. This is by design: the build is standard library only (`docs/deploy.md:17`). |
| svc-stream-dont-materialise | draft | `worker.js:55-57` | inferred | Parses a 436 KB JSON file per filtered request. Free-plan Workers get 10 ms of CPU, and it was not measured. |
| code-a11y-check-in-ci | draft | absent in `check.yml` | proven | The repo builds a web UI and has a test suite. |
| code-documented-setup-runs | draft | `CONTRIBUTING.md:23`; `test/test_schema.py:17`; `test/test_skill.py:81` | proven | On a fresh clone, `python3 -m unittest discover -s test` gives `FAILED (errors=12)` (`FileNotFoundError: site/cards.json`). No doc says to build first. |
| prod-slo-error-budget | draft | absent in the repo and `docs/` | inferred | `llms.txt` consumers rely on the site, and no availability target exists. impact: low. |

Go (7) and TypeScript (5) packs: N/A, because the repo has no Go or TS code. The JavaScript is `src/worker.js` and the inline JS in `build.py`. The other 117 drafts did not FAIL (PASS or N/A, not itemised), mostly `<data>`, proto, queue, auth, and diff-only.

## Product bugs (no-card)

- **B1.** The Audits nav menu never renders (`build.py:23`, `:121`, `:495-500`). Verified: 0 `summary>Audits<` matches in `site/*.html`, and the CSS for it (`:303-305`) is dead.
- **B2.** `references/audit.md`, `site/audit.md`, and `site/audit.html` each print the opening paragraph twice: `AUDIT_STEPS[0]` (`build.py:111`) equals `AUDIT_INTRO` (`:119`), and both are joined at `:120`, `:782`, and `:961`. Verified: `rg -c` counts 2 in each file.
- **B3.** The stable Python cards are shipped as drafts and as stable cards at once:
  - `references/pack-python.md` opens with "A draft card is not vetted" over all 23 Python cards, 14 of them stable (`build.py:951`).
  - `SKILL.md:65` lists `pack-python.md` under "Draft cards".
  - The same 14 cards are also in `references/function.md`, `module.md`, and `change.md` as stable (`build.py:828`).
  - The level HTML pages leave them out (`build.py:755`, core only).
  - In `cards.json`, the `levels[].stable_count` values sum to 127, while `cards` holds 141 (`build.py:743`).
- **B4.** `SECURITY.md:5` and `security.txt` (`build.py:1007`) send reporters to private vulnerability reporting, but `gh api repos/.../private-vulnerability-reporting` returns `{"enabled":false}`.
- **B5.** `eval.yml` cannot fail on findings, because `eval.py run` always exits 0 (`eval.py:308-328`).
- **B6.** `sync-skills.yml` has no `concurrency:`, so two quick pushes race and the second `git push` is rejected (inferred). Its bot commit does not trigger `check.yml` (`sync-skills.yml:3`), so the regenerated `skills/` on `main` is never tested.
- **B7.** The tests need `site/` from a prior build (`test_schema.py:11-17`, `test_skill.py:81`). The failure is 12 tracebacks with no hint.

## Proposed changes

- S: Drop `AUDIT_STEPS[0]`. Fixes B2.
- S: Rename the second `AUDIT` to `AUDIT_SECTION`. Fixes B1 and code-dead-code.
- S: Fix the stale text: W3, W4, W5, W6, and audit.md's "today".
- S: Turn on private vulnerability reporting, or change SECURITY.md (B4).
- S: Pin the claude-code version in `eval.yml` (code-dependency-pinning).
- S: Make `eval.py run` exit 1 on failures and send errors to stderr.
- S: Add a CSP `script-src 'sha256-…'; object-src 'none'; base-uri 'none'` from a hash of `JS`.
- S: Add `concurrency:` to `sync-skills.yml`.
- M: Protect `main` with required checks. Run `agent_ready_check.py`, a local link check, and ruff and a type check in CI.
- M: Decide the place of stable pack cards: draft label, levels, `stable_count`, and audit.md's source tags (B3, W2).
- M: Write a `cards.json` versioning note, and either paginate it or document it as one bounded file.
- L: Write the CREATORS decision record and fix every "three organisations" claim (W1), or drop the exception.
- L: Split `build.py`: assets, the renderer, and output stages.

## Meta

### Noisy

- **N1.** The UI function cards produced 16 PASS rows for a single inline CSS/JS blob in `build.py:261-415`. The format asks for each PASS on its own line, so the ledger is about 40% low-signal PASS rows.
- **N2.** `svc-timeouts` fires on every subprocess (applies_when: "network or process boundary"), while its Rule only asks about remote calls, so `build.py:697` (`git log`) triggers it and then passes.
- **N3.** On a static docs site whose output is generated:
  - `svc-cli-destructive-dry-run` (`build.py:749`), `svc-list-endpoint-paginates` (`cards.json`), and `prod-canary-staged-rollout` (block) all FAIL, each with `impact: low`.
  - None of the three cards has a carve-out for regenerated, git-tracked output or for static assets.
- **N4.** Draft triage was the most expensive step with the least yield:
  - It covered 115 core drafts and 21 pack drafts (Go and TS all N/A), in `drafts.md` (48,587 chars) and the pack files.
  - 117 did not FAIL.
  - Most of the 19 that failed are maintainability findings in one file (`build.py`).
- **N5.** Overlapping cards produce double entries:
  - `ORG_FLOOR_STRICT` is evidence for both code-dead-code and mod-yagni.
  - The Worker's 200 on bad input fits svc-invalid-input-is-4xx, svc-api-specific-status-codes (draft), and svc-api-problem-json (draft).
  - The overlap rule ("narrower applies_when owns it") cannot rank code-dead-code against mod-yagni, because their applies_when are not comparable.
- **N6.** When `ORG_FLOOR_STRICT` is `True`, `validate.py:165-166` prints a WARNING list that repeats every floor error already printed.
- **N7.** On a fresh clone, the 12 `FileNotFoundError` tracebacks (B7) bury the real cause: the build has not run.
- **N8.** Each audit line now carries four tags: severity, proven/inferred, source, and impact. A 19-FAIL ledger is hard to scan.

### Wrong

- **W1.** The claim that every stable card has three organisations is false for 13 stable cards.
  - Where it is made: `README.md:5`, `CONTRIBUTING.md:10`, `build.py:145-146` (BACKING), `:167`, `:171` (About), `CHANGELOG.md:23`, and `docs/PROMOTION.md` rule 1.
  - What `validate.py:127` actually does: it accepts any card that cites a `CREATORS` source.
  - These cards cite 0 organisations: py-field-only-when-adds, py-httpx-client-lifespan, py-imports, py-modern-typing, py-no-cast, py-no-init-or-model-tests, py-paths-from-file, py-ruff-gate, py-test-hygiene.
  - These cite 1: py-cancellation and py-task-reference (psf), py-class-earns-its-instance and py-docstrings-google (google).
  - The maintainer's own guide backs rules that this repo then uses to judge itself. The PROMOTION bar has no independence check for that.
- **W2.** audit.md:9 says "today every pack card is a draft". In fact 14 of 35 pack cards are `status: stable`. The audit source tags (`vetted` or `pack`) do not say which applies to a stable pack card.
- **W3.** `docs/PROMOTION.md` says validate.py "warns … set `ORG_FLOOR_STRICT = True` … to make the warning an error". It is already `True` (`validate.py:22`). The same stale claim is at `test/test_schema.py:47`.
- **W4.** About (`build.py:177`) says the Worker answers "only addresses that match no file". The Worker also serves the filtered `/concerns.md` and `/cards.json` (`wrangler.jsonc:9`, `docs/deploy.md:7`).
- **W5.** `SECURITY.md:13` says "The workflow", but there are three. `build.py:471` and `:710` describe Cloudflare Pages, but the deploy uses Workers static assets (`docs/deploy.md:3`).
- **W6.** audit.md says "the `metadata.version` above", but audit.md has no metadata. It lives in `SKILL.md`, which a reader of `site/audit.md` may never load.
- **W7.** `py-ruff-gate` is `level: change`, while its applies_when is a repo property ("The project is Python and has a linter configuration"). audit.md skips change cards, so an audit can never check it. This repo ships it as stable and has no ruff config.
- **W8.** applies_when is phrased for a diff on cards at other levels: `mod-yagni` ("The change adds") and `py-no-init-or-model-tests` ("The diff adds"). In an audit they are N/A as written.
- **W9.** Rules that are narrower or wider than their own cards:
  - `code-workflow-supply-chain`: the Rule only asks for SHA pins. Least-privilege tokens, untrusted input kept out of `run:`, and provenance are only in the Why, so they cannot FAIL. `eval.yml:26` interpolates `${{ inputs.* }}` into `run:` and still passes.
  - `code-dependency-licence-sbom`: the id says licence, but the Rule never asks for one. The licence check is "team policy" in the Why, and the concerns list only `security`.
  - `svc-timeouts`: applies_when covers process boundaries, but the Rule only covers remote calls.
  - `py-modern-typing`: applies_when adds "or the type gate is missing", which the Rule does not require.
  - `code-release-gated-on-ci` (draft): covers tag-push releases only, so the deploy-on-push-to-main here is out of scope.
- **W10.** Line budgets disagree. `SKILL_BUDGET = 400` lines (`build.py:22`), `test_skill.py:44` allows under 500, and the spec says under 500 lines. AGENTS.md's budget table lists characters only.
- **W11.** Budget and spec results:
  - Within budget: `llms.txt` 10,085/12,000. SKILL.md 76 lines, body 6,454/16,000. Largest index `function-index.md` 8,491/12,000. Largest reference `function.md` 59,506/70,000 (85%).
  - `agent_ready_check.py` in the throwaway clone: all checks pass, including item 16 (llms.txt shape) and items 22-23 (`.md` twins with frontmatter).
  - Not run: the official `skills-ref validate`, because it needs maintainer approval.

### Missing

- **M1.** Controls the repo lacks:
  - Branch protection or rulesets with required checks.
  - `agent_ready_check.py` in CI.
  - A docs link check.
  - Ruff and a type gate on `tools/`. The repo ships `py-ruff-gate` and `py-modern-typing` as stable but follows neither.
  - `.github/dependabot.yml` for action SHA bumps. Only security updates are on.
  - CODEOWNERS.
  - A test that a stable card is never labelled draft (B3).
  - A test that the nav renders (B1).
  - A deploy gated on CI passing. Cloudflare builds `main` whatever `check.yml` says.
- **M2.** Cards with no stable home:
  - Docs claims that drift from code or config. Only the draft `fn-comments-survive-context` is close, and W3-W6 show this is the repo's most common defect.
  - CI token least privilege and script injection as failable rules (W9).
  - Write-then-check, or non-atomic build output.
  - Tests that depend on build artefacts.
  - Continuous deploy from `main` not gated on CI.
  - Edge-function CPU and quota limits.
  - Independence of evidence for promotion. Nothing stops a self-cited source.
- **M3.** Thin levels: incident has 2 stable cards, and module has 7 core stable cards against 21 drafts.
- **M4.** Audit steps the procedure lacks:
  - Which platform settings to query. I ran 7 `gh api` calls: repo, `branches/main/protection`, `rulesets`, `actions/permissions/workflow`, `dependabot/alerts`, `secret-scanning/alerts`, and `private-vulnerability-reporting`.
  - A step to cross-check doc claims against code and config. That step found W1-W6 and B4.
  - How to tag stable pack cards.
  - The production scope for a repo that deploys continuously.
  - How to show 40+ PASS rows compactly.
  - Whether "Verdict: approve/request changes" belongs in an audit that "certifies nothing".

## Method

Ran:
- In a throwaway clone at `/tmp/claude-1000/.../scratchpad/clone`: `python3 tools/validate.py` (exit 0, 1.0 s) and `python3 tools/build.py` (exit 0: "141 stable cards; llms.txt 10085 chars"). `git status` was clean afterwards, so `skills/` is in sync. Also `python3 tools/agent_ready_check.py` (all pass), `python3 -m unittest discover -s test` (40 OK), and `node --test test/worker.test.mjs` (9 pass).
- In a second fresh clone without a build: `unittest` gave 12 errors.
- Read-only `gh api` calls, listed in M4.
- A regex secret scan over `git log --all -p`.
- A relative-link scan of the Markdown docs.
- An OKLCH→sRGB contrast calculation of the CSS tokens.

Read in full: `SKILL.md`, `references/audit.md`, `codebase.md`, the triage lines of every level and pack, the full text of every card marked FAIL or PASS above, `tools/validate.py`, `schema.py`, `build.py`, `eval.py`, `orgs.py` (head and functions), `src/worker.js`, all workflows, `wrangler.jsonc`, `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `docs/deploy.md`, `docs/PROMOTION.md` (first 60 lines), `test/test_skill.py`, `test_schema.py`, `test_eval.py` (head), and `worker.test.mjs` (head).

Not examined: `tools/agent_ready_check.py` (run, not read), `tools/org_icons.json`, `test/evals/cases/*` inputs, `glossary/`, `docs/research/*` (except grep), `docs/COVERAGE.md` (grep only), `CHANGELOG.md` (grep only), the body text of most of the 141 stable cards (I opened only the cards I marked), and the issue templates.

Could not check: the Cloudflare dashboard (rollout, TLS, Transform Rules), and the live site's headers. I fetched nothing from the network except `gh api`.

Ambiguities I resolved myself:
- **A1.** Brief vs SKILL.md. The brief asks for PASS/FAIL/N/A per rule, and SKILL.md asks for N/A as one count. I listed every FAIL and PASS and grouped the N/As by reason.
- **A2.** Production scope. audit.md skips production "unless the input includes a release". The repo carries its deploy path (`wrangler.jsonc`, `docs/deploy.md`) and deploys on every push to `main`, so I ran production. Its one FAIL is `inferred` and `impact: low`.
- **A3.** Stable pack cards. I tagged them `pack (stable)` and counted them in the ledger (W2).
- **A4.** Card-set version. The "metadata.version above" is in SKILL.md (`1.0`). The commit is `0c3b898`.
- **A5.** Diff-phrased applies_when on non-change cards (W8). I applied `mod-yagni` to options that exist, and left `py-no-init-or-model-tests` N/A.
- **A6.** "Unscoped codebase review" asks for one design-decision line. I put it at the end of the ledger.
- **A7.** "Severity never changes". I kept the block severity on `prod-canary-staged-rollout` and added `impact: low`.

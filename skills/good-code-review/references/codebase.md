# codebase

## code-a11y-check-in-ci

severity: should-fix  
concerns: accessibility, testing  
applies_when: The repo builds a web UI and has an automated test suite.  
context: ui  
tool gate: This card is the gate: axe (through `@axe-core/playwright` or similar) against rendered pages in the test step; `eslint-plugin-jsx-a11y` in the lint step for JSX code.  
Backed by: jsx-eslint project (unjudged), Deque (unjudged), GOV.UK (supports), USWDS (unjudged), Microsoft (unjudged), CivicActions (supports), University of Arizona (supports). Backing: strong.

**Rule.** Run an automated accessibility check, such as axe on rendered pages, in the automated tests, and fail the test on a violation.

**Why.** A violation that nobody sees at review ships. A failing test catches the missing label or `alt` on the pull request that adds it, and run in CI on every pull request it blocks the merge. A JSX lint such as `jsx-a11y` catches some of the same problems earlier, in the editor. Either way it is a floor: tools find only part of the problems, so a person still tests with a keyboard and reviews the results the engine marks "incomplete".

**FAIL**

```js
// e2e: axe runs, but nothing fails on what it finds
const results = await new AxeBuilder({ page }).analyze();
console.log(results.violations.length);
```

**PASS**

```js
// e2e: fail on any axe violation
const results = await new AxeBuilder({ page }).analyze();
expect(results.violations).toEqual([]);
```

**Counterpoint.** "Tools only catch a minority, and we have a backlog, so a failing check would turn every build red." The check catches the cheap failures at no review cost, which frees the manual pass for what only a person can judge. For the backlog, exclude the known violations by name (`disableRules`, `exclude`, or a fingerprint of each known issue) and fail on anything new. Remove each exclusion once it is fixed.

## code-adr

severity: discuss  
concerns: maintainability, process  
applies_when: Auditing whether the reasons behind significant design choices are recorded.  
Backed by: AWS (unjudged), Microsoft (unjudged), Google (unjudged), GOV.UK (unjudged), Spotify (unjudged), Cognitect (unjudged), Rust project (unjudged), Python Software Foundation (unjudged), Kubernetes (unjudged), Oxide Computer Company (unjudged). Backing: unjudged. People cited: Rich Hickey (unjudged).

**Rule.** Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, the options ruled out, and its consequences.

**Why.** Without a record, the next reader reverses a decision blindly or cargo-cults it. A record that weighs only the chosen design, its strengths or its flaws, is not a trade-off analysis, so say why each ruled-out option lost. Give each record a status (proposed, accepted, superseded). Do not edit an accepted record: write a new one that supersedes it and keep the old one. If review finds an undocumented decision, write its record then.

**FAIL**

```text
Repo uses Kafka for one 10-msg/day job. No record why; nobody dares remove it.
```

**PASS**

```text
docs/adr/0007-queue.md: context, decision, consequences, status, and the 2 options ruled out.
```

**Counterpoint.** ADRs rot and become paperwork. Keep each to a page, write them only for hard-to-reverse choices, and mark superseded ones.

## code-ai-pr-disclosure

severity: should-fix  
concerns: process  
applies_when: A pull request was written in whole or part by an AI tool.  
tool gate: PR template checkbox for AI assistance; commit trailer check.  
Backed by: Linux kernel (unjudged), Ghostty (unjudged), Godot Engine (unjudged). Backing: unjudged.

**Rule.** Disclose AI assistance in the PR, and have a human author who can explain and defend every changed line without the tool.

**Why.** Reviewers calibrate by who wrote the code. An undisclosed generated change gets the wrong scrutiny, and an author who cannot explain it leaves the reviewer to do the author's job.

**FAIL**

```text
PR description: "Add retry logic."
(500 generated lines; asked why a 3rd retry, the author says "the model chose it")
```

**PASS**

```text
PR description: "Add retry logic. Drafted with <tool>; I read and tested every line.
 Tests: test_retry.py. Not covered: jitter."
Trailer: Assisted-by: <tool>
```

**Counterpoint.** "Disclosure stigmatises tool use." The rule is about scrutiny, not blame: disclosed work is reviewed the same way and merged on the same terms. The agent never signs off or certifies origin; the human does.

## code-build-hermetic

severity: should-fix  
concerns: process  
applies_when: The repository has a build, a packaging, or a release step.  
tool gate: Build twice in clean containers and compare checksums; `diffoscope` shows where two artifacts differ.  
Backed by: Google (unjudged), Reproducible Builds (unjudged), Airbnb (unjudged), Slack (unjudged), Dropbox (unjudged). Backing: unjudged.

**Rule.** Build from declared inputs only, so that the same source revision gives the same artifact.

**Why.** A build that reads whatever is installed on the machine gives different output on different machines, so a bug cannot be reproduced and a release cannot be checked against its source. Tools are inputs too: pin the compiler and toolchain versions, and do not call host binaries. Undeclared shared files also break builds at scale, for example two tasks that clean and use the same `/tmp` directory race each other.

**FAIL**

```yaml
steps:
  - run: make               # uses whatever gcc, node and protoc the runner has
  - run: date > BUILD_ID    # the clock is an undeclared input
```

**PASS**

```yaml
container:
  image: ghcr.io/acme/builder@sha256:4b1e...   # toolchain pinned by digest
steps:
  - run: SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) make   # timestamps come from the commit
```

**Counterpoint.** "Bit-identical builds are overkill." Full reproducibility is the ceiling. Declared inputs, pinned tools, and a recorded revision are the floor, and they cost little. [code-dependency-pinning](codebase.md#code-dependency-pinning) covers dependency pins.

## code-ci-gates

severity: should-fix  
concerns: process  
applies_when: Auditing which checks must pass before a change merges.  
tool gate: Branch protection with required status checks.  
Backed by: OpenSSF (unjudged), Palantir (unjudged), Kubernetes (unjudged). Backing: unjudged. People cited: McIntosh et al. (unjudged).

**Rule.** Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.

**Why.** Any rule that depends on someone remembering will be skipped. Components where changes merge unreviewed or without discussion tend to ship more post-release defects. Changes reach the branch only through a pull request, and force-push and branch deletion are blocked, so what was reviewed is what ships.

**FAIL**

```text
Default branch: no protection. Force-push allowed. CI optional.
```

**PASS**

```text
Protected main: pull request required, 1 approval + required checks (build, test, lint, types).
Force-push and branch deletion blocked.
```

**Counterpoint.** Gates slow small teams, and flaky tests train people to override. Keep gates few and reliable, fix flakes instead of overriding them, and let the gates own the mechanical checks so review time goes to design.

## code-consistency-drift

severity: discuss  
concerns: correctness, maintainability  
applies_when: Auditing whether one concern is solved in several incompatible ways across the repo.  
tool gate: Lint rules that ban the deprecated pattern once a standard is chosen.  
Backed by: The Pragmatic Engineer (unjudged), Google (unjudged), Spotify (unjudged), Uber (unjudged), Cabify (unjudged), Stripe (unjudged). Backing: unjudged. People cited: Sébastien Portebois (unjudged).

**Rule.** For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.

**Why.** Each extra variant is another thing to learn, test, and secure, and drift accumulates through changes that each looked locally fine. Two limiters built two ways enforce the same quota differently. List the older variants and count them, so the migration shows progress and a new one shows up in review.

**FAIL**

```text
Three HTTP clients (requests, urllib3, httpx) with three timeout conventions;
no document says which is current.
```

**PASS**

```text
docs: "use httpx via net/client.py". Lint bans direct requests imports;
legacy sites listed in MIGRATION.md.
```

**Counterpoint.** "Forcing one way can block a better tool." Allow change through a proposal that updates the standard and the migration list, not through a quiet second pattern. Consistency breaks ties. It does not outrank a measured reason to switch.

## code-dead-code

severity: should-fix  
concerns: maintainability  
applies_when: Auditing for code, flags and files that nothing uses.  
tool gate: An unused-code linter in CI (vulture, knip, or deadcode); allowlist each intentional exception with a reason.  
Backed by: Palantir (unjudged), Google (unjudged), Meta (unjudged), Carnegie Mellon SEI (unjudged), Linux kernel (unjudged), NVIDIA (unjudged), Microsoft (unjudged), GitLab (unjudged), Apache Software Foundation (unjudged), Home Assistant (unjudged), Uber (unjudged), Statsig (unjudged), JetBrains (unjudged), Lockheed Martin (unjudged), TUM ESI (unjudged). Backing: unjudged. People cited: Henrik Warne (unjudged), tef (programmingisterrible) (unjudged).

**Rule.** Delete unreferenced functions and variables, unreachable code, commented-out code, and expired feature flags with their branches and configuration.

**Why.** Dead code costs reading time, misleads searches, and gets "fixed" and tested for no benefit. The same holds for unused imports and files nothing links to: delete them too and let version control remember.

**FAIL**

```text
def old_export(): ...      # no caller anywhere in the repo
if FLAGS["legacy_ui"]:     # flag permanently false since release 4
    render_legacy()
# if USE_CACHE: warm()     # commented-out code, kept "just in case"
return result
log.info("done")          # unreachable
```

**PASS**

```text
Unused function, unreachable code, commented-out code and expired-flag branch deleted; version history shows where they went.
The unused-code linter reports 0 symbols, or each is allowlisted with a reason.
```

**Counterpoint.** Code may be called by reflection, plugins, or external users. Check with the detector's config and a grep of consumers. For public API, deprecate first (see `chg-expand-contract`).

## code-dead-docs-deleted

severity: discuss  
concerns: maintainability  
applies_when: Auditing a repo whose docs, READMEs or design notes describe code that has since changed or gone.  
tool gate: A freshness check (last-reviewed date or owner per page) that fails or flags pages untouched past a threshold.  
Backed by: Google (unjudged), GitLab (unjudged), Linux kernel (unjudged). Backing: unjudged.

**Rule.** Delete the docs for code or features that were removed or never shipped, instead of leaving or hiding them.

**Why.** A wrong page is worse than none: readers trust it. A design doc left as a living doc after the code ships drifts the same way, so archive it as a decision record. Version control keeps the history, so deleting loses nothing. Docs known to be wrong go for the same reason.

**FAIL**

```text
docs/design-auth-v1.md   # describes a login flow removed two releases ago, no status line
```

**PASS**

```text
docs/adr/0004-auth.md    # status: superseded by 0009; the old design doc is deleted
```

**Counterpoint.** "Old docs may still help someone." Version control keeps them. The kernel guide allows an outdated-warning banner on a page you cannot fix yet. Mark a still-useful record `superseded` and link the replacement so nobody mistakes it for current.

## code-dependency-licence-sbom

severity: should-fix  
concerns: security  
applies_when: Auditing what third-party code the repo ships and under which terms.  
tool gate: A vulnerability scanner such as OSV-Scanner or Dependabot alerts; an SBOM generator such as Syft.  
Backed by: OWASP (unjudged), OpenSSF (unjudged), CISA (unjudged), NIST (unjudged), GitHub (unjudged), Cabify (unjudged). Backing: unjudged.

**Rule.** Generate an SBOM, and scan dependencies for known vulnerabilities on every change or on a schedule, and raise an alert when a new vulnerability applies. Each ask is judged separately: name which one failed on the FAIL line.

**Why.** Without an inventory, a team cannot answer a disclosed vulnerability quickly. CI is the usual place for both steps: the SBOM then matches what was built, and the scan runs without anyone remembering it. Team policy: also fail the build on a dependency whose licence is not on the approved list.

**FAIL**

```text
No SBOM anywhere, no scanner in CI, and dependency alerts turned off.
```

**PASS**

```text
CI: generate SBOM, run vulnerability scanner, fail on high severity;
release artifacts attach the SBOM; a new advisory for a shipped component raises an alert.
```

**Counterpoint.** SBOMs and scanners create noise that nobody triages. Tune severity thresholds and assign an owner, since an ignored report is worse than none. The licence list is team policy, not a universal rule. Drop it if your team has no licence constraints.

## code-dependency-pinning

severity: block  
concerns: security  
applies_when: Auditing how the repo resolves third-party packages.  
tool gate: Lockfile-required install in CI; dependency-update bot config present.  
Backed by: OWASP (unjudged), OpenSSF (unjudged), Google (unjudged), Python Software Foundation (unjudged), npm (unjudged), Rust project (unjudged), Poetry (unjudged), pnpm (unjudged), Mend Renovate (unjudged), GitLab (unjudged), GitHub (unjudged). Backing: unjudged.

**Rule.** Commit a lockfile with hashes and install from it in CI.

**Why.** Unpinned versions make builds non-reproducible and let a compromised release flow straight into production. Updates should arrive as reviewed, staged changes, not silently. Run an update bot (Dependabot, Renovate or an autoroller) so the lock does not go stale and updates arrive as pull requests. [code-workflow-supply-chain](codebase.md#code-workflow-supply-chain) covers CI action pins.

**FAIL**

```text
requirements.txt:  requests>=2   (no lockfile; CI runs pip install -U)
```

**FAIL** (other ecosystems)

```text
CI: npm install            (rewrites package-lock.json, ignores drift)
CI: go build -mod=mod ./...   (go.sum changes silently)
CI: uv sync               (re-resolves and rewrites uv.lock when it is stale)
CI: poetry install        (no poetry.lock committed, so it resolves and creates one)
```

**PASS**

```text
requirements.lock with hashes; CI: pip install --require-hashes -r requirements.lock
Update bot opens PRs; changes are rolled out in stages.
```

```text
CI: npm ci                       (integrity hashes in package-lock.json; fails on drift)
CI: go mod verify && go build -mod=readonly ./...   (go.sum committed)
CI: uv sync --locked      (fails if uv.lock is stale)
CI: poetry install        (poetry.lock committed; fails if it is stale)
```

**Counterpoint.** Pinning delays security patches. A pin plus an update bot with a defined cadence beats floating versions, because the lock makes the update visible and revertable.

## code-doc-examples-stay-true

severity: discuss  
concerns: maintainability, testing  
applies_when: Auditing docs, READMEs or doc comments that contain code samples.  
tool gate: Rust `cargo test --doc`, Go example functions, Python `doctest`, or a build step that includes samples from files that CI compiles.  
Backed by: Rust project (unjudged), Google (unjudged), Elixir (unjudged). Backing: unjudged.

**Rule.** Run each code example in the docs as a test.

**Why.** A pasted example drifts from the API it shows, and readers copy it. A tested example fails the build when the API changes. Including the sample from a source file that CI builds, instead of pasting it, gives the same protection.

**FAIL**

```text
README.md: a 12-line ```python block pasted by hand, never run
```

**PASS**

```text
README.md: the sample is the body of tests/test_quickstart.py, run by `pytest --doctest-glob`
```

**Counterpoint.** "Some samples are fragments that cannot run." Mark those as fragments and keep them short. The rule is for samples a reader will copy and run.

## code-docs-link-dont-duplicate

severity: discuss  
concerns: maintainability  
applies_when: Auditing docs, READMEs or comments that restate a guide, spec or page that already exists elsewhere.  
Backed by: Google (unjudged), GitLab (unjudged), Mozilla (unjudged), Kubernetes (unjudged). Backing: unjudged.

**Rule.** Link to the existing page or guide instead of rewriting or restating it.

**Why.** Each copy is one more page to keep current, and the copies drift apart. A link has a single owner who fixes it once.

**FAIL**

```text
README.md: a 40-line "How to use git rebase" section copied from the team wiki
```

**PASS**

```text
README.md: Rebase and branch rules are in [the contributing guide](docs/contributing.md#branches).
```

**Counterpoint.** "A link breaks and the reader has to leave the page." Run a link check (see `code-docs-refs-resolve`) and quote only the one line the reader needs here.

## code-docs-link-text-descriptive

severity: discuss  
concerns: accessibility, usability  
applies_when: A diff adds or edits a link in documentation, a README or a user-facing message.  
tool gate: markdownlint `MD059` (descriptive link text) or a regex for "here" and "click here" link text.  
Backed by: Google (unjudged), GitLab (unjudged), Microsoft (unjudged), Kubernetes (unjudged). Backing: unjudged.

**Rule.** Write link text that says where the link goes, never "here", "this page" or "click here".

**Why.** Readers scan links on their own, and screen readers list them out of context. "Here" tells neither what they will find.

**FAIL**

```text
For the deploy steps, click [here](docs/deploy.md).
```

**PASS**

```text
Follow the [deploy steps](docs/deploy.md).
```

**Counterpoint.** "Short link text reads better." The descriptive phrase is usually the words already in the sentence, so it costs no length.

## code-docs-no-directional-words

severity: discuss  
concerns: accessibility  
applies_when: A diff adds documentation text that points to other content or to something on screen.  
tool gate: A Vale rule (`Google.WordList`, `Microsoft.Avoid`) or a regex for "above", "below", "left" and "right" in docs.  
Backed by: Google (unjudged), Microsoft (unjudged), Mozilla (unjudged), GitLab (unjudged), Elastic (unjudged), Red Hat (unjudged). Backing: unjudged.

**Rule.** Do not point to content with "above", "below", "left" or "right"; name it or link to it.

**Why.** A screen reader gives those words no meaning, and the page reflows on a phone. A reorder of the page also turns "the table below" into a false pointer.

**FAIL**

```text
See the example above, and the options in the table below.
```

**PASS**

```text
See [the retry example](#retry-example) and [the options table](#options).
```

**Counterpoint.** "Readers understand 'below'." Most do, until the section moves. A link survives a reorder, and "the following" works where a link is too heavy.

## code-docs-no-future-promises

severity: discuss  
concerns: maintainability  
applies_when: A diff adds text to published documentation that describes a feature, release or date that is not shipped.  
Backed by: Google (unjudged), Kubernetes (unjudged), GitLab (unjudged). Backing: unjudged.

**Rule.** Do not promise unreleased features, versions or dates in published docs.

**Why.** A promise in the docs reads as a commitment. When the plan changes, the page is wrong, readers have planned around it, and nobody owns the fix.

**FAIL**

```text
Bulk export will arrive in the next release.
```

**PASS**

```text
Bulk export is not supported. Track the request in issue #482.
```

**Counterpoint.** "Users want a roadmap." Keep one, outside the reference docs. Link the issue, which says what is planned without a date.

## code-docs-no-minimising-words

severity: discuss  
concerns: usability  
applies_when: A diff adds documentation text that describes a task or a step.  
tool gate: A Vale rule (GitLab `SubstitutionWarning`, Google `WordList`) or a regex for "simply", "just", "easily" and "obviously".  
Backed by: Django Software Foundation (unjudged), GitLab (unjudged), Google (unjudged), Docker (unjudged), Elastic (unjudged). Backing: unjudged.

**Rule.** Do not call a step "simple", "easy", "just" or "simply" in docs.

**Why.** What is easy for the author is not easy for a newcomer. A reader who fails at an "easy" step blames themselves, and the word adds nothing to the instruction.

**FAIL**

```text
Simply run the migration, then just restart the worker.
```

**PASS**

```text
Run the migration, then restart the worker.
```

**Counterpoint.** "'Just' softens the tone." Cut the word and keep the instruction. If a step really is optional, say so.

## code-docs-redirect-on-move

severity: discuss  
concerns: maintainability, usability  
applies_when: A diff renames, moves or deletes a published documentation page.  
tool gate: A redirect-file check in CI that fails when a page is removed and no redirect names it.  
Backed by: GitLab (unjudged), Cloudflare (unjudged), GitHub (unjudged), Microsoft (unjudged), TYPO3 (unjudged), Mozilla (unjudged). Backing: unjudged.

**Rule.** Add a redirect from the old URL in the same change that moves, renames or deletes a documentation page.

**Why.** Links in issues, search results and other docs keep pointing at the old address. Without a redirect they land on a 404, and the broken links are found one reader at a time.

**FAIL**

```text
Diff: git mv docs/deploy.md docs/ops/deploy.md   (no redirect entry)
```

**PASS**

```text
Diff: git mv docs/deploy.md docs/ops/deploy.md
      redirects.yml: /docs/deploy -> /docs/ops/deploy
```

**Counterpoint.** "Internal docs have few outside links." Then the redirect is a one-line file. Skip it only for a page that was never published.

## code-docs-refs-resolve

severity: should-fix  
concerns: maintainability  
applies_when: Auditing a repo whose README, guides or AGENTS.md cite file paths, anchors or other pages.  
tool gate: A link checker in CI, such as lychee (`lychee --offline --include-fragments docs README.md`) or mdBook linkcheck.  
Backed by: GitHub (unjudged), GitLab (unjudged), Rust project (unjudged). Backing: unjudged.

**Rule.** Run a link check in CI over the docs, so that every relative link and anchor they cite resolves.

**Why.** A rename or a deleted file leaves docs that point at nothing. Readers and agents then follow a dead path, and nobody notices until someone trips on it. A machine finds a dangling reference on the pull request that causes it.

**FAIL**

```text
README.md:  See [the deploy guide](docs/deploy.md).      <- docs/deploy.md was renamed to docs/ops/deploy.md
AGENTS.md:  See [Setup](docs/dev.md#setup).             <- the heading was renamed
CI:         no link check, no job reads the docs
```

**PASS**

```yaml
docs-links:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@<40-char-sha>
    - run: lychee --offline --include-fragments README.md AGENTS.md docs
```

**Counterpoint.** "External links flake, so the job will be red half the time." Check local paths and anchors on every change, where the result is stable. Run the external links on a schedule, so a dead site never blocks a merge.

## code-env-files-ignored

severity: should-fix  
concerns: security  
applies_when: Auditing a repo whose application reads settings from .env files.  
tool gate: A secret scan on push; a CI check that `git ls-files` lists no .env.local or .env file with real values.  
Backed by: Laravel (unjudged), Symfony (unjudged), Vercel (unjudged), Vite (unjudged). Backing: unjudged.

**Rule.** Git-ignore local environment files that hold real values; commit only a template with placeholders.

**Why.** An `.env` file with real credentials, once committed, sits in every clone and in history, and deleting it later does not recall the copies ([code-secrets-not-plaintext-in-repo](codebase.md#code-secrets-not-plaintext-in-repo)). A committed template with placeholder values still tells the next developer which variables the app needs.

**FAIL**

```text
.gitignore:   (no .env entries)
.env          DB_PASSWORD=S3cr37-prod        (tracked by git)
```

**PASS**

```text
.gitignore:   .env
              .env.*.local
.env.example  DB_PASSWORD=change-me          (tracked, placeholders only)
```

**Counterpoint.** Frameworks such as Symfony and Next.js commit a `.env` of non-secret defaults, and an encrypted env file can be committed too. Both are fine: the check is that no file in the repo holds a real credential in plaintext, and that local override files are ignored.

## code-file-lines-ceiling

severity: discuss  
concerns: maintainability, process  
applies_when: Auditing a repo for files that have grown past comprehension.  
tool gate: Pylint too-many-lines (C0302, max-module-lines default 1000), ESLint max-lines, or Checkstyle FileLength, with an allowlist for generated files.  
Backed by: Pylint (unjudged), ESLint (weak), Checkstyle (weak), RuboCop (unjudged), PMD (unjudged). Backing: mixed. People cited: Sébastien Portebois (unjudged), tef (programmingisterrible) (unjudged).

**Rule.** Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.

**Why.** Huge files hide unrelated decisions, attract merge conflicts, and cannot be understood in one read. Linters ship a default for this because a file that passes it is "hard to understand" (Checkstyle). The defaults differ from 300 to 2,000 lines, so pick one and enforce it.

**FAIL**

```text
$ wc -l src/*.py | sort -n | tail -2
  4,812 src/utils.py
  3,105 src/app.py
```

**PASS**

```text
pylint: max-module-lines = 1000; no hand-written file over it; generated files listed in an allowlist.
```

**Counterpoint.** Ousterhout favours deep modules and a long file can be coherent. Splitting for its own sake adds shallow pieces. 1,000 lines is a trigger for a look, not a verdict. The fix is to separate decisions (his information-leakage and temporal-decomposition flags).

## code-flaky-test-quarantine

severity: should-fix  
concerns: testing, process  
applies_when: Auditing how the codebase handles tests that pass and fail on the same code.  
Backed by: Dropbox (unjudged), Shopify (unjudged), Cabify (unjudged), Atlassian (supports), GitLab (supports), Airtable (supports). Backing: strong.

**Rule.** Report every test that passes only on retry, move it to a quarantine with a named owner and a ticket, and return it to the merge gate only after it passes many reruns.

**Why.** A test that fails at random on unchanged code teaches people to rerun until green, and then a real regression looks like noise. Dropbox removes tests that fail too often from the main pool and files a bug against the owner. Its fix workflow then runs the test 100 or more times in CI before the fix lands. Give the ticket a due date, so a quarantined test gets fixed or deleted instead of sitting there for good. Shopify retries a failed test but tells developers about every pass after a retry. The usual causes are a fixed pause where the test should wait for an element (Shopify) and state left behind by an earlier test (Cabify, Dropbox).

**FAIL**

```yaml
# .github/workflows/test.yml
- run: pytest --reruns 3          # a pass on retry counts as a pass, and nobody hears about it
```

**PASS**

```yaml
# .github/workflows/test.yml
- run: pytest --reruns 3 -m "not quarantine" --junitxml=report.xml
- run: python tools/flaky_report.py report.xml   # opens a ticket per pass after retry, owner from CODEOWNERS
# nightly.yml: a quarantined test rejoins the gate after 100 clean runs
- run: pytest -m quarantine --count 100
```

**Counterpoint.** "Retries keep the build green, and quarantine hides coverage." Shopify's data backs retries: a slightly slower build beats an engineer rerunning it by hand. Retries are fine when each pass after a retry reaches someone. A quarantined test still runs outside the gate, and its owner and ticket stop it from staying there for good. Skipping or deleting a flaky test in a diff is a separate FAIL. See [chg-no-silenced-diagnostics](change.md#chg-no-silenced-diagnostics). For the merge gate itself, see [code-ci-gates](codebase.md#code-ci-gates).

## code-gate-new-violations-only

severity: should-fix  
concerns: maintainability, process  
applies_when: Auditing a codebase that adopted a linter, a quality gate or an architecture rule after most of its code existed.  
tool gate: A baseline or frozen violation store with CI set to read it but not rewrite it (ArchUnit `FreezingArchRule`, a linter baseline file).  
Backed by: SonarSource (unjudged), ArchUnit (unjudged), Google (unjudged). Backing: unjudged.

**Rule.** Gate CI on new or modified code, and track pre-existing violations in a separate store without letting a build add to it.

**Why.** A gate that fails on thousands of old findings gets switched off, and a gate with no record of them lets the debt grow unseen. Failing only on new findings keeps the gate on and stops the debt growing, and the store shows what is left to pay down.

**FAIL**

```properties
# archunit.properties
freeze.refreeze=true
```

CI refreezes on each run, so a new violation is absorbed and the build stays green.

**PASS**

```properties
# archunit.properties
freeze.store.default.path=archunit_store
freeze.store.default.allowStoreCreation=false
freeze.store.default.allowStoreUpdate=false
```

```java
@ArchTest
static final ArchRule no_cycles =
    FreezingArchRule.freeze(slices().matching("com.app.(*)..").should().beFreeOfCycles());
```

**Counterpoint.** "A baseline hides real problems." It lists them in a file under version control, in plain view, and a change that touches a baselined spot is held to the full rule. Pair it with a plan to shrink the store.

## code-perf-budget-in-ci

severity: should-fix  
concerns: performance, process  
applies_when: The repo has a performance target (bundle size, page metrics, latency under load, or a benchmark) that matters to users.  
tool gate: Lighthouse CI assert, size-limit, k6 thresholds, Gatling assertions, or a benchstat comparison in CI.  
Backed by: Google (unjudged), Size Limit project (unjudged), Grafana Labs (unjudged), Gatling (unjudged), Microsoft (unjudged), AWS (unjudged), Mozilla (unjudged). Backing: unjudged.

**Rule.** Write the performance budget down as a CI check that fails the build when it is exceeded.

**Why.** Performance regresses a few percent at a time, and no reviewer sees a 3% slowdown in a diff. A budget that only warns becomes a log line nobody reads.

**FAIL**

```text
lighthouserc.json: "assertions": { "categories:performance": ["warn", { "minScore": 0.9 }] }
k6 script with no thresholds block
```

**PASS**

```text
size-limit: [{ "path": "dist/app.js", "limit": "180 kB" }]   # npm run size in CI
k6: thresholds: { http_req_duration: ["p(95)<300"] }        # non-zero exit fails the job
```

**Counterpoint.** "Benchmarks in CI are noisy and flake." They are when a gate trusts one run. Gate on a stable budget, compare repeated runs (benchstat wants 10 to 20), and keep the threshold above the noise. On a site with much room to improve, a tight budget only turns every build red, so set it at today's level and lower it later.

## code-readme-per-module

severity: discuss  
concerns: maintainability  
applies_when: Auditing a repo with several packages, modules or self-contained components.  
tool gate: A CI check that every package root holds a README (a glob test, or a docs linter).  
Backed by: Google (unjudged), Microsoft (unjudged), HashiCorp (unjudged), GitHub (unjudged). Backing: unjudged.

**Rule.** Give each package, module or self-contained component a README at its root that says what it holds and how to use it.

**Why.** A reader landing in a directory from search or a stack trace has no other place to learn what the code is for. The README is the one file everyone opens first.

**FAIL**

```text
services/billing/    (12 files, no README)
```

**PASS**

```text
services/billing/README.md   What billing owns, how to run its tests, who to ask.
```

**Counterpoint.** "A README per folder is clutter." The rule stops at the unit that has its own purpose. Leave plain subfolders without one.

## code-release-gated-on-ci

severity: should-fix  
concerns: reliability, process  
applies_when: Auditing a workflow or pipeline that publishes a release when a tag is pushed.  
tool gate: Release job with `needs:` the test job, or a `workflow_run` trigger checked for `conclusion == 'success'`; a tag ruleset with required status checks.  
Backed by: Kubernetes (unjudged), GitHub (unjudged), GitLab (unjudged), OpenJS Foundation (supports), Envoy (supports), Google (supports). Backing: strong.

**Rule.** Make a release or publish job depend on the checks passing for the tagged commit, never on the tag alone.

**Why.** A tag can point at a commit that was never built or tested, or one whose checks are red. A workflow that fires on the tag then ships it. Branch protection does not help, because the tag does not go through a pull request.

**FAIL**

```yaml
on:
  push:
    tags: ["v*"]
jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>
      - run: make publish
```

**PASS**

```yaml
on:
  push:
    tags: ["v*"]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>
      - run: make test
  publish:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>
      - run: make publish
```

**Counterpoint.** "CI already passed on the pull request, so rerunning tests on the tag wastes time." The pull request tested another commit if the base moved or the tag was cut elsewhere. Reuse the result by requiring the status check on the tagged commit, instead of dropping the gate.

## code-rule-has-enforcer

severity: should-fix  
concerns: maintainability  
applies_when: Auditing any written repo rule (AGENTS.md, CONTRIBUTING, a docs page, a code comment, repeated review comments) that a type check, lint rule, test or CI check could enforce.  
tool gate: The enforcer itself: a type, a lint rule or a CI check.  
Backed by: Cursor (unjudged), Spotify (unjudged), Stripe (unjudged), Cabify (unjudged). Backing: unjudged.

**Rule.** Back each written repo rule that a type, lint or CI check could enforce with that check, not with a line in an instruction file or a repeated review comment.

**Why.** A rule that relies on memory gets broken, and reviewers then repeat the same correction. An instruction file is advisory: a person or an agent can skip it. A lint message that names the fix teaches it at the moment of the mistake. A "do not remove" code comment has the same weakness as an instruction file line. Where no static check can see the rule, a hook or script that blocks the action is the enforcer.

**FAIL**

```text
CONTRIBUTING.md: "never call requests.get without a timeout"   (no lint rule)
Review history: the same comment on 6 PRs
```

**PASS**

```toml
# pyproject.toml, checked by ruff in CI
[tool.ruff.lint]
extend-select = ["S113"]   # request-without-timeout
```

```go
// rules_test.go, run by `go test ./...` in CI
func TestNoBareHTTPGet(t *testing.T) { /* walk the AST, fail on http.Get */ }
```

**Counterpoint.** "Not every rule is checkable." Right, and judgement rules stay as prose. The FAIL is a checkable rule with no check. See [code-ci-gates](codebase.md#code-ci-gates) for where checks run, and [chg-review-signal](change.md#chg-review-signal) for what reviewers stop commenting on once a tool owns it.

## code-scoped-validation-loop

severity: discuss  
concerns: testing, process  
applies_when: Auditing how a contributor checks a small change.  
tool gate: A documented command that runs tests and lint for one path or package.  
Backed by: Cursor (unjudged), Google (supports), Django Software Foundation (supports), Python Software Foundation (supports). Backing: strong.

**Rule.** Document a command that checks one package or path, with readable output, so a small change does not need the full-repo run.

**Why.** If the only check takes twenty minutes or prints thousands of lines, people skip it and push to CI, and agents cannot tell which failure is theirs.

**FAIL**

```text
CONTRIBUTING.md: "run `make test` (all 14,000 tests, ~25 min)"
```

**PASS**

```text
pytest tests/billing -q        # about 20 s
ruff check src/billing
```

**Counterpoint.** "CI runs everything anyway." CI is the last check, not the loop. A scoped command lets the author find a failure in seconds instead of after a push.

## code-secret-scan

severity: block  
concerns: security, process  
applies_when: Any repository, including its history, issues and pull requests.  
tool gate: Secret scanning on push (provider or pre-commit hook) with push protection on.  
Backed by: GitHub (unjudged), OWASP (unjudged), CISA (unjudged), GitLab (unjudged). Backing: unjudged.

**Rule.** Scan for committed credentials, and treat any hit as leaked: revoke and replace it first. With no scanner present and no secret found, the FAIL is the missing control; evidence is "absent in <paths>". A platform scanner (GitHub secret scanning with push protection, GitLab secret detection) counts when it is enabled on the repo and covers history.

**Why.** A secret in history is readable by everyone with clone access, and forks and caches keep it after a rewrite. Rewriting history is slow and often unnecessary once the secret is dead.

**FAIL**

```text
git log -p | rg 'AKIA'      # a live cloud key in an old commit; "removed it in the next commit"
```

**PASS**

```text
scanner runs on every push and covers history
key revoked and reissued the same day; new value comes from the secret store
```

**Counterpoint.** "Scanners give false positives." Tune with an allowlist of reviewed, non-secret strings. A missed live key costs far more than a triaged alert. When you run a scanner as part of a review, run it with live verification off: checking a hit against the issuing service sends the secret to a third party and shows up in the reviewer's network logs. Treat the hit as leaked without the check. [sys-secrets-and-errors](system.md#sys-secrets-and-errors) covers where secrets live at runtime.

## code-secrets-not-plaintext-in-repo

severity: should-fix  
concerns: security  
applies_when: Auditing source files, config files and infrastructure code for credentials, keys and tokens.  
tool gate: Secret scanning on push; a lint that rejects literal values for fields named password, token or key.  
Backed by: OWASP (unjudged), GitLab (unjudged), CISA (unjudged), Laravel (unjudged), Symfony (unjudged), Vercel (unjudged), Vite (unjudged). Backing: unjudged.

**Rule.** Keep secrets out of source code and config.

**Why.** Anyone with read access to the repository, and every clone and fork, gets a plaintext secret, and removing it later does not recall the copies. Read the secret at run time from a secret store, and it can be rotated without a code change. [code-env-files-ignored](codebase.md#code-env-files-ignored) covers local `.env` files.

**FAIL**

```python
DB_PASSWORD = "S3cr37-prod"
conn = connect(host="db.internal", user="app", password=DB_PASSWORD)
```

**PASS**

```python
import os
conn = connect(host="db.internal", user="app", password=os.environ["DB_PASSWORD"])
```

**Counterpoint.** "Environment variables are plaintext too, and they leak into process listings and crash dumps." True, so the secret store is the source and the variable is only the hand-off. Mount the value from the store at start, and keep it out of logs. [code-secret-scan](codebase.md#code-secret-scan) covers finding a secret that is already committed.

## code-test-fixtures-built-once

severity: should-fix  
concerns: testing, performance  
applies_when: Auditing a test suite in which many tests share an expensive setup (a database schema and seed data, a container, a loaded application context).  
tool gate: A CI job timeout plus a slowest-tests report in the build log (pytest or Django --durations, Gradle build scan).  
Backed by: Django Software Foundation (unjudged), Ruby on Rails (unjudged), Spring (unjudged), Laravel (unjudged), Ecto (unjudged), SQLAlchemy (unjudged), Microsoft (unjudged), Alloy.ai (unjudged), GitLab (unjudged). Backing: unjudged.

**Rule.** Build an expensive fixture once per test run, and reset state between tests with a rollback or a truncate, never a rebuild.

**Why.** A fixture that takes 20 seconds costs 20 seconds times the number of tests that rebuild it, and adding tests adds that cost again. One team measured about 10 seconds to drop, recreate and migrate a database per test and a 14-minute suite for 78 integration tests; wrapping each test in a rolled-back transaction cut it to 8 minutes. A slow suite then gets skipped locally, and changes arrive in larger, riskier batches.

**FAIL**

```text
before each test:
    create database; run all migrations; load seed data     # 20-30 s
after each test:
    drop database
```

**PASS**

```text
once per run (session, test binary, or global setup):
    create database; run all migrations; load seed data
before each test:  begin a transaction (or savepoint)
after each test:   roll it back
tests that must commit: their own database, cleaned with DELETE or TRUNCATE after each test, run serially
```

**Counterpoint.** "A shared fixture breaks test isolation and blocks parallel runs." It does when the shared part is mutable or when tests commit. Keep the shared part read-only, undo each test's writes by rollback, give each parallel worker its own database, and give the few tests that must commit a separate database. A database kept between runs goes stale after a schema change, so rebuild it when the migrations change.

## code-test-pyramid-shape

severity: discuss  
concerns: testing, process  
applies_when: Auditing a repo whose layout or CI report separates unit, integration and end-to-end tests, so a reviewer can count tests per tier. Without that split there is no count to fail, so mark the card N/A.  
tool gate: A CI report that prints the number of tests per tier next to the run time.  
Backed by: Google (unjudged), GitLab (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Keep most tests at the unit level, fewer at the integration level and fewest end-to-end.

**Why.** End-to-end tests are the slowest to run and the costliest to keep working, and a failure in one points at the whole system, not at a line. A suite that leans on them gives slow, flaky feedback. Unit tests run in milliseconds and locate the failure. The mix is a guide, not a quota.

**FAIL**

```text
CI report: unit 40, integration 120, end-to-end 310 (65% end-to-end).
Full run: 55 minutes.
```

**PASS**

```text
CI report: unit 1,450, integration 210, end-to-end 38 (about 85/12/2).
Full run: 11 minutes.
```

**Counterpoint.** "Our service is a thin layer over a database, and a UI-heavy app gets little from unit tests." Fair: such systems get more value from integration tests, and the right mix is not fixed. Raise a finding only when end-to-end tests clearly dominate and the run is slow, and raise it for discussion, not as a defect.

## code-test-selection-on-pr

severity: discuss  
concerns: testing, performance, process  
applies_when: A pull-request CI job runs a test suite that is slower than the team's feedback target for a pull request. Mark `N/A` when the full suite already fits the target.  
tool gate: A PR job that runs the affected-tests command (`nx affected -t test`, Azure Test Impact Analysis, Develocity Predictive Test Selection), plus a full-suite job off the PR path.  
Backed by: Meta (unjudged), Microsoft (unjudged), Shopify (unjudged), Google (unjudged), Nx (unjudged), Gradle (unjudged). Backing: unjudged.

**Rule.** When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.

**Why.** A full suite on every pull request makes the queue wait for tests the change cannot break. Meta runs a third of the affected tests and reports catching more than 99.9 percent of regressions. Shopify runs the tests related to the change. Meta and Gradle pick them with a model trained on past results, not from what the change touches. The full run still happens, outside the pull-request gate.

**FAIL**

```yaml
# the only test job
on: pull_request
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest          # 40-minute suite on every PR, no nightly or pre-deploy run
```

**PASS**

```yaml
# .github/workflows/pr.yml
on: pull_request
jobs:
  affected:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: nx affected -t test

# .github/workflows/nightly.yml
on:
  schedule: [{ cron: "0 3 * * *" }]
jobs:
  full:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pytest
```

**Counterpoint.** "Selection misses regressions." Shopify says a stale mapping let failing tests merge, about 0.06 percent of pull requests, and Shopify and Microsoft run every test when they cannot map or classify a change. Keep the full run, fall back to all tests when the mapping cannot decide, and do not present the pull-request run as full coverage. The selected tests gate the merge, as [code-ci-gates](codebase.md#code-ci-gates) asks; the full run comes before deploy or on a schedule.

## code-tests-no-fixed-sleep

severity: should-fix  
concerns: testing, reliability  
applies_when: Auditing a test suite, or reviewing a diff that adds or changes a test that waits for something to happen.  
tool gate: Grep the test directories for sleep calls (`time.sleep`, `Thread.sleep`, `cy.wait(<number>)`) and fail CI on a new one.  
Backed by: Google (unjudged), Microsoft (unjudged), Cypress (unjudged). Backing: unjudged.

**Rule.** Do not wait in a test on a fixed delay; wait for the condition you need, or inject a clock.

**Why.** A delay that is long enough on a fast machine is too short on a loaded CI runner, so the test turns flaky, and it adds its whole length to every run even when the thing it waits for finished at once. A sleep also often means the code reaches a dependency the test should have replaced. For the same reasons, small unit tests do no real network, database or file-system I/O.

**FAIL**

```python
import time
from concurrent.futures import ThreadPoolExecutor

def test_job_finishes():
    pool = ThreadPoolExecutor()
    future = pool.submit(run_job)
    time.sleep(5)
    assert future.done()
```

**PASS**

```python
from concurrent.futures import ThreadPoolExecutor

def test_job_finishes():
    with ThreadPoolExecutor() as pool:
        future = pool.submit(run_job)
        assert future.result(timeout=5) == "done"
```

**Counterpoint.** "Some systems give no signal to wait on, so polling with a sleep is the only way." Poll with a short interval and a deadline, and return as soon as the condition holds, so the delay is a ceiling and not a cost. End-to-end and integration tests legitimately use real I/O and polling; the rule bans the fixed wait, not the poll.

## code-vuln-remediation-window

severity: should-fix  
concerns: security, process  
applies_when: The repo has open dependency alerts, update pull requests, or scan reports; with none open, mark it N/A.  
tool gate: Dependabot or Renovate alerts with a severity SLA; OSV-Scanner or Scorecard `Vulnerabilities` in CI.  
Backed by: OpenSSF (unjudged), CISA (unjudged), GitHub (unjudged), OWASP (unjudged), Cabify (unjudged). Backing: unjudged.

**Rule.** Write down how long a known-vulnerable dependency may stay unfixed and fix or upgrade it inside that window.

**Why.** A scan that finds a vulnerability and then sits unread protects nobody. An alert left open past its window is the failure, whatever the tool says. If a fix is not possible, record the accepted risk with the CVE, the reason, an owner and an expiry date that lapses on its own, so the open alert is a decision and not an oversight. [code-dependency-licence-sbom](codebase.md#code-dependency-licence-sbom) covers running the scan, and this card covers acting on the result.

**FAIL**

```text
Dependabot: 14 open alerts, 3 critical, oldest opened 210 days ago.
Open update PRs for those alerts: unreviewed. No stated window, no dismissal reason.
```

**PASS**

```text
SECURITY.md: critical and exploited: 7 days; high: 30 days; medium: 60 days.
Open alerts: all younger than their window.
```

**Counterpoint.** "Most alerts are not reachable in our code, so the window is busywork." Then triage the alert inside the window and dismiss it with the reason. Reachability is a finding to record, not a reason to skip the clock.

## code-workflow-supply-chain

severity: block  
concerns: security, process  
applies_when: Auditing CI workflow files and release pipelines.  
tool gate: OpenSSF Scorecard `Pinned-Dependencies` and `Dangerous-Workflow` checks; zizmor `unpinned-uses` audit.  
Backed by: OpenSSF (unjudged), OWASP (unjudged), GitHub (unjudged), StepSecurity (unjudged), GitLab (unjudged). Backing: unjudged.

**Rule.** Pin every CI action to a full commit SHA, and keep code from an unreviewed change out of any job that holds secrets or can deploy.

**Why.** The pipeline holds secrets and publish rights, so a compromised action or injected input owns the artifact. A privileged trigger that checks out a fork runs the fork's code with the base repository's token and secrets. Give workflows least-privilege tokens, keep untrusted event data out of `run:` and out of `pull_request_target` checkouts, and attach build provenance to releases. Review a change to the workflow file like any other code, because it can grant the next job anything. [code-dependency-pinning](codebase.md#code-dependency-pinning) covers dependency pins, and [code-dependency-licence-sbom](codebase.md#code-dependency-licence-sbom) covers the inventory.

**FAIL**

```yaml
on: pull_request_target
permissions: write-all
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4        # tag, can be moved to other code
        with:
          ref: ${{ github.event.pull_request.head.sha }}
      - run: ./build.sh                  # runs the PR author's code with the base repo's token
```

**PASS**

```yaml
on: pull_request
permissions:
  contents: read
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@<40-char-sha>   # v4.2.2
      - uses: some/action@<40-char-sha>        # v3.1.0
  deploy:
    if: github.ref == 'refs/heads/main'      # never runs for a fork or an unmerged change
    needs: build
    runs-on: ubuntu-latest
    environment: production                  # protected environment: required reviewers, scoped secrets
    steps:
      - run: ./deploy.sh
```

**Counterpoint.** "SHA pinning blocks automatic fixes and adds update churn." Let an update bot propose SHA bumps, so fixes still arrive as reviewed changes. Where the platform offers a lockfile for workflow dependencies, that lockfile is stronger than SHA pins and meets this check. A `pull_request_target` job can be safe when it never checks out or runs the fork's code, but splitting the privileged job from the untrusted one is easier to review than keeping them together.

## code-workflow-token-per-job-write

severity: should-fix  
concerns: security  
applies_when: Auditing GitHub Actions workflow files.  
tool gate: OpenSSF Scorecard `Token-Permissions` check; zizmor `excessive-permissions` audit.  
Backed by: OpenSSF (unjudged), Rust project (unjudged), GitHub (unjudged). Backing: unjudged.

**Rule.** Set workflow token permissions to read-only or none at the top level and grant write only on the job that needs it.

**Why.** Every job in a workflow gets the workflow's token. A compromised step in a test job can then push code or edit releases if the token is wide. Write access held by one job shrinks what a bad step elsewhere can do. [code-workflow-supply-chain](codebase.md#code-workflow-supply-chain) covers pinning and untrusted triggers.

**FAIL**

```yaml
permissions: write-all
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - run: make test
  release:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - run: make release
```

**PASS**

```yaml
permissions: {}
jobs:
  test:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - run: make test
  release:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: write
    steps:
      - run: make release
```

**Counterpoint.** "Repeating permissions on every job is noise." Only the jobs that need more than the top level repeat anything, and a missing key fails closed. The noise is the point: each grant shows in review.

## code-workload-identity

severity: should-fix  
concerns: security  
applies_when: A CI job or a service authenticates to a cloud provider.  
Backed by: GitHub (unjudged), Google (unjudged), GitLab (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Exchange the platform's OIDC token for a short-lived cloud credential, and pin the trust policy to the workload.

**Why.** A cloud key stored as a CI secret stays valid until someone rotates it, and every job that reads it can use it elsewhere. An OIDC token is minted for one job, expires with it, and names the repository, branch or environment. The cloud side has to check that name. A trust policy with no `sub` condition lets any repository assume the role. Match on stable IDs, not names that can change, and check the audience too, so a token minted for another service or platform is refused.

**FAIL**

```yaml
env:
  AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
  AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

**PASS**

```yaml
on:
  push:
    branches: [main]
permissions:
  id-token: write
  contents: read
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: aws-actions/configure-aws-credentials@<40-char-sha>
        with:
          role-to-assume: arn:aws:iam::123456789012:role/deploy
          aws-region: eu-west-1
# trust policy condition:
# token.actions.githubusercontent.com:sub: repo:org/repo:ref:refs/heads/main
# repositories created after 15 July 2026, or opted in, use immutable IDs:
# repo:org@123456/repo@456789:ref:refs/heads/main
```

**Counterpoint.** "Static keys work with every provider and every runner." Some providers and self-hosted setups cannot issue an OIDC token, so a scoped key is the fallback. If a key is unavoidable, scope it to the one deploy action, keep it in the platform's secret store rather than in the repository, rotate it, and keep the deploy job away from pull request code. Where OIDC is available, use it and pin the claim.

## py-ruff-gate

severity: should-fix  
concerns: maintainability  
applies_when: The project is Python and has a linter configuration.  
tool gate: ruff  
Backed by: no organisation yet. People cited: Pablo González (unjudged).

**Rule.** Enable the Ruff rule sets E, F, I, B, UP, SIM, BLE, TID and D in CI.

**Why.** The tool owns formatting, import order, the choice between `Optional` and `X | None`, bare `except`, and relative imports. Human review time goes to what tools cannot see. `D1xx` stays ignored: the gate checks docstring format, not presence. Anything the gate decides is not a review comment; the comment is "add the gate".

**FAIL**

```toml
[tool.ruff.lint]
select = ["E", "F"]
```

**PASS**

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "BLE", "TID", "D"]
ignore = ["D100", "D101", "D102", "D103", "D104", "D105", "D106", "D107"]
[tool.ruff.lint.pydocstyle]
convention = "google"
[tool.ruff.lint.flake8-tidy-imports]
ban-relative-imports = "all"
```

**Counterpoint.** "Strict lint slows contributors." It speeds review: repeated nitpicks are a sign of a missing gate (Google, Pragmatic Engineer notes).

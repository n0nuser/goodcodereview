# codebase

## code-a11y-check-in-ci

severity: should-fix  
concerns: accessibility, testing  
applies_when: The repo builds a web UI and has an automated test suite.  
context: ui  
tool gate: This card is the gate: axe (through `@axe-core/playwright` or similar) against rendered pages in the test step; `eslint-plugin-jsx-a11y` in the lint step for JSX code.  
Backed by: jsx-eslint project (unjudged), Deque (unjudged), GOV.UK (supports), USWDS (unjudged), Microsoft (unjudged), CivicActions (supports), University of Arizona (supports). Backing: strong.

**Rule.** Run an automated accessibility check, such as axe on rendered pages, in the automated tests, and fail the test on a violation.

**Why.** A violation that nobody sees at review ships. A failing test catches the missing label or `alt` on the pull request that adds it, and run in CI on every change it blocks the merge. A JSX lint such as `jsx-a11y` catches some of the same problems earlier, in the editor. Either way it is a floor: tools find only part of the problems, so a person still tests with a keyboard.

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

**Rule.** Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, and its consequences.

**Why.** Without a record, the next reader reverses a decision blindly or cargo-cults it. Also list the options you ruled out and why: a record that weighs only the chosen design, its strengths or its flaws, is not a trade-off analysis.

**FAIL**

```text
Repo uses Kafka for one 10-msg/day job. No record why; nobody dares remove it.
```

**PASS**

```text
docs/adr/0007-queue.md: context, decision, consequences, status, and the 2 options ruled out.
```

**Counterpoint.** ADRs rot and become paperwork. Keep each to a page, write them only for hard-to-reverse choices, and mark superseded ones.

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

**Why.** Any rule that depends on someone remembering will be skipped. Components where changes merge unreviewed or without discussion tend to ship more post-release defects.

**FAIL**

```text
Default branch: no protection. Force-push allowed. CI optional.
```

**PASS**

```text
Protected main: 1 approval + required checks (build, test, lint, types).
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
Backed by: Palantir (unjudged), Google (unjudged), Meta (unjudged), Carnegie Mellon SEI (unjudged), Linux kernel (unjudged), NVIDIA (unjudged), Microsoft (unjudged), GitLab (unjudged), Uber (unjudged), Statsig (unjudged), JetBrains (unjudged), Lockheed Martin (unjudged). Backing: unjudged. People cited: Henrik Warne (unjudged), tef (programmingisterrible) (unjudged).

**Rule.** Delete unreferenced functions and variables, and the branches of expired feature flags.

**Why.** Dead code costs reading time, misleads searches, and gets "fixed" and tested for no benefit. The same holds for the common cases of commented-out code and files nothing links to: delete them too and let version control remember.

**FAIL**

```text
def old_export(): ...      # no caller anywhere in the repo
if FLAGS["legacy_ui"]:     # flag permanently false since release 4
    render_legacy()
```

**PASS**

```text
Unused function and expired-flag branch deleted; version history shows where they went.
The unused-code linter reports 0 symbols, or each is allowlisted with a reason.
```

**Counterpoint.** Code may be called by reflection, plugins, or external users. Check with the detector's config and a grep of consumers. For public API, deprecate first (see `chg-expand-contract`).

## code-dependency-licence-sbom

severity: should-fix  
concerns: security  
applies_when: Auditing what third-party code the repo ships and under which terms.  
tool gate: A vulnerability scanner such as OSV-Scanner or Dependabot alerts; an SBOM generator such as Syft.  
Backed by: OWASP (unjudged), OpenSSF (unjudged), CISA (unjudged), NIST (unjudged), GitHub (unjudged), Cabify (unjudged). Backing: unjudged.

**Rule.** Generate an SBOM, and scan dependencies for known vulnerabilities on every change or on a schedule. Each ask is judged separately: name which one failed on the FAIL line.

**Why.** Without an inventory, a team cannot answer a disclosed vulnerability quickly. CI is the usual place for both steps: the SBOM then matches what was built, and the scan runs without anyone remembering it. Team policy: also fail the build on a dependency whose licence is not on the approved list.

**FAIL**

```text
No SBOM anywhere, no scanner in CI, and dependency alerts turned off.
```

**PASS**

```text
CI: generate SBOM, run vulnerability scanner, fail on high severity;
release artifacts attach the SBOM.
```

**Counterpoint.** SBOMs and scanners create noise that nobody triages. Tune severity thresholds and assign an owner, since an ignored report is worse than none. The licence list is team policy, not a universal rule. Drop it if your team has no licence constraints.

## code-dependency-pinning

severity: block  
concerns: security  
applies_when: Auditing how the repo resolves third-party packages.  
tool gate: Lockfile-required install in CI; dependency-update bot config present.  
Backed by: OWASP (unjudged), OpenSSF (unjudged), Google (unjudged), Python Software Foundation (unjudged), npm (unjudged). Backing: unjudged.

**Rule.** Commit a lockfile with hashes and install from it in CI.

**Why.** Unpinned versions make builds non-reproducible and let a compromised release flow straight into production. Updates should arrive as reviewed, staged changes, not silently. [code-workflow-supply-chain](codebase.md#code-workflow-supply-chain) covers CI action pins.

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

**Why.** A test that fails at random on unchanged code teaches people to rerun until green, and then a real regression looks like noise. Dropbox removes tests that fail too often from the main pool and files a bug against the owner. Its fix workflow then runs the test 100 or more times in CI before the fix lands. Shopify retries a failed test but tells developers about every pass after a retry. The usual causes are a fixed pause where the test should wait for an element (Shopify) and state left behind by an earlier test (Cabify, Dropbox).

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

**Why.** A rule that relies on memory gets broken, and reviewers then repeat the same correction. An instruction file is advisory: a person or an agent can skip it. A lint message that names the fix teaches it at the moment of the mistake. A "do not remove" code comment has the same weakness as an instruction file line.

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

**Counterpoint.** "Scanners give false positives." Tune with an allowlist of reviewed, non-secret strings. A missed live key costs far more than a triaged alert. [sys-secrets-and-errors](system.md#sys-secrets-and-errors) covers where secrets live at runtime.

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

## code-test-selection-on-pr

severity: discuss  
concerns: testing, performance, process  
applies_when: A pull-request CI job runs a test suite that is slower than the team's feedback target for a pull request. Mark `N/A` when the full suite already fits the target.  
tool gate: A PR job that runs the affected-tests command (`nx affected -t test`, Azure Test Impact Analysis, Develocity Predictive Test Selection), plus a full-suite job off the PR path.  
Backed by: Meta (unjudged), Microsoft (unjudged), Shopify (unjudged), Google (unjudged), Nx (unjudged), Gradle (unjudged). Backing: unjudged.

**Rule.** When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.

**Why.** A full suite on every pull request makes the queue wait for tests the change cannot break. Meta runs a third of the affected tests and reports catching more than 99.9 percent of regressions. Shopify runs the tests related to the change. The full run still happens, outside the pull-request gate.

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

**Counterpoint.** "Selection misses regressions." Shopify says a stale mapping let failing tests merge, about 0.06 percent of pull requests, and Microsoft falls back to all tests when it cannot classify a change. Keep the full run, fall back to all tests when the mapping cannot decide, and do not present the pull-request run as full coverage. The selected tests gate the merge, as [code-ci-gates](codebase.md#code-ci-gates) asks; the full run comes before deploy or on a schedule.

## code-vuln-remediation-window

severity: should-fix  
concerns: security, process  
applies_when: The repo has open dependency alerts, update pull requests, or scan reports; with none open, mark it N/A.  
tool gate: Dependabot or Renovate alerts with a severity SLA; OSV-Scanner or Scorecard `Vulnerabilities` in CI.  
Backed by: OpenSSF (unjudged), CISA (unjudged), GitHub (unjudged), OWASP (unjudged). Backing: unjudged.

**Rule.** Write down how long a known-vulnerable dependency may stay unfixed and fix or upgrade it inside that window.

**Why.** A scan that finds a vulnerability and then sits unread protects nobody. An alert left open past its window is the failure, whatever the tool says. If a fix is not possible, record the accepted risk with an owner and a review date, so the open alert is a decision and not an oversight. [code-dependency-licence-sbom](codebase.md#code-dependency-licence-sbom) covers running the scan, and this card covers acting on the result.

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

## code-workload-identity

severity: should-fix  
concerns: security  
applies_when: A CI job or a service authenticates to a cloud provider.  
Backed by: GitHub (unjudged), Google (unjudged), GitLab (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Exchange the platform's OIDC token for a short-lived cloud credential, and pin the trust policy to the workload.

**Why.** A cloud key stored as a CI secret stays valid until someone rotates it, and every job that reads it can use it elsewhere. An OIDC token is minted for one job, expires with it, and names the repository, branch or environment. The cloud side has to check that name. A trust policy with no `sub` condition lets any repository assume the role.

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

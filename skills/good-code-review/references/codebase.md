# codebase

## code-a11y-check-in-ci

severity: should-fix  
concerns: accessibility, testing  
applies_when: The repo builds a web UI and has an automated test suite.  
context: ui  
Backed by: jsx-eslint project, Deque, GOV.UK, USWDS, Microsoft, CivicActions, University of Arizona.

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
Backed by: AWS, Microsoft, Google, GOV.UK, Spotify, Cognitect. People cited: Rich Hickey.

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
Backed by: Google, Reproducible Builds, Airbnb, Slack, Dropbox.

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
Backed by: OpenSSF, Palantir, Kubernetes. People cited: McIntosh et al..

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
Backed by: The Pragmatic Engineer, Google, Spotify, Uber, Cabify, Stripe. People cited: Sébastien Portebois.

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
Backed by: Palantir, Google, Meta, Carnegie Mellon SEI, Linux kernel, NVIDIA, Microsoft, GitLab, Uber, Statsig, JetBrains, Lockheed Martin. People cited: Henrik Warne, tef (programmingisterrible).

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
Backed by: OWASP, OpenSSF, CISA, NIST, GitHub, Cabify.

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
Backed by: OWASP, OpenSSF, Google, Python Software Foundation, npm.

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
Backed by: GitHub, GitLab, Rust project.

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

## code-flaky-test-quarantine

severity: should-fix  
concerns: testing, process  
applies_when: Auditing how the codebase handles tests that pass and fail on the same code.  
Backed by: Dropbox, Shopify, Cabify, Atlassian, GitLab, Airtable.

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
Backed by: Google, Size Limit project, Grafana Labs, Gatling, Microsoft, AWS, Mozilla.

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
Backed by: Kubernetes, GitHub, GitLab, OpenJS Foundation, Envoy, Google.

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
Backed by: Cursor, Spotify, Stripe, Cabify.

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
Backed by: Cursor, Google, Django Software Foundation, Python Software Foundation.

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
Backed by: GitHub, OWASP, CISA, GitLab.

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

## code-vuln-remediation-window

severity: should-fix  
concerns: security, process  
applies_when: The repo has open dependency alerts, update pull requests, or scan reports; with none open, mark it N/A.  
Backed by: OpenSSF, CISA, GitHub, OWASP.

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
Backed by: OpenSSF, OWASP, GitHub, StepSecurity.

**Rule.** Pin every CI action to a full commit SHA.

**Why.** The pipeline holds secrets and publish rights, so a compromised action or injected input owns the artifact. Also give workflows least-privilege tokens, keep untrusted event data out of `run:` and out of `pull_request_target` checkouts, and attach build provenance to releases. [code-dependency-pinning](codebase.md#code-dependency-pinning) covers dependency pins, and [code-dependency-licence-sbom](codebase.md#code-dependency-licence-sbom) covers the inventory.

**FAIL**

```yaml
steps:
  - uses: actions/checkout@v4        # tag, can be moved to other code
  - uses: some/action@main           # branch, changes on every push
```

**PASS**

```yaml
permissions:
  contents: read
steps:
  - uses: actions/checkout@<40-char-sha>   # v4.2.2
  - uses: some/action@<40-char-sha>        # v3.1.0
```

**Counterpoint.** "SHA pinning blocks automatic fixes and adds update churn." Let an update bot propose SHA bumps, so fixes still arrive as reviewed changes. Where the platform offers a lockfile for workflow dependencies, that lockfile is stronger than SHA pins and meets this check.

## py-ruff-gate

severity: should-fix  
concerns: maintainability  
applies_when: The project is Python and has a linter configuration.  
Backed by: no organisation yet. People cited: Pablo González.

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

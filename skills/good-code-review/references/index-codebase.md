# Codebase audit index

One line per stable codebase card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `codebase.md`: read them with offset `<first>` and limit `<count>`.

- `code-a11y-check-in-ci` [should-fix] {accessibility, testing} <ui> L3+30: Run an automated accessibility check, such as axe on rendered pages, in the automated tests, and fail the test on a violation.
- `code-adr` [discuss] {maintainability, process} L34+24: Keep a short written record for each significant design choice (datastore, framework, deviation from a pattern) that states the context, the decision, and its consequences.
- `code-build-hermetic` [should-fix] {process} L59+30: Build from declared inputs only, so that the same source revision gives the same artifact.
- `code-ci-gates` [should-fix] {process} L90+25: Require review and passing build, tests, lint, and type checks on the default branch before merge, and leave nothing mechanical to reviewer vigilance.
- `code-consistency-drift` [discuss] {correctness, maintainability} L116+27: For each recurring concern (errors, config, HTTP clients, logging), make one pattern the standard instead of leaving several as equal peers.
- `code-dead-code` [should-fix] {maintainability} L144+28: Delete unreferenced functions and variables, and the branches of expired feature flags.
- `code-dependency-licence-sbom` [should-fix] {security} L173+26: Generate an SBOM, and scan dependencies for known vulnerabilities on every change or on a schedule. Each ask is judged separately: name which one failed on the FAIL line.
- `code-dependency-pinning` [block] {security} L200+42: Commit a lockfile with hashes and install from it in CI.
- `code-docs-refs-resolve` [should-fix] {maintainability} L243+31: Run a link check in CI over the docs, so that every relative link and anchor they cite resolves.
- `code-file-lines-ceiling` [discuss] {maintainability, process} L275+27: Set a file-length limit in the linter (Pylint and SonarSource default to 1,000 lines), keep hand-written files under it unless a listed exception says otherwise, and split larger files by knowledge owned, not by execution order.
- `code-flaky-test-quarantine` [should-fix] {testing, process} L303+29: Report every test that passes only on retry, move it to a quarantine with a named owner and a ticket, and return it to the merge gate only after it passes many reruns.
- `code-perf-budget-in-ci` [should-fix] {performance, process} L333+27: Write the performance budget down as a CI check that fails the build when it is exceeded.
- `code-release-gated-on-ci` [should-fix] {reliability, process} L361+47: Make a release or publish job depend on the checks passing for the tagged commit, never on the tag alone.
- `code-rule-has-enforcer` [should-fix] {maintainability} L409+33: Back each written repo rule that a type, lint or CI check could enforce with that check, not with a line in an instruction file or a repeated review comment.
- `code-scoped-validation-loop` [discuss] {testing, process} L443+26: Document a command that checks one package or path, with readable output, so a small change does not need the full-repo run.
- `code-secret-scan` [block] {security, process} L470+26: Scan for committed credentials, and treat any hit as leaked: revoke and replace it first. With no scanner present and no secret found, the FAIL is the missing control; evidence is "absent in <paths>". A platform scanner (GitHub secret scanning with push protection, GitLab secret detection) counts when it is enabled on the repo and covers history.
- `code-test-fixtures-built-once` [should-fix] {testing, performance} L497+32: Build an expensive fixture once per test run, and reset state between tests with a rollback or a truncate, never a rebuild.
- `code-test-selection-on-pr` [discuss] {testing, performance, process} L530+49: When the full suite is slower than the pull-request feedback target, run only the tests the change affects on the pull request, and run the full suite before deploy or on a schedule.
- `code-vuln-remediation-window` [should-fix] {security, process} L580+27: Write down how long a known-vulnerable dependency may stay unfixed and fix or upgrade it inside that window.
- `code-workflow-supply-chain` [block] {security, process} L608+49: Pin every CI action to a full commit SHA, and keep code from an unreviewed change out of any job that holds secrets or can deploy.
- `code-workload-identity` [should-fix] {security} L658+43: Exchange the platform's OIDC token for a short-lived cloud credential, and pin the trust policy to the workload.
- `py-ruff-gate` [should-fix] {maintainability} L702+32: Enable the Ruff rule sets E, F, I, B, UP, SIM, BLE, TID and D in CI.

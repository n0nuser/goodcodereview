# Coverage: change and codebase cards

Source item -> card id. "gap" marks items with no usable source in `docs/research/`.

| Source item | Card |
|---|---|
| Consistency with codebase unless pattern is bad; improve what you touch | chg-match-codebase-pattern |
| Reuse: search for an existing helper first | chg-reuse-before-write |
| Move logic to shared module with 2+ call sites; wrong-abstraction | chg-abstraction-needs-two-callers |
| Scope: one concern per change | chg-one-concern |
| Size spread, SmartBear/Cisco single vendor study | chg-size-ceiling |
| Refactors separate; moves not edited | chg-refactor-separate |
| Tests ship with the change | chg-tests-ship-with-change |
| New API ships with a usage | chg-new-api-has-usage |
| Spec match, no unrequested changes | chg-matches-spec |
| Author hygiene: description, self-review, CI green | chg-author-hygiene |
| Expand/contract (gap: recipe unsourced) | chg-expand-contract |
| Breaking-change taxonomy (Hyrum's law) | chg-breaking-change-taxonomy |
| Rollback path (thin source) | chg-rollback-path |
| Flag owner and retirement (thin source) | chg-flag-owner-retirement |
| New attack surface named (thin source) | chg-name-attack-surface |
| Severity labels, one comment per finding | chg-review-comment-format |
| What not to flag; few high-conviction comments | chg-review-signal |
| Verify before claim | chg-verify-before-claim |
| No silenced diagnostics | chg-no-silenced-diagnostics |
| Chesterton's fence | chg-chestertons-fence |
| Agent code: hallucinated APIs, re-implemented helpers | chg-agent-grounded-code |
| Agent code: mock-asserting tests | chg-agent-mock-asserting-tests |
| Agent code: same-session self-review | chg-agent-independent-review |
| File-size ceiling 1k lines (gap: heuristic) | code-file-lines-ceiling |
| Dead code | code-dead-code |
| Dependency pinning | code-dependency-pinning |
| Licences, SBOM (licence part is a gap) | code-dependency-licence-sbom |
| CI gates | code-ci-gates |
| ADRs (gap: format unsourced) | code-adr |
| Consistency drift | code-consistency-drift |
| Supply chain: workflows, provenance | code-workflow-supply-chain |

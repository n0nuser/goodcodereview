# Source sweep: review items applied

Applied from `review-opus.md`: all 12 Act on items and all 21 Consider items. Noted and Dismissed were skipped.

## Act on

1. mod-yagni: Rule and Counterpoint no longer name a second use; note says Shopify and Microsoft ask for three or several uses.
2. code-secret-scan: removed the "source code and build artifacts" sentence and the two sources added for it. code-secrets-not-plaintext-in-repo owns keep-out, now "source code and config".
3. prod-shadow-compare-before-cutover: removed the traffic-in-steps Rule sentence; Why now links prod-canary-staged-rollout and prod-kill-switch-fallback.
4. sys-n-plus-one-pooling: Rule back to one query or batch; the lazy-load guard moved to the Why ("where the ORM offers it ... in tests").
5. fn-no-eval-untrusted: "avoid run-time code generation" moved from the Rule to the Why.
6. sys-load-shedding-bounded-queues: added the Uber load-management URL to `borrowed_from`; note lists per-clause orgs.
7. svc-api-deprecation-sunset: PASS now `Deprecation: @1798761600` (2027-01-01) and `Sunset: Sat, 01 Jan 2028 00:00:00 GMT`. The review gave "Fri", but 2028-01-01 is a Saturday, so the weekday is corrected.
8. chg-approval-tied-to-patch: Counterpoint no longer names GitLab or Prow; the names moved to `note`.
9. sys-cache-hit-rate-watched: FAIL uses `Redis(host="cache")` with maxmemory set in redis.conf.
10. code-gate-new-violations-only: FAIL is now `freeze.refreeze=true` with the refreeze caption.
11. fn-no-aria-hidden-on-focusable: Rule limited to `aria-hidden="true"` on a focusable element or an element left visually hidden while focused; `role="presentation"` moved to the Why; applies_when and the FAIL (a skip link with no :focus rule) and PASS (skip link with :focus) match.
12. svc-bound-inbound-concurrency: added `import asyncio` to both snippets.

## Consider

1. fn-tls-verify-on: Rule says to check against the host you meant to reach, not a name the server supplies; FAIL gains `server_hostname=peer_cert_cn`.
2. svc-update-rollback-on-failure: PASS keeps `.old` until the new binary starts and passes a self-check; Why and Counterpoint say so.
3. svc-saga-steps: no third org for "every forward step"; Rule back to the original, the wider claim sits in the Why.
4. svc-api-naming-consistent: plural example added to FAIL and PASS and a plural sentence to the Why; Counterpoint no longer names Zalando or Microsoft. Not split into two cards.
5. fn-dialog-focus-managed: Rule adds "or, if it is gone, to the next logical control"; Counterpoint notes native dialog restores focus.
6. code-dependency-licence-sbom: Rule and PASS say "raise an alert", without an owner, so the sibling's boundary sentence still holds.
7. code-dead-code: FAIL gains commented-out and unreachable code lines; PASS updated.
8. fn-related-controls-in-fieldset: Why bounds "related" as controls that answer one question together.
9. sys-load-shedding-bounded-queues: clause scoped to requests whose caller has already given up.
10. svc-token-revocation: Rule and PASS say which: this session's refresh token at logout, all of the user's on disable; PASS also mentions issued access tokens where supported.
11. py-imports: Counterpoint states relative and function-level imports are tolerated elsewhere and why this pack chooses otherwise, with no org names.
12. svc-api-deprecation-sunset: added the `rel="sunset"` Link header to the PASS.
13. Draft overlaps: no edit. Each is a promotion-time task: cut the matching Why sentence from the stable card and link the new one (py-test-hygiene, svc-security-headers, sys-cache-bounds-invalidation, code-workflow-supply-chain).
14. svc-path-normalise-before-authz: PASS uses the HTTP connection manager fields; FAIL labelled pseudo-config.
15. svc-rate-limit-by-cost: removed the GitHub "5 points" and Shopify "caps one query at 1,000" claims.
16. mod-no-repeated-switches: removed the Python FAQ claim and its source URL.
17. chg-agent-independent-review: "most review tools can bar it".
18. prod-alerts-symptoms-golden-signals: split the run-on Why sentence.
19. fn-nesting-depth-cap and fn-password-min-length: `lacks:` lines point at Rule clauses.
20. fn-flags-type-for-flag-sets: "language's or ecosystem's flags type", `bitflags` crate.
21. code-tests-order-independent: Rule reworded to "Make each test pass in any order, sharing no mutable state with other tests."

## Side effect

`lint/src/goodcodereview_lint/data/cards.json` was regenerated with `lint/scripts/snapshot.py`, because test_lint compares it to the built cards.

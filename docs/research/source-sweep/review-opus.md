# Source sweep: independent review (Opus)

Scope: `git diff -- cards packs` (108 files, 16 Rule edits) and the 34 untracked draft cards under `cards/` and `packs/`. Bar: `docs/PROMOTION.md`. Org counts come from `tools/orgs.py` run over each card's `borrowed_from`. Evidence is cited by cache hash and by row index in the sweep's rules file, never by quote dump. `python3 tools/validate.py` exits 0 on the working tree.

Verdict tiers: **Act on** (breaks a PROMOTION rule or ships a wrong example; concrete fix given), **Consider** (judgement call or weak spot), **Noted** (true but no action needed now), **Dismissed** (flagged issue that does not hold).

## Act on

1. **mod-yagni** (stable). The Rule clause "or a second use" has no organisation behind it, and two cited orgs contradict it. Shopify says to wait for three instances (row 212, `120575ec01`). Microsoft wants several implementations and consumers (row 1252, `c51a25fad1`). The card's `note` says "Shopify backs the second-use clause", which is false. The "need" clause has Google (row 189), Microsoft (rows 1257, 2511) and Wikimedia (row 1343). Fix: change the Rule to "...add it when the need appears.", change "the real second caller" in the Counterpoint to "the real caller", and rewrite the note to say that Shopify and Microsoft ask for three or several uses, so no use count sits in the Rule.

2. **code-secret-scan** (stable, block) and **code-secrets-not-plaintext-in-repo** (new draft). These two cards duplicate each other (rule 8). The new Rule sentence "Keep secrets out of source code and build artifacts" is the draft's Rule. The stable card's `applies_when` covers the repository and its history, not build artifacts, and "build artifacts" has one org (OWASP ASVS, row 1927, `15bc08ae29`). For "source code", CISA (`41310def9e`), AWS (`91a2ec6af8`, rows 1599 and 2533) and OWASP back it. The GitHub pages that say it (rows 683, 1645) are not cited. Fix: revert the new first sentence of the Rule and keep code-secret-scan about detection and response. Let the draft own keep-out, with "source code and config" only. Otherwise, mark the draft `lacks: duplicate`. Do not keep both.

3. **prod-shadow-compare-before-cutover** (stable). The new Rule sentence "Move traffic in steps, and keep a switch that sends it all back to the old system" repeats stable `prod-canary-staged-rollout` ("Roll out in stages…") and stable `prod-kill-switch-fallback` ("switchable off without a deploy"). That breaks rule 8. Its orgs (Amex, GitHub, Shopify, Stripe) are fine, but the clause belongs to those cards. Fix: revert the Rule sentence, keep the new PASS comment, and add one Why line: "Then shift traffic in steps with a way back; see [[prod-canary-staged-rollout]] and [[prod-kill-switch-fallback]]."

4. **sys-n-plus-one-pooling** (stable). The new clause "make an unplanned lazy load raise outside production" has two problems. (a) The PASS is Django, which has no built-in lazy-load guard, so the PASS does not meet the edited Rule (rule 5). (b) "Outside production" comes from Laravel only (`Model::preventLazyLoading(! isProduction())`, `5ae6878a87`). Rails (`2a92a0df3d`) and SQLAlchemy (`a64d658cee`) describe raise-on-lazy-load as an option, with no environment scope. The Why already explains the guard. Fix: move the clause back to the Why ("Where the ORM offers it, make an unplanned lazy load raise in tests"), and leave the Rule as it was.

5. **fn-no-eval-untrusted** (stable, block). The known issue is confirmed. The new sentence "Avoid run-time code generation altogether where a parser or a lookup does the job" has four problems. (a) It applies to trusted text, which `applies_when` excludes ("some of the text comes from a request…"). (b) It is a hedge ("where… does the job"), so a reviewer cannot mark it FAIL cleanly. (c) No FAIL or PASS exercises it. (d) It runs at block severity. The orgs are real: OWASP ASVS (row 884), MITRE CWE-94 (row 2486) and Mozilla (row 663). Fix: move the sentence to the Why ("Better still, avoid run-time code generation where a parser or a lookup does the job"), and leave `applies_when` and severity unchanged.

6. **sys-load-shedding-bounded-queues** (stable, block). The new clause "drop queued requests that have waited too long" cites two orgs: AWS (row 2062, `378c83ac32`) and the Google SRE book (CoDel and LIFO passage, `fe1c3ecadc`). The third org named in the edit log, Uber (`f4891c5ec4`, "shedding stale work" under CoDel), is not in `borrowed_from`. Netflix (`3e776df05b`) says nothing about queue age. Fix: add the Uber load-management URL to `borrowed_from`, and update the note with the per-clause orgs.

7. **svc-api-deprecation-sunset** (stable). The PASS example contradicts its own Why. The Why now says to keep deprecated behaviour "for one to two years", but the PASS puts `Sunset` six months after `Deprecation` (`@1767225600` is 2026-01-01, and Sunset is 2026-07-01). The Sunset date is also in the past (today is 2026-11-18), and RFC 8594 section 3 says Sunset SHOULD be in the future. Fix: set the PASS `Deprecation` to `@1798761600` (2027-01-01) and `Sunset` to `Fri, 01 Jan 2028 00:00:00 GMT`.

8. **chg-approval-tied-to-patch** (draft). The new Counterpoint sentence "GitLab and Prow drop approvals on any new commit by default" names organisations in a Counterpoint (rule 7). Fix: reword it as "Many review tools drop approvals on any new commit by default, so the exemptions above are the tuned case, not the baseline", and move the GitLab and Prow names into `note`.

9. **sys-cache-hit-rate-watched** (new draft). The FAIL example `Redis(maxmemory="2gb")` is not a redis-py constructor argument, and it raises `TypeError` (rule 5). Fix: use `cache = Redis(host="cache")  # maxmemory 2gb set in redis.conf; no hit-rate metric, no memory alert`.

10. **code-gate-new-violations-only** (new draft). The FAIL caption is wrong about ArchUnit. The ArchUnit guide (`5723e3b106`) says `allowStoreUpdate` defaults to true and lets the store change, and that `freeze.refreeze=true` is the setting that adds current violations. With `allowStoreUpdate=true` alone, a new violation still fails the build, so the FAIL does not fail. Fix: make the FAIL `freeze.refreeze=true` with the caption "CI refreezes on each run, so a new violation is absorbed and the build stays green". Keep the PASS.

11. **fn-no-aria-hidden-on-focusable** (new draft). The Rule bans "CSS hiding on an element that can take focus", which breaks two ways. (a) It condemns the standard visually-hidden skip link that shows on focus. (b) It contradicts the card's own PASS, `<nav hidden>`, which is CSS-equivalent hiding of a focusable link. WebAIM's line is narrower: do not hide *focused* elements (row 936, `01c9d0a19a`). Separately, ARIA tells browsers to ignore `role="presentation"` on a focusable element, so the FAIL's `<button role="presentation">` is still announced as a button. Google (row 933) still says not to add it, so keep it as a lint-level point. Fix: change the Rule to "Never put `aria-hidden="true"` on an element that can take focus, or leave an element visually hidden while it has focus." Move `role="presentation"` to the Why as a conflict that axe flags.

12. **svc-bound-inbound-concurrency** (new draft). The FAIL and PASS both call `asyncio.timeout` and `asyncio.Semaphore` but import only `aiohttp.web`, so neither snippet runs (rule 5). Fix: add `import asyncio` to both.

## Consider

1. **fn-tls-verify-on** (stable, block). The new clause "give the client the hostname it expects" has three orgs: Google (rows 846, 2277), PSF (row 2263) and IETF RFC 9525 (row 983). It stays inside verification (see Dismissed). Its remaining problems: (a) The wording is vague, and it reads as "pass a hostname" when the failure is a name taken from the server. (b) No FAIL or PASS exercises it. (c) Go (`tls.Client` with no `ServerName`) and Python (`check_hostname` with no `server_hostname`) already refuse a missing name, so the realistic FAIL is a name derived from the peer, a redirect or a certificate. Either reword it as "and check the certificate against the host you meant to reach, not a name the server supplies" and add a FAIL line such as `ctx.wrap_socket(sock, server_hostname=peer_cert_cn)`, or move the clause to the Why, which already says it.

2. **svc-update-rollback-on-failure** (stable). The known issue is confirmed in part. The PASS handles a failed swap correctly, so it meets the Rule as written. It cannot roll back a new binary that fails to start, because it deletes `.old` right after the rename. Microsoft, Mender and Google (the partial-edit log) back keeping the old version until the new one is confirmed. Move `os.Remove(old)` to the next successful start ("delete `.old` once the new binary has started and passed its self-check"). Then add a Why sentence. Making it a Rule clause would also work, since it has three orgs.

3. **svc-saga-steps** (stable). The Rule widened from "idempotent after the pivot" to "every saga step… idempotent". AWS states it for all participants (`c5907730fd`). Microsoft states idempotence generally (`4439278667`). Temporal states it for compensations only (`687e5e7268`), not for forward steps. That is a thin third org for the widened clause. Before promotion, look for a third org that says every forward step is idempotent.

4. **svc-api-naming-consistent** (stable). The new Rule sentence on plural nouns is well sourced (Zalando, Google AIP, Microsoft, Kubernetes, Ísland.is). No FAIL or PASS shows a plural, and the Why still talks only about casing. Add `"item": [...]` → `"items": [...]` to the examples. Also check whether "naming" now covers two rules that would read better as two cards. The Counterpoint names Zalando and Microsoft (rule 7), which is pre-existing; reword it as "Published guides disagree…".

5. **fn-dialog-focus-managed** (stable, block). The Rule clause "return focus to the control that opened it" is absolute, but W3C APG says "unless that element no longer exists" (row 987), and WebAIM says "should usually". Add "or, if it is gone, to the next logical control". The Counterpoint could also note that a native `<dialog>` restores focus on close in current browsers, which makes the PASS `onclose` handler belt and braces.

6. **code-dependency-licence-sbom** (stable). The orgs for the "alert an owner" clause hold up: NIST (row 479, `f93dc4f622`), OWASP (`c24b7ffb81`), OpenSSF (`5fb463f6b6`) and Cabify (`88626010af`). Only Cabify names an *owner*, though. The sibling card `code-vuln-remediation-window` says "[[code-dependency-licence-sbom]] covers running the scan, and this card covers acting on the result". The alert clause now sits on that boundary. Either say "alert" without "an owner", or update the sibling's boundary sentence.

7. **code-dead-code** (stable). The Rule edit is well sourced: unreachable code from CMU SEI, Lockheed and NVIDIA; commented-out code from Lockheed, JetBrains and TUM; flag config from Microsoft, GitLab and Uber. The FAIL and PASS still show only an unused function and a flag branch. Add a FAIL line for commented-out code so every clause has an example a reviewer can match.

8. **fn-related-controls-in-fieldset** (stable). The widening to "other set of related controls" is backed by USWDS (`6b863ca000`), W3C (`eba271d842`) and GOV.UK (`6ed4d9ce41`). "Related" is now open-ended (a sign-in form's two fields?), which weakens the FAIL line a reviewer can draw. Give one bound in the Why, such as "controls that answer one question".

9. **sys-load-shedding-bounded-queues**. Besides the citation (Act on 6), the new clause says "drop", while the PASS and Counterpoint still say "spillover queue for old deltas" and "spill to durable storage". Scope the clause to requests whose caller has given up, as the PASS line does ("past the caller's timeout"). Leave messages to the spillover path.

10. **svc-token-revocation** (stable). The Rule is fine. The Cognito versus Auth0 and RFC 7009 conflict touches only the PASS phrase "(and its grant)". Use the Why's own wording: "mark the refresh token revoked, and where the server supports it, the access tokens issued from it". The phrase "the user's refresh tokens" at logout could mean this session or all sessions. Say which.

11. **py-imports** (stable, creator source). The status is unaffected, because the card cites the creator's guide (ADR 0001). The PSF programming FAQ suggests a function-level import as one way to break a cycle, against the Counterpoint's "it hides the cycle". PEP 8 also accepts explicit relative imports, against "absolute only". Add a clause to the Counterpoint, such as "PEP 8 tolerates explicit relative imports; this pack does not, because…", so the house rule reads as a deliberate choice.

12. **svc-api-deprecation-sunset**. Add `Link: <…>; rel="sunset"` to the PASS. RFC 8594 section 7.2 defines it, and the pilot flagged it.

13. **Draft overlaps with Why text this diff added to stable cards.** Each draft is a fair candidate, but each now repeats a sentence the same diff put in a stable Why:
    - `code-tests-order-independent` repeats the new `py-test-hygiene` Why sentence ("none depends on another's result or order").
    - `svc-tls-all-traffic` repeats the new `svc-security-headers` Why sentence ("Serve no plain-HTTP endpoint for an API"). `svc-security-headers` is itself a draft.
    - `sys-cache-hit-rate-watched` repeats `sys-cache-bounds-invalidation`'s Why ("hit, miss, and origin-request metrics").
    - `code-workflow-token-per-job-write` shares the `permissions: write-all` FAIL and the "least-privilege tokens" Why with stable `code-workflow-supply-chain`.

    When a draft is promoted, cut the matching Why sentence from the stable card and link the new card.

14. **svc-path-normalise-before-authz** (draft). The PASS uses the `envoy.extensions.http.header_validators.envoy_default.v3` UHV extension. The long-standing production options are the HTTP connection manager fields `normalize_path`, `merge_slashes` and `path_with_escaped_slashes_action: REJECT_REQUEST`, which the cited Envoy page (`9dd74c145b`) documents. Use those. The FAIL is pseudo-config and should say so.

15. **svc-rate-limit-by-cost** (draft). Two Why figures could not be found in the cached pages. (a) "GitHub scores a mutation at 5 points against 1 for a read": no match in `bbf4ffdbec`. (b) "Shopify caps one query at 1,000 points": `34c135e224` gives 1,000 as the bucket size, not a per-query cap. The live pages may hold them. Re-check before promotion, or change (b) to "a bucket of 1,000 points".

16. **mod-no-repeated-switches** (stable). The note now says that "the Cursor pstack model-the-domain skill and the Python FAQ back the one-lookup-table alternative". Cursor (`d630dfd68f`) does ("a map, registry… instead of branching"). The cached Python FAQ page (`7ae056bc4b`) has no switch/case entry. The dict-dispatch answer sits in the Design FAQ, which may not be the cited URL. Verify the URL.

17. **chg-agent-independent-review** (draft). The new Why claim "review tools bar [self-approval] by default" holds for GitHub. GitLab's "prevent approval by author" is a project setting. Soften it to "most review tools can bar it".

18. **prod-alerts-symptoms-golden-signals** (stable). The new clause turned the last Why sentence into a broken list: "…and saturation, and page on saturation when a limit is about to be reached, not only after it is hit, track latency…". Split it into two sentences.

19. **Draft `lacks:` lines that cite non-Rule clauses.** `fn-nesting-depth-cap` blames "the numeric limit", but the number sits in the Why, and the Rule says "the project's depth limit". `fn-password-min-length` blames "the max-length clause", which sits in the Counterpoint. Point each `lacks:` note at the Rule clause.

20. **fn-flags-type-for-flag-sets** (draft). "The language's flags type (… `bitflags` in Rust)" is wrong: `bitflags` is a crate, not a language feature. Say "the language's or ecosystem's flags type".

21. **code-tests-order-independent** (draft). The Rule is not imperative ("Tests give the same result…"), which the template asks for. "Between suites" does not match the FAIL, which shares state between two tests in one module. Fix it as "Make each test pass in any order, sharing no mutable state with other tests."

## Noted

1. **All 16 Rule edits match the partial-edit logs.** They are code-adr, code-dead-code, code-dependency-licence-sbom, code-secret-scan, fn-dialog-focus-managed, fn-jwt-verify-pinned, fn-no-eval-untrusted, fn-related-controls-in-fieldset, fn-tls-verify-on, mod-colour-tokens-meet-contrast, prod-shadow-compare-before-cutover, svc-api-naming-consistent, svc-saga-steps, sys-load-shedding-bounded-queues, sys-n-plus-one-pooling and chg-no-per-user-ide-files. Each Rule is still one paragraph. code-secret-scan was already four sentences before the edit.

2. **Rule edits that pass without comment:**
    - code-adr: options ruled out has Google, Oxide, Kubernetes and Rust.
    - fn-jwt-verify-pinned: `exp` has Google (row 1080), the cited OWASP JWT cheat sheet (`db98e24e44`) and the cited Microsoft access-token page (`c6b32044c7`). The clearest OWASP line (row 1489) is on an uncited REST page; consider citing it.
    - mod-colour-tokens-meet-contrast: the WCAG large-text definition comes from W3C, Deque and WebAIM.
    - chg-no-per-user-ide-files: `git rm --cached` has Git (`5df1328ba2`), GitHub (`b14fb79e5a`) and Microsoft (`523a83a26c`). Its second sentence reads like Why material, but it can be failed: the diff adds an ignore entry while the file stays tracked.

3. **New drafts meet the structural bar.** All 34 are `status: draft`. None is above `should-fix` (6 are `discuss`), and each has a well-formed `lacks:` line. Twelve list three or more organisations: code-secrets-not-plaintext-in-repo, code-signed-commits-protected, code-workflow-token-per-job-write, fn-complexity-cap, fn-early-return-no-else, fn-nesting-depth-cap, fn-password-min-length, svc-api-version-on-every-request, svc-bound-inbound-concurrency, svc-client-paces-outgoing-calls, svc-tls-all-traffic and sys-cache-hit-rate-watched. The `lacks:` reason is honest on the rest.

4. **No sourcing chatter in draft Rules, examples or Counterpoints.** The only org name is "NIST asks for 15 characters" in the fn-password-min-length Why, which rule 7 allows. Pre-existing chatter in stable Counterpoints (code-test-selection-on-pr's Shopify and Microsoft, svc-api-naming-consistent's Zalando and Microsoft) was extended or left as it was by this diff. Clean it up in a separate pass.

5. **Draft examples checked and correct:** svc-paginate-by-server-links (`requests` `r.links`), sys-hedge-budget (gRPC `hedgingPolicy` and `retryThrottling` fields), sys-shuffle-shard (`random.Random(bytes)` is deterministic), svc-server-read-timeouts, svc-tenant-scope-in-data-layer, fn-flags-type-for-flag-sets (prints `3` versus `Read, Write`), fn-complexity-cap and fn-nesting-depth-cap tool defaults (PMD 10 and 3, CA1502 25, Pylint 5), py-raises-specific-exception (ruff and bugbear B017), and go-return-error-not-panic.

6. **Draft link targets.** fn-nesting-depth-cap links the draft fn-early-return-no-else, and svc-logs-tamper-resistant links the draft svc-security-event-logging. Rule 9 binds only stable cards, so this is fine while both stay drafts.

7. **Out of scope:** `tools/config.py` raises `PAGE_MAX` from 105,000 to 130,000. That is not a card change, so it should be its own commit with a reason.

8. **Brief versus disk:**
    - The checkout is on `main`, not `source-sweep-cards`.
    - There are 34 untracked draft cards, not 33.
    - `new-cards/cpp-no-c-style-cast.md` has no card on disk, since there is no C++ pack.
    - `docs/research/source-sweep/` holds no `rules.json` or `clusters-*.md`. The rules file lives only in the private sweep folder.

9. **Quote spot-check (rule 3 evidence).** 30 checks, made with exact-string search in the cache:
    - 24 sweep quotes, all found: rows 212, 479, 477, 663, 746, 791, 846, 874, 884, 933, 936, 983, 987, 1080, 1192, 1231, 1252, 1454, 1489, 1581, 2062, 2466, 2486 and 2563.
    - Six reader-text claims:
      - eslint-plugin-import "usually indicates the module is doing too much" (`3ebc23276d`): found.
      - Microsoft "difficult to maintain" (`bb53236178`): found.
      - Shopify "about 0.06 percent" (`1884cec5be`): paraphrase. The page gives 0.06% of PRs merged with failing tests; the "stale mapping" cause is the card's reading.
      - Dropbox "100 or more times" (`d3184227c7`): found.
      - GitHub "mutation 5 points": not found.
      - Python FAQ lookup-table claim: not found (see Consider 15 and 16).

    The 24 sweep quotes were extracted from those same pages, so finding them proves the cache is faithful, not that each quote supports its card. The per-card support checks are above.

## Dismissed

1. **fn-tls-verify-on: the Rule goes beyond verification.** Dismissed. RFC 9525 makes the client's own reference identity an input to hostname verification (row 983), and Go and Python tie the check to the name the caller supplies. The clause stays inside verification. Its wording and examples are a separate point (Consider 1).

2. **svc-api-deprecation-sunset versus RFC 8594 section 1.4.** Dismissed. Section 1.4 says Sunset marks the end of a resource's life, not the "no longer preferred" stage, so Sunset alone must not stand in for deprecation. RFC 9745 (`706e91bda9`), which the card cites, says to send `Sunset` alongside `Deprecation` on a resource that still responds, to say when it will become unresponsive. It also says Sunset must not be earlier than Deprecation. The card does exactly that. The source pilot read section 1.4 as forbidding Sunset on live routes, and that reading is wrong. The real defects are the PASS dates (Act on 7) and the missing `rel="sunset"` (Consider 12).

3. **go-wrap-errors-with-w: NVIDIA bans `fmt.Errorf`.** Dismissed. It is one project's convention in favour of its own error package, not a practice that contradicts wrapping with `%w`. The card is a draft with `lacks: orgs`, and that stays true.

4. **svc-token-revocation: Cognito versus Auth0 and RFC 7009 as a Rule conflict.** Dismissed for the Rule. The Rule asks to revoke refresh tokens at logout and on disable, and all three agree. The disagreement is only about how far one revocation reaches, and that lives in the PASS (Consider 10).

5. **svc-update-rollback-on-failure: the PASS is wrong.** Dismissed as stated. The PASS rolls back a failed swap and meets the Rule as written. The gap is a stronger practice the Rule does not yet ask for (Consider 2).

# New cards pass 1: five leads from the company sweeps

Fetched 2026-10-25 with `curl -sL` and a browser User-Agent, tags stripped. Netflix post pages return a Cloudflare challenge to curl, so Netflix posts were read through the blog's RSS feed (https://netflixtechblog.com/feed), which carries full post bodies. Each Netflix URL below matches an `<item>` link in that feed. Years come from the fetched page; "n.d." means the page text shows no date. Paraphrase only. Quotes are at most 15 words.

## `prod-shadow-compare-before-cutover`

1. https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb. Netflix, 2026. The team ran the old and new ad-event pipelines in parallel and diffed their output on live traffic before cutting over. That was slower than a flag-day switch. Quote: "Running both systems in parallel and diffing their output on live traffic". Backs the Rule and the Counterpoint.
2. https://stripe.dev/blog/how-stripes-document-databases-supported-99.999-uptime-with-zero-downtime-data-migrations. Stripe, 2024. After replication syncs, a correctness check compares point-in-time snapshots of source and target shards, then the traffic switch follows. Quote: "comparing point-in-time snapshots". Backs the Rule and the Counterpoint (snapshots for writes). The sweep's URL (`99999` in the slug) returns 404; this slug works.
3. https://airbnb.tech/infrastructure/beyond-synthetic-testing-capturing-and-replaying-real-database-workloads-at-airbnb/. Airbnb, n.d. Captured production queries run against two databases at once and the results are compared. For the MySQL 8.0 upgrade this found queries with undetermined row order and duplicate cacheable queries. Quote: "their results are compared with any discrepancies logged". Backs the Rule and the Why.
4. https://github.blog/engineering/engineering-principles/how-we-improved-availability-through-iterative-simplification. GitHub, 2024. A Scientist experiment runs a candidate code block beside the control and reports results before the change is made permanent. Quote: "we measure and report results before making the changes permanent". Backs the Rule.

## `svc-best-effort-optional-deps`

5. https://netflixtechblog.com/ontology-driven-observability-building-an-end-to-end-knowledge-graph-at-netflix-scale-421392cf5adf. Netflix, 2026. Calls to metrics, logs, and other external systems are best-effort, so a slow dependency degrades the knowledge graph but does not block it. Quote: "A slow dependency should utmost degrade the graph, never block it." Backs the Rule. Caveat: a pipeline build, not a user request, so the Rule says "critical path".
6. https://www.uber.com/es/en/blog/ubers-rate-limiting-system/. Uber, 2026. When the rate limiter's control plane is unavailable, clients fail open and let traffic through. Quote: "clients failed open, allowing traffic to continue". Backs the Rule and the fail-open sentence in the Counterpoint.
7. https://tech.cabify.com/blog/engineering/degraded-experiences. Cabify, 2025. A non-critical outage leads to a degraded experience, such as skipping some details in a driver offer. Every degradation needs metrics and alerts. Quote: "Degradations should have the same visibility as critical flows." Backs the Rule (count every fallback) and the Why.

## `sys-cells-limit-blast-radius`

8. https://netflixtechblog.com/single-tenant-titus-vm-level-isolation-on-a-multi-tenant-container-platform-6d8b1909d163. Netflix, 2026. Each Titus region is divided into independent cells, which limits how large one control plane can get. Quote: "each region is divided into independent cells". Backs the Rule.
9. https://slack.engineering/slacks-migration-to-a-cellular-architecture/. Slack, 2023. Slack moved its critical user-facing services to a cell-based architecture to add redundancy and limit the blast radius of site failures. Quote: "limit the blast radius of site failures". Backs the Rule.
10. https://airbnb.tech/infrastructure/building-a-fault-tolerant-metrics-storage-system-at-airbnb/. Airbnb, n.d. The metrics store moved to a multi-cluster architecture to set up several failure domains and reduce the blast radius. Quote: "establish multiple failure domains and minimize the blast radius of issues". Backs the Rule. The per-tenant write guardrails in the same post belong to `svc-rate-limit-quota` and are not used.
11. https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/. Cloudflare, 2023. Remediation after the data-centre outage includes testing the blast radius of failures and minimising the services one failure affects. Quote: "Test the blast radius of system failures". Backs the Counterpoint (ask what one failure takes down). Caveat: it states the goal, not cells.

## `code-flaky-test-quarantine`

12. https://dropbox.tech/application/accelerating-iteration-velocity-on-dropboxs-desktop-client-part-1. Dropbox, 2017. Quarantine Keeper removes tests that fail too often from the main pool and files a bug against the test's owner. The post names short timeouts and state left by earlier tests as causes. Quote: "removes tests from the main pool if they fail too often". Backs the Rule (quarantine, owner) and the Why.
13. https://dropbox.tech/machine-learning/introducing-nova-our-internal-platform-for-coding-agents. Dropbox, 2026. A proposed flaky-test fix is validated by running the test 100 or more times in CI. Quote: "running the test 100 or more times in CI". Backs the Rule (many reruns).
14. https://shopify.engineering/unreasonable-effectiveness-test-retries-android-monorepo-case-study. Shopify, 2019. A failed test is retried up to three times, and every test that passes after a retry is reported to developers as a warning. Quote: "we detect all the tests that pass after a retry and notify the developers". Backs the Rule (report passes after retry) and the Counterpoint.
15. https://shopify.engineering/mobile-e2e-testing. Shopify, 2026. Fixed pauses instead of explicit waits for elements piled up into flaky mobile E2E tests. Quote: "The fix was to explicitly wait for elements to appear". Backs the Why (causes).
16. https://tech.cabify.com/blog/engineering/acceptance-testing-go-services-using-aceptadora. Cabify, n.d. Dependencies that kept their state between tests made some tests flaky. Quote: "retained their state between tests". Backs the Why (causes). Not counted for the Rule.

## `svc-rate-limit-by-cost`

17. https://shopify.engineering/rate-limiting-graphql-apis-calculating-query-complexity. Shopify, 2021. Each GraphQL query gets a cost from static analysis before it runs: one point per object, zero for scalars and enums, 50 points per second up to 1,000. Quote: "every GraphQL request has a different cost". Backs the Rule and the Why.
18. https://docs.github.com/en/graphql/overview/rate-limits-and-query-limits-for-the-graphql-api. GitHub, n.d. The GraphQL API assigns points to each query and limits the points used per time window. Quote: "The GraphQL API assigns points to each query". Backs the Rule. Found outside the sweep rows.
19. https://airbnb.tech/infrastructure/from-static-rate-limiting-to-adaptive-traffic-management-in-airbnbs-key-value-store/. Airbnb, n.d. Resource-aware rate control charges operations in request units based on bytes and latency, because a one-row lookup and a 100,000-row scan were treated equally. Quote: "charging operations in request units (RU) rather than raw requests per second". Backs the Rule and the Why.
20. https://www.uber.com/es/en/blog/from-static-rate-limiting-to-intelligent-load-management/. Uber, n.d. Uber tried capacity-unit quotas based on bytes processed and dropped them: the central Redis counter added a hop and a failure point, and the cost model was imprecise. Quote: "this approach didn't hold up in production". Backs the Counterpoint only. It is evidence against the Rule's simplest form.

## Checked, not added

- https://tech.cabify.com/blog/engineering/mysql-upgrade-no-downtime: checks for zero replication lag and connection multiplexing before a swap. A precondition, not a diff of outputs, so it does not back `prod-shadow-compare-before-cutover`.
- Uber's load-management post as support for cost-based limits: it ranks traffic by priority and dropped its cost quota. Used only as the Counterpoint.
- `slack-raw/24.txt` (agentic E2E tests): mentions flaky workflows but no quarantine, owner, or rerun rule.

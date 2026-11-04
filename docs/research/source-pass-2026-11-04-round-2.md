# Source pass, round 2, 2026-11-04

A targeted second search for cards that had one or two supporting organisations after the first pass. Same method as the first pass (see source-pass-2026-11-04.md): each URL fetched and its quote confirmed on the page, then judged against the card's Rule. This note lists the supporting sources added for the cards the pass moved to stable.

| Card | Source | Why it supports the Rule |
|---|---|---|
| `svc-saga-steps` | https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/saga-choreography.html | Prescriptive guidance: saga participants must be idempotent. |
| `svc-saga-steps` | https://docs.temporal.io/design-patterns/saga-pattern | Compensations must be idempotent and handle never-executed forward step. |
| `chg-agent-independent-review` | https://www.anthropic.com/engineering/claude-code-best-practices | States a fresh reviewer helps because it has not seen the author's reasoning. |
| `chg-chestertons-fence` | https://getyourguide.careers/posts/how-we-work-efficiently-with-legacy-code | Write characterization tests before refactoring a subsystem |
| `chg-chestertons-fence` | https://www.redhat.com/en/blog/refactoring-speed-mission-agent-mesh-approach-legacy-system-modernization-red-hat-ai | Characterization tests capture original behaviour before any change; vendor pipeline description. |
| `chg-name-attack-surface` | https://peps.python.org/pep-0012/ | Change proposals must state security implications of the new feature |
| `chg-proto-reserve-removed-fields` | https://learn.microsoft.com/en-us/aspnet/core/grpc/versioning | Says reserve deleted field numbers and names with reserved. |
| `chg-proto-reserve-removed-fields` | https://deliveroo.engineering/2019/02/05/improving-stream-data-quality-with-protobuf-schema-validation.html | Team rule: removed fields must get a reserved entry. |
| `mod-layers-point-inward` | https://learn.microsoft.com/en-us/dotnet/architecture/modern-web-apps-azure/common-web-application-architectures | Clean architecture: dependencies flow toward the core |
| `mod-layers-point-inward` | https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/hexagonal-architecture.html | Hexagonal: domain knows nothing of external dependencies |
| `mod-layers-point-inward` | https://netflixtechblog.com/ready-for-changes-with-hexagonal-architecture-b315ec967749 | Team states all dependencies point inward; logic ignores transport. |
| `mod-no-import-side-effects` | https://airflow.apache.org/docs/apache-airflow/2.10.0/best-practices.html | No DB or network I/O in DAG top-level (import-time) code. |
| `mod-no-import-side-effects` | https://azure.github.io/azure-sdk/typescript_implementation.html | SDK guideline: avoid module side effects. |
| `mod-no-import-side-effects` | https://dagster.io/blog/dignified-python-10-rules-to-improve-your-llm-agents | Company rules list says avoid import-time side effects, with reasons. |
| `mod-no-import-side-effects` | https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/BEST_PRACTICES.md | Project best practices: avoid import-time side effects. |
| `mod-one-name-per-concept` | https://github.com/island-is/handbook/blob/master/docs/api-design-guide/naming-conventions.md | Same name for the same concept across the ecosystem |
| `mod-one-name-per-concept` | https://github.com/tum-esi/common-coding-conventions | University coding conventions: one word per concept |
| `mod-one-name-per-concept` | https://github.com/microsoft/api-guidelines/blob/vNext/azure/ConsiderationsForServiceDesign.md | States the rule: same name for same concept, different for different. |
| `prod-slo-error-budget` | https://sre.google/workbook/error-budget-policy/ | Policy halts releases when error budget is exhausted |
| `prod-slo-error-budget` | https://handbook.gitlab.com/handbook/engineering/infrastructure-platforms/database/ | Team stops introducing change when the budget is used up. |
| `prod-slo-error-budget` | https://www.atlassian.com/blog/atlassian-engineering/unlocking-reliability-with-splunk-smartstore | Team halts engineering work for reliability when budget is exhausted. |
| `svc-api-documented-errors` | https://developer.siemens.com/guidelines/api-guidelines/rest/error.html | Error response codes must be documented |
| `svc-circuit-breaker-bulkhead` | https://aws.amazon.com/builders-library/dependency-isolation | Separate concurrency limit (bulkhead) per dependency |
| `svc-circuit-breaker-bulkhead` | https://netflixtechblog.com/fault-tolerance-in-a-high-volume-distributed-system-91ab4faae74a | Netflix isolates each dependency in its own thread pool. |
| `chg-agent-grounded-code` | https://labs.cloudsecurityalliance.org/research/csa-research-note-ai-codegen-vulnerability-debt-20260406-csa/ | Recommends verifying AI-suggested packages exist in registry; packages only, not signatures. |
| `chg-migration-add-column-rewrite` | https://medium.com/paypal-tech/postgresql-at-scale-database-schema-changes-without-downtime-20d3749ed680 | PayPal team adds column without default as a migration step. |
| `chg-migration-add-column-rewrite` | https://retool.com/blog/running-safe-database-migrations-using-postgres | Retool backfills values in batches after adding the column. |
| `code-scoped-validation-loop` | https://android.googlesource.com/platform/frameworks/support/+/17957fcb324a42599abc868ffe8204a0384b2aee/camera/AGENTS.md | Google documents a per-project test command for contributors |
| `code-scoped-validation-loop` | https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/unit-tests/ | Contributor docs explain running a subset instead of the whole suite. |
| `code-scoped-validation-loop` | https://devguide.python.org/testing/run-write-tests/ | CPython devguide documents running a single test file. |
| `svc-best-effort-optional-deps` | https://engineering.atspotify.com/2013/03/achieving-fault-tolerance-with-intelligent-daemons | Weak dependency returns partial response with fallback values. |
| `svc-best-effort-optional-deps` | https://engineering.zalando.com/posts/2022/04/operation-based-slos.html | Counts degraded successful responses as errors; covers counting clause. |
| `svc-dlq` | https://www.notion.com/blog/building-observability-into-notions-dead-letter-queue | Notion runs a DLQ for exhausted retries; replay not in quote. |
| `svc-dlq` | https://www.uber.com/blog/reliable-reprocessing/ | Uber republishes dead-letter messages for reprocessing; covers replay. |
| `sys-health-liveness-readiness` | https://learn.microsoft.com/en-us/azure/architecture/patterns/health-endpoint-monitoring | Shallow liveness checks so dependency outages do not restart apps. |
| `sys-health-liveness-readiness` | https://docs.gitlab.com/administration/monitoring/health_check/ | Do not load-balance on endpoint that checks shared backends. |

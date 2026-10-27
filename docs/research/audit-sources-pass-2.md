# Sources added to fifteen cards after the per-clause audit

Quotes were copied from the pages at the URLs below on 2026-10-27 and verified against the
rendered page. Pages that restate another organisation, state only part of a clause, or were
not reachable are recorded in each card's `note` rather than counted silently.

## Background tasks are bounded

- AWS Builders' Library, https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/: "A second concurrency guard that can be used is a semaphore that measures and limits the amount of concurrency that can be used for any single workload at any instant in time." and "Across services at Amazon, we use separate thread pools for each workload to avoid one workload from consuming all of the available threads."

## Reflow and zoom

- WebAIM, https://webaim.org/techniques/reflow/: "This means that for content that normally scrolls vertically, there must be no loss of information or functionality, and no horizontal scrolling required, down to a viewport width equivalent to 320 CSS pixels. This ensures that content will reflow when users zoom full-size displays or use small devices." The page quotes the WCAG wording but also gives its own manual test.
- Mozilla (MDN), https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/meta/name/viewport: "Disabling zooming capabilities by setting user-scalable to a value of no prevents people experiencing low vision conditions from being able to read and understand page content." and "Additionally, WCAG requires a minimum of 2× scaling; however, the best practice is to enable a 5× zoom."
- Google (web.dev), https://web.dev/articles/accessible-responsive-design: "You can use the viewport meta tag to prevent zooming, by setting maximum-scale=1 or user-scaleable=no. Avoid doing this, and let your users zoom in if they need to."
- Microsoft (Teams app design guidance), https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/design/design-teams-app-layout-scaling: "Mobile designs must be 320 pixels." This states a design floor, not reflow at 400% zoom.

## Retry policy

- AWS Builders' Library, https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/: "A transient failure is when a request fails for a short period of time. Retries allow clients to survive these random partial failures and short-lived transient failures by sending the same request again." and "In almost all cases, our solution is to limit the number of times that the client retries, and handle the resulting failure earlier in the service-oriented architecture." and "Our solution is jitter. Jitter adds some amount of randomness to the backoff to spread the retries around in time."
- Stripe, https://docs.stripe.com/rate-limits: "Watch for 429 status codes and implement a retry mechanism to handle rate limiting. Follow an exponential backoff schedule to reduce request volume when necessary, and add randomness to the backoff schedule to avoid a thundering herd effect."
- GitHub, https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api: "Otherwise, wait for at least one minute before retrying. If your request continues to fail due to a secondary rate limit, wait for an exponentially increasing amount of time between retries, and throw an error after a specific number of retries."

## Slow operation shows progress

- Microsoft, https://learn.microsoft.com/en-us/windows/apps/design/controls/progress-controls: "A progress control provides feedback to the user that a long-running operation is underway." and "The determinate state for both ProgressBar and ProgressRing shows the percentage completed of a task. This should be used during an operation whose duration is known, but its progress should not block the user's interaction with the app."
- Atlassian Design System, https://atlassian.design/components/spinner/usage: "Only show a spinner if the expected wait time is more than a second. There should only be a single spinner on a page at any time."

## Agent tools get least privilege

- Microsoft, https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk: "Apply least privilege and least action. Allow only the minimum tools, data, and operations required. Deny everything else by default."

## Cache bounds and expiry

- Microsoft Azure Architecture Center, https://learn.microsoft.com/en-us/azure/architecture/best-practices/caching: "You can set a default expiration policy when you configure the cache. In many cache services, you can also specify the expiration period for individual objects when you store them programmatically in the cache."
- Google Cloud (Memorystore), https://cloud.google.com/memorystore/docs/redis/memory-management-best-practices: "If you are using a volatile-* eviction policy, make sure you are setting TTLs on keys that you want to expire, otherwise Redis has no keys to evict." The page names Redis's own `maxmemory` knob, so it partly restates the Redis page.
- Cloudflare, https://developers.cloudflare.com/cache/how-to/edge-browser-cache-ttl/: "Edge Cache TTL (Time to Live) specifies the maximum time to cache a resource in the Cloudflare global network."

## Consistent UI terms

- U.S. General Services Administration (USWDS), https://designsystem.digital.gov/components/icon/: "Be consistent with icon meaning. Icons used more than once in an application or site must be used to represent the same thing, and have the same text description in every instance."
- Atlassian, https://atlassian.design/foundations/iconography: "Wherever possible, use existing icons to maintain consistency and reinforce visual concepts across Atlassian apps so they become familiar to customers."

## Fan-out leg deadlines

- AWS Builders' Library, https://aws.amazon.com/builders-library/timeouts-retries-and-backoff-with-jitter/: "A best practice in Amazon is to set a timeout on any remote call, and generally on any call across processes even on the same box. This includes both a connection timeout and a request timeout." The page is about remote calls, not fan-out by name.

## Lock fencing

- Microsoft (Azure Storage), https://learn.microsoft.com/en-us/azure/storage/blobs/concurrency-manage: "If the blob's current ETag value differs from the ETag value specified in the If-Match conditional header provided on the request, then Azure Storage returns HTTP status code 412 (Precondition Failed)."
- Amazon (DynamoDB), https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/WorkingWithItems.html: "DynamoDB optionally supports conditional writes for these operations. A conditional write succeeds only if the item attributes meet one or more expected conditions. Otherwise, it returns an error." and "Conditional writes check their conditions against the most recently updated version of the item."

## PII minimise and retain

- Microsoft (Purview), https://learn.microsoft.com/en-us/purview/retention: "With these two retention actions, you can configure retention settings for the following outcomes:" and "Retain and then delete: Retain content for a specified period of time and then permanently delete it." The page covers Microsoft 365 content rather than application tables and logs.

## Secrets and errors

- Microsoft (Azure MCP Server), https://learn.microsoft.com/en-us/azure/developer/azure-mcp-server/security: "Fail closed on certificate errors. Treat an unverified or unrecognized Azure MCP Server certificate as a connection failure, not a warning to bypass." The scope is certificate validation, not every validation or auth error.

## Author hygiene

- GitLab, https://docs.gitlab.com/development/code_review/: "Self-review your MR following the Code Review guidelines. Add inline comments on lines where you made decisions or trade-offs, or where context helps the reviewer understand the code." and "You have self-reviewed this MR per code review guidelines."

## Expand and contract

- Microsoft (Azure SQL Dev Corner), https://devblogs.microsoft.com/azure-sql/schema-change/: "Before removing the old column, validate the new state. Confirm that expected rows have values, investigate any unexpected NULL values, verify that reports and downstream consumers have moved, and add any final constraints or indexes that belong on the new columns." and "Expand the schema first. Let old and new representations coexist. Move writes, move data, move reads, validate, and only then contract the schema."

## Refactors in their own commit

- LLVM, https://llvm.org/docs/Contributing.html: "If you think that this might be the case for your changes, or are unsure, we recommend that you add the formatting changes as a separate commit within the Pull Request." and "Reviewers may request that this formatting commit be made into a separate Pull Request that will be merged before your actual changes." The page does not mention renames.

## Verify before claiming

- GitLab, https://docs.gitlab.com/development/code_review/: "Request maintainer reviews only when tests pass. If tests are failing, explain why in a comment." and "You have tested this MR in all supported browsers, or determined that this testing is not needed."

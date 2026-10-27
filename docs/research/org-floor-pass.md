# Organisation floor pass

Ten cards had fewer than three organisations behind them once single authors were set aside. This note records the pages that fill the gaps and the sentence on each page that backs the Rule. A search that found nothing means nothing turned up in this pass, not that nothing exists.

## fn-status-announced-live-region

- W3C, https://www.w3.org/WAI/WCAG22/Techniques/aria/ARIA22: the test step is "Check that the container destined to hold the status message has a role attribute with a value of status", done before the message occurs.
- Mozilla, https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Guides/Live_regions: "Establish the live region before updating its content ... The most reliable way ... is to include them in the initial markup." The same page says `role="alert"` content "is announced, even when the region ... is injected dynamically", so the rule about existing first holds for `role="status"` and `aria-live`, and `role="alert"` is exempt.
- WebAIM, https://webaim.org/techniques/aria/: "This attribute must be set when the page first loads; injecting it later doesn't work reliably."

## svc-no-redundant-entry

- GOV.UK Design System, https://design-system.service.gov.uk/patterns/question-pages: "Make sure to only ask for a piece of information once within a single journey." and "Whenever possible, do not ask a user to re-enter information they've already provided." It suggests "pre-populating the relevant fields" or "showing carried-forward responses as an option for the user to select".
- Baymard Institute, https://baymard.com/blog/set-billing-equal-to-shipping: "the billing address should default to the previously entered shipping address, with the billing address fields hidden". It warns against "forcing users to retype their address again". Baymard sells research, so treat it as a vendor.
- The Nielsen Norman Group heuristics page states recognition over recall, not the practice, so it stays a Why source.

## sys-migration-expand-contract

- GitLab, https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/: "To reduce database pressure you should instead use a background migration"; background migrations "spread the work / load over a longer time period".
- Ecto, https://ecto-sql.hexdocs.pm/backfilling_data.html: "There are four keys to backfilling safely:", and batching is one of them. It also says "Store data migrations separately from your schema migrations."
- CockroachDB, https://docs.cockroachlabs.com/docs/stable/bulk-update-data: "we recommend iteratively updating subsets of the rows that you want to update". CockroachDB is a database vendor and the page backs batching only.
- Stripe, https://stripe.com/blog/online-migrations: the backfill is its own step after dual writing, run as "a large, multi-threaded migration ... with a fleet of processes". It backs the separate-step clause by structure and does not mention batches.

## chg-expand-contract

- Stripe, https://stripe.com/blog/online-migrations: four steps, "Dual writing", "Changing all read paths", "Changing all write paths", "Removing old data".
- Kubernetes, https://kubernetes.io/docs/reference/using-api/deprecation-policy/: an element can not be "removed from that version or have its behavior significantly changed", and the preferred API version "may not advance until after a release has been made that supports both the new version and the previous version". The page states the add-both-then-remove rule for API versions and does not use the name expand-contract.
- GitLab, https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/ covers column renames in the same way.

## chg-refactor-separate

- Google, https://google.github.io/eng-practices/review/developer/small-cls.html: "It's usually best to do refactorings in a separate CL from feature changes".
- Apache Flink, https://flink.apache.org/how-to-contribute/code-style-and-quality-pull-requests/: "Pull Requests must put cleanup, refactoring, and core changes into separate commits." Its examples include "Renaming packages, classes, or methods" and "Moving code (to other packages or classes)".
- Linux kernel, https://docs.kernel.org/process/submitting-patches.html: "Separate each logical change into a separate patch." This is general advice about logical changes and does not name refactors, so it backs the card loosely.
- Python Software Foundation, https://devguide.python.org/getting-started/pull-request-lifecycle/: "Do not do cosmetic changes to unrelated code in the same commit as some feature/bugfix." It backs the reformatting clause only.

## fn-comments-explain-why

- Google, https://google.github.io/eng-practices/review/reviewer/looking-for.html: if the code is not clear, make the code simpler; comments explain why the code exists.
- Mozilla, https://developer.mozilla.org/en-US/docs/MDN/Writing_guidelines/Code_style_guide/JavaScript: "If the purpose or logic of the code isn't obvious, add a comment with your intention" and "restating the code in prose is not a good use of comments".
- Python Software Foundation, https://peps.python.org/pep-0008/: "Inline comments are unnecessary and in fact distracting if they state the obvious." Its useful example is `x = x + 1  # Compensate for border`.
- Apache Flink, https://flink.apache.org/how-to-contribute/code-style-and-quality-common/: "In-code comments help explain the 'why'" and "In-code comments should not state redundant information".
- Linux kernel, https://docs.kernel.org/process/coding-style.html: "it's much better to write the code so that the working is obvious". Only Google and the kernel say to rewrite before commenting, so that point sits in the Why.

## sys-lock-fencing

- Google, https://www.usenix.org/legacy/event/osdi06/tech/full_papers/burrows/burrows.pdf (the OSDI 2006 Chubby paper by Burrows, section 2.4): "The recipient server is expected to test whether the sequencer is still valid and has the appropriate mode; if not, it should reject the request."
- Apache Hadoop, https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-hdfs/HDFSHighAvailabilityWithQJM.html: "the JournalNodes will only ever allow a single NameNode to be a writer at a time." The resource side rejects the stale writer by epoch.
- Hazelcast, https://docs.hazelcast.com/hazelcast/5.7/data-structures/fencedlock: "Lock holders are ordered by a monotonic fencing token ... passed to external services or resources to ensure sequential execution of the side effects." Hazelcast is a vendor, and the page draws on Chubby and Kleppmann.
- AWS, https://aws.amazon.com/builders-library/leader-election-in-distributed-systems/: "garbage collection pauses between a lock being checked and work being done can lead to incorrect behavior". It names the hazard and never says to check at the resource, so it backs the Why only.

## chg-breaking-change-taxonomy

- Google, https://google.aip.dev/180: "APIs must not change visible behavior or semantics in ways that are likely to break reasonable user code." and "Changing the default value is considered breaking and must not be done."
- Microsoft, https://learn.microsoft.com/en-us/dotnet/core/compatibility/library-change-rules: disallowed changes include "Changing the returned values", "Changing the default value of a property, field, or parameter", "Changing the order in which events are fired", and "Adding or removing ... parameters". A change in parsing and throwing new exceptions needs judgment. The page allows "Improving the performance of an operation" and "Changing the text of an error message", so timing is not a breaking change there.
- Kubernetes, https://kubernetes.io/docs/reference/using-api/deprecation-policy/: an element can not be "removed from that version or have its behavior significantly changed".
- The Python devguide pull request page says only "Be aware of backwards-compatibility considerations". It states nothing on this rule and does not count.

## code-dead-code and mod-yagni

- Linux kernel, https://docs.kernel.org/process/coding-style.html: "if a function or variable always goes unused, delete it."
- NVIDIA, https://github.com/NVIDIA/Model-Optimizer/blob/main/CONTRIBUTING.md: "Remove dead code" and "Prefer simple, surgical changes". It is a contributor guide, and its scope advice is about refactors, not abstractions.
- JetBrains, https://www.jetbrains.com/help/inspectopedia/CommentedOutCode.html: "it is better to delete commented out code completely and use the VCS history instead." JetBrains makes IDEs.
- Uber, https://www.uber.com/blog/piranha/: "all code artifacts related to the flag need to be removed from the source code".
- Statsig, https://statsig.com/blog/feature-flag-code-cleanup: stale flags make code "harder to read, reason about, and refactor". Statsig is a vendor.

Only the kernel and NVIDIA state the rule on unused code, commented-out code has one source, and nobody but Google states the rule on speculative abstraction. Both cards are drafts for that reason.

## Pass 9: short clauses on three change cards

- GitLab, https://docs.gitlab.com/development/performance/: "Once a change has been deployed make sure to again measure for at least 24 hours to see if your changes have any impact on the production environment." Backs before-and-after measurement in `chg-perf-claim-evidence`.
- Rust, https://rustc-dev-guide.rust-lang.org/tests/adding.html: "every PR that fixes a bug in rustc [comes] accompanied by a regression test of some kind. This test should fail in main but pass after the PR."
- Rails, https://edgeguides.rubyonrails.org/contributing_to_ruby_on_rails.html: "Include tests that fail without your code, and pass with it."
- Microsoft, https://microsoft.github.io/code-with-engineering-playbook/code-reviews/process-guidance/reviewer-guidance/: "Tests should always be committed in the same PR as the code itself" and "Since parts of reviews can be automated via linters and such, human reviewers can focus on architectural and functional correctness." Backs the same-change clause of `chg-tests-ship-with-change` and the tool-enforced clause of `chg-review-signal`.
- Mozilla, https://firefox-source-docs.mozilla.org/testing/testing-policy/index.html: a landing without tests "requires a comment from the reviewer explaining why it's appropriate". The reviewer writes the reason, not the author, so it does not back the author's stated-reason clause.

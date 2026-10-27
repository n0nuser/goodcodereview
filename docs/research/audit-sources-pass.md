# Sources added after the per-clause audit

Quotes were read on the live pages.

## Dialog focus
- GitHub Primer, https://primer.style/product/components/dialog/accessibility: "On opening, focus should move to the first focusable element inside the modal, with focus locked within the modal until it's closed."

## Placeholder is not a label
- GOV.UK Design System, https://design-system.service.gov.uk/components/text-input/: "Do not use placeholder text in place of a label, or for hints or examples, as:"
- WebAIM, https://webaim.org/techniques/forms/advanced: "The placeholder attribute does not take the place of a <label>."

## Independent work runs together
- Microsoft Learn, https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/: "You wait on each task only when you need the results."
- Apple, https://developer.apple.com/videos/play/wwdc2025/268/: "When you need to perform work in a specific order, you should run that work in a single task."

## Non-text contrast
- WebAIM, https://webaim.org/standards/wcag/checklist: "A contrast ratio of at least 3:1 is present for differentiating graphical objects (such as icons and components of charts or graphs) and author-customized interface components (such as buttons, form controls, and focus indicators/outlines)."

## Canary and abort by rule
- Microsoft Azure Well-Architected, https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments: "Canary deployments are a common example of progressive exposure." and "During a rollout, if you receive an alert about a health change relating to an end user, the rollout should immediately halt".
- AWS CodeDeploy, https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html: "You can configure a deployment group or deployment to automatically roll back when a deployment fails or when a monitoring threshold you specify is met."

## Latency percentiles
- Microsoft Azure Well-Architected, https://learn.microsoft.com/en-us/azure/well-architected/performance-efficiency/monitoring: "Measure performance metrics, like latency, response time, or load times, with percentiles (p50, p95, p99), not averages."

## API deprecation
- GitHub, https://docs.github.com/en/rest/about-the-rest-api/api-versions: the `Deprecation` and `Sunset` response headers, "The date when the API version will be completely removed (retired), after which requests will return a 410 Gone response."
- Google AIP-185, https://google.aip.dev/185: "API elements (fields, messages, RPCs) may be marked deprecated in any channel to indicate that they should no longer be used".

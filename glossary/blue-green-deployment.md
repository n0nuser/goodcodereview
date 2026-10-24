# Blue-green deployment

Two full environments. Traffic switches from the old one to the new one in a single step.

**Why a reviewer cares.** The switch is fast to reverse, but it tests the release all at once, unlike a canary.

**Checks.** `prod-canary-staged-rollout`

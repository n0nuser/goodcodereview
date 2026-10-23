# Blue-Green Deployment

Two full environments; traffic switches from the old to the new in one step.

**Why a reviewer cares.** Fast to reverse, but the whole switch is not a gradual test like a canary.

**Checks.** `prod-canary-staged-rollout`

# Cold Starts

Slow first requests after a deploy, restart or scale-up, when caches and runtimes are empty.

**Why a reviewer cares.** Cold caches can stampede the dependency.

**Checks.** `svc-cache-miss-protection`

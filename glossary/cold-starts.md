# Cold starts

Slow first requests after a deploy, restart, or scale-up, while caches and runtimes are empty.

**Why a reviewer cares.** Cold caches can flood the dependency with requests.

**Checks.** `sys-cache-cold-start`

# Optimistic Locking

Write only if the version is unchanged since read; retry on conflict.

**Why a reviewer cares.** The AWS leader page suggests it before reaching for a leader.

**Checks.** `sys-lock-fencing`

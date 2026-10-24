# Optimistic locking

Write only if the version has not changed since the read. Retry on conflict.

**Why a reviewer cares.** The AWS leader-election page suggests trying it before electing a leader.

**Checks.** `sys-lock-fencing`

# Pessimistic locking

Take a lock before working so that others wait.

**Why a reviewer cares.** Lock duration and mode decide who gets blocked, for example during migrations.

**Checks.** `sys-migration-lock-timeout`

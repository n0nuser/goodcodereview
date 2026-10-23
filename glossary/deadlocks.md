# Deadlocks

Two or more actors each waiting on a lock the other holds.

**Why a reviewer cares.** Timeouts on lock acquisition turn a hang into an error.

**Checks.** `chg-migration-lock-timeout`

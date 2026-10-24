# Deadlocks

Two or more actors that each wait on a lock another one holds.

**Why a reviewer cares.** A timeout on lock acquisition turns a hang into an error.

**Checks.** `sys-migration-lock-timeout`

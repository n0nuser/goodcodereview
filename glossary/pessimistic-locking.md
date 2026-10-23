# Pessimistic Locking

Take a lock before working so others wait.

**Why a reviewer cares.** Lock duration and mode decide who gets blocked, as in migrations.

**Checks.** `chg-migration-lock-timeout`

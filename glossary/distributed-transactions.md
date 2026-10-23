# Distributed Transactions

One logical operation spanning several services or stores, with no single commit.

**Why a reviewer cares.** Without a saga or equivalent, partial failure leaves inconsistent data.

**Checks.** `svc-saga-steps`

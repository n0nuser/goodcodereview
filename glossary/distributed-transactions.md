# Distributed transactions

One logical operation that spans several services or stores and has no single commit.

**Why a reviewer cares.** Without a saga or an equivalent, a partial failure leaves the data inconsistent.

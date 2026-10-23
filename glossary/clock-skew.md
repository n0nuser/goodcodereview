# Clock Skew

Different machines disagreeing about the time.

**Why a reviewer cares.** TTL-based locks and expiry logic depend on clocks; monotonic time is the minimum.

**Checks.** `svc-lock-fencing`

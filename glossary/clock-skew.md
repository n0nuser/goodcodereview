# Clock skew

Machines that disagree about the time.

**Why a reviewer cares.** TTL-based locks and expiry logic depend on clocks. Use monotonic time at a minimum.

**Checks.** `sys-lock-fencing`

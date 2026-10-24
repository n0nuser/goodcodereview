# Load balancing

Spreading requests across several backends and using health signals to skip unhealthy ones.

**Why a reviewer cares.** The health check wired to the balancer decides which hosts stay in rotation. A check that probes a shared dependency can empty the whole pool.

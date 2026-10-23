# Load Balancing

Spreading requests across several backends, using health signals to skip bad ones.

**Why a reviewer cares.** A health check wired to the balancer decides which hosts live or die; a check that probes a shared dependency can empty the whole pool.

# Race conditions

Behaviour that depends on the unplanned timing of concurrent operations.

**Why a reviewer cares.** Reading the code rarely shows them. Ask what guards the shared state.

**Checks.** `sys-lock-fencing`

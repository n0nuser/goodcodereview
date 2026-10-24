# Garbage collection

Automatic reclaiming of unreachable memory.

**Why a reviewer cares.** The collector can reclaim some objects early, such as unreferenced asyncio tasks. Catch these in review.

**Checks.** `py-task-reference`

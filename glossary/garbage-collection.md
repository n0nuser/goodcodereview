# Garbage Collection

Automatic reclaiming of unreachable memory.

**Why a reviewer cares.** Things the collector may reclaim early, like unreferenced asyncio tasks, are a review catch.

**Checks.** `py-create-task-reference`

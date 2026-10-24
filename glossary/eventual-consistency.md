# Eventual consistency

Replicas converge if no new writes arrive, but they can disagree until then.

**Why a reviewer cares.** Code that assumes read-your-writes can break without any error.

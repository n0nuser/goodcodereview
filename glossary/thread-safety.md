# Thread Safety

Code that stays correct when called from several threads at once.

**Why a reviewer cares.** Reviewers should ask which state is shared and what protects it.

**Checks.** `fn-resource-lifetime`

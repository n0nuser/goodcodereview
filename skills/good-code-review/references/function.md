# function

## fn-comments-explain-why

severity: should-fix  
applies_when: A comment sits next to code, or the code needs one to be understood.

**Rule.** Write comments that give a reason, a constraint or a trade-off. Never restate what the next line does. Rename before commenting.

**Why.** A restating comment rots silently and adds nothing. A missing reason makes the next person delete the code that mattered.

**FAIL**

```text
counter += 1  # increment the counter
retry = False  # see the PR, currently disabled
```

**PASS**

```text
# Business decision: activation and entitlement update in one transaction,
# so a user never has access without an active subscription.
# TODO: remove when billing emits entitlement events itself.
```

**Counterpoint.** "Good names make comments unnecessary." Names carry *what*; they cannot carry why a branch exists, a unit, or what callers may rely on, and a missing reason costs more than a slightly stale one. Rename first, then comment what the name cannot say. A stale comment is a defect either way. The test: does it add information the code cannot carry?

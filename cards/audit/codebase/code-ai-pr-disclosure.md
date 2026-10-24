---
id: code-ai-pr-disclosure
level: codebase
tags: [process, agents, contribution]
severity: should-fix
status: draft
lang: core
applies_when: A pull request was written in whole or part by an AI tool.
tool_gate: PR template checkbox for AI assistance; commit trailer check.
borrowed_from:
  - https://docs.kernel.org/process/generated-content.html
  - https://docs.kernel.org/process/coding-assistants.html
  - https://github.com/ghostty-org/ghostty/blob/main/AI_POLICY.md
---

**Rule.** Disclose AI assistance in the PR, and have a human author who can explain and defend every changed line without the tool.

**Why.** Reviewers calibrate by who wrote the code. An undisclosed generated change gets the wrong scrutiny, and an author who cannot explain it leaves the reviewer to do the author's job.

**FAIL**

```text
PR description: "Add retry logic."
(500 generated lines; asked why a 3rd retry, the author says "the model chose it")
```

**PASS**

```text
PR description: "Add retry logic. Drafted with <tool>; I read and tested every line.
 Tests: test_retry.py. Not covered: jitter."
Trailer: Assisted-by: <tool>
```

**Counterpoint.** "Disclosure stigmatises tool use." The rule is about scrutiny, not blame: disclosed work is reviewed the same way and merged on the same terms. The agent never signs off or certifies origin; the human does.

---
id: sys-agent-tool-least-privilege
level: system
tags: [security, process, llm, agents]
severity: block
status: stable
lang: core
applies_when: An LLM agent can call tools, run code, or act on external systems.
tool_gate: Tool registry reviewed in code; downstream credentials scoped in IAM and tested as the agent identity.
note: The narrow tool set is backed by OWASP, NCSC and Microsoft. This Microsoft page is not the MSRC prompt-injection post already cited and states least privilege and least action for the tools, data and operations an agent may use
borrowed_from:
  - https://genai.owasp.org/llmrisk/llm062025-excessive-agency/
  - https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
  - https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
  - https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
  - https://learn.microsoft.com/en-us/security/zero-trust/sfi/manage-agentic-risk
---

**Rule.** Give the agent only the narrow tools and the minimal credentials its task needs.

**Why.** Hallucination or an injected instruction can drive any tool the model holds. An open-ended shell or URL fetch hands over everything the service account can do. Where you can, run each tool as the requesting user rather than a shared admin identity, and let the downstream system check that user's rights on every call. [[sys-prompt-injection]] covers validating model output and human approval; this card covers how much the agent can reach in the first place.

**FAIL**

```text
tools = [shell(), http_fetch(any_url), db(admin_role)]       # one shared service identity
```

**PASS**

```text
tools = [read_ticket(id), add_comment(id, text)]             # narrow functions
creds = user_scoped_token(user, scopes=["tickets:rw"])       # downstream checks the user
```

**Counterpoint.** "Narrow tools make the agent less useful." Add tools when a task needs them and remove those that no task uses. A tool the model never calls is risk without benefit.

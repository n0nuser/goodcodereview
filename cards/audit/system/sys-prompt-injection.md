---
id: sys-prompt-injection
level: system
tags: [security, llm]
severity: block
status: draft
lang: core
applies_when: An LLM reads untrusted text (user input, web pages, documents) and can call tools or produce output that code acts on.
tool_gate: none
borrowed_from:
  - https://genai.owasp.org/llmrisk/llm01-prompt-injection/
---

**Rule.** Validate model output deterministically before code acts on it.

**Why.** Injected instructions in retrieved text can steer tool calls. OWASP says no fool-proof prevention exists and RAG or fine-tuning do not fully fix it, so the goal is limiting impact. Also keep credentials in code, not in the model, and require human approval for high-risk actions.

**FAIL**

```text
tool_call = llm(user_doc); shell(tool_call.cmd)     # model holds the API token
```

**PASS**

```text
cmd = parse_strict(llm(...)); if cmd not in ALLOWED: reject
destructive actions -> human confirm ; untrusted text labelled in the prompt
```

**Counterpoint.** "Guardrail prompts block it." They reduce risk but are not a boundary. The permission model has to hold even when the model is fooled.

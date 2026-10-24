---
id: sys-prompt-injection
level: system
tags: [security, llm]
severity: block
status: stable
lang: core
applies_when: An LLM reads untrusted text (user input, web pages, documents) and can call tools or produce output that code acts on.
tool_gate: none
borrowed_from:
  - https://genai.owasp.org/llmrisk/llm01-prompt-injection/
  - https://www.ncsc.gov.uk/blog-post/prompt-injection-is-not-sql-injection
  - https://www.microsoft.com/en-us/msrc/blog/2025/07/how-microsoft-defends-against-indirect-prompt-injection-attacks
  - https://blog.google/security/mitigating-prompt-injection-attacks/
---

**Rule.** Validate model output deterministically before code acts on it.

**Why.** Injected instructions in retrieved text can steer tool calls. No known prevention is fool-proof, and RAG or fine-tuning do not fully fix it, so the goal is to limit what a fooled model can make the code do. Also keep credentials in code, not in the model, and require human approval for high-risk actions.

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

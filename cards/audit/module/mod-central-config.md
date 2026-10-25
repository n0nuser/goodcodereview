---
id: mod-central-config
level: module
tags: [maintainability, config]
severity: should-fix
status: draft
lacks: orgs, "one settings module" has no org; Uber and Cabify back only keeping knobs out of code
lang: core
applies_when: Business code reads environment variables or holds configuration values.
tool_gate: none
borrowed_from:
  - https://www.uber.com/blog/ubers-rate-limiting-system/
  - https://tech.cabify.com/blog/engineering/hubs-experience
note: from the author's own Python review guide; Uber and Cabify back 'no knobs in code', but nobody backs 'one settings module'
---

**Rule.** Read configuration in one settings module and pass it in; business code must not read the environment or hold knobs.

**Why.** Scattered reads hide what the app depends on and make tests mutate the process environment.

**FAIL**

```text
timeout = float(os.environ.get("TIMEOUT", "5"))   # inside a service
```

**PASS**

```text
settings.request_timeout_s    # defined once in settings.py, injected
```

**Counterpoint.** "One more env read is harmless." Each one hides a deployment dependency from review and from the docs. One module is also where you add validation.

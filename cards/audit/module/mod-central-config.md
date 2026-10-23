---
id: mod-central-config
level: module
tags: [config]
severity: should-fix
status: draft
lang: core
applies_when: Business code reads environment variables or holds configuration values.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Read configuration in one settings module and pass it in. Business code does not read the environment or hold knobs.

**Why.** Scattered reads hide what the app depends on and make tests mutate the process environment.

**FAIL**

```text
timeout = float(os.environ.get("TIMEOUT", "5"))   # inside a service
```

**PASS**

```text
settings.request_timeout_s    # defined once in settings.py, injected
```

**Counterpoint.** "One more env read is harmless." Each hides a deployment dependency from review and from the docs. One module is also where you add validation.

---
id: svc-debug-off-in-production
level: service
tags: [security, config]
severity: should-fix
status: stable
lang: core
applies_when: The service has a debug mode, such as Flask or Django debug, a framework debugger or verbose error pages.
context: [server]
tool_gate: A config check that debug is false in the production settings, and a smoke test that a deliberate server error returns a plain error page with no traceback.
note: The Rule covers debug mode, backed by OWASP ASVS, Django and Flask. Microsoft backs the Swagger UI point in the Why alone, so it is not part of the Rule
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x22-V13-Configuration.md
  - https://docs.djangoproject.com/en/stable/howto/deployment/checklist/
  - https://flask.palletsprojects.com/en/stable/debugging/
  - https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api
---

**Rule.** Keep debug mode off in production, and turn it on by environment so that a missing setting leaves it off.

**Why.** A debug mode prints stack traces, settings and local variables, and some frameworks serve an interactive console that runs code from the browser. Each hands an attacker a map and secrets. A docs UI such as Swagger UI is the same kind of exposure: it lists every endpoint, parameter and model, including internal ones, so serve it in development only or put it behind authentication. Make the safe state the default.

**FAIL**

```python
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=True)   # the interactive debugger is reachable wherever this runs
```

```python
# settings.py
DEBUG = True   # tracebacks with settings and source excerpts on every error page
```

**PASS**

```python
import os
from flask import Flask

app = Flask(__name__)

if __name__ == "__main__":
    app.run(debug=os.environ.get("APP_ENV") == "development")
```

```python
# settings.py
DEBUG = os.environ.get("DJANGO_DEBUG") == "1"   # unset means off
```

**Counterpoint.** "We need the traceback to diagnose a production bug." Send errors to a log or an error tracker, where the team can read them and visitors cannot. To reproduce a problem with debug on, run the same build in a staging environment that is not public.

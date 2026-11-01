---
id: svc-fail-closed-defaults
level: service
tags: [security, configuration]
severity: should-fix
status: stable
lang: core
applies_when: The service reads configuration for authentication, an allow-list, a safety check, or a signing secret.
context: [server]
tool_gate: A startup check that raises on a missing or placeholder secret (Django refuses an unset `SECRET_KEY`; Pydantic Settings fields without a default); a test that boots the service with an empty environment and expects a failed start or denied requests.
note: A route that forgets a login check is a separate defect; this card covers a control that is switched off, empty, or backed by a placeholder until someone configures it. sys-secrets-and-errors covers errors that continue after a failed check
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x22-V13-Configuration.md
  - https://learn.microsoft.com/en-us/aspnet/core/security/authorization/secure-data
  - https://google.github.io/building-secure-and-reliable-systems/raw/ch08.html
  - https://docs.djangoproject.com/en/5.2/ref/settings/
  - https://cwe.mitre.org/data/definitions/1393.html
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic_policy-eval-denyallow.html
  - https://www.cisa.gov/sites/default/files/2023-10/SecureByDesign_1025_508c.pdf
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  - https://github.com/usnistgov/oscal-content/blob/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json
---

**Rule.** Ship every security control switched on, with an empty allow-list denying everything.

**Why.** A control that is off until configured is off in the deployment where nobody read the setup page. An empty allow-list that means "allow all" and a built-in `changeme` key both boot cleanly, so nothing alerts anyone while the service runs open or signs tokens anyone can forge. Refuse to start when a secret is missing or still a placeholder: failing at startup moves the discovery from an incident to the first deploy.

**FAIL**

```python
import os

AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "false") == "true"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")  # "" means no filtering below
SECRET_KEY = os.environ.get("SECRET_KEY", "changeme")

def host_ok(host):
    return not ALLOWED_HOSTS[0] or host in ALLOWED_HOSTS
```

**PASS**

```python
import os

AUTH_ENABLED = os.environ.get("AUTH_ENABLED", "true") == "true"
ALLOWED_HOSTS = [h for h in os.environ.get("ALLOWED_HOSTS", "").split(",") if h]
SECRET_KEY = os.environ["SECRET_KEY"]          # KeyError stops the boot
if SECRET_KEY in {"", "changeme"}:
    raise RuntimeError("SECRET_KEY is a placeholder")

def host_ok(host):
    return host in ALLOWED_HOSTS               # empty list denies all
```

**Counterpoint.** "Developers need to run it locally without setup." Give them a separate dev entry point or a dev-only flag that is named for what it does (`INSECURE_DEV_MODE=1`) and that production images never set. The default stays closed, and the open mode is a visible, greppable choice.

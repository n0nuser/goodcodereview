---
id: fn-mask-credentials-in-output
level: function
tags: [security, secrets, usability]
severity: should-fix
status: stable
lang: core
applies_when: A CLI command, admin page or debug view prints stored configuration that can include tokens, API keys, or URLs with embedded secrets.
context: [cli]
tool_gate: A test that seeds a fake token, runs the list/show/debug command, and asserts the full value is absent from stdout and stderr.
note: sys-secrets-and-errors covers secrets in errors and logs; this card covers a command whose purpose is to display configuration. svc-no-secrets-in-url covers secrets in request URLs
borrowed_from:
  - https://cli.github.com/manual/gh_auth_status
  - https://docs.djangoproject.com/en/5.2/ref/settings/
  - https://docs.gitlab.com/ci/variables/
  - https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html
  - https://docs.aws.amazon.com/cli/latest/reference/configure/list.html
  - https://kubernetes.io/docs/reference/kubectl/generated/kubectl_config/kubectl_config_view/
  - https://www.pulumi.com/docs/iac/concepts/secrets/
---

**Rule.** Mask credentials in list, show and debug output (keep only the last four characters), and print a full value only behind an explicit flag.

**Why.** Output gets pasted into tickets, chat and CI logs, and screen-shared. A webhook URL that carries its token, or an API key shown whole by `config show`, becomes a leak the first time someone asks for help. Masking keeps the output useful for telling two credentials apart.

**FAIL**

```python
for hook in hooks:
    print(f"{hook.name}\t{hook.url}")      # https://hooks.example.com/T0/B1/xK9...full secret
print("api_key:", settings.api_key)
```

**PASS**

```python
def mask(value: str) -> str:
    return "****" + value[-4:] if len(value) > 8 else "****"

for hook in hooks:
    print(f"{hook.name}\t{urlsplit(hook.url).netloc}/...{hook.url[-4:]}")
print("api_key:", mask(settings.api_key))
# `show --reveal` prints the full value on request
```

**Counterpoint.** "Users need the value to copy it." Then give them an explicit reveal flag that is off by default, so the copy is a deliberate act and the default output is safe to paste. Never ask users to scrape the full secret out of a listing.

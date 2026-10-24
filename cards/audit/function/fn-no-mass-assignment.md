---
id: fn-no-mass-assignment
level: function
tags: [security, authz, api]
severity: block
status: stable
lang: core
applies_when: A handler copies request fields into a model, ORM entity or settings object.
tool_gate: A custom Semgrep rule for `Model(**request.json)`; tests that post extra fields such as `is_admin` and assert they are ignored or rejected.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Mass_Assignment_Cheat_Sheet.html
  - https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization
  - https://learn.microsoft.com/en-us/aspnet/core/data/ef-mvc/crud?view=aspnetcore-9.0
  - https://guides.rubyonrails.org/action_controller_overview.html
  - https://docs.djangoproject.com/en/5.2/topics/forms/modelforms/
---

**Rule.** Bind request data to a DTO or an explicit field allowlist, never straight onto the model.

**Why.** When the model has `is_admin`, `balance` or `owner_id`, a client that adds those keys to the JSON body sets them. A blocklist fails the day someone adds a new sensitive column. The allowlist still needs the object-level check from [[fn-object-level-authz]].

**FAIL**

```text
user = User(**request.json)          # body {"name": "a", "is_admin": true}
user.save()
```

**PASS**

```text
class UserIn(BaseModel):            # only editable fields exist here
    name: str
user = User(**UserIn(**request.json).model_dump())
```

**Counterpoint.** "A DTO per endpoint is boilerplate." Generate DTOs from the API schema. The boilerplate costs less than one privilege escalation.

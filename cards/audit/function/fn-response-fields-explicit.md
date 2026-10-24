---
id: fn-response-fields-explicit
level: function
tags: [security, compatibility, api, data]
severity: should-fix
status: stable
lang: core
applies_when: A handler returns a stored object or entity to the client.
tool_gate: Response-schema tests that fail on unlisted fields.
borrowed_from:
  - https://api-security.owasp.org/editions/2023/en/0xa3-broken-object-property-level-authorization
  - https://learn.microsoft.com/en-us/aspnet/core/tutorials/first-web-api
  - https://www.django-rest-framework.org/api-guide/serializers/
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228-upd1.pdf
---

**Rule.** Return a response type that lists each field, never the stored model or a generic dump of it.

**Why.** A model gains `password_hash`, `internal_notes` or `email` and every endpoint that serialises it leaks the new field silently. Callers also start to depend on whatever is sent, so removing a field later is a breaking change. An explicit response type makes each exposed field a decision someone reviewed. The write side is [[fn-no-mass-assignment]].

**FAIL**

```text
return jsonify(user.__dict__)
return user_model.to_dict()          # all columns
```

**PASS**

```text
class UserOut(BaseModel): id: int; display_name: str
return UserOut.model_validate(user)
```

**Counterpoint.** "A response type per endpoint duplicates the model." Derive it from the model with a field list. The duplication is one line per field and shows up in the diff when a field is added.

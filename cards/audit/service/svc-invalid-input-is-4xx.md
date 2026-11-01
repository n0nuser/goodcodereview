---
id: svc-invalid-input-is-4xx
level: service
tags: [correctness, reliability, api, validation]
severity: should-fix
status: stable
lang: core
applies_when: A handler takes a number, an id, a header or a body field from the caller and uses it in a query, a calculation or an encoder.
context: [server]
tool_gate: Schema or model constraints on every field (minimum, maximum, enum, format); a test that posts a negative number, an unknown id and a non-ASCII header and expects a 4xx.
note: The domain check and the reject are backed by OWASP, Google (gRPC INVALID_ARGUMENT, user code only) and Kubernetes (422). The 4xx class is backed by IETF, Microsoft, Stripe, Google and Kubernetes. A missing id answering 404 is backed by IETF, Google (NOT_FOUND) and Kubernetes. Stripe and Microsoft state the status for a bad request, not for a foreign key. Which 4xx and where the check lives are covered by other cards
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
  - https://grpc.io/docs/guides/status-codes/
  - https://github.com/kubernetes/community/blob/master/contributors/devel/sig-architecture/api-conventions.md
  - https://www.rfc-editor.org/rfc/rfc9110.html#name-client-error-4xx
  - https://learn.microsoft.com/en-us/azure/architecture/best-practices/api-design
  - https://docs.stripe.com/api/errors
---

**Rule.** Check each caller-supplied value against its allowed domain (range, allowed set, an id that must exist, an encoding the code can handle) at the boundary, and answer a failed check with a 4xx, never a 5xx.

**Why.** A negative quota, a limit of zero, an id with no row, or a header with a non-ASCII character is the caller's error. If it reaches the database or an `.encode("ascii")`, the user gets a 500: the caller retries, the error-rate alert fires, and a negative quota may be stored and later allow unlimited use. A schema constraint or an explicit lookup costs one line per field. [[svc-bound-client-controlled-sizes]] caps size and count; this card covers every other value.

**FAIL**

```python
@app.post("/quotas")
def set_quota(body: dict):
    db.execute("UPDATE plans SET quota=%s WHERE id=%s", (body["quota"], body["plan_id"]))
    # quota=-5 is stored; a plan_id with no row updates nothing and answers 200
    return {"ok": True}

def sign(request):
    return hmac_header(request.headers["X-Name"].encode("ascii"))   # "Zoë" -> UnicodeEncodeError -> 500
```

**PASS**

```python
class SetQuota(BaseModel):
    quota: int = Field(ge=0, le=10_000)
    plan_id: int

@app.post("/quotas")
def set_quota(body: SetQuota):
    if not db.exists("SELECT 1 FROM plans WHERE id=%s", (body.plan_id,)):
        raise HTTPException(404, "unknown plan_id")
    db.execute("UPDATE plans SET quota=%s WHERE id=%s", (body.quota, body.plan_id))

def sign(request):
    try:
        name = request.headers["X-Name"].encode("ascii")
    except UnicodeEncodeError:
        raise HTTPException(400, "X-Name must be ASCII")
    return hmac_header(name)
```

**Counterpoint.** "The database has a CHECK and a foreign key, so the data is safe." It is, but the constraint violation surfaces as a 500 unless the code maps it. Keep the constraint as the last line and validate first, so the caller gets a message that names the field. Catching the database error and mapping it to a 4xx also meets this card when a pre-check would race.

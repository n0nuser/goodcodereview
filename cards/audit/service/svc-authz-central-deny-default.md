---
id: svc-authz-central-deny-default
level: service
tags: [security, authz]
severity: block
status: draft
lang: core
applies_when: The service exposes routes or functions that different roles may call.
tool_gate: Router that denies routes with no policy; a test that lists every route and its required role.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html
  - https://api-security.owasp.org/editions/2023/en/0xa5-broken-function-level-authorization
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control
  - https://portswigger.net/web-security/access-control
  - https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic_policy-eval-denyallow.md
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-228-upd1.pdf
---

**Rule.** Route every request through one authorization layer that denies when no rule allows it.

**Why.** Per-handler checks drift: one admin route ships without its decorator and any user can call it. A central layer with deny as the fallback turns a forgotten check into a 403 instead of a hole. [[svc-sqli-authn]] names the default-deny idea; this card is the structure that enforces it.

**FAIL**

```text
@app.route("/admin/export")        # no role check; framework default is allow
def export(): ...
```

**PASS**

```text
policy = {"/admin/export": {"admin"}}      # one table, reviewed in one place
@app.before_request
def gate(): require_role(policy.get(request.path))   # missing entry -> 403
```

**Counterpoint.** "A central policy is a bottleneck for feature teams." Keep the engine central and let each team own its rows. The cost of a one-line policy entry is small next to an unguarded admin route.

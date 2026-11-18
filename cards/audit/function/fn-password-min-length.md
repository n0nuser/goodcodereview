---
id: fn-password-min-length
level: function
tags: [security, authn]
severity: should-fix
status: stable
lang: core
applies_when: Code accepts a new password from a user, at sign-up, a change, or a reset.
context: [server]
tool_gate: none; a test that submits a short password. ASP.NET Identity sets it with Password.RequiredLength.
borrowed_from:
  - https://pages.nist.gov/800-63-4/sp800-63b.html
  - https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html
  - https://www.cisa.gov/sites/default/files/2023-01/cisa_cpg_checklist_12052022.pdf
  - https://www.ncsc.gov.uk/files/Cyber-Essentials-Requirements-for-Infrastructure-v3-1-April-2023.pdf
---

**Rule.** Enforce a minimum password length on the server whenever a user sets a password.

**Why.** Length is the cheapest strength control: each added character multiplies the guesses an attacker needs. A check in the browser alone can be skipped by calling the API directly. NIST asks for 15 characters when the password is the only factor, and 8 when it is one of several. Framework defaults can be lower, so set the number on purpose.

**FAIL**

```python
@app.post("/signup")
def signup(form):
    user = create_user(form.email, hash_password(form.password))
```

**PASS**

```python
MIN_PASSWORD_LENGTH = 15

@app.post("/signup")
def signup(form):
    if len(form.password) < MIN_PASSWORD_LENGTH:
        return error("Password must be at least 15 characters")
    user = create_user(form.email, hash_password(form.password))
```

**Counterpoint.** "Long minimums push users to reuse or write passwords down." Length without composition rules is easier to remember than a short mixed password, and a passphrase works. Pair the limit with a generous maximum of at least 64 characters, and never truncate silently.

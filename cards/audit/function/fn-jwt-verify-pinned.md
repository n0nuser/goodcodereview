---
id: fn-jwt-verify-pinned
level: function
tags: [security, authn, jwt]
severity: block
status: stable
lang: core
applies_when: Code accepts a JWT as proof of identity or permission.
tool_gate: CodeQL `js/jwt-missing-verification`; a grep for `verify_signature": False` and for `jwt.decode(` calls with no `algorithms=`.
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc8725
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control
  - https://cheatsheetseries.owasp.org/cheatsheets/JSON_Web_Token_Cheat_Sheet.html
  - https://learn.microsoft.com/en-us/entra/identity-platform/access-tokens
  - https://developers.google.com/identity/gsi/web/guides/verify-google-id-token
  - https://codeql.github.com/codeql-query-help/javascript/js-jwt-missing-verification/
  - https://pyjwt.readthedocs.io/en/stable/api.html
---

**Rule.** Verify the signature against a fixed list of accepted algorithms, and check `iss` and `aud`, before reading any claim.

**Why.** If the verifier takes the algorithm from the token header, an attacker picks `none` or turns an RSA public key into an HMAC secret. Claims read before verification are attacker text. Pinning the algorithm and binding each key to one algorithm closes both. Also require `exp`, so a stolen token stops working.

**FAIL**

```python
claims = jwt.decode(token, options={"verify_signature": False})
claims = jwt.decode(token, key)               # PyJWT 1.x: algorithm taken from the header
```

**PASS**

```python
claims = jwt.decode(token, key, algorithms=["RS256"],
                    issuer=ISSUER, audience=AUD,
                    options={"require": ["exp", "iss", "aud"]})
```

**Counterpoint.** "Our gateway already verifies the token." Then the service trusts a header that any internal caller can forge. Verify at each trust boundary, or prove that only the gateway can reach the service.

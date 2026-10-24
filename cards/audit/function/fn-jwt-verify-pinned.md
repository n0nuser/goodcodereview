---
id: fn-jwt-verify-pinned
level: function
tags: [security, authn, jwt]
severity: block
status: draft
lang: core
applies_when: Code accepts a JWT as proof of identity or permission.
tool_gate: SAST rule for `decode(..., verify=False)` and for a missing `algorithms=` argument.
note: RFC 8725 used; OWASP's JWT cheat sheet URLs returned 404 during the fetch
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc8725
  - https://top10.owasp.org/2025/A01_2025-Broken_Access_Control
---

**Rule.** Verify the signature against a fixed algorithm list, then check `exp`, `iss` and `aud` before reading any claim.

**Why.** If the verifier takes the algorithm from the token header, an attacker picks `none` or turns an RSA public key into an HMAC secret. Claims read before verification are attacker text. Pinning the algorithm and binding each key to one algorithm closes both.

**FAIL**

```python
claims = jwt.decode(token, options={"verify_signature": False})
claims = jwt.decode(token, key)               # algorithm taken from the header
```

**PASS**

```python
claims = jwt.decode(token, key, algorithms=["RS256"],
                    issuer=ISSUER, audience=AUD,
                    options={"require": ["exp", "iss", "aud"]})
```

**Counterpoint.** "Our gateway already verifies the token." Then the service trusts a header that any internal caller can forge. Verify at each trust boundary, or prove that only the gateway can reach the service.

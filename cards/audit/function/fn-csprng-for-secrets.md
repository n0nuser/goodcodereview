---
id: fn-csprng-for-secrets
level: function
tags: [security, crypto]
severity: block
status: stable
lang: core
applies_when: Code generates a token, session ID, password-reset code, API key, nonce or IV.
tool_gate: Bandit B311 (`random`) for Python; elsewhere a grep for `Math.random` and `rand()` in code that builds tokens or keys.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
  - https://docs.python.org/3/library/secrets.html
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Math/random
  - https://www.rfc-editor.org/rfc/rfc4086.html
  - https://pkg.go.dev/crypto/rand
---

**Rule.** Draw every security-relevant random value from the platform CSPRNG.

**Why.** A general-purpose PRNG is predictable from a few outputs, so an attacker who sees two tokens can guess the next. UUIDv1 is time-based and also not secret. The API call is the whole fix, so it is cheap to demand.

**FAIL**

```python
token = "".join(random.choices(string.ascii_letters, k=32))
reset = str(int(time.time()))
```

**PASS**

```python
token = secrets.token_urlsafe(32)           # os.urandom under the hood
# JavaScript: crypto.getRandomValues(new Uint8Array(32))
```

**Counterpoint.** "Math.random is fine for a short-lived code." Short-lived codes still get brute-forced, and predictable ones need no brute force. Use the CSPRNG for anything an attacker gains from guessing.

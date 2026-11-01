---
id: fn-constant-time-secret-compare
level: function
tags: [security, crypto]
severity: should-fix
status: stable
lang: core
applies_when: Code compares a caller-supplied API key, token, signature, MAC or CSRF value with a stored or computed secret.
tool_gate: Semgrep or CodeQL rules for `==` on secrets; Bandit has no rule for this, so grep for `==` next to names such as `token`, `signature`, `api_key`, `digest`.
note: fn-csprng-for-secrets covers generating the value; this card covers checking it. A password hash check goes through the hash library's verify call (fn-password-slow-hash)
borrowed_from:
  - https://docs.python.org/3/library/hmac.html
  - https://pkg.go.dev/crypto/subtle
  - https://nodejs.org/api/crypto.html
  - https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries
  - https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://cwe.mitre.org/data/definitions/208.html
---

**Rule.** Compare a secret, token or MAC with the platform's constant-time function, never with `==` or `!=`.

**Why.** Ordinary equality stops at the first differing byte, so the response time tells an attacker how many leading bytes were right. Repeated requests recover the value one byte at a time. The constant-time call costs one line and no performance anyone will notice.

**FAIL**

```python
def verify(body: bytes, header_sig: str, key: bytes) -> bool:
    expected = hmac.new(key, body, "sha256").hexdigest()
    return expected == header_sig
```

**PASS**

```python
def verify(body: bytes, header_sig: str, key: bytes) -> bool:
    expected = hmac.new(key, body, "sha256").hexdigest()
    return hmac.compare_digest(expected.encode(), header_sig.encode())   # bytes: a non-ASCII header raises no TypeError
# Go: subtle.ConstantTimeCompare(a, b) == 1
# Node: crypto.timingSafeEqual(bufA, bufB) after checking the lengths match
```

**Counterpoint.** "Network jitter hides the difference." Attackers average thousands of samples, and the jitter shrinks when they sit in the same cloud region. Also, some constant-time functions need equal lengths (Node throws otherwise); compare fixed-length digests, or check the length first, since the length of a MAC is not secret.

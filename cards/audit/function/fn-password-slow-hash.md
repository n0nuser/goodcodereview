---
id: fn-password-slow-hash
level: function
tags: [security, authn, crypto]
severity: block
status: draft
lang: core
applies_when: Code stores or verifies a user password.
tool_gate: Grep or SAST rule for `md5`, `sha1`, `sha256` near a `password` identifier.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
  - https://www.rfc-editor.org/rfc/rfc9106.html
  - https://pages.nist.gov/800-63-4/sp800-63b.html
---

**Rule.** Hash passwords with Argon2id (or scrypt, bcrypt, PBKDF2) and a per-password salt from the library.

**Why.** A fast hash such as SHA-256 lets an attacker with the database try billions of guesses a second. A slow, salted, memory-hard hash makes each guess cost real time. OWASP lists Argon2id with at least 19 MiB memory and 2 iterations as the baseline; check the current numbers when you review.

**FAIL**

```text
stored = hashlib.sha256(password.encode()).hexdigest()
```

**PASS**

```text
ph = argon2.PasswordHasher()            # salt and parameters stored in the hash string
stored = ph.hash(password)
ph.verify(stored, attempt)             # rehash when check_needs_rehash()
```

**Counterpoint.** "Argon2 is expensive at login." That cost is the defence; tune it to about a second on production hardware. Where FIPS compliance rules Argon2 out, PBKDF2-HMAC-SHA256 with a high iteration count is the accepted fallback.

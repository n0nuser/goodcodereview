---
id: mod-vetted-crypto-only
level: module
tags: [security, crypto]
severity: block
status: stable
lang: core
applies_when: A module encrypts or decrypts data.
tool_gate: A grep for `MODE_ECB`, `MODE_CBC` with no MAC, and nonces built from constants.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
  - https://www.rfc-editor.org/rfc/rfc5116.html
  - https://csrc.nist.gov/pubs/sp/800/38/d/final
  - https://pkg.go.dev/crypto/cipher#NewGCM
  - https://developers.google.com/tink
---

**Rule.** Encrypt with an authenticated mode such as AES-GCM, and never reuse a nonce under one key.

**Why.** Unauthenticated modes allow silent tampering, and ECB also leaks the structure of the plaintext. Reusing a nonce under one key breaks GCM completely: it leaks the XOR of the plaintexts and the authentication key. Take the call from a maintained library and never write your own cipher. Keys belong in a KMS or secrets manager, never in source; [[sys-secrets-and-errors]] covers where secrets live at runtime.

**FAIL**

```python
cipher = AES.new(KEY, AES.MODE_ECB)
ct = bytes(b ^ k for b, k in zip(msg, KEY * 99))
```

**PASS**

```python
aead = AESGCM(key_from_kms)
ct = aead.encrypt(os.urandom(12), msg, aad)      # fresh nonce per message
```

**Counterpoint.** "The library API is awkward, so a wrapper is safer." Wrap the vetted call, do not replace it. Review the wrapper only for nonce handling and key sourcing.

---
id: mod-vetted-crypto-only
level: module
tags: [security, crypto]
severity: block
status: draft
lang: core
applies_when: A module encrypts, signs or derives keys.
tool_gate: SAST rules for `ECB`, hand-written XOR ciphers and MD5 or SHA-1 used as a security primitive.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html
  - https://top10.owasp.org/2025/A04_2025-Cryptographic_Failures
---

**Rule.** Use a maintained library's authenticated-encryption call (AES-GCM or similar), and never write your own cipher or reuse a nonce.

**Why.** Home-made schemes and ECB mode leak structure. Unauthenticated modes allow silent tampering. Reusing a nonce under one key breaks GCM completely. Keys belong in a KMS or secrets manager, never in source; [[sys-secrets-and-errors]] covers where secrets live at runtime.

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

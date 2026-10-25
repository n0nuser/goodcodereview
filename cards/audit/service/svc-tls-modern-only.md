---
id: svc-tls-modern-only
level: service
tags: [security, tls, network]
severity: should-fix
status: draft
lang: core
applies_when: The service or its load balancer terminates TLS.
tool_gate: testssl.sh or a similar scan against the public endpoint in CI; the load balancer's named security policy checked in config review.
note: ASVS 12.1.1 and 12.1.2; fn-tls-verify-on covers the client side
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc8996.html
  - https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-52r2.pdf
  - https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x21-V12-Secure-Communication.md
  - https://learn.microsoft.com/en-us/security/engineering/solving-tls1-problem
---

**Rule.** Accept only TLS 1.2 and TLS 1.3 on servers, and set that minimum in the config instead of relying on the default.

**Why.** TLS 1.0 and 1.1 lack modern cipher suites and are deprecated by RFC 8996, and SSL 3.0 is broken outright. A server that still offers them lets an attacker on the path force a downgrade, and it fails compliance scans. Library defaults have moved to TLS 1.2, but an explicit lower setting, an old base image, or a load-balancer policy from years ago keeps the old versions alive. With TLS 1.2, prefer AEAD suites with forward secrecy.

**FAIL**

```python
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version = ssl.TLSVersion.TLSv1
```

**PASS**

```python
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ctx.minimum_version = ssl.TLSVersion.TLSv1_2
```

**Counterpoint.** "Some of our users have old clients." NIST SP 800-52 lets public-facing servers keep TLS 1.0 and 1.1 when needed, after checking who still uses them. Measure first: log the negotiated version, and if old clients are a real share, serve them from a separate endpoint with an end date instead of weakening every endpoint.

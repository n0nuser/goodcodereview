---
id: fn-header-value-encoding
level: function
tags: [security, http, injection]
severity: block
status: stable
lang: core
applies_when: A handler puts a request-derived value into a response header, such as `Location` or `Set-Cookie`.
context: [server]
tool_gate: A test that sends `%0d%0a` in the echoed parameter and asserts a 400 or an encoded value; Node and Django throw at runtime, which is a guard rather than a linter.
note: fn-redirect-target-allowlist checks where a redirect points; this card checks how the value is written. Both clauses have IETF (RFC 9112 names header-writing APIs that filter bad octets), MITRE, OpenJS and Django
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9112.html
  - https://cwe.mitre.org/data/definitions/113.html
  - https://nodejs.org/api/http.html
  - https://docs.djangoproject.com/en/5.2/ref/request-response/
---

**Rule.** Set every response header through the framework's header API, never by writing to the connection, and reject or encode CR and LF in any request-derived value.

**Why.** A header value is one line. Bytes that end the line start a new header, so a value the attacker controls can add a header or a second response. The browser follows the attacker's redirect, stores the attacker's cookie, or reads the attacker's body under your origin. Filtering `%0d%0a` at one decode step is not enough, because a second decode or a charset change puts the bytes back.

**FAIL**

```python
u = request.query["u"]                    # %0d%0a arrives as CR LF
conn.write(f"HTTP/1.1 302 Found\r\nLocation: /next?u={u}\r\n\r\n")
```

The CR and LF from the query end the `Location` line, so the browser reads the rest of the value as another header.

**PASS**

```python
u = request.query["u"]
resp = Response(status=302)
resp.headers["Location"] = "/next?u=" + quote(u, safe="")   # quote() encodes CR and LF; the header API rejects any that remain
```

**Counterpoint.** "The framework rejects newlines, so this cannot happen." It does reject them, for headers set through its API. The failure sits in the code that writes the status line or the whole response itself, such as a proxy, a websocket handshake, or a hand-rolled error page. Keep those on the API path too.

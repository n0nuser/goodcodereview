---
id: sys-ssrf
level: system
tags: [security, ssrf]
severity: block
status: stable
lang: core
applies_when: The server fetches a URL that a user or external data supplies.
tool_gate: CodeQL `py/full-ssrf`; an egress proxy or firewall allowlist.
borrowed_from:
  - https://owasp.org/Top10/2025/
  - https://cheatsheetseries.owasp.org/cheatsheets/Server_Side_Request_Forgery_Prevention_Cheat_Sheet.html
  - https://codeql.github.com/codeql-query-help/python/py-full-ssrf/
  - https://docs.aws.amazon.com/codeguru/detector-library/go/server-side-request-forgery/
  - https://portswigger.net/web-security/ssrf
---

**Rule.** Fetch a user-supplied URL only when its host matches a server-side allowlist.

**Why.** The server can reach networks that the attacker cannot, such as internal services and the cloud metadata address, and an open fetch lets the attacker read them. A hostname allowlist alone does not stop DNS rebinding, so also check that the resolved address is not private and connect to that address. Turn off redirect following, or check each redirect target the same way.

**FAIL**

```python
requests.get(request.args["url"])
```

**PASS**

```python
u = urlparse(request.args["url"])
if u.scheme != "https" or u.hostname not in ALLOWED_HOSTS: abort(400)
requests.get(u.geturl(), allow_redirects=False, timeout=5)
```

**Counterpoint.** "Blocklisting private ranges is enough." Alternate IP forms, URL parser tricks and open redirects get past a blocklist. An allowlist fails closed when someone finds a new trick.

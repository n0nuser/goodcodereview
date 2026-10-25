---
id: fn-xml-no-external-entities
level: function
tags: [security, xml, parsing]
severity: block
status: draft
lacks: evidence, OWASP, PortSwigger and GitHub CodeQL are listed, but no stable pass has read them for a recommendation versus a definition
lang: core
applies_when: Code parses XML, SVG, SOAP, SAML, or an office document that a user or another system can supply.
tool_gate: CodeQL `py/xxe`; Bandit B313 to B319 (stdlib XML parse calls) and B405 to B410 (XML imports).
note: ASVS 1.5.1; sys-ssrf covers outbound fetches that XXE can also trigger
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/XML_External_Entity_Prevention_Cheat_Sheet.html
  - https://cwe.mitre.org/data/definitions/611.html
  - https://portswigger.net/web-security/xxe
  - https://codeql.github.com/codeql-query-help/python/py-xxe/
---

**Rule.** Parse untrusted XML with DTDs, external entities, and network access turned off, or with a hardened wrapper such as `defusedxml`.

**Why.** A DTD can declare an entity whose value is `file:///etc/passwd` or an internal URL, and a parser that resolves it pastes that content into the document or makes the request for the attacker. Nested internal entities can also expand a small file into gigabytes. Each parser has its own switches, so name them in the code instead of trusting the library default.

**FAIL**

```python
parser = lxml.etree.XMLParser(resolve_entities=True, no_network=False)
doc = lxml.etree.fromstring(request.get_data(), parser)
```

**PASS**

```python
import defusedxml.ElementTree as ET
doc = ET.fromstring(request.get_data())   # rejects DTD entities by default
```

**Counterpoint.** "Recent Python XML modules already refuse external entities." Some do, and CodeQL says so. The FAIL above opts back in, Java and .NET parsers have their own defaults, and a later change to the parser config reopens the hole. An explicit hardened parser makes the setting visible in review.

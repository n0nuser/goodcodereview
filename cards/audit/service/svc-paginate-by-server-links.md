---
id: svc-paginate-by-server-links
level: service
tags: [correctness, compatibility, api]
severity: should-fix
status: draft
lacks: orgs, next link has GitHub firm; Microsoft and Zalando state server-side rules only; opaque token has Google and Zalando (cursor opacity); needs more client-side orgs
lang: core
applies_when: The code calls a paginated HTTP or RPC API and reads more than one page.
context: [server]
tool_gate: none
note: Microsoft says the server must return a nextLink the client can GET. Zalando says the server should return pagination links and that a cursor is an opaque pointer never to be inspected or constructed by clients. Zalando body text for the links rule was not matched, only its heading
borrowed_from:
  - https://docs.github.com/en/rest/using-the-rest-api/using-pagination-in-the-rest-api
  - https://google.aip.dev/158
  - https://raw.githubusercontent.com/microsoft/api-guidelines/vNext/azure/Guidelines.md
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Fetch the next page only from the link or token the server returned; do not build page numbers or open the token.

**Why.** The server owns the paging scheme. A client that builds `page=N` or reads fields out of a token breaks when the server switches to cursors or changes the token layout. Page numbers also skip or repeat items when rows are inserted between requests.

**FAIL**

```python
page = 1
while True:
    r = requests.get(f"{base}/issues", params={"per_page": 100, "page": page}, timeout=10)
    if not r.json():
        break
    items.extend(r.json())
    page += 1
```

**PASS**

```python
url = f"{base}/issues?per_page=100"
while url:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    items.extend(r.json())
    url = r.links.get("next", {}).get("url")
```

**Counterpoint.** "Page numbers let us fetch pages in parallel or jump to the last one." Do that only when the API documents page numbers as part of its contract. Otherwise the next link is the only promise the server makes, and a parallel fetch can be built from the first response only if the server says how.

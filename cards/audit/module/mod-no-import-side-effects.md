---
id: mod-no-import-side-effects
level: module
tags: [testing, maintainability, architecture]
severity: block
status: draft
lacks: orgs, only the author's own Python review guide backs it; no independent org
lang: core
applies_when: A module does anything at import or load time other than defining names.
tool_gate: none
borrowed_from: []
note: from the author's own Python review guide
---

**Rule.** Keep I/O at the edges: importing a package must not touch the network, read files, or read the environment.

**Why.** Import-time effects make tests slow and order-dependent, break tooling that merely imports the module, and fail in places that had no reason to need a network.

**FAIL**

```text
CLIENT = HttpClient(os.environ["API_URL"])   # at import
DATA = json.load(open("data.json"))
```

**PASS**

```text
def make_client(settings): return HttpClient(settings.api_url)
def load_data(path): ...
```

**Counterpoint.** "Loading once at import is fast." Load once at startup, explicitly, where the caller controls it and tests can substitute it.

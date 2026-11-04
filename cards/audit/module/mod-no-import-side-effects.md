---
id: mod-no-import-side-effects
level: module
tags: [testing, maintainability, architecture]
severity: should-fix
status: stable
lang: core
applies_when: A module does anything at import or load time other than defining names.
tool_gate: none
borrowed_from:
  - https://airflow.apache.org/docs/apache-airflow/2.10.0/best-practices.html
  - https://azure.github.io/azure-sdk/typescript_implementation.html
  - https://dagster.io/blog/dignified-python-10-rules-to-improve-your-llm-agents
  - https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/BEST_PRACTICES.md
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

# Promote mod-no-module-mutable-state

Rule: "Keep no mutable state at module level." One clause. Read live 2026-11-01.

| Org | URL | Verbatim quote |
|---|---|---|
| Google | https://google.github.io/styleguide/pyguide.html#25-mutable-global-state | "Avoid mutable global state." ... "Module-level constants are permitted and encouraged." |
| Uber | https://github.com/uber-go/guide/blob/master/style.md#avoid-mutable-globals | "Avoid mutating global variables, instead opting for dependency injection." |
| Microsoft | https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/ca2211 | "static fields are best used to store data that does not change." Fix: "make the static field constant or read-only." |

Caveats: CA2211 targets public or protected static fields in libraries ("applications should not expose any fields"), so Microsoft backs the Rule at its weakest. The Google guide allows documented exceptions in "rare cases".

Not counted: Rust Book ch20-01 ("If two threads are accessing the same mutable global variable, it can cause a data race") states a hazard, not a practice. 12factor (Heroku) "processes are stateless and share-nothing" is process-level, not module-level. Google Go guide is the same org as Google.

New tools/orgs.py row: prefix `github.com/uber-go/` -> `uber` (Uber). Microsoft and Google URLs already map.

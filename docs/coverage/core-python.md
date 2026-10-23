# Coverage: Python guide to cards

Source: the author's Python code review guide. Each rule heading maps to a card id, or to an explicit out-of-scope note (cards owned by other tasks).

| Guide section | Rule | Card |
|---|---|---|
| How I review | Ledger: PASS/FAIL/N/A with evidence | out of scope (change-level cards) |
| What the tools own | Linter owns what it can decide; add the gate | py-ruff-gate |
| Architecture | Three layers named by what they do; dependencies point inward | mod-layers-point-inward |
| Architecture | Entry module stays thin | mod-thin-entry-point |
| Architecture | No helpers.py / utils.py | mod-no-utils-grab-bag |
| Architecture | Large literals in their own module; one cohesive unit; single-module folder inlined | mod-cohesive-unit |
| Architecture | `__init__.py` empty except at a public boundary | py-init-py-empty |
| Architecture | I/O at the edges; import touches nothing | mod-no-import-side-effects |
| Architecture | YAGNI | mod-yagni |
| Architecture | No pass-through wrappers | fn-no-pass-through-wrapper |
| Architecture | Behaviour lives with the state it owns | mod-behaviour-lives-with-state |
| Config and typing | Env config through pydantic-settings | py-settings-pydantic-settings |
| Config and typing | Config values live in the settings module | mod-central-config |
| Config and typing | No `cast()` | py-no-cast |
| Config and typing | Fixed key set gets a type | fn-known-keys-get-a-type |
| Config and typing | No stringly-typed returns | fn-no-stringly-typed-returns, py-strenum-not-strings |
| Config and typing | `X \| None`, builtin generics, strict typing | py-modern-typing |
| Config and typing | `Field()` only when it adds something | py-field-only-when-adds |
| Imports | Top of module, absolute, no `_` names, `__all__` only in re-export | py-imports |
| State and `__init__` | No module-level mutable state | mod-no-module-mutable-state |
| State and `__init__` | No logic in `__init__` | mod-no-logic-in-constructors, py-init-assign-only |
| State and `__init__` | Inject boundary collaborators | mod-inject-boundary-collaborators |
| Naming and classes | Semantics and consistency; one name per concept; glossary wins; no borrowed terms | mod-one-name-per-concept |
| Naming and classes | Name intermediate conditions | fn-name-intermediate-conditions |
| Naming and classes | Bool argument at call site | fn-bool-arg-at-callsite |
| Naming and classes | Code explains itself; rename before commenting | fn-comments-explain-why |
| Naming and classes | English everywhere | gap: no card |
| Naming and classes | No codenames or ticket numbers in code | fn-comments-survive-context |
| Naming and classes | A class earns its instance; Protocol needs two implementations | py-class-earns-its-instance |
| Naming and classes | Field names over indexes; no getattr/setattr | fn-no-getattr-for-known-names |
| Naming and classes | No anonymous tuples | fn-no-anonymous-tuples, py-frozen-dataclass-over-tuple |
| Naming and classes | List-returning functions return `[]` | fn-empty-collection-not-none |
| Naming and classes | No magic strings or numbers | fn-no-magic-values, py-strenum-not-strings |
| Validation | Pydantic models, validate at the boundary once, snake_case with alias | mod-validate-at-boundary-once, py-pydantic-validation |
| Error handling | Specific exceptions only | fn-specific-exceptions-only |
| Error handling | Propagate, translate with `from` | fn-propagate-dont-swallow |
| Error handling | Base exception per package, errors module | py-error-hierarchy |
| Error handling | Retry only transient failures on idempotent operations | out of scope (service-level cards) |
| Error handling | Error responses don't leak internals | out of scope (service-level cards) |
| Error handling | Log the branches that matter with a request ID | out of scope (service-level cards) |
| Security | Validate every input; name new attack surface; secrets from settings | out of scope (service-level cards) |
| Docstrings and comments | Comments explain why | fn-comments-explain-why |
| Docstrings and comments | Comments survive loss of context | fn-comments-survive-context |
| Docstrings and comments | No forced docstrings, Google style | py-docstrings-google |
| Docstrings and comments | No section banners | mod-cohesive-unit |
| Docstrings and comments | Check every stated reason against the artifact | fn-comments-explain-why (Counterpoint) |
| Docstrings and comments | Empty `__init__.py` means empty | py-init-py-empty |
| Testing | `parametrize` for variations | py-pytest-parametrize |
| Testing | No `test_init_*` or plain-model tests | py-no-init-or-model-tests |
| Testing | Whole-object assertions; mock at the boundary; fake has real signature | mod-mock-at-boundaries-only |
| Testing | No Arrange/Act/Assert comments; deterministic; layout mirrors source; fixtures; regression test first | py-test-hygiene |
| Concurrency | No check-then-act across `await`; atomic operations | fn-no-check-then-act-across-await, py-await-check-then-act |
| Concurrency | Shared state reasoned about for races | out of scope (change-level cards) |
| Resource lifecycle | Per-key caches bounded | mod-bounded-caches |
| Resource lifecycle | Pooled clients built once | mod-pooled-clients-built-once, py-httpx-client-lifespan |
| Resource lifecycle | Timeouts on both legs | svc-timeouts, py-httpx-client-lifespan |
| Resource lifecycle | Stream, don't materialise; bound background tasks | gap: no card |
| Change discipline | Never silence a diagnostic | py-no-silenced-diagnostics |
| Change discipline | No paths relative to the working directory | py-paths-from-file |
| Change discipline | Verify before claiming; delete workarounds; stay in scope; Chesterton; measure | out of scope (change-level cards) |
| Writing the review | Severity labels, one comment per finding, design first | out of scope (change-level cards) |
| Critical rules | Bookmark table | severity `block` on the cards above |
| Additions beyond the guide | Deep modules | mod-deep-modules |
| Additions beyond the guide | Wrong abstraction | mod-no-wrong-abstraction |
| Additions beyond the guide | Fowler smells | mod-fowler-smells |

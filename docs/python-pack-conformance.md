# Python pack conformance

How this repository's own Python (`tools/`, `test/`) meets each card in `packs/python/`. `ruff check tools test`, `mypy`, and `pytest` run these gates in CI. Code under `test/evals/cases/` is planted-defect input for the evals and is excluded.

| Card | Status | Evidence |
|---|---|---|
| py-await-check-then-act | N/A | No asyncio code. |
| py-cancellation | N/A | No asyncio code. |
| py-class-earns-its-instance | PASS | No static-only class and no `Protocol`; every class holds state: `tools/models.py:74`, `tools/agent_ready_check.py:32`. |
| py-docstrings-google | PASS | Ruff `D` with the Google convention checks format; `D1xx` is ignored, so presence is never forced (`pyproject.toml:19-29`). |
| py-error-hierarchy | PASS | One base, `ToolError`, with `BuildError` and `HarnessError` in `tools/errors.py:4-12`; nothing raises a bare `Exception`. |
| py-field-only-when-adds | N/A | No pydantic. The one `dataclasses.field` sets a `default_factory` (`tools/agent_ready_check.py`, `Report.failures`). |
| py-frozen-dataclass-over-tuple | PASS | Records are `@dataclass(frozen=True, slots=True)`: `tools/models.py:74-135` (`RawCard`, `Card`, `PageSpec`, `Twin`, `IndexPart`, ...), `tools/schema.py:22`. `parse_front`, `orgs.split`, `eval.command`, and `parse_headers` return named records, not tuples. |
| py-httpx-client-lifespan | N/A | No `httpx` and no network code. |
| py-imports | PASS | Absolute imports at module top; no relative import (`TID252` via `ban-relative-imports`, `pyproject.toml:32`); no `_`-prefixed import across modules; no `__all__`. Tests find `tools/` through `pythonpath` (`pyproject.toml:40`), not `sys.path.insert`. |
| py-init-assign-only | PASS | No `__post_init__`. `Page.__init__` only assigns; parsing moved to `Page.parse` (`tools/agent_ready_check.py:64`). |
| py-init-py-empty | PASS | There is no `__init__.py`; `tools/` is a script directory. |
| py-modern-typing | PASS | `X | None` and builtin generics only (Ruff `UP`); `mypy --strict` gates `tools/` (`pyproject.toml:35`). `typing` supplies only `Any`, `Literal`, `get_args`, `get_origin`, `get_type_hints`. A second checker (pyright) is not run: one hard gate is the card's minimum. |
| py-no-cast | PASS | No `cast()` in `tools/` or `test/`. |
| py-no-init-or-model-tests | PASS | No test asserts that an `__init__` or a plain dataclass stores its fields; tests exercise behaviour (`test/test_build.py`, `test/test_schema.py`). |
| py-no-silenced-diagnostics | PASS | No `# noqa` and no `# type: ignore` in `tools/` or `test/`; the old `sys.path.insert` + `# noqa: E402` pairs are gone. |
| py-paths-from-file | PASS | Every path derives from `__file__` (`tools/config.py:4`, `tools/orgs.py:122`); `validate.py` no longer defaults `--root` to the working directory. |
| py-pydantic-validation | N/A | The build is standard-library only (`docs/deploy.md`); `tools/validate.py` parses card front matter by hand. |
| py-pytest-parametrize | PASS | Tests that differ only in inputs are parametrized: `test/test_orgs.py` (`test_org_of`, `test_a_stable_card_below_the_floor_fails`), `test/test_eval.py` (`test_triggered`, `test_scoped_review_may_not_cite_other_concerns`), `test/test_build.py` (`test_check_md_flags_unsupported_markdown`). Each list is a literal, never computed, so an empty parametrization cannot hide. |
| py-ruff-gate | PASS | `pyproject.toml:19-32` selects E, F, I, B, UP, SIM, BLE, TID, D, ignores D100-D107, sets the Google convention and bans relative imports. Two reasoned per-file `E501` ignores cover prose and tables (`tools/prose.py`, `tools/assets.py`, `tools/orgs.py`). |
| py-settings-pydantic-settings | N/A | The build reads no environment variables. |
| py-strenum-not-strings | PASS | `StrEnum` for level, severity, status, context, concern, lacks reason (`tools/models.py:8-55`), the schema kind (`tools/schema.py:17`), and the eval mode, agent, and split (`tools/eval.py:62-74`). No HTTP status codes in the code. |
| py-task-reference | N/A | No asyncio code. |
| py-test-hygiene | PASS | Network blocked in every test with `--disable-socket` (`pyproject.toml:42`, `pytest-socket`); the clock is frozen with `freezegun` where code reads it (`test/test_build.py:62`). |

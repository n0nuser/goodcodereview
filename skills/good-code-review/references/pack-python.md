# Python pack

A draft card is not vetted. Report a `FAIL` of one under Draft findings, at `should-fix` at most, never in the ledger or the verdict.

## py-await-check-then-act

level: function  
severity: should-fix  
concerns: correctness  
applies_when: An `async def` reads state, awaits, then writes based on that read.  
lacks: held, cites the draft card(s) fn-no-check-then-act-across-await; stable once those are stable

When more than one worker or process can run, make check-then-act an atomic DB statement or constraint, because a Python lock covers one process only.

## py-cancellation

level: service  
severity: should-fix  
concerns: reliability, correctness  
applies_when: Async code catches exceptions around awaits or uses asyncio.timeout.  
lacks: 

Re-raise `CancelledError` (do not catch it via bare `except` or `BaseException`), and catch `TimeoutError` outside the `asyncio.timeout()` block.

## py-class-earns-its-instance

level: module  
severity: discuss  
concerns: maintainability  
applies_when: A Python class has no state, only static methods, or a `Protocol` with one implementation.  
lacks: 

Give a class real state or a collaborator; otherwise write a module function.

## py-docstrings-google

level: function  
severity: discuss  
concerns: maintainability  
applies_when: A Python function or class has, or lacks, a docstring.  
lacks: 

Write a Google-style docstring only when it adds what the signature cannot say.

## py-error-hierarchy

level: module  
severity: should-fix  
concerns: correctness  
applies_when: A Python package raises its own exceptions.  
lacks: held, cites the draft card(s) fn-propagate-dont-swallow; stable once those are stable

Give each package one base exception, with the specific ones in an `errors` module.

## py-field-only-when-adds

level: module  
severity: discuss  
concerns: correctness  
applies_when: A pydantic model or settings class uses `Field()`.  
lacks: 

Use `Field()` only when it adds something (a constraint, an alias, or API docs), and set plain defaults directly.

## py-frozen-dataclass-over-tuple

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A Python function returns a tuple whose positions differ in meaning.  
lacks: held, cites the draft card(s) fn-no-anonymous-tuples; stable once those are stable

Return a `@dataclass(frozen=True, slots=True)` instead of a positional tuple.

## py-httpx-client-lifespan

level: module  
severity: should-fix  
concerns: performance  
applies_when: A Python service creates an `httpx` client.  
lacks: 

Pass an explicit `httpx.Timeout` to every `httpx` client.

## py-imports

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: A Python module has imports.  
lacks: 

Put imports at module top, absolute only.

## py-init-assign-only

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: A Python class defines `__init__` or `__post_init__`.  
lacks: held, cites the draft card(s) mod-no-logic-in-constructors; stable once those are stable

Keep `__init__` and `__post_init__` to assignments, and do I/O in a `@classmethod` factory.

## py-init-py-empty

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: The change adds or edits an `__init__.py`.  
lacks: held, cites the draft card(s) mod-no-import-side-effects; stable once those are stable

Keep `__init__.py` empty unless it re-exports the public API.

## py-modern-typing

level: function  
severity: should-fix  
concerns: correctness  
applies_when: Annotations use `typing` aliases, or the type gate is missing.  
lacks: 

Write `X | None` and builtin generics, not `typing` aliases.

## py-no-cast

level: function  
severity: should-fix  
concerns: correctness  
applies_when: Code calls `typing.cast(...)`.  
lacks: 

Do not use `cast()`; parse the boundary into a typed model, or narrow with `isinstance`.

## py-no-init-or-model-tests

level: module  
severity: should-fix  
concerns: testing  
applies_when: The diff adds `test_init_*` or a test file for a plain model or dataclass.  
lacks: 

Cover `__init__` and plain models through the behaviour that uses them.

## py-no-silenced-diagnostics

level: change  
severity: should-fix  
concerns: maintainability  
applies_when: A diff adds `# noqa` or `# type: ignore`.  
lacks: held, cites the draft card(s) chg-no-silenced-diagnostics; stable once those are stable

Suppress a Python diagnostic only with a single named code and a reason on the same line.

## py-paths-from-file

level: function  
severity: should-fix  
concerns: correctness  
applies_when: Python code builds a path to a data file or fixture.  
lacks: 

Resolve paths from `__file__`, not the current working directory.

## py-pydantic-validation

level: module  
severity: should-fix  
concerns: correctness  
applies_when: A Python function validates request or config data by hand.  
lacks: held, cites the draft card(s) mod-validate-at-boundary-once; stable once those are stable

Validate request data with a pydantic model, not hand-written checks.

## py-pytest-parametrize

level: function  
severity: should-fix  
concerns: testing  
applies_when: Tests differ only in inputs and expected values.  
lacks: 

Write tests that differ only in inputs and expected values as one `@pytest.mark.parametrize` test.

## py-ruff-gate

level: change  
severity: should-fix  
concerns: maintainability  
applies_when: The project is Python and has a linter configuration.  
lacks: 

Enable the Ruff rule sets E, F, I, B, UP, SIM, BLE, TID and D in CI.

## py-settings-pydantic-settings

level: module  
severity: should-fix  
concerns: maintainability  
applies_when: Python code reads configuration from the environment.  
lacks: held, cites the draft card(s) mod-central-config; stable once those are stable

Load env config with `BaseSettings` from `pydantic_settings`.

## py-strenum-not-strings

level: function  
severity: should-fix  
concerns: correctness  
applies_when: Python code compares against string or number literals for a fixed set of values.  
lacks: held, cites the draft card(s) fn-no-magic-values, fn-no-stringly-typed-returns; stable once those are stable

Use `StrEnum` for fixed string sets and `HTTPStatus` for HTTP codes.

## py-task-reference

level: service  
severity: should-fix  
concerns: correctness  
applies_when: Python code calls asyncio.create_task or ensure_future.  
lacks: 

Never discard the result of `create_task`; keep a reference and surface its exceptions, preferably through a `TaskGroup`.

## py-test-hygiene

level: module  
severity: discuss  
concerns: testing  
applies_when: A Python test uses the current date or time, or reaches the network.  
lacks: 

Freeze time and block network in tests.

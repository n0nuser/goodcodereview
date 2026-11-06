# Python pack

Draft cards only; the stable Python cards are in the level files. A draft card is not vetted. Report a `FAIL` of one under Draft findings, at `should-fix` at most, never in the ledger or the verdict.

## py-await-check-then-act

level: function  
severity: should-fix  
concerns: correctness  
applies_when: An `async def` reads state, awaits, then writes based on that read.  
lacks: held, cites the draft card(s) fn-no-check-then-act-across-await; stable once those are stable

When more than one worker or process can run, make check-then-act an atomic DB statement or constraint, because a Python lock covers one process only.

## py-error-hierarchy

level: module  
severity: should-fix  
concerns: correctness  
applies_when: A Python package raises its own exceptions.  
lacks: held, cites the draft card(s) fn-propagate-dont-swallow; stable once those are stable

Give each package one base exception, with the specific ones in an `errors` module.

## py-frozen-dataclass-over-tuple

level: function  
severity: should-fix  
concerns: correctness  
applies_when: A Python function returns a tuple whose positions differ in meaning.  
lacks: held, cites the draft card(s) fn-no-anonymous-tuples; stable once those are stable

Return a `@dataclass(frozen=True, slots=True)` instead of a positional tuple.

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

## py-no-silenced-diagnostics

level: change  
severity: should-fix  
concerns: maintainability  
applies_when: A diff adds `# noqa` or `# type: ignore`.  
lacks: held, cites the draft card(s) chg-no-silenced-diagnostics; stable once those are stable

Suppress a Python diagnostic only with a single named code and a reason on the same line.

## py-pydantic-validation

level: module  
severity: should-fix  
concerns: correctness  
applies_when: A Python function validates request or config data by hand.  
lacks: held, cites the draft card(s) mod-validate-at-boundary-once; stable once those are stable

Validate request data with a pydantic model, not hand-written checks.

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

## py-test-collection-and-imports

level: module  
severity: discuss  
concerns: testing, performance  
applies_when: A pytest run spends seconds collecting tests or importing modules before the first test starts.  
lacks: orgs, "set testpaths" has Trail of Bits; the pytest page only defines the option; needs two more orgs that recommend it

Set `testpaths` in the pytest configuration.

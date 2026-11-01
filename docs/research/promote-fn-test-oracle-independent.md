# Promote fn-test-oracle-independent

Quotes were read on the live pages (2026-11-01). Clause A: expected value comes from the requirement. Clause B: pair every "not called" assertion with a case where the call happens.

## Google: Software Engineering at Google, chapter 12 (clause A)

https://abseil.io/resources/swe-book/html/ch12.html

- "When the whole string is written out, we can see right away that we're expecting two slashes in the URL instead of just one. If the production code made a similar mistake, this test would fail to detect a bug."
- "in test code, stick to straight-line code over clever logic, and consider tolerating some duplication when it makes the test more descriptive and meaningful."
- Nothing on "not called" assertions (clause B).

## Microsoft Learn: unit testing best practices for .NET (clause A, loose)

https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices

- "avoid manual string concatenation, logical conditions, such as `if`, `while`, `for`, and `switch`, and other conditions. If you include logic in your test suite, the chance of introducing bugs increases dramatically."
- The page's FAIL example computes `expected += 3` in a loop; the fix uses literal `[InlineData("1,2,3", 6)]`. It is about logic in tests, not strictly "expected from the requirement", so a reviewer may rate it weaker.
- Nothing on "not called" assertions.

## Cursor: pstack principle-test-behavior-not-implementation (clauses A and B, already cited)

## Not counted

- Clause B search found only framework API docs (Sinon, MATLAB, Mockito never()) and a Telerik bug report: none states the pairing practice. Error Prone MockitoUsage (Google) is about misplaced verify, not pairing.
- Microsoft team blog "Team dojo 12": a personal blog on an MS host, discusses tradeoff, not a rule.

## Verdict

Clause A: Google, Microsoft (weaker), Cursor = 3. Clause B: Cursor only. Card narrowed to clause A; clause B moved into the Why. `chg-agent-mock-asserting-tests` is still draft, so its link was dropped.

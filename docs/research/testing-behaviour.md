# Testing: assert behaviour, not implementation

Backs `fn-test-behaviour-not-implementation`. Quotes were read on the live pages.

## Google: Software Engineering at Google, chapter 12

https://abseil.io/resources/swe-book/html/ch12.html

- "There's a better way: rather than writing a test for each method, write a test for each behavior."
- "As just defined, a brittle test is one that fails in the face of an unrelated change to production code that does not introduce any real bugs."

## Microsoft Learn: unit testing best practices for .NET

https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices

- "The minimalist approach helps tests become more resilient to future changes in the codebase and focus on verifying the behavior over the implementation."
- "Private methods are an implementation detail and never exist in isolation."

## Spotify engineering: testing of microservices

https://engineering.atspotify.com/2018/01/11/testing-of-microservices

- "Now we are able to refactor the internals without touching any tests."
- Too many unit tests "also restricts how we can change the code without also having to change the tests."
- Spotify still keeps tests of implementation details for isolated, complex logic. The card's counterpoint covers this.

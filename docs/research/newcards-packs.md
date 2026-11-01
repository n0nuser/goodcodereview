# New cards: Go and TypeScript packs

Quotes read on the live pages (curl, tags stripped) on 2026-11-01. All cards are drafts.

## Go

- Google (Go team). https://go.dev/blog/govulncheck. "we know that many developers will want to run govulncheck as part of their CI/CD systems." Backs go-govulncheck-in-ci (govulncheck in CI).
- Uber. https://github.com/uber-go/guide/blob/master/style.md. "We recommend using the following linters at a minimum" (errcheck, goimports, revive, govet, staticcheck); "lint consistently across a codebase". Backs go-vet-lint-gate. Same page: "Avoid `init()` where possible" and "Avoid I/O, including both filesystem, network, and system calls." Backs go-no-init-side-effects. Same page: "Use `%w` if the caller should have access to the underlying error. This is a good default for most wrapped errors". Backs go-wrap-errors-with-w.
- Google (Go team). https://go.dev/doc/articles/race_detector. "To start, run your tests using the race detector ( go test -race )." Backs go-test-race-in-ci.
- Google (Go team). https://go.dev/ref/mod. "-mod=readonly tells the go command to ignore the vendor directory and to report an error if go.mod needs to be updated." and "go mod verify checks that dependencies of the main module stored in the module cache have not been modified since they were downloaded." Backs go-mod-readonly-verified (readonly, verify).
- Google (Go team). https://go.dev/blog/supply-chain. "It contains a list of cryptographic hashes of each dependency that contributes to the build. Again, an incomplete go.sum causes an error". Backs go.sum committed.
- Google (Go team). https://go.dev/blog/go1.13-errors. "Wrapping an error with %w makes it available to errors.Is and errors.As". Backs go-wrap-errors-with-w. The "check every err" clause rests on Uber's errcheck line ("to ensure that errors are handled") only.
- Cloudflare. https://blog.cloudflare.com/the-complete-guide-to-golang-net-http-timeouts/. "timeouts are amongst the easiest and most subtle things to get wrong" and "Client-side timeouts ... are just as important to prevent leaking resources or getting stuck." Backs go-http-client-timeout.
- Google (Go team). https://pkg.go.dev/net/http. "A Timeout of zero means no timeout." Backs go-http-client-timeout (zero timeout is none).

Gaps: no source found for "deferred Close error on writes not dropped"; card dropped. Google Go style guide pages were fetched but state nothing for these rules beyond context handling, so they are not cited.

## TypeScript / Vitest

- Microsoft. https://www.typescriptlang.org/tsconfig/. "The strict flag enables a wide range of type checking behavior that results in stronger guarantees of program correctness." Backs typescript-strict-mode.
- typescript-eslint. https://typescript-eslint.io/rules/no-floating-promises/. "A "floating" Promise is one that is created without any code set up to handle any errors it might throw." Backs typescript-no-floating-promises.
- Vitest. https://vitest.dev/guide/mocking/requests. "We recommend Mock Service Worker to accomplish this." (network mocking). Backs the boundary-fake clause of typescript-mock-at-the-boundary.
- Testing Library. https://testing-library.com/docs/guiding-principles/. "The more your tests resemble the way your software is used, the more confidence they can give you." Backs the same card.
- Vitest. https://vitest.dev/guide/mocking/modules. "The factory method accepts an importOriginal function that will execute the original module and return its module object". Backs typescript-partial-mock-keeps-original. The instanceof consequence is the author's inference, not a quoted statement.
- Vitest. https://vitest.dev/config/setupfiles. "Paths to setup files resolved relative to the root . They will run before each test file in the same process." Backs typescript-shared-test-setup.

Dropped: locale parity test (no source; project specific).

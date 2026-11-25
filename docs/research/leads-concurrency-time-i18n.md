# Leads: concurrency, async, time and i18n

Method: pages fetched 2026-11-24 with `curl -sL`, tags stripped with `python3 -I`, sentence found with `rg` in the stripped text. Quotes are 25 words or fewer. Org grouping follows docs/PROMOTION.md (Google covers Go, Android, AIP; Microsoft covers Learn; Mozilla covers MDN and Fluent). Fetch count was about 95, over the 60 target, because most pages were JS-free reference docs fetched in batches; several returned nothing useful (Kotlin docs, Apple docs, GNU gettext, Microsoft globalization pages, Sonar: JS shells or 404, not counted).

Existing-card check (`rg` over cards/): no card on time zones, UTC, clocks, locale, Unicode, i18n or plurals. `monotonic` appears only incidentally in `sys-lock-fencing` and `svc-client-paces-outgoing-calls`. Concurrency neighbours: `fn-resource-lifetime` (draft, lacks orgs), `svc-bounded-background-tasks`, `fn-no-check-then-act-across-await`, `fn-no-blocking-call-in-async-code`, `svc-timeouts`, `sys-fanout-leg-deadlines`, `mod-single-writer-per-state`, `mod-inject-boundary-collaborators` (clock injection).

## Ranking

| # | Rule | Orgs | Verdict |
|---|---|---|---|
| 1 | Measure elapsed time and timeouts with a monotonic clock, not the wall clock | 4 (Google, Oracle, Mozilla, Python; Rust soft) | clears 3, new card |
| 2 | Store and exchange instants in UTC; convert to local time only for display | 3 firm (W3C, Django, Zalando) + 2 soft (PostgreSQL wiki, Google AIP-142) | clears 3, new card |
| 3 | Every spawned task or goroutine has a stop signal and an owner that waits for it | 3 (Google, Uber, Python) | clears 3; feeds draft `fn-resource-lifetime` |
| 4 | Long-running work takes a cancellation signal and honours it; do not swallow cancellation | 3 (Google, Microsoft, Python) | clears 3 with caveat, new card |
| 5 | Case-convert, format and parse machine strings with an explicit locale (ROOT or invariant) | 3 (Oracle, Google/Android, Microsoft) | clears 3, new card |
| 6 | Do not hold a sync lock across an `await` | 1 (Tokio) | short |
| 7 | User-facing strings live in resource files, not code | 2 (Android, Microsoft) | short |
| 8 | Plural text comes from plural-category messages, not `n == 1` | 2 (Mozilla, Android; ICU descriptive) | short |
| 9 | Do not concatenate translated fragments | 1 (Mozilla) | short |
| 10 | Future local events store the zone ID, not an offset | 1 firm (W3C), Zalando partial | short |

## 1. Monotonic clock for durations

Rule candidate: "Measure elapsed time and timeout deadlines with a monotonic clock, never by subtracting wall-clock readings." FAIL: `time.time() - start` or `System.currentTimeMillis()` used to time an operation or compute a timeout. Nearest card: none. New card.

1. https://pkg.go.dev/time . Google (Go). "the wall clock is for telling time and the monotonic clock is for measuring time."
2. https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/System.html . Oracle. nanoTime: "This method can only be used to measure elapsed time and is not related to any other notion of system or wall-clock time."
3. https://developer.android.com/reference/android/os/SystemClock . Google (Android, same org as 1). The wall clock "may jump backwards or forwards unpredictably"; "Interval or elapsed time measurements should use a different clock."
4. https://developer.mozilla.org/en-US/docs/Web/API/Performance/now . Mozilla. "Date.now() may have been impacted by system and user clock adjustments, clock skew"; performance.now is monotonic "isn't subject to adjustments."
5. https://docs.python.org/3/library/time.html . Python. time.monotonic is "a clock that cannot go backwards. The clock is not affected by system clock updates." Descriptive: it does not say to prefer it, so Python is soft.
6. https://doc.rust-lang.org/std/time/struct.Instant.html . Rust. Instants are "often useful for tasks such as measuring benchmarks or timing how long an operation takes." Descriptive, soft.
7. Also https://man7.org/linux/man-pages/man3/clock_gettime.3.html . Linux man-pages: CLOCK_REALTIME "is affected by discontinuous jumps in the system time"; CLOCK_MONOTONIC "is not." Descriptive.

Count: Google, Oracle, Mozilla = 3 firm; Python and Rust soft. Scope: elapsed time and timeouts inside one process. Across restarts or hosts, monotonic readings are meaningless (Java note: values only meaningful within one JVM), so persisted or cross-host deadlines still use wall time (see `sys-lock-fencing`). Counterpoint: Go's `time.Now()` carries both readings, so Go code that subtracts two `Time` values is already safe; the card needs a language note. Draft id: `fn-monotonic-clock-for-durations`.

## 2. Store and exchange instants in UTC

Rule candidate: "Store, log and send instants as UTC (or an unambiguous offset form such as RFC 3339 `Z`); convert to a local zone only at display." FAIL: a naive `timestamp` column or `datetime.now()` stored without zone; local-time strings in an API body. Nearest card: none. New card.

1. https://www.w3.org/TR/timezone/ . W3C. "Whenever possible, use UTC or choose a consistent time zone when creating time-based content or data value so that values from discrete sources can be compared more readily."
2. https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/ . Django (DSF). "it's still good practice to store data in UTC in your database"; "use UTC in the code and use local time only when interacting with end users."
3. https://opensource.zalando.com/restful-api-guidelines/ . Zalando. "we recommend storing all dates consistently in UTC without offset."
4. Soft: https://wiki.postgresql.org/wiki/Don%27t_Do_This . PostgreSQL community wiki. "Don't use the timestamp type to store timestamps, use timestamptz" (timestamptz stores a point in time in UTC). Rule is about the column type, not UTC text; partial.
5. Soft: https://google.aip.dev/142 . Google. Fields "that represent an absolute point in time (independent of any time zone or calendar) should use the google.protobuf.Timestamp type." Same idea, one step removed.

Count: W3C, Django, Zalando = 3 firm; PostgreSQL, Google soft. Counterpoints: (a) future local events (a 09:00 meeting in Madrid) must keep the zone, since zone rules change (W3C 4.2.2); (b) calendar dates (birthdays, holidays) are not instants (W3C 4.2.4). The card scopes to instants. Draft id: `fn-timestamps-utc-at-rest`.

## 3. Every task has a stop signal and an owner that waits

Rule candidate: "Every goroutine, thread or task started has a way to be told to stop and an owner that waits for it; no fire-and-forget." FAIL: `go func() { for { ... } }()` with no stop channel or context and no WaitGroup; `asyncio.create_task(x)` with the result dropped. Nearest card: `fn-resource-lifetime` (draft, `lacks: orgs`, one source: a person's blog). This lead gives it its three. Clause on the existing card, not new.

1. https://google.github.io/styleguide/go/decisions . Google (Go style). "When you spawn goroutines, make it clear when or whether they exit."; leaving them in flight "can cause other subtle and hard-to-diagnose problems."
2. https://raw.githubusercontent.com/uber-go/guide/master/style.md . Uber. Heading "Don't fire-and-forget goroutines": "every goroutine must have a predictable time at which it will stop running; or there must be a way to signal to the goroutine that it should stop", and code must be able to "block and wait for the goroutine to finish."
3. https://docs.python.org/3/library/asyncio-task.html . Python. "Save a reference to the result of this function, to avoid a task disappearing mid-execution"; use `asyncio.TaskGroup`, which "keeps a strong reference to each task, awaits them and propagates their exceptions."
4. https://go.dev/blog/context . Google (same org as 1). "When a request is canceled or times out, all the goroutines working on that request should exit quickly." Supports the stop signal only.

Count: Google, Uber, Python = 3. Python's text is about task loss and exceptions, a neighbouring but not identical claim (owner holds the task); mark Python as the weakest. Counterpoint: process-lifetime daemons (a metrics loop) legitimately run until exit; the card needs the "stops at process exit, documented" exception. Add to `fn-resource-lifetime` `borrowed_from`: the three URLs above.

## 4. Long-running work honours cancellation

Rule candidate: "A long-running loop or call takes a cancellation signal (context, token) and checks it between steps; catching a cancellation exception must re-raise it." FAIL: a worker loop with no `ctx.Done()` or token check; `except asyncio.CancelledError: pass`. Nearest cards: `svc-timeouts` and `sys-fanout-leg-deadlines` set deadlines on the caller; neither says the callee must observe cancellation. New card or clause on `svc-timeouts`.

1. https://go.dev/blog/context . Google. "all the goroutines working on that request should exit quickly so the system can reclaim any resources they are using."
2. https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads . Microsoft. "the cancellation request means that the operation should stop as soon as possible after any required cleanup is performed"; for loops, poll `IsCancellationRequested` and "clean up and terminate as quickly as possible."
3. https://docs.python.org/3/library/asyncio-task.html . Python. "In case asyncio.CancelledError is explicitly caught, it should generally be propagated when clean-up is complete."; components "might misbehave if a coroutine swallows asyncio.CancelledError."

Count: Google, Microsoft, Python = 3. Not found: Kotlin docs (JS shell, nothing matched). Caveat: the three state different halves (honour the signal; do not swallow it), so the Rule should be written as one clause per half and each re-counted. Counterpoint: uninterruptible critical sections (commit, write-ahead) must finish; Microsoft says "after any required cleanup." Draft id: `fn-honour-cancellation`.

## 5. Explicit locale for machine strings

Rule candidate: "When code lower-cases, upper-cases, formats or parses a string that is not human text (identifiers, headers, protocol keys, persisted numbers), pass an explicit locale (`Locale.ROOT`, invariant culture)." FAIL: `name.toLowerCase()` to normalise an HTTP header; `String.format("%.2f", x)` written to a file. Nearest card: none. New card.

1. https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/String.html . Oracle. toLowerCase "is locale sensitive, and may produce unexpected results if used for strings that are intended to be interpreted locale independently"; "use toLowerCase(Locale.ROOT)."
2. https://developer.android.com/reference/java/util/Locale . Google (Android). "You should also be wary of the String.toLowerCase and String.toUpperCase overloads that don't take a Locale"; Turkish behaviour is "inappropriate for, say, HTTP headers." The same page warns that locale-formatted numbers "likely cause problems if presented to another computer."
3. https://learn.microsoft.com/en-us/dotnet/standard/base-types/best-practices-strings . Microsoft. "Use formatting with the invariant culture to persist non-string data in string form"; "Use StringComparison.Ordinal or StringComparison.OrdinalIgnoreCase ... for culture-agnostic string matching."

Count: Oracle, Google, Microsoft = 3. Not counted: Sonar RSPEC-4790 (JS shell), Rust (`to_lowercase` is locale independent by design, so no rule needed). Scope: Java, Kotlin, C#, and other runtimes with a default-locale API; N/A in languages where the call is locale-free. `tool_gate` candidates exist (Error Prone `StringCaseLocaleUsage`, CA1304/CA1311), not yet confirmed; open the rule pages before naming one. Draft id: `fn-explicit-locale-machine-strings`.

## Short leads (not enough yet)

6. Do not hold a sync lock across an `await`. https://tokio.rs/tokio/tutorial/shared-state (Tokio): "using a synchronous mutex from within asynchronous code is fine as long as contention remains low and the lock is not held across calls to .await." One org. Not searched further (fetch budget). Next try: Microsoft CS1996 (`await` inside `lock`), Python asyncio sync-primitives page, Rust async book, Java virtual-thread pinning guidance. Nearest: `fn-no-blocking-call-in-async-code`; likely a clause there.
7. User-facing strings out of code. https://developer.android.com/guide/topics/resources/localization : "don't hardcode any strings. Instead, declare all your strings as resources." https://learn.microsoft.com/en-us/dotnet/core/extensions/localization : UI block "contains only localizable user-interface elements such as strings, error messages". Two orgs. Mozilla Fluent is built on this but I did not find a sentence that states it. Also a UI-only context card.
8. Plurals from plural categories. https://developer.android.com/guide/topics/resources/string-resource : "Different languages have different rules for grammatical agreement with quantity ... zero, one, two, few, many, and other." https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/PluralRules (Mozilla): English has two forms while others have up to six. https://firefox-source-docs.mozilla.org/l10n/fluent/tutorial.html (Mozilla, same org): plural rules from CLDR. ICU message docs show `plural` selectors but state no rule. Two orgs plus descriptive ICU. Next try: Apple stringsdict docs (JS shell), Rails/Django i18n guides, GNU gettext (ngettext) manual, W3C i18n.
9. No concatenation of translated fragments. https://firefox-source-docs.mozilla.org/l10n/fluent/tutorial.html : "no concatenations, replacements or splitting should happen after the translation is completed." One org. Next try: GNU gettext manual, Android, Apple, W3C i18n articles.
10. Future local events keep the zone ID. https://www.w3.org/TR/timezone/ 4.2.2: "you will need the time zone (and not merely the local time offset) to ensure proper time computation." Zalando lists an IANA zone-id format but states no rule. One org. Next try: Google Calendar API (`timeZone`), Microsoft DateTimeOffset docs, Java ZonedDateTime javadoc, Temporal docs (TC39 page fetched states concepts, not a rule).

## Skipped

- Clock injection for tests: Microsoft TimeProvider page (https://learn.microsoft.com/en-us/dotnet/standard/datetime/) states it, but `mod-inject-boundary-collaborators` already covers collaborators. Candidate for a `borrowed_from` addition there only if that card does not already name a clock; not checked.
- Go `sync.Mutex` must not be copied: one org (Google style); `go vet` copylocks covers it.
- Document goroutine exit conditions: Google only; folded into lead 3.
- Money as decimal or minor units, ISO 8601 in APIs beyond Zalando: not searched.

## Sources added by the card writer (re-fetched raw, sentence matched)

Cited by `fn-honour-cancellation`:

- https://docs.oracle.com/javase/tutorial/essential/concurrency/interrupt.html
- https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/coroutines-cancellation.md
- https://developer.android.com/kotlin/coroutines/coroutines-best-practices

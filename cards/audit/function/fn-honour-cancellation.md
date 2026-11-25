---
id: fn-honour-cancellation
level: function
tags: [reliability, correctness, concurrency]
severity: should-fix
status: stable
lang: core
applies_when: The code runs a long-lived loop, a background task or request-scoped work in a language with a cancellation mechanism (context, token, interrupt, coroutine or asyncio task).
tool_gate: none
note: Each clause has its own organisations. Check the signal between steps - Google (Go), Microsoft (.NET), Oracle (Java) and JetBrains (Kotlin). Re-raise a caught cancellation - Python, Google (Android Kotlin) and JetBrains
borrowed_from:
  - https://go.dev/blog/context
  - https://learn.microsoft.com/en-us/dotnet/standard/threading/cancellation-in-managed-threads
  - https://docs.oracle.com/javase/tutorial/essential/concurrency/interrupt.html
  - https://raw.githubusercontent.com/Kotlin/kotlinx.coroutines/master/docs/topics/coroutines-cancellation.md
  - https://docs.python.org/3/library/asyncio-task.html
  - https://developer.android.com/kotlin/coroutines/coroutines-best-practices
---

**Rule.** Take a cancellation signal in long-running work and check it between steps; when a handler catches a cancellation, finish the cleanup and re-raise it.

**Why.** A caller that timed out or gave up still has its work running unless the work looks at the signal, so abandoned requests keep holding connections and threads. Cancellation is cooperative: nothing stops the code that does not check. A handler that swallows the cancellation turns a stop request into a task that carries on, and timeouts built on cancellation then misbehave.

**FAIL**

```python
async def poll(client):
    while True:
        try:
            await client.fetch()
        except asyncio.CancelledError:
            pass                      # swallowed: the task never stops
```

```go
func run() {
	for {
		step() // nothing can tell this loop to stop
	}
}
```

**PASS**

```python
async def poll(client):
    try:
        while True:
            await client.fetch()
    except asyncio.CancelledError:
        await client.close()          # cleanup first
        raise                         # then let the cancellation through
```

```go
func run(ctx context.Context) {
	for ctx.Err() == nil {
		step()
	}
}
```

**See also.** [[svc-timeouts]] sets the deadline on the caller; this card makes the callee honour it.

**Counterpoint.** "Some steps must not be interrupted, such as a commit or a write-ahead flush." Let that step finish and check the signal after it; the rule asks for a check between steps, not an abort in the middle of one. A deliberately detached task that must outlive the request should say so and carry its own owner and stop condition.

---
id: fn-monotonic-clock-for-durations
level: function
tags: [correctness, reliability, time]
severity: should-fix
status: stable
lang: core
applies_when: The code measures how long something took, or waits until a deadline, inside one process.
tool_gate: none
note: Go, Oracle (Java), Android and Mozilla state it as a rule; Python and Rust describe the monotonic clock without telling you to prefer it, so they are extra sources. In Go, time.Now carries a monotonic reading, so subtracting two Time values is already safe
borrowed_from:
  - https://pkg.go.dev/time
  - https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/System.html
  - https://developer.android.com/reference/android/os/SystemClock
  - https://developer.mozilla.org/en-US/docs/Web/API/Performance/now
  - https://docs.python.org/3/library/time.html
---

**Rule.** Measure elapsed time and timeouts with a monotonic clock, never by subtracting wall-clock readings.

**Why.** The wall clock jumps when the system clock is corrected, set by hand or resumed after a pause, so a difference of two readings can be negative or hours long. A timeout built on it fires at once or never. A monotonic reading only moves forward, but it means something only inside one process: a deadline saved to a database or sent to another host still uses wall time.

**FAIL**

```python
start = time.time()
do_work()
elapsed = time.time() - start
deadline = time.time() + 30
```

**PASS**

```python
start = time.monotonic()
do_work()
elapsed = time.monotonic() - start
deadline = time.monotonic() + 30
```

**Counterpoint.** "The drift is tiny, and the wall clock is what the logs show." Corrections of seconds happen on any host that syncs its time, and one negative duration breaks a rate limiter or a retry loop. Keep wall time for what people read, such as a log line or a created-at field, and take the elapsed time from the monotonic clock.

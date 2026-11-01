---
id: fn-bounded-read-fails-at-cap
level: function
tags: [correctness, reliability, security, io]
severity: should-fix
status: draft
lacks: evidence, the sources are API, setting and status-code definitions; only OWASP states the practice
lang: core
applies_when: A function reads a file, a response or a request body through a reader that has a byte limit.
tool_gate: Go lint rule against `io.LimitReader` on untrusted input; a test that feeds one byte more than the cap and expects an error.
note: Google (Go) states the difference between a limit that ends with EOF and one that errors. Django raises an error at its cap, IETF defines 413 for a body over the cap, and OWASP says to reject instead of continuing with partial data. Python and Java readers that cut at n are not cited
borrowed_from:
  - https://pkg.go.dev/net/http#MaxBytesReader
  - https://pkg.go.dev/io#LimitReader
  - https://docs.djangoproject.com/en/5.2/ref/settings/#data-upload-max-memory-size
  - https://www.rfc-editor.org/rfc/rfc9110.html#name-413-content-too-large
  - https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html
---

**Rule.** When a size cap is reached, return an error; never hand back the first N bytes as if they were the whole input.

**Why.** A reader that stops at the cap reports a normal end of input. The code then parses half a JSON document, saves a truncated file, or hashes a prefix, and nothing says the data was cut. The failure appears later as a corrupt record. Check for bytes beyond the cap, or use a reader that errors.

**FAIL**

```go
body, err := io.ReadAll(io.LimitReader(resp.Body, 16<<20)) // 17 MiB payload: err == nil, body cut at 16 MiB
if err != nil {
	return nil, err
}
return body, nil
```

**PASS**

```go
body, err := io.ReadAll(io.LimitReader(resp.Body, 16<<20+1))
if err != nil {
	return nil, err
}
if len(body) > 16<<20 {
	return nil, fmt.Errorf("response exceeds %d bytes", 16<<20)
}
return body, nil
```

**Counterpoint.** "We only need the first part, like a preview." Then say so in the name and the return value, such as `readPrefix` returning a `truncated` flag. The card fails a function that presents the prefix as the full content.

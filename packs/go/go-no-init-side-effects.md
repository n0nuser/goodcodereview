---
id: go-no-init-side-effects
level: function
tags: [maintainability, correctness, go]
severity: discuss
status: draft
lacks: orgs, only Uber states it; needs two more organisations
lang: go
applies_when: A Go file defines `func init()`.
tool_gate: gochecknoinits (golangci-lint)
borrowed_from:
  - https://github.com/uber-go/guide/blob/master/style.md
---

**Rule.** `init()` does no I/O, reads no environment and does not depend on other `init()` functions; do that work from `main()`.

**Why.** `init()` runs on import, in an order readers do not see, before tests can set anything up. A network call or env read there makes importing the package a side effect.

**FAIL**

```go
var db *sql.DB

func init() {
	db, _ = sql.Open("postgres", os.Getenv("DATABASE_URL"))
}
```

**PASS**

```go
func main() {
	db, err := sql.Open("postgres", os.Getenv("DATABASE_URL"))
	if err != nil {
		log.Fatal(err)
	}
	run(db)
}
```

**Counterpoint.** "Registering a driver needs `init()`." Pure registration into a map is deterministic and has no I/O; that is the allowed case.

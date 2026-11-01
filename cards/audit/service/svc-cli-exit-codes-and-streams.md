---
id: svc-cli-exit-codes-and-streams
level: service
tags: [correctness, maintainability, cli, automation]
severity: should-fix
status: stable
note: Non-zero exit on failure backed by Google (gcloud), GitHub (gh exit codes), AWS (CLI return codes), HashiCorp (terraform plan) and The Open Group (POSIX); results on stdout and diagnostics on stderr backed by The Open Group (POSIX), Heroku (CLI style guide) and the Rust CLI working group; clig.dev is a reference
lang: core
applies_when: The code ships a command-line tool that scripts or other programs may run.
context: [cli]
tool_gate: CLI test that runs a failing command and checks the exit code and that stdout is empty.
borrowed_from:
  - https://cloud.google.com/sdk/docs/scripting-gcloud
  - https://cli.github.com/manual/gh_help_exit-codes
  - https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-returncodes.html
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap01.html
  - https://devcenter.heroku.com/articles/cli-style-guide
  - https://rust-cli.github.io/book/tutorial/output.html
  - https://clig.dev/
---

**Rule.** Exit non-zero when a command fails, and write results to stdout and errors and progress to stderr.

**Why.** Scripts branch on the exit code and pipe stdout into the next program. A failure that exits 0 reads as success, and an error line on stdout lands in the next program's input. Add a `--json` flag for structured results, and keep prompts out of non-terminal runs (see [[svc-cli-non-interactive]]).

**FAIL**

```go
if err := run(); err != nil {
	fmt.Println("error:", err) // error goes into the pipe
}
// main returns: exit status 0
```

**PASS**

```go
if err := run(); err != nil {
	fmt.Fprintln(os.Stderr, "error:", err)
	os.Exit(1)
}
```

**Counterpoint.** "Some tools use exit codes for non-error results." Documented codes for states such as "differences found" are fine. The rule is that a failure never exits 0.

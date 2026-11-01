---
id: svc-cli-non-interactive
level: service
tags: [maintainability, process, cli, automation]
severity: should-fix
status: stable
note: Rule backed by GitHub (GH_PROMPT_DISABLED, --title/--body skip the prompt), Google (gcloud --quiet), HashiCorp (terraform -input=false) and Microsoft (az core.disable_confirm_prompt); failing at once with an example call when a flag is missing has one org (clig.dev, a reference), so it sits in Why
lang: core
applies_when: The code ships a command-line tool that scripts or agents may run.
context: [cli]
tool_gate: CLI test that runs every command with stdin closed.
borrowed_from:
  - https://cli.github.com/manual/gh_help_environment
  - https://cli.github.com/manual/gh_pr_create
  - https://cloud.google.com/sdk/docs/scripting-gcloud
  - https://developer.hashicorp.com/terraform/cli/commands/plan
  - https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform
  - https://learn.microsoft.com/en-us/cli/azure/azure-cli-configuration
  - https://clig.dev/
  - https://github.com/cursor/plugins/blob/main/cli-for-agent/skills/cli-for-agents/SKILL.md
---

**Rule.** Let the caller turn every prompt off with a flag or an environment variable, so the command never waits on a terminal.

**Why.** A script or an agent has no one to answer a prompt, so the command hangs until a timeout kills it. When stdin is not a terminal, the best behaviour is to fail at once with an error that names the missing flag and shows an example call, so the caller fixes it in one step.

**FAIL**

```go
env := flag.String("env", "", "target environment")
flag.Parse()
if *env == "" {
	fmt.Print("Choose environment: ")
	fmt.Scanln(env) // always prompts: no way to turn it off, hangs in CI
}
```

**PASS**

```go
env := flag.String("env", "", "target environment")
noInput := flag.Bool("no-input", false, "never prompt")
flag.Parse()
if *env == "" {
	if *noInput || !term.IsTerminal(int(os.Stdin.Fd())) { // golang.org/x/term
		fmt.Fprintln(os.Stderr, "error: --env is required. Example: deploy --env staging")
		os.Exit(2)
	}
	fmt.Fprint(os.Stderr, "Choose environment: ")
	fmt.Scanln(env)
}
```

**Counterpoint.** "Prompts are friendlier for people." Keep them. The rule only asks that the caller can switch prompts off.

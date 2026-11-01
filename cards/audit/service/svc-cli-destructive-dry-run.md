---
id: svc-cli-destructive-dry-run
level: service
tags: [reliability, maintainability, cli, safety]
severity: should-fix
status: stable
note: Preview flag backed by Kubernetes (kubectl --dry-run), Git (git clean -n) and GNU (make -n); confirmation bypass backed by GitHub (gh repo delete --yes), Microsoft (az --yes), Google (gcloud --quiet) and HashiCorp (terraform -auto-approve)
lang: core
applies_when: A command-line tool has a command that deletes, overwrites or sends something.
context: [cli]
tool_gate: CLI test that runs the command with the preview flag and checks nothing changed.
borrowed_from:
  - https://kubernetes.io/docs/reference/kubectl/generated/kubectl_delete/
  - https://git-scm.com/docs/git-clean
  - https://www.gnu.org/software/make/manual/html_node/Options-Summary.html
  - https://cli.github.com/manual/gh_repo_delete
  - https://learn.microsoft.com/en-us/cli/azure/group
  - https://cloud.google.com/sdk/docs/scripting-gcloud
  - https://developer.hashicorp.com/terraform/cli/commands/apply
  - https://clig.dev/
  - https://github.com/cursor/plugins/blob/main/cli-for-agent/skills/cli-for-agents/SKILL.md
---

**Rule.** Give a destructive command a preview flag that changes nothing and a flag that skips the confirmation prompt.

**Why.** Without a preview, the first run is the real one. Without a bypass, a script cannot run the command at all, so people write wrappers that pipe "yes" into it.

**FAIL**

```go
func main() {
	fmt.Printf("Delete %d backups? [y/N] ", len(old))
	var ans string
	fmt.Scanln(&ans) // no preview flag, no way to skip the prompt
	if ans == "y" {
		for _, b := range old {
			os.Remove(b)
		}
	}
}
```

**PASS**

```go
dry := flag.Bool("dry-run", false, "list what would be deleted, delete nothing")
yes := flag.Bool("yes", false, "do not ask for confirmation")
flag.Parse()
for _, b := range old {
	fmt.Println(b)
}
if *dry {
	return
}
if !*yes && !confirm(fmt.Sprintf("Delete %d backups?", len(old))) {
	os.Exit(1)
}
for _, b := range old {
	os.Remove(b)
}
```

**Counterpoint.** "A bypass flag invites accidents." The prompt stays the default for people, and the flag has to be typed on purpose. Pair it with [[svc-cli-non-interactive]].

---
id: svc-update-rollback-on-failure
level: service
tags: [reliability, cli]
severity: should-fix
status: stable
note: Backed by Microsoft (Windows Installer automatic rollback), Google (Android A/B updates keep the old slot as a fallback) and Mender (the bootloader rolls back to the previous version); go-update documents the rename-and-restore steps for a single binary and is a reference
lang: core
applies_when: The code replaces its own binary or an installed program with a new version.
tool_gate: Test that makes the final step fail and checks the old version still runs.
borrowed_from:
  - https://learn.microsoft.com/en-us/windows/win32/msi/rollback-installation
  - https://source.android.com/docs/core/ota/ab
  - https://docs.mender.io/overview/introduction
  - https://pkg.go.dev/github.com/inconshreveable/go-update
---

**Rule.** When an update fails, restore the previous version instead of leaving a missing or half-written one.

**Why.** Deleting the old binary before the new one is in place leaves nothing to run if the copy fails, and the tool cannot update itself back. On Windows a running executable cannot be deleted but can be renamed, so move it aside first and restore it on failure. Keep the old version until the new one has started and passed a self-check, since a binary that installs but will not start needs the old one back.

**FAIL**

```go
exe, _ := os.Executable()
os.Remove(exe) // fails on Windows for a running exe; if the next line fails, no binary is left
return os.Rename(newBin, exe)
```

**PASS**

```go
exe, err := os.Executable()
if err != nil {
	return err
}
old := exe + ".old"
if err := os.Rename(exe, old); err != nil {
	return err
}
if err := os.Rename(newBin, exe); err != nil {
	if rerr := os.Rename(old, exe); rerr != nil {
		return fmt.Errorf("update failed (%v) and rollback failed: %w", err, rerr)
	}
	return err
}
// keep old until the new binary has started and passed its self-check;
// delete it at the next successful start, not here
return nil
```

**Counterpoint.** "Keeping a second copy costs disk space and clutter." One binary-sized file, removed once the new version has started, is cheap next to a tool that cannot start.

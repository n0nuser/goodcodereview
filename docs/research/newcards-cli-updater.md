# New cards pass: CLI behaviour and updaters

Quotes read on the live pages (fetched with curl, 2026-11-01). Orgs per tools/orgs.py. clig.dev and go-update are people-or-community references and never count toward the three.

## svc-cli-non-interactive (promoted)

Clause: take every input from a flag; prompt only as a fallback the caller can switch off.

- GitHub, https://cli.github.com/manual/gh_help_environment: "GH_PROMPT_DISABLED: set to any value to disable interactive prompting in the terminal."
- GitHub, https://cli.github.com/manual/gh_pr_create: "A prompt will also ask for the title and the body of the pull request. Use --title and --body to skip this"
- Google, https://cloud.google.com/sdk/docs/scripting-gcloud: "You can disable prompts from gcloud CLI commands by setting the disable_prompts property in your configuration to True or by using the global --quiet or -q flag."
- HashiCorp, https://developer.hashicorp.com/terraform/cli/commands/plan: "-input=false - Disables Terraform's default behavior of prompting for input for root module input variables ... particularly useful when running Terraform in non-interactive automation systems."
- HashiCorp, https://developer.hashicorp.com/terraform/tutorials/automation/automate-terraform: "terraform plan -out=tfplan -input=false"
- Microsoft, https://learn.microsoft.com/en-us/cli/azure/azure-cli-configuration: "disable_confirm_prompt boolean Turn confirmation prompts on/off."
- Reference (clig.dev, https://clig.dev/): "Never require a prompt. Always provide a way of passing input with flags or arguments. If stdin is not an interactive terminal, skip prompting and just require those flags/args." Also: "If the command requires input, fail and tell the user how to pass the information as a flag." This is the only source for the fail-with-example clause, so it moved to Why.
- Cursor (already listed): cli-for-agents skill.

Result: 4 orgs (GitHub, Google, HashiCorp, Microsoft) for the Rule. Stable, should-fix.

## svc-cli-destructive-dry-run (promoted)

Clause 1, preview flag that changes nothing:
- Kubernetes, https://kubernetes.io/docs/reference/kubectl/generated/kubectl_delete/: "--dry-run ... If client strategy, only print the object that would be sent, without sending it."
- Git, https://git-scm.com/docs/git-clean: "-n --dry-run Don't actually remove anything, just show what would be done."
- GNU, https://www.gnu.org/software/make/manual/html_node/Options-Summary.html: "Print the recipe that would be executed, but do not execute it (except in certain circumstances)."
- Reference (clig.dev): "-n, --dry-run: Dry run. Do not run the command, but describe the changes that would occur if the command were run."

Clause 2, flag that skips confirmation:
- GitHub, https://cli.github.com/manual/gh_repo_delete: "To delete the current repository non-interactively, specify it explicitly (e.g., gh repo delete owner/repo --yes )."
- Microsoft, https://learn.microsoft.com/en-us/cli/azure/group (az group delete): "--yes -y Do not prompt for confirmation."
- Google, https://cloud.google.com/sdk/docs/scripting-gcloud: "disable prompts ... by using the global --quiet or -q flag."
- HashiCorp, https://developer.hashicorp.com/terraform/cli/commands/apply: "-auto-approve - Skips interactive approval of the plan before applying."

Result: 3 orgs for clause 1 (Kubernetes, Git, GNU), 4 for clause 2. Stable, should-fix.

## svc-cli-exit-codes-and-streams (new; no overlap)

The two existing CLI cards cover prompts and previews, not exit status or streams. Prompts on non-TTY stay in svc-cli-non-interactive; the new card links to it.

Clause 1, non-zero exit on failure:
- Google, https://cloud.google.com/sdk/docs/scripting-gcloud: "Do depend on command exit status. If the exit status is not zero, an error occurred and the output may be incomplete"
- GitHub, https://cli.github.com/manual/gh_help_exit-codes: "If a command completes successfully, the exit code will be 0 If a command fails for any reason, the exit code will be 1"
- AWS, https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-returncodes.html: "use these codes to determine if a command was successful or if it failed" (0 = no errors; 1 and 2 describe failures)
- HashiCorp, https://developer.hashicorp.com/terraform/cli/commands/plan: "-detailed-exitcode ... 0 = Succeeded with empty diff (no changes) 1 = Error 2 = Succeeded with non-empty diff"
- The Open Group, https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap01.html: "standard utilities shall issue a diagnostic message to standard error and exit with a non-zero exit status."
- Reference (clig.dev): "Return zero exit code on success, non-zero on failure."

Clause 2, results on stdout, errors and progress on stderr:
- The Open Group (same page): "shall issue a diagnostic message to standard error"
- Heroku, https://devcenter.heroku.com/articles/cli-style-guide: "Actions are displayed on stderr because they are out-of-band information on a running task." and "printing to stdout with this.log()"
- Rust CLI working group (org "rust"), https://rust-cli.github.io/book/tutorial/output.html: "Printing errors should be done via stderr to make it easier for users and other tools to pipe their outputs to files or more tools." and "stdout is for the program's actual output while stderr allows errors and other messages to be kept separate"
- Reference (clig.dev): "Send output to stdout ... Send messaging to stderr."

Result: 5 orgs for clause 1, 3 for clause 2 (Open Group, Heroku, Rust). The Rust CLI book is a working-group guide, so a reviewer may weigh it lightly. Stable, should-fix. The --json flag (GitHub, Heroku, Rust) is only in Why.

## svc-update-verify-provenance (new)

Clause A, verify authenticity with a signature, attestation or pinned key, or a checksum from another route; clause B, a same-host checksum does not count.
- Sparkle, https://sparkle-project.org/documentation/: "Sign the published update archive (dmg, zip, etc), binary delta updates, and installer packages with Sparkle's EdDSA (ed25519) signature. Please ensure your signing keys are kept safe and cannot be stolen if your web server is compromised." Backs A and B.
- Sigstore, https://docs.sigstore.dev/about/overview/: "Compromised site where package is hosted" listed as a threat; "Digital signatures are a way to verify the authenticity of a software artifact." Backs A and B.
- TUF, https://theupdateframework.io/security/: "An attacker who can compromise the one key in a single key system ... can compromise clients. These attacks can occur whether the client relies on a single online key (if only being protected by SSL) or a single offline key" Backs B and A.
- Debian, https://wiki.debian.org/SecureApt: "Notice that so far there is one file that apt doesn't have a way to check: The Release file. Secure apt is all about making apt verify the Release file before it does anything else with it" Backs B (checksums chain to a signed file) and A.
- GitHub, https://docs.github.com/en/actions/concepts/security/artifact-attestations: "Artifact attestations enable you to create unfalsifiable provenance and integrity guarantees for the software you build. In turn, people who consume your software can verify where and how your software was built." Backs A.
- Google, https://go.dev/blog/supply-chain: "The sumdb makes it impossible for compromised dependencies or even Google-operated Go infrastructure to target specific dependents with modified (e.g. backdoored) source." Backs A (hashes come from a separate verifiable log).
- Reference (go-update, https://pkg.go.dev/github.com/inconshreveable/go-update): "While checksum verification is important, it should always be combined with signature verification (next section) to guarantee that the code came from a trusted party." and "an appropriate checksum (that was otherwise retrived via a secure channel)". Person, does not count.

Result: Sparkle, Sigstore, TUF, Debian for both clauses. Stable, should-fix. Not used: Homebrew, Rustup, Deno pages (their installers fetch a checksum from the same host as the archive; Deno docs say "Each asset has a matching .sha256sum file"; this is the practice the card FAILs, not a source for it). SLSA, Microsoft winget, Apple pages not needed.

## svc-update-rollback-on-failure (new)

The ask bundled provenance and rollback; they are two rules, so two cards.
- Microsoft, https://learn.microsoft.com/en-us/windows/win32/msi/rollback-installation: "If however the installation is unsuccessful, the installer automatically performs a rollback installation that returns the system to its original state."
- Google, https://source.android.com/docs/core/ota/ab: "This approach makes updates fault resistant by keeping the unused slot as a fallback: If an error occurs during or immediately after an update, the system can rollback to the old slot and continue to have a working system."
- Mender, https://docs.mender.io/overview/introduction: "If something causes the device to reboot before committing the update, the bootloader knows that something went wrong and will roll back to the previous version by flipping the active and inactive partitions back again."
- Reference (go-update): "Renames /path/to/target to /path/to/.target.old 6. Renames /path/to/.target.new to /path/to/target ... If the final rename fails, attempts to roll back by renaming /path/to/.target.old back to /path/to/target." and "On Windows, the removal of /path/to/target.old always fails, so instead Apply hides the old file instead." Person, does not count; it backs the Windows rename detail in Why.

Result: 3 orgs (Microsoft, Google, Mender). The sources are OS and device updaters, not CLI binaries, so the rule is an analogy to single-file self-update; the Windows rename case rests on go-update alone. Stable, should-fix.

---
id: fn-no-shell-with-input
level: function
tags: [security, injection, command]
severity: block
status: stable
lang: core
applies_when: Code starts a process and some part of the command comes from a request, a file or model output.
tool_gate: Bandit B602 (`subprocess_popen_with_shell_equals_true`) and B605 (`start_process_with_a_shell`) for Python.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/OS_Command_Injection_Defense_Cheat_Sheet.html
  - https://genai.owasp.org/llmrisk/llm052025-improper-output-handling/
  - https://docs.python.org/3/library/subprocess.html
  - https://pkg.go.dev/os/exec
  - https://www.cisa.gov/resources-tools/resources/secure-design-alert-eliminating-os-command-injection-vulnerabilities
---

**Rule.** Start processes with the program and each argument as separate list items, and never through a shell string.

**Why.** A shell reads `;`, `|` and `$()` as commands, so a filename of `a; rm -rf ~` runs. Argument arrays skip the shell. The values still need validation, since an argument beginning with `-` becomes an option; end options with `--` where the tool allows it.

**FAIL**

```python
os.system("convert " + upload_name + " out.png")
subprocess.run(f"git log {branch}", shell=True)
```

**PASS**

```python
subprocess.run(["convert", upload_path, "out.png"], check=True)   # upload_path is a server-generated name
subprocess.run(["git", "log", branch], check=True)   # branch checked against an allowlist
```

**Counterpoint.** "We need shell features like pipes." Chain two `subprocess` calls in code, or use the library that does the job. If a shell is unavoidable, build the string only from constants.

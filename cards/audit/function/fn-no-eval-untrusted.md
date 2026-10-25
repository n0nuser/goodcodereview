---
id: fn-no-eval-untrusted
level: function
tags: [security, injection]
severity: block
status: draft
lacks: evidence, OWASP, MITRE, Mozilla and PortSwigger are listed, but no stable pass has read them for a recommendation versus a definition
lang: core
applies_when: Code runs `eval`, `exec`, `new Function`, an expression language, or compiles a template, and some of the text comes from a request, a file, a database row, or model output.
tool_gate: Bandit B307 (`eval`) and B102 (`exec_used`); CodeQL `py/code-injection`; ESLint `no-eval` and `no-implied-eval`.
note: overlaps fn-no-shell-with-input (commands, not code) and fn-no-raw-html-sink (HTML, not templates); ASVS 1.3.2 and 1.3.7
borrowed_from:
  - https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x10-V1-Encoding-and-Sanitization.md
  - https://cwe.mitre.org/data/definitions/94.html
  - https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval
  - https://portswigger.net/web-security/server-side-template-injection
---

**Rule.** Never pass untrusted text to `eval`, `exec`, `new Function`, an expression language, or a template compiler. Pass it to a fixed template or a parser as data.

**Why.** Each of these turns a string into code that runs with the server's rights, so one field becomes remote code execution. A template engine counts: `render_template_string(request.args["msg"])` lets `{{ config }}` or worse run on the server. Parse the data format instead (`json.loads`, `ast.literal_eval`), and keep templates in files the author wrote, with user values passed as variables.

**FAIL**

```python
total = eval(request.args["expr"])
html = render_template_string("Hello " + request.args["name"])
```

**PASS**

```python
data = json.loads(request.get_data())
html = render_template("hello.html", name=request.args["name"])
```

**Counterpoint.** "Users need formulas, so we need `eval`." Write or adopt a small expression parser that knows only numbers and the operators you allow. A sandbox around `eval` loses to the next escape someone publishes.

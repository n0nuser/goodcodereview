---
id: fn-confine-file-path
level: function
tags: [security, path-traversal, files]
severity: block
status: stable
lang: core
applies_when: Code opens, reads, writes or deletes a file whose name or path includes request data.
tool_gate: CodeQL `py/path-injection` (CWE-22) or the equivalent query for your language.
borrowed_from:
  - https://community.owasp.org/attacks/Path_Traversal
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://go.dev/blog/osroot
  - https://codeql.github.com/codeql-query-help/python/py-path-injection/
---

**Rule.** Resolve the final path and check that it stays inside the intended base directory before using it.

**Why.** A name like `../../etc/passwd`, or its percent-encoded form, walks out of the upload folder. Stripping `../` fails against `....//` and double encoding. The reliable check works on the resolved path. Better still, map a user choice to an ID and build the path in code.

**FAIL**

```python
return send_file(os.path.join(UPLOADS, request.args["name"]))
```

**PASS**

```python
p = (UPLOADS / request.args["name"]).resolve()
if not p.is_relative_to(UPLOADS.resolve()): abort(400)
return send_file(p)
```

**Counterpoint.** "We already strip `..`." String stripping is a blocklist and gets bypassed. Resolve first, compare second. Resolving catches a symlink that already points outside, but a symlink swapped in between the check and the open still escapes. For trees that untrusted users can write to, use a rooted open such as Go's `os.OpenInRoot`, which refuses any escape at open time.

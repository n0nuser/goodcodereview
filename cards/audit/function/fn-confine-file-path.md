---
id: fn-confine-file-path
level: function
tags: [security, path-traversal, files]
severity: block
status: draft
lang: core
applies_when: Code opens, reads, writes or deletes a file whose name or path includes request data.
tool_gate: SAST rule for `open(`, `send_file(` and `os.path.join` with a request-tainted argument.
borrowed_from:
  - https://community.owasp.org/attacks/Path_Traversal
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
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

**Counterpoint.** "We already strip `..`." String stripping is a blocklist and gets bypassed. Resolve first, compare second. Symlinks inside the base directory can still escape, so do not follow them for untrusted trees.

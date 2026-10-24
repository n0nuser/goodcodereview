---
id: svc-upload-validate-store
level: service
tags: [security, files, uploads]
severity: block
status: draft
lang: core
applies_when: The service accepts file uploads.
tool_gate: Upload tests with a renamed `.php`, an oversized file and a zip bomb; storage outside the web root.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
  - https://learn.microsoft.com/en-us/aspnet/core/mvc/models/file-uploads
  - https://portswigger.net/web-security/file-upload
  - https://docs.djangoproject.com/en/5.2/topics/security/#user-uploaded-content
---

**Rule.** Allowlist the file type, cap the size, store under a generated name outside the web root, and serve through a handler.

**Why.** The client-supplied name and Content-Type are attacker text. A user-chosen name allows path tricks, and an upload served from the web root with its original extension can run as code. Count the decompressed size of archives. [[fn-confine-file-path]] covers the path check.

**FAIL**

```text
path = f"/var/www/uploads/{file.filename}"
file.save(path)                       # any type, any size, public URL
```

**PASS**

```text
if ext(file.filename) not in {".png", ".jpg"} or size > 5_000_000: abort(400)
file.save(STORE / f"{uuid4()}.bin")   # outside web root; served by /files/<id>
```

**Counterpoint.** "Checking magic bytes costs time." It is a few bytes read per upload. Skipping it lets a script posing as an image through your extension check.

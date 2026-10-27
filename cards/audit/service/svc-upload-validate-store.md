---
id: svc-upload-validate-store
level: service
tags: [security, files, uploads]
severity: block
status: stable
lang: core
applies_when: The service accepts file uploads.
tool_gate: Upload tests with a renamed `.php`, an oversized file and a zip bomb.
borrowed_from:
  - https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html
  - https://api-security.owasp.org/editions/2023/en/0xa4-unrestricted-resource-consumption
  - https://learn.microsoft.com/en-us/aspnet/core/mvc/models/file-uploads
  - https://portswigger.net/web-security/file-upload
  - https://docs.djangoproject.com/en/5.2/topics/security/#user-uploaded-content
---

**Rule.** Allowlist the file type, cap the size, and store each upload under a generated name where the server will not execute it.

**Why.** The client-supplied name and Content-Type are attacker text. A user-chosen name allows path tricks, and an upload served from the web root with its original extension can run as code. Count the decompressed size of archives. Storing outside the web root and serving files through a handler, or from a separate domain, keeps a file that slips past the type check from running. [[fn-confine-file-path]] covers the path check.

**FAIL**

```python
path = f"/var/www/uploads/{file.filename}"
file.save(path)                       # any type, any size, public URL
```

**PASS**

```python
if sniff_type(file.stream) not in {"image/png", "image/jpeg"} or size > 5_000_000: abort(400)   # type from the content, not the name
file.save(STORE / f"{uuid4()}.bin")   # outside web root; served by /files/<id>
```

**Counterpoint.** "The extension check is enough." The extension is attacker text, and double extensions or parser quirks get past a check on it. The generated name and a storage place that never executes files are what make a file that slips through harmless.

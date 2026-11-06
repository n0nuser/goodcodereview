---
id: svc-decompression-cap
level: service
tags: [security, performance, dos]
severity: should-fix
status: stable
lang: core
applies_when: The code decompresses or decodes input whose size it does not control.
context: [server]
tool_gate: Apache `DeflateInflateLimitRequestBody`; ASP.NET Core `MaxRequestBodySize`; a test that inflates a 1 MB gzip to about 1 GB and asserts the decoder stops at the cap.
borrowed_from:
  - https://nodejs.org/api/zlib.html
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/middleware/request-decompression?view=aspnetcore-10.0
  - https://httpd.apache.org/docs/2.4/mod/mod_deflate.html
  - https://docs.python.org/3/library/tarfile.html
---

**Rule.** Cap the decompressed output of every decoder, and set the cap on the output rather than the compressed input.

**Why.** A small gzip can expand a thousand-fold: DEFLATE tops out near 1030:1, so a 1 MB gzip can inflate to about 1 GB, and nested archives or other codecs can go further. A body limit on the compressed bytes does not bound that expansion, so the decoder needs its own ceiling. `Content-Length` counts the compressed stream, not the inflated body, and Apache's inflated-body directive is unset by default. In Node, the convenience methods take `maxOutputLength`, whose default is `buffer.kMaxLength`, so pass a real number. The zip entry iterator is a separate case: `zipEntry.contentIterator()` has no default `maxSize` and is not covered by the zip-wide ceiling, so pass `maxSize` on that call. Python's tar filters address paths and links, and its docs say they do not prevent every unsafe archive, so size still needs its own bound. See also [[svc-bound-client-controlled-sizes]] for the request-body cap and [[svc-upload-validate-store]] for archives in uploads.

**FAIL**

```javascript
const body = zlib.gunzipSync(req.body); // no maxOutputLength
parse(body);
```

**PASS**

```javascript
const body = zlib.gunzipSync(req.body, { maxOutputLength: 1 << 20 });
parse(body);
```

**Counterpoint.** "The proxy already caps the request body." It caps the compressed bytes, which is the wrong number. A 1 MB gzip can still inflate to about 1 GB, and `Content-Length` says nothing about the decompressed size. Set the inflated cap at the decoder and keep the body cap. Where the platform offers a decompression limit, check that it is on: Apache's directive falls back to the post-deflation `LimitRequestBody`, and a value of `0` removes the inflated-body limit.

# API pass: HTTP APIs and service contracts

Fetched 2026-10-24 through WebFetch (a small model summarises each page). Everything below is paraphrase. Each row gives the URL, the distilled point, whether a reviewer can mark it `FAIL`, and the card id it supports. Cards named here are new unless marked "existing".

Reading limits, so a later reviewer knows what was not seen:

- RFC 9110 is 560k characters. Sections 9.2.1, 9.2.2, 9.3.4, 9.3.5, 10.2.3, 13.1.1 and 15.3.2 were read. Section 15.5.6 (405) was not; the 405 and `Allow` rule rests on the pointer in section 10.2.1.
- Zalando rule 119 and the guideline text on internal fields and contract testing did not appear in the part of the page that was read. No card leans on them.
- The Pact page does not describe provider verification or the broker. Those facts are from general knowledge and are left out of the cards.
- The IETF rate-limit header text is still an Internet-Draft, not an RFC.

## 1. Specification as the source of truth

1. https://spec.openapis.org/oas/v3.1.0.html. An OpenAPI document describes the API; `info.version` is the version of that description, separate from the implementation and from the `openapi` field. Each `operationId` is unique across the document. Nothing in the spec says the description must match the running service. FAIL: yes, the match check is a test or generation step. -> `svc-api-spec-matches-impl`.
2. https://opensource.zalando.com/restful-api-guidelines/. Rule 100 (MUST): design the API first, against the guidelines, with early peer review. Rule 101 (MUST): write the spec in OpenAPI as one self-contained YAML file under version control. Zalando's own wording makes this a design-process rule; the cards check the artefact, not the process. FAIL: yes for a missing spec or a spec that drifts. -> `svc-api-spec-matches-impl`, `chg-api-spec-in-same-change`.
3. https://opensource.zalando.com/restful-api-guidelines/. Rule 151 (MUST): document success and error responses in the spec. The OpenAPI Responses object must list at least one response code and may use `default` for the rest. FAIL: yes. -> `svc-api-documented-errors`.
4. https://spec.openapis.org/oas/v3.1.0.html. A media type object takes `example` or `examples`, not both. A schema example is overridden by a value set on the media type. FAIL: partly. A reviewer can mark a missing example; the mutual-exclusion rule is a linter job. -> `svc-api-documented-errors`.

## 2. Errors

5. https://www.rfc-editor.org/rfc/rfc9457.html. Problem details are a JSON object served as `application/problem+json`. The members `type`, `title`, `status`, `detail` and `instance` are all optional. `type` defaults to `about:blank`, meaning "nothing beyond the status code". The `status` member must match the real HTTP status. FAIL: yes. -> `svc-api-problem-json`.
6. https://www.rfc-editor.org/rfc/rfc9457.html. Clients must ignore unknown extension members and must not parse `detail`. Machine-readable data belongs in extension members. So the stable thing a client keys on is `type` or an extension code, never the sentence. FAIL: yes. -> `svc-api-error-code-stable`.
7. https://www.rfc-editor.org/rfc/rfc9457.html. Security section: do not put stack traces or other internals in a problem response, and vet what each problem type reveals. FAIL: yes. -> `svc-api-problem-json`; the existing `sys-secrets-and-errors` covers the wider case.
8. https://google.aip.dev/193. Errors carry a machine-readable `reason` in `ErrorInfo`, upper snake case and at most 63 characters, plus a `domain`. The pair identifies one logical error. Request-specific values also go in `metadata`, so clients never parse the message. Once published, a metadata key stays. FAIL: yes. -> `svc-api-error-code-stable`.
9. https://google.aip.dev/193. Check permission before existence: a caller without access gets 403 whether or not the resource exists; 404 only for callers who have access. FAIL: yes, but it overlaps `svc-sqli-authn`-style authorisation review. Left as a note, no card. -> none.
10. https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md. Azure's guidelines (see also row 22) require an `x-ms-error-code` header that equals the body's top-level `code`, and a documented list of codes. Supports row 6 and 8 as a second vendor doing the same. -> `svc-api-error-code-stable`.

## 3. Methods and status codes

11. https://www.rfc-editor.org/rfc/rfc9110.html section 9.2.1. GET, HEAD, OPTIONS and TRACE are safe: meant to be read-only. A handler for a safe method that changes state breaks caches, prefetchers and crawlers. FAIL: yes. -> `svc-api-safe-idempotent-methods`.
12. https://www.rfc-editor.org/rfc/rfc9110.html section 9.2.2. PUT, DELETE and every safe method are idempotent, which is what lets a client retry them after a connection failure. POST and PATCH are not, by definition. FAIL: yes. -> `svc-api-safe-idempotent-methods`; retries of POST stay under existing `svc-idempotency-key`.
13. https://www.rfc-editor.org/rfc/rfc9110.html sections 9.3.4 and 9.3.5. PUT: 201 if it created the resource, 200 or 204 if it replaced one. DELETE: 202 if deletion is likely but not done, 204 if done with nothing to say, 200 if done with a status description. FAIL: yes. -> `svc-api-specific-status-codes`.
14. https://www.rfc-editor.org/rfc/rfc9110.html section 15.3.2. 201 Created identifies the new resource by the `Location` header, or by the request URI if there is none. FAIL: yes. -> `svc-api-specific-status-codes`.
15. https://www.rfc-editor.org/rfc/rfc9110.html section 10.2.1. A 405 response must carry an `Allow` header listing the supported methods. FAIL: yes. Only the pointer in 10.2.1 was read, not 15.5.6. -> `svc-api-specific-status-codes`.
16. https://opensource.zalando.com/restful-api-guidelines/. Rule 220 (MUST): choose the most specific status code that fits. Rule 150 (SHOULD): stay within the commonly used codes. FAIL: yes for 200 with an error body or 500 for bad input; no for the exact code chosen between two fitting ones. -> `svc-api-specific-status-codes`.

## 4. Retry, rate limits, conditional writes

17. https://www.rfc-editor.org/rfc/rfc9110.html section 10.2.3. `Retry-After` on a 503 says how long the service is unavailable; on a 3xx it is the minimum wait before following the redirect. The value is a number of seconds or an HTTP-date. 429 comes from RFC 6585, which was not fetched; the existing `svc-rate-limit-quota` card already assumes it. FAIL: yes. -> `svc-api-retry-after`.
18. https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/. Draft 11 defines `RateLimit-Policy` and `RateLimit` to replace the unstandardised `X-RateLimit-*` headers. Servers may send them on any response and are not required to. If `Retry-After` is also present, clients follow it. It is a draft, and an early directorate review rated an earlier version "not ready". FAIL: no for the draft headers. Only `Retry-After` is checkable. -> `svc-api-retry-after` (counterpoint only).
19. https://opensource.zalando.com/restful-api-guidelines/. Rule 153 (MUST): return 429 with rate-limit headers when limits are hit. Zalando's headers predate the draft. FAIL: yes for the 429; the header names are a house choice. -> `svc-api-retry-after`.
20. https://www.rfc-editor.org/rfc/rfc9110.html section 13.1.1. `If-Match` makes a write conditional on the current entity tag; the server uses strong comparison and does not perform the method on a mismatch. It may answer 412 (Precondition Failed). The header exists mainly to stop lost updates. FAIL: yes for a PUT or PATCH on a shared resource with no precondition. -> `svc-api-conditional-writes`.
21. https://opensource.zalando.com/restful-api-guidelines/. Rule 182 is a MAY: consider ETag with `If-Match` or `If-None-Match` for optimistic locking. Weaker than the RFC, so the card is `should-fix`, not `block`. -> `svc-api-conditional-writes`.
22. https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md. Azure honours `If-Match`, `If-None-Match`, `If-Modified-Since` and `If-Unmodified-Since`. A mismatched `If-Match` on PUT, PATCH or DELETE returns 412. `If-None-Match: *` on a create returns 412 if the resource exists. Reads and updates return an `ETag`, preferably a hash of the full representation. Also: async operations return 202 with an `operation-location` header and a status monitor, and status polls carry `retry-after` in whole seconds. FAIL: yes. -> `svc-api-conditional-writes`.

## 5. Caching

23. https://www.rfc-editor.org/rfc/rfc9111.html section 5.2.2. `no-store` forbids storing; `no-cache` allows storing but requires revalidation before reuse; `private` bars shared caches; `public` marks a response cacheable even when it would not otherwise be; `max-age` sets freshness in seconds; `s-maxage` overrides it for shared caches. `no-store` is not a reliable privacy control against a misbehaving cache. FAIL: yes. -> `svc-api-cache-control`.
24. https://www.rfc-editor.org/rfc/rfc9111.html sections 4.2.2 and 7.3. With no explicit expiry, a cache may invent a freshness lifetime from `Last-Modified` (about a tenth of the age is the common guideline). A `Set-Cookie` header does not stop caching, so servers should set explicit directives. A shared cache holding a user-specific response can serve it to another user. FAIL: yes. -> `svc-api-cache-control`.
25. https://www.rfc-editor.org/rfc/rfc9111.html section 4.1. A stored response is reused only when the request headers named in `Vary` match; `Vary: *` never matches. A response that differs by header (language, encoding, auth) and omits `Vary` is served to the wrong caller. FAIL: yes. -> `svc-api-cache-control`.
26. https://opensource.zalando.com/restful-api-guidelines/. Rule 227 (MUST): document which GET, HEAD and POST endpoints are cacheable. The page text read does not cover `Cache-Control` itself. -> `svc-api-cache-control`.

## 6. Versioning and deprecation

27. https://opensource.zalando.com/restful-api-guidelines/. Rules 106 to 110: do not break compatibility; prefer compatible extensions; clients must tolerate unknown fields; return JSON objects at the top level so fields can be added. Rule 113: avoid versioning when possible. Rules 114 and 115: if you must version, use media types, not version numbers in URLs. Rule 116: spec version is MAJOR.MINOR.PATCH. FAIL: partly. A policy exists or does not; the choice of media type versus header versus path is a house decision. Microsoft and Stripe pick other mechanisms (rows 28 and 29). -> `svc-api-versioning-policy`; existing `svc-api-compat-pagination` and `chg-breaking-change-taxonomy` cover the content of a change.
28. https://github.com/microsoft/api-guidelines/blob/vNext/azure/Guidelines.md. Every operation requires an `api-version` query parameter (`YYYY-MM-DD`, with `-preview` for previews). A missing or unknown value returns 400. No version number in the path. A preview lives at most a year, and retiring one needs at least 90 days' notice. No breaking changes inside a version. FAIL: yes against the API's own stated policy. -> `svc-api-versioning-policy`.
29. https://docs.stripe.com/api/versioning. Since the 2024-09-30 release, Stripe ships a new API version monthly with no breaking changes and a major release twice a year that may break. A request uses the account's pinned version unless the `Stripe-Version` header overrides it, and webhook endpoints pin a version at creation. Supports "a client pins a version; the server keeps old versions working". -> `svc-api-versioning-policy`.
30. https://www.rfc-editor.org/rfc/rfc9745.html. `Deprecation` is a response header whose value is a date (a structured-field date, written as `@` plus a Unix timestamp). It can be in the past or future. It applies to the one resource in the response. It does not change how the resource behaves. A `Link` with relation `deprecation` can point to documentation. The RFC does not define a `successor-version` relation, so do not require one. FAIL: yes. -> `svc-api-deprecation-sunset`.
31. https://www.rfc-editor.org/rfc/rfc8594.html. `Sunset` is one HTTP-date saying when the resource is expected to stop responding. A past date reads as "now". After it, requests may fail with 4xx or 3xx or not connect at all. `Link` relation `sunset` points to retirement information. The header is unrelated to caching. FAIL: yes. -> `svc-api-deprecation-sunset`.
32. https://www.rfc-editor.org/rfc/rfc9745.html. The `Sunset` date must not be earlier than the `Deprecation` date. A client that sees otherwise should ask the developer. FAIL: yes. -> `svc-api-deprecation-sunset`.
33. https://opensource.zalando.com/restful-api-guidelines/. Rule 189 (SHOULD): deprecated endpoints send `Deprecation` and `Sunset`. Rule 190 (SHOULD): monitor traffic that carries them, so you know who still calls before you remove it. Rule 191 (MUST): do not start using an API already marked deprecated. FAIL: yes. -> `svc-api-deprecation-sunset`.
34. https://spec.openapis.org/oas/v3.1.0.html. An operation has a boolean `deprecated` (default false) that tells consumers to stop using it. FAIL: yes, paired with row 30. -> `svc-api-deprecation-sunset`.

## 7. Naming and leaking internals

35. https://opensource.zalando.com/restful-api-guidelines/. Rule 118 (MUST): JSON properties are snake_case. Microsoft's Azure guidelines say camelCase for fields and query parameters and kebab-case for headers and paths. The two guidelines disagree, so the rule that survives is "one convention, documented, applied everywhere". FAIL: yes for mixed casing in one API. -> `svc-api-naming-consistent`.
36. https://protobuf.dev/best-practices/dos-donts/. Use separate messages for the RPC API and for storage so storage can change independently. Same idea as a REST handler that returns a database row. The source is about protobuf; the REST application is inference. FAIL: yes. -> `svc-api-no-internal-fields`; existing gap id `mod-no-wire-types-in-public-api` is the module-level mirror.

## 8. Tracing

37. https://www.w3.org/TR/trace-context/. `traceparent` has a version, a 16-byte trace id, an 8-byte parent id and flags. All-zero ids are invalid. A service must forward `traceparent` and `tracestate`. If `traceparent` is missing or invalid, it starts a new trace and drops `tracestate`. For each outgoing call it sets a new parent id and keeps the trace id. FAIL: yes. -> `svc-api-trace-context`.
38. https://www.w3.org/TR/trace-context/. `tracestate` entries from other vendors are not to be deleted or rewritten; a vendor updates only its own entry and moves it to the left. Neither header may carry personal data. FAIL: yes for the personal-data case; the rest is library behaviour. -> `svc-api-trace-context`.
39. https://opensource.zalando.com/restful-api-guidelines/. Rule 233 (MUST): support the `X-Flow-ID` header. Older than Trace Context and vendor-specific. Not a card; `traceparent` is the standard. -> none; existing `svc-request-id-logging` is the log-side rule.

## 9. Contract tests

40. https://docs.pact.io/. Pact tests HTTP and message integrations against a contract generated by the consumer's own automated tests. It is consumer-driven: only the parts of a provider that consumers use are tested, so the provider can change the rest. It replaces slow end-to-end tests that deploy every service. A schema such as OpenAPI describes every possible state; a Pact contract is a set of concrete request and response examples run as tests. Provider-only checks against a spec do not show that consumers call it correctly. FAIL: yes for a cross-team or cross-service call with no contract test of any kind. Pact is one tool; a schema-diff plus example test also satisfies the card. -> `svc-api-contract-tests`.

## 10. Protobuf and gRPC compatibility

41. https://protobuf.dev/best-practices/dos-donts/. Never reuse a field number, even when old data seems gone. On delete, reserve the number and the name. FAIL: yes in the diff. -> `chg-proto-reserve-removed-fields`.
42. https://protobuf.dev/best-practices/dos-donts/. Do not change a field's type or default value, and do not change repeated to scalar. Do not rely on renaming fields or enum values when the JSON or text format is in use, because those formats carry names. FAIL: yes in the diff. -> `chg-proto-no-field-type-change`.
43. https://protobuf.dev/best-practices/dos-donts/. First enum value is a zero value named like `FOO_UNSPECIFIED` with no real meaning. Delete an enum value by reserving its number and name. Do not add required fields; document the requirement and use optional or repeated. FAIL: yes. -> `mod-proto-enum-zero-unspecified`. The "no required fields" half has no card yet: one more rule would be `mod-proto-no-required-fields`, left unwritten to keep this pass to one rule per source point that matters most.
44. https://protobuf.dev/best-practices/dos-donts/. Do not depend on serialised bytes being identical across builds, for example in a cache key. FAIL: yes. No card; narrow. -> none.

## Existing cards refined

- `svc-request-id-logging`: add a see-also line pointing to `svc-api-trace-context` (the header that carries the id between services).
- `svc-rate-limit-quota`: add a see-also line pointing to `svc-api-retry-after` (what the 429 must carry).
- `chg-breaking-change-taxonomy` is stable, so it gets no link to these drafts until they are promoted. The new cards link to it instead.

## Not carried into a card

- Rate-limit header names (row 18): draft, not an RFC.
- `X-Flow-ID` (row 39): superseded in practice by `traceparent`.
- Permission-before-existence (row 9): an authorisation-review point, not an API-contract one.
- Long-running operations with 202 and a status monitor (row 22): one vendor's pattern.

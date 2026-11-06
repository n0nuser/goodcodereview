---
id: svc-request-framing
level: service
tags: [security, http, protocol]
severity: block
status: stable
lang: core
applies_when: The service parses HTTP requests itself, or receives them through a proxy, load balancer, or CDN.
context: [server]
tool_gate: A test that sends one request with both Content-Length and Transfer-Encoding and expects 400 or a closed connection.
note: reject or remove one framing field - IETF, PortSwigger, Microsoft, Fastly, Envoy and Cloudflare; strict parsing - IETF, OpenJS (Node), PortSwigger, Envoy and Microsoft; the HTTP/1.1 downgrade rule has PortSwigger and Fastly only, so it is in Why
borrowed_from:
  - https://www.rfc-editor.org/rfc/rfc9112.html
  - https://portswigger.net/web-security/request-smuggling
  - https://learn.microsoft.com/en-us/aspnet/core/fundamentals/servers/kestrel/security-considerations?view=aspnetcore-10.0
  - https://www.fastly.com/learning/security/what-is-http-request-smuggling
  - https://www.envoyproxy.io/docs/envoy/latest/api-v3/extensions/http/header_validators/envoy_default/v3/header_validator.proto.html
  - https://developers.cloudflare.com/support/troubleshooting/http-status-codes/4xx-client-error/error-400/
  - https://nodejs.org/api/http.html
---

**Rule.** Reject a request that carries both `Transfer-Encoding` and `Content-Length`, or remove one field at the first hop, and parse header framing strictly rather than with a leniency flag.

**Why.** Two hops can disagree about where a request ends. The front end reads one body length and the back end reads another, so the leftover bytes become the start of the next request on the same connection. That request skips the front end's checks: it can reach an admin route, poison a cache, or splice one user's response into another user's connection. The ambiguity comes from a second framing field, a malformed header name, or a parser that accepts what the specification rejects. A front end that downgrades HTTP/2 to HTTP/1.1 reopens the gap, so validate the rewritten request as well.

**FAIL**

```text
POST /login HTTP/1.1
Host: app.example
Content-Length: 15
Transfer-Encoding: chunked

0

GET /admin
```

The proxy forwards this over a reused upstream connection. The front end reads fifteen bytes as the body. The back end finds the end of the chunked body and keeps `GET /admin` for the next request on the connection, so it reaches a route the front end never checked.

**PASS**

```text
# front end
if both framing fields are present:
    return 400 and close the connection      # or drop Content-Length, forward, then close

# parser
insecureHTTPParser: false                    # Node
allow_chunked_length: false                  # Envoy
whitespace before a header colon: 400
```

**Counterpoint.** "We speak HTTP/2 end to end, so there is nothing to smuggle." HTTP/2 has one framing mechanism, but many deployments still downgrade at the last hop, and compatibility flags keep the old leniency in parsers. Check both ends of every connection and the rewrite between them, not the version the client negotiated.

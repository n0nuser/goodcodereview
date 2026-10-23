# Reverse Proxies

A server that receives client traffic and forwards it to backends, often adding TLS, caching or routing.

**Why a reviewer cares.** Reviewers care about which layer owns timeouts, retries and headers, so they are not applied twice.

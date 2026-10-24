# Reverse proxies

A server that receives client traffic and forwards it to backends. It often adds TLS, caching, or routing.

**Why a reviewer cares.** Check which layer owns timeouts, retries, and headers, so that none is applied twice.

---
id: svc-webhook-replay-window
level: service
tags: [security, messaging, webhooks]
severity: should-fix
status: stable
lang: core
applies_when: The code accepts signed webhooks or signed messages from another system.
context: [server]
tool_gate: A test that replays a captured request with the timestamp moved outside the tolerance and asserts a 4xx, and one that changes only the timestamp header and asserts a 4xx.
note: tolerance on a signed creation time backed by Svix, Slack and Stripe (all three put the timestamp inside the signed content); IETF RFC 9421 permits the check and is a reference only
borrowed_from:
  - https://docs.svix.com/receiving/verifying-payloads/how-manual
  - https://docs.slack.dev/authentication/verifying-requests-from-slack/
  - https://www.rfc-editor.org/rfc/rfc9421.html
  - https://docs.stripe.com/webhooks
---

**Rule.** Reject an inbound signed message whose creation time is outside a short tolerance, and sign that time with the body so it cannot be swapped.

**Why.** A valid signature proves who sent the message, not when. A captured request keeps its signature and can be sent again. Put the timestamp inside the signed content, as Slack, Svix and Stripe do. A timestamp in a separate header that the signature does not cover can be replaced by the attacker. Compare the timestamp with local time before doing any work. Retries are normal, so also store the message id and skip an id already processed. Deduplication stops a replay inside the window. The window stops one outside it and bounds how long the id store must keep entries.

**FAIL**

```python
if not verify_hmac(body, headers["X-Signature"], secret):
    return 401
apply_event(body)   # a captured request replays for as long as the secret lives
```

**PASS**

```python
ts = headers["X-Timestamp"]
if abs(time.time() - int(ts)) > 300:
    return 401
if not verify_hmac(f"{ts}.".encode() + body, headers["X-Signature"], secret):
    return 401
apply_event(body)
```

**Counterpoint.** "A tight window drops delayed deliveries and retries." It does. RFC 9421 lets an application enforce a maximum signature age and leaves the number to it, and five minutes is the default of Slack and Stripe, not a standard. Pick a tolerance from the provider's retry schedule and your clock skew, log every reject with the offset, and keep deduplication by event id so a replay inside the window still does nothing. A signature with no timestamp at all cannot be bounded this way. The receiving endpoint has to rely on deduplication and on the sender's short-lived credential.

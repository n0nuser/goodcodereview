---
id: svc-saml-assertion-binding
level: service
tags: [security, authn, saml]
severity: block
status: stable
lang: core
applies_when: The service is a SAML 2.0 service provider and accepts a response or assertion at an assertion consumer service endpoint.
context: [server]
tool_gate: none
note: fn-xml-no-external-entities covers the XML parser; this card covers what to check before a NameID becomes a session. For an IdP-initiated response, `InResponseTo` must be absent; keep the replay cache.
borrowed_from:
  - https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf
  - https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html
  - https://pages.nist.gov/800-63-4/sp800-63c/Federation/
  - https://learn.microsoft.com/en-us/entra/identity-platform/single-sign-on-saml-protocol
  - https://github.com/SAML-Toolkits/python3-saml
---

**Rule.** Verify the XML signature over the assertion you read, with the IdP's configured key rather than a key carried in the response, then require the assertion's `Audience` and its bearer `SubjectConfirmationData` `Recipient` to name this SP, the response `Destination` to be this endpoint, `InResponseTo` to match your request (absent for an IdP-initiated response), `NotOnOrAfter` to be current, and the assertion ID to be unseen. These are one step, verify the assertion, and each check is cited.

**Why.** A valid signature elsewhere in the document proves nothing about the `<NameID>` your code just read. That gap is the signature-wrapping attack, and it lets an attacker choose which identity your service trusts. A lookup such as `.//NameID` is how the signed element and the read element get separated. Pinning the key to the IdP stops the document choosing its own verification key. The audience and destination checks stop an assertion minted for another SP from being posted here. `InResponseTo` catches a response injected into a browser that never started the request, and the time window plus the used-ID set stop a captured assertion from being replayed.

**FAIL**

```text
doc = etree.fromstring(base64.b64decode(form["SAMLResponse"]))
name_id = doc.find(".//NameID").text
login(name_id)      # no signature check, no audience, no replay set
```

**PASS**

```python
signed = verify_signature(response, key=IDP_CERT)     # returns the signed element
assertion = signed.assertion
if assertion.audience != SP_ENTITY_ID or response.destination != ACS_URL:
    raise InvalidAssertion
if assertion.subject_confirmation.recipient != ACS_URL:
    raise InvalidAssertion
if assertion.subject_confirmation.in_response_to != request_id:
    raise InvalidAssertion
if assertion.not_on_or_after <= now() or used_ids.seen(assertion.id, until=assertion.not_on_or_after):
    raise InvalidAssertion
```

**Counterpoint.** "The library validates the signature, so the assertion is trustworthy." The signature vouches for the bytes it covers, not for the element your handler reads. A strict mode that validates the response but leaves an unsigned assertion in the tree still passes a wrapped `NameID`. Require the assertion to be inside the signed content, take the key from IdP metadata, and record the ID of the assertion you accepted, not the ID of its wrapper.

**See also.** [[fn-xml-no-external-entities]] covers the parser; [[svc-session-lifecycle]] starts where this card ends.

# module

## mod-colour-tokens-meet-contrast

severity: should-fix  
concerns: accessibility, usability  
applies_when: A design-system module or theme defines foreground and background colour tokens.  
Backed by: W3C, Deque, The A11y Project, Apple, Google.

**Rule.** Make every text and background token pair meet 4.5:1 (3:1 for large text), and every border, icon, and focus colour meet 3:1 against its neighbour.

**Why.** Low contrast is invisible to the author on a bright monitor. Fixing it once in the tokens fixes every component. Fixing it per component means hunting through each one, and each new component can reintroduce it.

**FAIL**

```css
:root {
  --text-muted: #9aa0a6;     /* 2.6:1 on white */
  --bg: #ffffff;
  --input-border: #e0e0e0;   /* 1.3:1 on white */
}
```

**PASS**

```css
:root {
  --text-muted: #5f6368;     /* 6.0:1 on white */
  --bg: #ffffff;
  --input-border: #767676;   /* 4.5:1 on white, above the 3:1 floor */
}
```

```js
test.each(pairs)("%s meets 4.5:1", (fg, bg) => expect(ratio(fg, bg)).toBeGreaterThanOrEqual(4.5));
```

**Counterpoint.** "The brand colour fails." A logo is exempt. A brand-coloured button label or link is not. Darken the shade used for text and keep the brand shade for fills. The ratio is exact: 4.499:1 fails.

## mod-derive-dont-duplicate

severity: should-fix  
concerns: compatibility, maintainability  
applies_when: A schema, spec, enum or list owns a shape that other code restates by hand.  
Backed by: Cursor, Uber, Stripe, Spotify.

**Rule.** Derive a type, list or enum from the schema or list that owns it, or add a build check that fails when the two disagree.

**Why.** A hand-kept copy drifts. The next field added to the schema is missing from the copy, and nothing fails until a user hits it.

**FAIL**

```text
openapi.yaml defines Status: [open, closed, void]
status.py:   class Status(Enum): OPEN, CLOSED     # void missing
```

**PASS**

```text
status.py is generated from openapi.yaml in the build, or a test asserts the two sets are equal
```

**Counterpoint.** "Generated code is awkward to read." A parity test gives the same safety with hand-written types. The rule fails only when neither derivation nor a check exists.

## mod-pooled-clients-built-once

severity: should-fix  
concerns: performance  
applies_when: Code creates a network or database client.  
Backed by: Microsoft, Google, Requests project, OpenJS Foundation.

**Rule.** Build pooled clients once at startup and reuse them.

**Why.** A client per call defeats connection pooling, leaks sockets, and pays a handshake every time. When a client must be short-lived, close it when the work ends.

**FAIL**

```csharp
async Task<string> Fetch(string url) {
    using var client = new HttpClient();     // new pool and socket per call
    return await client.GetStringAsync(url);
}
```

**PASS**

```csharp
static readonly HttpClient Client = new() { Timeout = TimeSpan.FromSeconds(10) };   // once

async Task<string> Fetch(string url) => await Client.GetStringAsync(url);
```

**Counterpoint.** "A throwaway client is simpler." For a one-off script, yes (scope it with `with`). On a server path it exhausts sockets under load.

## mod-single-writer-per-state

severity: should-fix  
concerns: correctness  
applies_when: More than one module, worker or process writes the same state.  
Backed by: Cursor, Netflix, Cabify, GitHub.

**Rule.** Let only one writer change a piece of state at a time, through a single owner, a queue that serialises the writes, or compare-and-swap, never by convention.

**Why.** A convention such as "only write your own field" is not concurrency control. Two workers writing different fields of one file still overwrite each other, and two deploy runs that overlap can undo each other's changes. Better still, split the state so that each writer owns its part and readers merge the parts: writers to different parts then never wait for each other.

**FAIL**

```text
worker A and worker B each load state.json, set their own key, and save the whole file
```

**PASS**

```text
workers send updates to one queue; a single consumer applies them to state.json in order
or: state/a.json and state/b.json, one writer each; readers merge them
```

**Counterpoint.** "A lock is simpler than a queue or an owner." A lock works only when the store rejects a writer whose lock has expired; see [sys-lock-fencing](system.md#sys-lock-fencing). Without that check, a paused holder can wake up and write after another writer took over.

## mod-vetted-crypto-only

severity: block  
concerns: security  
applies_when: A module encrypts or decrypts data.  
Backed by: OWASP, IETF, NIST, Google.

**Rule.** Encrypt with an authenticated mode such as AES-GCM, and never reuse a nonce under one key.

**Why.** Unauthenticated modes allow silent tampering, and ECB also leaks the structure of the plaintext. Reusing a nonce under one key breaks GCM completely: it leaks the XOR of the plaintexts and the authentication key. Take the call from a maintained library and never write your own cipher. Keys belong in a KMS or secrets manager, never in source; [sys-secrets-and-errors](system.md#sys-secrets-and-errors) covers where secrets live at runtime.

**FAIL**

```python
cipher = AES.new(KEY, AES.MODE_ECB)
ct = bytes(b ^ k for b, k in zip(msg, KEY * 99))
```

**PASS**

```python
aead = AESGCM(key_from_kms)
ct = aead.encrypt(os.urandom(12), msg, aad)      # fresh nonce per message
```

**Counterpoint.** "The library API is awkward, so a wrapper is safer." Wrap the vetted call, do not replace it. Review the wrapper only for nonce handling and key sourcing.

## mod-yagni

severity: should-fix  
concerns: maintainability, process  
applies_when: The change adds an abstraction, parameter, hook or option.  
Backed by: Google. People cited: Kent C. Dodds, Henrik Warne.

**Rule.** Add an abstraction only when the logic is reused, non-trivial, or clutters the main flow; do not build for a need that does not exist yet.

**Why.** Speculative flexibility costs reading time every day and is usually the wrong shape when the need arrives. Reviewers cannot verify a use that does not exist.

**FAIL**

```text
class NotifierFactory: ...   # one product, one caller
def send(msg, retries=3, backoff=None, hook=None): ...   # nobody passes these
```

**PASS**

```text
def send_welcome_email(user): ...
```

**Counterpoint.** "But we will surely need it." Then add it when you do, in a change that has the real second caller to shape it. Optimising for easy change means simple code, not built-in flexibility. Trivial single-use logic stays inline. The cost of waiting is low, and the cost of the wrong guess is not.

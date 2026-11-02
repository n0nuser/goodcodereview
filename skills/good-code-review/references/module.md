# module

## mod-colour-tokens-meet-contrast

severity: should-fix  
concerns: accessibility, usability  
applies_when: A design-system module or theme defines foreground and background colour tokens.  
context: ui  
Backed by: W3C, Deque, The A11y Project, Apple, Google, WebAIM.

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

## mod-no-module-mutable-state

severity: should-fix  
concerns: correctness, testing  
applies_when: A module defines a variable that changes after load: a list, dict, counter, cache, client or singleton.  
Backed by: Google, Uber, Microsoft.

**Rule.** Keep no mutable state at module level.

**Why.** Hidden global state leaks between tests, between requests, and between threads, and its order of mutation is unreadable. A frozen, load-once constant such as settings is the exception. A singleton used to dodge injection is not.

**FAIL**

```python
_cache = {}

def get(key):
    if key not in _cache:
        _cache[key] = load(key)
    return _cache[key]
```

**PASS**

```python
class Loader:
    def __init__(self, cache):
        self._cache = cache

    def get(self, key):
        if key not in self._cache:
            self._cache[key] = load(key)
        return self._cache[key]
```

**Counterpoint.** "A module global is the simplest cache." It is also unbounded and shared by everything. If you need one, bound it (LRU or TTL), inject it, and tie its lifetime to what it caches.

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
applies_when: The code adds or keeps an abstraction, parameter, hook or option.  
Backed by: Google, Wikimedia (MediaWiki), Microsoft, Shopify, NVIDIA. People cited: Kent C. Dodds, Martin Fowler, Henrik Warne.

**Rule.** Do not build an abstraction or capability for a need that does not exist yet; add it when the need or a second use appears.

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

**Counterpoint.** "But we will surely need it." Then add it when you do, in a change that has the real second caller to shape it. Optimising for easy change means simple code, not built-in flexibility. The cost of waiting is low, and the cost of the wrong guess is not. When the need is certain and a retrofit would be costly, as for a public API that cannot change later, weigh that cost before waiting.

## py-class-earns-its-instance

severity: discuss  
concerns: maintainability  
applies_when: A Python class has no state, only static methods, or a `Protocol` with one implementation.  
Backed by: Google. People cited: Pablo González.

**Rule.** Give a class real state or a collaborator; otherwise write a module function.

**Why.** A static-only class is a module with extra typing. A `Protocol` with one implementation is a speculative interface. A `Protocol` needs two or more real implementations swapped at runtime; see [mod-yagni](module.md#mod-yagni).

**FAIL**

```python
class DateUtils:
    @staticmethod
    def parse(s): ...
class Notifier(Protocol): ...   # one impl, ever
```

**PASS**

```python
dates.py:  def parse(s): ...
# use the concrete class until a second real impl exists
```

**Counterpoint.** "Protocols make testing easy." A fake of a concrete class in tests works with duck typing too. The Go review guide takes the same stance: declare interfaces where consumed, and avoid speculative ones.

## py-field-only-when-adds

severity: discuss  
concerns: correctness  
applies_when: A pydantic model or settings class uses `Field()`.  
Backed by: no organisation yet. People cited: Pablo González.

**Rule.** Use `Field()` only when it adds something (a constraint, an alias, or API docs), and set plain defaults directly.

**Why.** `Field(default=5.0)` is noise that hides which fields are constrained.

**FAIL**

```python
request_timeout_s: float = Field(default=5.0)
```

**PASS**

```python
request_timeout_s: float = 5.0
max_batch_size: int = Field(default=500, gt=0, le=2_000)
```

**Counterpoint.** "Uniform `Field` everywhere is consistent." Consistency that hides the constraints is not worth the scan cost. Every `Field` should tell the reader something.

## py-httpx-client-lifespan

severity: should-fix  
concerns: performance  
applies_when: A Python service creates an `httpx` client.  
Backed by: no organisation yet. People cited: Pablo González.

**Rule.** Pass an explicit `httpx.Timeout` to every `httpx` client.

**Why.** Core rules: [svc-timeouts](service.md#svc-timeouts), [mod-pooled-clients-built-once](module.md#mod-pooled-clients-built-once). `read=None` disables the read timeout. Build the client once in the app lifespan and reuse it.

**FAIL**

```python
async def fetch(url):
    async with httpx.AsyncClient(timeout=None) as c:
        return await c.get(url)
```

**PASS**

```python
@asynccontextmanager
async def lifespan(app):
    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0, connect=2.0)) as c:
        app.state.http = c
        yield
```

**Counterpoint.** "httpx defaults are fine." They are (5s), but set the value explicitly so that a library change cannot silently change behaviour.

## py-imports

severity: should-fix  
concerns: maintainability  
applies_when: A Python module has imports.  
Backed by: no organisation yet. People cited: Pablo González.

**Rule.** Put imports at module top, absolute only.

**Why.** Local imports hide dependencies and cycles. Relative imports break when files move. Importing a private name couples you to something its owner may change without notice. Never import a `_`-prefixed name from another module, and use `__all__` only in a re-export `__init__.py`.

**FAIL**

```python
def handler():
    from .helpers import _parse
```

**PASS**

```python
from app.billing.parsing import parse
```

**Counterpoint.** "Import inside the function avoids a cycle." It hides the cycle instead of fixing it, and the design needs a third module or a dependency inversion. A lazy import for a heavy optional dependency is the one defensible exception; document it with a reason.

## py-no-init-or-model-tests

severity: should-fix  
concerns: testing  
applies_when: The code adds `test_init_*` or a test file for a plain model or dataclass.  
Backed by: no organisation yet. People cited: Pablo González.

**Rule.** Cover `__init__` and plain models through the behaviour that uses them.

**Why.** Such tests restate the class and break on every field change without proving behaviour.

**FAIL**

```python
def test_init_sets_name(): assert User(name="a").name == "a"
```

**PASS**

```python
def test_welcome_email_uses_user_name(): ...
```

**Counterpoint.** "Validators on the model need tests." Yes: test the validator's behaviour (valid and invalid input), not that assignment works.

## py-test-hygiene

severity: discuss  
concerns: testing  
applies_when: A Python test uses the current date or time, or reaches the network.  
Backed by: no organisation yet. People cited: Pablo González.

**Rule.** Freeze time and block network in tests.

**Why.** Tests that depend on the clock or the network flake, and fail in CI at midnight or offline.

**FAIL**

```python
def test_token_expires():
    token = issue_token(ttl=60)
    assert token.expires_at > datetime.now()
```

**PASS**

```python
from freezegun import freeze_time

@freeze_time("2026-01-01 12:00:00")
def test_token_expires():
    token = issue_token(ttl=60)
    assert token.expires_at == datetime(2026, 1, 1, 12, 1)
# run with: pytest --disable-socket
```

**Counterpoint.** "Real time catches real bugs." It catches flakes. Test time-dependent logic with a frozen clock, and cover real-network behaviour in a separate, opt-in suite.

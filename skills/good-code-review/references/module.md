# module

## mod-behaviour-lives-with-state

severity: discuss  
concerns: maintainability  
applies_when: A function computes something only from one object's own fields.  
Backed by: Microsoft (unjudged), PMD (unjudged), NimblePros (DevIQ) (unjudged). Backing: unjudged.

**Rule.** Put the invariants and calculations that read only one object's fields on that object.

**Why.** A rule about one object scattered across services makes every caller learn where the rule lives, and the object cannot enforce it. Microsoft says an entity's methods "take care of the invariants and rules of the entity instead of having those rules spread across the application layer". PMD calls a data holder whose behaviour lives elsewhere a sign of "poor data-behaviour proximity". DevIQ says model objects should "use encapsulation to manage their internal state and behavior".

**FAIL**

```text
def order_total(order): return sum(l.price * l.qty for l in order.lines)
```

**PASS**

```text
class Order:
    def total(self): return sum(l.price * l.qty for l in self.lines)
```

**Counterpoint.** "Records, data classes and dataclasses are made to carry data." They are, and a carrier with no rules has nothing to move. The rule is about the calculation, not the declaration, so `total()` on a record does not stop it being a record. Keep the type a pure carrier when it holds only data. A simple CRUD context can keep a data-only model, and a functional design keeps behaviour in functions over data. The rule is for an object model.

## mod-bounded-fan-out

severity: discuss  
concerns: maintainability  
applies_when: A change adds imports or type references to a class, file or function that already depends on many others.  
tool gate: Microsoft CA1506 (95 types, 40 members), Checkstyle ClassFanOutComplexity (20), eslint-plugin-import import/max-dependencies (10), PMD CouplingBetweenObjects (20) and ExcessiveImports (30).  
Backed by: Microsoft (unjudged), Checkstyle (unjudged), eslint-plugin-import (unjudged), PMD (unjudged). Backing: unjudged.

**Rule.** Set a limit on how many other types or modules one unit depends on, and split a unit that passes it.

**Why.** A unit that depends on many others breaks when any of them changes and is hard to test, because each dependency needs a stand-in. eslint-plugin-import says "a module with too many dependencies is a code smell, and usually indicates the module is doing too much". Microsoft's rule gives the same reason: high class coupling is "difficult to maintain".

**FAIL**

```text
order_service.py: 46 imports (payments, shipping, tax, email, pdf, audit, 40 more)
```

**PASS**

```text
order_service.py: 9 imports; tax, shipping and notification each sit behind one module
eslint: "import/max-dependencies": ["error", { "max": 10 }]
```

**Counterpoint.** "The entry point has to import everything to wire it up." It does, so allowlist the composition root and nothing else. Microsoft's own page says to suppress the rule when the type "is considered maintainable despite its large number of dependencies".

## mod-class-size-budget

severity: discuss  
concerns: maintainability  
applies_when: One class or type passes the project's size limit for fields, public methods or lines, or the project sets no limit. A long file that holds several units belongs to code-file-lines-ceiling, and a module that mixes concepts is judged for cohesion, not size.  
tool gate: Pylint too-many-instance-attributes (R0902, max-attributes default 7) and too-many-public-methods (R0904, default 20), PMD NcssCount (classReportLevel default 1500) or GodClass, RuboCop Metrics/ClassLength (default 100).  
Backed by: Pylint (unjudged), PMD (unjudged), RuboCop (unjudged). Backing: unjudged.

**Rule.** Split a class that passes the project's size limit for fields, public methods or lines, unless it is a data record.

**Why.** A class that owns too much has too many reasons to change, and the project's linter should carry a limit for it. Pricing, tax, invoicing, dunning and notification in one type means five sets of fields, five test setups and a constructor nobody can call correctly. The linters count different things: fields, public methods, lines, source statements or a maintainability index. Any of them is a prompt to ask what the class owns. A data record with many fields is a different case, and a wide but cohesive API can be justified.

**FAIL**

```text
class BillingService:        # 25 fields, 40 public methods
    price(); tax(); invoice(); dunning(); notify()
```

**PASS**

```text
class Pricing: ...
class Tax: ...
class Invoice: ...
class Dunning: ...
class Notifier: ...
# each owns its state and stays under the project's limit
```

**Counterpoint.** "Splitting a large class leaves shallow pieces that call each other." That happens when the split follows methods instead of knowledge. Move the state with the methods that use it, and keep one thin entry point for callers. If the pieces would only forward, the class is not too large. It is one concept with a wide surface, and the limit is the wrong signal. A data record is judged by its shape, not by this card.

## mod-colour-tokens-meet-contrast

severity: should-fix  
concerns: accessibility, usability  
applies_when: A design-system module or theme defines foreground and background colour tokens.  
context: ui  
tool gate: axe `color-contrast` on rendered components; a unit test that computes the ratio for each token pair. axe cannot see text on images or gradients.  
Backed by: W3C (unjudged), Deque (unjudged), The A11y Project (unjudged), Apple (unjudged), Google (unjudged), WebAIM (unjudged). Backing: unjudged.

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

## mod-deep-modules

severity: discuss  
concerns: maintainability  
applies_when: A new class or module is introduced, or an existing interface grows.  
Backed by: Microsoft (unjudged), Rust project (unjudged), Google (unjudged). Backing: unjudged. People cited: Sébastien Portebois (unjudged), John Ousterhout (unjudged).

**Rule.** Prefer a small interface that hides its implementation, and add a member only when callers need it.

**Why.** An interface with too many members is hard to learn and hard to implement, and a public detail is a commitment you cannot change later. A shallow module, whose interface is nearly as complex as its implementation, charges the reader the cost of learning it and returns nothing. The complexity moves; it does not shrink.

**FAIL**

```text
class Reader:
    def open(self); def read_line(self); def set_encoding(self, e); def close(self)
    # caller must sequence all four; same work in a function would be one call
```

**PASS**

```text
def read_lines(path, encoding="utf-8") -> list[str]: ...
```

**Counterpoint.** Ousterhout and Martin disagree. Martin favours many very small functions, and Ousterhout says that yields shallow, entangled pieces. Evidence is thin on both sides. Ask the local question: does the split help a reader here?

## mod-derive-dont-duplicate

severity: should-fix  
concerns: compatibility, maintainability  
applies_when: A schema, spec, enum or list owns a shape that other code restates by hand.  
tool gate: Codegen from the schema, or a test that diffs the two lists.  
Backed by: Cursor (unjudged), Uber (unjudged), Stripe (unjudged), Spotify (unjudged). Backing: unjudged.

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

## mod-fowler-smells

severity: discuss  
concerns: maintainability  
applies_when: A reviewer sees long methods, feature envy, data clumps, primitive obsession, speculative generality, or divergent change.  
Backed by: Google (unjudged), GitLab (unjudged), Palantir (unjudged). Backing: unjudged. People cited: Sébastien Portebois (unjudged).

**Rule.** Name the smell, point to the line, and suggest the refactoring; do not file smells as taste.

**Why.** Smells are cheap to see and expensive to ignore, but a vague "this feels off" gives the author nothing to fix.

**FAIL**

```text
review: "This is messy."
```

**PASS**

```text
review: "should-fix: price_total reads only Order fields (feature envy). Move it to Order."
```

**Counterpoint.** "Smells are subjective." Yes: they signal; they do not prove. That is why the comment names the smell, the line, and the refactoring. "This is messy" gives the author nothing to act on.

## mod-inject-boundary-collaborators

severity: should-fix  
concerns: testing, maintainability  
applies_when: A class uses a database, HTTP, cloud or clock collaborator.  
Backed by: Microsoft (supports), Symfony (supports), Google (supports). Backing: strong.

**Rule.** Inject boundary collaborators through the constructor; do not construct them inside or reach for a global.

**Why.** Hard-wired collaborators force tests to patch module internals and tie the class to one environment.

**FAIL**

```text
class Billing:
    def charge(self, o): return StripeClient(KEY).charge(o)
```

**PASS**

```text
class Billing:
    def __init__(self, gateway): self._gateway = gateway
```

**Counterpoint.** "Injection everywhere is enterprise bloat." Inject only the boundary (DB, HTTP, cloud, clock). Internal collaborators stay plain and real in tests.

## mod-internals-unreachable

severity: should-fix  
concerns: maintainability  
applies_when: A module has an intended public surface, with internal files, symbols or members.  
tool gate: Import-boundary lint (import-linter, ESLint `no-restricted-imports`, package `exports`), Pylint protected-access (W0212).  
Backed by: Cursor (unjudged), Google (supports), Microsoft (supports), Refactoring.Guru (unjudged), Python Software Foundation (unjudged), Pylint (unjudged). Backing: mixed.

**Rule.** Keep a module's internals unimportable and untouched from outside it. A caller uses the public surface, not a private file or member.

**Why.** Anything a caller can import becomes the interface, and a field a caller writes becomes part of the contract. A naming convention such as a leading underscore stops no one, and the module can no longer change its internals without breaking callers.

**FAIL**

```python
from billing.internal.tax_tables import RATES   # nothing stops this
order._lines.append(line)                       # outside Order
```

**PASS**

```text
billing/__init__.py exports calculate_tax; import-linter contract forbids billing.internal.* from outside billing
order.add_line(line)
```

**Counterpoint.** "A boundary check is overhead for a small repo, and tests need internals." One lint contract is cheap, and the first outside import of an internal costs more. Tests may use a documented test-only export, and Java's qualified `exports ... to` or C#'s `InternalsVisibleTo` give them a door. For a single-file module, there is no inside to protect, so mark `N/A`.

## mod-law-of-demeter

severity: discuss  
concerns: maintainability  
applies_when: A change adds a call chain that reaches through one object to use another, such as order.customer().address().city().  
tool gate: PMD LawOfDemeter (trustRadius, default 1), JetBrains inspection LawOfDemeter.  
Backed by: PMD (unjudged), Google (unjudged), JetBrains (unjudged). Backing: unjudged.

**Rule.** Call methods on your direct collaborators, and do not call a method on an object that another call returned (a chain of two or more getters).

**Why.** A chain such as `order.customer().address().city()` ties the caller to the structure of three classes it does not own, so a change in any of them breaks it. PMD describes the rule as forbidding "fetching data from 'too far away'" to reduce coupling.

**FAIL**

```text
city = order.customer().address().city()
```

**PASS**

```text
city = order.shipping_city()      # Order owns how it finds the city
```

**Counterpoint.** "Fluent builders and stream pipelines chain by design." They return the same type or a value, so they do not expose structure. The rule targets getters that expose another object's parts. Every wrapper is code you now own. Pay that cost on the path that changes, and leave a stable library chain alone. The inspection ignores library calls by default. The law is a style guideline, which is why the severity is `discuss`. Use the project's tool setting as the threshold.

## mod-layers-point-inward

severity: should-fix  
concerns: maintainability  
applies_when: The codebase has separable transport, logic, and outbound-boundary code.  
tool gate: import-linter or similar  
Backed by: Microsoft (supports), AWS (supports), Netflix (supports). Backing: strong.

**Rule.** Make dependencies point inward: surface, then logic, then boundary.

**Why.** Once transport types leak into logic, you cannot reuse or test the logic without the transport, and a change to the API shape ripples into the rules. Name the layers for what they do (surface, logic, boundary).

**FAIL**

```text
service/orders.py:  def create(request: HttpRequest) -> HttpResponse
controller/orders.py: calls repository directly
```

**PASS**

```text
controller -> service -> repository      (imports only along this arrow)
service takes plain domain types
```

**Counterpoint.** "Three layers is ceremony for a CRUD app." For a ten-endpoint app, yes; fold them. The check applies once you have real logic. It asks only that dependencies not point outward, not that you build all three folders.

## mod-no-import-cycles

severity: should-fix  
concerns: maintainability  
applies_when: A change adds an import, dependency or project reference between modules, packages or build targets.  
tool gate: eslint-plugin-import import/no-cycle, Pylint R0401 (cyclic-import), Nx @nx/enforce-module-boundaries, or ArchUnit slices().should().beFreeOfCycles().  
Backed by: Google (unjudged), Rust project (unjudged), eslint-plugin-import (unjudged), Nx (unjudged), ArchUnit (unjudged), Pylint (unjudged). Backing: unjudged.

**Rule.** Keep the dependency graph between modules or packages acyclic, and break a cycle by moving the shared part into a third module that both depend on.

**Why.** Two modules that import each other cannot be built, tested or understood alone, and a change in one can break the other. Go rejects the cycle at compile time, Bazel defines its dependency graph as acyclic, and Cargo tells authors to split a package so it "remains strictly acyclic". Where the language allows the cycle, it still ties the two modules into one.

**FAIL**

```text
billing/invoice.py   imports  customers/account.py
customers/account.py imports  billing/invoice.py     # cycle
```

**PASS**

```text
billing/invoice.py     imports  customers/account.py
customers/account.py   imports  nothing from billing/
(shared types live in customers/types.py, which both import)
```

**Counterpoint.** "Python lets you import inside the function, so the cycle works." That hides the cycle at run time and leaves the two modules coupled. Apply the rule at the package or module boundary, where the toolchain or a lint rule can check it, and allow a documented exception for generated code or a test-only dependency.

## mod-no-import-side-effects

severity: should-fix  
concerns: testing, maintainability  
applies_when: A module does anything at import or load time other than defining names.  
Backed by: Apache Software Foundation (supports), Microsoft (supports), Dagster (supports), UK AI Security Institute (supports). Backing: strong.

**Rule.** Keep I/O at the edges: importing a package must not touch the network, read files, or read the environment.

**Why.** Import-time effects make tests slow and order-dependent, break tooling that merely imports the module, and fail in places that had no reason to need a network.

**FAIL**

```text
CLIENT = HttpClient(os.environ["API_URL"])   # at import
DATA = json.load(open("data.json"))
```

**PASS**

```text
def make_client(settings): return HttpClient(settings.api_url)
def load_data(path): ...
```

**Counterpoint.** "Loading once at import is fast." Load once at startup, explicitly, where the caller controls it and tests can substitute it.

## mod-no-logic-in-constructors

severity: should-fix  
concerns: correctness, testing  
applies_when: A constructor does work beyond assigning its arguments.  
Backed by: Microsoft (supports), Google (supports), Meta (supports). Backing: strong.

**Rule.** Assign only in constructors, and put I/O, parsing, and heavy computation in a named factory.

**Why.** A constructor with side effects makes every instantiation, including in tests, read a file or call an API. You need a real resource or a patch just to build the object.

**FAIL**

```text
class PriceList:
    def __init__(self, path):
        self._prices = json.loads(path.read_text())
```

**PASS**

```text
class PriceList:
    def __init__(self, prices): self._prices = prices
    @classmethod
    def from_file(cls, path): ...
```

**Counterpoint.** "A factory per class is ceremony." For a value object with no I/O, there is nothing to factor out. The rule targets constructors that read, call, or parse. With the factory, the test builds the object in one line.

## mod-no-module-mutable-state

severity: should-fix  
concerns: correctness, testing  
applies_when: A module defines a value that changes after load: a module-level variable, a list, dict, counter, cache, client or singleton.  
Backed by: Google (unjudged), Uber (unjudged), Microsoft (unjudged). Backing: unjudged.

**Rule.** Keep no mutable state at module level; hold it on an instance.

**Why.** Hidden global state leaks between tests, between requests, and between threads, and its order of mutation is unreadable. A mutable class or static field fails the same way, and the Google Python guide names class attributes as well. A frozen, load-once constant such as settings is the exception. A singleton used to dodge injection is not.

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

**Counterpoint.** "A module global is the simplest cache." It is also unbounded and shared by everything. If you need one, bound it (LRU or TTL), inject it, and tie its lifetime to what it caches. A rare, documented internal global behind functions can stay; say why in a comment.

## mod-no-shotgun-surgery

severity: discuss  
concerns: maintainability  
applies_when: A change to one rule, format or decision needs small edits in many classes or files.  
Backed by: Refactoring.Guru (unjudged), Microsoft (unjudged), NDepend (unjudged). Backing: unjudged.

**Rule.** Keep one decision in one module, and when a single change needs edits in many classes, move the scattered parts together.

**Why.** One change repeats in file after file, and the copy you miss is the defect. Refactoring.Guru describes the smell as "a single responsibility has been split up among a large number of classes". Microsoft says behaviour spread over several places is "a frequent source of errors" and asks for one construct to own it. NDepend says knowledge should exist in one place. The test is concrete: the same rule changes in the same set of files every time.

**FAIL**

```text
Adding a currency edits: pricing.py, invoice.py, tax.py, export.py, email.py, api.py, report.py
# the last two currency changes edited the same seven files
```

**PASS**

```text
Adding a currency edits: money.py   (rounding, formatting and tax rules live there)
```

**Counterpoint.** "A feature naturally touches many files." A new field does touch the model, the API and the UI. The smell is one internal rule that spreads. Duplication beats coupling to the wrong abstraction, and that is the limit: if the edits are unrelated decisions, merging them would create the wrong abstraction. The signal is that every change of this kind edits the same files.

## mod-no-utils-grab-bag

severity: should-fix  
concerns: maintainability  
applies_when: The diff adds or grows a module named `utils`, `helpers`, `common`, or `misc`.  
Backed by: Google (supports), GitLab (supports), Feature-Sliced Design (supports). Backing: strong. People cited: Sébastien Portebois (unjudged).

**Rule.** Put a helper in the module that owns the concept, or in a new module named after the concept.

**Why.** A grab-bag has no owner and no cohesion. It becomes the dependency of everything and the place where unrelated code accretes.

**FAIL**

```text
utils.py: parse_date, send_email, price_with_tax, retry
```

**PASS**

```text
dates.py, notifications.py, pricing.py, retry.py
```

**Counterpoint.** "Tiny helpers do not deserve a file." Then inline them where they are used (YAGNI applies). When one is shared, naming its concept is the work that makes it findable.

## mod-no-wrong-abstraction

severity: should-fix  
concerns: maintainability  
applies_when: A shared helper or base class has gained flags or conditionals so different callers can bend it.  
tool gate: Ruff FBT001 and FBT002 (boolean positional arguments) catch the usual first sign.  
Backed by: Shopify (unjudged), thoughtbot (unjudged), Astral (unjudged). Backing: unjudged. People cited: Sandi Metz (unjudged), Kent C. Dodds (unjudged), Sébastien Portebois (unjudged).

**Rule.** Inline an abstraction that has grown flags for its callers.

**Why.** Extract an abstraction when real call sites need it ([mod-yagni](module.md#mod-yagni)). A wrong one is harder to remove than the duplication it replaced, because each new caller adds a branch until nobody can say what the code is for. After you inline it, wait for the third similar caller before extracting again, so the new shape comes from real call sites.

**FAIL**

```text
def render(doc, *, as_pdf=False, for_email=False, legacy=False, skip_header=False): ...
```

**PASS**

```text
render_pdf(doc), render_email(doc)   # small, similar, independent
```

**Counterpoint.** Sources disagree. Ousterhout lists repetition as a red flag (one fact in many places), and the AHA/Sandi Metz line prefers duplication to a wrong abstraction. They fit together: dedupe knowledge (a rule, a format, a constant), wait on shape, and extract only when the second real caller shows what is shared.

## mod-one-name-per-concept

severity: should-fix  
concerns: maintainability  
applies_when: The change introduces or reuses names for domain concepts.  
Backed by: Ísland.is (supports), TUM ESI (supports), Microsoft (supports), Refactoring.Guru (unjudged). Backing: strong. People cited: Sébastien Portebois (unjudged).

**Rule.** Use one name for one concept across the codebase.

**Why.** If `customer`, `client`, and `account` all mean the same thing, readers wonder whether they differ. A name that misdescribes behaviour is worse than a vague one. Follow the project glossary, and never choose a name that says something the code does not do. Two classes that perform the same job under different method names make a reader learn the operation twice.

**FAIL**

```text
get_customer(); load_client(); fetch_account()   # same entity
UserRepo.fetch(id); AccountRepo.load(id)          # same lookup, two names
def profile_data(df): ...   # inspects column types, not performance
```

**PASS**

```text
get_customer(); load_customer(); fetch_customer()
UserRepo.get(id); AccountRepo.get(id)
def discover_structure(df): ...
```

**Counterpoint.** "Names are bikeshedding." Reviewers should not argue taste. They should check that the name is consistent and true. Vague names (names that could mean many things) are a design smell. Do not rename wholesale in a feature change; make the rename a separate change. An adapter at a boundary is exempt: its job is to present a different interface, and it should say which one it adapts.

## mod-pooled-clients-built-once

severity: should-fix  
concerns: performance  
applies_when: Code creates a network or database client.  
Backed by: Microsoft (unjudged), Google (unjudged), Requests project (unjudged), OpenJS Foundation (unjudged). Backing: unjudged.

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

## mod-proto-enum-zero-unspecified

severity: should-fix  
concerns: compatibility  
applies_when: A `.proto` file defines an enum.  
tool gate: Protobuf linter (`buf lint`, ENUM_ZERO_VALUE_SUFFIX).  
Backed by: Google (unjudged), Dropbox (unjudged), Buf (supports), Envoy (supports), OpenTelemetry (supports). Backing: strong.

**Rule.** Give every protobuf enum a zero value named `<ENUM>_UNSPECIFIED` with no real meaning.

**Why.** A reader that sees an unset or unknown field gets zero. If zero means a real state, such as `PAID`, a missing field reads as a payment.

**FAIL**

```proto
enum Status {
  PAID = 0;
  REFUNDED = 1;
}
```

**PASS**

```proto
enum Status {
  STATUS_UNSPECIFIED = 0;
  PAID = 1;
  REFUNDED = 2;
}
```

**Counterpoint.** "Zero as the common default saves a field on the wire." The saving is a byte on a field already at its most common value, and the cost is a silent wrong state. Published enums keep their numbers, so the fix for an existing enum is a new unspecified name only if no value has to be renumbered.

## mod-single-writer-per-state

severity: should-fix  
concerns: correctness  
applies_when: More than one module, worker or process writes the same state.  
Backed by: Cursor (unjudged), Netflix (unjudged), Cabify (unjudged), GitHub (unjudged). Backing: unjudged.

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
tool gate: A grep for `MODE_ECB`, `MODE_CBC` with no MAC, and nonces built from constants.  
Backed by: OWASP (unjudged), IETF (unjudged), NIST (unjudged), Google (unjudged). Backing: unjudged.

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
Backed by: Google (unjudged), Wikimedia (MediaWiki) (unjudged), Microsoft (unjudged), Shopify (unjudged), NVIDIA (unjudged), AWS (unjudged). Backing: unjudged. People cited: Kent C. Dodds (unjudged), Martin Fowler (unjudged), Henrik Warne (unjudged).

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
tool gate: ruff PLR6301 (partial), Pylint R0903 (min-public-methods=2, dataclasses exempt; it counts public methods, not state, so a static-only class with two methods passes)  
Backed by: Google (unjudged), Refactoring.Guru (unjudged), Pylint (unjudged). Backing: unjudged. People cited: Pablo González (unjudged).

**Rule.** Give a class real state or a collaborator; otherwise write a module function.

**Why.** A static-only class is a module with extra typing. A `Protocol` with one implementation is a speculative interface. A `Protocol` needs two or more real implementations swapped at runtime; see [mod-yagni](module.md#mod-yagni). Every class costs time to understand and maintain, so one that does too little should become a function. A class kept to mark future work is the same speculation: delete it, or name the plan and its owner. Pylint flags a class with too few public methods and shows a dataclass plus a function, or a larger API, as the fixes.

**FAIL**

```python
class DateUtils:
    @staticmethod
    def parse(s): ...
class TaxCalc:
    def total(self, order): return order.total   # no state, one method
class Notifier(Protocol): ...   # one impl, ever
```

**PASS**

```text
dates.py:  def parse(s): ...
tax.py:    def total(order): ...
# use the concrete class until a second real impl exists
```

**Counterpoint.** "Protocols make testing easy." A fake of a concrete class in tests works with duck typing too. Declare an interface where it is consumed, and avoid speculative ones.

## py-field-only-when-adds

severity: discuss  
concerns: correctness  
applies_when: A pydantic model or settings class uses `Field()`.  
Backed by: no organisation yet. People cited: Pablo González (unjudged).

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
Backed by: no organisation yet. People cited: Pablo González (unjudged).

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
tool gate: ruff I, TID252, PLC0415  
Backed by: no organisation yet. People cited: Pablo González (unjudged).

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
Backed by: no organisation yet. People cited: Pablo González (unjudged).

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

## py-pytest-expensive-fixture-scope

severity: should-fix  
concerns: testing, performance  
applies_when: A pytest or unittest suite builds a database, a container, a client or a model in a fixture that many tests use.  
tool gate: pytest --durations=10 --durations-min=1.0 to find the fixture, and a CI job timeout to hold the line.  
Backed by: pytest (unjudged), Python Software Foundation (unjudged), pytest-django (unjudged), SQLAlchemy (unjudged), Django Software Foundation (unjudged). Backing: unjudged. People cited: awesome-pytest-speedup (zupo) (unjudged).

**Rule.** Give an expensive pytest fixture `scope="session"` or `"module"` and isolate each test with a rollback, never a schema build or a seed load inside a function-scoped fixture.

**Why.** pytest destroys a function-scoped fixture after every test, and function scope is the default, so an expensive fixture pays its full cost for each test. A module or session scope pays it once. unittest has the same trade: `setUpClass` builds once per class, `setUp` once per test.

**FAIL**

```python
@pytest.fixture                       # scope defaults to "function"
def db():
    engine = create_engine(TEST_URL)
    Base.metadata.create_all(engine)  # ~25 s, repeated for every test
    seed_reference_data(engine)
    yield engine
    Base.metadata.drop_all(engine)
```

**PASS**

```python
@pytest.fixture(scope="session")
def engine():
    engine = create_engine(TEST_URL)
    Base.metadata.create_all(engine)  # ~25 s, once
    seed_reference_data(engine)
    yield engine
    engine.dispose()

@pytest.fixture
def db(engine):
    conn = engine.connect()
    tx = conn.begin()
    session = Session(bind=conn, join_transaction_mode="create_savepoint")
    yield session                     # milliseconds per test
    session.close()
    tx.rollback()
    conn.close()
```

In Django, `pytest-django` already does this: it builds the database once, runs each `db` test in a transaction that it rolls back, and `--reuse-db` skips the rebuild between runs.

**Counterpoint.** "A session fixture is shared, so one test can leak state into the next." That holds for mutable objects, which is why the PASS keeps the engine shared and gives each test its own rolled-back session. A fixture that cannot be reset stays at function scope. Python's own docs warn that shared fixtures break isolation and parallelism, so build the shared part read-only.

## py-test-hygiene

severity: discuss  
concerns: testing, reliability  
applies_when: A Python unit test touches the network, the shared filesystem, the database or the real clock. A per-test temporary directory (pytest `tmp_path`) is not the shared filesystem.  
tool gate: pytest-socket (`--disable-socket`), plus a unit-test CI job with no database service and no network credentials  
Backed by: Google (unjudged), Microsoft (unjudged), Spring (unjudged), GitLab (unjudged), Django Software Foundation (unjudged), Ruby on Rails (unjudged), Laravel (unjudged). Backing: unjudged. People cited: Pablo González (unjudged).

**Rule.** Keep unit tests off external I/O (the network, the shared filesystem and the database) and off the real clock, and run tests that need them in a separate, slower tier.

**Why.** A test that reaches the network, the disk or the database is slow and fails for reasons outside the code: an offline CI runner, a schema change, a clock at midnight. Those dependencies belong in an integration tier, where the failure is about the integration. Google's small tests cannot reach the network or disk; Microsoft's unit tests have no file system or database and control the clock through a seam; Django's `SimpleTestCase` blocks database queries by default.

**FAIL**

```python
def test_invoice_total(db):
    db.execute("insert into line ...")
    assert invoice_total(1) == 12.0

def test_token_expires():
    assert issue_token(ttl=60).expires_at > datetime.now()
```

**PASS**

```python
def test_invoice_total(fake_repo, frozen_clock):
    assert invoice_total(fake_repo) == 12.0

# pytest --disable-socket; the integration tests run in their own CI job
```

**Counterpoint.** "Most tests should hit the real stack, and mocking every collaborator hides real failures." Many teams keep most tests at the feature level and prefer real dependencies where they can keep them. Both hold: the rule is about the network, disk, database and clock boundary, not about doubling every collaborator. A feature or system test that boots the app belongs in the slower tier, and a team can run that tier on every merge. The unit tier stays fast and deterministic.

## py-xdist-worker-isolated-state

severity: should-fix  
concerns: testing, reliability  
applies_when: A pytest suite runs in parallel with pytest-xdist (`-n`) and its tests use a database or another shared resource.  
Backed by: pytest-xdist (unjudged), pytest-django (unjudged), Trail of Bits (unjudged). Backing: unjudged.

**Rule.** Under pytest-xdist, give each worker its own database or other mutable resource, keyed by `worker_id`, and build an expensive shared one once with a lock file.

**Why.** Each xdist worker collects its own tests, so a `session` fixture runs once per worker and not once per run. Workers that share one mutable database corrupt each other's tests, and the failures look random. PyPI's suite found this the moment it moved to `-n auto`; per-worker databases fixed it, and execution time fell from 191 s to 63 s.

**FAIL**

```python
@pytest.fixture(scope="session")
def pg_db():
    create_database("tests")      # all workers create and use the same "tests" database
    yield "tests"
```

**PASS**

```python
@pytest.fixture(scope="session")
def pg_db(worker_id):             # "gw0", "gw1", ... or "master" without xdist
    name = f"tests-{worker_id}"
    create_database(name)
    yield name
    drop_database(name)
```

**Counterpoint.** "Building a database per worker multiplies the setup cost." It does, by the number of workers, which is still far less than the number of tests. When one build is too slow even per worker, build it once under a file lock, as the xdist documentation shows, and copy it for each worker with a database template.

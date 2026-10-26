# function

## fn-aria-role-has-state-and-keys

severity: should-fix  
concerns: accessibility  
applies_when: A custom widget sets `role` or an `aria-*` attribute because no native element fits.  
backed by: W3C, Mozilla, Heydon Pickering, Deque, Google

**Rule.** When a native element cannot do the job, give the custom widget the state attribute and the keys its role promises.

**Why.** A role only tells assistive technology what the element is. It adds no keyboard behaviour, and it says nothing about state. A `role="switch"` with no `aria-checked` is announced as a switch of unknown state. Wrong ARIA is worse than none, because it gives a screen-reader user a false picture. The widget also needs an accessible name, from its text or a label, or it is announced by role alone.

**FAIL**

```jsx
<button type="button" role="switch" onClick={toggle}>Dark mode</button>
// no aria-checked: announced as a switch of unknown state
```

**PASS**

```jsx
<button type="button" role="switch" aria-checked={on} onClick={toggle}>
  Dark mode
</button>
// a native <button> already takes Tab, Enter, and Space
```

**Counterpoint.** "ARIA patterns are in the guide, so we copy them." Copy the keyboard table as well as the attributes. For a plain toggle, a `button` with `aria-pressed` is enough, and the label should stay the same when the state changes.

## fn-colour-not-sole-cue

severity: should-fix  
concerns: accessibility, usability  
applies_when: Styles or markup show an error, a required field, a status, or a link using colour.  
backed by: W3C, Nielsen Norman Group, Apple, Heydon Pickering

**Rule.** Pair every colour that carries meaning with a second cue: text, an icon, a shape, or an underline.

**Why.** Colour-blind users, glare, greyscale mode, and a screen reader all remove colour. A red border on a bad field, or a link that differs from body text only by hue, tells those users nothing.

**FAIL**

```css
.field.error { border-color: red; }
.status-ok   { color: green; }
a { color: #0a58ca; text-decoration: none; }   /* no underline, no hover or focus cue */
```

**PASS**

```html
<input aria-invalid="true" aria-describedby="e1" style="border: 2px solid #b42318">
<p id="e1" class="error"><svg aria-hidden="true">…</svg> Error: enter a date such as 27/03/2026</p>
<a href="/terms" style="text-decoration: underline">terms</a>
```

**Counterpoint.** "Colour is the quickest cue, and the icon clutters the design." Colour can stay as the fast cue. The rule asks for a second one, not for removing the first. A text prefix such as "Error:" costs a few characters. A link in body text can also pass with 3:1 contrast against the text around it plus a non-colour cue on hover and focus. The underline is the simpler fix.

## fn-comments-explain-why

severity: should-fix  
concerns: maintainability  
applies_when: A comment sits next to code, or the code needs one to be understood.  
backed by: Sébastien Portebois, Google, John Ousterhout, Henrik Warne

**Rule.** Write comments that give a reason, a constraint, or a trade-off; rename before commenting, and never restate what the next line does.

**Why.** A restating comment rots silently and adds nothing. A missing reason makes the next person delete the code that mattered.

**FAIL**

```text
counter += 1  # increment the counter
retry = False  # see the PR, currently disabled
```

**PASS**

```text
# Business decision: activation and entitlement update in one transaction,
# so a user never has access without an active subscription.
# TODO: remove when billing emits entitlement events itself.
```

**Counterpoint.** "Good names make comments unnecessary." Names carry *what*. They cannot carry why a branch exists, a unit, or what callers may rely on, and a missing reason costs more than a slightly stale one. Rename first, then comment what the name cannot say. A stale comment is a defect either way. The test is whether the comment adds information that the code cannot carry.

## fn-confine-file-path

severity: block  
concerns: security  
applies_when: Code opens, reads, writes or deletes a file whose name or path includes request data.  
backed by: OWASP, Google, GitHub

**Rule.** Resolve the final path and check that it stays inside the intended base directory before using it.

**Why.** A name like `../../etc/passwd`, or its percent-encoded form, walks out of the upload folder. Stripping `../` fails against `....//` and double encoding. The reliable check works on the resolved path. Better still, map a user choice to an ID and build the path in code.

**FAIL**

```python
return send_file(os.path.join(UPLOADS, request.args["name"]))
```

**PASS**

```python
p = (UPLOADS / request.args["name"]).resolve()
if not p.is_relative_to(UPLOADS.resolve()): abort(400)
return send_file(p)
```

**Counterpoint.** "We already strip `..`." String stripping is a blocklist and gets bypassed. Resolve first, compare second. Resolving catches a symlink that already points outside, but a symlink swapped in between the check and the open still escapes. For trees that untrusted users can write to, use a rooted open such as Go's `os.OpenInRoot`, which refuses any escape at open time.

## fn-csprng-for-secrets

severity: block  
concerns: security  
applies_when: Code generates a token, session ID, password-reset code, API key, nonce or IV.  
backed by: OWASP, Python Software Foundation, Mozilla, IETF, Google

**Rule.** Draw every security-relevant random value from the platform CSPRNG.

**Why.** A general-purpose PRNG is predictable from a few outputs, so an attacker who sees two tokens can guess the next. UUIDv1 is time-based and also not secret. The API call is the whole fix, so it is cheap to demand.

**FAIL**

```python
token = "".join(random.choices(string.ascii_letters, k=32))
reset = str(int(time.time()))
```

**PASS**

```python
token = secrets.token_urlsafe(32)           # os.urandom under the hood
# JavaScript: crypto.getRandomValues(new Uint8Array(32))
```

**Counterpoint.** "Math.random is fine for a short-lived code." Short-lived codes still get brute-forced, and predictable ones need no brute force. Use the CSPRNG for anything an attacker gains from guessing.

## fn-destructive-confirm-or-undo

severity: should-fix  
concerns: usability  
applies_when: A handler deletes user data, spends money, or sends something that cannot be recalled.  
backed by: Nielsen Norman Group, Apple, W3C, Ben Shneiderman

**Rule.** Make a destructive action reversible with undo, or ask the user to confirm it before it runs.

**Why.** People click the wrong thing. If the action cannot be reversed and nothing stops it, one slip deletes their work. Undo costs a successful user nothing, while a dialog on every click trains them to click through. A dialog works best when its buttons name the outcome, such as "Delete project" and "Cancel", because "OK" and "Are you sure?" say nothing about what happens next.

**FAIL**

```jsx
<button onClick={() => api.deleteProject(id)}>Delete</button>
```

**PASS**

```jsx
async function remove() {
  await api.softDelete(id);
  toast("Project deleted", { action: { label: "Undo", onClick: () => api.restore(id) } });
}
// irreversible case: a dialog "Delete project “Q3 plan”?" with buttons "Delete project" and "Cancel"
```

**Counterpoint.** "Confirm everything to be safe." Frequent prompts are dismissed without reading, so they protect nothing. Use undo for common actions and reserve the dialog for rare, irreversible ones. Do not make Cancel the default button.

## fn-dialog-focus-managed

severity: block  
concerns: accessibility, usability  
applies_when: A component opens a modal dialog, drawer, or menu that covers the page.  
backed by: W3C, Mozilla, WebAIM

**Rule.** When a modal opens, move focus into it and keep Tab inside it. Make Escape close it.

**Why.** Without it, a keyboard user keeps tabbing through the page behind the dialog, or gets stuck inside it with no exit. When it closes, return focus to the control that opened it. Focus that falls to the top of the page makes them start over.

**FAIL**

```jsx
{open && <div className="modal"><h2>Delete?</h2><button onClick={del}>Delete</button></div>}
```

**PASS**

```html
<button id="opener">Delete project</button>
<dialog id="dlg" aria-labelledby="t"><h2 id="t">Delete project?</h2>
  <button autofocus>Cancel</button> <button>Delete</button></dialog>
<script>
  const opener = document.getElementById("opener"), dlg = document.getElementById("dlg");
  opener.onclick = () => dlg.showModal();   // focus moves in, page behind is inert
  dlg.onclose = () => opener.focus();       // focus returns to the opener
</script>
```

**Counterpoint.** "Our library handles it." Check, because a library that traps focus but never restores it is common. Prefer the native `<dialog>` with `showModal()`, which makes the page inert and closes on Escape. A dialog built from generic elements must recreate each of those.

## fn-disclosure-hides-only-secondary

severity: should-fix  
concerns: usability  
applies_when: Markup or a component hides content behind a `<details>`, an accordion, a "Show more" link, or an "Advanced" toggle.  
backed by: Nielsen Norman Group, GOV.UK, Appian

**Rule.** Do not hide a required field, the primary action, or information most users need behind a disclosure that starts closed.

**Why.** Users who never open the disclosure must still be able to finish the task. A closed `<details>` that holds the delivery date, or an "Advanced" section that holds a required field, sends most users hunting. Disclosure is for what only some users need. A field that appears because of the user's own answer, such as a follow-up field shown after they pick "Yes", is a conditional reveal, not a disclosure, and passes. Nesting adds its own cost. NN/g counts the first view as level one, so a disclosure inside a disclosure is already level three, and NN/g found designs past two levels lose people as they move between levels. In a step-by-step flow, such as picking a make and then a model, Appian says to disable fields that are not ready yet rather than hide them.

**FAIL**

```html
<details>
  <summary>Delivery options</summary>
  <label for="address">Delivery address</label>
  <input type="text" id="address" required>
</details>
```

**PASS**

```html
<label for="address">Delivery address</label>
<input type="text" id="address" required>
<details>
  <summary>Add an order reference</summary>
  <label for="ref">Order reference</label>
  <input type="text" id="ref">
</details>
```

**Counterpoint.** "Hiding fields makes the form shorter." It makes the first view shorter, but required content still has to be found. Measure who opens the disclosure. If most users open it, the content belongs on the default view.

## fn-error-says-what-and-how

severity: should-fix  
concerns: usability, accessibility  
applies_when: Code builds the message shown when user input fails validation.  
backed by: Nielsen Norman Group, GOV.UK, W3C, USWDS, Ben Shneiderman

**Rule.** Show each validation error next to its field, in plain words that name what is wrong and how to fix it.

**Why.** "Invalid input" or an error code leaves the user to guess which field and what to change. A message at the top of a long form, or in a toast that fades, sends a magnifier user searching. Naming the fix is the shortest path to a valid form.

**FAIL**

```html
<input id="dob" name="dob" class="red">
<div class="toast">Error 422: invalid data</div>
```

**PASS**

```html
<label for="dob">Date of birth</label>
<p id="dob-err"><span class="visually-hidden">Error:</span>
   Enter a date of birth in the past, such as 27 3 1986</p>
<input id="dob" name="dob" aria-invalid="true" aria-describedby="dob-err">
```

**Counterpoint.** "Detailed messages leak information." For a login, that is true: say "Email or password is wrong". For ordinary fields, the specific message is the fix. Hold back the suggestion only where it would weaken security.

## fn-fetch-only-needed-data

severity: should-fix  
concerns: performance  
applies_when: A function queries a database or an API and then filters, counts, or sums the result in application code.  
backed by: Microsoft, Django Software Foundation, Markus Winand, SQLAlchemy

**Rule.** Filter, count, and aggregate in the query, and select only the columns the code uses.

**Why.** Loading every row to count it, or every column to read one, moves data across the network and through memory for nothing. `SELECT *` also rules out an index-only scan.

**FAIL**

```python
total = sum(o.amount for o in Order.objects.all() if o.status == "paid")
n = len(Order.objects.filter(user=u))        # loads every row
emails = [u.email for u in User.objects.all()]   # loads every column
```

**PASS**

```python
total = Order.objects.filter(status="paid").aggregate(Sum("amount"))["amount__sum"]
n = Order.objects.filter(user=u).count()
emails = User.objects.values_list("email", flat=True)
```

**Counterpoint.** "Pushing logic into the database makes it the bottleneck." It does for formatting and business rules. Filtering and aggregation are what the database is built for, and moving them out usually ships far more data than it saves.

## fn-focus-indicator-visible

severity: block  
concerns: accessibility, usability  
applies_when: Styles or script change `outline`, `:focus`, or `:focus-visible`.  
backed by: W3C, Google, WebAIM, The A11y Project

**Rule.** Keep a visible focus indicator on every focusable element. Never set `outline: none` without a replacement.

**Why.** A keyboard user finds their place by the focus ring. Remove it and they navigate blind. A sticky header that covers the focused link has the same effect once they tab down the page. `scroll-padding-top` on `html`, as tall as the header, keeps the focused element in view.

**FAIL**

```css
*:focus { outline: none; }
a:focus { outline: 0; }
```

**PASS**

```css
:focus-visible { outline: 3px solid #1a56db; outline-offset: 2px; }
```

**Counterpoint.** "Designers dislike the ring on mouse clicks." `:focus-visible` shows the ring for keyboard focus and hides it for most mouse clicks. Restyle the ring if you must. Do not remove it.

## fn-form-control-has-label

severity: block  
concerns: accessibility, usability  
applies_when: Markup or a component renders an input, a select, or a textarea.  
backed by: W3C, Mozilla, Deque, The A11y Project, jsx-eslint project

**Rule.** Tie every form control to a visible `<label>`, with `for` and a matching `id` or by wrapping it. A placeholder is not a label.

**Why.** A screen reader announces a bare field as "edit text". Voice-control users cannot say its name. A label also enlarges the click target. A placeholder vanishes when the user types, so it fails every user who looks away and comes back.

**FAIL**

```html
<input type="email" placeholder="Email">
<div class="label">Name</div>
<input type="text" id="name">
```

**PASS**

```html
<label for="email">Email</label>
<input type="email" id="email" autocomplete="email">

<label>Name <input type="text" name="name" autocomplete="name"></label>
```

**Counterpoint.** "The design shows a floating placeholder label." A floating label is a real label if it stays visible and is wired to the input. Use `aria-label` only where the purpose is already visible, such as a search field next to a Search button.

## fn-heading-structure

severity: should-fix  
concerns: accessibility, usability  
applies_when: Markup or a component renders a title or a section heading.  
backed by: W3C, Mozilla, The A11y Project

**Rule.** Mark every heading with a real `<h1>` to `<h6>` element, not a styled `div`, `span`, or `p`.

**Why.** Screen-reader users jump from heading to heading to scan a page. A `div` styled as a heading is invisible to that. Pick the level from the outline, not from the size you want: a skipped level, such as `h2` to `h4`, makes the outline look as if a section is missing.

**FAIL**

```html
<div class="title-large">Account</div>
<p><b>Billing</b></p>
<span class="bold">Invoices</span>
```

**PASS**

```html
<h1>Account</h1>
<h2>Billing</h2>
<h3>Invoices</h3>
<!-- size comes from CSS: h2 { font-size: 1rem } -->
```

**Counterpoint.** "The design needs a small `h2`." That is a CSS problem. Keep the level that matches the outline and set the size in the stylesheet. Jumping back up a level, such as `h4` to `h2`, is fine when a section ends.

## fn-img-alt-text

severity: should-fix  
concerns: accessibility  
applies_when: Markup or a component renders an image, an icon, or a chart.  
backed by: W3C, Mozilla, Deque, The A11y Project, jsx-eslint project

**Rule.** Give every `<img>` an `alt` attribute: text that serves the image's purpose, or `alt=""` when the image is decorative.

**Why.** A screen reader has nothing to say about an image with no `alt`, and often reads the file name instead. An informative image with an empty `alt` hides its content. A decorative image with a long `alt` adds noise to every page view.

**FAIL**

```html
<img src="/img/IMG_0042.jpg">
<img src="/img/chart.png" alt="chart">
<img src="/img/divider.png" alt="divider line">
<button><img src="/img/trash.svg"></button>
```

**PASS**

```html
<img src="/img/q3-revenue.png" alt="Revenue grew from 4.1 to 5.3 million in Q3">
<img src="/img/divider.png" alt="">
<button><img src="/img/trash.svg" alt="Delete draft"></button>
```

**Counterpoint.** "A linter already checks `alt`." It checks that the attribute exists, not that the text fits the image or the context. Review the text itself. For a chart, give a short `alt` plus the data nearby as text.

## fn-independent-work-concurrent

severity: should-fix  
concerns: performance, correctness  
applies_when: A function awaits or calls several I/O operations that do not depend on each other.  
backed by: Google, Cursor, Python Software Foundation, Mozilla

**Rule.** Start independent I/O together and wait for all of it; run calls in sequence only when one needs the result of another.

**Why.** Sequential awaits add their latencies. Three 200 ms calls take 600 ms in a row and 200 ms together.

**FAIL**

```python
user = await get_user(uid)
orders = await get_orders(uid)       # does not use `user`
prefs = await get_prefs(uid)
```

**PASS**

```python
user, orders, prefs = await asyncio.gather(
    get_user(uid), get_orders(uid), get_prefs(uid))
```

**Counterpoint.** "Parallel calls load the dependency harder and complicate errors." Cap fan-out with a semaphore or pool, and use a task group so one failure cancels the rest. A deliberate order, for rate limits or ordering, is a valid reason. Write it down.

## fn-join-dont-concat-in-loop

severity: should-fix  
concerns: performance  
applies_when: A function builds a string from pieces in a loop whose length depends on input.  
backed by: Python Software Foundation, Google, Microsoft

**Rule.** Build a string from a loop with a builder or a join, never with repeated `+=`.

**Why.** Strings are immutable in Python, Go, Java, and .NET, so each `+=` copies everything built so far. Over n pieces the total cost grows with the square of the output length.

**FAIL**

```python
out = ""
for row in rows:
    out += f"{row.id},{row.name}\n"
```

**PASS**

```python
out = "".join(f"{row.id},{row.name}\n" for row in rows)
```

**Counterpoint.** "CPython optimises `+=` in place." Sometimes: only in CPython, and only while nothing else holds a reference to the string. Code that leans on it turns quadratic on other runtimes. A small fixed number of pieces is fine with `+` or an f-string, which read better. The rule covers loops over input-sized data.

## fn-jwt-verify-pinned

severity: block  
concerns: security  
applies_when: Code accepts a JWT as proof of identity or permission.  
backed by: IETF, OWASP, Microsoft, Google, GitHub, PyJWT project

**Rule.** Verify the signature against a fixed list of accepted algorithms, and check `iss` and `aud`, before reading any claim.

**Why.** If the verifier takes the algorithm from the token header, an attacker picks `none` or turns an RSA public key into an HMAC secret. Claims read before verification are attacker text. Pinning the algorithm and binding each key to one algorithm closes both. Also require `exp`, so a stolen token stops working.

**FAIL**

```python
claims = jwt.decode(token, options={"verify_signature": False})
claims = jwt.decode(token, key)               # PyJWT 1.x: algorithm taken from the header
```

**PASS**

```python
claims = jwt.decode(token, key, algorithms=["RS256"],
                    issuer=ISSUER, audience=AUD,
                    options={"require": ["exp", "iss", "aud"]})
```

**Counterpoint.** "Our gateway already verifies the token." Then the service trusts a header that any internal caller can forge. Verify at each trust boundary, or prove that only the gateway can reach the service.

## fn-keep-input-on-error

severity: should-fix  
concerns: usability  
applies_when: A form handler or component re-renders after a failed validation or a failed submit.  
backed by: Nielsen Norman Group, GOV.UK, Baymard Institute, Ben Shneiderman

**Rule.** After a failed validation or submit, show the form again with every value the user entered, correct or not.

**Why.** A form that wipes its fields turns one typo into ten minutes of retyping, and some users give up. The user fixes one field, not the whole page.

**FAIL**

```jsx
async function submit(e) {
  e.preventDefault();
  const res = await post("/signup", values);
  if (!res.ok) { setErrors(res.errors); setValues(EMPTY); }
}
```

**PASS**

```jsx
async function submit(e) {
  e.preventDefault();
  const res = await post("/signup", values);
  if (!res.ok) setErrors(res.errors);   // values stay as typed
}
```

**Counterpoint.** "Clear a password or card number on error for safety." That is a fair exception for secrets, and the message should say so. Everything else the user typed stays.

## fn-label-above-field

severity: discuss  
concerns: usability, accessibility  
applies_when: Markup or styles lay out a form field and its visible label.  
backed by: GOV.UK, Atlassian, Nielsen Norman Group, W3C

**Rule.** Put the visible label of a text input, select, or textarea directly above it.

**Why.** A label sitting below a field, or halfway between two fields, gets read as the label of the wrong one. W3C notes that a label above the field cuts sideways scrolling for low-vision and phone users, who can lose a side label off the edge of the screen. Hint and error text can go between the label and the field. A help link, a button, or another field cannot. Checkboxes and radios are the exception: W3C puts the control first and its label to the right, in left-to-right languages.

**FAIL**

```html
<input type="text" id="town">
<label for="town">Town or city</label>
```

**PASS**

```html
<label for="town">Town or city</label>
<input type="text" id="town" autocomplete="address-level2">

<label for="postcode">Postcode</label>
<p id="postcode-hint">For example, SW1A 2AA</p>
<input type="text" id="postcode" aria-describedby="postcode-hint">
```

**Counterpoint.** "Labels to the left fit our long desktop admin form better." Labels beside the field are an accepted convention for very long desktop forms. Accept a left label on such a form if it stays next to its own field at every breakpoint. A wrapping label, as in the `fn-form-control-has-label` PASS, passes when CSS sets the label text to `display: block` so it sits above the field. A label below the field is still a `FAIL`. This card covers placement only. `fn-form-control-has-label` covers the code tie between label and field.

## fn-native-button-or-link

severity: block  
concerns: accessibility, usability  
applies_when: A component handles a click or tap, or navigates.  
backed by: W3C, Mozilla, WebAIM, jsx-eslint project, Don Norman

**Rule.** Use `<button>` for an action and `<a href>` for navigation. Do not attach a click handler to a `div`, `span`, or `a` with no `href`.

**Why.** A `div` is not in the tab order, has no role, and ignores Enter and Space. A keyboard or screen-reader user cannot reach or operate it. A fake link also loses open-in-new-tab and copy-link. A native element gives all of that with no code.

**FAIL**

```jsx
<div className="btn" onClick={save}>Save</div>
<a href="#" onClick={openMenu}>Menu</a>
<span onClick={() => navigate("/billing")}>Billing</span>
```

**PASS**

```jsx
<button type="button" onClick={save}>Save</button>
<button type="button" onClick={openMenu}>Menu</button>
<a href="/billing">Billing</a>
```

**Counterpoint.** "Native buttons are hard to style." They are not: reset `border`, `background`, and `font` on the element. Rebuilding the keyboard, role, and focus behaviour by hand costs more and fails more often. Where a custom widget is unavoidable, follow the WAI-ARIA Authoring Practices pattern for it.

## fn-no-blocking-call-in-async-code

severity: block  
concerns: performance, correctness  
applies_when: Code runs on an event loop or an async runtime (asyncio, Node.js, Tokio, ASP.NET async handlers).  
backed by: Python Software Foundation, OpenJS Foundation, Tokio project, Microsoft

**Rule.** Never make a blocking I/O call or run long CPU work directly in async code; use the async API or hand the work to a thread or worker.

**Why.** An event loop runs one callback at a time. A `time.sleep`, a synchronous HTTP call, or a big hash inside a handler stalls every other request on that loop, not just the slow one.

**FAIL**

```python
async def handler(req):
    data = requests.get(url).json()          # blocks the loop
    digest = hashlib.pbkdf2_hmac("sha256", pw, salt, 600_000)
```

**PASS**

```python
async def handler(req):
    data = (await client.get(url)).json()    # httpx.AsyncClient
    digest = await asyncio.to_thread(hashlib.pbkdf2_hmac, "sha256", pw, salt, 600_000)
```

**Counterpoint.** "This call is fast enough." A short read from a local SSD can be quicker synchronously. Measure it with asyncio debug mode or the runtime's equivalent. A call that crosses the network, or that waits on anything outside the process, is never in that class.

## fn-no-eval-untrusted

severity: block  
concerns: security  
applies_when: Code runs `eval`, `exec`, or `new Function`, or compiles a template, and some of the text comes from a request, a file, a database row, or model output.  
backed by: OWASP, MITRE, Mozilla, PortSwigger, GitHub

**Rule.** Never pass untrusted text to `eval`, `exec`, `new Function`, or a template compiler. Pass it to a fixed template or a parser as data.

**Why.** Each of these turns a string into code that runs with the server's rights, so one field becomes remote code execution. A template engine counts: `render_template_string(request.args["msg"])` lets `{{ config }}` or worse run on the server. An expression language, such as SpEL, carries the same risk. Parse the data format instead (`json.loads`, `ast.literal_eval`), and keep templates in files the author wrote, with user values passed as variables.

**FAIL**

```python
total = eval(request.args["expr"])
html = render_template_string("Hello " + request.args["name"])
```

**PASS**

```python
data = json.loads(request.get_data())
html = render_template("hello.html", name=request.args["name"])
```

**Counterpoint.** "Users need formulas, so we need `eval`." Write or adopt a small expression parser that knows only numbers and the operators you allow. A sandbox around `eval` loses to the next escape someone publishes.

## fn-no-mass-assignment

severity: block  
concerns: security  
applies_when: A handler copies request fields into a model, ORM entity or settings object.  
backed by: OWASP, Microsoft, Ruby on Rails, Django Software Foundation

**Rule.** Bind request data to a DTO or an explicit field allowlist, never straight onto the model.

**Why.** When the model has `is_admin`, `balance` or `owner_id`, a client that adds those keys to the JSON body sets them. A blocklist fails the day someone adds a new sensitive column. The allowlist still needs the object-level check from [fn-object-level-authz](function.md#fn-object-level-authz).

**FAIL**

```text
user = User(**request.json)          # body {"name": "a", "is_admin": true}
user.save()
```

**PASS**

```text
class UserIn(BaseModel):            # only editable fields exist here
    name: str
user = User(**UserIn(**request.json).model_dump())
```

**Counterpoint.** "A DTO per endpoint is boilerplate." Generate DTOs from the API schema. The boilerplate costs less than one privilege escalation.

## fn-no-native-deserialise-untrusted

severity: block  
concerns: security  
applies_when: Code turns bytes or text from outside the process into objects.  
backed by: OWASP, Python Software Foundation, Microsoft, Oracle, GitHub

**Rule.** Parse untrusted input with a data-only format, never with a native object deserialiser.

**Why.** `pickle`, `ObjectInputStream`, `BinaryFormatter` and full-power YAML loaders can run attacker-chosen code while they load, so validating after the call is too late. JSON cannot instantiate arbitrary classes. Validate the parsed data against a schema afterwards, as the PASS does.

**FAIL**

```python
obj = pickle.loads(request.data)
cfg = yaml.load(body, Loader=yaml.Loader)
```

**PASS**

```python
obj = Model.model_validate_json(request.data)
cfg = yaml.safe_load(body)
```

**Counterpoint.** "The data comes from our own queue." Anyone who can write to the queue can run code on every consumer, so the queue is a trust boundary. Signing the payload, or a Java serialisation filter that allowlists classes, narrows the risk while you migrate. The call still fails this check until it reads a data-only format.

## fn-no-positive-tabindex

severity: should-fix  
concerns: accessibility, usability  
applies_when: Markup sets `tabindex`, or a layout reorders content with CSS.  
backed by: W3C, Google, WebAIM, The A11y Project

**Rule.** Write the DOM in reading order and never set `tabindex` above 0.

**Why.** A positive `tabindex` jumps those elements to the front of the tab order, ahead of everything else on the page. Each new control then needs a new number, and the order stops matching what the user sees. CSS that moves items visually without moving them in the DOM does the same thing.

**FAIL**

```html
<input name="last" tabindex="2">
<input name="first" tabindex="1">
<button tabindex="3">Save</button>
```

**PASS**

```html
<input name="first">
<input name="last">
<button>Save</button>
<!-- tabindex="0" only to add a custom widget to the order; tabindex="-1" to focus it from script -->
```

**Counterpoint.** "The visual layout puts the sidebar first, but the main content comes first in the DOM." Reorder the DOM to match, or accept the difference only if the order still makes sense to a keyboard user. Do not patch it with numbers.

## fn-no-prototype-pollution

severity: block  
concerns: security  
applies_when: JavaScript or TypeScript code merges, clones, or assigns properties whose key names come from JSON, a query string, or other untrusted input.  
backed by: OWASP, MITRE, PortSwigger, GitHub, Snyk

**Rule.** Never write an untrusted key into a plain object. Use a `Map`, an object from `Object.create(null)`, or an allowlist of keys.

**Why.** `obj[key] = value` with `key` set to `__proto__` writes to `Object.prototype`, so every object in the process gains that property. An attacker who sets `isAdmin` or a template option there can skip checks or reach code execution. The bug sits in generic helpers such as deep merge and path setters, so one bad helper exposes every caller. Blocking `__proto__`, `constructor`, and `prototype` inside a deep merge helps, but a blocklist misses obfuscated keys, so treat it as a stopgap.

**FAIL**

```javascript
function merge(dst, src) {
  for (const k in src) {
    if (typeof src[k] === "object") merge(dst[k] ??= {}, src[k]);
    else dst[k] = src[k];
  }
}
merge(settings, JSON.parse(body));   // body: {"__proto__": {"isAdmin": true}}
```

**PASS**

```javascript
const ALLOWED = new Set(["theme", "lang"]);
const prefs = new Map();
for (const [k, v] of Object.entries(JSON.parse(body))) {
  if (ALLOWED.has(k)) prefs.set(k, v);
}
```

**Counterpoint.** "Just freeze `Object.prototype` at startup." That helps, but it can break libraries that patch prototypes, and it leaves `constructor.prototype` paths in class instances open. Fix the merge, and add the freeze on top if your dependencies allow it.

## fn-no-raw-html-sink

severity: block  
concerns: security  
applies_when: Code writes a string into a page, a template or a rendered model-output view.  
backed by: OWASP, Mozilla, Meta, Google, CISA

**Rule.** Write untrusted text through an encoding sink (`textContent`, auto-escaped template), never through a raw HTML sink.

**Why.** One `innerHTML` of a username or of model output runs the attacker's script with the victim's session. Encoding must match the context: body, attribute, script string and URL each differ. Framework escape hatches such as `dangerouslySetInnerHTML` have the same effect.

**FAIL**

```text
el.innerHTML = comment.body;
<div dangerouslySetInnerHTML={{ __html: reply }} />
```

**PASS**

```text
el.textContent = comment.body;
<div>{reply}</div>                       // escaped by the framework
// user-authored HTML: DOMPurify.sanitize(html), nothing edited afterwards
```

**Counterpoint.** "We need to render rich text." Then sanitise with a maintained library such as DOMPurify at render time and add a CSP as a second layer. A CSP alone is not a fix, because it is defence in depth.

## fn-no-shell-with-input

severity: block  
concerns: security  
applies_when: Code starts a process and some part of the command comes from a request, a file or model output.  
backed by: OWASP, Python Software Foundation, Google, CISA

**Rule.** Start processes with the program and each argument as separate list items, and never through a shell string.

**Why.** A shell reads `;`, `|` and `$()` as commands, so a filename of `a; rm -rf ~` runs. Argument arrays skip the shell. The values still need validation, since an argument beginning with `-` becomes an option; end options with `--` where the tool allows it.

**FAIL**

```python
os.system("convert " + upload_name + " out.png")
subprocess.run(f"git log {branch}", shell=True)
```

**PASS**

```python
subprocess.run(["convert", upload_path, "out.png"], check=True)   # upload_path is a server-generated name
subprocess.run(["git", "log", branch], check=True)   # branch checked against an allowlist
```

**Counterpoint.** "We need shell features like pipes." Chain two `subprocess` calls in code, or use the library that does the job. If a shell is unavoidable, build the string only from constants.

## fn-object-level-authz

severity: block  
concerns: security  
applies_when: A handler loads, changes or deletes a record by an ID that comes from the request.  
backed by: OWASP, Microsoft, Cloudflare, NIST

**Rule.** Check that the caller may act on the specific record before returning or changing it.

**Why.** A login proves who the caller is, not which records they own. Without a per-object check, changing `id=41` to `id=42` reads or edits another user's data (IDOR, also called BOLA). Random IDs only hide the problem.

**FAIL**

```text
order = db.get(Order, request.args["id"])     # any logged-in user, any order
return order.to_json()
```

**PASS**

```text
order = db.get(Order, request.args["id"])
if order is None or order.owner_id != user.id: raise NotFound()   # same error for both
return order.to_json()
```

**Counterpoint.** "The IDs are UUIDs, nobody can guess them." A UUID leaks through logs, links and shared screenshots, and it is not an access check. Keep it as a second layer. Scope the query itself (`WHERE owner_id = :me`) so the check cannot be forgotten on the next endpoint.

## fn-password-slow-hash

severity: block  
concerns: security  
applies_when: Code stores or verifies a user password.  
backed by: OWASP, IETF, NIST

**Rule.** Hash passwords with Argon2id (or scrypt, bcrypt, PBKDF2) and a per-password salt from the library.

**Why.** A fast hash such as SHA-256 lets an attacker with the database try billions of guesses a second. A slow, salted, memory-hard hash makes each guess cost real time. A common baseline is Argon2id with at least 19 MiB of memory and 2 iterations. Check the current numbers when you review.

**FAIL**

```text
stored = hashlib.sha256(password.encode()).hexdigest()
```

**PASS**

```text
ph = argon2.PasswordHasher()            # salt and parameters stored in the hash string
stored = ph.hash(password)
ph.verify(stored, attempt)             # rehash when check_needs_rehash()
```

**Counterpoint.** "Argon2 is expensive at login." That cost is the defence; tune it to about a second on production hardware. Where FIPS compliance rules Argon2 out, PBKDF2-HMAC-SHA256 with a high iteration count is the accepted fallback.

## fn-redirect-target-allowlist

severity: should-fix  
concerns: security  
applies_when: A handler redirects to a URL taken from a query parameter, form field, header, or stored value, such as `?next=` after login.  
backed by: OWASP, MITRE, Microsoft, PortSwigger, GitHub

**Rule.** Redirect only to a local path or to a host on a server-side allowlist, never to a URL taken from the request as is.

**Why.** A link such as `https://bank.example/login?next=https://evil.example` carries your domain, so users and mail filters trust it, and after login the user lands on a phishing page. When page script sets `location` from the same value, a `javascript:` URL runs as script. Parse the URL and compare its scheme and host. A `startswith("/")` check alone passes `//evil.example`, and browsers read `/\evil.example` the same way. Better still, accept a short name and map it to the URL on the server.

**FAIL**

```python
return redirect(request.args["next"])
```

**PASS**

```python
target = urlparse(request.args.get("next", "/"))
if target.scheme or target.netloc or not target.path.startswith("/") or "\\" in target.path:
    target = urlparse("/")
return redirect(target.path)
```

**Counterpoint.** "The redirect only matters after a successful login." That is when it hurts most: the user has just typed a password and trusts the next page. A phishing copy of the login form on that page collects the password a second time.

## fn-reduced-motion-respected

severity: should-fix  
concerns: accessibility, usability  
applies_when: Styles or script add a transition, an animation, a parallax effect, or autoplay motion.  
backed by: Mozilla, W3C, Apple, The A11y Project, Google

**Rule.** Switch off or replace large, repeating, or interaction-triggered motion when `prefers-reduced-motion: reduce` is set.

**Why.** Scaling, panning, and parallax can trigger nausea and dizziness for people with vestibular disorders. They have already told their device so. A page that ignores the setting makes them leave.

**FAIL**

```css
.hero   { animation: zoom-in 1.2s ease-out infinite alternate; }
.card   { transition: transform 0.6s; }
.card:hover { transform: scale(1.3) rotate(4deg); }
```

**PASS**

```css
.hero { animation: zoom-in 1.2s ease-out infinite alternate; }
@media (prefers-reduced-motion: reduce) {
  .hero { animation: none; }
  .card { transition: opacity 0.2s; }
  .card:hover { transform: none; opacity: 0.9; }
}
```

**Counterpoint.** "Motion carries meaning, such as a loading spinner." Keep what the user needs and make it gentler: swap movement for a fade. The rule is about decorative and large movement, not about every pixel that moves.

## fn-regex-compiled-once

severity: should-fix  
concerns: performance  
applies_when: Code builds a regular expression or similar compiled matcher inside a loop or a function that runs per request.  
backed by: Rust project, Google, Python Software Foundation, Microsoft

**Rule.** Compile a regular expression once, at module or startup level, and reuse it.

**Why.** Compiling costs far more than matching and throws away reusable allocations. Inside a loop or a per-request function, the cost repeats on every call.

**FAIL**

```go
func valid(s string) bool {
	return regexp.MustCompile(`^[a-z]+$`).MatchString(s)   // compiled per call
}
```

**PASS**

```go
var lower = regexp.MustCompile(`^[a-z]+$`)

func valid(s string) bool { return lower.MatchString(s) }
```

**Counterpoint.** "The library caches patterns." Python and .NET keep recently used patterns, so a few static calls are fine. A pattern built from input or an unbounded set of patterns defeats the cache.

## fn-related-controls-in-fieldset

severity: should-fix  
concerns: accessibility, usability  
applies_when: Markup or a component renders a radio group, a checkbox group, or a value split across several inputs, such as a date or an address.  
backed by: GOV.UK, W3C, USWDS, The A11y Project

**Rule.** Wrap each radio group, checkbox group, and multi-part value, such as day, month, and year, in a `<fieldset>` with a `<legend>` that names the group, often as the question.

**Why.** Each radio's own label says only "Yes" or "No". Without a group, a screen reader user hears the option but not the question it answers. Put the `legend` first inside the `fieldset`. It acts as the group's heading, so assistive technology can tie each option to its question. The same holds for a date split into three boxes labelled "Day", "Month", and "Year". The visual group needs a matching code group, or the two drift apart.

**FAIL**

```html
<p>Do you have a passport?</p>
<input type="radio" id="pp-yes" name="passport" value="yes">
<label for="pp-yes">Yes</label>
<input type="radio" id="pp-no" name="passport" value="no">
<label for="pp-no">No</label>
```

**PASS**

```html
<fieldset>
  <legend>Do you have a passport?</legend>
  <input type="radio" id="pp-yes" name="passport" value="yes">
  <label for="pp-yes">Yes</label>
  <input type="radio" id="pp-no" name="passport" value="no">
  <label for="pp-no">No</label>
</fieldset>
```

**Counterpoint.** "A `fieldset` draws a border we don't want." Remove the border in CSS with `border: 0; padding: 0; margin: 0`. The grouping still reaches assistive technology. A `div` with `role="group"` and `aria-labelledby` is a fallback for a design system that cannot render a `fieldset`. VoiceOver on iOS ignores `fieldset` and `legend`. That is a reason to add `aria-labelledby` on each input as well, not to drop the group. A single checkbox, such as "I agree", needs no `fieldset`.

## fn-rerun-safe-after-crash

severity: block  
concerns: reliability  
applies_when: A function or job changes state and can be run twice, or can be killed partway.  
backed by: Cursor, Uber, Stripe, Dropbox, Netflix, GitHub

**Rule.** Make a state-changing operation give the same result on a second run and after a crash at any step, by deriving each step from current state and making leftovers recognisable as stale.

**Why.** Jobs get retried and processes get killed. An append, a counter bump, or a lock file with no owner and time leaves the next run unable to tell finished work from half-done work. Record "done" only after the last step succeeds, so a crash leaves the work visibly pending.

**FAIL**

```python
cur.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, acct))  # a retry applies it twice
open("out.json", "w").write(data)                                                       # a crash leaves a truncated file
```

**PASS**

```python
cur.execute("INSERT INTO applied_ops (op_id) VALUES (%s) ON CONFLICT DO NOTHING", (op_id,))
if cur.rowcount == 1:  # first run of this operation; same transaction as the update
    cur.execute("UPDATE accounts SET balance = balance + %s WHERE id = %s", (amount, acct))
tmp = path.with_suffix(".tmp")
tmp.write_text(data)
os.replace(tmp, path)  # the reader sees the old file or the new one, never half of one
```

**Counterpoint.** "Retries are rare." Crashes are not. For API calls that cross a network, [svc-idempotency-key](service.md#svc-idempotency-key) covers the key-based form of this rule.

## fn-response-fields-explicit

severity: should-fix  
concerns: security, compatibility  
applies_when: A handler returns a stored object or entity to the client.  
backed by: OWASP, Microsoft, Django REST framework, NIST

**Rule.** Return a response type that lists each field, never the stored model or a generic dump of it.

**Why.** A model gains `password_hash`, `internal_notes` or `email` and every endpoint that serialises it leaks the new field silently. Callers also start to depend on whatever is sent, so removing a field later is a breaking change. An explicit response type makes each exposed field a decision someone reviewed. The write side is [fn-no-mass-assignment](function.md#fn-no-mass-assignment).

**FAIL**

```text
return jsonify(user.__dict__)
return user_model.to_dict()          # all columns
```

**PASS**

```text
class UserOut(BaseModel): id: int; display_name: str
return UserOut.model_validate(user)
```

**Counterpoint.** "A response type per endpoint duplicates the model." Derive it from the model with a field list. The duplication is one line per field and shows up in the diff when a field is added.

## fn-status-announced-live-region

severity: should-fix  
concerns: accessibility, usability  
applies_when: Script shows a message after an async action without moving focus, such as "Saved", a result count, or an error.  
backed by: W3C, Mozilla, Heydon Pickering

**Rule.** Announce an async status message through a live region (`role="status"` or `role="alert"`) that is already in the markup before its text changes.

**Why.** A sighted user sees "Saved" appear. A screen-reader user hears nothing, because focus did not move. Most readers announce a change only in a region that existed first, so a region created together with its message is often skipped.

**FAIL**

```js
const note = document.createElement("div");
note.textContent = "Changes saved";
document.body.append(note);
```

**PASS**

```html
<div id="status" role="status" aria-live="polite"></div>
<script>
  document.getElementById("status").textContent = "Changes saved";
</script>
```

**Counterpoint.** "Move focus to the message instead." Use that for a blocking error after submit, where the user must act. For a passive result, moving focus steals the user's place. Keep `assertive` and `role="alert"` for errors, because they interrupt speech.

## fn-target-size

severity: should-fix  
concerns: accessibility, usability  
applies_when: Styles size a button, icon button, checkbox, or link that a pointer or finger operates.  
backed by: W3C, Apple, The A11y Project, Deque, Mozilla

**Rule.** Make each pointer target at least 24 by 24 CSS pixels, or space it so that a 24 px circle centred on it touches no other target and no other undersized target's circle.

**Why.** Small, tight controls cause mis-taps for anyone with a tremor, a large thumb, or a bumpy train. A mis-tap on "Delete" next to "Edit" costs more than a mis-tap on a menu item.

**FAIL**

```css
.icon-btn { width: 16px; height: 16px; margin: 0; }
```

```html
<button class="icon-btn">✎</button><button class="icon-btn">🗑</button>
```

**PASS**

```css
.icon-btn { min-width: 24px; min-height: 24px; padding: 4px; }
```

**Counterpoint.** "Inline links and dense tables are exempt." Targets inside a sentence are, and so are controls with an equivalent control that is big enough. A row of toolbar icons is neither, and nor are the action buttons on a table row. Touch platforms often ask for 44 px or more, so treat 24 px as the floor, not the goal.

## fn-tls-verify-on

severity: block  
concerns: security  
applies_when: Code makes an outbound HTTPS, database or message-broker connection.  
backed by: OWASP, IETF, Google, GitHub, Python Software Foundation

**Rule.** Leave certificate and hostname verification on in every environment that ships.

**Why.** With verification off, any on-path attacker presents a certificate and reads or changes the traffic. The flag is usually added to silence a dev-box error and then ships. Fix the trust store or pin a private CA instead.

**FAIL**

```text
requests.get(url, verify=False)                  # Python
https.request({ rejectUnauthorized: false })     // Node.js
```

**PASS**

```python
requests.get(url, verify="/etc/ssl/company-ca.pem")   # private CA added, check stays on
```

**Counterpoint.** "It is an internal network." Internal links get sniffed after one compromised host. A private CA gives you the same convenience with the check intact.

## fn-xml-no-external-entities

severity: block  
concerns: security  
applies_when: Code parses XML, SVG, SOAP, SAML, or an office document that a user or another system can supply.  
backed by: OWASP, MITRE, PortSwigger, GitHub

**Rule.** Parse untrusted XML with external entity resolution turned off, for example through a hardened parser such as `defusedxml`.

**Why.** A DTD can declare an entity whose value is `file:///etc/passwd` or an internal URL, and a parser that resolves it pastes that content into the document or makes the request for the attacker. Nested internal entities can also expand a small file into gigabytes. Where the parser allows it, also turn off DTDs and the parser's network access. Each parser has its own switches, so name them in the code instead of trusting the library default.

**FAIL**

```python
parser = lxml.etree.XMLParser(resolve_entities=True, no_network=False)
doc = lxml.etree.fromstring(request.get_data(), parser)
```

**PASS**

```python
import defusedxml.ElementTree as ET
doc = ET.fromstring(request.get_data())   # rejects DTD entities by default
```

**Counterpoint.** "Recent Python XML modules already refuse external entities." Some do. The FAIL above opts back in, Java and .NET parsers have their own defaults, and a later change to the parser config reopens the hole. An explicit hardened parser makes the setting visible in review.

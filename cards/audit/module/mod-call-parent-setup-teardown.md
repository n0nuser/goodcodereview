---
id: mod-call-parent-setup-teardown
level: module
tags: [testing, reliability]
severity: should-fix
status: draft
lacks: orgs, Laravel and Django back it; the Python unittest page states no such rule; needs a third org
lang: core
applies_when: A test class overrides setUp, tearDown, setUpClass or tearDownClass in an xUnit-style framework.
tool_gate: none
note: Laravel says to call parent::setUp and parent::tearDown; Django says to call the super implementation of setUpClass and tearDownClass. The unittest page was re-read and states no rule on calling the parent, so it does not count
borrowed_from:
  - https://laravel.com/docs/12.x/testing
  - https://docs.python.org/3/library/unittest.html
  - https://docs.djangoproject.com/en/stable/topics/testing/tools/
---

**Rule.** A test class that overrides `setUp`, `tearDown`, `setUpClass` or `tearDownClass` calls the parent's version.

**Why.** The base class may build the database, boot the app or reset state there. An override that skips the call drops that work, and the tests fail with confusing errors or, worse, leak state into the next test.

**FAIL**

```python
class DbTestCase(unittest.TestCase):
    def setUp(self):
        self.db = open_test_db()

class OrderTest(DbTestCase):
    def setUp(self):
        self.cart = Cart()  # self.db is never created
```

**PASS**

```python
class OrderTest(DbTestCase):
    def setUp(self):
        super().setUp()
        self.cart = Cart()

    def tearDown(self):
        self.cart.clear()
        super().tearDown()
```

**Counterpoint.** "My base class has empty hooks, so the call is noise." The base gains a hook body later and every override silently skips it. Call it anyway: set up after `super().setUp()` and tear down before `super().tearDown()`.

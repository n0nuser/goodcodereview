---
id: fn-side-effects-after-commit
level: function
tags: [correctness, reliability, data]
severity: should-fix
status: stable
lang: core
applies_when: Code inside a database transaction enqueues a job, sends a message or email, calls another service, or clears a cache.
context: [data]
tool_gate: A test that rolls the transaction back and asserts nothing was sent or enqueued; Rails `enqueue_after_transaction_commit = true` makes the safe form the default for jobs.
note: After commit is backed by Django, Rails, Spring, Sidekiq and GitLab (GitLab says to keep jobs, emails and HTTP calls out of the transaction block). The outbox row is backed by AWS and Microsoft (the transactional outbox pattern), Spring (the event publication registry writes in the business transaction) and Rails (a queue in the same database joins the transaction). The lock-holding argument in the Why rests on GitLab alone
borrowed_from:
  - https://docs.djangoproject.com/en/5.2/topics/db/transactions/
  - https://api.rubyonrails.org/classes/ActiveRecord/Transactions/ClassMethods.html
  - https://guides.rubyonrails.org/active_job_basics.html
  - https://docs.spring.io/spring-framework/reference/data-access/transaction/event.html
  - https://docs.spring.io/spring-modulith/reference/events.html
  - https://github.com/sidekiq/sidekiq/wiki/FAQ
  - https://docs.gitlab.com/development/database/transaction_guidelines/
  - https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html
  - https://learn.microsoft.com/en-us/azure/architecture/databases/guide/transactional-outbox-cosmos
---

**Rule.** Start side effects only after the transaction commits, with an `on_commit` or `after_commit` hook, or record them as an outbox row written inside the same transaction.

**Why.** Inside the transaction, the worker can pick up the job before the row is visible, and it fails with "record not found". If the transaction then rolls back, the email or the message has already gone out for data that does not exist. A network call inside the transaction also keeps its locks open for as long as the call takes. After commit, the data is permanent and the effect follows it. Work that must not be lost, such as a payment event, needs the outbox form: a crash between the commit and the enqueue drops an after-commit hook, and an outbox row survives it.

**FAIL**

```python
from django.db import transaction

def place_order(cart):
    with transaction.atomic():
        order = Order.objects.create(user=cart.user, total=cart.total)
        send_receipt.delay(order.id)   # may run before the commit, or after a rollback
    return order
```

**PASS**

```python
from django.db import transaction

def place_order(cart):
    with transaction.atomic():
        order = Order.objects.create(user=cart.user, total=cart.total)
        transaction.on_commit(lambda: send_receipt.delay(order.id))
    return order
```

```python
def place_order(cart):
    with transaction.atomic():
        order = Order.objects.create(user=cart.user, total=cart.total)
        Outbox.objects.create(topic="order.placed", payload={"order_id": order.id})
    return order   # a relay process publishes Outbox rows and marks them sent
```

**Counterpoint.** "An after-commit hook can be lost if the process dies right after the commit." True, which is why the Rule offers the outbox for work that must happen. For best-effort effects, such as a cache clear or a notification the user can live without, the hook is enough. A queue that stores its jobs in the same database already joins the transaction and meets the Rule; confirm that it does before you rely on it.

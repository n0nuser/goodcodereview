---
id: svc-dlq
level: service
tags: [reliability, queues, resilience]
severity: should-fix
status: stable
lang: core
applies_when: The code consumes from a queue or stream.
context: [server]
tool_gate: A config check that every consumed queue has a dead-letter target (for SQS in Terraform, a `redrive_policy` with `maxReceiveCount`), and an alarm on dead-letter queue depth.
note: dead-letter queue and replay backed by AWS (alarm on any message, re-process after the fix), Netflix (failed events spill into dead-letter queues, an offline job replays them), Notion (re-enqueue from the dead-letter queue is a first-class workflow) and Uber (dead-letter messages are published back into the first retry topic); the retry cap (AWS) and the depth alarm (AWS) sit in Why; Microsoft, Google and AWS back the ordered-queue clause
borrowed_from:
  - https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
  - https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb
  - https://www.notion.com/blog/building-observability-into-notions-dead-letter-queue
  - https://www.uber.com/blog/reliable-reprocessing/
  - https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-sessions
  - https://cloud.google.com/pubsub/docs/ordering
  - https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-understanding-logic.html
---

**Rule.** Give every consumer queue a dead-letter queue and keep a way to replay it after the fix. On an ordered queue, key the group or session to the unit that must stay ordered, so a poison message holds only its own unit.

**Why.** A poison message otherwise loops forever, uses the consumers' capacity and hides the real backlog. On an ordered queue it also holds the messages behind it: in a FIFO queue no further messages from the same group are returned until the stuck message is deleted or becomes visible again, and an unacknowledged ordering key can delay the others. Give each independent stream its own group, session or queue, so one failure stays contained. Then cap the retries, so that a failing message moves to the dead-letter queue after a few attempts. Alarm on any message in the dead-letter queue, because each one is a bug to fix. Replay has a cost on these queues: a message put back after a dead-letter loses its place in the order, so replay only where order no longer matters, or reorder downstream.

**FAIL**

```hcl
resource "aws_sqs_queue" "orders" {
  name       = "orders.fifo"
  fifo_queue = true
  # no redrive_policy: a message that always fails is retried forever
  # and holds its whole message group
}
```

```python
# every producer uses one group, so one stuck message blocks all orders
sqs.send_message(QueueUrl=url, MessageBody=body, MessageGroupId="orders")
```

**PASS**

```hcl
resource "aws_sqs_queue" "orders_dlq" {
  name       = "orders-dlq.fifo"
  fifo_queue = true
}

resource "aws_sqs_queue" "orders" {
  name       = "orders.fifo"
  fifo_queue = true
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.orders_dlq.arn
    maxReceiveCount     = 5
  })
}
# replay after the fix: aws sqs start-message-move-task --source-arn <orders-dlq ARN>
```

```python
# one group per order, so one stuck order does not block the others
sqs.send_message(QueueUrl=url, MessageBody=body, MessageGroupId=order_id)
```

**Counterpoint.** "A dead-letter queue already stops the poison message." It stops it after the retry cap. Until then the redelivery holds its group, and in a FIFO queue that means every message behind it. Grouping and the dead-letter queue do different jobs, so keep both. Choose the group key from the unit that must stay ordered. A single group restores the head-of-line block you were trying to remove. On a standard queue with no ordering, there is no group to key and the second sentence of the Rule does not apply.

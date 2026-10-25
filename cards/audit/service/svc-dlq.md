---
id: svc-dlq
level: service
tags: [reliability, queues, resilience]
severity: should-fix
status: stable
lang: core
applies_when: The code consumes from a queue or stream.
tool_gate: A config check that every consumed queue has a dead-letter target (for SQS in Terraform, a `redrive_policy` with `maxReceiveCount`), and an alarm on dead-letter queue depth.
note: dead-letter queue and replay backed by AWS (alarm on any message, re-process after the fix), Netflix (failed events land in dead-letter queues, an offline job replays them) and Dropbox (a stated proposal - a retry cap, then a dead-letter queue and tools to reschedule); the depth alarm is AWS only and sits in Why
borrowed_from:
  - https://aws.amazon.com/builders-library/avoiding-insurmountable-queue-backlogs/
  - https://netflixtechblog.com/behind-the-scenes-evolving-netflixs-ads-event-pipeline-for-live-part-ii-826ebf9ad9fb
  - https://dropbox.tech/infrastructure/asynchronous-task-scheduling-at-dropbox
---

**Rule.** Give every consumer queue a dead-letter queue, with a retry cap before a message moves there and a way to replay it after the fix.

**Why.** A poison message otherwise loops forever, uses the consumers' capacity and hides the real backlog. Alarm on any message in the dead-letter queue, because each one is a bug to fix. Also keep the visibility timeout longer than the worst-case processing time (or extend it), or slow work is delivered twice.

**FAIL**

```hcl
resource "aws_sqs_queue" "orders" {
  name = "orders"   # no redrive_policy: a message that always fails is retried forever
}
```

**PASS**

```hcl
resource "aws_sqs_queue" "orders_dlq" {
  name = "orders-dlq"
}

resource "aws_sqs_queue" "orders" {
  name = "orders"
  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.orders_dlq.arn
    maxReceiveCount     = 5
  })
}
# replay after the fix: aws sqs start-message-move-task --source-arn <orders-dlq ARN>
```

**Counterpoint.** "A dead-letter queue just hides failures." Only if nobody watches it. With an alarm on its depth it shows each failure once, instead of hiding it in retries, and the replay step means a fix does not lose the messages that failed before it.

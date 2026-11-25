---
id: fn-timestamps-stored-in-utc
level: function
tags: [correctness, data, time]
severity: should-fix
status: stable
lang: core
applies_when: The code stores, logs or sends a point in time (an instant), such as a created-at field, an event time or an API field.
tool_gate: none
note: W3C, Django and Zalando back the store-and-send-in-UTC Rule. Only Django also says to convert to local time at the edge, so that half sits in the Why. The PostgreSQL wiki (use timestamptz) and Google AIP-142 (use Timestamp) are close but not counted
borrowed_from:
  - https://www.w3.org/TR/timezone/
  - https://docs.djangoproject.com/en/5.1/topics/i18n/timezones/
  - https://opensource.zalando.com/restful-api-guidelines/
---

**Rule.** Store and send instants in UTC.

**Why.** Local times repeat or skip an hour when clocks change, and values written in different zones cannot be compared or sorted without knowing each zone. Keep the data in UTC and convert to a person's zone only where you show it to them. Scope: a calendar date (a birthday) is not an instant, and a future local event (a 09:00 meeting in Madrid) needs its zone name, because zone rules change before the event.

**FAIL**

```python
created_at = datetime.now()          # naive local time, the zone is lost
```

```sql
created_at timestamp                 -- no zone information
```

**PASS**

```python
created_at = datetime.now(timezone.utc)
```

```sql
created_at timestamptz
```

**Counterpoint.** "All our users are in one time zone." Daylight saving time still makes some local times ambiguous or missing twice a year, and the second time zone arrives after the data is in. Storing UTC costs nothing now and converting at display is one call; fixing mixed local times later means guessing what each row meant.

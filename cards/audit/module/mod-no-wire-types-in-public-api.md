---
id: mod-no-wire-types-in-public-api
level: module
tags: [maintainability, api-design, boundaries]
severity: should-fix
status: draft
lang: core
applies_when: A module exposes a public function, class or re-export.
tool_gate: none
note: one vendor's engineering guidance (opinion), from pstack principle-boundary-discipline
borrowed_from:
  - https://github.com/cursor/plugins/blob/main/pstack/skills/principle-boundary-discipline/SKILL.md
---

**Rule.** Expose domain types in a module's public interface, and keep transport, storage and framework types behind it.

**Why.** A public signature that returns an ORM row or a protobuf message ties every caller to that library and schema. A storage change then ripples through code that never cared about storage.

**FAIL**

```python
def get_user(id: str) -> UserRow: ...          # SQLAlchemy model
from proto.user_pb2 import User                # re-exported as the API
```

**PASS**

```python
def get_user(id: UserId) -> User: ...          # plain domain dataclass; mapping lives inside
```

**Counterpoint.** "Mapping costs a copy and a class." For a thin pass-through with no second consumer, that cost can exceed the benefit; say so in the review. The rule bites when the type crosses a package or team boundary.

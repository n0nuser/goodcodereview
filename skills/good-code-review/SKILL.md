---
name: good-code-review
description: Review code against stable cards, from a diff up to an incident. Use when asked to review, audit or check code.
---

# Good Code Review

## Routing

| Input | Entry point |
|---|---|
| diff / PR | change |
| file / function | function |
| package / path | module |
| service | service |
| cross-service design doc | system |
| repo | codebase |
| release / launch | production |
| incident | incident |

## Verdict format

Per check: `PASS`, `FAIL` or `N/A`, with `file:line` evidence.
A `FAIL` carries the card severity: block, should-fix or discuss.

Full text per level: `references/<level>.md`.

# Incident audit index

One line per stable incident card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `incident.md`: read them with offset `<first>` and limit `<count>`.

- `inc-perf-fix-has-profile-evidence` [should-fix] {performance, testing} L3+26: Tie the performance fix to evidence that names the bottleneck: a profile, a trace, or a USE check.
- `inc-rollback-path-tested` [should-fix] {reliability} L30+26: Exercise each mitigation that a runbook names (rollback, failover, flag off) on a regular schedule.

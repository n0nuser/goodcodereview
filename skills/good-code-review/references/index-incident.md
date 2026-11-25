# Incident audit index

One line per stable incident card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's lines in `incident.md`: read them with offset `<first>` and limit `<count>`.

- `inc-perf-fix-has-profile-evidence` [should-fix] {performance, testing} L3+26: Tie the performance fix to evidence that names the bottleneck: a profile, a trace, or a USE check.
- `inc-postmortem-blameless` [should-fix] {process} L30+29: Write a postmortem so that it names causes in the system and the decisions around it, never a person or team as the one at fault.
- `inc-rollback-path-tested` [should-fix] {reliability} L60+26: Exercise each mitigation that a runbook names (rollback, failover, flag off) on a regular schedule.
- `inc-single-incident-commander` [discuss] {process, reliability} L87+27: Name one incident commander for each major incident, who holds the overall state of the response and oversees the other roles.

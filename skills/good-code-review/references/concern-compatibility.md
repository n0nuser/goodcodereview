# compatibility cards

Every stable card that lists the `compatibility` concern, by level. The place `<level>.md:L<first>+<count>` is the card's lines: read them with offset `<first>` and limit `<count>`.

## change

- `chg-breaking-change-taxonomy` [block] {compatibility} change.md:L114+27: Treat any change that callers can observe in a signature, return values, error types, defaults, or side effects as breaking until a consumer check says otherwise.
- `chg-delete-legacy-after-migration` [should-fix] {compatibility, maintainability} <data> change.md:L169+30: When no consumer sits outside the repo, move every caller to the new API and delete the old one, and the tests that pinned its internals, in the same change.
- `chg-devex-breaking-config` [should-fix] {compatibility, process} change.md:L200+28: Flag a change that renames or removes an environment variable, moves a secret, or remaps a port as breaking for developers and operators, and update every place that documents or sets it.
- `chg-expand-contract` [block] {compatibility} <data> change.md:L229+28: Evolve shared contracts in steps: add the new form beside the old (expand), migrate every consumer, then remove the old form (contract) in a later change.
- `chg-migration-add-column-rewrite` [should-fix] {compatibility} <data> change.md:L288+27: Add the column nullable or with a constant default, then fill volatile, computed, or identity values in batches.
- `chg-proto-no-field-type-change` [should-fix] {compatibility} change.md:L458+31: Never change the type of a protobuf field, switch it between repeated and scalar, or rename it while any consumer reads JSON or text format; add a new field instead.
- `chg-proto-reserve-removed-fields` [should-fix] {compatibility} change.md:L490+32: When you delete a protobuf field or enum value, add `reserved` for its number and name in the same change, and never reuse a number.

## function

- `fn-response-fields-explicit` [should-fix] {security, compatibility} <server> function.md:L1636+28: Return a response type that lists each field, never the stored model or a generic dump of it.

## module

- `mod-derive-dont-duplicate` [should-fix] {compatibility, maintainability} module.md:L154+26: Derive a type, list or enum from the schema or list that owns it, or add a build check that fails when the two disagree.
- `mod-proto-enum-zero-unspecified` [should-fix] {compatibility} module.md:L574+32: Give every protobuf enum a zero value named `<ENUM>_UNSPECIFIED` with no real meaning.

## service

- `svc-api-contract-tests` [should-fix] {compatibility, testing} <server> service.md:L103+28: Run a contract test for each cross-service call, derived from the consumer's real requests, and fail the provider's build when it breaks one.
- `svc-api-deprecation-sunset` [should-fix] {compatibility} <server> service.md:L132+31: Before removing an endpoint, mark it `deprecated` in the spec and send `Deprecation` and `Sunset` headers.
- `svc-api-documented-errors` [should-fix] {correctness, compatibility} <server> service.md:L164+34: Document every error status each operation can return, with a schema and one example.
- `svc-api-error-code-stable` [should-fix] {compatibility} <server> service.md:L199+29: Give each error a stable machine-readable code that callers branch on, and never make them parse the message text.
- `svc-api-problem-json` [should-fix] {compatibility} <server> service.md:L288+34: Return errors as `application/problem+json` with a `status` that equals the HTTP status, and leave stack traces and internal detail out.
- `svc-api-specific-status-codes` [should-fix] {compatibility} <server> service.md:L354+29: Return the most specific status code that fits: 201 with `Location` for a create, 405 with `Allow` for a wrong method, and a 4xx or 5xx for any failure.
- `svc-api-versioning-policy` [should-fix] {compatibility} <server> service.md:L384+29: Write down one versioning scheme for the API, and ship no breaking change inside a version it has published.

## system

- `sys-index-concurrently` [should-fix] {compatibility} <data> system.md:L175+28: Create indexes with `CONCURRENTLY`, outside a transaction block, and handle a failed build that leaves an INVALID index.
- `sys-migration-expand-contract` [block] {reliability, compatibility} <data> system.md:L263+26: Run data backfills in batches, in a migration separate from the schema change.
- `sys-migration-lock-timeout` [should-fix] {compatibility} <data> system.md:L290+27: Set `lock_timeout` for the migration session and retry on timeout.

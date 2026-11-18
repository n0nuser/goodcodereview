# Promotion pass B

All four cards promoted to stable. `python3 tools/validate.py` exits 0.

## svc-api-version-on-every-request: PROMOTED (severity should-fix)
Rule clause "name the version on every request, in a header or query parameter": GitHub (X-GitHub-Api-Version header), Google (AIP-185: requests must send the version in a header or query parameter), Microsoft (api-version query parameter required on every operation). No Rule edit. Links only stable svc-api-versioning-policy.

## code-secrets-not-plaintext-in-repo: TRIMMED+PROMOTED (severity should-fix)
Old Rule: "Keep secrets out of source code and config: read them from a secret store, or commit only encrypted values."
New Rule: "Keep secrets out of source code and config."
Clause "or commit only encrypted values" had one org (Pulumi) and GitLab says to keep secrets outside the repository, so it was dropped. Clause "read from a secret store" moved to the Why. The Pulumi source and the encrypted-YAML PASS were removed; CISA was added (source code, secret manager).
Remaining clause: OWASP (do not hard-code keys, do not check them into version control), CISA (secrets not present in source code), GitLab (store secrets outside the repository). The AWS sweep hit was a navigation link only and was not used. code-secret-scan is stable and about detection, so no duplicate.

## fn-password-min-length: PROMOTED (severity should-fix)
Rule clause "enforce a minimum length on the server": NIST SP 800-63B (verifiers shall require 15 or 8), OWASP (minimum length enforced by the application), Microsoft (Identity RequiredLength, enforced by default). No Rule edit.
Judgement call: the Microsoft page is a settings reference with a default of 6, not a recommendation. I counted it as a description of what the framework enforces; a stricter reviewer may want a different third org.

## fn-early-return-no-else: TRIMMED+PROMOTED (severity discuss)
Old Rule: "...return early, so the main path is not nested and needs no `else`."
New Rule: "...return early, so the main path is not nested."
The "no else" clause has two orgs (Go, LLVM); Flink says only to avoid nesting by exiting early. The else sentence stays in the Why.
Remaining clause: Go (error cases return, flow runs down the page), Apache Flink (avoid deep nesting by exiting early), LLVM (use early exits). Severity left at discuss because it is a style rule. fn-nesting-depth-cap is still a draft that links this card, which is fine.

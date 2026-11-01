# py-pytest-parametrize and svc-fail-closed-defaults: source pass, round 1

Fetched 2026-11-01. Found by an opencode worker (DeepSeek V4.1 Flash Free), then re-checked with curl: every quote below was FOUND on its page.

1. https://go.dev/wiki/TableDrivenTests (org: Go project). "If you ever find yourself using copy and paste when writing a test, think about whether refactoring into a table-driven test or pulling the copied code out into a helper function might be a better option." States the practice. Backs `py-pytest-parametrize`.
2. https://docs.nunit.org/articles/nunit/writing-tests/attributes/testcase.html (org: NUnit). "You may apply the attribute multiple times to create several cases from one method." Attribute reference page: not counted (PROMOTION rule 3).
3. https://docs.pytest.org/en/stable/how-to/parametrize.html (org: pytest). "The builtin pytest.mark.parametrize decorator enables parametrization of arguments for a test function." Feature description: not counted.
4. https://www.cisa.gov/sites/default/files/2023-10/SecureByDesign_1025_508c.pdf (org: CISA, with NSA, FBI and partners). "A secure configuration should be the default baseline." States the practice. Backs the "switched on" clause of `svc-fail-closed-defaults`: OWASP, Microsoft and CISA make three.
5. https://www.postgresql.org/docs/current/auth-pg-hba-conf.html (org: PostgreSQL). "If no record matches, access is denied." Reference page: not counted.
6. https://guides.rubyonrails.org/configuring.html (org: Rails). "Causes the app to not boot if a master key hasn't been made available through ENV["RAILS_MASTER_KEY"] or the config/master.key file." Option description: not counted.

Counts: `py-pytest-parametrize` 1 practice source (Go). `svc-fail-closed-defaults`: clause A 3 (OWASP, Microsoft, CISA); the allow-list and secret clauses still lack practice sources.

## Round 2 (Haiku worker, quotes re-checked with curl)

7. https://learn.microsoft.com/en-us/dotnet/core/testing/unit-testing-best-practices (org: Microsoft). "Some common approaches for implementing a single Act task include creating a separate test for each Act or using parameterized tests." Practice. Backs `py-pytest-parametrize`.
8. https://tech.gr.vodafone.com/post/junit-parameterized-tests (org: Vodafone). "All of the three unit tests above are really the same unit test with a different input parameter." A team's description of the practice. Backs `py-pytest-parametrize`.
9. https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html (org: OWASP). "For security purposes an application should be configured to deny access by default." Backs the allow-list clause of `svc-fail-closed-defaults`.
10. https://github.com/usnistgov/oscal-content/blob/main/nist.gov/SP800-53/rev5/json/NIST_SP-800-53_rev5_catalog.json (org: NIST, repository owner usnistgov). SP 800-53 rev 5 SC-7(5): "Deny network communications traffic by default and allow network communications traffic by exception." Read from the OSCAL JSON catalog. Backs the allow-list clause.
11. https://www.playframework.com/documentation/latest/ApplicationSecret (org: Play Framework). On startup Play throws an error if the secret is unset or `changeme`. Framework behaviour, one source: not counted.

Counts: `py-pytest-parametrize` Google (go.dev counts as Google), Microsoft, Vodafone = 3. `svc-fail-closed-defaults`: "switched on" OWASP, Microsoft, CISA = 3; "empty allow-list denies" Google, AWS, OWASP, NIST = 4. The secret clause has no second practice source (Play only), so it moved from the Rule to the Why.

# Source pass 6: third org for three draft cards

Fetched 2026-10-25 through WebFetch (a small model summarises the page). Paraphrase only. Each row gives the URL, org, distilled point, and the card clause it backs.

1. https://learn.microsoft.com/en-us/aspnet/core/security/authentication/identity-configuration. Microsoft. ASP.NET Core Identity ships account lockout: a set number of failed attempts (default 5) locks the account for a default 5 minutes, and a successful sign-in resets the count. Backs `svc-auth-throttle-generic-errors`, throttle clause (limit failed attempts per account). Caveat: the sample passes `lockoutOnFailure: false`, so lockout is opt-in.
2. https://auth0.com/docs/secure/attack-protection/brute-force-protection. Auth0 (Okta). Counts failed logins from one IP against one user identifier and blocks past a threshold (default 10, range 1 to 100); an optional account lockout blocks all attempts to the account. Backs `svc-auth-throttle-generic-errors`, throttle clause. Caveat: the default key is IP plus account, not account alone; the account-wide lockout is optional.
3. https://docs.cloud.google.com/identity-platform/docs/admin/email-enumeration-protection. Google. With enumeration protection on, a failed sign-in returns one generic invalid-credentials error, and password-reset requests give no sign of whether the address exists. Backs `svc-auth-throttle-generic-errors`, generic-errors clause (same message whether or not the account exists). Caveat: says nothing about timing; sign-up still reveals an existing address.
4. https://www.stepsecurity.io/blog/pinning-github-actions-for-enhanced-security-a-complete-guide. StepSecurity. Recommends pinning actions to a full commit SHA (immutable) and restricting `GITHUB_TOKEN` permissions to least privilege. Backs `code-workflow-supply-chain`, Rule (pin to a full SHA) and the least-privilege token sentence in Why. Caveat: a security vendor's blog, not a standard.
5. https://www.nist.gov/itl/executive-order-14028-improving-nations-cybersecurity/software-security-supply-chains-software-1. NIST. Software producers should maintain SBOMs in accessible, signed repositories and share them with buyers; it also recommends tying vulnerability detection to SBOM repositories. Backs `code-dependency-licence-sbom`, SBOM clause (generate an SBOM) and the link between inventory and vulnerability alerts. Caveat: written for federal producers; it does not name CI as the place to run it.

## Checked, not added

- https://docs.gitlab.com/ee/ci/yaml/: GitLab advises a full commit SHA for `include:project` refs, not for third-party actions. Does not back the Rule as written.
- https://github.com/microsoft/sbom-tool: documents running SBOM generation in CI, but is a tool README, not a recommendation. Not added.
- https://docs.gitlab.com/ee/user/application_security/dependency_scanning/: GitLab scans dependencies for known vulnerabilities in pipelines and uses SBOM artifacts. Would be a 4th org for the scan clause, which already has 3. Not added.
- https://www.ntia.gov/page/software-bill-materials, https://www.cisa.gov/resources-tools/resources/software-bill-materials-sbom-sharing-lifecycle-report, https://csrc.nist.gov/projects/ssdf, https://csrc.nist.gov/pubs/sp/800/218/final: pages read did not recommend producing an SBOM. Not added.
- https://developer.mozilla.org/en-US/docs/Web/Security/Practical_implementation_guides: no enumeration or rate-limit content.
- Microsoft account-confirmation tutorial and Azure Pipelines security page: no enumeration or SHA-pinning statement. Not added.
- Google security blog SBOM post and several Auth0/Okta/Google Cloud blog URLs: article body missing or 404.

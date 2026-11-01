# New security cards from audits

Quotes read on the live pages (curl, 2026-11-01).

## svc-fail-closed-defaults
Clause A: controls on by default, empty allow-list denies.
- OWASP. https://raw.githubusercontent.com/OWASP/ASVS/master/5.0/en/0x22-V13-Configuration.md. "The application's default configuration must be secure for use on the Internet."
- Microsoft. https://learn.microsoft.com/en-us/aspnet/core/security/authorization/secure-data. "Having authorization required by default is more secure than relying on new controllers and Razor Pages to include the [Authorize] attribute."
- Google. https://google.github.io/building-secure-and-reliable-systems/raw/ch08.html (footnote 11). "Systems using ACLs must fail closed (secure), with access explicitly granted by ACL entries."

Clause B: refuse to start on missing or placeholder secret.
- Django. https://docs.djangoproject.com/en/5.2/ref/settings/. "Django will refuse to start if SECRET_KEY is not set."
- OWASP. ASVS V13.2.3: "the credential being used by the consumer is not a default credential (e.g., root/root or admin/admin)."
- MITRE. https://cwe.mitre.org/data/definitions/1393.html, mitigation: "Prohibit use of default, hard-coded, or other values that do not vary for each installation of the product".

## fn-constant-time-secret-compare
- PSF. https://docs.python.org/3/library/hmac.html. "recommended to use the compare_digest() function instead of the == operator to reduce the vulnerability to timing attacks."
- Google. https://pkg.go.dev/crypto/subtle. ConstantTimeCompare: "The time taken is a function of the length of the slices and is independent of the contents."
- OpenJS. https://nodejs.org/api/crypto.html. crypto.timingSafeEqual: "compares the underlying bytes ... using a constant-time algorithm".
- GitHub. https://docs.github.com/en/webhooks/using-webhooks/validating-webhook-deliveries. "Never use a plain == operator. Instead consider using a method like secure_compare or crypto.timingSafeEqual".
- OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html. "Compare the submitted and expected HMACs in the same representation using a constant-time comparison function , and reject mismatches."
- MITRE (reference for the Why). https://cwe.mitre.org/data/definitions/208.html. "even small variations in timing can be exploited by attackers to indirectly infer certain details".

## fn-mask-credentials-in-output (draft)
- GitHub. https://cli.github.com/manual/gh_auth_status. Flag "--show-token: Display the auth token" is opt-in; default hides it. Backs: full value only behind a flag.
- Django. https://docs.djangoproject.com/en/5.2/ref/settings/. "As a security measure, Django will not include settings that might be sensitive, such as SECRET_KEY." (debug page)
- GitLab. https://docs.gitlab.com/ci/variables/. "Default visibility changed from Visible to Masked in GitLab 18.3." (CI variable logs)
- OWASP. https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html. Lists "Access tokens", "Authentication passwords", "Database connection strings", "Encryption keys and other primary secrets" as data to exclude from logs.
Gap: only GitHub and Django show list/show/debug output; the others cover logs. Hence draft.
- AWS. https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic_policy-eval-denyallow.html (fetched 2026-11-01). "By default, all requests are implicitly denied with the exception of the AWS account root user, which has full access." Backs the empty allow-list clause of `svc-fail-closed-defaults`. Kubernetes NetworkPolicy was checked and allows by default, so it is no backer.

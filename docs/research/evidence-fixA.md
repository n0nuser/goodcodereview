# Evidence, fix round A (2026-11-06)
Fetched by me with WebFetch; other quotes are from the two judge reports (both judges quoted them independently) and were not re-fetched.

svc-password-reset | https://docs.djangoproject.com/en/5.2/topics/auth/default/ | Django | "Changing a user's password will log out all their sessions." ; PasswordResetView "generating a one-time use link" | revoke sessions; single-use
svc-password-reset | https://api.rubyonrails.org/classes/ActiveRecord/TokenFor/ClassMethods.html | Rails | "By default, tokens do not expire." (expiry is optional) | NOT used as a source (no recommendation)
svc-account-linking | https://auth0.com/docs/manage-users/user-accounts/user-account-linking | Auth0 | "request authentication for both accounts before linking occurs" | prove control of both (kept)
svc-mfa-step-up | https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication | Auth0 | "require users to authenticate with a stronger authentication mechanism to access sensitive resources" | sensitive actions (OWASP, Microsoft, Auth0 = 3)
svc-api-key-scope | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html | AWS | "use temporary security credentials ... instead of creating long-term credentials" ; "secret access key can be retrieved only at the time you create it" | bounded lifetime; show once

Counts per Rule clause (judge-confirmed unless above): oauth PKCE/redirect/state/ID-token 3 each; saml 3-4; account-linking prove-both 4 (OWASP, MSRC, Auth0, Google), iss+sub 4; mfa factor-change 3, sensitive 3; password-reset single-use 3 (OWASP, Auth0, Django), short-lived 3 (OWASP, Auth0, NIST), sessions 3-4; api-key scope 4, lifetime 3 (GitHub, GitLab, AWS), after exposure 3; host-header 3-5; cache-key 3; cache-control 3-4; header-encoding 4.

# Evidence T2: identity security cards

Fetched 2026-11-06. One line per quote relied on. Organisation counting follows docs/PROMOTION.md.

## svc-oauth-code-flow-binding

svc-oauth-code-flow-binding | https://www.rfc-editor.org/rfc/rfc9700.html | IETF | "When comparing client redirection URIs against pre-registered URIs, authorization servers MUST utilize exact string matching except for port numbers in localhost redirection URIs of native apps" | exact redirect_uri and the loopback port exception
svc-oauth-code-flow-binding | https://www.rfc-editor.org/rfc/rfc9700.html | IETF | "Public clients MUST use PKCE [RFC7636] to this end" | PKCE
svc-oauth-code-flow-binding | https://www.rfc-editor.org/rfc/rfc9700.html | IETF | "Currently, S256 is the only such method." | S256, the method that does not expose the verifier
svc-oauth-code-flow-binding | https://www.rfc-editor.org/rfc/rfc9700.html | IETF | "In any case, the PKCE challenge or OpenID Connect nonce MUST be transaction-specific and securely bound to the client and the user agent in which the transaction was started." | state/nonce bound to this transaction
svc-oauth-code-flow-binding | https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html | OWASP | "Clients are preventing injection (replay) of authorization codes into the authorization response by using PKCE flow." | PKCE
svc-oauth-code-flow-binding | https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html | OWASP | "When using PKCE, Clients should use PKCE code challenge methods that do not expose the PKCE verifier in the authorization request." | S256, non-revealing challenge method
svc-oauth-code-flow-binding | https://cheatsheetseries.owasp.org/cheatsheets/OAuth2_Cheat_Sheet.html | OWASP | "The PKCE challenge or OpenID Connect "nonce" must be transaction-specific and securely bound to the client and the user agent in which the transaction was started." | state/nonce bound to this transaction
svc-oauth-code-flow-binding | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "This URI MUST exactly match one of the Redirection URI values for the Client pre-registered at the OpenID Provider" | exact redirect_uri
svc-oauth-code-flow-binding | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "If present in the ID Token, Clients MUST verify that the nonce Claim Value is equal to the value of the nonce parameter sent in the Authentication Request." | nonce matches the request
svc-oauth-code-flow-binding | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "It MUST contain the OAuth 2.0 client_id of the Relying Party as an audience value." | aud
svc-oauth-code-flow-binding | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "Expiration time on or after which the ID Token MUST NOT be accepted by the RP when performing authentication with the OP." | exp
svc-oauth-code-flow-binding | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "The Client MUST validate the signature of all other ID Tokens according to JWS" | signature
svc-oauth-code-flow-binding | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "The Client MUST use the keys provided by the Issuer." | signature key source
svc-oauth-code-flow-binding | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow | Microsoft | "It must exactly match one of the redirect URIs you registered in the Microsoft Entra admin center" | exact redirect_uri
svc-oauth-code-flow-binding | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow | Microsoft | "The app should verify that the state values in the request and response are identical." | state
svc-oauth-code-flow-binding | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow | Microsoft | "This parameter is now recommended for all application types, both public and confidential clients" | PKCE
svc-oauth-code-flow-binding | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-auth-code-flow | Microsoft | "This SHOULD be S256" | S256
svc-oauth-code-flow-binding | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP | "Validate ID Tokens on the relying party: issuer (iss), audience (aud), signature (per provider JWKs), expiration (exp)." | ID-token signature, iss, aud, exp
svc-oauth-code-flow-binding | https://developers.google.com/identity/gsi/web/guides/verify-google-id-token | Google | "The ID token is properly signed by Google." | signature
svc-oauth-code-flow-binding | https://developers.google.com/identity/gsi/web/guides/verify-google-id-token | Google | "The value of aud in the ID token is equal to one of your app's client IDs." | aud
svc-oauth-code-flow-binding | https://developers.google.com/identity/gsi/web/guides/verify-google-id-token | Google | "The value of iss in the ID token is equal to accounts.google.com or https://accounts.google.com." | iss
svc-oauth-code-flow-binding | https://developers.google.com/identity/gsi/web/guides/verify-google-id-token | Google | "The expiry time (exp) of the ID token has not passed." | exp

## svc-saml-assertion-binding

svc-saml-assertion-binding | https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf | OASIS | "Regardless of the SAML binding used, the service provider MUST do the following:" | the check list
svc-saml-assertion-binding | https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf | OASIS | "Verify any signatures present on the assertion(s) or the response" | signature
svc-saml-assertion-binding | https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf | OASIS | "Verify that the Recipient attribute in any bearer <SubjectConfirmationData> matches the assertion consumer service URL to which the <Response> or artifact was delivered" | Recipient
svc-saml-assertion-binding | https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf | OASIS | "Verify that the NotOnOrAfter attribute in any bearer <SubjectConfirmationData> has not passed" | NotOnOrAfter
svc-saml-assertion-binding | https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf | OASIS | "Verify that the InResponseTo attribute in the bearer <SubjectConfirmationData> equals the ID of its original <AuthnRequest> message" | InResponseTo
svc-saml-assertion-binding | https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf | OASIS | "<AudienceRestriction> including the service provider's unique identifier as an <Audience>" | Audience
svc-saml-assertion-binding | https://docs.oasis-open.org/security/saml/v2.0/saml-profiles-2.0-os.pdf | OASIS | "The service provider MUST ensure that bearer assertions are not replayed, by maintaining the set of used ID values for the length of time for which the assertion would be considered valid based on the NotOnOrAfter attribute" | replay cache
svc-saml-assertion-binding | https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html | OWASP | "Obtain the key directly from the identity provider, store it in a local file and ignore any KeyInfo elements in the document." | key from the IdP, not from the response
svc-saml-assertion-binding | https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html | OWASP | "Verify that the XML signature's <ds:Reference URI> resolves to the signed Assertion or Response, and that the exact assertion used for authentication is protected by that validated signature." | signature covers the assertion read
svc-saml-assertion-binding | https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html | OWASP | "Validate the Destination attribute on <samlp:Response> exactly matches the SP's expected Assertion Consumer Service (ACS) URL" | Destination
svc-saml-assertion-binding | https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html | OWASP | "Reject responses that are missing Destination or where it does not match" | Destination
svc-saml-assertion-binding | https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html | OWASP | "Validate <saml:Audience> matches the SP's EntityID" | Audience
svc-saml-assertion-binding | https://cheatsheetseries.owasp.org/cheatsheets/SAML_Security_Cheat_Sheet.html | OWASP | "Validate Recipient attribute, InResponseTo, and <saml:SubjectConfirmationData> (Recipient, NotOnOrAfter, InResponseTo)" | Recipient, InResponseTo, NotOnOrAfter
svc-saml-assertion-binding | https://pages.nist.gov/800-63-4/sp800-63c/Federation/ | NIST | "The RP SHALL validate the digital signature or MAC of each such assertion based on the issuer's verification key." | signature with the issuer's key
svc-saml-assertion-binding | https://pages.nist.gov/800-63-4/sp800-63c/Federation/ | NIST | "This signature SHALL cover the entire assertion, including its identifier, issuer, audience, subject, and time validity window." | signature covers the assertion
svc-saml-assertion-binding | https://pages.nist.gov/800-63-4/sp800-63c/Federation/ | NIST | "All RPs SHALL check that the audience of an assertion contains an identifier for their RP" | Audience
svc-saml-assertion-binding | https://learn.microsoft.com/en-us/entra/identity-platform/single-sign-on-saml-protocol | Microsoft | "Microsoft Entra ID uses the signing key in the IDPSSODescriptor element of its metadata document." | key from IdP metadata
svc-saml-assertion-binding | https://learn.microsoft.com/en-us/entra/identity-platform/single-sign-on-saml-protocol | Microsoft | "InResponseTo: This is set to the ID attribute of the AuthnRequest element that initiated the response." | InResponseTo
svc-saml-assertion-binding | https://github.com/SAML-Toolkits/python3-saml | SAML-Toolkits project | "In order to avoid them, the SP can keep a list of SAML Messages or Assertion IDs already validated and processed." | replay cache
svc-saml-assertion-binding | https://github.com/SAML-Toolkits/python3-saml | SAML-Toolkits project | "Checking that the ID of the current Message/Assertion does not exists in the list of the ones already processed will prevent replay attacks." | replay cache
svc-saml-assertion-binding | https://github.com/SAML-Toolkits/python3-saml | SAML-Toolkits project | "Destination, NameId, Conditions ... are validated too." | Destination and conditions
svc-saml-assertion-binding | https://github.com/SAML-Toolkits/python3-saml | SAML-Toolkits project | "In production also we highly recommend to register on the settings the IdP certificate instead of using the fingerprint method." | key from IdP configuration
svc-saml-assertion-binding | https://github.com/SAML-Toolkits/python3-saml | SAML-Toolkits project | "get_last_assertion_not_on_or_after The NotOnOrAfter value of the valid SubjectConfirmationData node (if any) of the last assertion processed (is only calculated with strict = true)" | NotOnOrAfter under strict mode

## svc-mfa-step-up

svc-mfa-step-up | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | OWASP | "Require reauthentication with an existing enrolled factor before allowing changes." | reauth before a factor change
svc-mfa-step-up | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | OWASP | "Do not rely solely on the active session, as it may be hijacked." | the session alone is not enough
svc-mfa-step-up | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | OWASP | "it may also be appropriate to require MFA for performing sensitive actions" | step-up before sensitive actions
svc-mfa-step-up | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | OWASP | "Changing passwords or security questions." | the sensitive actions
svc-mfa-step-up | https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html | OWASP | "Notify the user through out-of-band channels (such as email or push notification) whenever an MFA factor is changed." | notify after a factor change
svc-mfa-step-up | https://pages.nist.gov/800-63-4/sp800-63b/events/ | NIST | "When any new authenticator is bound to a subscriber account, the CSP SHALL ensure that the process requires authentication at either the maximum AAL currently available in the subscriber account or the maximum AAL at which the new authenticator will be used, whichever is lower." | fresh authentication at factor binding
svc-mfa-step-up | https://pages.nist.gov/800-63-4/sp800-63b/session/ | NIST | "A session MAY be considered at a lower AAL than the authentication event but SHALL NOT be considered at a higher AAL than the authentication event." | a session cannot be stronger than its authentication
svc-mfa-step-up | https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/protected-actions-overview | Microsoft | "When a user attempts to perform a protected action, they must first satisfy the Conditional Access policies assigned to the required permissions." | step-up at the action
svc-mfa-step-up | https://learn.microsoft.com/en-us/entra/identity/role-based-access-control/protected-actions-overview | Microsoft | "users are prompted only when needed." | step-up at the action, not every request
svc-mfa-step-up | https://auth0.com/docs/secure/multi-factor-authentication/step-up-authentication | Auth0 | "applications that allow access to different types of resources can require users to authenticate with a stronger authentication mechanism to access sensitive resources." | step-up for sensitive resources
svc-mfa-step-up | https://learn.microsoft.com/en-us/entra/identity/authentication/howto-registration-mfa-sspr-combined | Microsoft | "Users connected on a nontrusted network must either perform MFA or sign in by using a temporary access pass to register for MFA or reset their password by using SSPR." | fresh factor or recovery path before registering security info

## svc-account-linking

svc-account-linking | https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks | Microsoft | "the service fails to verify that the user actually owns the supplied identifier" | verify the identifier before use
svc-account-linking | https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks | Microsoft | "When a service merges an account created via the classic route with one created via the federated route (or vice-versa), the service must ensure that the user currently controls both accounts." | prove control of both
svc-account-linking | https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks | Microsoft | "If the service uses an IdP, it should check whether the IdP performs this verification or perform its own additional verification." | unverified IdP email
svc-account-linking | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP | "Identify the federated identity using the combination of iss (issuer) and sub (subject), not sub alone." | key on iss + sub
svc-account-linking | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP | "Do not automatically link accounts solely because their email, preferred_username, or other profile attributes match." | never link on a profile claim
svc-account-linking | https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html | OWASP | "Require an authenticated session with the existing application account before adding or removing linked identities" | prove control of the existing account
svc-account-linking | https://pages.nist.gov/800-63-4/sp800-63c/Federation/ | NIST | "the RP SHALL require an authenticated session with the subscriber account for all linking functions." | prove control of the existing account
svc-account-linking | https://pages.nist.gov/800-63-4/sp800-63c/Federation/ | NIST | "it is imperative that an RP never process the subject identifier without accounting for the IdP that issued the subject identifier." | key on iss + sub
svc-account-linking | https://auth0.com/docs/manage-users/user-accounts/user-account-linking | Auth0 | "For both manual and automatic account links, your tenant should request authentication for both accounts before linking occurs." | prove control of both
svc-account-linking | https://developers.google.com/identity/gsi/web/guides/verify-google-id-token | Google | "You can show a web page that allows the end user to input their password and link the legacy account with their Google credentials." | prove control of the existing account
svc-account-linking | https://developers.google.com/identity/gsi/web/guides/verify-google-id-token | Google | "Only use Google ID token sub field as identifier for the user as it is unique among all Google Accounts and never reused." | stable identifier
svc-account-linking | https://developers.google.com/identity/gsi/web/guides/verify-google-id-token | Google | "don't use email address as an identifier because a Google Account can have multiple email addresses at different points in time." | never key on email
svc-account-linking | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "the only guaranteed unique identifier for a given End-User is the combination of the iss Claim and the sub Claim." | key on iss + sub
svc-account-linking | https://openid.net/specs/openid-connect-core-1_0.html | OpenID Foundation | "other Claims such as email, phone_number, preferred_username, and name MUST NOT be used as unique identifiers for the End-User" | never key on a profile claim

## svc-password-reset

svc-password-reset | https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html | OWASP | "Single use and expire after an appropriate period." | single use and short life
svc-password-reset | https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html | OWASP | "Invalidated after they have been used." | single use
svc-password-reset | https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html | OWASP | "Stored in a secure manner, as discussed in the Password Storage Cheat Sheet." | hashed storage
svc-password-reset | https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html | OWASP | "After successful recovery, invalidate existing sessions and outstanding password reset and recovery links or codes so they cannot restore an attacker's access." | revoke sessions and other reset tokens
svc-password-reset | https://pages.nist.gov/800-63-4/sp800-63b/events/ | NIST | "Saved recovery codes SHALL be stored in the subscriber account in hashed form using an approved one-way function" | hashed storage
svc-password-reset | https://pages.nist.gov/800-63-4/sp800-63b/events/ | NIST | "Following the use of a saved recovery code, the CSP SHALL invalidate that recovery code" | single use
svc-password-reset | https://pages.nist.gov/800-63-4/sp800-63b/events/ | NIST | "Issued recovery codes SHALL be valid for at most: 10 minutes when sent via text message or voice; 24 hours when sent to an email address" | short life
svc-password-reset | https://auth0.com/docs/authenticate/database-connections/password-change | Auth0 | "The reset password link in the email is valid for one use only." | single use
svc-password-reset | https://auth0.com/docs/authenticate/database-connections/password-change | Auth0 | "If the user receives multiple password reset emails, only the password link in the most recent email is valid." | other reset tokens invalid
svc-password-reset | https://auth0.com/docs/authenticate/database-connections/password-change | Auth0 | "Resetting a user’s password makes their session expire." | revoke sessions
svc-password-reset | https://learn.microsoft.com/en-us/entra/identity/authentication/concept-sspr-howitworks | Microsoft | "users resetting their password receive an email notifying them that their password has been changed." | notify after reset
svc-password-reset | https://www.microsoft.com/en-us/msrc/blog/2022/05/pre-hijacking-attacks | Microsoft | "Sign out all other sessions and invalidate all other authentication tokens for that account" | revoke sessions and tokens
svc-password-reset | https://symfony.com/doc/current/security/reset_password.html | Symfony | "you might use a separate hasher for password recovery codes or API tokens." | hashed storage of recovery tokens
svc-password-reset | https://symfony.com/doc/current/security/reset_password.html | Symfony | "$hashedToken = $this->passwordHasher->hash($plaintextToken);" | hashed storage

## svc-api-key-scope

svc-api-key-scope | https://cloud.google.com/docs/authentication/api-keys | Google | "Unrestricted API keys are insecure." | narrow scope
svc-api-key-scope | https://cloud.google.com/docs/authentication/api-keys | Google | "API restrictions: Limit an API key to only be used with a specific set of APIs." | narrow scope
svc-api-key-scope | https://cloud.google.com/docs/authentication/api-keys | Google | "By periodically rotating your API keys, you can limit the impact of any compromised API keys." | rotation
svc-api-key-scope | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens | GitHub | "You should choose the minimal repository access that meets your needs." | narrow scope
svc-api-key-scope | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens | GitHub | "You should choose the minimal permissions necessary for your needs." | narrow scope
svc-api-key-scope | https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens | GitHub | "we highly recommend adding an expiration to your personal access tokens." | expiry
svc-api-key-scope | https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure | GitHub | "only select the minimum permissions or scopes needed, and set an expiration date for the minimum amount of time you'll need to use the token" | narrow scope and expiry
svc-api-key-scope | https://docs.github.com/en/rest/authentication/keeping-your-api-credentials-secure | GitHub | "Generate a new credential. Replace the old credential with the new one everywhere that you are storing or accessing the credential. Delete the old compromised credential." | revoke on exposure and rotate
svc-api-key-scope | https://docs.stripe.com/keys-best-practices | Stripe | "Follow the principle of least privilege" | narrow scope
svc-api-key-scope | https://docs.stripe.com/keys-best-practices | Stripe | "Use restricted API keys with limited permissions instead of unrestricted secret API keys." | narrow scope
svc-api-key-scope | https://docs.stripe.com/keys-best-practices | Stripe | "Rotate secret API keys periodically" | rotation
svc-api-key-scope | https://docs.stripe.com/keys-best-practices | Stripe | "When you create a secret API key in the Stripe Dashboard, you see it one time." | show once
svc-api-key-scope | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html | AWS | "use temporary security credentials (such as IAM roles) instead of creating long-term credentials like access keys" | prefer short-lived credentials
svc-api-key-scope | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html | AWS | "The secret access key can be retrieved only at the time you create it." | show once
svc-api-key-scope | https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html | AWS | "Regularly review, update, and delete access keys as needed." | rotation and revocation
svc-api-key-scope | https://docs.gitlab.com/security/tokens/ | GitLab | "When creating a scoped token, use the most limited scope possible to reduce the impact of an accidentally leaked token." | narrow scope
svc-api-key-scope | https://docs.gitlab.com/security/tokens/ | GitLab | "Consider setting a token that expires when your task is complete." | expiry
svc-api-key-scope | https://docs.gitlab.com/security/tokens/ | GitLab | "Review all active access tokens of all types on a regular basis and revoke any you don't need." | rotation and revocation
svc-api-key-scope | https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ | NIST | "All look-up secrets SHALL be stored in a hashed form using an approved hashing function." | hashed storage (Why)
svc-api-key-scope | https://pages.nist.gov/800-63-4/sp800-63b/authenticators/ | NIST | "A secret from a look-up secret authenticator SHALL be used successfully only once." | single use (Why)

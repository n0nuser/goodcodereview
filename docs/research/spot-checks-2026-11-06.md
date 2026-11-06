# Spot checks of research files G to L, 2026-11-06

Re-fetched by the coordinator with WebFetch. A row stays only if every quote checked matched.

| File | Page re-fetched | Quotes checked | Verdict |
|---|---|---|---|
| sec-classes-G | fastly.com host-header attacks | 4 | VERIFIED |
| sec-classes-G | learn.microsoft.com Kestrel security considerations | 4 | VERIFIED |
| sec-classes-G | developers.cloudflare.com avoid-web-poisoning | 4 | VERIFIED |
| sec-classes-G | cloud.google.com/cdn/docs/caching (now redirects to docs.cloud.google.com) | 2 | VERIFIED; caveat: `FORCE_CACHE_ALL` lifts the Authorization restriction |
| sec-classes-H | learn.microsoft.com Entra auth-code flow | 3 (+nonce) | VERIFIED |
| sec-classes-H | auth0.com validate-id-tokens | 3 | VERIFIED |
| sec-classes-H | OWASP OAuth2 cheat sheet | 2 | VERIFIED |
| sec-classes-I | nodejs.org/api/zlib.html | 3 | VERIFIED; caveat: `zipEntry.contentIterator()` maxSize default is "no limit" (streaming is bounded per chunk) |
| sec-classes-I | OWASP Multi-Tenant Security cheat sheet | 4 | VERIFIED |
| sec-classes-I | docs.slack.dev verifying requests | 3 | VERIFIED |
| sec-classes-I | learn.microsoft.com EF Core global query filters | 3 | VERIFIED |
| smells-J | learn.microsoft.com CA1505 | 2 (default 10, scope) | VERIFIED |
| smells-J | checkstyle MethodLength | 2 (rationale, default 150) | VERIFIED |
| smells-K | jetbrains.com FieldCanBeLocal | 2 | VERIFIED |
| third-orgs-L | jetbrains.com LawOfDemeter | 2 (Java inspection, ignoreLibraryCalls default Selected) | VERIFIED |
| third-orgs-L | blog.ndepend.com shotgun-surgery | 2 (company blog, no named author) | VERIFIED |
| third-orgs-L | scipy.github.io CI page | 3 (5 s full, 1 s fast, per test) | VERIFIED |

No row dropped. Stable cards still need every quote they cite re-fetched before promotion.

## Second round (files M, N, O, Q)

| File | Page re-fetched | Quotes checked | Verdict |
|---|---|---|---|
| draft-gaps-Q | about.gitlab.com pipeline metrics blog | 2 (45-minute MR pipeline target) | VERIFIED |
| draft-gaps-Q | developer.apple.com WWDC20 10680 transcript | 2 | VERIFIED; note: about Objective-C string constants imported into Swift, not return values as such |
| sec-gaps-O | symfony.com password hashing page (URL reset_password.html) | 2 | VERIFIED; note: the hasher is for "password recovery codes or API tokens", the page is mainly about password hashing |
| test-practices-N | guides.rubyonrails.org testing | 2 (per-worker database) | VERIFIED |
| test-practices-N | abseil.io SWE book ch. 11 | 2 (small tests: no network or disk) | VERIFIED |
| ide-files-M | intellij-support.jetbrains.com 206544839 (403 to WebFetch, read in Chrome) | 3 | VERIFIED |
| sec-gaps-P | sequelize.org paranoid | 2 | VERIFIED |
| sec-gaps-P | httpd.apache.org mod_deflate | 3 (0 = no limit; ratio default 200) | VERIFIED; the body-sentence wording "specifies the maximum size of an inflated request body" not confirmed word for word (directive summary says "Maximum size of inflated request bodies") |
| sec-gaps-P | cloud.google.com pubsub ordering | 3 | VERIFIED |

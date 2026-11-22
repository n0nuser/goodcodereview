# Docs and comments practices: org pass 2a (Spotify, Stripe, Atlassian, Cloudflare, Shopify)

Fetched 2026-11-22 with WebFetch (page text summarised by the fetch model, not read raw). Practice numbers as in docs-comments-orgs-pass.md: (1) docs/comments updated in the same change as code; (2) delete wrong or obsolete docs, archive design docs; (3) short comments, long explanation to linked docs; (4) minimum viable docs, README per directory, link instead of duplicating.

Result: no page from these five orgs backs practices 2 or 3. One row each for 1 and 4, both weak.

## Rows

1. https://github.com/Shopify/ruby-style-guide. Shopify. Update a comment whenever the code it describes changes, so the two do not drift apart. Backs 1 (comments only; no review or docs rule).
2. https://engineering.atspotify.com/2019/10/solving-documentation-for-monoliths-and-monorepos. Spotify. Docs live as close to the code as possible, with a per-folder docs config in a monorepo instead of one root docs folder or one README everywhere. Backs 4 (placement, weakly; says nothing on minimum docs or linking).
3. https://backstage.io/blog/2020/09/08/announcing-tech-docs. Spotify (Backstage). Docs are Markdown in the code repo and move through the same CI and review workflow as code; code examples are embedded from source rather than copied, so they do not go stale. Backs 1 (weakly: same workflow, no "same change" rule) and 4 (embed instead of duplicate).
4. https://developers.cloudflare.com/style-guide/documentation-content-strategy/content-types/changelog/. Cloudflare. A changelog entry stays short and points to the page that documents the change, and is written once and reused. Backs 4 (link instead of duplicating; scoped to changelog entries).

## Not counted (read, no qualifying practice)

- https://developers.cloudflare.com/style-guide/how-we-docs/redirects/. Cloudflare. Deleting or moving a page needs a redirect in the same PR, with a bot reminder and CI checks. This is about handling deletion, not a rule to delete obsolete docs. Not a card for 2, but see lead A.
- Cloudflare documentation-content-strategy index, content-types page, how-we-docs index, cloudflare-docs CONTRIBUTING.md: no practice on 1-4. The FAQ type says to link to the source of truth, mentioned only in passing.
- stripe-node CONTRIBUTING.md: links to the README for setup instead of repeating it; no stated rule.
- Stripe docs culture: only secondhand (Mintlify, Slab, Pragmatic Engineer, First Round). They say doc expectations sit in the career ladder and performance reviews. No Stripe primary page found; not counted.
- Atlassian: only a community post ("The Documentation Paradox") and nothing from Atlassian engineering; the fetch returned no article text. Not counted.
- Backstage TechDocs feature page: docs live with code; nothing on updating, deleting, or linking.

## Not reached

- https://github.com/Shopify/polaris/blob/main/.github/contributing.md (404)
- https://github.com/Shopify/shopify-dev/blob/main/CONTRIBUTING.md (404)
- https://shopify.engineering/shopify-development-handbook and /shopify-dev-docs-gitbook (404; guessed URLs, web search found no Shopify docs-practice post)
- https://www.atlassian.com/team-playbook/plays/documentation-health (404)
- https://developers.cloudflare.com/style-guide/how-we-docs/link-maintenance/ (404; the index lists a Link maintenance subpage under another path)
- https://community.atlassian.com/t5/Teamwork-Lab-articles/The-Documentation-Paradox/ba-p/2936344 (no article text returned)
- Spotify: no post found on deleting stale docs. Atlassian: no engineering-blog post found. Both searched once.

## New-card leads (checkable, no existing row covers them)

A. Moving or deleting a doc page adds a redirect in the same PR (Cloudflare redirects page); CI rejects redirect chains and loops.
B. Code examples in docs are embedded from source files, not pasted copies (Backstage TechDocs announcement).
C. Docs show owner and last-updated date, and open doc issues are routed to the owning team (Backstage TechDocs announcement; Spotify notes the date alone does not prove quality).
D. Docs ownership declared via CODEOWNERS on the files each team owns (Backstage TechDocs announcement).
E. Each page has a declared content type (how-to, reference, concept, changelog, FAQ) and title, description metadata (Cloudflare content strategy index).
F. Comments explain why, not what, and skip the obvious (Shopify ruby-style-guide; same as Google, already noted).

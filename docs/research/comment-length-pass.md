# Long comments: sources for `fn-comments-stay-short`

Searched 2026-11-21. Paraphrase only. Each row gives the URL, the org, and the clause of the card it backs.

1. https://google.github.io/styleguide/docguide/best_practices. Google. Inline comments carry what the code cannot, such as why it is there. Long reasoning belongs in a design doc that serves as the archive of the decision. Backs the Rule.

Count: Google = 1 org. The card stays a draft (`lacks: orgs`). Searches for Rust, Go, Mozilla, Microsoft, Apache, Kubernetes and Angular guides found no page that states the practice. Lint tools that cap comment length exist (Go `commentlen`, `maxcomments-lint`; ESLint `comment-length`; Ruff W505) but they are tools, not an organisation's stated practice.

## Google docguide, further practices (fetched 2026-11-21)

Backs `chg-docs-updated-with-code` ("Update Docs with Code": change docs in the same change; reviewers insist docstrings and READMEs are updated) and `code-dead-docs-deleted` ("Delete Dead Documentation": delete known-wrong docs; "Documentation is the Story of Your Code": archive design docs as decision records after implementation). One org (Google) each, so both are drafts.

Not carded, one org and mostly covered: minimum viable docs (see `fn-comments-stay-short`), README per directory, link instead of duplicating a shared guide, doc behaviour has a test.

Also added as a source to existing cards: `fn-comments-explain-why` (inline comments say why) and `code-adr` (design docs become decision records). Google already counts there, so neither card gains an organisation.

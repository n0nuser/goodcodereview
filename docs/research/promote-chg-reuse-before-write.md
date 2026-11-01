# chg-reuse-before-write: promotion pass

Fetched 2026-11-01 with curl and WebFetch. Quotes were read on the live pages. Rule before: "Search the repo for an existing helper before adding a new one. The author names where they searched." Clause A is "search first". Clause B is "author names where they searched".

1. https://github.blog/ai-and-ml/generative-ai/agent-pull-requests-are-everywhere-heres-how-to-review-them/ (org: GitHub). "For every new helper or utility in an agent pull request, do a quick search. If you find an equivalent, don't leave a comment. Require consolidation before merge." Its review table says: "Search for new functions, helpers, or modules. For each one, do a quick repo search to check for duplicates." Backs A. For B it says only "Require justification for adding new utilities in agent pull requests above a size threshold", which is not naming where the author searched.
2. https://cursor.com/learn/understanding-your-codebase (org: Cursor). "The agent might create a new utility function when one already exists, or use a different pattern than the rest of your codebase. Before asking for changes, ask the agent to explore first". Backs A. Does not back B.
3. https://github.com/google-gemini/gemini-cli/blob/main/.gemini/skills/review-duplication/SKILL.md (org: Google, repository owner google-gemini; file last changed 2026-03-26). The Gemini CLI team's review skill: "proactively investigate the codebase for duplicated functionality, reinvented wheels, or failure to reuse existing project best practices and shared utilities". It tells the reviewer to name "the absolute or project-relative file path and the specific symbol ... that should be reused". Backs A. It names the existing helper, not where the author searched, so B is not backed.
4. https://www.kernel.org/doc/html/latest/process/coding-style.html (org: Linux kernel). "Don't re-invent the kernel macros ... macros that you should use, rather than explicitly coding some variant of them yourself." States use-existing, not search-first. Kept in `borrowed_from` as support, not counted.

Not usable: Anthropic's best-practices page and the GitLab frontend guide had no sentence on finding existing helpers. Microsoft's hve-core template says "Never duplicate logic" (DRY, not search). OpenStack's review guidelines say to point authors to an existing utility, but the wiki page did not load by curl, so it was not read. Many "search first" agent skills (skills.sh, claudskills) are personal or third-party and do not count.

Count, clause A: GitHub, Cursor, Google = 3 organisations. All three are from AI-assisted-review guidance, so a reviewer should judge whether "repo" in the Rule is broad enough. Clause B: 0 organisations. It moved out of the Rule (PROMOTION.md rule 2): the sentence "The author names where they searched." is deleted from the Why.

Rule edit: none to the Rule line; the second sentence was in the Why and is removed.

orgs.py rows needed: `cursor.com` -> `cursor` (org exists, "Cursor"; only the `github.com/cursor/plugins/` prefix is mapped); `github.com/google-gemini/` -> `google` ("Google").

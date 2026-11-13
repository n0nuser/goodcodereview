# Whole-level file vs hub plus per-context parts

Date: 2026-11-11. Question: keep service.md as one file (104.7K chars, about 25K tokens, 61 cards an agent must all check), or serve a hub plus 5 part files, or both.

Verification key: "opened" means I fetched the page or PDF this session and read the cited text. "Secondary" means a third-party write-up. "Unverified" means I could not confirm it.

## Short answer

Do both. Keep the whole file, add the parts, and point llms.txt and the hub at the parts first. Reason: the whole file is over the afdocs fail threshold (100K chars) and over the limit where Claude Code's WebFetch truncates, so a fetch tool can silently cut or summarize it. The long-context papers say 25K tokens costs some accuracy but is not catastrophic. The splitting risk (agent skips parts) is real but can be made visible with a count the agent must report. Details and the evidence that would change this are in section 5.

## 1. Long-context quality

All five sources below were opened. None tests the exact case here (an exhaustive 61-item checklist at about 25K tokens), so treat the numbers as direction, not prediction.

**Lost in the Middle** (Liu et al., arXiv 2307.03172, https://arxiv.org/abs/2307.03172). Opened abstract and PDF text. Tasks: multi-document QA and key-value retrieval. Models: MPT-30B-Instruct, LongChat-13B (16K), GPT-3.5-Turbo, Claude-1.3 (PDF intro, https://arxiv.org/pdf/2307.03172). Lengths: 20 documents is about 4K tokens, 30 documents about 6K tokens (PDF). Finding: accuracy is highest when the relevant item is at the start or end and drops when it is in the middle. Also, going from 20 to 50 retrieved documents improved accuracy only about 1 to 1.5 percent. Limits for us: tiny contexts by today's standard, 2023 models, one relevant item per query.

**RULER** (Hsieh et al., COLM 2024, arXiv 2404.06654, https://arxiv.org/abs/2404.06654). Opened abstract and PDF text. 17 long-context models, lengths 4K to 128K, 13 tasks in four categories: retrieval, multi-hop tracing, aggregation, QA. Models include Gemini-1.5-Pro, GPT-4, Llama3.1 (70B and 8B), Qwen2-72B, Command-R-plus, GLM4, Mixtral-8x22B, Yi-34B, Phi3-medium, Mistral-v0.2 (PDF Table 3). Finding: near-perfect on vanilla needle-in-a-haystack but large degradation on harder tasks as length grows; "only half of them can effectively handle sequence length of 32K" (PDF). By my reading of Table 3, effective length at the 4K-baseline threshold was 64K for GPT-4 and Llama3.1-70B, 32K for Qwen2-72B, Command-R-plus, Llama3.1-8B, Mixtral, Yi and Phi3, and 16K or lower for Mistral-v0.2 and the smaller models. Aggregation tasks (common and frequent word extraction) are the closest proxy to "check all items"; the paper names two failure modes there: using parametric knowledge instead of the context, and inaccurate aggregation (PDF appendix). I did not extract per-task scores, so I cannot say how much aggregation drops at 32K. Limits: 2024 models, none of today's.

**NoLiMa** (Modarressi et al., ICML 2025, arXiv 2502.05167, https://arxiv.org/abs/2502.05167). Opened abstract. 13 models claiming 128K or more, tested from under 1K to 32K tokens. At 32K, 11 of 13 fall below 50 percent of their short-context baseline; GPT-4o drops from 99.3 to 69.7 percent. Needles have little word overlap with the question, so this is the hard case. Our checklist cards probably have high overlap with the review task (the agent compares code against named rules), which is the easier case. That is my inference, not a result from the paper.

**Context Rot** (Chroma, https://www.trychroma.com/research/context-rot; old URL research.trychroma.com redirects there). Opened. 18 models (Claude Opus 4, Sonnet 4, 3.7, 3.5, Haiku 3.5; GPT-4.1 family, o3, GPT-4o; Gemini 2.5 and 2.0; Qwen3). Findings: accuracy falls with input length for all models, faster for lower needle-question similarity; one distractor hurts and four hurt more; LongMemEval full prompts (about 113K tokens) scored below focused prompts (about 300 tokens), with Claude showing the largest gap, mostly from abstaining. Needle position had no notable effect in their test, which differs from Lost in the Middle. This is a vendor report, not peer reviewed.

**Context Length Alone Hurts** (Du et al., Findings of EMNLP 2025, arXiv 2510.05381, https://arxiv.org/abs/2510.05381). Opened abstract. Five models, math, QA and code. Accuracy fell 13.9 to 85 percent as input grew, even with perfect retrieval and with irrelevant tokens masked. Having the model restate the relevant evidence first helped (up to 4 percent for GPT-4o on RULER). Relevance for us: a checklist task can degrade from length alone, and "restate the cards, then check them" is a cheap mitigation that works with either layout.

**IFScale** (Jaroslawicz et al., arXiv 2507.11538, https://arxiv.org/abs/2507.11538). Opened abstract. 20 models, up to 500 simultaneous keyword instructions in a report-writing task. Best models reach 68 percent at 500 instructions; models favor earlier instructions. This is the closest published proxy for "apply many rules at once", but 61 rules is far below its top density and the task is generation, not review. I did not read the per-density curve, so I cannot say what accuracy is at 61.

Reading across: all of these show accuracy declining with length and task difficulty. At 25K tokens the decline is measurable but most 2024-25 frontier models were still above their threshold at 32K on RULER. The sources do not test the models agents run today (Claude 4.x/5-era, GPT-5.x), so none of this settles whether 25K is safe now. A first-party test is the only way to know.

## 2. What splitting buys and costs

**Anthropic, Effective context engineering for AI agents** (opened, https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents). Supports splitting: recall "decreases" as context grows, context is "a finite resource with diminishing marginal returns", and agents can "assemble understanding layer by layer". It states the cost directly: "runtime exploration is slower than retrieving pre-computed data", it needs "opinionated and thoughtful engineering", and without guidance an agent can "waste context by misusing tools, chasing dead-ends". It suggests a hybrid (some data up front, some on demand) for less dynamic content.

**Agent Skills docs** (opened, https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices). Progressive disclosure is the official pattern: keep SKILL.md under 500 lines, link to reference files. Two points matter here. First, "Claude might partially read files when they're referenced from other referenced files... might use commands such as `head -100` to preview content... resulting in incomplete information", so keep references one level deep from the entry file. Second, for files over 100 lines include a table of contents at the top so a partial read still shows the full scope. Both are direct evidence of silent incompleteness, from the vendor, and both favor a flat hub (hub links straight to the 5 parts, parts do not link onward). The same page recommends a copyable checklist so the agent can "track its progress" through multistep work.

**Multi-hop and stopping studies.** Opened: arXiv 2601.19827 (https://arxiv.org/abs/2601.19827), a diagnostic study on 11 LLMs in scientific multi-hop QA. It lists "incomplete hop coverage" (a reasoning chain leaves hops unaddressed) as a failure that persists under iterative retrieval, and "high composition failure rates even with perfect retrieval". Seen only in a search snippet, not opened: HALT (arXiv 2608.02009) and Stop-RAG (arXiv 2510.14337) on stopping policies, and PAR2-RAG (arXiv 2603.29085) on committing before evidence is sufficient. Treat those three as unverified. I found no study that isolates chunk boundaries as the cause of skipped follow-up pages, so the claim "splitting makes agents skip parts" is supported by analogy and by the trace data in section 4, not by a direct experiment.

Costs of splitting, as supported:

- Missed parts: agents may stop before all 5 parts (section 4: median 2 docs pages per run).
- Extra round trips: 6 fetches instead of 1, each with latency (Anthropic post, above).
- Silent incompleteness: an agent can report a review as done after 3 of 5 parts, and nothing in the output shows it. The whole file has the same problem in a different form when a tool truncates it (section 3).
- Partial reads of linked files (Agent Skills docs, above).

## 3. Fetch tooling limits

**Claude Code WebFetch.** Anthropic's tool description in this session says it fetches, converts HTML to markdown, and "answers prompt against it using a small fast model", with an `offset` parameter for "a page too long for one call" (the tool's own schema, first party). Third-party reverse engineering (secondary): result truncated to 100 KB of text with a warning, run through Haiku 3.5, 15-minute cache (https://mikhail.io/2025/10/claude-code-web-tools/, opened). A search summary also reported that markdown under 100K characters skips the small-model step; mikhail.io says plain text still goes to Haiku, so that point conflicts and is unverified. A user issue about WebFetch truncating large documentation pages exists (https://claudeissues.com/issue/22937-webfetch-tool-truncates-large-documentation-pages-preventing-access-to-critical) but the host did not resolve, so I did not open it. Consequence for us: a 104.7K-char file is at or over the reported truncation point, and a small summarizing model sits between the file and the agent. Summarization is the worst case for "check all 61 cards".

**Cursor.** A forum thread on indexing a 4 MB llms.txt as Docs suggests splitting into smaller files; the thread states no hard cap and I found no official figure (https://forum.cursor.com/t/is-there-any-size-limit-for-llms-txt-indexed-as-docs/148660, seen in search results, not opened). Third-party guides say attached files over the limit are reduced to the most relevant chunks (unverified). Mintlify reports splitting llms.txt by navigation section with a root index, because splitting by character count gave ambiguous files (https://www.mintlify.com/blog/scaling-llms-txt, search result only, not opened).

**ChatGPT browsing.** I found nothing on its page-length handling. Unverified, no claim made.

**Why afdocs uses 100K.** Opened https://afdocs.dev/checks/page-size. The check `page-size-markdown` passes under 50,000 characters, warns from 50,000 to 100,000, and fails above 100,000; `page-size-html` uses the same bands after conversion to text. Stated rationale: "Agent platforms have diverse truncation limits, from 5K characters on some platforms to over 100K on others", truncation is silent ("the agent sees the beginning of the page and loses the rest"), and 100K+ is truncated by "all major agent platforms" (unnamed; I could not verify that claim). So 100K is the point where the spec says truncation is near certain, and 50K is the "some platforms still cut" band. I did not find a published derivation of the number beyond that. The same page says paginated markdown can look complete when it is not, and that truncation removes trailing notes first, so a "part 1 of 5" note at the bottom would be the first thing lost; put it at the top (the single-fetch check counts a declaration as at the top within the first 10 percent of content).

Applied: service.md at 104.7K fails. Five parts of about 21K each pass with margin, and a hub of a few thousand characters passes easily.

## 4. AgentReady trace data

Source: https://raw.githubusercontent.com/agentready-org/standard/main/data/traces.csv, downloaded to my scratch dir and parsed with `python3 -I`. 1,033 runs, 25 sites, models claude-haiku-4-5 (327), claude-sonnet-4-6 (236), gpt-5.4 (236), claude-fable-5 (234), harnesses claude-agent-sdk and eve, collected June to August 2026 (data README, https://raw.githubusercontent.com/agentready-org/standard/main/data/README.md). Tasks are lookup tasks (find pricing, find rate limits, integrate an API), not exhaustive reviews.

Docs pages fetched per run (`docs_pages_fetched`):

- Mean 2.78, median 2, max 20.
- 178 runs (17.2%) fetched zero docs pages; 204 fetched one; 235 fetched two.
- 196 runs (19.0%) fetched 5 or more; 149 (14.4%) fetched 6 or more. A hub plus 5 parts needs 6.
- By model, mean pages: haiku-4-5 3.41, sonnet-4-6 2.92, gpt-5.4 2.66, fable-5 1.88 (median 1).

Hub following:

- 329 runs reached llms.txt. Of the 325 with a value, 117 (36%) later fetched at least one page it lists (`llms_followed_listing`); 208 did not.
- Runs that followed the listing fetched more docs pages: mean 3.17 vs 2.43 for those that did not.
- The data cannot answer "did they fetch ALL children". The column is a yes/no for at least one listed page, and there is no per-hub child count. So the claim that agents fetch every child of an index is neither supported nor refuted. What the data does show is that fetching many pages is the exception: 3 or more docs pages in 416 of 1,033 runs (40%), 6 or more in 14%.
- Answer grounding was 86.1% for runs with 3+ docs pages and 78.8% for runs with fewer, so more fetching correlated with better grounding, but this is correlation across different tasks and sites.

Caveat: these agents were answering a narrow question, so stopping early was correct for them. A review task that states "check all 61 cards" is a different instruction and may be followed differently. The traces show the default behavior is to fetch few pages, which is the risk for a 6-page layout if the hub does not force completion.

## 5. Recommendation

**Both.** Keep service.md; add the hub and 5 parts; make the hub the entry that llms.txt links by default.

Concrete shape (design suggestions, nothing implemented):

1. Hub at the top of its own file lists all 5 parts with card count per part and the total (61), and says in the first lines "you must read all 5 parts; report which you read". The top-of-file placement follows the afdocs rule.
2. Each part states "part N of 5, cards a to b of 61" at the top, and the hub links parts directly (one level deep, per Agent Skills guidance). No part links to other parts as its only route.
3. The review output asks the agent to list cards checked by ID, so a skipped part shows as a missing ID range. This turns silent incompleteness into a visible gap. It also applies the "restate the evidence first" mitigation from Du et al.
4. llms.txt describes the whole file as "single file, 104.7K chars, may be truncated by fetch tools; use only if you can download it to disk" and the hub as the default.
5. Optional: trim the whole file under 100K to clear the afdocs fail band, though that means removing 4.7K chars of content; do not do this just to pass a check.

Why not whole-only: it fails page-size-markdown (3), is at the reported WebFetch truncation point, and is the case where a small summarizing model may drop cards. Why not parts-only: agents with shell access can download and read the whole file reliably, the whole file avoids the extra round trips, and removing it breaks existing links. Why not hub-only without the count: traces show most agents stop after a few pages.

What would change this:

- Whole-file only is right if a first-party test (same review task, 61 cards, current models, each harness you care about) shows no meaningful drop in cards covered versus the parts layout, and the harnesses tested return the file untruncated and unsummarized. A fetch tool that returns raw text up to 10 MB (afdocs transfer check) would support it.
- Parts-only is right if the test shows agents consistently read all 5 parts when the hub gives the count, and the whole file loses cards in the middle.
- Drop the parts if ID-coverage logs from real runs show agents routinely finishing with a part missing even with the count, and the whole file does not show the same loss.
- The cheapest decisive experiment: run N reviews per layout per model, record the set of card IDs reported, and compare coverage. I did not run it.

## Gaps

- No source tested exhaustive checklist application at 25K tokens on current models.
- RULER per-task aggregation scores and IFScale density curves were not extracted.
- ChatGPT browsing, Cursor page limits: no verified data.
- Claude Code truncation figure and Haiku model are from third-party analysis; the 15-minute cache and the small-model description match the tool's own description.
- HALT, Stop-RAG, PAR2-RAG: seen in search results only.

## Implemented 2026-11-11

Parts say "part N of M" with their card range and total, name the other parts, and point to the whole file with its size (`tools/site_twins.py`). `llms.txt` lists the parts first, then the whole file with a truncation warning (`tools/skill_files.py`). `agent_ready_check.py` item 54 checks it. Not done: asking agents to list checked card ids in the verdict (changes skill text, so it needs eval runs), and the A/B experiment.

## Experiment, 2026-11-12 (tools/eval_layout.py)

Same `service` review of the `audit_repo` files, Sonnet 5.5 through `claude -p` with Read, Grep and Glob, 3 runs per layout, checklist as local files. Score: card ids reported, of the 59 core stable ids.

| Layout | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| whole file only | 59 | 59 | 59 |
| five parts only | 59 | 59 | 59 |
| `llms.txt` with both | 59 | 59 | 59 |

A first parts-only run scored 42 of 59 three times. It was a staging error: the part headers link to https://goodcodereview.com/..., which does not exist beside the files, so the agent said the other parts "were not given". After the links were made local, coverage was complete. The lesson stands for real use: a part header that tells an agent to read the others only helps if those links resolve, and the headers already use absolute URLs.

What it does not show: truncation or summarising by a fetch tool (the Read tool returned the 105K-character file), other models, harnesses without a Read tool, and larger repos. N is 3. The result says parts with "part N of M" headers lose no cards for an agent that can open the links, not that fetch tools will not truncate the whole file. Keep both files and the warning.

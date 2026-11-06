# Graph Report - goodcodereview  (2026-11-04)

## Corpus Check
- Large corpus: 520 files · ~256,924 words. Semantic extraction will be expensive (many Claude tokens). Consider running on a subfolder.

## Summary
- 851 nodes · 1949 edges · 37 communities (28 shown, 9 thin omitted)
- Extraction: 92% EXTRACTED · 8% INFERRED · 0% AMBIGUOUS · INFERRED: 156 edges (avg confidence: 0.92)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Site config and budgets
- Index schema tests
- Agent-readiness checks
- Eval runner
- Link-check tests
- JS test tooling
- CLI package
- Release and security tests
- CLI commands
- Build core and index parts
- Errors and models
- Build tests
- Card field parsing
- Release workflow
- Skill sync workflow
- Packs and twins
- Promote-draft form
- Build context
- Card proposal form
- Check workflow
- Bug form
- Card correction form
- Card backers and stability
- Guides pages
- Concerns page
- Accepted-risk demo app
- Dependabot config
- Issue config
- Index line rendering
- Wrap script
- Misc
- Misc

## God Nodes (most connected - your core abstractions)
1. `Card` - 42 edges
2. `BuildInput` - 40 edges
3. `BuildError` - 26 edges
4. `Page` - 25 edges
5. `Level` - 24 edges
6. `page()` - 23 edges
7. `skill_output()` - 22 edges
8. `cards_files()` - 20 edges
9. `Report` - 18 edges
10. `main()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `test_the_plan_is_deterministic()` --uses--> `Plan`  [INFERRED]
  test/test_build.py → tools/build.py
- `test_sitemap_lists_each_slug_with_the_build_date()` --calls--> `sitemap()`  [INFERRED]
  test/test_build.py → tools/site_meta.py
- `test_inline_renders_code_bold_and_card_links()` --calls--> `inline()`  [INFERRED]
  test/test_build.py → tools/markdown.py
- `test_rule_reads_the_first_paragraph()` --calls--> `rule()`  [INFERRED]
  test/test_build.py → tools/markdown.py
- `test_no_draft_is_block_and_context_uses_the_closed_list()` --calls--> `load_cards()`  [INFERRED]
  test/test_skill.py → tools/validate.py

## Import Cycles
- None detected.

## Communities (37 total, 9 thin omitted)

### Community 0 - "Site config and budgets"
Cohesion: 0.05
Nodes (37): buttons(), card_html(), chips(), copy_pre(), _filters(), icon(), lacks_html(), link_text() (+29 more)

### Community 1 - "Index schema tests"
Cohesion: 0.06
Nodes (33): test_the_index_schema_rejects_a_missing_or_extra_key(), json_schema(), test_a_card_without_orgs_fails(), test_a_missing_key_fails(), test_a_reason_outside_the_list_fails(), test_a_value_outside_the_enum_fails(), test_an_unknown_key_fails(), test_built_files_match_the_schema() (+25 more)

### Community 2 - "Agent-readiness checks"
Cohesion: 0.08
Nodes (21): _items_14_29_37_42(), _items_15_16_17_19(), _items_1_12_30(), _items_20_38(), _items_21_33(), _items_22_23(), _items_25_28(), _items_2_3_4() (+13 more)

### Community 3 - "Eval runner"
Cohesion: 0.07
Nodes (26): stream(), test_bare_reply_is_graded_on_substance_only(), test_command_for_claude_forced(), test_command_for_opencode_forced_asks_to_load_the_skill(), test_command_for_opencode_with_a_model(), test_every_case_is_well_formed_and_names_stable_cards(), test_query_file_is_balanced_and_split(), test_scoped_review_may_not_cite_other_concerns() (+18 more)

### Community 4 - "Link-check tests"
Cohesion: 0.06
Nodes (27): test_fenced_code_is_skipped(), test_links(), test_repeated_headings_get_numbered_anchors(), test_the_message_names_file_and_line(), test_the_repository_docs_resolve(), write(), errors_for(), test_a_creator_source_satisfies_the_floor() (+19 more)

### Community 5 - "JS test tooling"
Cohesion: 0.06
Nodes (35): description, devDependencies, axe-core@^4.14.0, jsdom@^30.1.3, name, private, axe-core, jsdom (+27 more)

### Community 6 - "CLI package"
Cohesion: 0.06
Nodes (25): cards_json(), plan(), site_text(), level_files(), test_check_concern_files(), test_check_index_fails_on_a_changed_rule(), test_check_union(), test_each_card_is_in_the_file_of_its_own_level() (+17 more)

### Community 7 - "Release and security tests"
Cohesion: 0.09
Nodes (22): test_security_txt_expires_180_days_after_the_build_date(), describe(), _encode(), main(), Plan, plan_build(), site_files(), _stale() (+14 more)

### Community 8 - "CLI commands"
Cohesion: 0.09
Nodes (22): cards(), fetch(), main(), main(), component(), test_a_missing_licence_fails(), test_a_missing_or_stale_file_fails(), test_current_file_passes() (+14 more)

### Community 9 - "Build core and index parts"
Cohesion: 0.09
Nodes (20): level_of(), BuildError, IndexPart, Level, _check_indexes(), _check_routes(), _frontmatter(), _head() (+12 more)

### Community 10 - "Errors and models"
Cohesion: 0.09
Nodes (17): ToolError, Concern, Context, LacksReason, ParsedFront, RawCard, Route, Severity (+9 more)

### Community 11 - "Build tests"
Cohesion: 0.09
Nodes (17): test_a_failed_budget_leaves_the_skill_untouched(), test_build_date_falls_back_to_today_outside_git(), test_check_md_flags_unsupported_markdown(), test_check_md_ignores_code_fences(), test_dry_run_writes_nothing(), test_inline_renders_code_bold_and_card_links(), test_internal_links_and_anchors_resolve_in_rendered_pages(), test_no_markdown_left_in_rendered_pages() (+9 more)

### Community 12 - "Card field parsing"
Cohesion: 0.16
Nodes (12): concerns(), lacks(), markdown_url(), page_name(), topics(), section(), Card, DraftLack (+4 more)

### Community 13 - "Release workflow"
Cohesion: 0.11
Nodes (18): GH_TOKEN, jobs, release, name, on, push, permissions, contents (+10 more)

### Community 14 - "Skill sync workflow"
Cohesion: 0.11
Nodes (18): concurrency, cancel-in-progress, group, jobs, sync, name, on, push (+10 more)

### Community 15 - "Packs and twins"
Cohesion: 0.22
Nodes (10): pack_name(), guides_index_text(), Twin, _concerns_page(), front(), _index_page(), markdown_twins(), audit_twin() (+2 more)

### Community 16 - "Promote-draft form"
Cohesion: 0.12
Nodes (15): description, label, options, placeholder, body, attributes, id, type (+7 more)

### Community 17 - "Build context"
Cohesion: 0.20
Nodes (6): href(), BuildInput, read_input(), source_errors(), LevelCount, NavLink

### Community 18 - "Card proposal form"
Cohesion: 0.14
Nodes (13): description, label, multiple, options, render, body, attributes, id (+5 more)

### Community 19 - "Check workflow"
Cohesion: 0.14
Nodes (13): runs-on, steps, jobs, check, name, on, if, name (+5 more)

### Community 20 - "Bug form"
Cohesion: 0.15
Nodes (12): description, label, options, render, body, attributes, id, type (+4 more)

### Community 21 - "Card correction form"
Cohesion: 0.17
Nodes (11): description, label, options, body, attributes, id, type, validations (+3 more)

### Community 22 - "Card backers and stability"
Cohesion: 0.23
Nodes (7): backers(), is_core(), is_stable(), _draft_files(), draft_line(), _llms_drafts(), url()

### Community 23 - "Guides pages"
Cohesion: 0.25
Nodes (5): Guide, guide_text(), _links(), _figure_pattern(), rule()

### Community 25 - "Accepted-risk demo app"
Cohesion: 0.39
Nodes (3): card_line(), files(), markdown()

### Community 26 - "Dependabot config"
Cohesion: 0.29
Nodes (6): interval, updates, directory, package-ecosystem, schedule, version

### Community 27 - "Issue config"
Cohesion: 0.33
Nodes (5): blank_issues_enabled, contact_links, about, name, url

### Community 28 - "Index line rendering"
Cohesion: 0.40
Nodes (5): context(), _context_line(), draft_section(), index_line(), _level_index()

## Knowledge Gaps
- **2 isolated node(s):** `goodcodereview`, `goodcodereview`
  These have ≤1 connection - possible missing edges. (Counts symbols only; 358 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Card` connect `Card field parsing` to `Site config and budgets`, `Index schema tests`, `Build core and index parts`, `Errors and models`, `Packs and twins`, `Build context`, `Card backers and stability`, `Index line rendering`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 30 inferred relationships involving `Card` (e.g. with `backers()` and `concerns()`) actually correct?**
  _`Card` has 30 INFERRED edges - model-reasoned connections that need verification._
- **What connects `goodcodereview`, `goodcodereview` to the rest of the system?**
  _2 weakly-connected nodes found - possible missing edges._
- **Should `Site config and budgets` be split into smaller, more focused modules?**
  _Cohesion score 0.050286058416139714 - nodes in this community are weakly interconnected._
- **Why does `BuildInput` connect `Build context` to `Site config and budgets`, `Index schema tests`, `Release and security tests`, `Build core and index parts`, `Card field parsing`, `Packs and twins`, `Card backers and stability`, `Guides pages`?**
  _High betweenness centrality (0.020) - this node is a cross-community bridge._
- **Are the 26 inferred relationships involving `BuildInput` (e.g. with `site_files()` and `Card`) actually correct?**
  _`BuildInput` has 26 INFERRED edges - model-reasoned connections that need verification._
- **Should `Index schema tests` be split into smaller, more focused modules?**
  _Cohesion score 0.05827067669172932 - nodes in this community are weakly interconnected._
"""The skill folder and llms.txt: SKILL.md, one reference file per level, the draft and pack references, and the level indexes."""
import json
import re
from dataclasses import dataclass

from card_fields import backers, concerns, context, group_by_context, is_core, is_stable, lacks, level_of
from config import (
    BASE,
    INDEX_BUDGET,
    LLMS_BUDGET,
    REPO,
    SKILL_BODY_BUDGET,
    SKILL_BUDGET,
    SKILL_NAME,
)
from context import BuildInput, pack_name
from errors import BuildError
from guides import GUIDES
from markdown import rule
from models import CONCERNS, LEVELS, Card, IndexPart, Level, Twin
from prose import (
    AUDIT_DESC,
    AUDIT_MD,
    AUDIT_SECTION,
    DATA_RULE,
    DEPTH_RULE,
    DEPTH_TABLE,
    DESIGN_NOTE,
    DIFF_RULE,
    DRAFT_NOTE,
    DRAFT_RULE,
    EMPTY_MARK,
    EMPTY_RULE,
    EXAMPLE,
    GOTCHAS,
    INCIDENT_EXAMPLE,
    INCIDENT_RULE,
    LEVEL_DESC,
    LLMS_HEAD,
    LLMS_HEAD_MAX,
    LLMS_IMPERATIVE,
    NAME,
    NOTES_RULE,
    OVERLAP_RULE,
    READ_RULE,
    REPORT_RULE,
    ROUTES,
    SCOPE_GREP,
    SKILL_DESC,
    TRIAGE,
    VERDICT,
)

DRAFT_LINK = "[the draft cards](https://goodcodereview.com/.well-known/agent-skills/good-code-review/references/drafts.md)"
SKILL_VERSION = "1.0"
CANONICAL_LICENCE = "CC-BY-4.0 for the content, MIT for the code"
COMPATIBILITY = "Reads Markdown only. Needs a file-read tool and, to triage, grep. An audit may also run read-only commands, such as gh api, to quote platform settings as evidence."


@dataclass(frozen=True, slots=True)
class SkillOutput:
    """The skill folder as files (paths relative to skills/good-code-review), plus what the site writers reuse."""

    files: dict[str, str]
    level_index: dict[Level, list[IndexPart]]
    level_twins: dict[str, Twin]
    llms: str
    llms_drafts: str
    plain_verdict: str
    stable_home: dict[str, str]
    level_chars: dict[str, int]  # characters in each level's whole-file Markdown


def plain_verdict() -> str:
    """The verdict text with the HTML code tags turned into backticks."""
    return VERDICT.replace("<code>", "`").replace("</code>", "`")


def _json(t: str) -> str:
    """A JSON string is a valid YAML scalar; a plain one breaks on ": " inside it."""
    return json.dumps(t, ensure_ascii=False)


def _context_line(card: Card) -> str:
    return "context: " + ", ".join(context(card)) + "  \n" if context(card) else ""


def index_line(card: Card) -> str:
    ctx = f" <{','.join(context(card))}>" if context(card) else ""
    return f"- `{card.fm['id']}` [{card.fm['severity']}] {{{', '.join(concerns(card))}}}{ctx}: {rule(card.body)}"


def card_ranges(text: str, ids: list[str]) -> dict[str, tuple[int, int]]:
    """Map each card id to (first line, line count) of its `## <id>` section in a reference file. Lines count from 1, so a reader can pass them as offset and limit."""
    lines = text.split("\n")
    starts: list[int] = []
    at = 0
    for i in ids:
        at = lines.index(f"## {i}", at)
        starts.append(at)
        at += 1
    ends = starts[1:] + [len(lines)]
    return {i: (a + 1, len("\n".join(lines[a:b]).rstrip("\n").split("\n"))) for i, a, b in zip(ids, starts, ends, strict=True)}


def ranged_line(card: Card, where: tuple[int, int], file: str = "") -> str:
    """An index line that carries the card's place in its reference file, as `<file>:L<first>+<count>`."""
    ctx = f" <{','.join(context(card))}>" if context(card) else ""
    return f"- `{card.fm['id']}` [{card.fm['severity']}] {{{', '.join(concerns(card))}}}{ctx} {file}L{where[0]}+{where[1]}: {rule(card.body)}"


def draft_line(card: Card) -> str:
    draft_lack = lacks(card)
    return index_line(card) + f" {backers(card)}" + (f" Lacks ({draft_lack.reason}): {draft_lack.note}" if draft_lack else "")


def _gate_line(card: Card) -> str:
    gate = card.fm.get("tool_gate", "none")
    return f"tool gate: {gate}  \n" if gate and gate != "none" else ""


def card_section(card: Card) -> str:
    fm = card.fm
    return (f"## {fm['id']}\n\nseverity: {fm['severity']}  \nconcerns: {', '.join(concerns(card))}  \napplies_when: {fm['applies_when']}  \n"
            f"{_context_line(card)}{_gate_line(card)}{backers(card)}\n\n{card.body.strip()}")


def draft_section(card: Card) -> str:
    fm = card.fm
    return (f"## {fm['id']}\n\nlevel: {fm['level']}  \nseverity: {fm['severity']}  \nconcerns: {', '.join(concerns(card))}  \napplies_when: {fm['applies_when']}  \n"
            f"{_context_line(card)}lacks: {fm.get('lacks', '')}\n\n{rule(card.body)}")


def _frontmatter() -> list[str]:
    return ["---", f"name: {SKILL_NAME}", f"description: {_json(SKILL_DESC)}",
            f"license: {_json(CANONICAL_LICENCE)}", f"compatibility: {_json(COMPATIBILITY)}",
            "metadata:", f"  author: {_json('Pablo Jesús González Rubio')}", f'  version: "{SKILL_VERSION}"', "---"]


def _head(empty: list[Level]) -> list[str]:
    head = ["# Good Code Review", "", "## Routing", "", "| Input | Entry point |", "|---|---|"]
    head += [f"| {r.input} | {r.level}{f' ({EMPTY_MARK})' if r.level in empty else ''} |" for r in ROUTES]
    head += ["", DIFF_RULE, "", INCIDENT_RULE, ""] + ([EMPTY_RULE, ""] if empty else [])
    head += ["## Verdict format", ""] + plain_verdict().replace(". ", ".\n").split("\n")
    head += ["", REPORT_RULE, "", OVERLAP_RULE, "", READ_RULE, "", DATA_RULE, "", "```", EXAMPLE, "```", "", DRAFT_RULE, NOTES_RULE, "", DESIGN_NOTE, ""] + AUDIT_SECTION
    return head


@dataclass(frozen=True, slots=True)
class SkillMd:
    """SKILL.md as lines and its head."""

    lines: list[str]
    head: list[str]


_SCOPE = ["## Scope by concern", "",
          "Each card lists its concerns: " + ", ".join(f"`{c}`" for c in CONCERNS) + ".",
          "To review only some concerns, such as a performance-only review, check only the cards that list them, leave the rest out of the ledger, and name the concerns in the verdict line."]


def _skill_scope() -> list[str]:
    """The Depth and Scope by concern sections of SKILL.md."""
    return ["## Depth", "", *DEPTH_TABLE, "", DEPTH_RULE, "", *_SCOPE, SCOPE_GREP, ""]


def _skill_md(b: BuildInput, empty: list[Level]) -> SkillMd:
    """SKILL.md as lines and its head."""
    head = _head(empty)
    pointers = ["The card text is in `references/<level>.md`, and each level has an index, `references/index-<level>.md`, with one line per card and its place `L<first>+<count>` in that file. "
                "Read the lines of the cards that apply, with offset `<first>` and limit `<count>`, and not the whole file. "
                "A review of some concerns starts from `references/concern-<concern>.md`, which lists that concern's cards across levels as `<level>.md:L<first>+<count>`. "
                "For Python code, the stable `py-` cards sit in the level indexes, and `references/pack-<lang>.md` holds the drafts of a language pack.",
                TRIAGE,
                "Draft cards (not vetted; findings go under Draft findings) are in `references/drafts.md`" + "".join(f", and the {pack_name(pk)} pack in `references/pack-{pk}.md`" for pk in b.packs)
                + ". Triage them with the same `grep`. Read the linked files as raw text: a fetch tool that summarises a page drops cards.",
                f"Glossary: {BASE}/glossary.md", ""]
    lines = _frontmatter() + [""] + head + pointers + ["## Gotchas", ""] + GOTCHAS + [""] + _skill_scope()
    return SkillMd(lines, head)


def _check_routes(by_level: dict[Level, list[Card]], ref_files: set[str], skill_text: str, stable_ids: set[str]) -> list[str]:
    """Return an error per routed level whose stable cards, reference file, or empty-level text disagree."""
    errs = []
    for route in ROUTES:
        lv = route.level
        marked = f"| {lv} ({EMPTY_MARK}) |" in skill_text
        if by_level[lv] and f"references/{lv}.md" not in ref_files:
            errs.append(f"routed level '{lv}' has stable cards but no references/{lv}.md")
        if by_level[lv] and marked:
            errs.append(f"routed level '{lv}' has stable cards but is marked '{EMPTY_MARK}'")
        if not by_level[lv] and not (marked and EMPTY_RULE in skill_text):
            errs.append(f"routed level '{lv}' has no stable cards and the routing text lacks the empty-level rule")
    if DIFF_RULE not in skill_text:
        errs.append("the routing text lacks the diff rule")
    if INCIDENT_RULE not in skill_text:
        errs.append("the routing text lacks the incident rule")
    named = re.findall(r"^(?:FAIL \[[a-z-]+\]|PASS|N/A) ([a-z0-9-]+)", EXAMPLE + "\n" + INCIDENT_EXAMPLE, re.M)
    errs += [f"EXAMPLE names '{i}', which is not a stable card" for i in named if i not in stable_ids]
    return errs


# The site's .md twin of an index adds YAML frontmatter (title, description, canonical, updated), about 200 characters.
# The budget counts the served file, so leave room for it.
TWIN_FRONT = 300


def _level_index(level: Level, cards: list[Card]) -> list[IndexPart]:
    """The index of a level: one file, or one per `context` when it would pass INDEX_BUDGET."""
    parts = {g: [index_line(c) for c in cs] for g, cs in group_by_context(cards).items()}  # context group -> card lines
    whole = (f"# {NAME[level]} index\n\nOne line per stable {level} card: id, severity, concerns, context, rule. "
             f"The full card is at {BASE}/{level}.md#<id>.\n\n" + "\n".join(line for lines in parts.values() for line in lines) + "\n")
    if len(whole) + TWIN_FRONT <= INDEX_BUDGET:
        return [IndexPart(f"{level}-index", f"{NAME[level]} index", whole, len(cards))]
    split = [
        IndexPart(
            f"{level}-index-{g}", f"{NAME[level]} index, {g}",
            f"# {NAME[level]} index, {g}\n\nOne line per stable {level} card for the `{g}` context. The full card is at {BASE}/{level}.md#<id>.\n\n"
            + "\n".join(lines) + "\n", len(lines))
        for g, lines in parts.items()
    ]
    if any(len(p.text) + TWIN_FRONT > INDEX_BUDGET for p in split):
        raise BuildError(f"{level}: a context group is over {INDEX_BUDGET} characters of index; add a context or split the level")
    # Progressive disclosure: llms.txt links only this hub, so it stays one line per level however many parts there are.
    hub = (f"# {NAME[level]} index\n\nThe {level} index is split by `context`; read the part that matches the code under review "
           f"(`any` holds cards that apply to every context). The full card is at {BASE}/{level}.md#<id>.\n\n"
           + "\n".join(f"- [{p.title}]({BASE}/{p.slug}.md): {p.count} stable card{'s' if p.count != 1 else ''}." for p in split) + "\n")
    return [IndexPart(f"{level}-index", f"{NAME[level]} index", hub, len(cards))] + split


def link_stable(text: str, home: dict[str, str]) -> str:
    """A stable card links only to another stable card, as a relative path inside references/. Any other target is plain text."""
    return re.sub(r"\[\[([^\]]+)\]\]", lambda m: f"[{m[1]}]({home[m[1]]}.md#{m[1]})" if m[1] in home else m[1], text)


def _llms(level_index: dict[Level, list[IndexPart]], b: BuildInput, chars: dict[str, int]) -> str:
    """Return llms.txt, which follows https://llmstxt.org/.

    A hand-written head (LLMS_HEAD, nothing copied from SKILL.md), then H2 file lists of `[name](url): notes` links, with secondary links under "Optional".
    tools/agent_ready_check.py checks the shape. Drafts live in llms-drafts.txt, never mixed in.
    """
    out = [LLMS_HEAD]
    for lv in LEVELS:
        if lv not in level_index:
            continue
        out += [f"## {lv}", ""]
        part = level_index[lv][0]  # the whole index, or the hub that links its context parts
        n = f"{part.count} stable card{'s' if part.count != 1 else ''}"
        if lv in b.split:  # read the parts; the whole file is the fallback for a reader that can download it (docs/research/context-splitting.md)
            first, *rest = b.parts(lv)
            core = sum(is_stable(c) for cs in b.parts(lv).values() for c in cs)
            extra = f" ({part.count - core} language-pack cards are on the pack pages)" if part.count > core else ""
            out.append(f"- [{NAME[lv]}, part 1 of {1 + len(rest)}: {first}]({BASE}/{lv}-{first}.md): {core} stable cards with examples{extra}, in {1 + len(rest)} parts; read every part. The others: "
                       + ", ".join(f"[{c}]({BASE}/{lv}-{c}.md)" for c in rest) + ".")
            out.append(f"- [{NAME[lv]}, whole file]({BASE}/{lv}.md): all {n} in one file of about {chars[lv] // 1000}K characters; a fetch tool may truncate it; use it only if you can download it.")
            out.append(f"- [{NAME[lv]} index]({BASE}/{part.slug}.md): one line per card, with a link to each part.")
        else:
            out.append(f"- [{NAME[lv]}]({BASE}/{lv}.md): {n} with FAIL and PASS examples and who backs them; [one-line index]({BASE}/{part.slug}.md).")
        out.append("")
    out += ["## Audit", "", f"- [Audit a repo, service, or release]({BASE}/audit.md): scope, read order, missing controls, accepted risk, and the report shape.", ""]
    out += ["## Glossary", "", f"- [Glossary]({BASE}/glossary.md): terms the cards link to.", "",
            "## Optional", "",
            f"- [Guides]({BASE}/guides.md): " + ", ".join(f"[{g.title.lower()}]({BASE}/guides/{g.slug}.md)" for g in GUIDES) + ".",
            f"- [Concerns]({BASE}/concerns.md): stable cards grouped by concern. [Home]({BASE}/): choose a review level.",
            "- [Language packs](" + f"{BASE}/pack-{b.packs[0]}.md): " + ", ".join(f"[{pk}]({BASE}/pack-{pk}.md)" for pk in b.packs) + ".",
            f"- [llms-full.txt]({BASE}/llms-full.txt): levels, audit, glossary, guides in one file.",
            f"- [Draft cards]({BASE}/llms-drafts.txt): not vetted. {DRAFT_RULE}",
            f"- [About]({BASE}/about.md): who makes this and under which licence.",
            f"- [Privacy]({BASE}/privacy.md): the site collects nothing.",
            f"- [Drafts by what they lack]({BASE}/drafts.md): every draft grouped by what keeps it from stable.",
            f"- [Sitemap]({BASE}/sitemap.xml): every page.",
            f"- [cards.json]({BASE}/cards.json): every stable card as JSON; the shape is in [cards.schema.json]({BASE}/cards.schema.json).",
            f"- [cards-index.json]({BASE}/cards-index.json): every stable card in slim form; schema in [cards-index.schema.json]({BASE}/cards-index.schema.json).",
            f"- [Agent Skills index]({BASE}/.well-known/agent-skills/index.json): the skill, with its sha256 digest.",
            f"- [agent.json]({BASE}/agent.json): every endpoint, including the per-level and per-concern card JSON and Markdown, and authentication (none); the same file answers `/?mode=agent`.",
            f"- [ARD manifest]({BASE}/.well-known/ard.json): Agentic Resource Discovery entries.",
            f"- [AGENTS.md]({REPO}/blob/main/AGENTS.md): how to review code with this repo and how to contribute a card.",
            f"- [Skill folder]({REPO}/tree/main/skills/good-code-review): `SKILL.md` and `references/` in the repository.",
            f"- [Contact]({REPO}/issues): GitHub Issues.", ""]
    return "\n".join(out)


def _llms_drafts(b: BuildInput) -> str:
    wk_refs = f"{BASE}/.well-known/agent-skills/{SKILL_NAME}/references"  # the draft and pack text, raw Markdown, served with the skill

    def url(card: Card) -> str:
        return f"{wk_refs}/pack-{card.fm['lang']}.md" if not is_core(card) else f"{wk_refs}/drafts.md"

    out = ["# Draft cards", "", f"Not vetted. {DRAFT_RULE} Report a `FAIL` of one under Draft findings, capped at `should-fix`, never as `PASS`.", ""]
    for lv in LEVELS:
        cs = [c for c in b.draft if level_of(c) == lv and is_core(c)]
        if cs:
            out += [f"## {lv}", "", f"Full text: {url(cs[0])}", ""] + [draft_line(c) for c in cs] + [""]
    for pk in b.packs:
        cs = [c for c in b.draft if c.fm["lang"] == pk]
        out += [f"## pack {pk}", "", f"Full text: {url(cs[0])}", ""] + [draft_line(c) for c in cs] + [""]
    return "\n".join(out)


def _draft_files(b: BuildInput) -> dict[str, str]:
    """The draft and pack cards ship inside the skill as compact references, so a review never depends on fetching pages."""
    core_drafts = [c for c in b.draft if is_core(c)]
    levels = [lv for lv in LEVELS if any(level_of(c) == lv for c in core_drafts)]
    files = {"references/drafts.md": "# Draft cards\n\n" + DRAFT_NOTE + " A draft `change`, `incident`, or `production` card applies only to a diff, an incident, or a release.\n\n"
             + "\n\n".join(f"# {lv} drafts\n\n" + "\n\n".join(draft_section(c) for c in core_drafts if level_of(c) == lv) for lv in levels) + "\n"}
    for pk in b.packs:
        files[f"references/pack-{pk}.md"] = (f"# {pack_name(pk)} pack\n\nDraft cards only; the stable {pack_name(pk)} cards are in the level files. {DRAFT_NOTE}\n\n"
                                            + "\n\n".join(draft_section(c) for c in b.cards if c.fm["lang"] == pk and not is_stable(c)) + "\n")
    return files


def skill_output(b: BuildInput) -> SkillOutput:
    """Build every file of the skill folder and llms.txt in memory. Raises BuildError when a budget or a consistency check fails."""
    stable = b.stable
    by_level = {lv: [c for c in stable if level_of(c) == lv] for lv in LEVELS}
    empty = [r.level for r in ROUTES if not by_level[r.level]]
    home = {c.fm["id"]: c.fm["level"] for c in stable}
    plain = plain_verdict()
    files: dict[str, str] = {}
    level_index: dict[Level, list[IndexPart]] = {}
    twins: dict[str, Twin] = {}
    ranges: dict[Level, dict[str, tuple[int, int]]] = {}
    for lv in LEVELS:
        cards = by_level[lv]
        if not cards:
            twins[lv] = Twin(NAME[lv], LEVEL_DESC[lv], f"# {lv}\n\nNo vetted cards for this level yet. It gives no verdict.\n")
            continue
        level_index[lv] = _level_index(lv, cards)
        ref = link_stable(f"# {lv}\n\n" + "\n\n".join(card_section(c) for c in cards) + "\n", home)
        files[f"references/{lv}.md"] = ref
        ranges[lv] = card_ranges(ref, [c.fm["id"] for c in cards])
        files[f"references/index-{lv}.md"] = (f"# {NAME[lv]} index\n\nOne line per stable {lv} card: id, severity, concerns, context, place, rule. The place `L<first>+<count>` is the card's "
                                              f"lines in `{lv}.md`: read them with offset `<first>` and limit `<count>`.\n\n"
                                              + "\n".join(ranged_line(c, ranges[lv][c.fm["id"]]) for c in cards) + "\n")
        twins[lv] = Twin(NAME[lv], LEVEL_DESC[lv], ref)
    if "incident" in twins:
        t = twins["incident"]
        twins["incident"] = Twin(t.title, t.description, t.markdown.replace("# incident\n\n", f"# incident\n\n{INCIDENT_RULE}\n\n", 1))
    skill_md = _skill_md(b, empty)
    skill_lines = skill_md.lines
    skill_text = "\n".join(skill_lines)
    bad = _check_routes(by_level, set(files), skill_text, set(home))
    if bad:
        raise BuildError("\n".join(bad))
    if len(skill_lines) > SKILL_BUDGET:
        raise BuildError(f"SKILL.md is {len(skill_lines)} lines, budget {SKILL_BUDGET}")
    body_chars = len(skill_text.split("\n---\n", 1)[1])
    if body_chars > SKILL_BODY_BUDGET:
        raise BuildError(f"SKILL.md body is {body_chars} characters, budget {SKILL_BODY_BUDGET}: move detail into references/")
    files["SKILL.md"] = skill_text
    files["references/audit.md"] = "# Audit a repo, service, or release\n\n" + AUDIT_MD.replace(DRAFT_LINK, "`drafts.md`")
    level_chars = {lv: len(t.markdown) for lv, t in twins.items()}
    llms = _llms(level_index, b, level_chars)
    llms_drafts = _llms_drafts(b)
    _check_indexes(b, level_index, home, llms, llms_drafts)
    files.update(_draft_files(b))
    files.update(_concern_indexes(by_level, ranges))
    files["references/index-drafts.md"] = _drafts_index(b, files["references/drafts.md"])
    return SkillOutput(files, level_index, twins, llms, llms_drafts, plain, home, level_chars)


def _concern_indexes(by_level: dict[Level, list[Card]], ranges: dict[Level, dict[str, tuple[int, int]]]) -> dict[str, str]:
    """One index per concern, across levels: a concern-only review reads this and then only the cards it lists. The card text stays in the level files."""
    out = {}
    for concern in CONCERNS:
        body = []
        for lv in LEVELS:
            cs = [c for c in by_level[lv] if concern in concerns(c)]
            if cs:
                body += [f"## {lv}", ""] + [ranged_line(c, ranges[lv][c.fm["id"]], f"{lv}.md:") for c in cs] + [""]
        if body:
            out[f"references/concern-{concern}.md"] = (f"# {concern} cards\n\nEvery stable card that lists the `{concern}` concern, by level. The place `<level>.md:L<first>+<count>` is the card's "
                                                      f"lines: read them with offset `<first>` and limit `<count>`.\n\n" + "\n".join(body))
    return out


def _drafts_index(b: BuildInput, drafts_text: str) -> str:
    """The draft cards that sit in drafts.md, with their lines there. The language packs are short, so they have no index."""
    core = [c for c in b.draft if is_core(c)]
    where = {}
    for lv in LEVELS:
        ids = [c.fm["id"] for c in core if level_of(c) == lv]
        sect = drafts_text.split(f"# {lv} drafts\n", 1)
        if ids and len(sect) == 2:
            offset = sect[0].count("\n") + 1  # lines before this level's section
            local = card_ranges("\n" * 0 + sect[1].split("\n# ", 1)[0], ids)
            where.update({i: (a + offset, n) for i, (a, n) in local.items()})
    lines = [f"- `{c.fm['id']}` [{c.fm['severity']}] {{{', '.join(concerns(c))}}} L{where[c.fm['id']][0]}+{where[c.fm['id']][1]}: {rule(c.body)}" for c in core]
    return ("# Draft index\n\nOne line per draft card in `drafts.md`: id, severity, concerns, place, rule. Draft cards are not vetted. The place `L<first>+<count>` is the card's lines "
            "in `drafts.md`.\n\n" + "\n".join(lines) + "\n")


def _check_indexes(b: BuildInput, level_index: dict[Level, list[IndexPart]], home: dict[str, str], llms: str, llms_drafts: str) -> None:
    def ids_in(text: str) -> list[str]:
        return re.findall(r"^- `([^`]+)` \[", text, re.M)

    indexed = [i for lv in LEVELS for part in level_index.get(lv, []) for i in ids_in(part.text)]
    draft_ids = {c.fm["id"] for c in b.draft}
    if sorted(indexed) != sorted(home) or draft_ids & set(indexed):
        raise BuildError("level indexes: stable ids differ from the stable cards, or a draft id sits in one")
    head = llms.split("\n## ", 1)[0]
    if len(head) > LLMS_HEAD_MAX or re.search(LLMS_IMPERATIVE, head):
        raise BuildError(f"llms.txt head is {len(head)} characters (max {LLMS_HEAD_MAX}) or holds a directive; it describes the site and shares nothing with SKILL.md")
    if len(llms) > LLMS_BUDGET:
        raise BuildError(f"llms.txt is {len(llms)} characters, budget {LLMS_BUDGET}: it holds routing and links; move detail behind a link")
    if sorted(ids_in(llms_drafts)) != sorted(draft_ids):
        raise BuildError("llms-drafts.txt: ids differ from the draft cards")


def audit_twin() -> Twin:
    return Twin("Audit a repo, service, or release", AUDIT_DESC, "# Audit a repo, service, or release\n\n" + AUDIT_MD)


"""A small Markdown renderer for the card, glossary, and page sources, and the readers for a card's sections."""
import html
import re
from pathlib import Path

# Markdown features md() cannot render. The build fails if a source file uses one outside a code fence.
UNSUPPORTED = {"numbered list": r"\s*\d+[.)] ", "table": r"\s*\|", "quote": r"\s*>", "nested bullet": r"\s{2,}[-*] ", "rule": r"-{3,}\s*$"}
UNSUPPORTED_PREVIEW = 50  # characters of the offending line shown in an error
CODE_PLACEHOLDER = "\0{}\0"  # stands in for an inline code span while the other inline rules run


def check_md(path: Path | str, text: str) -> list[str]:
    """Return an error per source line md() would render wrongly."""
    prose = re.sub(r"^```[^\n]*\n.*?^```[ \t]*$", "", text, flags=re.S | re.M)
    errors = [
        f"{path}: unsupported markdown ({kind}): {line.strip()[:UNSUPPORTED_PREVIEW]}"
        for line in prose.split("\n")
        for kind, pattern in UNSUPPORTED.items()
        if re.match(pattern, line)
    ]
    errors += [
        f"{path}: heading with text on the next line: {block.strip()[:UNSUPPORTED_PREVIEW]}"
        for block in re.split(r"\n\s*\n", prose)
        if re.match(r"#+ ", block) and "\n" in block.strip()
    ]
    return errors


def inline(s: str, ids: dict[str, str]) -> str:
    """Render the inline Markdown of one paragraph: code, bold, italic, links, and [[card-id]] cross-references."""
    s = html.escape(s)
    codes: list[str] = []

    def stash(m: re.Match[str]) -> str:
        codes.append(m.group(1))
        return CODE_PLACEHOLDER.format(len(codes) - 1)

    s = re.sub(r"`([^`]+)`", stash, s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<![*\w])\*(?!\s)([^*\n]+?)(?<!\s)\*(?![*\w])", r"<em>\1</em>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    s = re.sub(r"\[\[([^\]]+)\]\]", lambda m: f'<a href="{ids.get(m.group(1), "#")}">{m.group(1)}</a>', s)
    return re.sub(r"\0(\d+)\0", lambda m: f"<code>{codes[int(m.group(1))]}</code>", s)


def _figure_pattern(cls: str) -> str:
    return rf'(<figure class="{cls}">(?:(?!</figure>).)*</figure>)'


def md(text: str, ids: dict[str, str]) -> str:
    """Render the Markdown subset the sources use. A FAIL and a PASS block that follow each other become one `.ex` pair."""
    out: list[str] = []
    mark = ""
    lang = ""
    for i, part in enumerate(re.split(r"^```([^\n]*)\n(.*?)^```[ \t]*$", text, flags=re.S | re.M)):
        if i % 3 == 1:
            lang = part.strip()
            continue
        if i % 3 == 2:
            cls = f' class="language-{html.escape(lang)}"' if lang else ""
            pre = f"<pre><code{cls}>{html.escape(part)}</code></pre>"
            caption = inline(f"**{mark.upper()}**", ids)
            out.append(f'<figure class="{mark}"><figcaption>{caption}</figcaption>{pre}</figure>' if mark else pre)
            mark = ""
            continue
        for blk in re.split(r"\n\s*\n", part.strip()):
            lines = blk.split("\n")
            if not blk.strip():
                continue
            if all(re.match(r"\s*[-*] ", line) for line in lines):
                items = "".join("<li>" + inline(re.sub(r"^\s*[-*] ", "", line), ids) + "</li>" for line in lines)
                out.append(f"<ul>{items}</ul>")
            elif m := re.match(r"(#+) (.*)", blk):
                out.append(f"<h{len(m[1]) + 1}>{inline(m[2], ids)}</h{len(m[1]) + 1}>")
            elif blk.strip() in ("**FAIL**", "**PASS**"):
                mark = blk.strip()[2:-2].lower()
            else:
                out.append(f"<p>{inline(' '.join(lines), ids)}</p>")
    return re.sub(_figure_pattern("fail") + "\n" + _figure_pattern("pass"), r'<div class="ex">\1\2</div>', "\n".join(out), flags=re.S)


def section(body: str, label: str) -> str:
    """The first paragraph after `**<label>.**` in a card body, on one line; empty when the card has none."""
    m = re.search(rf"\*\*{label}\.\*\*\s*(.*?)(?:\n\s*\n|$)", body, re.S)
    return " ".join(m.group(1).split()) if m else ""


def rule(body: str) -> str:
    """A card's one-sentence Rule."""
    return section(body, "Rule")
